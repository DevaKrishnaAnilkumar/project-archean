import csv, hashlib, io, json, struct, zipfile
from pathlib import Path
import numpy as np
from scipy.stats import t
BASE=Path('/mnt/data')
review=zipfile.ZipFile(BASE/'Archean_C11_Scientific_Review.zip')
def verify(z):
    manifest=dict((name,h) for h,name in (line.split(maxsplit=1) for line in z.read('SHA256SUMS.txt').decode().splitlines()))
    assert set(manifest)==set(z.namelist())-{'SHA256SUMS.txt'}
    for name,h in manifest.items(): assert hashlib.sha256(z.read(name)).hexdigest()==h,name
    return len(manifest)
def rows(z,path): return list(csv.DictReader(io.StringIO(z.read(path).decode())))
def histories(founders,ev,periods):
    roster=dict(enumerate(founders)); seen=set(roster); changes=np.zeros((240,6),dtype=np.int64); nextid=60
    for (aid,parent,g),p in zip(ev,periods,strict=True):
        assert 0<=g<=5 and 0<=p<240
        if parent==65535:
            assert roster.pop(aid)==g; changes[p,g]-=1
        else:
            assert parent in roster and aid not in seen and aid==nextid
            nextid+=1;roster[aid]=g;seen.add(aid);changes[p,g]+=1
        assert len(roster)<=120
    counts=np.bincount(founders,minlength=6)+np.cumsum(changes,axis=0)
    assert np.all(counts>=0) and np.all(counts.sum(axis=1)<=120)
    return counts
out={'review_manifest_files':verify(review),'studies':{}}
for study in 'AB':
    z=zipfile.ZipFile(BASE/f'Archean_C11_{study}_Raw_Evidence.zip'); manifest_n=verify(z)
    design=rows(z,f'{study}_evaluation/design.csv'); ref=rows(review,f'{study}_evaluation_audit/worlds.csv'); archived={(r['condition'],int(r['seed'])):r for r in ref}; assert len(archived)==len(design)
    curves=np.load(io.BytesIO(review.read(f'{study}_evaluation_audit/curves.npy')),allow_pickle=False)
    curve_ix={ (r['condition'],int(r['seed'])):i for i,r in enumerate(ref)}
    measures={}; replays=0; ext={}; actions=0; birth=0;death=0
    for r in design:
        key=r['condition'],int(r['seed']); assert key not in measures
        prefix=f'{study}_evaluation/{r["path"]}/';read=lambda n:z.read(prefix+n)
        f=list(read('founders.bin'));assert len(f)==60
        events=list(struct.iter_unpack('<HHHB',read('events.bin')));periods=[e[0] for e in events]; assert periods==sorted(periods)
        ev=[e[1:] for e in events]; counts=histories(f,ev,periods);n=counts.sum();a=counts[:,4:].sum();assert n>0
        idx=curve_ix[key];assert np.array_equal(counts,curves[idx,:,:6]);
        ps=np.zeros((240,6),dtype=np.int64);replay_num=int(r['replays']);replays+=replay_num
        for j in range(replay_num):
            pe=list(struct.iter_unpack('<HHB',read(f'passive{j}.bin')));assert len(pe)==len(ev)
            assert all((x[1]==65535)==(y[1]==65535) for x,y in zip(pe,ev));pc=histories(f,pe,periods);assert np.array_equal(pc.sum(axis=1),counts.sum(axis=1));ps+=pc
        assert np.array_equal(ps,curves[idx,:,7:13]);p=ps[:,4:].sum()/replay_num if replay_num else float('nan')
        extinct=int(counts[-1].sum()==0);ext[key[0]]=ext.get(key[0],0)+extinct
        actions+=len(read('actions.bin'))//30;birth+=sum(x[1]!=65535 for x in ev);death+=sum(x[1]==65535 for x in ev)
        measures[key]={'U':n/28800,'D':(a-p)/28800,'G':(a-p)/n}
    seeds=range(3900,3964) if study=='A' else range(4000,4064)
    def v(c,k):return np.array([measures[c,s][k] for s in seeds])
    contrasts={'A-P1':v('A1','D'),'A-P2':v('A1','D')-v('A2','D'),'A-P3':v('A1','D')-v('A3','D')} if study=='A' else {'B-P1':v('B2-informative','U')-v('B1-informative','U'),'B-P2':v('B3-informative','G')-v('B3-null','G')}
    primary={r['contrast']:r for r in rows(review,f'{study}_results/primary.csv')}; seedrows=rows(review,f'{study}_results/primary_seed_contrasts.csv'); assert [int(r['seed']) for r in seedrows]==list(seeds)
    results={}
    for label,x in contrasts.items():
        np.testing.assert_allclose(x,[float(r[label]) for r in seedrows],atol=1e-12,rtol=0)
        m=x.mean();sd=x.std(ddof=1);hw=t.ppf(1-.05/(2*len(contrasts)),63)*sd/8
        for k,val in {'mean':m,'sd':sd,'adjusted_lo':m-hw,'adjusted_hi':m+hw}.items():assert abs(float(primary[label][k])-val)<1e-12
        results[label]={'mean_pp':100*m,'adjusted_ci_pp':[100*(m-hw),100*(m+hw)],'positive_blocks':int((x>0).sum())}
    out['studies'][study]={'manifest_files':manifest_n,'worlds':len(design),'replays':replays,'extinctions':ext,'births':birth,'deaths':death,'action_rows':actions,'primary':results,'all_period_active_and_summed_passive_genotype_counts_match':True}
print(json.dumps(out,indent=2))
