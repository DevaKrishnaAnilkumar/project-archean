"""Plot seed results and the exact expected optimality gaps."""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from audit_results import rows
from exact_analysis import COSTS, LIKELIHOODS, POLICIES


def plot(results,out):
    out.mkdir(parents=True,exist_ok=False)
    seed=rows(results/'per_seed.csv')
    conditions=rows(results/'condition_means.csv')
    colors=plt.get_cmap('tab10')
    for metric,title,file in [
        ('energy','Expected final energy (units)','net_energy_by_cost.png'),
        ('visits','Observation visits','observations_by_cost.png'),
        ('accuracy','Correct resource choice','accuracy_by_cost.png'),
        ('exact_gap','Exact gap from adaptive optimum (units)','adaptive_policy_optimality_gap.png')]:
        fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout='constrained',sharey=True)
        for ax,regime in zip(axes,LIKELIHOODS):
            for i,policy in enumerate(POLICIES):
                values=[]
                x=np.arange(3)+(i-2)*.11
                for j,cost in enumerate(COSTS):
                    table=conditions if metric=='exact_gap' else seed
                    v=[float(r[metric]) for r in table if (r['regime'],r['cost'],r['policy'])==(regime,cost,policy)]
                    values.append(np.mean(v))
                    if len(v)>1:
                        ax.scatter(np.full(len(v),x[j]),v,s=9,alpha=.22,color=colors(i))
                ax.plot(x,values,'o-',color=colors(i),label=policy.replace('_',' '))
            ax.set(title=regime.capitalize(),xticks=np.arange(3),xticklabels=list(COSTS),xlabel='Sampling cost')
            ax.grid(axis='y',alpha=.2)
        axes[0].set_ylabel(title)
        axes[1].legend(fontsize=8)
        fig.savefig(out/file,dpi=160)
        plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(11.5,4),layout='constrained',sharex=True,sharey=True)
    for ax,cost in zip(axes,COSTS):
        for i,policy in enumerate(POLICIES):
            subset=[r for r in seed if (r['regime'],r['cost'],r['policy'])==('informative',cost,policy)]
            x=[1-float(r['entropy']) for r in subset]
            y=[float(r['energy']) for r in subset]
            ax.scatter(x,y,color=colors(i),s=16,alpha=.55,label=policy.replace('_',' '))
        ax.set(title=cost.capitalize(),xlabel='Entropy reduction (bits)')
    axes[0].set_ylabel('Expected final energy (units)')
    axes[-1].legend(fontsize=8)
    fig.savefig(out/'information_vs_energy.png',dpi=160)
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results',type=Path)
    parser.add_argument('figures',type=Path)
    args=parser.parse_args()
    plot(args.results,args.figures)
