# v2.0.0 — Direct-navigation baseline

[Back to research overview](../README.md) · [Reviewed historical files](snapshot/) · [Technical provenance](../workspace/docs/PUBLIC_TECHNICAL_PROVENANCE.md)

This is a retrospective guide to historical checkpoint `7354b8f600b5740ffe202e70f62bc5478ee7a963`. The `snapshot/` directory is a curated copy with editorial revisions to documentation and source annotations; executable logic and recorded results are retained. Exact original files are preserved separately. This is not a newly run experiment.

## Research question
Does metabolic selection improve measurable vent-reaching performance when exact vent offsets are available?

Three independently seeded populations evolved for five epochs. Frozen controllers were evaluated on 96 shared starts; outside-zone reach rate excludes free successes at step zero.

## Findings
Outside-zone reach increased from 32.4% to 99.2%, 37.7% to 99.8%, and 31.6% to 37.5% across the three seeds. An exploratory extension of seed 2 reached 43.3% after ten epochs. Family dominance was correlated with performance, not established as causal.

## Evidence
- [Historical model overview (editorially revised)](snapshot/README.md)
- [Research programme and protocol](snapshot/RESEARCH.md)
- [Navigation source](snapshot/navigation_baseline.py)
- [Baseline data](snapshot/baseline_results/summary.csv) and [raw archives](snapshot/baseline_results/)
- [Extended seed 2 data](snapshot/seed2_followup/summary.csv)

## Reproduce
From `snapshot/` with Python, NumPy and Matplotlib installed, using fresh output paths:

```sh
python navigation_baseline.py ../new_results
python navigation_baseline.py ../extended_results --epochs 10 --seeds 2
```

## Next question
The controller receives the exact direction of the food by design. Test locally available sensory information in [v2.1.0](../03-v2.1.0-local-sensing/).
