"""Create C06 figures from exact expectations and audited seed aggregates."""
import csv
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from theory import ENERGIES,COSTS,RELIABILITIES,OBJECTIVES,POLICIES


def read(p):
    with p.open() as f:
        return {(int(r['initial_energy']),float(r['cost_multiplier']),float(r['reliability']),r['objective'],r['policy']):r
                for r in csv.DictReader(f)}


def plots(exact,pilot,out):
    out.mkdir(exist_ok=False)
    for metric,title in [('survival','Survival'),('completion','Completed round trip alive'),
                         ('acquisition','Resource reward received'),('abstention','Abstention')]:
        fig,axs=plt.subplots(1,2,figsize=(10.5,4),layout='constrained',sharey=True)
        for ax,o in zip(axs,OBJECTIVES):
            for p in POLICIES:
                k=[(e,1.,1.,o,p) for e in ENERGIES]
                line,=ax.plot(ENERGIES,[float(exact[i][metric]) for i in k],label=p.replace('_',' '))
                ax.scatter(ENERGIES,[float(pilot[i][metric]) for i in k],s=13,color=line.get_color())
            ax.set(xscale='log',xticks=ENERGIES,xticklabels=ENERGIES,ylim=(-.04,1.04),
                   title=o.replace('_',' ').capitalize(),xlabel='Initial energy')
        axs[0].set_ylabel(title+' probability')
        axs[1].legend(fontsize=8)
        fig.suptitle('Cost multiplier 1, full reliability · exact lines and simulation points')
        fig.savefig(out/f'{metric}_by_initial_energy.png',dpi=150)
        plt.close(fig)

    def get(e,c,r,o,p,m):
        return float(exact[e,c,r,o,p][m])

    specs=[
        ('myopic_vs_planning.png','Adaptive minus myopic completion',
          lambda e,c,r:get(e,c,r,'task_first','adaptive','completion')-get(e,c,r,'task_first','myopic','completion')),
        ('energy_cost_reliability.png','Compulsory entropy survival probability',
          lambda e,c,r:get(e,c,r,'task_first','entropy','survival')),
        ('objectives_comparison.png','Task-first minus survival-first completion',
          lambda e,c,r:get(e,c,r,'task_first','adaptive','completion')-get(e,c,r,'survival_first','adaptive','completion')),
        ('optimality_gaps.png','Adaptive minus myopic final energy',
          lambda e,c,r:get(e,c,r,'task_first','adaptive','final_energy')-get(e,c,r,'task_first','myopic','final_energy'))]
    for fn,title,val in specs:
        fig,axs=plt.subplots(1,3,figsize=(12,4.2),layout='constrained')
        grids=[np.array([[val(e,c,r) for c in COSTS] for e in ENERGIES]) for r in RELIABILITIES]
        vmax=max(abs(d).max() for d in grids) or 1
        signed=any(np.min(d)<-1e-12 for d in grids)
        for r,d,ax in zip(RELIABILITIES,grids,axs):
            im=ax.imshow(d,origin='lower',vmin=-vmax if signed else 0,vmax=vmax,cmap='RdBu' if signed else 'viridis')
            ax.set(title=f'Reliability {r}',xticks=range(6),xticklabels=COSTS,yticks=range(6),
                   yticklabels=ENERGIES,xlabel='Cost multiplier')
        axs[0].set_ylabel('Initial energy')
        fig.colorbar(im,ax=axs,label=title)
        fig.savefig(out/fn,dpi=150)
        plt.close(fig)


if __name__=='__main__':
    plots(read(Path(sys.argv[1])),read(Path(sys.argv[2])),Path(sys.argv[3]))
