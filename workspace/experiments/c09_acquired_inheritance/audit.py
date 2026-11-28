"""Reconstruct C09 outcomes independently from its binary ledgers."""
import argparse
import csv
import importlib.util
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location("c08audit",Path(__file__).parent.parent/"c08_heritable_learning/audit.py")
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
N,CAP,FOUNDERS,DEAD=old.N,old.CAP,old.FOUNDERS,old.DEAD
BIRTH=np.dtype([(k,"<u2") for k in ("t","id","parent","donor")]+[
    ("gt","u1"),("fee","u1"),("donor_p","<f8"),("child_p","<f8")])

def mutate(allele,rng):
    if (next(rng)>>11)*2**-53>=.02:
        return allele
    return (allele+1+old.uniform_index(rng,2))%3

def from_state(state):
    while True:
        state=(state+0x9e3779b97f4a7c15)&old.MASK
        yield old.mix(state)

def audit_passive(seed,i,genesis,ledger,replay):
    ids=list(range(FOUNDERS))
    gt=list(genesis)
    parents=old.draws(seed,10,replay=i)
    deaths=old.draws(seed,11,replay=i)
    mutations=old.draws(seed,12,replay=i)
    for source,event in zip(ledger,replay,strict=True):
        if source["parent"]==DEAD:
            at=old.uniform_index(deaths,len(ids))
            assert (event["id"],event["parent"],event["gt"])==(ids[at],DEAD,gt[ids[at]])
            ids[at]=ids[-1]
            ids.pop()
        else:
            parent=ids[old.uniform_index(parents,len(ids))]
            child=mutate(gt[parent],from_state(next(mutations)))
            assert (event["id"],event["parent"],event["gt"])==(len(gt),parent,child)
            ids.append(len(gt))
            gt.append(child)

