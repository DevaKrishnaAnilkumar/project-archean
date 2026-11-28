// C10 uses the archived C08 foraging kernel; the historical source is unchanged.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main c08_entry_point
#include "../c08_heritable_learning/model.cpp"
#undef main
#pragma GCC diagnostic pop

namespace c10 {
constexpr Stream crossover = static_cast<Stream>(14);
struct Condition { int regime=0, fee=5, prize=192, number=60, initial=384; double q=.85, mu=.02; bool balanced=false; };
std::vector<Condition> design() {
    std::vector<Condition> v(12);
    v[1].regime=1; v[2].regime=2;
    v[3].mu=0; v[4].mu=0; v[4].regime=1;
    v[5].mu=.10; v[6].mu=.10; v[6].regime=1;
    v[7].prize=128; v[8].prize=128; v[8].fee=40;
    v[9].number=12; v[9].initial=128;
    v[10].balanced=true; v[11].q=.5;
    return v;
}
#pragma pack(push,1)
struct Birth { uint16_t t,id,p1,p2; uint8_t pre,gt; uint16_t debit1,debit2; double p1belief,p2belief,child; };
struct Period { uint16_t eligible,births,unpaired,blocked; uint16_t counts[6]; };
#pragma pack(pop)
static_assert(sizeof(Birth)==38 && sizeof(Period)==20);
int memory(int arm) { return arm==0||arm==2||arm==5 ? 0 : arm==4||arm==7 ? 2 : 1; }
uint8_t combine(uint8_t a,uint8_t b,RNG rng) { const auto l=rng.index(2); const auto s=rng.index(2); return 3*(l?b/3:a/3)+(s?b%3:a%3); }
void world(const fs::path& path,Condition c,int seed,int arm) {
    const bool pair=arm>=2, recomb=arm>=5;
    fs::create_directories(path);
    std::vector<uint8_t> genesis(c.number);
    for(int i=0;i<c.number;++i) genesis[i]=c.balanced?i/(c.number/6):i<c.number/2?2:3;
    shuffle(genesis,stream(seed,founder));
    std::vector<Agent> living; living.reserve(capacity);
    for(int i=0;i<c.number;++i) living.push_back({uint16_t(i),genesis[i],c.initial,.5});
    uint16_t next_id=c.number;
    std::vector<Step> actions; actions.reserve(periods*capacity);
    std::vector<Birth> births; std::vector<Event> events; std::vector<Period> counts;
    std::vector<uint8_t> schedule;
    auto maps=stream(seed,mapping); const int initial=maps.index(2);
    for(int t=0;t<periods;++t) {
        int random_map=maps.index(2), m=initial;
        if(c.regime==1) m^=(t/24)%2;
        if(c.regime==2) m=random_map;
        schedule.push_back(m);
        for(auto& a:living) {
            actions.push_back(forage(a,{c.regime,c.fee,c.prize,0,c.q},seed,t,m,-1));
            if(!a.energy) events.push_back({uint16_t(t),a.id,UINT16_MAX,a.gt});
        }
        std::erase_if(living,[](const Agent& a){return !a.energy;});
        std::vector<unsigned> eligible;
        for(unsigned i=0;i<living.size();++i) if(living[i].energy>=512) eligible.push_back(i);
        shuffle(eligible,stream(seed,reproduction,t));
        unsigned stride=pair?2:1;
        unsigned possible=eligible.size()/stride;
        unsigned n=std::min(possible,unsigned(capacity-living.size()));
        Period p{}; p.eligible=eligible.size();p.births=n;p.unpaired=pair?eligible.size()%2:0;p.blocked=possible-n;
        for(unsigned i=0;i<n;++i) {
            auto& a=living[eligible[i*stride]];
            auto& b=living[eligible[i*stride+(pair?1:0)]];
            const uint8_t pre=recomb?combine(a.gt,b.gt,stream(seed,crossover,next_id)):a.gt;
            const uint8_t gt=inherit(pre,stream(seed,mutation,next_id),c.mu);
            double inherited=memory(arm)==0?.5:memory(arm)==1?a.belief:(a.belief+b.belief)*.5;
            uint16_t d1=pair?104:208,d2=pair?104:0;
            births.push_back({uint16_t(t),next_id,a.id,uint16_t(pair?b.id:UINT16_MAX),pre,gt,d1,d2,a.belief,pair?b.belief:.5,inherited});
            events.push_back({uint16_t(t),next_id,a.id,gt});
            a.energy-=d1; if(pair)b.energy-=d2;
            living.push_back({next_id++,gt,192,inherited});
        }
        for(auto& a:living) ++p.counts[a.gt];
        counts.push_back(p);
    }
    save(path/"founders.bin",genesis);save(path/"mapping.bin",schedule);
    save(path/"actions.bin",actions);save(path/"births.bin",births);save(path/"events.bin",events);save(path/"periods.bin",counts);
}
}
int main(int argc,char**argv){
    if(argc!=3)return 2;
    std::string mode=argv[1];
    if(mode!="smoke"&&mode!="eval")return 2;
    fs::path root=argv[2];if(fs::exists(root))throw std::runtime_error("Output exists");fs::create_directories(root);
    std::ofstream manifest(root/"design.csv");
    manifest<<"setting,regime,fee_ticks,reward_ticks,founders,initial_ticks,q,mutation,balanced,seed,arm,path\n";
    auto design=c10::design();int first=mode=="smoke"?3790:3800,last=mode=="smoke"?3791:3819;
    for(unsigned s=0;s<design.size();++s)for(int seed=first;seed<=last;++seed)for(int arm=0;arm<8;++arm){
        auto c=design[s];std::string path=std::to_string(s)+"_"+std::to_string(seed)+"_"+std::to_string(arm);
        c10::world(root/path,c,seed,arm);
        manifest<<s<<','<<c.regime<<','<<c.fee<<','<<c.prize<<','<<c.number<<','<<c.initial<<','<<c.q<<','<<c.mu<<','<<c.balanced<<','<<seed<<','<<arm<<','<<path<<'\n';
    }
    return manifest?0:1;
}
