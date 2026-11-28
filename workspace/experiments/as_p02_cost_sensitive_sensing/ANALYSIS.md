# AS-P02 analysis plan

## 10. Primary analysis

Primary outcome:

Expected final energy conditional on the actual selected patch and true hidden state, calculated by the researcher after the episode.

Formula:

16 − actual observation expenditure − 4 + 8 × reward probability of selected patch.

This reduces random reward-outcome noise while preserving the consequences of actual policy decisions.

The agent must not receive this researcher-only outcome calculation during sampling.

Primary comparison:

Cost-sensitive exploration minus best fixed sampling.

Calculate the paired seed-level contrast separately in each of the three informative cost regimes.

Report:

- All 20 paired seed contrasts.
- Mean difference.
- Sample standard deviation.
- Two-sided 95% paired t confidence interval.
- Exact theoretical expected difference.

Use 19 degrees of freedom.

The three intervals are exploratory and unadjusted for multiplicity.

Do not interpret intervals crossing zero as evidence of equivalence.

## 11. Secondary outcomes

Report separately:

- Actual realised final energy.
- Resource acquisition frequency.
- Correct resource selection.
- Mean observation count.
- Full distribution of observation counts from zero to three.
- Observation expenditure.
- Resource-travel expenditure.
- Posterior entropy.
- Brier score.
- Log loss.
- Sampling location sequences.
- Frequency of early stopping.
- Gap from the exact optimal adaptive benchmark.

Also report the cost-sensitive policy's comparisons with no sensing, random sampling and compulsory entropy seeking.

Calculate exact theoretical expectations for every simulated policy and regime.

## 14. Acceptance and interpretation

Technical acceptance requires complete data, passing tests, valid controls, matching analytical calculations, reproducible provenance and successful independent raw-data reconstruction.

Scientific conclusions must be reported separately for each cost regime.

A negative or inconclusive result is acceptable.

The exact theoretical optimum must not be presented as evidence of emergent intelligence or learning.

The experiment measures the utility of designed information-acquisition and stopping policies. It does not test evolution, intergenerational information transfer, lifetime learning or biological navigation.

The computational cost of reasoning itself is not modelled. Only movement and sensing costs are included.


Use the two-sided 19-df critical value 2.093024054. Evaluate seed-to-theory discrepancies descriptively using seed SD and standard error. A discrepancy greater than four standard errors on expected energy, accuracy, visit count or realised energy triggers review before acceptance. A zero-standard-error quantity must match within 1e-12. Assess the policy against the exact dynamic-programming bound in expectation. Finite sample means may lie above the population bound. The final decision uses the same tie draw at index three even when sampling stops early. Movement and sensing expenditures are respectively 0.5 and 0.25 times the cost multiplier per step or observation.
