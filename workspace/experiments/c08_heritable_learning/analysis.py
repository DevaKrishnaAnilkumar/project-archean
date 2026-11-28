"""Locked world-level contrasts, full setting tables and diagnostic plots."""
import argparse
import csv
from pathlib import Path
import numpy as np

REGIMES = ("Stable", "Reversal", "Unpredictable")
GENOTYPES = ("L0 S0", "L0 S½", "L0 S1", "L1 S0", "L1 S½", "L1 S1")
T19 = 2.093024054408263


def write_table(path, rows):
    with path.open("w", newline="") as f:
        output = csv.DictWriter(f, fieldnames=rows[0].keys())
        output.writeheader()
        output.writerows(rows)


def interval(values):
    n = len(values)
    assert n == 20
    mean, sd = np.mean(values), np.std(values, ddof=1)
    half = T19*sd/np.sqrt(n)
    return {"n": n, "mean": mean, "sd": sd, "low95": mean-half, "high95": mean+half}


def ratio(numerator, denominator):
    return numerator/denominator if denominator else float("nan")


def analyse(source, out):
    with (source/"worlds.csv").open() as f:
        data = list(csv.DictReader(f))
    curves = np.load(source/"curves.npy", allow_pickle=False)
    assert len(data) == len(curves) == 800 and curves.shape[1:] == (240,13)
    condition_rows, genotype_rows, time_rows, transition_rows = [], [], [], []
    deltas, mean_traces, extinction = {}, {}, {}
    by_seed = {int(row["seed"]): row for row in data[:20]}
    assert set(by_seed) == set(range(3600,3620))
    for setting in range(40):
        ids = [i for i, row in enumerate(data) if int(row["setting"])==setting]
        ids.sort(key=lambda i: int(data[i]["seed"]))
        block = [data[i] for i in ids]
        trace = curves[ids]
        assert [int(r["seed"]) for r in block] == list(range(3600,3620))
        values = lambda key: np.array([float(row[key]) for row in block])
        c = block[0]
        totals = trace[:,:,:6].sum(axis=2)
        trace_mean = trace.mean(axis=0)
        deltas[setting] = values("delta")
        mean_traces[setting] = trace_mean
        extinction[setting] = values("extinction")
        diversity = 1-np.square(trace[:,:,:6]/np.maximum(1,totals[:,:,None])).sum(axis=2)
        shares = trace[:,:,:6].sum(axis=(0,1))/totals.sum()
        final = trace[:,-1,:6].sum(axis=0)
        base = {"setting":setting, "regime":REGIMES[int(c["regime"])],
                "sensing_cost":int(c["fee_ticks"])/16, "reward":int(c["reward_ticks"])/16,
                "overhead":int(c["overhead_ticks"])/16, "q":c["q"]}
        condition_rows.append({
            **base, "active":values("active").mean(), "passive_mean":values("passive_mean").mean(),
            **{f"delta_{key}":v for key,v in interval(deltas[setting]).items()},
            "extinct_worlds":int((extinction[setting]<240).sum()),
            "mean_extinction_or_censor_time_0_index":extinction[setting].mean(),
            "mean_population":totals.mean(), "mean_final_population":totals[:,-1].mean(),
            "mean_final_lineages":trace[:,-1,6].mean(), "mean_active_lineages":trace[:,:,6].mean(),
            "diversity_nonempty_world_periods":diversity[totals>0].mean(),
            "learning_share":shares[3:].sum(), "sensing_positive_share":shares[[1,2,4,5]].sum(),
            "sensing_allele_mean":shares[[1,4]].sum()*.5+shares[[2,5]].sum(),
            "final_learner_share":ratio(final[3:].sum(),final.sum()),
            "final_sensing_share":ratio(final[[1,2,4,5]].sum(),final.sum()),
            **{f"sum_{key}":int(values(key).sum()) for key in ("births","deaths","mut_l","mut_s","blocked_births")},
        })
        for g, name in enumerate(GENOTYPES):
            per_gt = {key:int(values(f"{key}_g{g}").sum()) for key in (
                "exposure","individuals","births_parent","offspring","censored","attempts",
                "samples","correct","rewards","net_action_ticks","overhead_ticks","sensing_ticks")}
            count = per_gt["exposure"]
            genotype_rows.append({
                **base, "genotype":name, **per_gt, "integrated_frequency":shares[g],
                "final_frequency":ratio(final[g],final.sum()),
                "passive_integrated_frequency":ratio(trace[:,:,7+g].sum(),totals.sum()*8),
                "mean_observed_action_periods":ratio(count,per_gt["individuals"]),
                "births_per_at_risk_period":ratio(per_gt["births_parent"],count),
                "observed_choice_accuracy":ratio(per_gt["correct"],per_gt["attempts"]),
                "mapping_brier_at_start":ratio(values(f"mapping_brier_sum_g{g}").sum(),count),
            })
            for child in range(6):
                transition_rows.append({**base,"parent":name,"child":GENOTYPES[child],
                                        "n":int(values(f"transition_{g}_{child}").sum())})
        for t in range(240):
            time_rows.append({**base,"t":t,"population":totals[:,t].mean(),"lineages":trace_mean[t,6],
                "nonextinct_worlds":int((totals[:,t]>0).sum()),
                **{f"active_g{g}":trace_mean[t,g] for g in range(6)},
                **{f"passive_g{g}":trace_mean[t,7+g]/8 for g in range(6)}})
    primary_values = {
        "Stable cheap enrichment":deltas[0],
        "Stable minus unpredictable cheap":deltas[0]-deltas[24],
        "Stable cheap minus stable expensive":deltas[0]-deltas[8],
    }
    for setting, fee, regime in ((0,.3125,"Stable"),(24,.3125,"Unpredictable"),(8,2.5,"Stable")):
        c = condition_rows[setting]
        assert (c["sensing_cost"],c["regime"],c["reward"],c["overhead"])==(fee,regime,8,0)
    contrasts = [{"contrast":name,**interval(values)} for name,values in primary_values.items()]
    paired_rows = [{"seed":seed,**{name:values[i] for name,values in primary_values.items()}}
                   for i,seed in enumerate(range(3600,3620))]
    out.mkdir(parents=True,exist_ok=True)
    for name, rows in (("conditions",condition_rows),("genotypes",genotype_rows),
                       ("transitions",transition_rows),("time_series",time_rows),
                       ("primary_contrasts",contrasts),("paired_world_contrasts",paired_rows)):
        write_table(out/f"{name}.csv",rows)
    draw(condition_rows, mean_traces, extinction, out)


