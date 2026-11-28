"""Simulate shared potential outcomes with configurable observation budgets."""
import numpy as np

SEEDS=tuple(range(3300,3350))
SMOKE=(3290,3291)


def schedule(seed,n):
    h,o,l,t,r=map(np.random.default_rng,np.random.SeedSequence(seed).spawn(5))
    return dict(hidden=h.permutation(np.repeat([0,1],n//2)),observations=o.random((n,5,2)),
                random=l.integers(2,size=(n,5)),ties=t.integers(2,size=(n,6)),rewards=r.random((n,2)))


def entropy(p):
    return -p*np.log2(p)-(1-p)*np.log2(1-p)


def gross(p):
    return 8*(.15+.7*np.maximum(p,1-p))


def decision(policy,p,l,fee,t,sequence,count,random,tie):
    if policy=='no_sensing':
        return np.full(len(p),-1)
    if policy=='fixed':
        return np.full(len(p),sequence[t] if t<len(sequence) else -1)
    if policy=='random':
        return random if t<count else np.full(len(p),-1)
    p=p[:,None]
    q=(1-p)*l[:,0]+p*l[:,1]
    yes=p*l[:,1]/q
    no=p*(1-l[:,1])/(1-q)
    if policy=='entropy':
        scores=-q*entropy(yes)-(1-q)*entropy(no)
    else:
        scores=q*gross(yes)+(1-q)*gross(no)-gross(p)-fee
    diff=scores[:,1]-scores[:,0]
    side=np.where(abs(diff)<=1e-12,tie,diff>0).astype(int)
    return np.where(scores.max(axis=1)>1e-12,side,-1) if policy=='cost_sensitive' else side


def simulate(s,k,policy,plan):
    l,fee,sequence,count,_=plan
    l=np.asarray(l)
    h=s['hidden']
    idx=np.arange(len(h))
    potential=s['observations'][:,:k]<l[:,h].T[:,None,:]
    rp=np.where(h[:,None]==[0,1],.85,.15)
    rewards=s['rewards']<rp
    beliefs=np.full((len(h),k+1),.5)
    sides=np.full((len(h),k),-1,dtype=np.int8)
    observed=sides.copy()
    positions=np.zeros((len(h),3*k+10,2),dtype=np.int8)
    energy=np.full(positions.shape[:2],64.)
    sampling=np.ones(len(h),dtype=bool)
    for t in range(k):
        p=beliefs[:,t]
        a=decision(policy,p,l,fee,t,sequence,count,s['random'][:,t],s['ties'][:,t])
        sampling &= a>=0
        a=np.where(sampling,a,-1)
        sides[:,t]=a
        z=potential[idx,t,a]
        observed[:,t]=np.where(sampling,z,-1)
        l0,l1=np.where(z[:,None],l[a],1-l[a]).T
        beliefs[:,t+1]=np.where(sampling&(l0!=l1),p*l1/((1-p)*l0+p*l1),p)
        j=3*t
        positions[:,j+1:j+3,0]=np.where(sampling,2*a-1,0)[:,None]
        for step,fraction in enumerate((.4,.2,.4),1):
            energy[:,j+step]=energy[:,j+step-1]-fee*fraction*sampling
    p=beliefs[:,-1]
    patch=np.where(abs(p-.5)<=1e-12,s['ties'][:,5],p>.5).astype(np.int8)
    acquired=rewards[idx,patch]
    for t,distance in enumerate((1,2,3,4,4,3,2,1,0),1):
        j=3*k+t
        positions[:,j,1]=(2*patch-1)*distance
        energy[:,j]=energy[:,j-1]+(8*acquired if t==5 else -.5)
    return dict(sides=sides,observed=observed,beliefs=beliefs,positions=positions,energy=energy,
                patch=patch,acquired=acquired,potential=potential,potential_rewards=rewards)


def metrics(s,d,fee):
    h=s['hidden']
    correct=d['patch']==h
    visits=(d['sides']>=0).sum(axis=1)
    p=d['beliefs'][:,-1]
    expected=-4-visits*fee+8*np.where(correct,.85,.15)
    final=d['energy'][:,-1]
    return dict(expected_net=expected,realised_net=final-64,accuracy=correct,visits=visits,
                expenditure=visits*fee,entropy=entropy(p),brier=(p-h)**2,
                log_loss=-np.log(np.clip(np.where(h,p,1-p),1e-12,1-1e-12)),
                acquisition=d['acquired'],expected_final=64+expected,realised_final=final)
