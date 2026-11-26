# v2.3.1 — Locked execution and analysis conventions

Companion to PROTOCOL.md and IMPLEMENTATION.md. Prepared before designated
research execution. No hypothesis, budget, sample size, or primary endpoint
is changed.

## Execution

Run from this directory in the isolated Python environment. Use
`PYTHONDONTWRITEBYTECODE=1 python -m unittest -v` for synthetic checks.
`PYTHONDONTWRITEBYTECODE=1 python run_study.py NEW_EXTERNAL_DIR --smoke`
uses only non-study seeds 101 and 102, four organisms each. It checks the
pipeline, not the hypotheses, and does not calculate a research interval.
The full study is enabled only by `--research` on a clean implementation
commit directly following the protocol, with a matching remote-tracking
research branch. Publish and verify the pre-execution checkpoint first.
Do not run the research command until the pre-execution review is accepted.
No output directories can be reused or written within the repository.

## Outputs

- `manifest.json`: conditions, seeds, source file SHA-256 hashes, environment
  and Git checkpoint (research mode).
- `raw/SEED/schedules.npz`: complete paired random inputs; one further NPZ
  for each of the 12 conditions. No pickled objects.
- `per_seed.csv`: 480 condition summaries in the full study.
- `paired_contrasts.csv`: one row per seed, including the primary contrast.
- `trial_counts.csv`, `trial_aggregate.csv`: scheduled, actual, correct,
  successful reward and survival counts; aggregate choice denominators.
- `death_counts.csv`: death counts by seed, condition, encounter and step.
- `condition_means.csv`: descriptive seed means of scheduled choice rates,
  survival, final energy, reward rate and completed trips.
- `summary.json`: primary paired t interval and exploratory mean contrasts
  in research mode only. `COMPLETE.json` is written last. Incomplete runs
  are retained, not silently analysed or overwritten.

## Statistical definitions

The primary difference is adaptive minus frozen in the stable world at
160 units over encounters 9–16, one contrast per seed. Compute the sample
standard deviation (ddof=1) and two-sided 95% interval using t=2.02269092
and n=40. Only a lower bound strictly above zero supports the primary
hypothesis. Report point and interval in percentage points (multiply by
100). This tests the specified designed learning mechanism, not emergence.

Exploratory paired contrasts: high-energy late minus early reversal
(25–32 minus 17–20), high-energy late reversed minus stable, high-energy
late-acquisition adaptive minus cue-blind (stable), and survival and final
energy adaptive minus each control for both budgets and worlds. Report
these as descriptive paired mean differences; no secondary significance
claims or substitution for the primary endpoint. Per-trial aggregate
conditional choice rates divide total correct decisions by total actual
choices, not by the number scheduled; these pooled counts are descriptive.
NaN indicates an undefined conditional rate. Death counts remain visible.

## Limits

The sample size was proposed without a formal power calculation. The 40
seeds, not 2,560 matched organism histories or 30,720 condition-assigned
trajectories, are the independent replicate units. Smoke results are not
research evidence. Fixed movement, a designed learning rule, independent
nondepleting resources and no reproduction limit interpretation.
