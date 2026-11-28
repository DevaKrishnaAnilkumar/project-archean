"""Enumerate the sensitivity grid with rational transition probabilities."""
from fractions import Fraction as Q
from functools import cache
from itertools import product
from math import log, log2

COST=(0,.25,.5,1,2,4)
BUDGET=(1,2,3,5)
RELIABILITY=(0,.25,.5,.75,1)
POLICIES=('no_sensing','fixed','random','entropy','cost_sensitive')
GRID=tuple(product(COST,BUDGET,RELIABILITY))
SIM=tuple(sorted(set([(c,3,1) for c in COST]+[(1,3,r) for r in RELIABILITY]
                     +[(1,k,1) for k in BUDGET]+list(product((.25,1,4),(1,5),(0,.5,1))))))
METRICS=('expected_net','realised_net','accuracy','visits','expenditure','entropy','brier','log_loss','acquisition')


def entropy(p):
    return -sum(float(x)*log2(float(x)) for x in (p,1-p) if x)


def solve(cost,budget,reliability):
    fee=Q(5,4)*Q(cost)
    base=Q(11,20)
    likelihood=tuple(tuple(base+Q(reliability)*(x-base) for x in l)
                     for l in ((Q(9,10),Q(1,5)),(Q(1,5),Q(9,10))))

    def gross(p):
        return Q(6,5)+Q(28,5)*max(p,1-p)

    @cache
    def outcomes(p,a):
        l0,l1=likelihood[a]
        result=[]
        for u,v in ((l0,l1),(1-l0,1-l1)):
            w=(1-p)*u+p*v
            result.append((w,p*v/w))
        return tuple(result)

    @cache
    def fixed(p,seq):
        if not seq:
            return gross(p)
        return sum(w*fixed(q,seq[1:]) for w,q in outcomes(p,seq[0]))-fee

    @cache
    def optimal(p,k):
        if not k:
            return gross(p)
        return max(gross(p),*(sum(w*optimal(q,k-1) for w,q in outcomes(p,a))-fee for a in (0,1)))

    prior=Q(1,2)
    seqs=[s for k in range(budget+1) for s in product((0,1),repeat=k)]
    sequence=max(seqs,key=lambda s:fixed(prior,s))
    count=max(range(budget+1),key=lambda k:sum(fixed(prior,s) for s in seqs if len(s)==k)/2**k)

    @cache
    def expectation(p,t,policy):
        sites=[]
        if t<budget:
            if policy=='fixed' and t<len(sequence):
                sites=[sequence[t]]
            elif policy=='random' and t<count:
                sites=[0,1]
            elif policy in ('entropy','cost_sensitive'):
                if policy=='entropy':
                    scores=[-sum(float(w)*entropy(q) for w,q in outcomes(p,a)) for a in (0,1)]
                else:
                    scores=[sum(w*gross(q) for w,q in outcomes(p,a))-fee-gross(p) for a in (0,1)]
                if policy=='entropy' or max(scores)>1e-12:
                    sites=[a for a in (0,1) if max(scores)-scores[a]<=1e-12]
        if not sites:
            net=gross(p)-4-fee*t
            return (net,net,max(p,1-p),t,fee*t,entropy(p),p*(1-p),entropy(p)*log(2),gross(p)/8)
        children=[(w/len(sites),expectation(q,t+1,policy)) for a in sites for w,q in outcomes(p,a)]
        return tuple(sum(w*v[i] for w,v in children) for i in range(len(METRICS)))

    optimum=optimal(prior,budget)-4
    rows={}
    for policy in POLICIES:
        values=expectation(prior,0,policy)
        assert values[0]<=optimum
        rows[policy]=dict(zip(METRICS,map(float,values)))
        rows[policy].update(optimal_net=float(optimum),gap=float(optimum-values[0]),
                            expected_final=64+float(values[0]),realised_final=64+float(values[1]))
    return tuple(tuple(map(float,l)) for l in likelihood),float(fee),sequence,count,rows
