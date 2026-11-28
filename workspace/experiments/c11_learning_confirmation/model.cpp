// C11-A calls original C08 model verbatim. C11-B changes only founder and transmission rules.
#define main c08_original_main
#include "../c08_heritable_learning/model.cpp"
#undef main
uint8_t inherit_b(uint8_t gt, RNG rng, double p) {
    return rng.unit()<p ? uint8_t(7-gt) : gt; // 2 <-> 5; sensing invariant
}
void replay_b(const std::vector<Event>& events, const std::vector<uint8_t>& genesis,
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
            auto genotype = inherit_b(genotypes[parent],{muts.next()},mutation_probability);
            genotypes.push_back(genotype);
            living.push_back(id);
            log.push_back({id,parent,genotype});
        }
    }
    save(path,log);
}

void run_b(const fs::path& path, int seed, Setting c, int arm, int fixture=-1) {
    fs::create_directories(path);
    std::vector<uint8_t> genesis(founders);
    for (int i=0; i<founders; ++i) genesis[i]=arm==0 ? 2 : arm==1 ? 5 : i<30 ? 2 : 5;
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
    const double probability = arm==3 && fixture!=0 ? .02 : 0;
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
            uint8_t gt = inherit_b(parent.gt,stream(seed,mutation,next_id),probability);
            events.push_back({uint16_t(t),next_id,parent.id,gt});
            living.push_back({next_id++,gt,192,.5});
        }
    }
    save(path/"founders.bin",genesis);
    save(path/"mapping.bin",schedule);
    save(path/"actions.bin",actions);
    save(path/"events.bin",events);
    if (arm>=2) for (int i=0; i<replays; ++i)
        replay_b(events,genesis,seed,i,probability,path/("passive"+std::to_string(i)+".bin"));
}

int main(int argc,char** argv) {
    if(argc!=4) return 2;
    std::string study=argv[1], mode=argv[2];
    if((study!="A" && study!="B") || (mode!="smoke" && mode!="evaluation" && mode!="fixtures" && mode!="equivalence")) return 2;
    if(mode=="equivalence" && study!="A") return 2;
    const fs::path root=argv[3];
    if(fs::exists(root)) throw std::runtime_error("Output exists");
    fs::create_directories(root);
    std::ofstream manifest(root/"design.csv");
    manifest<<"study,phase,condition,seed,regime,q,fee_ticks,reward_ticks,overhead_ticks,founders,mutation_L,mutation_S,replays,fixture,path\n";
    auto emit=[&](int id,int seed,int fixture) {
        Setting c; std::string name,genesis; int arm=-1, nr=8; double ml=.02, ms=.02;
        if(study=="A") { c=settings()[id];name=id==0?"A1":id==24?"A2":id==8?"A3":"fixture";genesis="balanced-six"; if(fixture==0) ml=ms=0; }
        else { arm=id%4; c={0,5,128,0,id<4?.85:.5};name="B"+std::to_string(arm+1)+(id<4?"-informative":"-null");genesis=arm==0?"frozen":arm==1?"learning":"mixed";ml=arm==3 && fixture!=0?.02:0;ms=0;nr=arm>=2?8:0; }
        auto path=std::to_string(id)+"_"+std::to_string(seed);
        if(study=="A") run(root/path,seed,c,fixture); else run_b(root/path,seed,c,arm,fixture);
        manifest<<study<<','<<mode<<','<<name<<','<<seed<<','<<c.regime<<','<<c.q<<','<<c.fee<<','<<c.prize<<','<<c.overhead<<','<<genesis<<','<<ml<<','<<ms<<','<<nr<<','<<fixture<<','<<path<<'\n';
    };
    if(mode=="fixtures") { for(int i=0;i<4;++i) emit(study=="A"?4:3,(study=="A"?3870:3874)+i,i); }
    else {
        int first=mode=="equivalence"?3590:mode=="smoke"?(study=="A"?3890:3990):(study=="A"?3900:4000);
        int count=mode=="evaluation"?64:2;
        for(int seed=first;seed<first+count;++seed) {
            if(study=="A") for(int id:{0,24,8}) emit(id,seed,-1);
            else for(int id=0;id<8;++id) emit(id,seed,-1);
        }
    }
    if(!manifest) return 1; return 0;
}
