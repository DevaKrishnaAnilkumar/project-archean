"""Run the locked AS-P01 protocol."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

import matplotlib
import numpy as np
from model import POLICIES, REGIMES, entropy, run, schedule

SOURCE = Path(__file__).resolve().parent
BASE = '80a67397c3d21921d1f4f5537bd93b676b279a41'
T_CRITICAL = 2.093024054


def git(*args):
    return subprocess.check_output(['git', '-C', SOURCE, *args], text=True).strip()


def checkpoint(expected):
    head = git('rev-parse', 'HEAD')
    if expected != head or git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Pilot requires the recorded clean implementation commit.')
    if git('log', '-1', '--format=%H', '--', '.') != head:
        raise ValueError('Current commit is not the implementation checkpoint.')
    return head


def metrics(hidden, results):
    p = results['beliefs'][:, -1]
    h = entropy(results['beliefs'])
    clipped = np.clip(p, 1e-12, 1-1e-12)
    return dict(gain=1-h[:, -1], accuracy=results['selected']==hidden,
                brier=(p-hidden)**2, log_loss=-np.where(hidden,np.log(clipped),np.log1p(-clipped)),
                reward=results['realised'], final_energy=results['energy'][:, -1],
                gain_per_energy=(1-h[:, -1])/3.75,
                **{f'entropy_{i}': h[:, i] for i in range(1,4)},
                **{f'side_b_{i+1}': results['locations'][:, i] for i in range(3)},
                sequence=results['locations'] @ np.array([4,2,1]))


def summarize(rows, fields):
    means, contrasts = [], []
    for regime in REGIMES:
        subsets = {}
        for policy in POLICIES:
            sample = [r for r in rows if (r['regime'],r['policy'])==(regime,policy)]
            subsets[policy] = sample
            means.append(dict(regime=regime,policy=policy,**{k:float(np.mean([r[k] for r in sample])) for k in fields}))
        for comparator in ('fixed','random'):
            delta = np.array([a['gain']-b['gain'] for a,b in zip(subsets['information'],subsets[comparator])])
            mean, sd = float(delta.mean()), float(delta.std(ddof=1))
            margin = T_CRITICAL*sd/np.sqrt(len(delta)) if len(delta)==20 else None
            contrasts.append(dict(regime=regime,comparator=comparator,n=len(delta),mean=mean,sd=sd,
                                  low=mean-margin if margin is not None else None,
                                  high=mean+margin if margin is not None else None))
    return means, contrasts


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, rows[0])
        writer.writeheader()
        writer.writerows(rows)


def run_study(out, pilot, expected=None):
    if pilot:
        checkpoint(expected)
    out.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc)
    timer = time.monotonic()
    seeds, n = (range(3100,3120),128) if pilot else (range(3090,3092),8)
    rows, episodes = [], []
    for seed in seeds:
        draws = schedule(seed,n)
        np.savez_compressed(out/f'schedule_{seed}.npz', **draws)
        for regime in REGIMES:
            for policy in POLICIES:
                result = run(draws,regime,policy)
                m = metrics(draws['hidden'],result)
                np.savez_compressed(out/f'{seed}_{regime}_{policy}.npz',**result)
                labels = dict(seed=seed,regime=regime,policy=policy)
                means = {k:float(v.mean()) for k,v in m.items() if k!='sequence'}
                means.update({f'sequence_{i:03b}': float(np.mean(m['sequence']==i)) for i in range(8)})
                rows.append(dict(**labels,**means))
                episodes.extend(dict(**labels,episode=i,**{k:float(v[i]) for k,v in m.items()}) for i in range(n))
    condition, contrasts = summarize(rows,means)
    write_csv(out/'per_seed.csv',rows)
    write_csv(out/'per_episode.csv',episodes)
    write_csv(out/'condition_means.csv',condition)
    write_csv(out/'paired_contrasts.csv',contrasts)
    (out/'summary.json').write_text(json.dumps(dict(conditions=condition, contrasts=contrasts),indent=2))
    manifest = dict(baseline_commit=BASE, protocol_commit=git('rev-parse','HEAD^'),
                    implementation_commit=git('rev-parse','HEAD'), command=sys.argv,
                    started_utc=started.isoformat(), ended_utc=datetime.now(timezone.utc).isoformat(),
                    elapsed_seconds=time.monotonic()-timer, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                    platform=platform.platform(), architecture=platform.machine(), python=sys.version,
                    numpy=np.__version__, matplotlib=matplotlib.__version__,
                    seeds=list(seeds), episodes_per_seed=n, policies=POLICIES, regimes=list(REGIMES),
                    condition_assigned_episodes=len(episodes), schedule_count=len(seeds), trajectories_archives=len(rows),
                    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in sorted(SOURCE.iterdir()) if p.suffix in ('.py','.md')},
                    deviations=['Linux execution authorised by amendment 01'])
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--pilot',action='store_true')
    mode.add_argument('--smoke',action='store_true')
    args = parser.parse_args()
    import os
    run_study(args.output,args.pilot,os.environ.get('AS_P01_IMPLEMENTATION'))
