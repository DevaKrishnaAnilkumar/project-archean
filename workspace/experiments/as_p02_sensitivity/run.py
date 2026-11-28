"""Run exact exploration, smoke checks or the committed fresh-seed evaluation."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import numpy as np
from audit import eq, reconstruct
from model import SEEDS, SMOKE, metrics, schedule, simulate
from theory import GRID, SIM, POLICIES, solve

FIELDS=('cost','budget','reliability','policy')


def labels(condition,policy):
    return dict(zip(FIELDS,(*condition,policy)))


def write(path,records):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,records[0])
        w.writeheader()
        w.writerows(records)


def git(*args):
    return subprocess.check_output(['git','-C',Path(__file__).resolve().parent,*args],text=True).strip()


def summaries(out,records,plans,conditions,nseeds):
    means, contrasts, differences, checks=[],[],[],[]
    for condition in conditions:
        groups={}
        exact=plans[condition][-1]
        for policy in POLICIES:
            key=labels(condition,policy)
            records_for_policy=[r for r in records if all(r[k]==v for k,v in key.items())]
            groups[policy]=records_for_policy
            fields=list(exact[policy])[:9]+['expected_final','realised_final']
            mean={k:float(np.mean([r[k] for r in records_for_policy])) for k in fields}
            means.append(dict(**key,**mean,optimal_net=exact[policy]['optimal_net'],
                              exact_gap=exact[policy]['gap'],sampled_gap=exact[policy]['optimal_net']-mean['expected_net']))
            if nseeds==50:
                for k in ('expected_net','realised_net','visits','accuracy'):
                    se=float(np.std([r[k] for r in records_for_policy],ddof=1)/np.sqrt(nseeds))
                    delta=mean[k]-exact[policy][k]
                    checks.append(dict(**key,metric=k,sample_minus_exact=delta,se=se,
                                       flag=bool(abs(delta)>max(1e-12,4*se))))
        for a,b in combinations(POLICIES,2):
            ds=np.array([x['expected_net']-y['expected_net'] for x,y in zip(groups[a],groups[b])])
            d=float(ds.mean())
            sd=float(ds.std(ddof=1))
            radius=2.00957523449*sd/np.sqrt(nseeds) if nseeds==50 else None
            key=dict(cost=condition[0],budget=condition[1],reliability=condition[2],policy_a=a,policy_b=b)
            contrasts.append(dict(**key,mean=d,sd=sd,low=d-radius if radius is not None else None,
                                  high=d+radius if radius is not None else None,
                                  exact=exact[a]['expected_net']-exact[b]['expected_net']))
            differences.extend(dict(**key,seed=r['seed'],difference=float(v)) for r,v in zip(groups[a],ds))
    write(out/'condition_means.csv',means)
    write(out/'paired_contrasts.csv',contrasts)
    write(out/'paired_seed_differences.csv',differences)
    if checks:
        write(out/'theory_checks.csv',checks)
    return checks


def execute(out,mode):
    start=datetime.now(timezone.utc)
    timer=time.monotonic()
    head=git('rev-parse','HEAD')
    if mode=='pilot':
        assert head==os.environ.get('C05_IMPLEMENTATION') and not git('status','--porcelain','--untracked-files=all')
        assert git('log','-1','--format=%H','--','.')==head
    out.mkdir(parents=True,exist_ok=False)
    grid=GRID if mode=='exact' else SIM
    plans={condition:solve(*condition) for condition in grid}
    write(out/'exact_expectations.csv',[dict(**labels(c,p),fee=plan[1],fixed_sequence=''.join('AB'[i] for i in plan[2]),
                                              random_count=plan[3],**plan[-1][p])
                                       for c,plan in plans.items() for p in POLICIES])
    seeds,n=(SEEDS,128) if mode=='pilot' else (SMOKE,8)
    records=[]
    checks=[]
    if mode!='exact':
        raw=out/'raw'
        raw.mkdir()
        for seed in seeds:
            s=schedule(seed,n)
            assert np.bincount(s['hidden']).tolist()==[n//2]*2
            np.savez_compressed(raw/f'{seed}_schedule.npz',**s)
            with np.load(raw/f'{seed}_schedule.npz',allow_pickle=False) as stored:
                audited_schedule=dict(stored)
            for k,v in s.items():
                eq(v,audited_schedule[k])
            for i,c in enumerate(grid):
                plan=plans[c]
                for p in POLICIES:
                    d=simulate(s,c[1],p,plan)
                    np.savez_compressed(raw/f'{seed}_{i:02}_{p}.npz',**d)
                    with np.load(raw/f'{seed}_{i:02}_{p}.npz',allow_pickle=False) as stored:
                        reconstructed=reconstruct(audited_schedule,stored,c[1],p,plan)
                    for k,v in metrics(s,d,plan[1]).items():
                        eq(v,reconstructed[k])
                    records.append(dict(seed=seed,**labels(c,p),**{k:float(v.mean()) for k,v in reconstructed.items()}))
        write(out/'per_seed.csv',records)
        checks=summaries(out,records,plans,grid,len(seeds))
    flagged=[r for r in checks if r['flag']]
    manifest=dict(mode=mode,status='REVIEW' if flagged else 'PASS',seed_blocks=list(seeds) if records else [],
                  episodes_per_seed=n if records else 0,conditions=[list(c) for c in grid],
                  episode_count=len(records)*n,started_utc=start.isoformat(),ended_utc=datetime.now(timezone.utc).isoformat(),
                  elapsed_seconds=time.monotonic()-timer,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  architecture=platform.machine(),platform=platform.platform(),python=sys.version,numpy=np.__version__,
                  implementation=head,protocol=git('rev-parse','HEAD^'),command=sys.argv,theory_flags=flagged,
                  input_baseline='12a62b92c1a47374480d81bc64937c4eb7150a87',
                  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(Path(__file__).resolve().parent.iterdir()) if p.suffix in ('.py','.md')})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if records:
        (out/'audit.json').write_text(json.dumps(dict(status=manifest['status'],archives=len(records),
              reconstructed_episodes=len(records)*n,tolerance=1e-12,negative_controls='PASS',
              theory_comparisons=len(checks),flagged=flagged),indent=2)+'\n')
    print({k:manifest[k] for k in ('mode','status','episode_count','elapsed_seconds','peak_rss_kib')})
    if flagged:
        raise SystemExit('Review simulation versus theory flags in the saved audit.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    p.add_argument('mode',choices=('exact','smoke','pilot'))
    a=p.parse_args()
    execute(a.output,a.mode)
