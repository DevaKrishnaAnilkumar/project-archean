# AS-P01 protocol

Locked at 2026-11-27T07:48:12.435992+00:00 under execution authorisation amendment 01.

## 7. C02 — AS-P01 active-sensing pilot

**Classification: CONFIRMED**

**Scientific classification: Exploratory mechanism-validation pilot.**

This is new work. No result may be assumed in advance.

### 7.1 Research question

Does information-seeking movement improve information acquisition and subsequent resource decisions relative to fixed and random sampling under matched movement, sensing and energy budgets?

### 7.2 Implementation location

Create:

`workspace/experiments/as_p01_active_sensing/`

Do not modify the existing simulation engines or historical snapshots.

Reuse v2.3.1's general approach to matched random schedules, seed-level comparisons, energy accounting, separate source and result directories and reproducibility checks.

The new module should contain:

- `PROTOCOL.md`
- `IMPLEMENTATION.md`
- `ANALYSIS.md`
- `model.py`
- `run_pilot.py`
- `test_model.py`
- `test_runner.py`
- `audit_results.py`
- `plot_results.py`

### 7.3 Environment

Use a two-dimensional discrete spatial task.

- Junction: (0, 0).
- Observation location A: (-1, 0).
- Observation location B: (1, 0).
- Resource patch R0: (0, -4).
- Resource patch R1: (0, 4).

Every episode has an independent hidden binary state H:

- H=0: R0 is the more rewarding resource.
- H=1: R1 is the more rewarding resource.

The agent starts with belief P(H=1)=0.5.

Each episode contains exactly three observation visits. Every visit starts and ends at the junction and produces exactly one observation.

No energy reward is available at observation locations.

After completing all three visits, the agent chooses a resource patch and makes an eight-step round trip.

### 7.4 Observation model

Let O be a binary observation.

**Informative environment:**

| Location | P(O=1 given H=0) | P(O=1 given H=1) |
|---|---:|---:|
| A | 0.90 | 0.20 |
| B | 0.20 | 0.90 |

Observations are conditionally independent given the hidden state and sampled location.

**Uninformative control:**

Both observation locations emit O=1 with probability 0.55, independently of the hidden state.

All policies receive the same correct likelihood model for their assigned regime. This explicitly isolates the value of sampling-policy selection, rather than testing whether agents discover the likelihood model.

The agent must never receive the actual hidden state or unsampled observations.

### 7.5 Three sampling policies

1. Fixed sampling: alternate locations A-B-A or B-A-B. Balance the starting side across episodes independently of the agent's observations.
2. Random sampling: select A or B with equal probability at each visit.
3. Information-seeking: select the location with the greatest expected reduction in binary entropy under the current belief.

Use Bayesian updating after every observation for all three policies.

Calculate information gain using the full predictive distribution of the two possible observations.

Use the same numerical tolerance for information-gain ties, specified as 1e-12. Resolve ties using a pre-generated random draw.

After three observations, all policies use the same maximum-posterior resource decision rule, with shared random tie-breaking when the posterior equals 0.5 within tolerance.

Do not allow the information-seeking policy to use resource reward probabilities as its sampling objective. It must select observation locations solely by expected information gain.

### 7.6 Matched energy budget

- Initial energy: 16 units.
- Movement cost: 0.5 per step.
- Observation cost: 0.25 per visit.
- Three observation round trips: six movement steps.
- Resource round trip: eight movement steps.
- Total movement: 14 steps.
- Total expenditure: 7.75 energy units.
- Successful resource acquisition: +8 energy units.
- Reward probability at the better patch: 0.85.
- Reward probability at the worse patch: 0.15.

Deduct movement and sensing costs as actions occur. Deduct the outward movement cost before granting resource reward.

Final energy must be 8.25 without resource acquisition and 16.25 with resource acquisition.

No mortality should occur under these deliberately matched conditions.

This pilot does not investigate survival under severe energy limitation.

### 7.7 Seeds and conditions

Full pilot:

- Seeds: 3100–3119 inclusive.
- 20 independent seed blocks.
- 128 matched episodes per seed.
- Exactly 64 episodes for each hidden state, randomly ordered.
- Three policies crossed with two observation regimes.
- Six conditions per seed.
- Total: 15,360 condition-assigned episodes.

Use independent NumPy SeedSequence child streams for hidden states, potential observations, random policy decisions, tie-breaking and potential resource outcomes.

Pre-generate potential observation draws for each episode, visit and location.

Match hidden states and potential observations across policies. Use the same underlying uniforms across observation regimes, applying the regime-specific probabilities.

Pre-generate independent potential resource reward draws for both patches. Reveal only the selected patch's outcome.

Do not share unintended RNG state between policy implementations.

### 7.8 Primary endpoint and analysis

Primary endpoint:

Mean reduction in binary entropy between the initial belief and the posterior after the third observation.

Calculate two paired contrasts in the informative environment:

- Information-seeking minus fixed.
- Information-seeking minus random.

First average over the 128 episodes within each condition and seed. Then give each of the 20 seeds equal weight.

