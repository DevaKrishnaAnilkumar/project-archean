"""Lock-check, execute and reconstruct the C07 lifetime experiment."""
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
import numpy as np
from analysis import CURVES,measures,tables
from audit import reconstruct
from model import SETTINGS,POLICIES,schedule,simulate

SOURCE=Path(__file__).resolve().parent
BASE='22dfd6ce97be82a32d1b9275b55bb90f6f57221d'


def git(*args):
    return subprocess.check_output(['git','-C',SOURCE,*args],text=True).strip()


def run(out,mode):
    started=datetime.now(timezone.utc).isoformat()
    clock=time.monotonic()
    head=git('rev-parse','HEAD')
    if mode=='pilot':
        assert head==os.environ.get('C07_IMPLEMENTATION') and not git('status','--porcelain','--untracked-files=all')
        assert git('log','-1','--format=%H','--','.')==head
    seeds=tuple(range(3500,3550)) if mode=='pilot' else (3490,3491)
    out.mkdir(parents=True,exist_ok=False)
    raw=out/'raw'
    raw.mkdir()
    means,curves=[],[]
    actual=choices=deaths=0
    for seed in seeds:
        s=schedule(seed)
        assert np.array_equal(np.bincount(s['initial_mapping']),[16,16])
        assert np.array_equal(np.bincount(s['fixed']),[16,16])
        data=simulate(s)
        path=raw/f'{seed}.npz'
        np.savez_compressed(path,**s,**data)
        with np.load(path,allow_pickle=False) as f:
            archived_schedule={k:f[k] for k in s}
            d={k:f[k] for k in data}
        for k,v in s.items():
            np.testing.assert_array_equal(v,archived_schedule[k])
        for k,v in data.items():
            np.testing.assert_array_equal(v,d[k])
        reconstruct(archived_schedule,d)
        m,c=measures(archived_schedule,d)
        means.append(m)
        curves.append(c)
        actual+=d['energy'][0].size+int((d['energy'][:-1]>0).sum())
        choices+=int((d['patch']>=0).sum())
        deaths+=int((d['energy'][-1]==0).sum())
    for name,rows in tables(np.asarray(means),seeds).items():
        with (out/f'{name}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,rows[0])
            w.writeheader()
            w.writerows(rows)
    np.savez_compressed(out/'seed_curves.npz',values=np.array(curves),seeds=seeds,metrics=CURVES)
    m=dict(status='PASS',mode=mode,baseline=BASE,implementation=head,protocol=git('rev-parse','HEAD^'),
           started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
           elapsed_seconds=time.monotonic()-clock,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           architecture=platform.machine(),platform=platform.platform(),python=sys.version,numpy=np.__version__,
           seeds=seeds,settings=SETTINGS,policies=POLICIES,organisms_per_seed_condition=32,periods=48,
           scheduled_periods=len(seeds)*len(SETTINGS)*len(POLICIES)*32*48,maintenance_events=actual,
           resource_choices=choices,deaths=deaths,
           hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.iterdir()) if p.suffix in ('.py','.md')})
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    (out/'audit.json').write_text(json.dumps(dict(status='PASS',seed_archives=len(seeds),
           reconstructed_scheduled_periods=m['scheduled_periods'],controls=['maintenance and energy continuity',
           'permanent mortality','reward timing','independent Bayesian feedback likelihood',
           'frozen beliefs and q=0.5 negative controls','high energy survival'],atol=1e-12),indent=2)+'\n')
    print({k:m[k] for k in ('mode','status','scheduled_periods','resource_choices','deaths','elapsed_seconds','peak_rss_kib')})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('mode',choices=('smoke','pilot'))
    args=parser.parse_args()
    run(args.output,args.mode)
