"""Paired simulated trajectories under optional sampling."""
import numpy as np
from exact_analysis import COSTS, LIKELIHOODS, POLICIES

TOL=1e-12
PILOT=tuple(range(3200,3220))
SMOKE=(3190,3191)


def schedule(seed,n):
    streams=dict(zip(('hidden','observations','random','ties','rewards'),
                     map(np.random.default_rng,np.random.SeedSequence(seed).spawn(5))))
    return dict(hidden=streams['hidden'].permutation(np.repeat([0,1],n//2)),
                observations=streams['observations'].random((n,3,2)),
                random=streams['random'].integers(2,size=(n,3)),
                ties=streams['ties'].integers(2,size=(n,4)),
                rewards=streams['rewards'].random((n,2)))


def entropy(p):
    return -(p*np.log2(p)+(1-p)*np.log2(1-p))


def gross(p):
    return 8*(.15+.7*np.maximum(p,1-p))


def updates(p,l):
    p=np.asarray(p)[...,None]
    q=(1-p)*l[:,0]+p*l[:,1]
    return q,p*l[:,1]/q,p*(1-l[:,1])/(1-q)


def choose(policy,p,l,fee,t,sequence,count,random,tie):
    if policy=='no_sensing':
        return np.full(len(p),-1)
    if policy=='fixed':
        return np.full(len(p),sequence[t] if t<len(sequence) else -1)
    if policy=='random':
        return random if t<count else np.full(len(p),-1)
    q,on,off=updates(p,l)
    if policy=='entropy':
        scores=entropy(p)[:,None]-q*entropy(on)-(1-q)*entropy(off)
    else:
        scores=q*gross(on)+(1-q)*gross(off)-gross(p)[:,None]-fee
    diff=scores[:,1]-scores[:,0]
    a=np.where(abs(diff)<=TOL,tie,diff>0).astype(int)
    return np.where(scores.max(axis=1)>TOL,a,-1) if policy=='cost_sensitive' else a


def simulate(draws,regime,cost,policy,plan):
    h=draws['hidden']
    n=len(h)
    idx=np.arange(n)
    l=np.asarray(LIKELIHOODS[regime],dtype=float)
    fee=float(COSTS[cost])
    multiplier=fee/1.25
    potential=draws['observations']<l[:,h].T[:,None,:]
    reward_probability=np.where(h[:,None]==[0,1],.85,.15)
    rewards=draws['rewards']<reward_probability
    sides=np.full((n,3),-1)
    observed=np.full((n,3),-1)
    belief=np.full((n,4),.5)
    position=np.zeros((n,19,2),dtype=int)
    energy=np.full((n,19),16.)
    live=np.ones(n,dtype=bool)
    for t in range(3):
        a=choose(policy,belief[:,t],l,fee,t,plan['fixed_sequence'],plan['random_count'],
                 draws['random'][:,t],draws['ties'][:,t])
        live &= a>=0
        a=np.where(live,a,-1)
        z=potential[idx,t,np.maximum(a,0)]
        sides[:,t]=a
        observed[:,t]=np.where(live,z,-1)
        prior=belief[:,t]
        l0,l1=np.where(z[:,None],l[a],1-l[a]).T
        belief[:,t+1]=np.where(live&(l0!=l1),prior*l1/((1-prior)*l0+prior*l1),prior)
        k=3*t
        position[:,k+1:k+3,0]=np.where(live,2*a-1,0)[:,None]
        energy[:,k+1]=energy[:,k]-.5*multiplier*live
        energy[:,k+2]=energy[:,k+1]-.25*multiplier*live
        energy[:,k+3]=energy[:,k+2]-.5*multiplier*live
    p=belief[:,-1]
    patch=np.where(abs(p-.5)<=TOL,draws['ties'][:,3],p>.5).astype(int)
    got=rewards[idx,patch]
    for k,y in enumerate((1,2,3,4,4,3,2,1,0),10):
        position[:,k,1]=y*(2*patch-1)
        energy[:,k]=energy[:,k-1]+(8*got if k==14 else -.5)
    return dict(sides=sides,observed=observed,belief=belief,position=position,energy=energy,patch=patch,
                acquired=got,potential_observations=potential,potential_rewards=rewards)