Report mean differences, sample standard deviations and two-sided 95% paired t intervals across the 20 seed contrasts.

Use 19 degrees of freedom and t-critical value 2.093024054.

These intervals are exploratory, unadjusted for the two comparisons. Do not describe them as formal confirmatory hypothesis tests.

### 7.9 Secondary outcomes

Report:

- Correct resource-patch selection.
- Brier score for the posterior probability.
- Binary logarithmic loss, with clipping to [1e-12, 1-1e-12] only for metric calculation.
- Realised resource-acquisition frequency.
- Final energy.
- Information gain per unit of sensing and observation-movement energy.
- Observation-location frequencies and sequences.
- Posterior entropy after each observation.
- Per-seed and per-episode outcomes.

Sampling energy is 3.75 units. Report resource-movement costs separately.

Do not use episode-level observations as independent replicates for uncertainty intervals.

### 7.10 Negative control

In the uninformative regime:

- Posterior belief remains 0.5.
- Entropy reduction is zero.
- Both sampling locations have zero expected information gain.
- Shared final decision tie-breaks produce identical resource choices across policies.
- Matched resource draws produce identical rewards and final energy.

Failure of these checks indicates an implementation error, not an unexpected scientific result.

### 7.11 Mandatory validation tests

Before the pilot, test:

1. Bayesian updates against analytically calculated examples.
2. Expected information gain against explicit enumeration of possible observations.
3. Information-gain nonnegativity within numerical tolerance.
4. Equal expected information gain at the symmetric prior.
5. Different preferred observation locations for appropriate asymmetric beliefs.
6. No access to the hidden state or unobserved potential outcomes.
7. Fixed and random policy compliance.
8. Shared hidden states and potential-outcome schedules.
9. Matched observation counts and movement distances.
10. Exact energy accounting.
11. Uninformative-regime invariance.
12. Deterministic seed replay.
13. Fresh output-directory enforcement.
14. Raw-data reconstruction of all reported metrics.
15. Separation of smoke seeds and evaluation seeds.

Use the existing NumPy and standard-library environment. Avoid adding unnecessary dependencies.

### 7.12 Protocol lock and execution order

Before implementation or exposure to evaluation-seed results:

- Write `PROTOCOL.md` and `ANALYSIS.md` with the complete design above.
- Record the actual UTC date and time.
- Commit them locally.
- Record the commit hash and SHA-256 hashes.

Then implement the experiment and tests.

Use smoke seeds 3090 and 3091, with eight episodes per seed, exclusively for implementation testing.

If methodology changes become necessary, preserve the original protocol, record a dated amendment and create another local checkpoint before accessing evaluation-seed outcomes.

After smoke testing passes, commit the final implementation and record its complete source hashes.

Do not backdate any commits or call the local checkpoint a formally registered study.

### 7.13 Required command-line interface

Implement the runner with the following interface:

```bash
cd "$JOB/repo/workspace/experiments/as_p01_active_sensing"

python -m unittest discover -s . -p 'test_*.py' -v \
  2>&1 | tee "$JOB/evidence/as_p01-tests.log"

python run_pilot.py "$JOB/as-p01-smoke" --smoke

python run_pilot.py "$JOB/as-p01-results" --pilot

python audit_results.py "$JOB/as-p01-results" \
  | tee "$JOB/evidence/as-p01-audit.json"

python plot_results.py "$JOB/as-p01-results" \
  "$JOB/evidence/figures"
```

These are the required interfaces for newly implemented scripts, not commands for files already present in Archean.

The pilot runner must refuse execution if the methodological source tree differs from the recorded clean implementation checkpoint.

Do not use evaluation seeds during debugging or smoke testing.

### 7.14 Runtime and resource boundaries

Estimated numerical execution time: seconds to a few minutes after implementation.

Measure actual elapsed time, platform, CPU architecture and memory usage where practical.

Use a single CPU process and avoid GPU dependencies.

If numerical execution exceeds 15 minutes or unexpectedly requires more than approximately 2 GB of memory, stop and investigate. Do not broaden the experiment.

### 7.15 Completion and scientific interpretation

Technical completion requires:

- All tests pass.
- All 20 seeds and six conditions complete.
- Exactly 15,360 condition-assigned episodes.
- All mandatory controls pass.
- No missing or selectively excluded seeds.
- All results reconstruct from raw archives.
- Full protocol and implementation provenance is retained.

Technical completion does not require a positive scientific outcome.

Classify the results as:

- Promising: both exploratory information-gain contrasts have positive lower 95% bounds, and mean resource-choice accuracy is not worse than either comparator.
- Mixed or inconclusive: information gain improves inconsistently, uncertainty intervals overlap zero, or improved information acquisition does not improve downstream decisions.
- Unfavourable: the designed policy does not provide a useful advantage under the specified conditions.
- Invalid: mandatory validation or control checks fail.

Even a promising result does not establish evolved active sensing, lifetime learning, biological insect navigation, evolutionary advantage or general intelligence.

Do not automatically proceed to another experiment.

