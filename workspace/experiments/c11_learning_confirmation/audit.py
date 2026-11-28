"""Independent reconstruction from active and passive event ledgers."""
import argparse
import csv
import json
import importlib.util
from pathlib import Path

import numpy as np

ACTION = np.dtype([
    ("t", "<u2"), ("id", "<u2"), ("before", "<i2"), ("after", "<i2"),
    ("hidden", "i1"), ("site", "i1"), ("obs", "i1"), ("patch", "i1"),
    ("got", "u1"), ("returns", "u1"), ("prior", "<f8"), ("belief", "<f8"),
])
EVENT = np.dtype([("t", "<u2"), ("id", "<u2"), ("parent", "<u2"), ("gt", "u1")])
PASSIVE = np.dtype([("id", "<u2"), ("parent", "<u2"), ("gt", "u1")])
N, CAP, FOUNDERS, DEAD = 240, 120, 60, 65535
MASK = (1 << 64) - 1


def mix(value):
    value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & MASK
    value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & MASK
    return value ^ (value >> 31)


def draws(seed, stream, key=0, replay=0):
    state = mix(seed) ^ mix(stream + 0x7fa56e1) ^ mix(key + 0x8b89e11) ^ mix(replay + 0x50ab921)
    while True:
        state = (state + 0x9e3779b97f4a7c15) & MASK
        yield mix(state)


def uniform_index(draw_stream, size):
    threshold = (1 << 64) % size
    return next(value % size for value in draw_stream if value >= threshold)


def mutation(gt, draw_stream, probability, sensing_probability):
    l, s = divmod(int(gt), 3)
    if (next(draw_stream) >> 11) * 2**-53 < probability:
        l = 1 - l
    if (next(draw_stream) >> 11) * 2**-53 < sensing_probability:
        s = (s + 1 + uniform_index(draw_stream, 2)) % 3
    return l * 3 + s


def roster(founders, ledger, times, audit_parent=True):
    births = ledger["parent"] != DEAD
    new, dead = ledger[births], ledger[~births]
    size = FOUNDERS + len(new)
    assert np.array_equal(new["id"], np.arange(FOUNDERS, size))
    assert np.all(ledger["id"] < size)
    assert len(np.unique(dead["id"])) == len(dead)
    assert np.all(ledger["gt"] < 6)
    birth_times = np.full(size, -1, dtype=int)
    birth_times[FOUNDERS:] = times[births]
    death_times = np.full(size, N, dtype=int)
    death_times[dead["id"]] = times[~births]
    assert np.all(birth_times < death_times)
    gt = np.r_[founders, new["gt"]]
    assert np.array_equal(gt[dead["id"]], dead["gt"])
    # Births occur after active deaths at a time. A passive newborn can parent
    # another passive birth in the same period if its creation preceded it.
    parents = new["parent"]
    assert np.all(parents < new["id"])
    assert np.all(birth_times[parents] <= times[births])
    assert np.all(death_times[parents] > times[births])
    if audit_parent:
        assert np.all(birth_times[parents] < times[births])
    delta = np.zeros((N + 1, 6), dtype=int)
    np.add.at(delta, (np.maximum(0, birth_times), gt), 1)
    np.add.at(delta, (death_times, gt), -1)
    trace = delta.cumsum(axis=0)[:N]
    # Population counts alone can mask an invalid replacement, so retain IDs.
    assert np.all(trace >= 0) and np.all(trace.sum(axis=1) <= CAP)
    return gt, birth_times, death_times, trace


