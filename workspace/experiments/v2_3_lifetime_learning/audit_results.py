"""Post-execution raw-data audit; does not modify original archive."""
import csv, hashlib, io, itertools, json, math, sys, zipfile
from pathlib import Path
import numpy as np

EXPECTED='500df8100610cb07c85e94cf78d11d844f3206584663aee3cbd067b03cc4992e'
CHECKPOINT='091731949bb5ad5eac74c0257d05a98c8d1a4786'
SEEDS=range(2300,2340)
CONDS=list(itertools.product(('adaptive','frozen','cue_blind'),('stable','reversed'),(160,24)))
PREFIX='archean-v231-research-01/'

def audit(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        def read(name): return z.read(PREFIX+name)
        def js(name): return json.loads(read(name))
        def rows(name): return list(csv.DictReader(io.StringIO(read(name).decode())))
        def npz(name):
            with np.load(io.BytesIO(read(name)),allow_pickle=False) as a: return dict(a)
        m=js('manifest.json'); assert m['checkpoint']==CHECKPOINT and m['seeds']==list(SEEDS) and m['cohort_size']==64 and m['trials']==32 and m['conditions']==[list(c) for c in CONDS]
        assert js('COMPLETE.json')==dict(mode='research',seed_count=40,condition_rows=480,raw_archives=520)
        expected_files={f'raw/{s}/schedules.npz' for s in SEEDS}|{f'raw/{s}/{a}_{w}_{b}.npz' for s in SEEDS for a,w,b in CONDS}
        assert {x[len(PREFIX):] for x in z.namelist() if x.endswith('.npz')}==expected_files
        def keyed(name, keys):
            r=rows(name); d={tuple(x[k] for k in keys):x for x in r}; assert len(r)==len(d); return d
        ident=('seed','arm','world','budget')
        recorded=keyed('per_seed.csv',ident); trials=keyed('trial_counts.csv',ident+('encounter',)); deaths=keyed('death_counts.csv',ident+('encounter','movement_step')); pairs=keyed('paired_contrasts.csv',('seed',)); agg=keyed('trial_aggregate.csv',('arm','world','budget','encounter')); means=keyed('condition_means.csv',('arm','world','budget'))
        assert [len(x) for x in (recorded,trials,deaths,pairs,agg,means)]==[480,15360,122880,40,384,12]
        checks=0; error=0.; trajectory_count=0; choice_count=0; deaths_total=0
        def check(actual, expected):
            nonlocal checks,error
            a,b=float(actual),float(expected)
            assert (math.isnan(a) and math.isnan(b)) or math.isclose(a,b,rel_tol=0,abs_tol=1e-12),(a,b)
            if math.isfinite(a): error=max(error,abs(a-b))
            checks+=1
        per={}; pc=[]; totals={}
        for seed in SEEDS:
            s=npz(f'raw/{seed}/schedules.npz'); assert set(s)=={'mapping','cue','blind','reward_draw','action_draw'}
            assert s['mapping'].shape==(64,) and np.isin(s['mapping'],[0,1]).all() and s['mapping'].sum()==32
            for k in ('cue','blind'): assert s[k].shape==(32,64) and np.isin(s[k],[0,1]).all()
            assert (s['cue'][:16].sum(0)==8).all() and (s['cue'][16:].sum(0)==8).all()
            for k,n in [('reward_draw',2),('action_draw',3)]: assert s[k].shape==(32,64,n) and ((s[k]>=0)&(s[k]<1)).all()
            prefixes={}; cond={}
            for a,w,b in CONDS:
                d=npz(f'raw/{seed}/{a}_{w}_{b}.npz'); trajectory_count+=64
                assert set(d)=={'good','observed','potential','action','reward','steps','death_step','completed','energy','position','alive','memory'}
                for k in ('good','observed','action','reward','steps','death_step','completed'): assert d[k].shape==(32,64)
                for k in ('energy','position','alive'): assert d[k].shape==(33,64)
                assert d['memory'].shape==(33,64,2,2) and d['potential'].shape==(32,64,2)
                good=s['cue']^s['mapping']; good=good.copy()
                if w=='reversed': good[16:]^=1
                obs=s['blind'] if a=='cue_blind' else s['cue']
                np.testing.assert_array_equal(d['good'],good); np.testing.assert_array_equal(d['observed'],obs)
                potential=s['reward_draw']<np.where(good[...,None]==np.arange(2),.85,.15)
                np.testing.assert_array_equal(d['potential'],potential)
                # Independently reconstruct each encounter using stored random draws and scalar energy rules.
                e=np.full(64,b,dtype=float); alive=np.ones(64,bool); pos=np.zeros(64,int); q=np.full((64,2,2),.5)
                for t in range(32):
                    for k,v in [('energy',e),('position',pos),('alive',alive),('memory',q)]: np.testing.assert_allclose(d[k][t],v,rtol=0,atol=1e-15)
                    for i in range(64):
                        act=rew=-1; steps=death=0; complete=False
                        if alive[i]:
                            draws=s['action_draw'][t,i]; vals=q[i,obs[t,i]]
                            act=int(draws[2]<.5) if draws[1]<.2 else (int(draws[0]<.5) if vals[0]==vals[1] else int(vals[1]>vals[0]))
                            direction=2*act-1
                            for step in range(1,9):
                                pos[i]+=direction if step<=4 else -direction; e[i]-=.5; steps+=1
                                if e[i]<=0: e[i]=0; alive[i]=False; death=step; break
                                if step==4:
                                    rew=int(potential[t,i,act]); e[i]+=8*rew
                                    if a!='frozen': q[i,obs[t,i],act]+=.3*(rew-q[i,obs[t,i],act])
                            complete=bool(alive[i])
                        assert (act,rew,steps,death,complete)==tuple(d[k][t,i] for k in ('action','reward','steps','death_step','completed')),(seed,a,w,b,t,i)
                for k,v in [('energy',e),('position',pos),('alive',alive),('memory',q)]: np.testing.assert_allclose(d[k][-1],v,rtol=0,atol=1e-15)
                if b==160: assert alive.all()
                prefix={k:v[:17 if k in ('energy','position','alive','memory') else 16] for k,v in d.items()}
                if w=='stable': prefixes[a,b]=prefix
                else:
                    for k,v in prefix.items(): np.testing.assert_array_equal(v,prefixes[a,b][k])
                chosen=d['action']>=0; correct=chosen&(d['action']==good); reward=d['reward']==1
                choice_count+=int(chosen.sum()); deaths_total+=int((d['death_step']>0).sum()); r={}
                for label,start,end in [('late_acquisition',8,16),('early_reversal',16,20),('late_reversal',24,32),('all',0,32)]+[(f'trial_{t+1:02}',t,t+1) for t in range(32)]:
                    c=int(correct[start:end].sum()); n=int(chosen[start:end].sum()); r.update({label+'_correct_all':c/((end-start)*64),label+'_correct_conditional':c/n if n else float('nan'),label+'_choices':n})
                r.update(survival=alive.mean(),final_energy=e.mean(),acquisition_rate=reward.mean(),mean_completed_trips=d['completed'].sum()/64)
                key=(str(seed),a,w,str(b)); rr=recorded[key]; assert set(rr)==set(ident)|set(r)
                for k,v in r.items(): check(v,rr[k])
                for t in range(32):
                    k=key+(str(t+1),); vals=[64,chosen[t].sum(),correct[t].sum(),reward[t].sum(),d['alive'][t+1].sum()]
                    for name,v in zip(('scheduled','choices','correct','rewards','alive_after'),vals): check(v,trials[k][name])
                    ak=k[1:]; totals[ak]=totals.get(ak,np.zeros(5,int))+vals
                    for j in range(1,9): check((d['death_step'][t]==j).sum(),deaths[k+(str(j),)]['deaths'])
                cond[a,w,b]=r; per.setdefault((a,w,b),[]).append(r)
            def v(a,w,b,k): return cond[a,w,b][k]
            ca='late_acquisition_correct_all'; cr='late_reversal_correct_all'
            p={'primary_adaptive_minus_frozen':v('adaptive','stable',160,ca)-v('frozen','stable',160,ca),'reversal_late_minus_early':v('adaptive','reversed',160,cr)-v('adaptive','reversed',160,'early_reversal_correct_all'),'reversal_late_minus_stable':v('adaptive','reversed',160,cr)-v('adaptive','stable',160,cr),'genuine_minus_blind_late_acquisition':v('adaptive','stable',160,ca)-v('cue_blind','stable',160,ca)}
            for w,b,c,k in itertools.product(('stable','reversed'),(160,24),('frozen','cue_blind'),('survival','final_energy')): p[f'{w}_{b}_adaptive_minus_{c}_{k}']=v('adaptive',w,b,k)-v(c,w,b,k)
            assert set(pairs[(str(seed),)])==set(p)|{'seed'}
            for k,x in p.items(): check(x,pairs[(str(seed),)][k])
            pc.append(p)
        for k,vv in totals.items():
            r=agg[k]
            for name,v in zip(('scheduled','choices','correct','rewards','alive_after'),vv): check(v,r[name])
            check(vv[2]/vv[0],r['correct_all']); check(vv[2]/vv[1] if vv[1] else float('nan'),r['correct_conditional'])
        for (a,w,b),rs in per.items():
            r=means[a,w,str(b)]
            for k in set(r)-{'arm','world','budget'}: check(np.mean([x[k] for x in rs]),r[k])
        summary=js('summary.json'); x=np.array([p['primary_adaptive_minus_frozen'] for p in pc]); mu=x.mean(); sd=x.std(ddof=1); half=2.02269092*sd/math.sqrt(40)
        for k,v in dict(n=40,mean=mu,sample_sd=sd,lower_95=mu-half,upper_95=mu+half).items(): check(v,summary['primary'][k])
        assert summary['primary']['supports_primary']==bool(mu-half>0)
        for k,v in summary['exploratory_mean_contrasts'].items(): check(np.mean([p[k] for p in pc]),v)
        return dict(zip_sha256=EXPECTED,checkpoint=CHECKPOINT,archives=520,trajectories=trajectory_count,scheduled_encounters=trajectory_count*32,actual_choices=choice_count,deaths=deaths_total,table_values_verified=checks,max_table_absolute_difference=error,primary=summary['primary'],positive_seed_contrasts=int((x>0).sum()),min_seed_contrast=float(x.min()),max_seed_contrast=float(x.max()),audit_python=sys.version.split()[0],audit_numpy=np.__version__)

if __name__=='__main__':
    print(json.dumps(audit(Path(sys.argv[1])),indent=2))
