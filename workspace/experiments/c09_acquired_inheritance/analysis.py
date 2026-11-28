"""World-scale inference and complete C09 setting summaries."""
import argparse
import csv
from pathlib import Path
import numpy as np

POP=("A blank","B full parent","C evolving parent","D evolving other survivor")
T={19:2.0930240544,18:2.1009220402,17:2.1098155778,16:2.1199052992,15:2.1314495456,
   14:2.1447866879,13:2.1603686565,12:2.1788128297,11:2.2009851601,10:2.2281388520,
   9:2.262157163,8:2.306004135,7:2.364624252,6:2.446911851,5:2.570581836,
   4:2.776445105,3:3.182446305,2:4.30265273,1:12.706204736}

def table(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def ratio(a,b):
    return a/b if b else float("nan")

def interval(values):
    values=np.array(values,float)
    values=values[np.isfinite(values)]
    mean=values.mean() if len(values) else float("nan")
    sd,half=float("nan"),float("nan")
    if len(values)>1:
        sd=values.std(ddof=1)
        half=T[len(values)-1]*sd/np.sqrt(len(values))
    return {"n":len(values),"mean":mean,"sd":sd,"lo95":mean-half,"hi95":mean+half}

def analyse(audit,out):
    with (audit/"worlds.csv").open() as f:
        worlds=list(csv.DictReader(f))
    curves=np.load(audit/"curves.npy",allow_pickle=False)
    durations=np.load(audit/"offspring_durations.npy",allow_pickle=False)
    assert len(worlds)==len(curves)==len(durations)==1200
    assert np.all(durations.sum(axis=(1,2,3))==[int(r["births"]) for r in worlds])
    out.mkdir()
    by={(int(w["setting"]),int(w["population"]),int(w["seed"])):i for i,w in enumerate(worlds)}
    def group(s,p):
        return [by[s,p,seed] for seed in range(3700,3720)]
    vals=lambda s,p,k: np.array([float(worlds[i][k]) for i in group(s,p)])
    enrich={s:vals(s,2,"enrichment") for s in range(15)}
    primary={"stable cheap free enrichment":enrich[0],
             "stable minus reversal":enrich[0]-enrich[4],
             "stable minus unpredictable":enrich[0]-enrich[8]}
    contrasts=[{"contrast":name,**interval(values)} for name,values in primary.items()]
    table(out/"primary.csv",contrasts)
    table(out/"paired_primary.csv",[{"seed":3700+i,**{name:float(v[i]) for name,v in primary.items()}}
                                     for i in range(20)])
    conditions,alleles,age_rows,secondary,time_rows=[],[],[],[],[]
    traces={}
    for s in range(15):
        for p in range(4):
            keys=group(s,p)
            curves_slice=curves[keys]
            trace=curves_slice.mean(axis=0)
            traces[s,p]=trace
            age=durations[keys].sum(axis=0)
            row=worlds[keys[0]]
            d={k:row[k] for k in ("setting","population","regime","fee_ticks","reward_ticks","transfer_ticks","q")}
            values=lambda k:vals(s,p,k)
            total=lambda k:values(k).sum()
            pop_alive=values("extinct_period")==240
            occupancy=values("occupancy")
            density=curves_slice[:,:,:3].sum()
            conditions.append({**d,"active_occupancy":occupancy.mean(),
                "passive_occupancy":values("passive_mean").mean(),
                **{f"enrichment_{k}":v for k,v in interval(values("enrichment")).items()},
                "abundance":values("abundance").mean(),"extinct":int((~pop_alive).sum()),
                "capped_extinction_time":values("extinct_period").mean(),
                "final_population":values("final_pop").mean(),"births":int(total("births")),
                "deaths":int(total("deaths")),"blocked_births":int(total("blocked_births")),
                "final_lineages":values("final_lineages").mean(),"donor_fallback":int(total("fallback")),
                "transmission_units":total("transfer")/16,"realised_t_positive":ratio(curves_slice[:,:,1:3].sum(),density),
                "births_observable":int(total("births_observable")),"first_attempts":int(total("first_attempts")),
                "first_correct_all_births":ratio(total("first_correct"),total("births")),
                "first_correct_observable_births":ratio(total("first_correct"),total("births_observable")),
                "first_correct_among_attempts":ratio(total("first_correct"),total("first_attempts")),
                "first_period_death_observable":ratio(total("first_period_deaths"),total("births_observable")),
                "birth_brier":ratio(total("belief_brier_sum"),total("births_observable")),
                "donor_brier":ratio(total("donor_brier_sum"),total("births_observable")),
                "switch_start":int(total("switch_start")),"switch_attempts":int(total("switch_attempts")),
                "switch_correct_per_start_three_periods":ratio(total("switch_correct"),total("switch_start")),
                "switch_accuracy_per_attempt":ratio(total("switch_correct"),total("switch_attempts")),
                "switch_death_per_start":ratio(total("switch_deaths"),total("switch_start")),
                "wrong_birth_belief":int(total("wrong_birth_belief")),"revised":int(total("revised")),
                "revision_mean_periods_after_first_action_occasion_completed_only":ratio(total("revision_period_sum"),total("revised")),
                "revision_mean_censor_periods":ratio(total("revision_censor_period_sum"),total("wrong_birth_belief")-total("revised")),
                "mean_offspring_observed_duration":ratio(sum(total(f"t{i}_offspring_periods") for i in range(3)),total("births")),
                "offspring_right_censored":int(age[:,:,1].sum())})
            for g in range(3):
                a=lambda k:total(f"t{g}_{k}")
                alleles.append({**d,"allele":g/2,"living_frequency":ratio(a("living"),density),
                    "final_frequency":ratio(a("final"),values("final_pop").sum()),"births":int(a("births")),
                    "births_per_at_risk_period":ratio(a("parents"),a("action_periods")),
                    "mean_observed_offspring_duration":ratio(a("offspring_periods"),a("births")),
                    "offspring_right_censored":int(a("offspring_censored")),
                    "first_correct_per_birth":ratio(a("first_correct"),a("births")),
                    "first_correct_per_observable_birth":ratio(a("first_correct"),a("births_observable")),
                    "first_correct_per_attempt":ratio(a("first_correct"),a("first_attempt")),
                    "first_brier":ratio(a("birth_brier_sum"),a("births_observable")),
                    "transmission_units":a("transfer")/16,"mutations_into_allele":int(a("mutations"))})
                risk=age[g].sum()
                for t,(died,censored) in enumerate(age[g]):
                    age_rows.append({**d,"allele":g/2,"observed_action_periods":t,"risk":int(risk),
                        "died":int(died),"censored":int(censored)})
                    risk-=died+censored
            for t,(g0,g1,g2,lineages) in enumerate(trace):
                time_rows.append({**d,"period":t,"T0":g0,"T05":g1,"T1":g2,"lineages":lineages})
        for p,q in ((1,0),(2,3)):
            def series(k,which):
                if k=="persistence":
                    return (vals(s,which,"extinct_period")==240).astype(float)
                if k in ("first_choice","child_brier","donor_brier"):
                    top={"first_choice":"first_correct","child_brier":"belief_brier_sum","donor_brier":"donor_brier_sum"}[k]
                    n=vals(s,which,"births")
                    if k!="first_choice":
                        n=vals(s,which,"births_observable")
                    return np.divide(vals(s,which,top),n,out=np.full(20,np.nan),where=n>0)
                return vals(s,which,k)
            for k in ("abundance","persistence","births","first_choice","child_brier","donor_brier","transfer"):
                secondary.append({"setting":s,"contrast":f"{POP[p]} minus {POP[q]}","metric":k,
                                  **interval(series(k,p)-series(k,q))})
    for filename,data in (("conditions",conditions),("alleles",alleles),("offspring_lifetimes",age_rows),
                          ("time_series",time_rows),("secondary_paired",secondary)):
        table(out/(filename+".csv"),data)
    draw(out,traces,enrich)

def draw(out,traces,enrich):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(11,6),sharex=True,layout="constrained")
    for ax,s in zip(axes.flat,(0,4,8,12,13,14)):
        for p,label in enumerate(POP):
            ax.plot(traces[s,p][:,:3].sum(axis=1),label=label)
        ax.set(title=f"Setting {s}",xlabel="Global period",ylabel="Mean population",ylim=(0,122))
    axes[0,0].legend(fontsize=7)
    fig.savefig(out/"population.png",dpi=150)
    plt.close(fig)
    fig,axes=plt.subplots(2,3,figsize=(11,6),sharex=True,sharey=True,layout="constrained")
    for j,s in enumerate((0,4,8)):
        for i,p in enumerate((2,3)):
            pop=traces[s,p][:,:3]
            rate=np.divide(pop,pop.sum(axis=1,keepdims=True),out=np.full_like(pop,np.nan),where=pop.sum(axis=1,keepdims=True)>0)
            for g in range(3):
                axes[i,j].plot(rate[:,g],label=f"T={g/2:g}")
            axes[i,j].set(title=f"{POP[p]} · {('Stable','Reversal','Unpredictable')[j]}",xlabel="Period",ylabel="Pooled living genotype frequency",ylim=(0,1))
    axes[0,0].legend(fontsize=7)
    fig.savefig(out/"retention_trajectories.png",dpi=150)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4),layout="constrained")
    stat=[interval(enrich[s]) for s in range(15)]
    point=np.array([r["mean"] for r in stat])
    error=point-np.array([r["lo95"] for r in stat])
    ax.errorbar(np.arange(15),100*point,yerr=100*error,fmt="o",capsize=3)
    ax.axhline(0,color="gray",lw=1)
    ax.set(xlabel="Setting index (see conditions.csv)",ylabel="C vs passive occupancy (percentage points)",xticks=range(15))
    fig.savefig(out/"enrichment.png",dpi=150)
    plt.close(fig)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("audit",type=Path)
    p.add_argument("out",type=Path)
    a=p.parse_args()
    analyse(a.audit,a.out)
