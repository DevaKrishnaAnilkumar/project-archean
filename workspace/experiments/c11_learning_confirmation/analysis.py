"""Prospectively specified world-seed paired analysis; no model imports."""
import argparse,csv,json,math
from pathlib import Path
import numpy as np
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def write_table(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def interval(x,alpha=.05):
    x=np.array(x,dtype=float); n=len(x);assert n==64 and np.all(np.isfinite(x));mean=float(x.mean());sd=float(x.std(ddof=1));h=float(t.ppf(1-alpha/2,n-1)*sd/math.sqrt(n));return mean,sd,mean-h,mean+h
def decision(lo,hi):
    if lo>.05:return 'positive_practically_meaningful'
    if hi<-.05:return 'negative_practically_meaningful'
    if lo>0:return 'positive_direction'
    if hi<0:return 'negative_direction'
    if lo>=-.05 and hi<=.05:return 'bounded_small'
    return 'inconclusive'
def main():
    p=argparse.ArgumentParser();p.add_argument('audit',type=Path);p.add_argument('out',type=Path);p.add_argument('study',choices=['A','B']);args=p.parse_args();args.out.mkdir(); rows=list(csv.DictReader((args.audit/'worlds.csv').open()));assert all(r['study']==args.study and r['phase']=='evaluation' for r in rows)
    seeds=range(3900,3964) if args.study=='A' else range(4000,4064);conditions=['A1','A2','A3'] if args.study=='A' else [f'B{i}-{cue}' for cue in ('informative','null') for i in range(1,5)]
    ix={(r['condition'],int(r['seed'])):r for r in rows};assert len(ix)==len(rows)==64*len(conditions) and set(ix)=={(c,s) for c in conditions for s in seeds}
    def v(c,k):return np.array([float(ix[c,s][k]) for s in seeds])
    if args.study=='A': contrasts={'A-P1':v('A1','delta'),'A-P2':v('A1','delta')-v('A2','delta'),'A-P3':v('A1','delta')-v('A3','delta')}
    else:contrasts={'B-P1':v('B2-informative','U')-v('B1-informative','U'),'B-P2':v('B3-informative','G')-v('B3-null','G')}
    primary=[];n=len(contrasts)
    for key,x in contrasts.items():
        mean,sd,lo,hi=interval(x);_,_,alo,ahi=interval(x,.05/n)
        primary.append(dict(contrast=key,n=len(x),mean=mean,sd=sd,lo95=lo,hi95=hi,adjusted_confidence=1-.05/n,adjusted_lo=alo,adjusted_hi=ahi,positive_seeds=int((x>0).sum()),negative_seeds=int((x<0).sum()),zero_seeds=int((x==0).sum()),decision=decision(alo,ahi),within_margin=bool(alo>=-.05 and ahi<=.05)))
    write_table(args.out/'primary.csv',primary);write_table(args.out/'primary_seed_contrasts.csv',[dict(seed=s,**{k:x[i] for k,x in contrasts.items()}) for i,s in enumerate(seeds)])
    secondary=[]
    for c in conditions:
        for k in ('U','F','active','delta','G','births','deaths','eligible','blocked_births','final_population','final_lineages','lineage_periods','mean_population','mut_l','mut_s'):
            x=v(c,k)
            if not np.all(np.isfinite(x)):
                assert np.all(np.isnan(x));continue
            mean,sd,lo,hi=interval(x);secondary.append(dict(condition=c,metric=k,n=len(x),mean=mean,sd=sd,lo95=lo,hi95=hi))
        x=(v(c,'extinction')<240).astype(float);mean,sd,lo,hi=interval(x);secondary.append(dict(condition=c,metric='extinct_fraction',n=len(x),mean=mean,sd=sd,lo95=lo,hi95=hi))
    write_table(args.out/'condition_means.csv',secondary)
    if args.study=='B':
        checks={'B3_informative_G':v('B3-informative','G'),'B3_null_G':v('B3-null','G'),'B4_minus_B3_informative_G':v('B4-informative','G')-v('B3-informative','G'),'B4_minus_B3_null_G':v('B4-null','G')-v('B3-null','G'),'B2_minus_B1_null_U':v('B2-null','U')-v('B1-null','U'),'B2_minus_B1_informative_extinction_risk':(v('B2-informative','extinction')<240).astype(float)-(v('B1-informative','extinction')<240).astype(float)}
        secondary_contrasts=[]
        for key,x in checks.items():
            m,s,l,h=interval(x);secondary_contrasts.append(dict(contrast=key,n=len(x),mean=m,sd=s,lo95=l,hi95=h))
        write_table(args.out/'secondary_contrasts.csv',secondary_contrasts)
    # Exposure-weighted descriptions; retain numerator and denominator for every ratio.
    genotype=[]
    for c in conditions:
        for g in range(6):
            total=lambda k:float(v(c,f'{k}_g{g}').sum())
            r=dict(condition=c,genotype=g)
            for k in ('periods','exposure','individuals','births_parent','offspring','censored','attempts','samples','correct','rewards','net_action_ticks','overhead_ticks','sensing_ticks','mapping_brier_sum','eligible','blocked'):r[k]=total(k)
            for k,a,b in [('accuracy','correct','attempts'),('sample_rate','samples','exposure'),('birth_rate','births_parent','exposure'),('eligible_birth_rate','births_parent','eligible'),('brier','mapping_brier_sum','exposure')]:r[k]=r[a]/r[b] if r[b] else float('nan')
            genotype.append(r)
    write_table(args.out/'genotype_descriptive.csv',genotype)
    tr=np.load(args.audit/'curves.npy',allow_pickle=False); assert tr.shape==(len(rows),240,13)
    fig,ax=plt.subplots(3,1,figsize=(9,10),sharex=True);tt=np.arange(240)+1;critical=t.ppf(.975,63)
    for c in conditions:
        subset=tr[[i for i,r in enumerate(rows) if r['condition']==c]];pop=subset[:,:,:6].sum(axis=2)
        for a,z in zip(ax,(pop,subset[:,:,4:6].sum(axis=2)/120,subset[:,:,6])):
            m=z.mean(axis=0);h=critical*z.std(axis=0,ddof=1)/8;a.plot(tt,m,label=c);a.fill_between(tt,m-h,m+h,alpha=.09)
    for a,title in zip(ax,('Living population','Joint-trait slot occupancy','Surviving founder lineages')):a.set_ylabel(title);a.grid(alpha=.2)
    ax[0].legend(ncol=2,fontsize=8);ax[-1].set_xlabel('Period');fig.tight_layout();fig.savefig(args.out/'population_curves.png',dpi=140);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4));
    for c in conditions:
        et=v(c,'extinction');ax.step(tt,np.array([(et>=period).mean() for period in tt]),where='post',label=c)
    ax.set(xlabel='Period',ylabel='World survival fraction',ylim=(-.02,1.02));ax.legend(fontsize=8,ncol=2);fig.tight_layout();fig.savefig(args.out/'extinction.png',dpi=140);plt.close(fig)
    (args.out/'summary.json').write_text(json.dumps({'study':args.study,'primary':primary,'conditions':conditions,'independent_seed_blocks':64},indent=2)+'\n');print(json.dumps(primary),flush=True)
if __name__=='__main__':main()
