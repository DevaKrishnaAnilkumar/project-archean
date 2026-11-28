// Reuse the locked C08 foraging kernel and seed streams without altering it.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main c08_entry_point
#include "../c08_heritable_learning/model.cpp"
#undef main
#pragma GCC diagnostic pop

namespace c09 {
constexpr Stream donor_stream=static_cast<Stream>(13);
#pragma pack(push,1)
struct Birth {
    uint16_t t,id,parent,donor;
    uint8_t allele;
    uint8_t transfer;
    double donor_belief,child_belief;
};
#pragma pack(pop)
static_assert(sizeof(Birth)==26);

uint8_t retention(uint8_t allele,RNG rng) {
    if (rng.unit()>=.02) return allele;
    return (allele+1+rng.index(2))%3;
}

void neutral(const fs::path& path,const std::vector<Event>& events,
             const std::vector<uint8_t>& founders_gt,int seed,int index) {
    std::vector<uint16_t> alive(founders);
    std::iota(alive.begin(),alive.end(),0);
    auto genotypes=founders_gt;
    auto parents=stream(seed,passive_parent,0,index);
    auto deaths=stream(seed,passive_death,0,index);
    auto muts=stream(seed,passive_mutation,0,index);
    std::vector<Passive> ledger;
    for (const auto& event : events) {
        if (event.parent==UINT16_MAX) {
            auto at=deaths.index(alive.size());
            auto id=alive[at];
            ledger.push_back({id,UINT16_MAX,genotypes[id]});
            alive[at]=alive.back();
            alive.pop_back();
        } else {
            auto parent=alive[parents.index(alive.size())];
            auto id=static_cast<uint16_t>(genotypes.size());
            auto gt=retention(genotypes[parent],{muts.next()});
            genotypes.push_back(gt);
            alive.push_back(id);
            ledger.push_back({id,parent,gt});
        }
    }
    save(path/("passive"+std::to_string(index)+".bin"),ledger);
}

void world(const fs::path& path,int seed,Setting c,int population) {
    fs::create_directories(path);
    std::vector<uint8_t> genesis(founders);
    for (int i=0;i<founders;++i) genesis[i]=population==0 ? 0 : population==1 ? 2 : i/20;
    shuffle(genesis,stream(seed,founder));
    auto genotypes=genesis;
    std::vector<Agent> living;
    living.reserve(capacity);
    for (int i=0;i<founders;++i) living.push_back({uint16_t(i),5,384,.5});
    std::vector<Step> actions;
    actions.reserve(periods*capacity);
    std::vector<Event> events;
    std::vector<Birth> births;
    std::vector<uint8_t> schedule;
    auto maps=stream(seed,mapping);
    const int initial=maps.index(2);
    for (int t=0;t<periods;++t) {
        const int random_map=maps.index(2);
        int m=initial;
        if (c.regime==1) m^=(t/24)%2;
        if (c.regime==2) m=random_map;
        schedule.push_back(m);
        for (auto& agent : living) {
            actions.push_back(forage(agent,{c.regime,c.fee,c.prize,0,c.q},seed,t,m,-1));
            if (!agent.energy) events.push_back({uint16_t(t),agent.id,UINT16_MAX,genotypes[agent.id]});
        }
        std::erase_if(living,[](const Agent& a){return a.energy==0;});
        if (living.size()==capacity) continue;
        const auto adult_count=living.size();
        std::vector<unsigned> eligible;
        for (unsigned i=0;i<adult_count;++i) if (living[i].energy>=512) eligible.push_back(i);
        shuffle(eligible,stream(seed,reproduction,t));
        for (unsigned i : eligible) {
            if (living.size()==capacity) break;
            auto& parent=living[i];
            auto id=static_cast<uint16_t>(genotypes.size());
            auto allele=genotypes[parent.id];
            if (population>=2) allele=retention(allele,stream(seed,mutation,id));
            uint16_t donor=parent.id;
            double belief=parent.belief;
            if (population==3) {
                if (adult_count>1) {
                    auto j=stream(seed,donor_stream,id).index(adult_count-1);
                    if (j>=i) ++j;
                    donor=living[j].id;
                    belief=living[j].belief;
                } else {
                    donor=UINT16_MAX;
                    belief=.5;
                }
            }
            double inherited=.5+allele*.5*(belief-.5);
            uint8_t transfer=c.overhead*allele/2;
            parent.energy-=208+transfer;
            events.push_back({uint16_t(t),id,parent.id,allele});
            births.push_back({uint16_t(t),id,parent.id,donor,allele,transfer,belief,inherited});
            genotypes.push_back(allele);
            living.push_back({id,5,192,inherited});
        }
    }
    save(path/"founders.bin",genesis);
    save(path/"mapping.bin",schedule);
    save(path/"actions.bin",actions);
    save(path/"events.bin",events);
    save(path/"births.bin",births);
    if (population==2) for (int i=0;i<replays;++i) neutral(path,events,genesis,seed,i);
}
}

int main(int argc,char** argv) {
    if (argc!=3) return 2;
    const std::string mode=argv[1];
    if (mode!="smoke" && mode!="eval") return 2;
    const fs::path root=argv[2];
    if (fs::exists(root)) throw std::runtime_error("Output already exists");
    fs::create_directories(root);
    std::vector<Setting> design;
    for (int r : {0,1,2}) for (int prize : {128,192}) for (int transfer : {0,16})
        design.push_back({r,5,prize,transfer,.85});
    design.insert(design.end(),{{0,40,128,0,.85},{0,5,192,0,.5},{0,5,192,16,.5}});
    std::ofstream manifest(root/"design.csv");
    manifest<<"setting,regime,fee_ticks,reward_ticks,transfer_ticks,q,seed,population,path\n";
    const int first=mode=="smoke" ? 3690 : 3700;
    const int last=mode=="smoke" ? 3691 : 3719;
    for (unsigned s=0;s<design.size();++s) {
        auto c=design[s];
        for (int seed=first;seed<=last;++seed) for (int pop=0;pop<4;++pop) {
            std::string path=std::to_string(s)+"_"+std::to_string(seed)+"_"+std::to_string(pop);
            c09::world(root/path,seed,c,pop);
            manifest<<s<<','<<c.regime<<','<<c.fee<<','<<c.prize<<','<<c.overhead<<','
                    <<c.q<<','<<seed<<','<<pop<<','<<path<<'\n';
        }
    }
    if (!manifest) return 1;
}
