"""Plot the lifetime curves and prespecified environmental controls."""
from pathlib import Path
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from model import SETTINGS,POLICIES
from analysis import CURVES

NAMES=('No sensing','Fixed, frozen','Adaptive, frozen','Fixed, learning','Adaptive, learning','Oracle')


def plot(pilot,out):
    out.mkdir(exist_ok=False)
    with np.load(pilot/'seed_curves.npz',allow_pickle=False) as f:
        v=f['values']
    period=np.arange(1,49)
    for metric,labels,indices,fn in [
        ('survival',['Stable · 8 energy','Stable · 24 energy','Reversal · 24 energy'],[0,1,4],'survival_curves.png'),
        ('scheduled_accuracy',['Stable','Reversal','Unpredictable'],[2,5,8],'learning_accuracy.png'),
        ('mapping_mass',['Stable','Reversal','Unpredictable'],[2,5,8],'mapping_learning.png'),
        ('reliable_share',['Stable','Reversal','Unpredictable'],[2,5,8],'reliable_sensor_selection.png')]:
        fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True,layout='constrained')
        for ax,title,i in zip(axes,labels,indices):
            for j,name in enumerate(NAMES):
                y=v[:,:,i,j,CURVES.index(metric)]
                if np.isnan(y).all():
                    continue
                avg=np.nanmean(y,axis=0); se=np.nanstd(y,axis=0,ddof=1)/np.sqrt(np.isfinite(y).sum(axis=0))
                line,=ax.plot(period,avg,label=name)
                ax.fill_between(period,avg-2.00957523449*se,avg+2.00957523449*se,color=line.get_color(),alpha=.12)
            if SETTINGS[i][0]=='reversal':
                ax.axvline(24.5,color='gray',linestyle=':')
            ax.set(title=title,xlabel='Period',ylim=(0,1.04))
        axes[0].set_ylabel(metric.replace('_',' ').capitalize())
        axes[-1].legend(fontsize=7)
        fig.savefig(out/fn,dpi=150)
        plt.close(fig)
    with (pilot/'condition_means.csv').open() as f:
        rows=list(csv.DictReader(f))
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for j,p in enumerate(POLICIES):
        selected=[r for r in rows if r['regime']=='stable' and r['initial_energy']=='8' and r['policy']==p]
        for ax,k in zip(axes,('sensing','final_energy')):
            ax.plot([float(r['sensing_ticks'])/16 for r in selected],[float(r[k]) for r in selected],'o-',label=NAMES[j])
    for ax,y in zip(axes,('Cumulative sensing expenditure','Mean final energy')):
        ax.set(xlabel='Cost per sensing trip',ylabel=y)
    axes[-1].legend(fontsize=7)
    fig.savefig(out/'energy_and_sensing_cost.png',dpi=150)
    plt.close(fig)


if __name__=='__main__':
    plot(Path(sys.argv[1]),Path(sys.argv[2]))
