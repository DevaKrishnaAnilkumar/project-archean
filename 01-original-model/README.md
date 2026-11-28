# Original model — homeostatic selection (May 2026)

[Back to research overview](../README.md) · [Reviewed historical files](snapshot/) · [Technical provenance](../workspace/docs/PUBLIC_TECHNICAL_PROVENANCE.md)

This is a retrospective guide to historical checkpoint `db28afb06bbaae807a7b9196e8525c3ee9f07964`. The `snapshot/` directory is a curated copy with editorial revisions to documentation and source annotations; executable logic and recorded results are retained. Exact original files are preserved separately. This is not a newly run experiment.

## Research question
Can metabolic cost, death, reproduction with mutation and a finite population capacity produce adaptive behaviour in a simple spatial population?

The original README records three tuning stages: extinction (v1.0), runaway population (v1.1), and introduction of a carrying-capacity bottleneck (v1.2). Only the final early-model state is preserved in this checkpoint; the earlier stages are historical descriptions, not separately tagged experiments.

## Evidence and limitations
- [Historical model overview (editorially revised)](snapshot/README.md)
- [Simulation source](snapshot/archean_simulation.py)
- [Historical age plot](snapshot/evolution_plot.png)

The controller receives exact vent offsets and internal energy. The plot measures mean current age among surviving cells at epoch boundaries, not independently measured chemotaxis or lifetime learning. Earlier interpretations of the age plot are not verified navigation findings; the original text is preserved in the private archive. No separate seed-level evidence for the earlier tuning runs is present here.

## Reproduce
Install Python, NumPy and Matplotlib. Copy `snapshot/` to a fresh scratch directory and run `python archean_simulation.py` there; it writes `evolution_plot.png` and displays the plot. No fixed seed was set in the historical script, so an exact reproduction of the original plot is not guaranteed.

## Next question
Measure navigation directly with frozen controllers and shared held-out starts. Continue to [v2.0.0](../02-v2.0.0-navigation/).
