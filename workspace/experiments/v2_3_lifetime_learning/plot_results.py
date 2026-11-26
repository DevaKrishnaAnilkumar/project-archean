"""Generate descriptive figures from saved aggregate CSV (no simulations)."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(source, output):
    with source.open() as f:
        rows=list(csv.DictReader(f))
    output.mkdir(parents=True,exist_ok=False)
    for budget,key,ylabel,name in [(160,'correct_all','Correct choices / scheduled encounters (%)','learning_curves'),(24,'alive_after','Survival after encounter (%)','survival_curves')]:
        fig,axs=plt.subplots(1,2,figsize=(10,4),sharey=True,layout='constrained')
        for ax,w in zip(axs,['stable','reversed']):
            for a,l,c in [('adaptive','Adaptive','#007A70'),('frozen','Frozen','#536981'),('cue_blind','Cue-blind','#B76521')]:
                r=sorted([r for r in rows if int(r['budget'])==budget and r['world']==w and r['arm']==a],key=lambda r:int(r['encounter']))
                assert [int(x['encounter']) for x in r]==list(range(1,33))
                y=[100*float(x[key])/(int(x['scheduled']) if key=='alive_after' else 1) for x in r]
                ax.plot(range(1,33),y,label=l,color=c,linewidth=1.7)
            if w=='reversed':
                ax.axvline(16.5,color='0.4',ls='--',lw=1)
                ax.text(17,5,'Reversal',fontsize=8,color='0.35')
            ax.set(title=w.capitalize(),xlabel='Encounter',ylim=(0,102),xlim=(1,32));ax.grid(alpha=.2);ax.spines[['top','right']].set_visible(False)
        axs[0].set_ylabel(ylabel);axs[0].legend(loc='best',frameon=False,fontsize=9)
        fig.suptitle(f'v2.3.1 | {budget}-unit initial energy • 40 seeds, 64 organisms per seed',fontsize=12)
        fig.savefig(output/f'{name}.png',dpi=180);plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args();main(a.source,a.output)
