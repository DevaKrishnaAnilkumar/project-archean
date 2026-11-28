"""Reconstruct archived episode outcomes using independent odds and cost calculations."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from exact_analysis import COSTS, LIKELIHOODS, POLICIES, theory
from run_pilot import summaries


def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def eq(a,b):
    np.testing.assert_allclose(a,b,atol=1e-12,rtol=0)


def reconstruct(draws,raw,regime,cost,policy,plan):
    h=draws['hidden']
    n=len(h)
    idx=np.arange(n)
    l=np.array(LIKELIHOODS[regime],float)
    fee=float(COSTS[cost])
    potential=draws['observations'] < l[:,h].T[:,None,:]
    rewards=draws['rewards'] < (.15+.70*(h[:,None]==np.arange(2)))
    eq(raw['potential_observations'],potential)
    eq(raw['potential_rewards'],rewards)
    odds=np.ones(n)
    active=np.ones(n,dtype=bool)
    eq(raw['belief'][:,0],.5)
    for t in range(3):
        p=odds/(1+odds)
        if policy=='fixed':
            seq=plan['fixed_sequence']
            choice=np.full(n,seq[t] if t<len(seq) else -1)
        elif policy=='random':
            choice=draws['random'][:,t] if t<plan['random_count'] else np.full(n,-1)
        elif policy=='no_sensing':
            choice=np.full(n,-1)
        else:
            scores=np.zeros((n,2))
            for result in [0,1]:
                v=l if result else 1-l
                a,b=(1-p[:,None])*v[:,0],p[:,None]*v[:,1]
                if policy=='entropy':
                    scores+=a*np.log2(a/(a+b))+b*np.log2(b/(a+b))
                else:
                    scores+=5.6*np.maximum(a,b)
            d=scores[:,1]-scores[:,0]
            choice=np.where(abs(d)<=1e-12,draws['ties'][:,t],d>0)
            if policy=='cost_sensitive':
                choice=np.where(scores.max(axis=1)-5.6*np.maximum(p,1-p)>fee+1e-12,choice,-1)
        active &= choice>=0
        choice=np.where(active,choice,-1)
        eq(raw['sides'][:,t],choice)
        obs=potential[idx,t,choice]
        eq(raw['observed'][:,t],np.where(active,obs,-1))
        ratio=np.where(obs[:,None],l[choice],1-l[choice])
        odds*=np.where(active,ratio[:,1]/ratio[:,0],1)
        eq(raw['belief'][:,t+1],odds/(1+odds))
    p=odds/(1+odds)
    pick=np.where(abs(p-.5)<=1e-12,draws['ties'][:,3],p>.5)
    acquired=rewards[idx,pick]
    eq(raw['patch'],pick)
    eq(raw['acquired'],acquired)
    sides=raw['sides']
    visit=sides>=0
    count=visit.sum(axis=1)
    expected_pos=np.zeros((n,19,2))
    expected_pos[:,[1,2,4,5,7,8],0]=np.repeat(np.where(visit,2*sides-1,0),2,axis=1)
    expected_pos[:,10:,1]=(2*pick[:,None]-1)*[1,2,3,4,4,3,2,1,0]
    eq(raw['position'],expected_pos)
    delta=np.full((n,18),-.5)
    delta[:,:9]=(visit[...,None]*[-.4*fee,-.2*fee,-.4*fee]).reshape(n,9)
    delta[:,13]=8*acquired
    eq(raw['energy'][:,0],16)
    eq(np.diff(raw['energy'],axis=1),delta)
    assert (raw['energy']>0).all()
    correct=pick==h
    if regime=='uninformative':
        eq(raw['belief'],.5)
        eq(count,3 if policy=='entropy' else 0)
        eq(pick,draws['ties'][:,3])
        eq(acquired,rewards[idx,draws['ties'][:,3]])
    probability=np.clip(np.where(h==1,p,1-p),1e-12,1-1e-12)
    return dict(energy=12-count*fee+8*(.15+.70*correct),realised_energy=12-count*fee+8*acquired,
                acquired=acquired,accuracy=correct,visits=count,observation_cost=count*fee,
                travel_cost=np.full(n,4.),entropy=-np.log2(p)*p-np.log2(1-p)*(1-p),
                brier=np.square(p-h),log_loss=-np.log(probability),early_stop=count<3,
                sequence=9*(sides[:,0]+1)+3*(sides[:,1]+1)+sides[:,2]+1)


def audit(out):
    m=json.loads((out/'manifest.json').read_text())
    seeds=list(range(3200,3220)) if m['mode']=='pilot' else [3190,3191]
    n=128 if m['mode']=='pilot' else 8
    assert m['seed_blocks']==seeds and m['episodes_per_seed']==n
    assert len(list(out.glob('*.npz')))==31*len(seeds)
    ep=iter(rows(out/'per_episode.csv'))
    seed_rows=[]
    expected=theory()
    for s in seeds:
        with np.load(out/f'schedule_{s}.npz',allow_pickle=False) as f:
            draws=dict(f)
        assert np.bincount(draws['hidden']).tolist()==[n//2,n//2]
        for regime in LIKELIHOODS:
            for cost in COSTS:
                for policy in POLICIES:
                    with np.load(out/f'{s}_{regime}_{cost}_{policy}.npz',allow_pickle=False) as raw:
                        values=reconstruct(draws,raw,regime,cost,policy,expected[regime][cost])
                    for i in range(n):
                        row=next(ep)
                        assert [row[k] for k in ('seed','regime','cost','policy','episode')]==[str(s),regime,cost,policy,str(i)]
                        eq([float(row[k]) for k in values],[v[i] for v in values.values()])
                    result={k:float(np.sum(v)/n) for k,v in values.items() if k!='sequence'}
                    for label,count in [('visits',4),('sequence',27)]:
                        for i,v in enumerate(np.bincount(values[label],minlength=count)/n):
                            result[f'{label}_{i:02}' if label=='sequence' else f'{label}_{i}']=float(v)
                    seed_rows.append(dict(seed=s,regime=regime,cost=cost,policy=policy,**result))
    assert next(ep,None) is None
    comparisons=summaries(seed_rows,expected)
    for name, calculated in dict(per_seed=seed_rows,**comparisons).items():
        documented=rows(out/f'{name}.csv')
        assert len(documented)==len(calculated)
        for a,b in zip(calculated,documented):
            assert set(a)==set(b)
            for key,val in a.items():
                if isinstance(val,str):
                    assert val==b[key]
                else:
                    eq(val,float(b[key]))
    theory_checks=[]
    if n==128:
        for r in comparisons['condition_means']:
            subset=[row for row in seed_rows if all(row[k]==r[k] for k in ('regime','cost','policy'))]
            targets=dict(energy=r['theory_energy'],accuracy=r['theory_accuracy'],visits=r['theory_visits'],
                         realised_energy=r['theory_energy'])
            for metric,target in targets.items():
                se=float(np.std([row[metric] for row in subset],ddof=1)/np.sqrt(len(seeds)))
                difference=r[metric]-target
                theory_checks.append(dict(regime=r['regime'],cost=r['cost'],policy=r['policy'],
                                          metric=metric,difference=difference,se=se))
                assert abs(difference)<=max(1e-12,4*se),theory_checks[-1]
    report=dict(status='PASS',episodes=len(seed_rows)*n,conditions_per_seed=30,seed_blocks=len(seeds),
                negative_control='PASS',theory_checks=theory_checks)
    (out/'audit_results.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('results',type=Path)
    print(json.dumps(audit(parser.parse_args().results),indent=2))
