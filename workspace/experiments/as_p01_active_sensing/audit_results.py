"""Reconstruct metrics and verify matched controls from stored trajectories."""
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np

from model import POLICIES, REGIMES, TOL


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def audit(out):
    manifest=json.loads((out/'manifest.json').read_text())
    seeds=manifest['seeds']
    assert seeds in (list(range(3090,3092)),list(range(3100,3120)))
    n=128 if len(seeds)==20 else 8
    assert manifest['episodes_per_seed']==n
    episodes=read(out/'per_episode.csv')
    seed_rows=read(out/'per_seed.csv')
    assert len(episodes)==len(seeds)*6*n and len(seed_rows)==len(seeds)*6
    seed_values={}
    for seed in seeds:
        with np.load(out/f'schedule_{seed}.npz',allow_pickle=False) as data:
            s={k:data[k] for k in data.files}
        h=s['hidden']
        assert np.bincount(h).tolist()==[n//2,n//2]
        for regime,likelihood in REGIMES.items():
            control=None
            for policy in POLICIES:
                with np.load(out/f'{seed}_{regime}_{policy}.npz',allow_pickle=False) as data:
                    b,x,z,c,r,e,pos=(data[k] for k in ('beliefs','locations','observations','selected','realised','energy','positions'))
                    q = np.where(h[:,None]==[0,1],.85,.15)
                    potential=s['observation_draws'] < likelihood[:,h].T[:,None,:]
                    rewards=s['reward_draws']<q
                    np.testing.assert_array_equal(data['potential_observations'],potential)
                    np.testing.assert_array_equal(data['potential_rewards'],rewards)
                idx=np.arange(n)
                np.testing.assert_array_equal(z,potential[idx[:,None],np.arange(3),x])
                np.testing.assert_array_equal(r,rewards[idx,c])
                odds=np.ones(n)
                np.testing.assert_array_equal(b[:,0],.5)
                for t in range(3):
                    if policy=='fixed':
                        np.testing.assert_array_equal(x[:,t],(idx+t)%2)
                    if policy=='random':
                        np.testing.assert_array_equal(x[:,t],s['random_sides'][:,t])
                    if policy=='information':
                        prior=b[:,t]
                        gains=[]
                        for probs in likelihood:
                            expected=np.zeros(n)
                            for pair in (probs,1-probs):
                                prob=(1-prior)*pair[0]+prior*pair[1]
                                posterior=prior*pair[1]/prob
                                expected+=prob*(-posterior*np.log2(posterior)-(1-posterior)*np.log2(1-posterior))
                            gains.append(-expected)
                        diff=gains[1]-gains[0]
                        np.testing.assert_array_equal(x[:,t],np.where(abs(diff)<=TOL,s['tie_sides'][:,t],diff>0))
                    l=np.where(z[:,t,None],likelihood[x[:,t]],1-likelihood[x[:,t]])
                    odds*=l[:,1]/l[:,0]
                    np.testing.assert_allclose(b[:,t+1],odds/(1+odds),rtol=0,atol=TOL)
                p=b[:,-1]
                np.testing.assert_array_equal(c,np.where(abs(p-.5)<=TOL,s['tie_sides'][:,3],p>.5))
                np.testing.assert_array_equal(pos[:,[0,3,6,9,18]],0)
                np.testing.assert_array_equal(pos[:,[1,4,7],0],2*x-1)
                np.testing.assert_array_equal(pos[:,13,1],4*(2*c-1))
                changes=np.abs(np.diff(pos,axis=1)).sum(axis=2)
                np.testing.assert_array_equal(changes.sum(axis=1),14)
                assert changes.max()==1
                delta=np.diff(e,axis=1)
                expected=-.5*changes
                expected[:,[1,4,7]]=-.25
                expected[:,13]=8*r
                np.testing.assert_array_equal(delta,expected)
                assert (e>0).all()
                np.testing.assert_array_equal(e[:,-1],8.25+8*r)
                if regime=='uninformative':
                    np.testing.assert_array_equal(b,.5)
                    if control is None:
                        control=c,r,e[:,-1]
                    else:
                        for actual, saved in zip((c,r,e[:,-1]),control):
                            np.testing.assert_array_equal(actual,saved)
                entropy=-(b*np.log2(b)+(1-b)*np.log2(1-b))
                pp=np.clip(p,1e-12,1-1e-12)
                v=dict(gain=1-entropy[:,-1],accuracy=c==h,brier=(p-h)**2,log_loss=-np.log(np.where(h,pp,1-pp)),
                       reward=r,final_energy=e[:,-1],gain_per_energy=(1-entropy[:,-1])/3.75,
                       **{f'entropy_{t}':entropy[:,t] for t in range(1,4)},
                       **{f'side_b_{t+1}':x[:,t] for t in range(3)},sequence=4*x[:,0]+2*x[:,1]+x[:,2])
                filt=lambda row: (row['seed'],row['regime'],row['policy'])==(str(seed),regime,policy)
                ep=[row for row in episodes if filt(row)]
                sr,=[row for row in seed_rows if filt(row)]
                assert [int(row['episode']) for row in ep]==list(range(n))
                for k,a in v.items():
                    np.testing.assert_allclose([float(row[k]) for row in ep],a,rtol=0,atol=TOL)
                m={k:float(a.mean()) for k,a in v.items() if k!='sequence'}
                m.update({f'sequence_{i:03b}':float(np.mean(v['sequence']==i)) for i in range(8)})
                for k,a in m.items():
                    assert abs(float(sr[k])-a)<=TOL
                seed_values[seed,regime,policy]=m
    means=read(out/'condition_means.csv')
    assert len(means)==6
    for row in means:
        r,p=row['regime'],row['policy']
        for k in m:
            assert abs(float(row[k])-np.mean([seed_values[s,r,p][k] for s in seeds]))<=TOL
    contrasts=read(out/'paired_contrasts.csv')
    assert len(contrasts)==4
    for row in contrasts:
        r,p=row['regime'],row['comparator']
        d=[seed_values[s,r,'information']['gain']-seed_values[s,r,p]['gain'] for s in seeds]
        avg=float(np.mean(d))
        sd=float(np.std(d,ddof=1))
        assert abs(avg-float(row['mean']))<=TOL and abs(sd-float(row['sd']))<=TOL
        if len(seeds)==20:
            margin=2.093024054*sd/math.sqrt(20)
            assert abs(avg-margin-float(row['low']))<=TOL and abs(avg+margin-float(row['high']))<=TOL
    summary=json.loads((out/'summary.json').read_text())
    for kind,table in [('conditions',means),('contrasts',contrasts)]:
        for j,row in enumerate(summary[kind]):
            assert all(('' if value is None else str(value))==table[j][key] for key,value in row.items())
    report=dict(status='PASS',seed_blocks=len(seeds),condition_assigned_episodes=len(episodes),conditions=6,
                negative_control='PASS',resource_movement_energy=4.,sampling_energy=3.75)
    (out/'audit_results.json').write_text(json.dumps(report,indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    report=audit(args.output)
    print(json.dumps(report,indent=2))
