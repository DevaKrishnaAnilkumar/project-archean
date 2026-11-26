"""Pre-specified v2.3.1 runner. Smoke mode never uses designated research seeds."""
import argparse
import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
from model import SEEDS, ARMS, WORLDS, BUDGETS, FAMILIES, TRIALS, schedules, simulate, summarise

HERE = Path(__file__).resolve().parent
CONDITIONS = tuple((arm, world, budget) for arm in ARMS for world in WORLDS for budget in BUDGETS)
SMOKE_SEEDS = (101, 102)
T_CRITICAL = 2.02269092
BASELINE = 'e0f65f897597377a337a64bbc0fe51c8056075ec'
BRANCH = 'research/v2.3-lifetime-learning'
SOURCE_FILES = ('PROTOCOL.md', 'IMPLEMENTATION.md', 'model.py', 'test_model.py',
                'run_study.py', 'test_runner.py', 'ANALYSIS.md')


def git(*args):
    return subprocess.check_output(['git', '-C', str(HERE), *args], text=True).strip()


def research_checkpoint():
    head = git('rev-parse', 'HEAD')
    if git('branch', '--show-current') != BRANCH or git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Full study requires the clean dedicated research branch')
    if not git('rev-parse', 'HEAD^').startswith('f484a1f') or git('rev-parse', 'HEAD^^') != BASELINE:
        raise ValueError('Full study requires the implementation commit directly after the protocol')
    if git('rev-parse', '--abbrev-ref', '@{upstream}') != 'origin/' + BRANCH:
        raise ValueError('Publish the pre-execution branch first')
    if git('rev-parse', '@{upstream}') != head:
        raise ValueError('Local and remote-tracking checkpoints differ')
    for name in SOURCE_FILES:
        git('ls-files', '--error-unmatch', str(HERE / name))
    return head


def interval(values):
    """Exactly the pre-specified 40-seed paired t interval."""
    a = np.asarray(values, dtype=float)
    if a.shape != (40,) or not np.isfinite(a).all():
        raise ValueError('Expected 40 finite seed-level contrasts')
    mean = float(a.mean())
    sd = float(a.std(ddof=1))
    half = T_CRITICAL * sd / math.sqrt(40)
    return dict(n=40, mean=mean, sample_sd=sd, lower_95=mean-half, upper_95=mean+half)


def primary(rows):
    return rows['adaptive','stable',160]['late_acquisition_correct_all'] - rows['frozen','stable',160]['late_acquisition_correct_all']


def contrasts(rows):
    result = {'primary_adaptive_minus_frozen': primary(rows)}
    a = rows['adaptive','reversed',160]
    result['reversal_late_minus_early'] = a['late_reversal_correct_all'] - a['early_reversal_correct_all']
    result['reversal_late_minus_stable'] = a['late_reversal_correct_all'] - rows['adaptive','stable',160]['late_reversal_correct_all']
    result['genuine_minus_blind_late_acquisition'] = rows['adaptive','stable',160]['late_acquisition_correct_all'] - rows['cue_blind','stable',160]['late_acquisition_correct_all']
    for world in WORLDS:
        for budget in BUDGETS:
            for control in ('frozen','cue_blind'):
                for metric in ('survival','final_energy'):
                    result[f'{world}_{budget}_adaptive_minus_{control}_{metric}'] = rows['adaptive',world,budget][metric] - rows[control,world,budget][metric]
    return result


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def write_json(path, data):
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, allow_nan=False); f.write('\n')


