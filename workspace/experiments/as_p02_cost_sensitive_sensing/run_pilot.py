"""Execute the committed AS-P02 protocol."""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

import matplotlib
import numpy as np
from exact_analysis import COSTS, LIKELIHOODS, POLICIES, theory
from model import PILOT, SMOKE, entropy, schedule, simulate

T_CRIT=2.093024054


def git(*args):
    return subprocess.check_output(['git','-C',Path(__file__).resolve().parent,*args],text=True).strip()


def write(out,name,rows):
    with (out/f'{name}.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,rows[0])
        writer.writeheader()
        writer.writerows(rows)


def episode_metrics(hidden,data,fee):
    correct=data['patch']==hidden
    count=(data['sides']>=0).sum(axis=1)
    p=data['belief'][:,-1]
    true_probability=np.clip(np.where(hidden,p,1-p),1e-12,1-1e-12)
    return dict(energy=12-count*fee+8*np.where(correct,.85,.15),
                realised_energy=data['energy'][:,-1], acquired=data['acquired'],accuracy=correct,
                visits=count,observation_cost=count*fee,travel_cost=np.full(len(p),4.),
                entropy=entropy(p),brier=(p-hidden)**2,log_loss=-np.log(true_probability),
                early_stop=count<3, sequence=(data['sides']+1)@np.array([9,3,1]))


def seed_means(values):
    out={k:float(a.mean()) for k,a in values.items() if k!='sequence'}
    out.update({f'visits_{i}':float(np.mean(values['visits']==i)) for i in range(4)})
    out.update({f'sequence_{i:02}':float(np.mean(values['sequence']==i)) for i in range(27)})
    return out


def summaries(rows,expected):
    conditions, contrasts, paired, comparisons=[],[],[],[]
    for regime in LIKELIHOODS:
        for cost in COSTS:
            groups={}
            for policy in POLICIES:
                s=[row for row in rows if (row['regime'],row['cost'],row['policy'])==(regime,cost,policy)]
                groups[policy]=s
                m={k:float(np.mean([row[k] for row in s])) for k in s[0] if k not in ('seed','regime','cost','policy')}
                e=expected[regime][cost]
                v=e['policies'][policy]
                conditions.append(dict(regime=regime,cost=cost,policy=policy,**m,theory_energy=v['energy'],
                                       theory_accuracy=v['accuracy'],theory_visits=v['visits'],
                                       adaptive_benchmark=e['optimal_energy'], exact_gap=v['optimality_gap'],
                                       sampled_gap=e['optimal_energy']-m['energy']))
            for comparator in POLICIES[:-1]:
                a,b=groups['cost_sensitive'],groups[comparator]
                d=np.array([x['energy']-y['energy'] for x,y in zip(a,b)])
                mean,sd=float(d.mean()),float(d.std(ddof=1))
                m=T_CRIT*sd/np.sqrt(len(d))
                e=expected[regime][cost]['policies']
                labels=dict(regime=regime,cost=cost,comparator=comparator)
                entry=dict(**labels,n=len(d),mean=mean,sd=sd,low=mean-m,high=mean+m,
                           exact=e['cost_sensitive']['energy']-e[comparator]['energy'])
                comparisons.append(entry)
                if regime=='informative' and comparator=='fixed':
                    contrasts.append(entry)
                    paired.extend(dict(**labels,seed=x['seed'],difference=float(di)) for x,di in zip(a,d))
    return dict(condition_means=conditions,primary_contrasts=contrasts,primary_per_seed=paired,comparisons=comparisons)


def execute(out,pilot):
    start=datetime.now(timezone.utc)
    clock=time.monotonic()
    head=git('rev-parse','HEAD')
    if pilot and (head!=os.environ.get('AS_P02_IMPLEMENTATION') or git('status','--porcelain','--untracked-files=all')
                  or git('log','-1','--format=%H','--','.')!=head):
        raise ValueError('Pilot requires the recorded clean implementation commit.')
    seeds,n=(PILOT,128) if pilot else (SMOKE,8)
    out.mkdir(parents=True,exist_ok=False)
    rows=[]
    expected=theory()
    with (out/'per_episode.csv').open('w',newline='') as file:
        writer=None
        for seed in seeds:
            s=schedule(seed,n)
            np.savez_compressed(out/f'schedule_{seed}.npz',**s)
            for regime, costs in expected.items():
                for cost,plan in costs.items():
                    for policy in POLICIES:
                        prefix=f'{seed}_{regime}_{cost}_{policy}'
                        data=simulate(s,regime,cost,policy,plan)
                        np.savez_compressed(out/f'{prefix}.npz',**data)
                        values=episode_metrics(s['hidden'],data,float(COSTS[cost]))
                        labels=dict(seed=seed,regime=regime,cost=cost,policy=policy)
                        rows.append(dict(**labels,**seed_means(values)))
                        batch=[dict(**labels,episode=i,**{k:float(v[i]) for k,v in values.items()}) for i in range(n)]
                        if writer is None:
                            writer=csv.DictWriter(file,batch[0])
                            writer.writeheader()
                        writer.writerows(batch)
    write(out,'per_seed',rows)
    for name, table in summaries(rows,expected).items():
        write(out,name,table)
    manifest=dict(status='generated',mode='pilot' if pilot else 'smoke',
        public_baseline='80a67397c3d21921d1f4f5537bd93b676b279a41',
        starting_checkpoint='40fb5c3bc6375f79a05d9e736029459e1a7a1093',
        protocol_commit=git('rev-parse','HEAD^'),implementation_commit=head,
        seed_blocks=list(seeds),episodes_per_seed=n,condition_count=30,
        condition_assigned_episodes=len(rows)*n,archive_count=len(rows),
        started_utc=start.isoformat(),ended_utc=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=time.monotonic()-clock,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        command=sys.argv,python=sys.version,platform=platform.platform(),architecture=platform.machine(),
        numpy=np.__version__,matplotlib=matplotlib.__version__,
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(Path(__file__).resolve().parent.iterdir()) if p.suffix in ('.py','.md')})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pilot',action='store_true')
    group.add_argument('--smoke',action='store_true')
    args=parser.parse_args()
    execute(args.output,args.pilot)
