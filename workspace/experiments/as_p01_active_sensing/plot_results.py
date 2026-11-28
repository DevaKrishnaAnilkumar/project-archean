import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from audit_results import read
from model import POLICIES, REGIMES


def plot(root,out):
    out.mkdir(parents=True,exist_ok=False)
    rows=read(root/'per_seed.csv')
    contrasts=read(root/'paired_contrasts.csv')
    groups={(r,p):[v for v in rows if v['regime']==r and v['policy']==p] for r in REGIMES for p in POLICIES}
    colors=['#50658a','#a45830','#167a72']
    for title,filename,keys in [
        ('Posterior entropy (bits)','entropy_by_observation.png',[f'entropy_{i}' for i in range(1,4)]),
        ('Correct resource choice','resource_choice_accuracy.png',['accuracy']),
        ('Visits to location B','sampling_policy_behaviour.png',[f'side_b_{i}' for i in range(1,4)])]:
        fig,axs=plt.subplots(1,2,figsize=(10,4.5),layout='constrained',sharey=True)
        for ax,r in zip(axs,REGIMES):
            for j,(p,color) in enumerate(zip(POLICIES,colors)):
                y=np.array([[float(v[k]) for k in keys] for v in groups[r,p]])
                x=np.arange(len(keys))+1+(j-1)*.15
                ax.scatter(np.broadcast_to(x,y.shape),y,s=10,alpha=.24,color=color)
                ax.errorbar(x,y.mean(axis=0),yerr=2.093024054*y.std(axis=0,ddof=1)/np.sqrt(len(y)),
                            fmt='o-',color=color,label=p,capsize=3)
            ax.set(title=r.capitalize(),xticks=np.arange(len(keys))+1,xticklabels=['Choice'] if len(keys)==1 else ['Visit 1','Visit 2','Visit 3'])
        axs[0].legend()
        fig.suptitle(title+' · seed points and exploratory 95% intervals')
        fig.savefig(out/filename,dpi=150)
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
    for i,row in enumerate(contrasts[:2]):
        comp=row['comparator']
        diff=[float(a['gain'])-float(b['gain']) for a,b in zip(groups['informative','information'],groups['informative',comp])]
        ax.scatter(diff,np.linspace(i-.14,i+.14,len(diff)),color=colors[i],alpha=.65)
        mean,low,high=(float(row[k]) for k in ('mean','low','high'))
        ax.errorbar(mean,i,xerr=[[mean-low],[high-mean]],fmt='ko',capsize=5)
    ax.axvline(0,color='gray')
    ax.set(yticks=[0,1],yticklabels=['Information − fixed','Information − random'],
           xlabel='Paired entropy reduction (bits)',title='Informative regime · 20 seed contrasts')
    fig.savefig(out/'paired_information_gain.png',dpi=150)
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('results',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    plot(args.results,args.output)
