"""Replay observations by posterior odds and reconstruct mortality in closed form."""
import numpy as np
from model import METRICS
from theory import A, RESOURCE_TIE, SITE_TIE


def close(a,b):
    np.testing.assert_allclose(a,b,rtol=0,atol=1e-12)


def reconstruct(s,initial,plan,raw):
    history,patch,reward,returns,end,spent=raw
    h=s['hidden']
    n=len(h)
    index=np.arange(n)
    policy=np.arange(6)[:,None]
    shape=(6,n)
    node=np.zeros(shape,np.int8)
    odds=np.ones(shape)
    stopped=np.zeros(shape,bool)
    picked=np.full(shape,-1)
    l=plan['likelihood_float']
    for t in range(4):
        a=plan['actions'][node,policy]
        now=(a<A)&~stopped
        p=odds/(1+odds)
        expected_patch=np.where(np.abs(p-.5)<=1e-12,s['tie'][:,3],p>.5)
        selected=np.where(a==RESOURCE_TIE,expected_patch,a-1)
        picked[now]=selected[now]
        stopped|=now
        if t==3:
            assert stopped.all()
            break
        event=history[:,:,t]
        side=np.where(stopped,0,np.where(a==SITE_TIE,np.where(policy==2,s['random'][:,t],s['tie'][:,t]),a-A))
        actual=s['observation'][index,t,side]<l[side,h]
        np.testing.assert_array_equal(event,np.where(stopped,-1,2*side+actual))
        ratios=np.where(actual,l[side,1]/l[side,0],(1-l[side,1])/(1-l[side,0]))
        odds*=np.where(stopped,1,ratios)
        node=np.where(stopped,node,node*4+1+event).astype(np.int8)
    np.testing.assert_array_equal(picked,patch)
    posterior=odds/(1+odds)
    close(posterior,plan['posterior'][node])
    visits=(history>=0).sum(axis=2)
    reserve=initial*16-visits*plan['fee']
    attempt=picked>=0
    assert np.all(reserve>0) and np.all(reserve[attempt]>32)
    probability=np.where(attempt,np.where(picked==h,.85,.15),0.)
    acquired=attempt&(s['reward'][index,picked]<probability)
    available=reserve-32+128*acquired
    return_steps=np.where(attempt,np.minimum(4,(available+7)//8),0)
    final=np.where(attempt,np.maximum(0,available-return_steps*8),reserve)
    cost=visits*plan['fee']+32*attempt+return_steps*8
    for expected,actual in ((acquired,reward),(return_steps,returns),(final,end),(cost,spent)):
        np.testing.assert_array_equal(expected,actual)
    if np.all(l==.55):
        close(posterior,.5)
    survive=final>0
    completed=attempt&survive
    guaranteed=reserve>64
    conditional=np.where(attempt,np.where(guaranteed,1,probability),0)
    expected_end=np.where(attempt,(np.maximum(reserve-64,0)+probability*(reserve+64-np.maximum(reserve-64,0)))/16,reserve/16)
    entropy=-posterior*np.log2(posterior)-(1-posterior)*np.log2(1-posterior)
    fields=(completed,survive,acquired,completed&acquired,attempt,attempt,~attempt,
            np.zeros_like(attempt),attempt&~survive,final/16,final/16-initial,visits,
            visits*plan['sensing']/16,(cost-visits*plan['sensing'])/16,cost/16,
            posterior,entropy,conditional,conditional+~attempt,probability,expected_end)
    assert len(fields)==len(METRICS)
    return np.array([x.mean(axis=1) for x in fields]).T,posterior
