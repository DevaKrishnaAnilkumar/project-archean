"""Vectorised event simulator. Energy is measured in sixteenths."""
import numpy as np
from theory import A, SITE_TIE, RESOURCE_TIE, POLICIES

FIELDS=('history','patch','acquired','return_steps','final_ticks','spent_ticks')
METRICS=('completion','survival','acquisition','reward_returned','arrival','attempt',
         'abstention','death_before_acquisition','return_death','final_energy','net_energy','visits',
         'sensing_spent','movement_spent','expenditure','posterior','entropy',
         'conditional_completion','conditional_survival','conditional_acquisition','conditional_final_energy')


def schedule(seed,n):
    h,o,a,t,r=[np.random.default_rng(x) for x in np.random.SeedSequence(seed).spawn(5)]
    return dict(hidden=h.permutation(np.repeat([0,1],n//2)),observation=o.random((n,3,2)),
                random=a.integers(0,2,(n,3)),tie=t.integers(0,2,(n,4)),reward=r.random((n,2)))


def compile_plan(plan):
    table=np.full((85,len(POLICIES)),-1,dtype=np.int8)
    belief=np.full(85,np.nan)
    for node,row in plan['table'].items():
        table[node]=row
        belief[node]=plan['belief'][node]
    return {**plan,'actions':table,'posterior':belief,'likelihood_float':np.asarray(plan['likelihood'],float)}


def debit(energy,alive,spent,mask,cost):
    charged=alive&mask
    spent+=cost*charged
    energy-=cost*charged
    alive &= energy>0
    np.maximum(energy,0,out=energy)
    return charged


def simulate(s,initial,plan):
    h=s['hidden']
    n=len(h)
    idx=np.arange(n)
    pol=np.arange(6)[:,None]
    shape=(6,n)
    e=np.full(shape,initial*16,dtype=np.int32)
    spent=np.zeros_like(e)
    alive=np.ones(shape,bool)
    terminal=np.zeros(shape,bool)
    node=np.zeros(shape,np.int8)
    history=np.full((*shape,3),-1,dtype=np.int8)
    patch=np.full(shape,-1,dtype=np.int8)
    l=plan['likelihood_float']
    for t in range(4):
        action=plan['actions'][node,pol]
        assert np.all(action[~terminal]>=0)
        stop=~terminal&(action<A)
        act=np.where(action==RESOURCE_TIE,1+s['tie'][:,3],action)
        patch[stop]=act[stop]-1
        terminal|=stop
        if t==3:
            assert terminal.all()
            break
        sampling=~terminal
        assert np.all(e[sampling]>plan['fee'])
        side=np.where(action==SITE_TIE,np.where(pol==2,s['random'][:,t],s['tie'][:,t]),action-A)
        side=np.where(sampling,side,0)
        debit(e,alive,spent,sampling,plan['step'])
        debit(e,alive,spent,sampling,plan['sensing'])
        z=s['observation'][idx,t,side]<l[side,h]
        token=2*side+z
        history[:,:,t]=np.where(sampling,token,-1)
        node=np.where(sampling,4*node+1+token,node).astype(np.int8)
        debit(e,alive,spent,sampling,plan['step'])
    attempted=patch>=0
    assert np.all(e[attempted]>32)
    for _ in range(4):
        debit(e,alive,spent,attempted,8)
    reward=attempted&alive&(s['reward'][idx,patch]<np.where(patch==h,.85,.15))
    e+=128*reward
    returns=np.zeros(shape,np.int8)
    for _ in range(4):
        returns+=debit(e,alive,spent,attempted,8)
    return history,patch,reward,returns,e.astype(np.int16),spent.astype(np.int16)


def aggregate(h,initial,fee,sensing,raw,posterior):
    history,patch,reward,returns,e,spent=raw
    visits=(history>=0).sum(axis=-1)
    attempt=patch>=0
    survive=e>0
    complete=attempt&survive&(returns==4)
    reserve=initial-visits*fee/16
    prob=np.where(attempt,np.where(patch==h,.85,.15),0.)
    cond_trip=np.where(attempt,np.where(reserve>4,1.,prob),0.)
    cond_end=np.where(attempt,np.maximum(0,reserve-4)*(1-prob)+(reserve+4)*prob,reserve)
    entropy=-(posterior*np.log2(posterior)+(1-posterior)*np.log2(1-posterior))
    fields=(complete,survive,reward,reward&complete,attempt,attempt,~attempt,
            np.zeros_like(attempt),attempt&~survive,e/16,e/16-initial,visits,visits*sensing/16,
            (spent-visits*sensing)/16,spent/16,posterior,entropy,cond_trip,
            cond_trip+(~attempt),prob,cond_end)
    return np.stack([a.mean(axis=-1) for a in fields],axis=-1)
