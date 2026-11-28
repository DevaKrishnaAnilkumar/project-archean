"""Reconstruct raw lifetimes with independent joint likelihoods and energy accounting."""
import numpy as np
from model import SETTINGS


def eq(a,b):
    np.testing.assert_allclose(a,b,atol=1e-12,rtol=0)


def reconstruct(s,d,settings=SETTINGS):
    initial,q,fee=(np.array([c[k] for c in settings])[:,None,None] for k in (1,2,3))
    n=len(s['initial_mapping'])
    shape=(len(settings),6,n)
    e=np.broadcast_to(initial*16,shape).copy()
    odds=np.ones(shape)*.5
    pids=np.arange(6)[None,:,None]
    learners=(pids==3)|(pids==4)

    for t,h in enumerate(s['hidden']):
        h=h[None,None,:]
        m=np.array([s['unpredictable'][t] if c[0]=='unpredictable' else
                    1-s['initial_mapping'] if c[0]=='reversal' and t>=24 else s['initial_mapping']
                    for c in settings])[:,None,:]
        maintained=np.maximum(e-16,0)
        current=maintained>0
        prior=np.where(current&learners&(t>0),odds+(1-2*odds)*.05,odds)
        prior=np.where(current&(pids==5),m,prior)
        eq(d['prior'][t],prior)
        visit=current&(pids!=0)&(maintained-fee>32)
        preferred=np.where(np.abs((q-.5)*(2*prior-1))<=1e-12,s['ties'][t,:,0],prior>.5)
        site=np.where(np.isin(pids,[1,3]),(s['fixed']+t)%2,np.where(pids==5,m,preferred))
        site=np.where(visit,site,-1)
        eq(d['site'][t],site)
        u=s['potential'][t,np.arange(n),np.maximum(site,0)]
        sensor_accuracy=np.where(site==m,q,.5)
        z=np.where(visit,np.where(u<sensor_accuracy,h,1-h),-1)
        eq(d['obs'][t],z)
        reliability_mass=np.where(site==0,1-prior,prior)
        sensor_p=.5*(1-reliability_mass)+q*reliability_mass
        h1=np.where(visit,np.where(z==1,sensor_p,1-sensor_p),.5)
        eq(d['patch_belief'][t],h1)
        reserve=maintained-visit*fee
        attempt=reserve>32
        patch=np.where(attempt,np.where(abs(h1-.5)<=1e-12,s['ties'][t,:,1],h1>.5),-1)
        eq(d['patch'][t],patch)
        u=s['reward_draws'][t,np.arange(n),np.maximum(patch,0)]
        got=attempt&(u<(.15+.70*(patch==h)))
        eq(d['acquired'][t],got)
        # Agreement of reading and chosen patch determines joint evidence.
        # For a sensor of accuracy a, P(reward | reading, choice) = .15+.70*a
        # when reading agrees with choice; otherwise replace a by 1-a.
        evidence=[]
        for i in range(2):
            acc=np.where(site==i,q,.5)
            reward=.15+.70*np.where(z==patch,acc,1-acc)
            evidence.append(np.where(got,reward,1-reward))
        n1=prior*evidence[1]
        n0=(1-prior)*evidence[0]
        odds=np.where(visit&attempt&learners,n1/(n0+n1),prior)
        eq(d['memory'][t],odds)
        arrived=reserve-32+128*got
        steps=np.where(attempt,np.minimum(4,(arrived+7)//8),0)
        eq(d['return_steps'][t],steps)
        ending=np.where(attempt,np.maximum(0,arrived-8*steps),reserve)
        eq(d['energy'][t],ending)
        assert np.all((e!=0)|(ending==0))
        e=ending
    assert np.all(d['energy'][:,initial[:,0,0]==512]>0)
    for i,c in enumerate(settings):
        if c[2]==.5:
            eq(d['memory'][:,i,1:5],.5)
            eq(d['patch_belief'][:,i],.5)
