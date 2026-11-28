#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;
constexpr int periods = 240, capacity = 120, founders = 60, replays = 8;
enum Stream : uint64_t { mapping=1, founder, resource, observation, reward,
    propensity, tie, mutation, reproduction, passive_parent, passive_death, passive_mutation };

uint64_t mix(uint64_t x) {
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}
struct RNG {
    uint64_t state;
    uint64_t next() { state += 0x9e3779b97f4a7c15ULL; return mix(state); }
    double unit() { return (next() >> 11) * 0x1.0p-53; }
    unsigned index(unsigned n) {
        uint64_t cutoff = (uint64_t(0) - n) % n;
        uint64_t v = next();
        while (v < cutoff) v = next();
        return v % n;
    }
};
RNG stream(int seed, Stream name, uint64_t opportunity=0, uint64_t replicate=0) {
    return {mix(uint64_t(seed)) ^ mix(uint64_t(name) + 0x7fa56e1ULL) ^
        mix(opportunity + 0x8b89e11ULL) ^ mix(replicate + 0x50ab921ULL)};
}
template<class T> void shuffle(std::vector<T>& values, RNG rng) {
    for (unsigned i = values.size(); i > 1; --i)
        std::swap(values[i-1], values[rng.index(i)]);
}

struct Setting { int regime, fee, prize, overhead; double q; };
std::vector<Setting> settings() {
    std::vector<Setting> out;
    for (int r : {0,1,2}) for (int fee : {5,20,40})
        for (int prize : {128,192}) for (int overhead : {0,2})
            out.push_back({r,fee,prize,overhead,.85});
    for (int overhead : {0,2}) out.push_back({0,5,192,overhead,.5});
    for (int overhead : {0,2}) out.push_back({0,0,128,overhead,.85});
    return out;
}
struct Agent { uint16_t id; uint8_t gt; int energy; double belief; };
#pragma pack(push,1)
struct Step {
    uint16_t t, id;
    int16_t before, after;
    int8_t hidden, site, read, patch;
    uint8_t got, returns;
    double prior, belief;
};
struct Event { uint16_t t, id, parent; uint8_t genotype; }; // parent 65535 marks death
struct Passive { uint16_t id, parent; uint8_t genotype; }; // event time is in active stream
#pragma pack(pop)
static_assert(sizeof(Step)==30 && sizeof(Event)==7 && sizeof(Passive)==5);

template<class Record>
void save(const fs::path& path, const std::vector<Record>& rows) {
    std::ofstream out(path, std::ios::binary);
    out.write(reinterpret_cast<const char*>(rows.data()), rows.size()*sizeof(Record));
    if (!out) throw std::runtime_error("Writing " + path.string());
}

uint8_t inherit(uint8_t gt, RNG rng, double probability) {
    int l = gt / 3, s = gt % 3;
    if (rng.unit() < probability) l = 1-l;
    if (rng.unit() < probability) s = (s + 1 + rng.index(2)) % 3;
    return 3*l + s;
}

double feedback(double prior, int site, int cue, int patch, bool got, double q) {
    std::array<double,2> likelihood{};
    for (int m=0; m<2; ++m) {
        double correct = site==m ? q : .5;
        for (int h=0; h<2; ++h) {
            double sensed = cue==h ? correct : 1-correct;
            double rewarded = patch==h ? .85 : .15;
            likelihood[m] += .5*sensed*(got ? rewarded : 1-rewarded);
        }
    }
    return prior*likelihood[1] / ((1-prior)*likelihood[0] + prior*likelihood[1]);
}

Step forage(Agent& agent, Setting c, int seed, int t, int map, int forced_reward) {
    Step step{uint16_t(t),agent.id,int16_t(agent.energy),0,-1,-1,-1,-1,0,0,
        agent.belief,agent.belief};
    bool learns = agent.gt >= 3;
    agent.energy = std::max(0, agent.energy-16-(learns ? c.overhead : 0));
    if (!agent.energy) return step;
    if (learns) agent.belief = .05 + .9*agent.belief;
    step.prior = agent.belief;
    const uint64_t key = uint64_t(t)*65536 + agent.id;
    step.hidden = stream(seed,resource,key).index(2);
    auto ties = stream(seed,tie,key);
    const int site_tie = ties.index(2), patch_tie = ties.index(2);
    int s = agent.gt%3;
    if (agent.energy > c.fee+32 && stream(seed,propensity,key).unit() < s*.5) {
        step.site = std::abs((c.q-.5)*(2*agent.belief-1)) <= 1e-12
            ? site_tie : int(agent.belief > .5);
        double chance = step.site==map ? c.q : .5;
        step.read = stream(seed,observation,2*key+step.site).unit() < chance
            ? step.hidden : 1-step.hidden;
        for (int cost : {c.fee*2/5,c.fee/5,c.fee*2/5}) agent.energy -= cost;
    }
    if (agent.energy > 32) {
        double p = .5;
        if (step.site >= 0) {
            double accuracy = .5+(c.q-.5)*(step.site==1 ? agent.belief : 1-agent.belief);
            p = step.read ? accuracy : 1-accuracy;
        }
        step.patch = std::abs(p-.5)<=1e-12 ? patch_tie : int(p>.5);
        for (int i=0; i<4; ++i) agent.energy -= 8;
        double chance = step.patch==step.hidden ? .85 : .15;
        step.got = forced_reward < 0
            ? stream(seed,reward,2*key+step.patch).unit()<chance : forced_reward;
        agent.energy += c.prize*step.got;
        if (learns && step.site >= 0)
            agent.belief = feedback(step.prior,step.site,step.read,step.patch,step.got,c.q);
        while (step.returns<4 && agent.energy>0) {
            agent.energy = std::max(0,agent.energy-8);
            ++step.returns;
        }
    }
    step.after = agent.energy;
    step.belief = agent.belief;
    return step;
}

