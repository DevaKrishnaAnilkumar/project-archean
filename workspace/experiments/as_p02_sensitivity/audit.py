"""Reconstruct simulated actions and outcomes independently from stored arrays."""
import numpy as np


def eq(a,b):
    np.testing.assert_allclose(a,b,rtol=0,atol=1e-12)


def reconstruct(s,d,k,policy,plan):
    l,fee,sequence,count,_=plan
    l=np.asarray(l)
    h=s['hidden']
    n=len(h)
    idx=np.arange(n)
    potential=s['observations'][:,:k]<l[:,h].T[:,None,:]
    rewards=s['rewards']<np.where(h[:,None]==[0,1],.85,.15)
    eq(d['potential'],potential)
    eq(d['potential_rewards'],rewards)
    odds=np.ones(n)
    active=np.ones(n,dtype=bool)
    eq(d['beliefs'][:,0],.5)
    for t in range(k):
        p=odds/(1+odds)
        if policy=='fixed':
            action=np.full(n,sequence[t] if t<len(sequence) else -1)
        elif policy=='random':
            action=s['random'][:,t] if t<count else np.full(n,-1)
        elif policy=='no_sensing':
            action=np.full(n,-1)
        else:
            value=np.zeros((n,2))
            for l0,l1 in (l.T,(1-l).T):
                a=(1-p[:,None])*l0
                b=p[:,None]*l1
                if policy=='entropy':
                    value+=a*np.log2(a/(a+b))+b*np.log2(b/(a+b))
                else:
                    value+=5.6*np.maximum(a,b)
            diff=value[:,1]-value[:,0]
            action=np.where(abs(diff)<=1e-12,s['ties'][:,t],diff>0).astype(int)
            if policy=='cost_sensitive':
                action=np.where(value.max(axis=1)-5.6*np.maximum(p,1-p)-fee>1e-12,action,-1)
        active &= action>=0
        action=np.where(active,action,-1)
        obs=potential[idx,t,action]
        eq(d['sides'][:,t],action)
        eq(d['observed'][:,t],np.where(active,obs,-1))
        lr=np.where(obs[:,None],l[action],1-l[action])
        odds*=np.where(active,lr[:,1]/lr[:,0],1)
        eq(d['beliefs'][:,t+1],odds/(1+odds))
    p=odds/(1+odds)
    patch=np.where(abs(p-.5)<=1e-12,s['ties'][:,5],p>.5)
    acquired=rewards[idx,patch]
    eq(d['patch'],patch)
    eq(d['acquired'],acquired)
    visits=d['sides']>=0
    count=visits.sum(axis=1)
    if np.all(l==.55):
        eq(p,.5)
        eq(count,k if policy=='entropy' else 0)
        eq(patch,s['ties'][:,5])
    pos=np.zeros((n,3*k+10,2))
    for t in range(k):
        pos[:,3*t+1:3*t+3,0]=np.where(visits[:,t],2*d['sides'][:,t]-1,0)[:,None]
    pos[:,3*k+1:,1]=(2*patch[:,None]-1)*[1,2,3,4,4,3,2,1,0]
    eq(d['positions'],pos)
    changes=np.full((n,3*k+9),-.5)
    changes[:,:3*k]=(visits[...,None]*[-.4*fee,-.2*fee,-.4*fee]).reshape(n,3*k)
    changes[:,3*k+4]=8*acquired
    eq(d['energy'][:,0],64)
    eq(np.diff(d['energy'],axis=1),changes)
    assert (d['energy']>0).all()
    expected=-4-count*fee+8*np.where(patch==h,.85,.15)
    realised=-4-count*fee+8*acquired
    return dict(expected_net=expected,realised_net=realised,accuracy=patch==h,visits=count,
                expenditure=count*fee,entropy=-np.log2(p)*p-np.log2(1-p)*(1-p),
                brier=np.square(p-h),log_loss=-np.log(np.clip(np.where(h,p,1-p),1e-12,1-1e-12)),
                acquisition=acquired,expected_final=64+expected,realised_final=64+realised)
