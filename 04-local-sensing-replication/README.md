# Local-sensing replication — 20 fresh seeds

[Back to research overview](../README.md) · [Reviewed historical files](snapshot/) · [Technical provenance](../workspace/docs/PUBLIC_TECHNICAL_PROVENANCE.md)

This is a retrospective guide to historical checkpoint `769c9052e856cddc86228d58dbd9bbbf978f6484`. The `snapshot/` directory is a curated copy with editorial revisions to documentation and source annotations; executable logic and recorded results are retained. Exact original files are preserved separately. This is not a newly run experiment.

## Research question
Does the genuine-cue advantage from the six-seed pilot persist across fresh evolutionary populations?

Twenty fresh training seeds (6–25) used the same field and paired cue interventions. The seed range, paired outcome and strict 85% threshold were fixed before this follow-up; the threshold was chosen after the pilot.

## Findings
Mean reach was 74.5% with genuine cues and 26.6% with shuffled cues. The median paired advantage was 57.2 percentage points. Genuine cues outperformed shuffling in all 20 seeds; 10 of 20 exceeded 85% reach. The zero-cue mean was 20.0%.

## Evidence
- [Historical model overview (editorially revised)](snapshot/README.md)
- [Replication protocol, figure and results](snapshot/LOCAL_SENSING_REPLICATION.md)
- [Paired rates](snapshot/replication_results/paired_rates.csv) and [raw archives](snapshot/replication_results/)
- [Pilot design](snapshot/LOCAL_SENSING.md)

## Reproduce
From `snapshot/` with Python, NumPy and Matplotlib installed, using a fresh output location:

```sh
for seed in $(seq 6 25); do
  OPENBLAS_NUM_THREADS=1 python local_sensing.py "../new_replication/seed_$seed" --seeds "$seed" || exit 1
done
```

## Limits and next question
The study tests repeatability over training populations, not generalization to noisy sensors or new ecologies. The spatial controllers remain fixed within a lifetime. A separate [v2.2.0 assay](../05-v2.2.0-inherited-experience/) tests effects of transferring acquired state.