void replay(const std::vector<Event>& events, const std::vector<uint8_t>& genesis,
            int seed, int index, double mutation_probability, const fs::path& path) {
    std::vector<uint16_t> living(founders);
    std::iota(living.begin(), living.end(), 0);
    auto genotypes = genesis;
    auto parents = stream(seed,passive_parent,0,index);
    auto deaths = stream(seed,passive_death,0,index);
    auto muts = stream(seed,passive_mutation,0,index);
    std::vector<Passive> log;
    log.reserve(events.size());
    for (const auto& e : events) {
        if (living.empty()) throw std::runtime_error("Empty passive replay event");
        if (e.parent == UINT16_MAX) {
            auto at = deaths.index(living.size());
            auto id = living[at];
            log.push_back({id,UINT16_MAX,genotypes[id]});
            living[at] = living.back();
            living.pop_back();
        } else {
            auto parent = living[parents.index(living.size())];
            auto id = static_cast<uint16_t>(genotypes.size());
            auto genotype = inherit(genotypes[parent],{muts.next()},mutation_probability);
            genotypes.push_back(genotype);
            living.push_back(id);
            log.push_back({id,parent,genotype});
        }
    }
    save(path,log);
}

void run(const fs::path& path, int seed, Setting c, int fixture=-1) {
    fs::create_directories(path);
    std::vector<uint8_t> genesis(founders);
    for (int i=0; i<founders; ++i) genesis[i]=i/10;
    shuffle(genesis,stream(seed,founder));
    std::vector<Agent> living;
    living.reserve(capacity);
    for (int i=0; i<founders; ++i) living.push_back({uint16_t(i),genesis[i],384,.5});
    std::vector<Step> actions;
    actions.reserve(periods*capacity);
    std::vector<Event> events;
    std::vector<uint8_t> schedule;
    uint16_t next_id = founders;
    auto maps = stream(seed,mapping);
    const int initial = maps.index(2);
    const double probability = fixture == 0 ? 0 : .02;
    for (int t=0; t<periods; ++t) {
        const int random_map = maps.index(2);
        int m = initial;
        if (c.regime==1) m ^= (t/24)%2;
        if (c.regime==2) m = random_map;
        schedule.push_back(m);
        for (auto& agent : living) {
            Step record = forage(agent,c,seed,t,m,fixture==2 ? 0 : fixture==3 ? 1 : -1);
            actions.push_back(record);
            if (!agent.energy) events.push_back({uint16_t(t),agent.id,UINT16_MAX,agent.gt});
        }
        std::erase_if(living,[](const Agent& agent){ return agent.energy==0; });
        if (fixture==1 || living.size()==capacity) continue;
        std::vector<unsigned> eligible;
        for (unsigned i=0; i<living.size(); ++i)
            if (living[i].energy>=512) eligible.push_back(i);
        shuffle(eligible,stream(seed,reproduction,t));
        for (unsigned i : eligible) {
            if (living.size()==capacity) break;
            Agent& parent = living[i];
            parent.energy -= 208;
            uint8_t gt = inherit(parent.gt,stream(seed,mutation,next_id),probability);
            events.push_back({uint16_t(t),next_id,parent.id,gt});
            living.push_back({next_id++,gt,192,.5});
        }
    }
    save(path/"founders.bin",genesis);
    save(path/"mapping.bin",schedule);
    save(path/"actions.bin",actions);
    save(path/"events.bin",events);
    for (int i=0; i<replays; ++i)
        replay(events,genesis,seed,i,probability,path/("passive"+std::to_string(i)+".bin"));
}

int main(int argc, char** argv) {
    if (argc!=3) return 2;
    const std::string mode=argv[1];
    if (mode!="fixtures" && mode!="smoke" && mode!="eval") return 2;
    const fs::path root=argv[2];
    if (fs::exists(root)) throw std::runtime_error("Output already exists");
    fs::create_directories(root);
    const auto design=settings();
    std::ofstream manifest(root/"design.csv");
    manifest << "setting,regime,fee_ticks,reward_ticks,overhead_ticks,q,seed,fixture,path\n";
    auto world = [&](int id, int seed, int fixture) {
        Setting c = design[id];
        std::string path = std::to_string(id)+"_"+std::to_string(seed);
        run(root/path,seed,c,fixture);
        manifest << id << ',' << c.regime << ',' << c.fee << ',' << c.prize << ','
                 << c.overhead << ',' << c.q << ',' << seed << ',' << fixture << ',' << path << '\n';
    };
    if (mode=="fixtures") {
        for (int i=0; i<4; ++i) world(4,3500+i,i);
    } else {
        const int first=mode=="smoke" ? 3590 : 3600;
        const int last=mode=="smoke" ? 3591 : 3619;
        for (unsigned id=0; id<design.size(); ++id)
            for (int seed=first; seed<=last; ++seed) world(id,seed,-1);
    }
    if (!manifest) return 1;
}
