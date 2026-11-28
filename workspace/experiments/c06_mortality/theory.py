"""Exact lexicographic policies and trajectory decision tables."""
from fractions import Fraction as Q
from functools import cache
from itertools import product
from math import log2

ENERGIES=(4,8,16,32,64,128)
COSTS=(0,.25,.5,1,2,4)
RELIABILITIES=(0,.5,1)
OBJECTIVES=('task_first','survival_first')
POLICIES=('no_sensing','fixed','random','entropy','myopic','adaptive')
EXACT=tuple(product(ENERGIES,COSTS,RELIABILITIES,OBJECTIVES))
SIM=tuple(product(ENERGIES,(0,.25,1,4),(0,1),OBJECTIVES))
METRICS=('completion','survival','final_energy','acquisition','visits','attempt','abstention','return_death')
ABSTAIN,R0,R1,RESOURCE_TIE,A,B,SITE_TIE=range(7)


def likelihoods(reliability):
    base=Q(11,20)
    return tuple(tuple(base+Q(reliability)*(p-base) for p in row)
                 for row in ((Q(9,10),Q(1,5)),(Q(1,5),Q(9,10))))


def reward_probability(p,patch):
    return Q(3,20)+Q(7,10)*(p if patch else 1-p)


def transition(p,l,z):
    h0,h1=l if z else (1-l[0],1-l[1])
    w=(1-p)*h0+p*h1
    return w,p*h1/w


def entropy(p):
    return -sum(float(x)*log2(float(x)) for x in (p,1-p) if x)


def weighted(branches):
    return tuple(sum(w*v[i] for w,v in branches) for i in range(len(METRICS)))


def utility(v,objective):
    trip,survival,e=v[:3]
    return (trip,survival,e) if objective=='task_first' else (survival,trip,e)


def terminal(p,e,objective):
    abstain=(Q(0),Q(1),Q(e,16),Q(0),Q(0),Q(0),Q(1),Q(0))
    if e<=32:
        return ABSTAIN,abstain
    options=[abstain]
    for patch in range(2):
        reward=reward_probability(p,patch)
        survivor=Q(1) if e>64 else reward
        ending=(1-reward)*Q(max(0,e-64),16)+reward*Q(e+64,16)
        options.append((survivor,survivor,ending,reward,Q(0),Q(1),Q(0),1-survivor))
    keys=[utility(v,objective) for v in options]
    selected=keys.index(max(keys))
    if selected and keys[1]==keys[2]:
        selected=RESOURCE_TIE
        return selected,weighted([(Q(1,2),options[1]),(Q(1,2),options[2])])
    return selected,options[selected]


def solve(initial,cost,reliability,objective):
    likelihood=likelihoods(reliability)
    step_ticks=int(8*cost)
    sense_ticks=int(4*cost)
    fee=2*step_ticks+sense_ticks
    initial_ticks=initial*16
    prior=Q(1,2)

    @cache
    def branches(p,a):
        return tuple(transition(p,likelihood[a],z) for z in range(2))

    @cache
    def stop(p,e):
        return terminal(p,e,objective)

    def view(p,e,a,next_value):
        v=weighted([(w,next_value(q,e-fee)) for w,q in branches(p,a)])
        return (*v[:4],v[4]+1,*v[5:])

    def order(v):
        return utility(v,objective)

    @cache
    def fixed(p,e,seq):
        if not seq or e<=fee:
            return stop(p,e)[1]
        return view(p,e,seq[0],lambda q,d:fixed(q,d,seq[1:]))

    @cache
    def random(p,e,k):
        if not k or e<=fee:
            return stop(p,e)[1]
        return weighted([(Q(1,2),view(p,e,a,lambda q,d:random(q,d,k-1))) for a in range(2)])

    enumeration=[s for k in range(4) for s in product(range(2),repeat=k)]
    sequence=max(enumeration,key=lambda s:order(fixed(prior,initial_ticks,s)))
    count=max(range(4),key=lambda k:order(random(prior,initial_ticks,k)))

    @cache
    def optimal(p,e,k):
        act,v=stop(p,e)
        if not k or e<=fee:
            return act,v
        values=[view(p,e,a,lambda q,d:optimal(q,d,k-1)[1]) for a in range(2)]
        a=max(range(2),key=lambda a:order(values[a]))
        return (A+a,values[a]) if order(values[a])>order(v) else (act,v)

    def action(p,e,t,policy):
        act,v=stop(p,e)
        if t==3 or e<=fee or policy=='no_sensing':
            return act
        if policy=='adaptive':
            return optimal(p,e,3-t)[0]
        if policy=='fixed':
            return A+sequence[t] if t<len(sequence) else act
        if policy=='random':
            return SITE_TIE if t<count else act
        if policy=='entropy':
            gains=[-sum(float(w)*entropy(q) for w,q in branches(p,a)) for a in range(2)]
            return SITE_TIE if abs(gains[0]-gains[1])<=1e-12 else A+(gains[1]>gains[0])
        values=[order(view(p,e,a,lambda q,d:stop(q,d)[1])) for a in range(2)]
        if max(values)<=order(v):
            return act
        return SITE_TIE if values[0]==values[1] else A+(values[1]>values[0])

    @cache
    def evaluate(p,e,t,policy):
        a=action(p,e,t,policy)
        if a<A:
            return stop(p,e)[1]
        sites=(0,1) if a==SITE_TIE else (a-A,)
        return weighted([(Q(1,len(sites)),view(p,e,i,lambda q,d:evaluate(q,d,t+1,policy))) for i in sites])

    values={p:evaluate(prior,initial_ticks,0,p) for p in POLICIES}
    best=optimal(prior,initial_ticks,3)[1]
    assert all(order(v)<=order(best) for v in values.values())
    assert values['adaptive']==best
    table={}
    belief={}
    def compile_tree(node,p,t):
        e=initial_ticks-t*fee
        belief[node]=float(p)
        table[node]=[action(p,e,t,policy) for policy in POLICIES]
        if t<3 and e>fee:
            for a in range(2):
                for z,(_,q) in enumerate(branches(p,a)):
                    compile_tree(4*node+1+2*a+z,q,t+1)
    compile_tree(0,prior,0)
    return dict(likelihood=likelihood,step=step_ticks,sensing=sense_ticks,fee=fee,sequence=sequence,count=count,
                values=values,table=table,belief=belief)