def replay_rng(founders, events, contents, seed, replay, probability, sensing_probability):
    parents = draws(seed, 10, replay=replay)
    deaths = draws(seed, 11, replay=replay)
    mutants = draws(seed, 12, replay=replay)
    living = list(range(FOUNDERS))
    genotype = list(founders)
    for event, row in zip(events, contents, strict=True):
        if event["parent"] == DEAD:
            at = uniform_index(deaths, len(living))
            assert row["id"] == living[at]
            living[at] = living[-1]
            living.pop()
        else:
            parent = living[uniform_index(parents, len(living))]
            assert row["parent"] == parent
            # Mutation uses a fresh state from the dedicated passive stream.
            state = next(mutants)

            def child_draws(state):
                while True:
                    state = (state + 0x9e3779b97f4a7c15) & MASK
                    yield mix(state)

            genotype.append(mutation(genotype[parent], child_draws(state), probability, sensing_probability))
            assert row["gt"] == genotype[-1]
            living.append(int(row["id"]))


def verify_world(path, row, check_rng):
    fixture, q = int(row["fixture"]), float(row["q"])
    fee, prize, overhead, seed = [int(row[key]) for key in ("fee_ticks", "reward_ticks", "overhead_ticks", "seed")]
    founder = np.fromfile(path / "founders.bin", "u1")
    map_trace = np.fromfile(path / "mapping.bin", "u1")
    actions = np.fromfile(path / "actions.bin", ACTION)
    events = np.fromfile(path / "events.bin", EVENT)
    genesis = {'balanced-six':np.repeat(np.arange(6),10), 'frozen':np.full(60,2), 'learning':np.full(60,5), 'mixed':np.repeat([2,5],30)}[row['founders']].tolist()
    f_rng=draws(seed,2)
    for i in range(len(genesis),1,-1):
        j=uniform_index(f_rng,i);genesis[i-1],genesis[j]=genesis[j],genesis[i-1]
    assert np.array_equal(founder,genesis)
    assert map_trace.shape == (N,) and np.all(map_trace < 2)
    map_rng = draws(seed, 1)
    initial = uniform_index(map_rng, 2)
    random_maps = np.array([uniform_index(map_rng, 2) for _ in range(N)])
    expected_maps = [np.full(N, initial), initial ^ (np.arange(N)//24 % 2), random_maps]
    assert np.array_equal(map_trace, expected_maps[int(row["regime"])])
    assert np.all(events["t"][1:] >= events["t"][:-1])
    gt, born, died, trace = roster(founder, events, events["t"])
    birthed = events[events["parent"] != DEAD]
    death_events = events[events["parent"] == DEAD]
    t, aid = actions["t"], actions["id"]
    assert len(np.unique(aid.astype("i8") * N + t)) == len(actions)
    assert np.all(t < N) and np.all(t > born[aid]) and np.all(t <= died[aid])
    exposure = np.minimum(died, N-1) - born
    assert np.array_equal(np.bincount(aid, minlength=len(gt)), exposure)
    assert np.array_equal(death_events["id"], aid[actions["after"] == 0])
    assert np.array_equal(death_events["t"], t[actions["after"] == 0])
    assert np.all(t[1:] >= t[:-1])
    assert np.all((t[1:] != t[:-1]) | (aid[1:] > aid[:-1]))

    order = np.lexsort((t, aid))
    sorted_actions = actions[order]
    sorted_ids = aid[order]
    first = t[order] == born[sorted_ids] + 1
    expected_energy = np.where(first, np.where(sorted_ids < FOUNDERS, 384, 192),
                               np.roll(sorted_actions["after"], 1))
    parent_key = birthed["parent"].astype("i8") * N + birthed["t"]
    action_key = sorted_ids.astype("i8") * N + t[order]
    assert len(np.unique(parent_key)) == len(parent_key)
    parent_rows = np.searchsorted(action_key, parent_key)
    assert np.array_equal(action_key[parent_rows], parent_key)
    assert np.all(sorted_actions["after"][parent_rows] >= 512)
    previous_key = action_key - 1
    expected_energy -= 208 * (~first & np.isin(previous_key, parent_key))
    assert np.array_equal(expected_energy, sorted_actions["before"])
    expected_previous = np.where(first, .5, np.roll(sorted_actions["belief"], 1))
    learning = gt[aid] >= 3
    maintenance = actions["before"] - 16 - learning.astype("i2") * overhead
    alive_after_maintenance = maintenance > 0
    sampled, attempted = actions["site"] >= 0, actions["patch"] >= 0
    assert np.all((actions["hidden"]>=0) == alive_after_maintenance)
    assert np.all(actions["hidden"]<=1) and np.all(actions["site"]<=1) and np.all(actions["patch"]<=1)
    assert np.all(actions["got"]<=1) and np.all(actions["returns"]<=4)
    assert np.array_equal(actions["obs"]>=0, sampled) and np.all(actions["obs"]<=1)
    assert np.all(~sampled | ((maintenance > fee+32) & (gt[aid]%3 > 0)))
    assert np.all(sampled | (maintenance <= fee+32) | (gt[aid]%3 != 2))
    assert np.array_equal(attempted, maintenance - fee*sampled > 32)
    assert np.all(attempted | (actions["got"]==0))
    if fixture in (2, 3):
        assert np.all(actions["got"][attempted] == fixture-2)
    after_reward = maintenance - fee*sampled - 32*attempted + prize*actions["got"]
    steps = np.where(attempted, np.minimum(4, (after_reward+7)//8), 0)
    assert np.array_equal(steps, actions["returns"])
    assert np.array_equal(np.maximum(0, after_reward-8*steps), actions["after"])
    learn_live = learning[order] & alive_after_maintenance[order]
    expected_prior = np.where(learn_live, .05+.9*expected_previous, expected_previous)
    assert np.allclose(sorted_actions["prior"], expected_prior, rtol=0, atol=1e-12)
    directed = sampled & (np.abs((q-.5)*(2*actions["prior"]-1)) > 1e-12)
    assert np.array_equal(actions["site"][directed], (actions["prior"][directed]>.5).astype("i1"))
    action_accuracy = .5+(q-.5)*np.where(actions["site"]==1, actions["prior"],1-actions["prior"])
    use_cue = sampled & (action_accuracy-.5 > 1e-12)
    assert np.array_equal(actions["patch"][use_cue], actions["obs"][use_cue])
    prior = actions["prior"]
    posterior = prior.copy()
    selected = sampled & learning
    cue, site, patch, got = [actions[name][selected] for name in ("obs","site","patch","got")]
    likelihoods = []
    for m in (0, 1):
        accuracy = np.where(site == m, q, .5)
        h0 = np.where(cue == 0, accuracy, 1-accuracy)
        h1 = 1-h0
        w0 = np.where((patch == 0) == got.astype(bool), .85, .15)
        likelihoods.append((h0*w0+h1*(1-w0))*.5)
    weighted = prior[selected]*likelihoods[1]
    posterior[selected] = weighted / ((1-prior[selected])*likelihoods[0]+weighted)
    assert np.allclose(posterior, actions["belief"], rtol=0, atol=1e-12)
    if q == .5:
        assert np.allclose(actions["belief"], .5, rtol=0, atol=1e-12)

    eligible = actions["after"] >= 512
    available = CAP-np.bincount(t[actions["after"]>0], minlength=N)
    eligible_count = np.bincount(t[eligible], minlength=N)
    birth_count = np.bincount(birthed["t"], minlength=N)
    if fixture != 1:
        assert np.array_equal(birth_count, np.minimum(available, eligible_count))
    else:
        assert not len(birthed)
    if fixture == 2:
        assert np.all(trace.sum(axis=1)[24:] == 0)
    if fixture == 3:
        assert np.any(trace.sum(axis=1) == CAP)
    probability, sensing_probability = float(row["mutation_L"]), float(row["mutation_S"])
    if check_rng:
        # Independent vectorised replay of all exogenous action opportunities.
        key=t.astype('u8')*np.uint64(65536)+aid.astype('u8')
        hidden=(rng(seed,3,key)&np.uint64(1)).astype('i1')
        assert np.array_equal(actions['hidden'],np.where(alive_after_maintenance,hidden,-1))
        assert np.array_equal(sampled,(maintenance>fee+32)&(unit(seed,6,key)<(gt[aid]%3)*.5))
        prior=actions['prior']; tie1=(rng(seed,7,key)&np.uint64(1)).astype('i1'); tie2=(rng(seed,7,key,2)&np.uint64(1)).astype('i1')
        site=np.where(np.abs((q-.5)*(2*prior-1))<=1e-12,tie1,prior>.5).astype('i1')
        assert np.array_equal(actions['site'],np.where(sampled,site,-1))
        cue=np.where(unit(seed,4,2*key+site.astype('u8'))<np.where(site==map_trace[t],q,.5),hidden,1-hidden)
        assert np.array_equal(actions['obs'],np.where(sampled,cue,-1))
        accuracy=.5+(q-.5)*np.where(site==1,prior,1-prior)
        p=np.where(sampled,np.where(cue==1,accuracy,1-accuracy),.5)
        patch=np.where(np.abs(p-.5)<=1e-12,tie2,p>.5).astype('i1')
        assert np.array_equal(actions['patch'],np.where(attempted,patch,-1))
        got=attempted&(unit(seed,5,2*key+patch.astype('u8'))<np.where(patch==hidden,.85,.15)) if fixture not in (2,3) else attempted&(fixture==3)
        assert np.array_equal(actions['got'],got)
        for period in np.flatnonzero(birth_count):
            ids = aid[eligible & (t==period)].tolist()
            shuffle_rng = draws(seed, 9, int(period))
            for i in range(len(ids), 1, -1):
                j = uniform_index(shuffle_rng, i)
                ids[i-1], ids[j] = ids[j], ids[i-1]
            matches = birthed[birthed["t"]==period]
            assert np.array_equal(matches["parent"], ids[:birth_count[period]])
            for b in matches:
                assert b["gt"] == mutation(gt[b["parent"]], draws(seed, 8, int(b["id"])), probability, sensing_probability)
    elif fixture == 0:
        assert np.array_equal(gt[birthed["parent"]], birthed["gt"])

    passive_values, passive_traces = [], []
    for replay in range(int(row["replays"])):
        contents = np.fromfile(path / f"passive{replay}.bin", PASSIVE)
        assert len(contents) == len(events)
        assert np.array_equal(events["parent"]==DEAD, contents["parent"]==DEAD)
        _, _, _, passive_trace = roster(founder, contents, events["t"], audit_parent=False)
        assert np.array_equal(passive_trace.sum(axis=1), trace.sum(axis=1))
        passive_values.append(passive_trace[:,4:].sum()/(CAP*N))
        passive_traces.append(passive_trace)
        if check_rng:
            replay_rng(founder, events, contents, seed, replay, probability, sensing_probability)

    founder_line = np.full(len(gt), -1, dtype=int)
    founder_line[:FOUNDERS] = np.arange(FOUNDERS)
    for b in birthed:
        founder_line[b["id"]] = founder_line[b["parent"]]
    lineage = np.zeros((N+1, FOUNDERS), dtype=int)
    np.add.at(lineage, (np.maximum(0,born), founder_line), 1)
    np.add.at(lineage, (died, founder_line), -1)
    lineage = (lineage.cumsum(axis=0)[:N]>0).sum(axis=1)
    pop = trace.sum(axis=1)
    assert np.all(pop[np.flatnonzero(pop==0)[0]:]==0) if np.any(pop==0) else True
    if row['study']=='B': assert np.all(gt%3==2)
    # End-of-period genotype accounting, including death, births and mutation.
    deaths_by=np.zeros((N,6),dtype=int); np.add.at(deaths_by,(death_events['t'],death_events['gt']),1)
    births_parent=np.zeros((N,6),dtype=int); np.add.at(births_parent,(birthed['t'],gt[birthed['parent']]),1)
    births_child=np.zeros((N,6),dtype=int); np.add.at(births_child,(birthed['t'],birthed['gt']),1)
    before=np.vstack((np.bincount(founder,minlength=6),trace[:-1]))
    assert np.array_equal(trace,before-deaths_by+births_child)
    mutations=np.zeros((N,6,6),dtype=int);np.add.at(mutations,(birthed['t'],gt[birthed['parent']],birthed['gt']),1)
    assert np.array_equal(trace,before-deaths_by+births_parent+mutations.sum(axis=1)-mutations.sum(axis=2))
    margin = trace[:,4:].sum()/(CAP*N)
    pm=float(np.mean(passive_values)) if passive_values else float('nan')
    u=pop.sum()/(CAP*N);assert u>0
    eligible_by=np.zeros((N,6),dtype=int);np.add.at(eligible_by,(t[eligible],gt[aid[eligible]]),1)
    assert np.all(eligible_by>=births_parent)
    accounting=np.column_stack((before,deaths_by,births_parent,births_child,mutations.reshape(N,36),eligible_by,eligible_by-births_parent,available))
    info = {**row, "active":margin, "passive_mean":pm, "delta":margin-pm, "U":u,"F":margin/u,"G":(margin-pm)/u,"actions":len(actions),"eligible":int(eligible_count.sum()),
            "extinction":int(np.flatnonzero(pop==0)[0]) if np.any(pop==0) else N,
            "births":len(birthed), "deaths":len(death_events), "mean_population":pop.mean(),
            "final_population":pop[-1], "final_lineages":lineage[-1],
            "lineage_periods":lineage.sum(), "blocked_births":int((eligible_count-birth_count).sum()),
            "mut_l":int((gt[birthed["parent"]]//3 != birthed["gt"]//3).sum()),
            "mut_s":int((gt[birthed["parent"]]%3 != birthed["gt"]%3).sum())}
    for i in range(8):
        info[f"passive_{i}"] = passive_values[i] if i<len(passive_values) else float("nan")
    exposure_gt = gt[aid]
    for g in range(6):
        subset = exposure_gt == g
        counts = trace[:,g]
        endings = died[gt==g]
        info.update({
            f"periods_g{g}": int(counts.sum()), f"final_g{g}": int(counts[-1]),
            f"exposure_g{g}": int(subset.sum()), f"individuals_g{g}": int((gt==g).sum()),
            f"births_parent_g{g}": int((gt[birthed["parent"]]==g).sum()),
            f"offspring_g{g}": int((birthed["gt"]==g).sum()),
            f"censored_g{g}": int((endings==N).sum()),
            f"attempts_g{g}": int((subset&attempted).sum()),
            f"samples_g{g}": int((subset&sampled).sum()),
            f"correct_g{g}": int((subset&attempted&(actions["patch"]==actions["hidden"])).sum()),
            f"rewards_g{g}": int(actions["got"][subset].sum()),
            f"net_action_ticks_g{g}": int((actions["after"][subset]-actions["before"][subset]).sum()),
            f"overhead_ticks_g{g}": int(subset.sum()*overhead*(g>=3)),
            f"sensing_ticks_g{g}": int((subset&sampled).sum()*fee),
            f"mapping_brier_sum_g{g}": float(((prior[subset]-map_trace[t[subset]])**2).sum()),
        })
    transitions = np.bincount(6*gt[birthed["parent"]]+birthed["gt"], minlength=36)
    info.update({f"transition_{k//6}_{k%6}": int(value) for k, value in enumerate(transitions)})
    for g in range(6):
        info[f'eligible_g{g}']=int(eligible_by[:,g].sum())
        info[f'blocked_g{g}']=int((eligible_by[:,g]-births_parent[:,g]).sum())
    return info, np.column_stack((trace,lineage,np.sum(passive_traces,axis=0) if passive_traces else np.zeros_like(trace))),accounting


U=np.uint64
INC=U(0x9e3779b97f4a7c15)
def vmix(x):
    x=np.asarray(x,dtype='u8')
    with np.errstate(over='ignore'):
        x=(x^(x>>U(30)))*U(0xbf58476d1ce4e5b9);x=(x^(x>>U(27)))*U(0x94d049bb133111eb)
    return x^(x>>U(31))
def rng(seed,stream,key,draw=1):
    state=U(mix(seed)^mix(stream+0x7fa56e1)^mix(0x50ab921))^vmix(np.asarray(key,dtype='u8')+U(0x8b89e11))
    with np.errstate(over='ignore'):return vmix(state+INC*U(draw))
def unit(seed,stream,key,draw=1):return (rng(seed,stream,key,draw)>>U(11)).astype('f8')*2**-53

def main():
    p=argparse.ArgumentParser();p.add_argument('raw',type=Path);p.add_argument('out',type=Path);p.add_argument('study',choices=['A','B']);p.add_argument('phase',choices=['smoke','evaluation','fixtures','equivalence']);args=p.parse_args()
    rows=list(csv.DictReader((args.raw/'design.csv').open()));assert not args.out.exists();args.out.mkdir()
    assert all(r['study']==args.study and r['phase']==args.phase for r in rows)
    assert len({r['path'] for r in rows})==len(rows)
    if args.phase in ('smoke','evaluation'):
        locked=[r for r in csv.DictReader((Path(__file__).parent/'design.csv').open()) if r['study']==args.study and r['phase']==args.phase]
        # exact numeric equivalence; CSV serialisation may remove trailing zeros
        def canon(r):return tuple(float(r[k]) if k in ('seed','regime','q','fee_ticks','reward_ticks','overhead_ticks','mutation_L','mutation_S','replays') else r[k] for k in locked[0])
        assert len(rows)==len(locked) and sorted(map(canon,rows))==sorted(map(canon,locked))
    else:assert len(rows)==(4 if args.phase=='fixtures' else 6)
    stats=[];curves=[];accounts=[]
    for r in rows:
        path=args.raw/r['path'];assert set(x.name for x in path.iterdir())=={'founders.bin','mapping.bin','actions.bin','events.bin'}|{f'passive{i}.bin' for i in range(int(r['replays']))}
        for file,dtype in [('actions.bin',ACTION),('events.bin',EVENT)]+[(f'passive{i}.bin',PASSIVE) for i in range(int(r['replays']))]:assert (path/file).stat().st_size%dtype.itemsize==0
        try:info,trace,account=verify_world(path,r,True)
        except Exception as exc:raise RuntimeError(f"Audit failure {r['path']}") from exc
        stats.append(info);curves.append(trace);accounts.append(account)
    if args.study=='B' and args.phase in ('smoke','evaluation'):
        for seed in sorted({r['seed'] for r in rows}):
            m={r['condition']:args.raw/r['path'] for r in rows if r['seed']==seed}; a,b=m['B1-null'],m['B2-null']
            assert (a/'mapping.bin').read_bytes()==(b/'mapping.bin').read_bytes()
            x,y=[np.fromfile(z/'actions.bin',ACTION) for z in (a,b)]
            for field in ACTION.names:
                if field in ('prior','belief'):assert np.allclose(x[field],y[field],rtol=0,atol=1e-12)
                else:assert np.array_equal(x[field],y[field])
            x,y=[np.fromfile(z/'events.bin',EVENT) for z in (a,b)]
            for field in ('t','id','parent'):assert np.array_equal(x[field],y[field])
            for label in ('informative','null'):assert (m[f'B3-{label}']/'founders.bin').read_bytes()==(m[f'B4-{label}']/'founders.bin').read_bytes()
    with (args.out/'worlds.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(stats[0]));w.writeheader();w.writerows(stats)
    np.save(args.out/'curves.npy',np.array(curves,dtype='i2'),allow_pickle=False)
    np.save(args.out/'accounting.npy',np.array(accounts,dtype='i2'),allow_pickle=False)
    result=dict(status='PASS',study=args.study,phase=args.phase,worlds=len(rows),replays=sum(int(r['replays']) for r in rows),actions=sum(r['actions'] for r in stats),births=sum(r['births'] for r in stats),deaths=sum(r['deaths'] for r in stats),extinct=sum(r['extinction']<N for r in stats),all_action_rng_replayed=True,all_mutations_and_passive_events_replayed=True)
    (args.out/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
