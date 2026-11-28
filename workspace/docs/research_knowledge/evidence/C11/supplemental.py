"""Post-execution secondary reconstruction, no simulations. All metrics descriptive."""
import csv,io,zipfile,struct,json
from pathlib import Path
import numpy as np
from scipy.stats import t
base=Path('/mnt/data'); out=base/'c11_review_local'; repo=out/'repo'; lock=list(csv.DictReader(next((repo/'workspace/experiments').glob('c11*/design.csv')).open()))
rows=[]; ages=[]; parity=0; risks=[]
for study in 'AB':
 with zipfile.ZipFile(base/f'Archean_C11_{study}_Raw_Evidence.zip') as z:
  design=list(csv.DictReader(io.StringIO(z.read(f'{study}_evaluation/design.csv').decode())))
  assert [{k:v for k,v in r.items() if k not in ('path','fixture')} for r in design]==[r for r in lock if r['study']==study and r['phase']=='evaluation'];assert all(r['fixture']=='-1' for r in design)
  for r in design:
   path=f'{study}_evaluation/{r["path"]}/'; founder=list(z.read(path+'founders.bin')); events=list(struct.iter_unpack('<HHHB',z.read(path+'events.bin'))); gt=np.bincount(founder,minlength=6); roster={i:(g,-1) for i,g in enumerate(founder)}; done=[[] for _ in range(6)]; censor=[[] for _ in range(6)]; deaths=np.zeros((240,6),int); parents=deaths.copy(); children=deaths.copy(); idx=0
   for period,aid,parent,g in events:
    if parent==65535:
     old,born=roster.pop(aid);assert old==g;done[g].append(period-born);deaths[period,g]+=1
    else:
     pg,_=roster[parent];parents[period,pg]+=1;children[period,g]+=1;roster[aid]=(g,period)
   for g,born in roster.values():censor[g].append(239-born)
   pre=gt+np.vstack([np.zeros((1,6),int),np.cumsum(children-deaths,axis=0)[:-1]])
   postdeath=pre-deaths;postbirth=postdeath+children
   assert np.all(postdeath>=0) and np.all(postbirth>=0)
   ident={'study':study,'condition':r['condition'],'seed':int(r['seed'])}
   for name,mask in [('learning',np.arange(6)>=3),('joint',np.arange(6)>=4)]:
    def freq(a):
     n=a.sum(axis=1); return np.divide(a[:,mask].sum(axis=1),n,out=np.full(240,np.nan),where=n>0)
    x=freq(postdeath)-freq(pre);y=freq(postbirth)-freq(postdeath)
    rows.append({**ident,'trait':name,'defined_death_stage_periods':int(np.isfinite(x).sum()),'death_stage_frequency_change_sum':float(np.nansum(x)),'defined_birth_stage_periods':int(np.isfinite(y).sum()),'birth_stage_frequency_change_sum':float(np.nansum(y)),'deaths_trait':int(deaths[:,mask].sum()),'births_to_trait_parents':int(parents[:,mask].sum()),'trait_offspring':int(children[:,mask].sum()),'net_transmission_change':int((children[:,mask]-parents[:,mask]).sum()),'extinct':int(postbirth[-1].sum()==0)})
   for g in range(6):
    ages.append({**ident,'genotype':g,'observed_deaths':len(done[g]),'death_lifetime_sum_periods':sum(done[g]),'mean_completed_lifetime':np.mean(done[g]) if done[g] else '', 'right_censored':len(censor[g]),'censored_exposure_sum_periods':sum(censor[g]),'mean_censored_exposure':np.mean(censor[g]) if censor[g] else ''})
  if study=='B':
   for seed in range(4000,4064):
    p=f'B_evaluation/4_{seed}/';q=f'B_evaluation/5_{seed}/';assert z.read(p+'mapping.bin')==z.read(q+'mapping.bin')
    e=lambda x:[r[:3] for r in struct.iter_unpack('<HHHB',z.read(x+'events.bin'))];assert e(p)==e(q)
    dtype=np.dtype([('disc','V14'),('prior','<f8'),('belief','<f8')]); a=np.frombuffer(z.read(p+'actions.bin'),dtype=dtype);b=np.frombuffer(z.read(q+'actions.bin'),dtype=dtype);assert np.array_equal(a['disc'],b['disc']);np.testing.assert_allclose(a['prior'],b['prior'],rtol=0,atol=1e-12);np.testing.assert_allclose(a['belief'],b['belief'],rtol=0,atol=1e-12);parity+=1
 ix={(r['condition'],r['seed']):r['extinct'] for r in rows if r['study']==study and r['trait']=='learning'}
 pairs=[('A2','A1'),('A3','A1')] if study=='A' else [('B2-informative','B1-informative'),('B3-informative','B3-null'),('B4-informative','B3-informative'),('B4-null','B3-null'),('B2-null','B1-null')]
 for a,b in pairs:
  seeds=range(3900,3964) if study=='A' else range(4000,4064);x=np.array([ix[a,s]-ix[b,s] for s in seeds]);m=x.mean();h=t.ppf(.975,63)*x.std(ddof=1)/8;risks.append({'study':study,'contrast':a+' minus '+b,'n':64,'risk_difference':m,'ordinary_lo95':m-h,'ordinary_hi95':m+h})
for name,data in [('demographic_stage_per_world.csv',rows),('longevity_per_world_genotype.csv',ages),('extinction_risk_contrasts.csv',risks)]:
 with (out/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
print(json.dumps({'locked_design_rows_match':True,'null_parity_blocks':parity,'demographic_rows':len(rows),'longevity_rows':len(ages),'extinction_risk_contrasts':len(risks)},indent=2))
