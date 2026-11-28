"""Generate and independently audit the locked C06 grid."""
import argparse
import csv
from datetime import datetime,timezone
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
from audit import close,reconstruct
from model import FIELDS,METRICS,aggregate,compile_plan,schedule,simulate
from theory import EXACT,SIM,POLICIES,METRICS as EXACT_METRICS,solve

SOURCE=Path(__file__).resolve().parent
KEYS=('initial_energy','cost_multiplier','reliability','objective')
BASE='3c062032202e270756d40ce7498dc9e2e7b56297'
PILOT=tuple(range(3400,3450))
SMOKE=(3390,3391)
INTERVAL_CRITICAL=2.00957523449


def git(*args):
    return subprocess.check_output(['git','-C',SOURCE,*args],text=True).strip()


def csv_file(out,name,records):
    with (out/f'{name}.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,records[0])
        writer.writeheader()
        writer.writerows(records)


def exact_rows(grid,plans):
    return [dict(**dict(zip(KEYS,c)),policy=p,
                 sequence=''.join('AB'[i] for i in plans[c]['sequence']),
                 random_count=plans[c]['count'],
                 **{name:float(v) for name,v in zip(EXACT_METRICS,plans[c]['values'][p])})
            for c in grid for p in POLICIES]


def report(out,seed_array,plans,seeds):
    rows,means,contrasts,primary,checks=[],[],[],[],[]
    n=len(seeds)
    mean=seed_array.mean(axis=0)
    metric_idx={m:i for i,m in enumerate(METRICS)}
    for c,setting in enumerate(SIM):
        labels=dict(zip(KEYS,setting))
        plan=plans[setting]
        for j,p in enumerate(POLICIES):
            rows.extend(dict(seed=s,**labels,policy=p,**dict(zip(METRICS,seed_array[i,c,j])))
                        for i,s in enumerate(seeds))
            means.append(dict(**labels,policy=p,**dict(zip(METRICS,mean[c,j]))))
            if n==50:
                for key in EXACT_METRICS:
                    x=seed_array[:,c,j,metric_idx[key]]
                    target=float(plan['values'][p][EXACT_METRICS.index(key)])
                    delta=float(x.mean()-target)
                    se=float(np.std(x,ddof=1)/np.sqrt(n))
                    checks.append(dict(**labels,policy=p,metric=key,sample_minus_exact=delta,se=se,
                                       flag=bool(abs(delta)>max(1e-12,5*se))))
        for j,i in combinations(range(len(POLICIES)),2):
            a,b=POLICIES[i],POLICIES[j]
            for metric in ('completion','survival','acquisition','final_energy'):
                d=seed_array[:,c,i,metric_idx[metric]]-seed_array[:,c,j,metric_idx[metric]]
                avg=float(d.mean())
                sd=float(d.std(ddof=1))
                radius=INTERVAL_CRITICAL*sd/np.sqrt(n) if n==50 else None
                idx=EXACT_METRICS.index(metric)
                v=dict(**labels,policy_a=a,policy_b=b,metric=metric,n=n,mean=avg,sd=sd,
                       low=avg-radius if radius is not None else None,
                       high=avg+radius if radius is not None else None,
                       exact=float(plan['values'][a][idx]-plan['values'][b][idx]))
                contrasts.append(v)
                if setting[-1]=='task_first' and metric=='completion' and (a,b) in (
                        ('myopic','fixed'),('adaptive','fixed'),('adaptive','myopic')):
                    primary.append(v)
    for name,table in [('per_seed',rows),('condition_means',means),('paired_contrasts',contrasts),
                       ('primary_contrasts',primary),('theory_checks',checks)]:
        if table:
            csv_file(out,name,table)
    return checks


def run(out,mode):
    started=datetime.now(timezone.utc).isoformat()
    clock=time.monotonic()
    head=git('rev-parse','HEAD')
    if mode=='pilot':
        assert head==os.environ.get('C06_IMPLEMENTATION') and not git('status','--porcelain','--untracked-files=all')
        assert git('log','-1','--format=%H','--','.')==head
    out.mkdir(parents=True,exist_ok=False)
    grid=EXACT if mode=='exact' else SIM
    plans={c:compile_plan(solve(*c)) for c in grid}
    csv_file(out,'exact_expectations',exact_rows(grid,plans))
    seeds,episodes=(PILOT,128) if mode=='pilot' else (SMOKE,8)
    checks=[]
    if mode!='exact':
        rawdir=out/'raw'
        rawdir.mkdir()
        result=np.empty((len(seeds),len(grid),6,len(METRICS)))
        for i,seed in enumerate(seeds):
            s=schedule(seed,episodes)
            assert np.bincount(s['hidden']).tolist()==[episodes//2]*2
            raw=[simulate(s,c[0],plans[c]) for c in grid]
            arrays={k:np.stack([d[j] for d in raw]) for j,k in enumerate(FIELDS)}
            archive=rawdir/f'{seed}.npz'
            np.savez_compressed(archive,**s,**arrays)
            with np.load(archive,allow_pickle=False) as f:
                stored_schedule={k:f[k] for k in s}
                trajectories={k:f[k] for k in FIELDS}
            for k,v in s.items():
                np.testing.assert_array_equal(stored_schedule[k],v)
            for j,c in enumerate(grid):
                d=tuple(trajectories[k][j] for k in FIELDS)
                for original,saved in zip(raw[j],d):
                    np.testing.assert_array_equal(original,saved)
                m,belief=reconstruct(stored_schedule,c[0],plans[c],d)
                close(m,aggregate(s['hidden'],c[0],plans[c]['fee'],plans[c]['sensing'],d,belief))
                result[i,j]=m
        checks=report(out,result,plans,seeds)
    flags=[r for r in checks if r['flag']]
    m=dict(status='REVIEW' if flags else 'PASS',mode=mode,baseline=BASE,implementation=head,
           protocol=git('rev-parse','HEAD^'),command=sys.argv,started_utc=started,
           ended_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,
           peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,architecture=platform.machine(),
           platform=platform.platform(),python=sys.version,numpy=np.__version__,seeds=list(seeds) if mode!='exact' else [],
           episodes_per_seed=episodes if mode!='exact' else 0,conditions=[list(c) for c in grid],policies=POLICIES,
           episode_count=len(seeds)*episodes*len(grid)*6 if mode!='exact' else 0,
           hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted(SOURCE.iterdir()) if p.suffix in ('.py','.md')})
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    if mode!='exact':
        (out/'audit.json').write_text(json.dumps(dict(status=m['status'],reconstructed_episodes=m['episode_count'],
                 seed_archives=len(seeds),theory_comparisons=len(checks),flags=flags,
                 uninformative_beliefs='PASS',energy_and_mortality='PASS',tolerance=1e-12),indent=2)+'\n')
    print({k:m[k] for k in ('mode','status','episode_count','elapsed_seconds','peak_rss_kib')})
    if flags:
        raise SystemExit('Investigate prespecified simulation/theory flags in audit.json.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('mode',choices=('exact','smoke','pilot'))
    args=parser.parse_args()
    run(args.output,args.mode)
