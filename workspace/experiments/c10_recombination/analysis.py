"""C10 prespecified world-level paired contrasts and descriptive outcomes."""
import csv,math,argparse,json
from pathlib import Path
import numpy as np
from scipy.stats import t as tdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ARM=['Single blank','Single parent memory','Pair clone blank','Pair clone primary','Pair clone pooled','Pair recomb blank','Pair recomb primary','Pair recomb pooled']
SETTING=['Stable','Reversal','Unpredictable','Stable, no mutation','Reversal, no mutation','Stable, 10% mutation','Reversal, 10% mutation','Stable, low reward','Stable, expensive sensing','Small, low energy founders','Balanced founders','Uninformative']
METRICS=['occupancy','joint','joint_living','final_population','extinct','births','deaths','richness','mean_richness','eligible','unpaired','blocked','joint_births','first_joint_birth','recombined_joint','mutated_births','birth_debit_ticks','observable_births','first_attempts','first_correct','first_accuracy','first_conditional','birth_brier','disagreement','conflicts','conflict_births_observable','conflict_brier','accuracy']
def write(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def contrast(d,s,a,b,metric,label):
    v=[];seedrows=[]
    for seed in range(3800,3820):
        x=float(d[s,seed,a][metric]);y=float(d[s,seed,b][metric]);diff=x-y
        seedrows.append({'label':label,'setting':s,'arm_a':a,'arm_b':b,'metric':metric,'seed':seed,'a':x,'b':y,'difference':diff})
        if math.isfinite(diff):v.append(diff)
    n=len(v);m=np.mean(v) if n else np.nan;sd=np.std(v,ddof=1) if n>1 else np.nan;half=tdist.ppf(.975,n-1)*sd/math.sqrt(n) if n>1 else np.nan
    return {'label':label,'setting':s,'arm_a':a,'arm_b':b,'metric':metric,'n':n,'mean':m,'sd':sd,'lo95':m-half,'hi95':m+half},seedrows

def main():
    p=argparse.ArgumentParser();p.add_argument('audit',type=Path);p.add_argument('out',type=Path);args=p.parse_args();assert not args.out.exists();args.out.mkdir(parents=True)
    rows=list(csv.DictReader((args.audit/'worlds.csv').open()));d={(int(r['setting']),int(r['seed']),int(r['arm'])):r for r in rows};assert len(d)==len(rows)==1920
    prim=[];paired=[]
    for s,a,b,metric,label in [(3,5,2,'joint','P1 recombination, no mutation'),(0,5,2,'joint','P2 recombination, 2% mutation'),(0,7,6,'occupancy','P3 pooled vs primary, stable'),(1,7,6,'occupancy','P4 pooled vs primary, reversal'),(9,2,0,'occupancy','P5 paired vs single, small founders')]:
        r,pr=contrast(d,s,a,b,metric,label);prim.append(r);paired.extend(pr)
    write(args.out/'primary.csv',prim);write(args.out/'primary_seed_contrasts.csv',paired)
    secondary=[];secondary_seeds=[]
    for s in range(12):
        for a,b in [(2,0),(5,2),(7,6),(4,3),(1,0)]:
            for metric in ('occupancy','joint','first_accuracy','birth_brier'):
                r,pr=contrast(d,s,a,b,metric,f'{a}-{b}');secondary.append(r);secondary_seeds.extend(pr)
    write(args.out/'secondary.csv',secondary);write(args.out/'secondary_seed_contrasts.csv',secondary_seeds)
    conditions=[]
    for s in range(12):
        for a in range(8):
            r=[d[s,z,a] for z in range(3800,3820)];o={'setting':s,'setting_name':SETTING[s],'arm':a,'arm_name':ARM[a],'worlds':20}
            for metric in METRICS:
                v=np.array([float(x[metric]) for x in r]);ok=np.isfinite(v);o[metric]=float(v[ok].mean()) if ok.any() else np.nan;o[metric+'_n']=int(ok.sum())
            o['worlds_joint_birth']=sum(int(x['joint_births'])>0 for x in r)
            o['worlds_extinct']=sum(int(x['extinct']) for x in r)
            o['total_births']=sum(int(x['births']) for x in r)
            o['total_conflicts']=sum(int(x['conflicts']) for x in r)
            o['total_recombined_joint']=sum(int(x['recombined_joint']) for x in r)
            for g in range(6):o[f'genotype{g}_periods']=sum(int(x[f'genotype{g}_periods']) for x in r)
            conditions.append(o)
    write(args.out/'conditions.csv',conditions)
    traces=np.load(args.audit/'traces.npy',allow_pickle=False);assert traces.shape==(1920,240,6)
    idx={k:i for i,k in enumerate((int(r['setting']),int(r['seed']),int(r['arm'])) for r in rows)}
    # Prespecified descriptive trajectories; all seeds, including extinct.
    ts=[]
    for s in range(12):
        for a in range(8):
            v=traces[[idx[s,z,a] for z in range(3800,3820)]].mean(0)
            for period,c in enumerate(v):ts.append({'setting':s,'arm':a,'period':period,'mean_population':c.sum(),**{f'gt{g}':c[g] for g in range(6)}})
    write(args.out/'time_series.csv',ts)
    # Visuals accompany tables, not independent statistical evidence.
    fig,ax=plt.subplots(figsize=(9,4.5));v=np.array([float(x['mean']) for x in prim])*100;l=np.array([float(x['lo95']) for x in prim])*100;h=np.array([float(x['hi95']) for x in prim])*100
    ax.errorbar(v,np.arange(5),xerr=[v-l,h-v],fmt='o',capsize=4);ax.axvline(0,linestyle='--');ax.set_yticks(range(5),[x['label'] for x in prim]);ax.invert_yaxis();ax.set_xlabel('Paired difference (percentage points of possible population slots)');ax.set_title('C10 primary exploratory contrasts (95% paired t intervals)');fig.tight_layout();fig.savefig(args.out/'primary_contrasts.png',dpi=160);plt.close(fig)
    for s in (0,1,3,8,9,11):
        fig,axes=plt.subplots(2,1,figsize=(9,7),sharex=True)
        for a in range(8):
            v=traces[[idx[s,z,a] for z in range(3800,3820)]].mean(0);axes[0].plot(v.sum(1),label=ARM[a]);axes[1].plot(v[:,5],label=ARM[a])
        axes[0].set_ylabel('Mean living organisms');axes[1].set_ylabel('Mean L1 S1 organisms');axes[1].set_xlabel('Period');axes[0].legend(fontsize=7,ncol=2);fig.suptitle(SETTING[s]);fig.tight_layout();fig.savefig(args.out/f'trajectories_setting{s}.png',dpi=130);plt.close(fig)
    for metric in ('occupancy','joint','extinct'):
        v=np.array([r[metric] for r in conditions]).reshape(12,8)*100;fig,ax=plt.subplots(figsize=(10,7));im=ax.imshow(v,aspect='auto');ax.set_yticks(range(12),SETTING,fontsize=8);ax.set_xticks(range(8),ARM,rotation=40,ha='right',fontsize=8);fig.colorbar(im,ax=ax,label='Percent');ax.set_title(metric+' across locked settings');fig.tight_layout();fig.savefig(args.out/f'{metric}_heatmap.png',dpi=140);plt.close(fig)
    print(json.dumps(prim,indent=2))
if __name__=='__main__':main()
