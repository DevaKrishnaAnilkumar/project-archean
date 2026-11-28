"""Sum every possible observation, sampling action, stopping and tie branch."""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
from math import log2

LIKELIHOODS = {'informative': ((Q(9,10),Q(1,5)),(Q(1,5),Q(9,10))),
               'uninformative': ((Q(11,20),Q(11,20)),)*2}
COSTS = {'low':Q(5,16),'original':Q(5,4),'high':Q(5,2)}
POLICIES = ('no_sensing','fixed','random','entropy','cost_sensitive')


def entropy(p):
    return -sum(float(x)*log2(float(x)) for x in (p,1-p) if x)


def gross(p):
    return Q(6,5)+Q(28,5)*max(p,1-p)


def outcomes(p, likelihood):
    for a,b in (likelihood,tuple(1-x for x in likelihood)):
        w=(1-p)*a+p*b
        yield w,p*b/w


def solve(regime,cost_name):
    likelihood,fee=LIKELIHOODS[regime],COSTS[cost_name]

    @lru_cache(None)
    def fixed_value(p,seq):
        if not seq:
            return gross(p)
        return sum(w*fixed_value(q,seq[1:]) for w,q in outcomes(p,likelihood[seq[0]]))-fee

    @lru_cache(None)
    def optimal(p,k):
        if not k:
            return gross(p)
        return max(gross(p),*(sum(w*optimal(q,k-1) for w,q in outcomes(p,l))-fee for l in likelihood))

    seqs=[s for k in range(4) for s in product(range(2),repeat=k)]
    prior=Q(1,2)
    fixed=max(seqs,key=lambda s:fixed_value(prior,s))
    count=max(range(4),key=lambda k:sum(fixed_value(prior,s) for s in seqs if len(s)==k)/2**k)

    def actions(p,visit,policy):
        if visit==3 or policy=='no_sensing':
            return []
        if policy=='fixed':
            return [fixed[visit]] if visit<len(fixed) else []
        if policy=='random':
            return [0,1] if visit<count else []
        if policy=='entropy':
            scores=[-sum(float(w)*entropy(q) for w,q in outcomes(p,l)) for l in likelihood]
        else:
            scores=[sum(w*gross(q) for w,q in outcomes(p,l))-gross(p)-fee for l in likelihood]
            if max(scores)<=1e-12:
                return []
        return [i for i,v in enumerate(scores) if max(scores)-v<=1e-12]

    @lru_cache(None)
    def expectation(p,visit,policy):
        sites=actions(p,visit,policy)
        if not sites:
            return gross(p)-fee*visit,max(p,1-p),visit
        branches=[(w/len(sites),expectation(q,visit+1,policy))
                  for a in sites for w,q in outcomes(p,likelihood[a])]
        return tuple(sum(w*v[j] for w,v in branches) for j in range(3))

    values={}
    optimum=12+optimal(prior,3)
    for p in POLICIES:
        energy,accuracy,visits=expectation(prior,0,p)
        assert 12+energy<=optimum
        values[p] = dict(energy=float(12+energy), accuracy=float(accuracy), visits=float(visits),
                         optimality_gap=float(optimum-(12+energy)))
    return dict(fixed_sequence=fixed, random_count=count, optimal_energy=float(optimum),policies=values)


def theory():
    return {r:{c:solve(r,c) for c in COSTS} for r in LIKELIHOODS}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    out=parser.parse_args().output
    out.mkdir(parents=True,exist_ok=False)
    (out/'expectations.json').write_text(json.dumps(theory(),indent=2)+'\n')
