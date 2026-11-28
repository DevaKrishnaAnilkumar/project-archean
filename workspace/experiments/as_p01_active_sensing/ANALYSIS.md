# AS-P01 analysis plan

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

