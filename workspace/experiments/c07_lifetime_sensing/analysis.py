"""Seed-level lifetime endpoints and paired inference."""
import numpy as np
from itertools import combinations
from model import SETTINGS,POLICIES,arrangement

LABELS=('regime','initial_energy','sensor_accuracy','sensing_ticks','policy')
TCRIT=2.00957523449
ENDPOINTS=('duration','survival','scheduled_accuracy','conditional_accuracy','late_accuracy',
           'pre_reversal_accuracy','post_reversal_accuracy','acquisitions','final_energy',
           'maintenance','movement','sensing','sampled','abstentions','skipped_sensing','mapping_mass',
           'reliable_sample_share','mapping_brier','patch_brier','recovered','recovery_delay',
           'maintenance_deaths','return_deaths')


def ratio(x,den):
    return np.divide(x,den,out=np.full_like(x,np.nan,dtype=float),where=den>0)


def measures(s,d):
    ending=d['energy']
    n=ending.shape[-1]
    starting=np.concatenate((np.broadcast_to(np.array([c[1]*16 for c in SETTINGS])[None,:,None,None],
                                               (1,len(SETTINGS),6,n)),ending[:-1]),axis=0)
    before=starting>0
    maintained=starting>16
    alive=ending>0
    choose=d['patch']>=0
    sample=d['site']>=0
    hidden=s['hidden'][:,None,None,:]
    mapping=arrangement(s)[:,:,None,:]
    scheduled_correct=choose&(d['patch']==hidden)
    p=d['prior']
    mapping_mass=np.where(mapping==1,p,1-p)
    reliable=sample&(d['site']==mapping)
    fee=np.asarray([x[3] for x in SETTINGS])[None,:,None,None]
    movement=(choose*4+d['return_steps'])*.5+sample*fee*.8/16
    sense=sample*fee*.2/16
    md=before&~maintained
    rd=choose&~alive
    a=lambda x:x.sum(axis=(0,3))
    b=lambda x:x.sum(axis=0).mean(axis=-1)
    minimum=np.minimum.reduce([mapping_mass[24:46],mapping_mass[25:47],mapping_mass[26:48]])>.5
    eligible=minimum&maintained[24:46]&maintained[25:47]&maintained[26:48]
    recovered=eligible.any(axis=0)
    delay=np.where(recovered,eligible.argmax(axis=0)+1,24)
    reversals=np.array([c[0]=='reversal' for c in SETTINGS])[:,None]
    vals=[b(alive),alive[-1].mean(axis=-1),scheduled_correct.mean(axis=(0,3)),
          ratio(a(scheduled_correct),a(choose)),scheduled_correct[32:].mean(axis=(0,3)),
          ratio(a(scheduled_correct[:24]),a(choose[:24])),ratio(a(scheduled_correct[24:]),a(choose[24:])),
          b(d['acquired']),ending[-1].mean(axis=-1)/16,b(before),b(movement),b(sense),b(sample),
          b(maintained&~choose),b(maintained&~sample&np.broadcast_to(np.arange(6)[None,None,:,None]>0,alive.shape)),
          ratio(a(mapping_mass*maintained),a(maintained)),ratio(a(reliable),a(sample)),
          ratio(a((p-mapping)**2*maintained),a(maintained)),ratio(a((d['patch_belief']-hidden)**2*choose),a(choose)),
          np.where(reversals,recovered.mean(axis=-1),np.nan),np.where(reversals,delay.mean(axis=-1),np.nan),
          b(md),b(rd)]
    curves=np.stack((alive.mean(axis=-1),scheduled_correct.mean(axis=-1),
                     ratio(scheduled_correct.sum(axis=-1),choose.sum(axis=-1)),
                     ratio((mapping_mass*maintained).sum(axis=-1),maintained.sum(axis=-1)),
                     ratio(reliable.sum(axis=-1),sample.sum(axis=-1)),
                     ending.mean(axis=-1)/16,md.mean(axis=-1),rd.mean(axis=-1)),axis=-1)
    return np.stack(vals,axis=-1),curves


CURVES=('survival','scheduled_accuracy','conditional_accuracy','mapping_mass','reliable_share','energy',
        'maintenance_death','return_death')


def keys(c,p):
    return dict(zip(LABELS,(*c,p)))


def contrast(d):
    finite=d[np.isfinite(d)]
    n=len(finite)
    if not n:
        return dict(n=0,mean=None,sd=None,low=None,high=None)
    avg=float(finite.mean())
    sd=float(finite.std(ddof=1)) if n>1 else None
    if n==50:
        critical=TCRIT
    elif n>1:
        # Secondary missing-data intervals use no extrapolated critical value.
        critical=None
    else:
        critical=None
    margin=critical*sd/np.sqrt(n) if critical else None
    return dict(n=n,mean=avg,sd=sd,low=avg-margin if margin is not None else None,
                high=avg+margin if margin is not None else None)


def tables(values,seeds):
    seed,conditions,secondary,primary=[],[],[],[]
    test=[(('stable',24,.85,5),'P5','P3','duration'),(('stable',24,.85,5),'P5','P4','duration'),
          (('stable',512,.85,5),'P5','P3','late_accuracy')]
    for c,setting in enumerate(SETTINGS):
        for p,policy in enumerate(POLICIES):
            labels=keys(setting,policy)
            v=values[:,c,p]
            seed.extend(dict(seed=s,**labels,**dict(zip(ENDPOINTS,x))) for s,x in zip(seeds,v))
            counts=np.isfinite(v).sum(axis=0)
            avg=ratio(np.nansum(v,axis=0),counts)
            conditions.append(dict(**labels,**dict(zip(ENDPOINTS,avg)),
                                   **{f'n_{k}':v for k,v in zip(ENDPOINTS,counts)}))
        for b,a in combinations(range(6),2):
            for k,name in enumerate(ENDPOINTS):
                row=dict(**dict(zip(LABELS,setting)),policy_a=POLICIES[a],policy_b=POLICIES[b],
                         metric=name,**contrast(values[:,c,a,k]-values[:,c,b,k]))
                secondary.append(row)
                if (setting,POLICIES[a],POLICIES[b],name) in test:
                    primary.append(row)
    assert len(primary)==3
    return dict(per_seed=seed,condition_means=conditions,secondary_contrasts=secondary,primary_contrasts=primary)
