"""Plot the exact full grid and prespecified simulated sweeps."""
import csv
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
from theory import BUDGET, COST, POLICIES, RELIABILITY


def read(p):
    with p.open() as f:
        return [{k:v if k=='policy' else float(v) for k,v in r.items() if k!='fixed_sequence'} for r in csv.DictReader(f)]


def plot(exact,simulation,out):
    out.mkdir(exist_ok=False)
    indexed={(r['cost'],r['budget'],r['reliability'],r['policy']):r for r in exact}
    delta=lambda c,k,r:indexed[c,k,r,'cost_sensitive']['expected_net']-indexed[c,k,r,'fixed']['expected_net']
    gap=lambda c,k,r:indexed[c,k,r,'cost_sensitive']['gap']
    for fn,label,value,cm in [('policy_advantage.png','Cost-sensitive minus best fixed (energy)',delta,'RdBu'),
                              ('optimality_gap.png','Exact optimal minus cost-sensitive (energy)',gap,'magma')]:
        data=[np.array([[value(c,k,r) for c in COST] for r in RELIABILITY]) for k in BUDGET]
        vmax=max(abs(d).max() for d in data)
        fig,axs=plt.subplots(2,2,figsize=(10,7),layout='constrained')
        for ax,k,d in zip(axs.flat,BUDGET,data):
            im=ax.imshow(d,origin='lower',vmin=-vmax if value==delta else 0,vmax=vmax,cmap=cm)
            ax.set(title=f'{k} visits allowed',xticks=range(len(COST)),xticklabels=COST,
                   yticks=range(len(RELIABILITY)),yticklabels=RELIABILITY,
                   xlabel='Cost multiplier',ylabel='Reliability multiplier')
        fig.colorbar(im,ax=axs,label=label)
        fig.savefig(out/fn,dpi=155)
        plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
    for ax,x,fixed in zip(axs,('cost','reliability','budget'),({'budget':3,'reliability':1},{'budget':3,'cost':1},{'cost':1,'reliability':1})):
        for policy in POLICIES:
            vals=[r for r in simulation if r['policy']==policy and all(r[k]==v for k,v in fixed.items())]
            vals.sort(key=lambda r:r[x])
            ax.plot([r[x] for r in vals],[r['expected_net'] for r in vals],'o-',label=policy.replace('_',' '))
        ax.set(xlabel=x.capitalize(),ylabel='Mean expected net energy')
        ax.axhline(0,color='silver',lw=1)
    axs[-1].legend(fontsize=8)
    fig.savefig(out/'simulation_sweeps.png',dpi=155)
    plt.close(fig)


if __name__=='__main__':
    plot(read(Path(sys.argv[1])),read(Path(sys.argv[2])),Path(sys.argv[3]))