def audit(raw,row):
    read=lambda name,dtype:np.fromfile(raw/(name+".bin"),dtype)
    g=read("founders","u1")
    maps=read("mapping","u1")
    e=read("events",old.EVENT)
    b=read("births",BIRTH)
    a=read("actions",old.ACTION)
    s,regime,pop,seed,fee,reward,transfer=(int(row[k]) for k in
        ("setting","regime","population","seed","fee_ticks","reward_ticks","transfer_ticks"))
    q=float(row["q"])
    expected=[np.full(60,0),np.full(60,2),np.repeat(range(3),20),np.repeat(range(3),20)][pop].tolist()
    founder=old.draws(seed,2)
    for i in range(60,1,-1):
        j=old.uniform_index(founder,i)
        expected[i-1],expected[j]=expected[j],expected[i-1]
    assert np.array_equal(g,expected)
    rng=old.draws(seed,1)
    initial=old.uniform_index(rng,2)
    random_maps=[old.uniform_index(rng,2) for _ in range(N)]
    assert np.array_equal(maps,[np.full(N,initial),initial^(np.arange(N)//24%2),random_maps][regime])
    birth_events=e[e["parent"]!=DEAD]
    assert all(np.array_equal(b[k],birth_events[k]) for k in ("id","parent","t","gt"))
    genotype,born,died,padded=old.roster(g,e,e["t"])
    traces=padded[:,:3]
    assert np.max(genotype)<=2 and np.all(e["t"][1:]>=e["t"][:-1])
    t,ids=a["t"],a["id"]
    keys=ids.astype("i8")*N+t
    assert len(np.unique(keys))==len(a) and np.all(t>born[ids]) and np.all(t<=died[ids])
    assert np.array_equal(np.bincount(ids,minlength=len(genotype)),np.minimum(N-1,died)-born)
    deaths=e[e["parent"]==DEAD]
    dead=a["after"]==0
    assert np.array_equal(deaths["id"],ids[dead]) and np.array_equal(deaths["t"],t[dead])
    assert np.all(t[1:]>=t[:-1])
    serial=np.argsort(keys)
    ordered=a[serial]
    sk=keys[serial]
    first=ordered["t"]==born[ordered["id"]]+1
    inherited=np.r_[np.full(60,.5),b["child_p"]]
    assert np.all(b["fee"]==transfer*b["gt"]//2)
    assert np.allclose(b["child_p"],.5+.5*b["gt"]*(b["donor_p"]-.5),rtol=0,atol=1e-12)
    assert np.allclose(ordered["prior"],np.where(ordered["before"]>16,
        .05+.9*np.where(first,inherited[ordered["id"]],np.roll(ordered["belief"],1)),
        np.where(first,inherited[ordered["id"]],np.roll(ordered["belief"],1))),rtol=0,atol=1e-12)
    parent_key=b["parent"].astype("i8")*N+b["t"]
    assert len(np.unique(parent_key))==len(b)
    parent_rows=np.searchsorted(sk,parent_key)
    assert np.array_equal(sk[parent_rows],parent_key) and np.all(ordered["after"][parent_rows]>=512)
    balance=np.zeros(len(a),dtype="i4")
    nxt=np.searchsorted(sk,parent_key+1)
    valid=(nxt<len(sk)) & (sk[np.minimum(nxt,len(sk)-1)]==parent_key+1) & (b["t"]<N-1)
    balance[nxt[valid]]=208+b["fee"][valid].astype("i4")
    assert np.array_equal(ordered["before"],np.where(first,np.where(ordered["id"]<60,384,192),
        np.roll(ordered["after"],1))-balance)
    can_sense=a["before"]>48+fee
    assert np.array_equal(a["site"]>=0,can_sense)
    attempt=a["before"]-16-fee*can_sense>32
    assert np.array_equal(a["patch"]>=0,attempt)
    arrived=a["before"]-16-fee*can_sense-32*attempt+reward*a["got"]
    returns=np.where(attempt,np.minimum(4,(arrived+7)//8),0)
    assert np.array_equal(a["returns"],returns) and np.array_equal(a["after"],np.maximum(0,arrived-8*returns))
    prior=a["prior"][can_sense]
    obs,site,patch,got=[a[k][can_sense] for k in ("obs","site","patch","got")]
    likelihood=[]
    for m in (0,1):
        acc=np.where(site==m,q,.5)
        h0=np.where(obs==0,acc,1-acc)
        w=np.where((patch==0)==got.astype(bool),.85,.15)
        likelihood.append(.5*(h0*w+(1-h0)*(1-w)))
    post=a["prior"].copy()
    post[can_sense]=prior*likelihood[1]/((1-prior)*likelihood[0]+prior*likelihood[1])
    assert np.allclose(post,a["belief"],rtol=0,atol=1e-12)
    if q==.5:
        assert np.allclose(inherited,.5,rtol=0,atol=1e-12) and np.allclose(post,.5,rtol=0,atol=1e-12)
    for i in np.linspace(0,len(a)-1,min(len(a),96),dtype=int):
        if a["before"][i]<=16:
            assert a["hidden"][i]==-1
            continue
        key=int(t[i])*65536+int(ids[i])
        hidden=old.uniform_index(old.draws(seed,3,key),2)
        assert a["hidden"][i]==hidden
        tie_draws=old.draws(seed,7,key)
        site_tie,patch_tie=[old.uniform_index(tie_draws,2) for _ in range(2)]
        p=a["prior"][i]
        accuracy=.5
        if can_sense[i]:
            site=site_tie if abs((q-.5)*(2*p-1))<=1e-12 else int(p>.5)
            assert a["site"][i]==site
            draw=(next(old.draws(seed,4,key*2+site))>>11)*2**-53
            obs=hidden if draw<(q if site==maps[t[i]] else .5) else 1-hidden
            assert a["obs"][i]==obs
            correctness=.5+(q-.5)*(p if site else 1-p)
            accuracy=correctness if obs else 1-correctness
        if attempt[i]:
            patch=patch_tie if abs(accuracy-.5)<=1e-12 else int(accuracy>.5)
            assert a["patch"][i]==patch
            draw=(next(old.draws(seed,5,key*2+patch))>>11)*2**-53
            assert a["got"][i]==(draw<(.85 if patch==hidden else .15))

    elig=a["after"]>=512
    assert np.array_equal(np.bincount(b["t"],minlength=N),np.minimum(
        CAP-np.bincount(t[~dead],minlength=N),np.bincount(t[elig],minlength=N)))
    for period in np.unique(b["t"]):
        actions=a[t==period]
        surv=actions[actions["after"]>0]
        eligible=surv["id"][surv["after"]>=512].tolist()
        rand=old.draws(seed,9,int(period))
        for j in range(len(eligible),1,-1):
            k=old.uniform_index(rand,j)
            eligible[j-1],eligible[k]=eligible[k],eligible[j-1]
        actual=b[b["t"]==period]
        assert np.array_equal(actual["parent"],eligible[:len(actual)])
        adults=surv["id"].tolist()
        beliefs=dict(zip(adults,surv["belief"],strict=True))
        for child in actual:
            parent,cid=map(int,(child["parent"],child["id"]))
            assert child["gt"]==(genotype[parent] if pop<2 else mutate(genotype[parent],old.draws(seed,8,cid)))
            donor=parent
            if pop==3:
                alternatives=[n for n in adults if n!=parent]
                donor=alternatives[old.uniform_index(old.draws(seed,13,cid),len(alternatives))] if alternatives else DEAD
            assert child["donor"]==donor and child["donor_p"]==beliefs.get(donor,.5)

    count=traces.sum(axis=1)
    zero=np.flatnonzero(count==0)
    assert len(zero)==0 or np.all(count[zero[0]:]==0)
    record={**row,"occupancy":traces[:,1:].sum()/(CAP*N),"abundance":count.mean(),
        "extinct_period":int(zero[0]) if len(zero) else N,"births":len(b),"deaths":len(deaths),
        "final_pop":int(count[-1]),"transfer":int(b["fee"].sum()),
        "fallback":int((b["donor"]==DEAD).sum()),"blocked_births":int(elig.sum()-len(b))}
    founder=np.full(len(genotype),-1)
    founder[:60]=np.arange(60)
    for child in b:
        founder[child["id"]]=founder[child["parent"]]
    lineage=np.zeros((N+1,60),dtype=int)
    np.add.at(lineage,(np.maximum(0,born),founder),1)
    np.add.at(lineage,(died,founder),-1)
    lineages=(lineage.cumsum(axis=0)[:N]>0).sum(axis=1)
    record["final_lineages"]=int(lineages[-1])
    record["mean_lineages"]=lineages.mean()
    passive_values=[]
    if pop==2:
        for i in range(8):
            replay=read(f"passive{i}",old.PASSIVE)
            audit_passive(seed,i,g,e,replay)
            _,_,_,passive=old.roster(g,replay,e["t"],False)
            assert np.array_equal(passive.sum(axis=1),count)
            passive_values.append(passive[:,1:].sum()/(CAP*N))
    for i in range(8):
        record[f"passive_{i}"]=passive_values[i] if passive_values else float("nan")
    record["passive_mean"]=np.mean(passive_values) if passive_values else float("nan")
    record["enrichment"]=record["occupancy"]-record["passive_mean"]
    matched_choice=attempt&(a["patch"]==a["hidden"])
    idx=np.full(len(genotype),len(a),dtype=int)
    np.minimum.at(idx,ids[attempt],np.flatnonzero(attempt))
    before_horizon=b["t"]<N-1
    next_map=maps[np.minimum(N-1,b["t"]+1)]
    # Ignore founders here; calibration is a birth-cohort endpoint.
    first_attempt=idx[b["id"]] <len(a)
    first_correct=np.zeros(len(b),bool)
    first_correct[first_attempt]=matched_choice[idx[b["id"]][first_attempt]]
    first_period=(born[ids]+1==t) & (ids>=60)
    contradict=before_horizon&((b["child_p"]-.5)*(2*next_map.astype(int)-1)<-1e-12)
    bad_ids=b["id"][contradict]
    align=(a["belief"]-.5)*(2*maps[t].astype(int)-1)>1e-12
    switched=(regime==1)&(t//24!=(born[ids]+1)//24)
    align_index=np.full(len(genotype),N,dtype=int)
    np.minimum.at(align_index,ids[align&~switched],t[align&~switched])
    duration=align_index[bad_ids]-born[bad_ids]-1
    alignment=align_index[bad_ids]<N
    revision_bound=np.minimum(np.minimum(died[bad_ids]+1,N),((born[bad_ids]+1)//24+1)*24 if regime==1 else N)
    record.update(births_observable=int(before_horizon.sum()),first_attempts=int(first_attempt.sum()),
        first_correct=int(first_correct.sum()),first_period_deaths=int((first_period&dead).sum()),
        belief_brier_sum=float(np.square(b["child_p"][before_horizon]-next_map[before_horizon]).sum()),
        donor_brier_sum=float(np.square(b["donor_p"][before_horizon]-next_map[before_horizon]).sum()),
        wrong_birth_belief=len(bad_ids),revised=int(alignment.sum()),
        revision_period_sum=int(duration[alignment].sum()),
        revision_censor_period_sum=int((revision_bound[~alignment]-born[bad_ids][~alignment]-1).sum()))
    revision_rows=[]
    for i,cid in enumerate(bad_ids):
        revision_rows.append({"setting":s,"seed":seed,"population":pop,"id":int(cid),
            "observed_alignment":int(alignment[i]),
            "periods":int(duration[i] if alignment[i] else revision_bound[i]-born[cid]-1)})
    switch_cohort=(regime==1)&(t>=24)&(t%24<3)&(born[ids]<(t//24)*24)
    record.update(switch_start=int((switch_cohort&(t%24==0)).sum()),
        switch_attempts=int((switch_cohort&attempt).sum()),switch_correct=int((switch_cohort&matched_choice).sum()),
        switch_deaths=int((switch_cohort&dead).sum()))
    for allele in range(3):
        cohort=b["gt"]==allele
        is_allele=genotype[ids]==allele
        record.update({f"t{allele}_{k}":v for k,v in {
            "living":int(traces[:,allele].sum()),"final":int(traces[-1,allele]),
            "births":int(cohort.sum()),"births_observable":int((cohort&before_horizon).sum()),
            "parents":int((genotype[b["parent"]]==allele).sum()),"action_periods":int(is_allele.sum()),
            "offspring_periods":int((is_allele&(ids>=60)).sum()),"offspring_censored":int((cohort&(died[b["id"]]==N)).sum()),
            "first_attempt":int((cohort&first_attempt).sum()),"first_correct":int((cohort&first_correct).sum()),
            "birth_brier_sum":float(np.square(b["child_p"][cohort&before_horizon]-next_map[cohort&before_horizon]).sum()),
            "transfer":int(b["fee"][cohort].sum()),"mutations":int((cohort&(genotype[b["parent"]]!=allele)).sum())
        }.items()})
    longevity=np.zeros((3,N+1,2),dtype=np.int32)
    child_ids=b["id"]
    observed=np.minimum(died[child_ids],N-1)-born[child_ids]
    censored=(died[child_ids]==N).astype(int)
    np.add.at(longevity,(b["gt"],observed,censored),1)
    return record,np.column_stack((traces,lineages)),revision_rows,longevity

def main():
    p=argparse.ArgumentParser()
    p.add_argument("raw",type=Path)
    p.add_argument("out",type=Path)
    args=p.parse_args()
    args.out.mkdir()
    with (args.raw/"design.csv").open() as f:
        schedule=list(csv.DictReader(f))
    assert len(schedule) in (120,1200)
    seeds=range(3690,3692) if len(schedule)==120 else range(3700,3720)
    assert {(int(r["setting"]),int(r["seed"]),int(r["population"])) for r in schedule} == {
        (s,seed,pop) for s in range(15) for seed in seeds for pop in range(4)}
    results,traces,revisions,lifetimes=[],[],[],[]
    for row in schedule:
        path=args.raw/row["path"]
        try:
            result,trace,revision,longevity=audit(path,row)
        except AssertionError as exc:
            raise AssertionError(f"Audit failed at {row['path']}") from exc
        results.append(result)
        traces.append(trace)
        revisions.extend(revision)
        lifetimes.append(longevity)
    for seed in seeds:
        a,b=[args.raw/f"13_{seed}_{pop}" for pop in (0,1)]
        for file in ("actions.bin","mapping.bin"):
            assert (a/file).read_bytes()==(b/file).read_bytes(),(seed,file)
        for file,fields,dtype in (("events.bin",["t","id","parent"],old.EVENT),("births.bin",["t","id","parent","donor","fee","donor_p","child_p"],BIRTH)):
            assert np.array_equal(np.fromfile(a/file,dtype)[fields],np.fromfile(b/file,dtype)[fields])
    for name,data in (("worlds",results),("revision_cohorts",revisions)):
        with (args.out/(name+".csv")).open("w",newline="") as f:
            fields=list(data[0]) if data else ["setting","seed","population","id","observed_alignment","periods"]
            writer=csv.DictWriter(f,fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    np.save(args.out/"curves.npy",np.array(traces,dtype=np.int16))
    np.save(args.out/"offspring_durations.npy",np.array(lifetimes,dtype=np.int16))
    print(f"PASS {len(results)} active worlds and {2*len(results)} passive replays; exact parent, donor, mutation and energy ledgers.")
    print(f"PASS free null-cue A/B parity for {len(seeds)} seeds; mapping, births, actions and energy agree.")
    print("PASS replay draws, complete pedigrees, Bayesian belief updates and sampled action RNG reconstruction.")

if __name__=="__main__":
    main()
