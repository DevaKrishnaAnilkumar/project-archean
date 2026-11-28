"""Continuous-lifetime sensing with integer energy and feedback-based inference."""
from itertools import product
import numpy as np

SETTINGS=tuple((r,e,.85,5) for r,e in product(('stable','reversal','unpredictable'),(8,24,512)))+(
    ('stable',4,.85,5),('reversal',4,.85,5),('stable',8,.85,40),('reversal',8,.85,40),
    ('stable',512,.5,5),('reversal',512,.5,5))
PERIODS=48
POLICIES=('P1','P2','P3','P4','P5','P6')
LEARN=np.isin(np.arange(6)[None,:,None],[3,4])
ORACLE=np.arange(6)[None,:,None]==5
FIXED=np.isin(np.arange(6)[None,:,None],[1,3])
SENSING=np.arange(6)[None,:,None]!=0


def schedule(seed,n=32):
    streams=dict(zip(('hidden','mapping','potential','reward','ties','fixed'),
                     map(np.random.default_rng,np.random.SeedSequence(seed).spawn(6))))
    return dict(hidden=streams['hidden'].integers(0,2,(48,n),dtype=np.int8),
                initial_mapping=streams['mapping'].permutation(np.tile([0,1],n//2)),
                unpredictable=streams['mapping'].integers(0,2,(48,n),dtype=np.int8),
                potential=streams['potential'].random((48,n,2)),
                reward_draws=streams['reward'].random((48,n,2)),
                ties=streams['ties'].integers(0,2,(48,n,2),dtype=np.int8),
                fixed=streams['fixed'].permutation(np.tile([0,1],n//2)))


def arrangement(s,settings=SETTINGS):
    schedules=[]
    for r,*_ in settings:
        x=np.broadcast_to(s['initial_mapping'],s['hidden'].shape)
        if r=='reversal':
            x=x^(np.arange(48)[:,None]>=24)
        elif r=='unpredictable':
            x=s['unpredictable']
        schedules.append(x)
    return np.stack(schedules,axis=1)


def feedback(prior,side,obs,patch,got,q):
    """Bayes update integrating H=0 and H=1 for each M hypothesis."""
    lh=[]
    for mapping in (0,1):
        a=np.where(side==mapping,q,.5)
        b=np.zeros_like(prior)
        for hidden in (0,1):
            obs_prob=np.where(obs==hidden,a,1-a)
            reward_prob=np.where(patch==hidden,.85,.15)
            b+=.5*obs_prob*np.where(got,reward_prob,1-reward_prob)
        lh.append(b)
    return prior*lh[1]/((1-prior)*lh[0]+prior*lh[1])


def debit(energy,alive,mask,ticks):
    charged=alive&mask
    energy-=ticks*charged
    alive &= energy>0
    np.maximum(energy,0,out=energy)
    return charged


def simulate(s,settings=SETTINGS):
    initial,q,fee=(np.array([c[k] for c in settings])[:,None,None] for k in (1,2,3))
    shape=(len(settings),6,len(s['initial_mapping']))
    e=np.broadcast_to(initial*16,shape).astype(np.int32).copy()
    prior=np.full(shape,.5)
    alive=np.ones(shape,bool)
    mappings=arrangement(s,settings)
    data={k:np.empty((48,*shape),dtype=typ) for k,typ in [
        ('energy',np.int32),('site',np.int8),('obs',np.int8),('patch',np.int8),
        ('acquired',bool),('return_steps',np.int8),('prior',float),('memory',float),('patch_belief',float)]}
    site_ids=np.arange(2)[None,None,:]
    for t,hidden in enumerate(s['hidden']):
        mapping=mappings[t,:,None,:]
        debit(e,alive,alive,16)
        if t:
            prior=np.where(alive&LEARN,.05+.9*prior,prior)
        prior=np.where(alive&ORACLE,mapping,prior)
        data['prior'][t]=prior
        sample=alive&SENSING&(e>fee+32)
        best=np.where(np.abs((q-.5)*(2*prior-1))<=1e-12,s['ties'][t,:,0],prior>.5)
        site=np.where(FIXED,s['fixed']^(t%2),np.where(ORACLE,mapping,best))
        site=np.where(sample,site,-1)
        chance=np.where(site_ids==mappings[t,:,:,None],q,.5)
        possible=np.where(s['potential'][t]<chance,hidden[None,:,None],1-hidden[None,:,None])
        obs=possible[np.arange(len(settings))[:,None,None],np.arange(len(hidden)),site]
        obs=np.where(sample,obs,-1)
        debit(e,alive,sample,fee*2//5)
        debit(e,alive,sample,fee//5)
        debit(e,alive,sample,fee*2//5)
        probability=.5+(q-.5)*np.where(site==1,prior,1-prior)
        p=np.where(sample,np.where(obs==1,probability,1-probability),.5)
        attempt=alive&(e>32)
        patch=np.where(attempt,np.where(abs(p-.5)<=1e-12,s['ties'][t,:,1],p>.5),-1)
        for _ in range(4):
            debit(e,alive,attempt,8)
        acquired=alive&attempt&(s['reward_draws'][t,np.arange(len(hidden)),patch]<np.where(patch==hidden,.85,.15))
        e+=128*acquired
        posterior=feedback(prior,site,obs,patch,acquired,q)
        prior=np.where(alive&attempt&sample&LEARN,posterior,prior)
        steps=np.zeros(shape,np.int8)
        for _ in range(4):
            steps+=debit(e,alive,attempt,8)
        for k,v in zip(data, (e,site,obs,patch,acquired,steps,data['prior'][t],prior,p)):
            data[k][t]=v
    return data