def draw(conditions, traces, extinction, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size":10,"figure.dpi":150})
    t = np.arange(240)
    ids = [0,12,24,8,36,38]
    labels = ["Stable, cheap", "Reversal, cheap", "Unpredictable, cheap",
              "Stable, expensive", "Null cues (reward 12)", "Free informative sensing"]
    fig, axes = plt.subplots(1,2,figsize=(11,4),layout="constrained")
    for setting,label in zip(ids,labels):
        axes[0].plot(t,traces[setting][:,:6].sum(axis=1),label=label)
        axes[1].plot(t,traces[setting][:,6],label=label)
    axes[0].set(ylabel="Mean living organisms",title="Population abundance",xlabel="Global period")
    axes[1].set(ylabel="Mean founder lineages represented",title="Lineage persistence",xlabel="Global period")
    axes[1].legend(fontsize=8)
    fig.savefig(out/"population_and_lineages.png")
    plt.close(fig)

    fig, axes = plt.subplots(2,3,figsize=(12,7),sharex=True,sharey=True,layout="constrained")
    for axis,setting,label in zip(axes.flat,ids,labels):
        values = traces[setting][:,:6]
        shares = np.divide(values,values.sum(axis=1)[:,None],out=np.full_like(values,np.nan),
                           where=values.sum(axis=1)[:,None]>0)
        for g in range(6):
            axis.plot(t,shares[:,g],label=GENOTYPES[g])
        axis.set(title=label,xlabel="Global period",ylabel="Pooled genotype share")
    axes[0,0].legend(ncol=2,fontsize=8)
    fig.savefig(out/"genotype_frequency.png")
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(7,4),layout="constrained")
    for setting,label in zip(ids,labels):
        axis.step(t,(extinction[setting][:,None]>t).mean(axis=0),where="post",label=label)
    axis.set(xlabel="Global period",ylabel="Fraction of worlds still living",ylim=(-.02,1.02))
    axis.legend(fontsize=8)
    fig.savefig(out/"world_extinction.png")
    plt.close(fig)

    fig, axes = plt.subplots(2,2,figsize=(10,7),layout="constrained")
    vmax = max(abs(r["delta_mean"]) for r in conditions[:36])
    for panel,(prize,overhead) in enumerate(((8,0),(8,.125),(12,0),(12,.125))):
        axis = axes.flat[panel]
        values = np.array([[next(r["delta_mean"] for r in conditions[:36] if
                   (r["reward"],r["overhead"],r["regime"],r["sensing_cost"])==(prize,overhead,regime,fee))
                   for fee in (.3125,1.25,2.5)] for regime in REGIMES])
        im = axis.imshow(values,vmin=-vmax,vmax=vmax,cmap="RdBu")
        axis.set(title=f"Reward {prize} · Learning overhead {overhead}",xticks=range(3),
                 xticklabels=["0.3125","1.25","2.5"],yticks=range(3),yticklabels=REGIMES,
                 xlabel="Sensing-trip cost")
        for y,x in np.ndindex(values.shape):
            axis.text(x,y,f"{100*values[y,x]:+.1f}",ha="center",va="center",
                      color="white" if abs(values[y,x])>vmax*.58 else "black")
    fig.colorbar(im,ax=axes,label="Active minus passive integrated joint abundance")
    fig.savefig(out/"enrichment_heatmaps.png")
    plt.close(fig)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("audit",type=Path)
    p.add_argument("results",type=Path)
    args = p.parse_args()
    analyse(args.audit,args.results)