def run(out, *, smoke, checkpoint=None):
    if not smoke:
        verified = research_checkpoint()
        if checkpoint != verified:
            raise ValueError('Full study requires verified checkpoint')
    seeds = SMOKE_SEEDS if smoke else SEEDS
    n = 4 if smoke else FAMILIES
    out = Path(out).resolve()
    # Never place results or smoke files in the source repository.
    try:
        root = Path(git('rev-parse','--show-toplevel')).resolve()
    except subprocess.CalledProcessError:
        if not smoke:
            raise
        root = HERE
    if out == root or root in out.parents:
        raise ValueError('Choose an output directory outside the source repository')
    out.mkdir(parents=True, exist_ok=False)
    raw = out / 'raw'; raw.mkdir()
    write_json(out/'manifest.json', dict(mode='smoke' if smoke else 'research', seeds=list(seeds),
        cohort_size=n, trials=TRIALS, conditions=[list(c) for c in CONDITIONS], checkpoint=checkpoint,
        python=sys.version, numpy=np.__version__, platform=platform.platform(), architecture=platform.machine(),
        source_sha256={name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in SOURCE_FILES if (HERE/name).is_file()}))
    rows = []; paired = []; trial_counts = []; deaths = []
    for seed in seeds:
        s = schedules(seed,n)
        sd = raw / str(seed); sd.mkdir()
        np.savez_compressed(sd/'schedules.npz', **s)
        by_condition = {}; prefix = {}
        for arm,world,budget in CONDITIONS:
            d = simulate(s,arm,world,budget)
            key = (arm,world,budget)
            # Enforce the prereversal match on every actual condition, not just unit tests.
            if world == 'stable':
                prefix[arm,budget] = {k:v[:17 if k in ('energy','position','alive','memory') else 16].copy() for k,v in d.items()}
            else:
                for k,v in prefix[arm,budget].items():
                    np.testing.assert_array_equal(v,d[k][:len(v)],err_msg=f'{seed} {arm} {budget} {k}')
            if budget == 160 and not d['alive'].all():
                raise ValueError('High-energy mortality violates protocol')
            np.testing.assert_array_equal(d['energy'][1:],d['energy'][:-1]-.5*d['steps']+8*(d['reward']==1))
            np.savez_compressed(sd/f'{arm}_{world}_{budget}.npz', **d)
            m = summarise(d); by_condition[key] = m
            ident = dict(seed=seed,arm=arm,world=world,budget=budget)
            rows.append(dict(**ident, **m))
            for t in range(TRIALS):
                chosen=d['action'][t]>=0
                trial_counts.append(dict(**ident, encounter=t+1, scheduled=n, choices=int(chosen.sum()),
                    correct=int((chosen & (d['action'][t]==d['good'][t])).sum()),
                    rewards=int((d['reward'][t]==1).sum()), alive_after=int(d['alive'][t+1].sum())))
                for step in range(1,9):
                    deaths.append(dict(**ident, encounter=t+1, movement_step=step, deaths=int((d['death_step'][t]==step).sum())))
        paired.append(dict(seed=seed, **contrasts(by_condition)))
    write_csv(out/'per_seed.csv',rows); write_csv(out/'paired_contrasts.csv',paired)
    write_csv(out/'trial_counts.csv',trial_counts); write_csv(out/'death_counts.csv',deaths)
    # Aggregate counts, retaining the denominators. These are descriptive, not independent samples.
    totals = {}
    for r in trial_counts:
        key = tuple(r[k] for k in ('arm','world','budget','encounter'))
        acc = totals.setdefault(key,dict(arm=key[0],world=key[1],budget=key[2],encounter=key[3],scheduled=0,choices=0,correct=0,rewards=0,alive_after=0))
        for k in ('scheduled','choices','correct','rewards','alive_after'): acc[k]+=r[k]
    aggregate=[]
    for a in totals.values():
        aggregate.append(dict(**a, correct_all=a['correct']/a['scheduled'],correct_conditional=a['correct']/a['choices'] if a['choices'] else float('nan')))
    write_csv(out/'trial_aggregate.csv',aggregate)
    group=[]
    for arm,world,budget in CONDITIONS:
        subset=[r for r in rows if (r['arm'],r['world'],r['budget'])==(arm,world,budget)]
        keys=('late_acquisition_correct_all','early_reversal_correct_all','late_reversal_correct_all','all_correct_all','survival','final_energy','acquisition_rate','mean_completed_trips')
        group.append(dict(arm=arm,world=world,budget=budget,**{k:float(np.mean([r[k] for r in subset])) for k in keys}))
    write_csv(out/'condition_means.csv',group)
    result=dict(mode='smoke' if smoke else 'research',seed_count=len(seeds),condition_rows=len(rows))
    if not smoke:
        main=interval([p['primary_adaptive_minus_frozen'] for p in paired])
        main['supports_primary']=main['lower_95']>0
        result['primary']=main
        result['exploratory_mean_contrasts']={k:float(np.mean([p[k] for p in paired])) for k in paired[0] if k not in ('seed','primary_adaptive_minus_frozen')}
    write_json(out/'summary.json',result)
    # A missing completion marker means output may be partial and must not be analysed.
    write_json(out/'COMPLETE.json',dict(mode=result['mode'],seed_count=len(seeds),condition_rows=len(rows),raw_archives=len(seeds)*(1+len(CONDITIONS))))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--smoke',action='store_true'); mode.add_argument('--research',action='store_true')
    args=p.parse_args()
    checkpoint=None if args.smoke else research_checkpoint()
    result=run(args.output,smoke=args.smoke,checkpoint=checkpoint)
    print(json.dumps(result,indent=2,allow_nan=False))
    print('COMPLETE:',args.output.resolve())

if __name__=='__main__': main()
