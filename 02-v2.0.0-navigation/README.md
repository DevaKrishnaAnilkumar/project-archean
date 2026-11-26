# v2.0.0 — Direct-navigation baseline

[Back to research overview](../README.md) · [Exact historical checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/7354b8f600b5740ffe202e70f62bc5478ee7a963) · [Tag v2.0.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.0.0)

This is a retrospective guide. The `snapshot/` directory preserves the entire tracked tree at commit `7354b8f600b5740ffe202e70f62bc5478ee7a963` byte-for-byte, including its original README and relative paths. This is a historical checkpoint, not a newly run experiment.

## Research question
Does metabolic selection improve measurable vent-reaching performance when exact vent offsets are available?

Three independently seeded populations evolved for five epochs. Frozen controllers were evaluated on 96 shared starts; outside-zone reach rate excludes free successes at step zero.

## Findings
Outside-zone reach increased from 32.4% to 99.2%, 37.7% to 99.8%, and 31.6% to 37.5% across the three seeds. An exploratory extension of seed 2 reached 43.3% after ten epochs. Family dominance was correlated with performance, not established as causal.

## Evidence
- [Original README (unchanged)](snapshot/README.md)
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
