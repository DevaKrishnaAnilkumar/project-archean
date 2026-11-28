"""Independent reconstruction of C10 ledgers; no import of the simulation implementation.
Uses archived C08 audit RNG primitives and independent vectorised replay of every action.
"""
import argparse,csv,importlib.util,json,math
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('c08audit',Path(__file__).parent.parent/'c08_heritable_learning/audit.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
N,CAP,DEAD=240,120,65535
BIRTH=np.dtype([(k,'<u2') for k in ('t','id','p1','p2')]+[(k,'u1') for k in ('pre','gt')]+[(k,'<u2') for k in ('debit1','debit2')]+[(k,'<f8') for k in ('p1belief','p2belief','child')])
PERIOD=np.dtype([(k,'<u2') for k in ('eligible','births','unpaired','blocked')]+[('counts','<u2',(6,))])
U=np.uint64
INC=U(0x9e3779b97f4a7c15)
def mix(x):
    x=np.asarray(x,dtype='u8')
    with np.errstate(over='ignore'):
        x=(x^(x>>U(30)))*U(0xbf58476d1ce4e5b9);x=(x^(x>>U(27)))*U(0x94d049bb133111eb)
    return x^(x>>U(31))
def rng(seed,stream,key,draw=1):
    state=U(old.mix(seed)^old.mix(stream+0x7fa56e1)^old.mix(0x50ab921))^mix(np.asarray(key,dtype='u8')+U(0x8b89e11))
    with np.errstate(over='ignore'):
        return mix(state+INC*U(draw))
def unit(seed,stream,key,draw=1):return (rng(seed,stream,key,draw)>>U(11)).astype('f8')*2**-53
def close(a,b):
    assert np.allclose(a,b,rtol=0,atol=1e-12)
def ratio(a,b):return a/b if b else float('nan')

def expected_design(setting):
    r,fee,prize,f,initial,q,mu,balanced=0,5,192,60,384,.85,.02,0
    if setting in (1,4,6):r=1
    if setting==2:r=2
    if setting in (3,4):mu=0.
    if setting in (5,6):mu=.10
    if setting in (7,8):prize=128
    if setting==8:fee=40
    if setting==9:f,initial=12,128
    if setting==10:balanced=1
    if setting==11:q=.5
    return r,fee,prize,f,initial,q,mu,balanced

def audit(path,row):
    read=lambda name,dtype:np.fromfile(path/(name+'.bin'),dtype)
    setting,seed,arm=[int(row[k]) for k in ('setting','seed','arm')]
    regime,fee,prize,f,initial,q,mu,balanced=expected_design(setting)
    assert (regime,fee,prize,f,initial,q,mu,balanced)==tuple(float(row[k]) for k in ('regime','fee_ticks','reward_ticks','founders','initial_ticks','q','mutation','balanced'))
    paired=arm>=2; recomb=arm>=5; mem=0 if arm in (0,2,5) else 2 if arm in (4,7) else 1
    g=read('founders','u1'); maps=read('mapping','u1'); a=read('actions',old.ACTION); e=read('events',old.EVENT); b=read('births',BIRTH); p=read('periods',PERIOD)
    expected=list(np.repeat(np.arange(6),f//6)) if balanced else [2]*(f//2)+[3]*(f//2)
    draw=old.draws(seed,2)
    for i in range(f,1,-1):
        j=old.uniform_index(draw,i);expected[i-1],expected[j]=expected[j],expected[i-1]
    assert np.array_equal(g,expected)
    draw=old.draws(seed,1); m=old.uniform_index(draw,2); rm=np.array([old.uniform_index(draw,2) for _ in range(N)])
    assert np.array_equal(maps,[np.full(N,m),m^(np.arange(N)//24%2),rm][regime])
    assert len(p)==N
    be=e[e['parent']!=DEAD]; de=e[e['parent']==DEAD]
    assert all(np.array_equal(b[x],be[y]) for x,y in [('t','t'),('id','id'),('p1','parent'),('gt','gt')])
    n=f+len(b); assert np.array_equal(b['id'],np.arange(f,n));gt=np.r_[g,b['gt']]; assert np.all(gt<6)
    assert np.all(e['id']<n) and np.all(e['t']<N) and np.all(e['t'][1:]>=e['t'][:-1])
    born=np.full(n,-1,dtype='i4');born[f:]=b['t']; died=np.full(n,N,dtype='i4');died[de['id']]=de['t']; assert len(np.unique(de['id']))==len(de) and np.all(born<died) and np.array_equal(de['gt'],gt[de['id']])
    t=a['t'].astype('i4'); aid=a['id'].astype('i4'); assert np.all(aid<n) and np.all(t<N)
    assert np.all(t>born[aid]) and np.all(t<=died[aid]); key=aid*N+t;assert len(np.unique(key))==len(a)
    assert np.array_equal(np.bincount(aid,minlength=n),np.minimum(N-1,died)-born)
    dead=a['after']==0;assert np.array_equal(de['id'],aid[dead]) and np.array_equal(de['t'],t[dead]);assert np.all(a['after']>=0)
    assert np.all(t[1:]>=t[:-1]); assert np.all(np.diff(aid)[np.diff(t)==0]>0)
    delta=np.zeros((N+1,6),dtype='i4');np.add.at(delta,(np.maximum(0,born),gt),1);np.add.at(delta,(died,gt),-1);trace=delta.cumsum(0)[:N];assert np.array_equal(trace,p['counts']) and np.all(trace>=0) and np.all(trace.sum(1)<=CAP)
    pop=trace.sum(1); assert not np.any(pop[np.argmax(pop==0):]) if np.any(pop==0) else True
    # Reconstruct energy continuity including both reproductive parents.
    order=np.argsort(key);sa=a[order];sk=key[order];si=aid[order];st=t[order];first=st==born[si]+1
    parents=b['p1'].astype('i4');partners=b['p2'].astype('i4');bt=b['t'].astype('i4')
    assert np.all(parents<b['id']) and np.all(born[parents]<bt) and np.all(died[parents]>bt)
    if paired:
        assert np.all(partners<b['id']) and np.all(partners!=parents) and np.all(born[partners]<bt) and np.all(died[partners]>bt)
        assert np.all(b['debit1']==104) and np.all(b['debit2']==104)
    else:assert np.all(partners==DEAD) and np.all(b['debit1']==208) and np.all(b['debit2']==0)
    pk=parents*N+bt; pk2=partners*N+bt if paired else np.array([],dtype='i4'); allpk=np.r_[pk,pk2];assert len(np.unique(allpk))==len(allpk)
    def row_at(keys):
        idx=np.searchsorted(sk,keys);assert np.all(idx<len(sk)) and np.array_equal(sk[idx],keys);return idx
    ip=row_at(pk); assert np.all(sa['after'][ip]>=512);close(b['p1belief'],sa['belief'][ip]);
    if paired:
        ip2=row_at(pk2); assert np.all(sa['after'][ip2]>=512);close(b['p2belief'],sa['belief'][ip2])
    else: close(b['p2belief'],.5)
    newborn=np.r_[np.full(f,.5),b['child']];close(b['child'],.5 if mem==0 else b['p1belief'] if mem==1 else .5*(b['p1belief']+b['p2belief']))
    debit=np.zeros(len(sa),dtype='i4'); nextkey=allpk+1; ix=np.searchsorted(sk,nextkey); costs=np.r_[b['debit1'],b['debit2']] if paired else b['debit1']; valid=(ix<len(sk))&(sk[np.minimum(ix,len(sk)-1)]==nextkey)&(allpk%N<N-1);debit[ix[valid]]=costs[valid]
    energy=np.where(first,np.where(si<f,initial,192),np.roll(sa['after'],1)).astype('i4')-debit;assert np.array_equal(energy,sa['before'])
    learn=gt[aid]>=3; maint=a['before'].astype('i4')-16; alive=maint>0;sampled=a['site']>=0;attempted=a['patch']>=0
    prev=np.where(first,newborn[si],np.roll(sa['belief'],1));close(sa['prior'],np.where(learn[order]&alive[order],.05+.9*prev,prev))
    # Reconstruct all realised random draws, not just a sample.
    rk=(t.astype('u8')*U(65536)+aid.astype('u8')); hidden=(rng(seed,3,rk)&U(1)).astype('i1');assert np.array_equal(a['hidden'],np.where(alive,hidden,-1))
    assert np.array_equal(sampled,(maint>fee+32)&(unit(seed,6,rk)<(gt[aid]%3)*.5))
    prior=a['prior'];tie1=(rng(seed,7,rk)&U(1)).astype('i1');tie2=(rng(seed,7,rk,2)&U(1)).astype('i1')
    site=np.where(np.abs((q-.5)*(2*prior-1))<=1e-12,tie1,prior>.5).astype('i1');assert np.array_equal(a['site'],np.where(sampled,site,-1))
    cue=np.where(unit(seed,4,2*rk+site.astype('u8'))<np.where(site==maps[t],q,.5),hidden,1-hidden);assert np.array_equal(a['obs'],np.where(sampled,cue,-1))
    assert np.array_equal(attempted,maint-fee*sampled>32)
    accuracy=.5+(q-.5)*np.where(site==1,prior,1-prior); posterior_patch=np.where(sampled,np.where(cue==1,accuracy,1-accuracy),.5)
    patch=np.where(np.abs(posterior_patch-.5)<=1e-12,tie2,posterior_patch>.5).astype('i1');assert np.array_equal(a['patch'],np.where(attempted,patch,-1))
    got=attempted&(unit(seed,5,2*rk+patch.astype('u8'))<np.where(patch==hidden,.85,.15));assert np.array_equal(a['got'],got)
    after_reward=maint-fee*sampled-32*attempted+prize*got;returns=np.where(attempted,np.minimum(4,(after_reward+7)//8),0);assert np.array_equal(a['returns'],returns) and np.array_equal(a['after'],np.maximum(0,after_reward-8*returns))
    selected=sampled&learn;po=prior.copy();ll=[]
    for m in (0,1):
        ac=np.where(site[selected]==m,q,.5);h0=np.where(cue[selected]==0,ac,1-ac);w=np.where((patch[selected]==0)==got[selected],.85,.15);ll.append(.5*(h0*w+(1-h0)*(1-w)))
    po[selected]=prior[selected]*ll[1]/((1-prior[selected])*ll[0]+prior[selected]*ll[1]);close(a['belief'],po)
    # Confirm ordered eligible parent pairs, independently seeded recombination and mutation.
    eligible=a['after']>=512;ec=np.bincount(t[eligible],minlength=N);available=CAP-np.bincount(t[~dead],minlength=N);bc=np.bincount(bt,minlength=N);possible=ec//(2 if paired else 1)
    assert np.array_equal(bc,np.minimum(possible,available)) and np.array_equal(p['births'],bc) and np.array_equal(p['eligible'],ec) and np.array_equal(p['blocked'],possible-bc) and np.array_equal(p['unpaired'],ec%2 if paired else np.zeros(N))
    for period in np.flatnonzero(bc):
        ids=aid[eligible&(t==period)].tolist();dr=old.draws(seed,9,int(period))
        for i in range(len(ids),1,-1):
            j=old.uniform_index(dr,i);ids[i-1],ids[j]=ids[j],ids[i-1]
        mask=bt==period;assert np.array_equal(parents[mask],ids[:bc[period]*(2 if paired else 1):(2 if paired else 1)])
        if paired:assert np.array_equal(partners[mask],ids[1:bc[period]*2:2])
    pre=gt[parents].copy()
    if recomb:
        l=(rng(seed,14,b['id'])&U(1))!=0;s=(rng(seed,14,b['id'],2)&U(1))!=0
        pre=3*np.where(l,gt[partners]//3,pre//3)+np.where(s,gt[partners]%3,pre%3)
    assert np.array_equal(pre,b['pre']);mut=3*np.where(unit(seed,8,b['id'])<mu,1-pre//3,pre//3)+np.where(unit(seed,8,b['id'],2)<mu,(pre%3+1+(rng(seed,8,b['id'],3)&U(1)).astype('i4'))%3,pre%3);assert np.array_equal(mut,b['gt'])
    if not recomb and not mu and not balanced:assert not np.any(gt==5)
    if q==.5: close(a['belief'],.5);close(b['child'],.5)
    observe=bt<N-1; firstkeys=b['id'][observe].astype('i4')*N+bt[observe]+1;fi=row_at(firstkeys);fa=sa[fi];fc=(fa['patch']>=0)&(fa['patch']==fa['hidden']);fa_count=int((fa['patch']>=0).sum())
    conflict=(b['p1belief']-.5)*(b['p2belief']-.5)<0; brier=(b['child'][observe]-maps[bt[observe]+1])**2
    # Retain original observable birth cohort as denominator; conditional endpoint is separate.
    out={**row,'actions':len(a),'births':len(b),'deaths':len(de),'occupancy':pop.sum()/(CAP*N),'joint':trace[:,5].sum()/(CAP*N),'joint_living':ratio(trace[:,5].sum(),pop.sum()),'final_population':int(pop[-1]),'extinct':int(pop[-1]==0),'extinction_period':int(np.flatnonzero(pop==0)[0]) if np.any(pop==0) else N,'mean_population':float(pop.mean()),'richness':int(len(np.unique(gt))),'mean_richness':float((trace>0).sum(1).mean()),'eligible':int(ec.sum()),'unpaired':int(p['unpaired'].sum()),'blocked':int(p['blocked'].sum()),'joint_births':int((b['gt']==5).sum()),'first_joint_birth':int(bt[b['gt']==5].min()) if np.any(b['gt']==5) else N,'recombined_joint':int(((b['pre']==5)&(gt[parents]!=5)&(gt[np.minimum(partners,n-1)]!=5)).sum()) if recomb else 0,'mutated_births':int((pre!=b['gt']).sum()),'birth_debit_ticks':int(b['debit1'].sum()+b['debit2'].sum()),'observable_births':int(observe.sum()),'first_attempts':fa_count,'first_correct':int(fc.sum()),'first_accuracy':ratio(int(fc.sum()),int(observe.sum())),'first_conditional':ratio(int(fc.sum()),fa_count),'birth_brier':float(brier.mean()) if len(brier) else float('nan'),'disagreement':float(np.abs(b['p1belief']-b['p2belief']).mean()) if paired and len(b) else float('nan'),'conflicts':int(conflict.sum()) if paired else 0,'conflict_births_observable':int((conflict&observe).sum()) if paired else 0,'conflict_brier':float(brier[conflict[observe]].mean()) if paired and np.any(conflict&observe) else float('nan'),'accuracy':ratio(int((attempted&(a['patch']==a['hidden'])).sum()),int(attempted.sum()))}
    for k in range(6):out[f'genotype{k}_periods']=int(trace[:,k].sum())
    return out,trace

def main():
    p=argparse.ArgumentParser();p.add_argument('raw',type=Path);p.add_argument('out',type=Path);p.add_argument('--mode',choices=['smoke','eval'],required=True);args=p.parse_args();assert not args.out.exists();args.out.mkdir(parents=True)
    rows=list(csv.DictReader((args.raw/'design.csv').open()));seeds=range(3790,3792) if args.mode=='smoke' else range(3800,3820);expected={(s,z,a) for s in range(12) for z in seeds for a in range(8)};assert len(rows)==len(expected) and {(int(r['setting']),int(r['seed']),int(r['arm'])) for r in rows}==expected
    summary=[];traces=[]
    for i,r in enumerate(rows):
        try:stat,trace=audit(args.raw/r['path'],r)
        except Exception as exc:raise RuntimeError(f'Failed independent audit: {r["path"]}') from exc
        summary.append(stat);traces.append(trace)
        if (i+1)%192==0:print('Audited',i+1,'worlds',flush=True)
    for seed in seeds:
        for arms in [(0,1),(2,3,4),(5,6,7)]:
            first=args.raw/f'11_{seed}_{arms[0]}'
            for arm in arms[1:]:
                other=args.raw/f'11_{seed}_{arm}'
                for name in ('founders','mapping','actions','events','births','periods'):assert (first/(name+'.bin')).read_bytes()==(other/(name+'.bin')).read_bytes(),(seed,arms,name)
    with (args.out/'worlds.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    np.save(args.out/'traces.npy',np.array(traces,dtype='u2'),allow_pickle=False)
    result={'worlds':len(summary),'actions':sum(r['actions'] for r in summary),'births':sum(r['births'] for r in summary),'deaths':sum(r['deaths'] for r in summary),'extinct':sum(r['extinct'] for r in summary),'null_parity_seeds':len(seeds),'all_action_rng_replayed':True,'all_parent_pairings_replayed':True,'all_birth_mutations_and_recombination_replayed':True,'status':'PASS'};(args.out/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
