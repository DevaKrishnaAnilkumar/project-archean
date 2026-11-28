# AS-P02 locked protocol

2026-11-27T08:38:40.723241+00:00

# Project Archean — AS-P02 research execution handover

Date: 27 November 2026

## 1. Research decision

AS-P01 passed technical validation but produced an inconclusive comparative outcome.

Proceed with AS-P02: Cost-sensitive active exploration.

Do not update the academic CV or research proposal. Do not attempt to produce favourable findings through parameter tuning.

## 2. Starting checkpoint

Public baseline:

Repository: https://github.com/DevaKrishnaAnilkumar/project-archean

Main commit:
80a67397c3d21921d1f4f5537bd93b676b279a41

Accepted local AS-P01 protocol:
ab3c63ffdc15adb003968af62ff567fcc4100592

Accepted local AS-P01 implementation:
40fb5c3bc6375f79a05d9e736029459e1a7a1093

Previous review package:
Archean_Sussex_AS_P01_Review.zip

SHA-256:
e494ecacbac83bdc2b9d04a9ca80505b2de4a70ebaf921fdb4e34c208243e548

Continue from the AS-P01 implementation checkpoint in a separate local branch named `research/as-p02-local`.

If the previous execution workspace is unavailable, restore the AS-P01 Git bundle against the verified public baseline. Verify the bundle, commit ancestry and source hashes. Do not recreate the previous commits manually.

Approved environment:

- Linux x86_64
- Python 3.12.14
- NumPy 2.3.5
- Matplotlib 3.10.8

Maintain the previous isolation and publication restrictions.

## 3. Confirmed execution inventory

C03 — Preserve AS-P01 and reproduce its analytical expectations.

C04 — Implement and execute AS-P02.

Both are authorised. Execute C03 first, then C04 after validation.

All other experiments remain proposed or blocked.

## 4. C03 — AS-P01 analytical follow-up

Preserve the original AS-P01 results unchanged.

Implement a separate exact decision-tree enumeration of the original experiment, using the archived protocol.

Calculate expected entropy reduction and resource-choice accuracy for:

- Balanced alternating fixed sampling.
- Uniform random sampling.
- Greedy information-gain sampling.
- Optimal finite-horizon entropy-reduction policy.

Integrate over hidden states, observations and policy tie-breaking probabilities.

Compare with the previously reported post-hoc analytical expectations:

| Policy | Entropy reduction | Accuracy |
|---|---:|---:|
| Fixed | 0.745251 bits | 94.100% |
| Random | 0.745277 bits | 93.925% |
| Information seeking | 0.752834 bits | 94.100% |
| Optimal entropy reduction | 0.752834 bits | 94.100% |

Treat these figures as claims to verify independently, not values to reproduce by adjusting the calculation.

Report discrepancies transparently. Preserve this work as a post-hoc analytical extension, distinct from the original AS-P01 analysis plan.

## 5. C04 — AS-P02 protocol

### Research question

When does adapting observation acquisition to its energetic value outperform predetermined or compulsory sampling?

### Hypothesis

A cost-sensitive sampling policy may improve expected net energy by avoiding observations whose decision-making benefits do not justify their costs.

Competing explanation: a well-chosen fixed sampling routine may already achieve equivalent or better performance.

### Scientific classification

Prospectively specified exploratory follow-up to AS-P01.

This is not independent confirmation of AS-P01 because the experimental objective and observation-budget rules change.

### Implementation location

`workspace/experiments/as_p02_cost_sensitive_sensing/`

Preserve the existing experimental modules.

### Environment

Retain AS-P01's geometry, hidden state, likelihoods and resource reward probabilities.

- Junction: (0,0).
- Observation sites: (-1,0) and (1,0).
- Resource sites: (0,-4) and (0,4).
- Binary hidden state, balanced across episodes.
- Initial prior probability: 0.5.
- Initial energy: 16 units.
- Maximum observation visits: three.
- Minimum observation visits: zero.
- Every observation requires a two-step round trip.
- Resource travel requires an eight-step round trip costing four energy units.
- Successful acquisition provides eight energy units.
- Reward probabilities: 0.85 at the correct patch and 0.15 at the incorrect patch.

Retain the observation likelihood matrix:

| Site | P(O=1 given H=0) | P(O=1 given H=1) |
|---|---:|---:|
| A | 0.90 | 0.20 |
| B | 0.20 | 0.90 |

Uninformative control: probability 0.55 at either site, independently of the hidden state.

All agents use identical Bayesian updating and the same final maximum-posterior resource decision rule.

The likelihoods are supplied, not learned.

## 6. Sampling cost regimes

Scale AS-P01's observation-trip movement and sensing costs together.

| Regime | Multiplier | Cost per observation visit |
|---|---:|---:|
| Low | 0.25 | 0.3125 |
| Original | 1.00 | 1.2500 |
| High | 2.00 | 2.5000 |

Resource-travel costs remain unchanged.

The low, original and high conditions are fixed before execution. Do not add, remove or tune cost levels after observing outcomes.

All policies receive identical starting energy, maximum observation count, cost schedule and sensory access.

Actual expenditure may differ because the experiment investigates whether choosing to acquire less information conserves energy.

No mortality is expected: even the maximum possible expenditure remains below the starting energy.

## 7. Policy definitions

### Policy 1 — No sensing

Make a resource decision immediately using the initial prior and shared tie-breaking draw.

### Policy 2 — Best fixed sampling

Enumerate all 15 predetermined sequences of zero to three visits to A or B.

Calculate the exact expected net energy of each sequence under the specified likelihood and cost regime.

Select the best sequence separately for each regime before evaluation.

Resolve ties by preferring fewer observations, then lexicographic ordering with A before B.

The sequence must not depend on acquired observations.

### Policy 3 — Random sampling

Choose the predetermined observation count from zero to three that maximises exact expected net energy when each observation location is selected uniformly at random.

Resolve ties using the smaller observation count.

Then choose locations uniformly using the pre-generated random schedule.

The observation count cannot change during an episode.

### Policy 4 — Compulsory entropy seeking

Use AS-P01's greedy information-gain policy with exactly three observation visits.

This tests whether maximising information without considering acquisition cost is energetically useful.

### Policy 5 — Cost-sensitive exploration

Calculate the expected gross resource reward from acting immediately:

V(p) = 8 × [0.15 + 0.70 × max(p, 1-p)]

For each observation site, calculate the expected value after one additional observation by enumerating both possible observation outcomes and their posterior probabilities.

One-step net value of information:

NVOI(site) = Expected V(updated belief) − V(current belief) − observation cost.

If the best NVOI is greater than 1e-12, visit that observation site and update the belief.

Otherwise, stop sampling and choose a resource patch.

Stop after at most three observations.

Resolve site ties using pre-generated random draws.

This is a myopic value-of-information policy, not a globally optimal policy. It may miss situations in which several observations are useful together.

Do not give any policy access to the true hidden state, unrealised observations or future rewards.

## 8. Exact adaptive benchmark

Calculate a finite-horizon dynamic-programming benchmark independently of the simulation.

Define:

F(p,0) = V(p)

For remaining observation budget k:

F(p,k) = maximum of:

- V(p), representing immediate stopping.
- For each site, expected F(updated belief,k-1) minus observation cost.

Calculate exact expected final energy by adding starting energy and subtracting fixed resource-travel cost.

This benchmark provides an upper bound for policies using the supplied likelihoods and available actions.

The benchmark does not itself establish biological feasibility, intelligence or computational efficiency.

Report the gap between the myopic cost-sensitive policy and the optimal adaptive benchmark.

## 9. Seed plan

- Smoke seeds: 3190 and 3191.
- Smoke episodes: eight per seed.
- Evaluation seeds: 3200–3219 inclusive.
- Independent seed blocks: 20.
- Episodes per seed: 128.
- Hidden state balanced 64/64.
- Five policies.
- Three cost regimes.
- Two observation regimes.
- Total conditions per seed: 30.
- Total condition-assigned evaluation episodes: 76,800.

Match hidden states, potential observations, potential rewards and relevant tie-breaking draws across policies and cost regimes.

Use independent named RNG streams.

Generate potential observations for each episode, observation index and site. Reveal only observations actually selected by the policy.

Do not access evaluation-seed outcomes before committing the complete protocol, analysis plan and implementation.

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

## 12. Mandatory controls and tests

Verify:

1. Bayesian updates and expected value calculations against independent enumeration.
2. Fixed and random policies select their sequence or count without evaluation data.
3. All policies obey the maximum three-visit budget.
4. The cost-sensitive policy stops whenever neither site has positive one-step net value.
5. Movement and sensing costs reconcile exactly.
6. No policy accesses hidden states or future outcomes.
7. Paired schedules match across conditions.
8. Resource decisions use the same posterior-based rule.
9. The uninformative control never changes the posterior from 0.5.
10. Cost-sensitive, best fixed and optimised random policies take zero observations in the uninformative control.
11. Compulsory entropy seeking takes three observations and incurs the corresponding costs even in the uninformative control.
12. Shared final resource decisions and rewards match episode by episode in the uninformative regime.
13. Exact optimal adaptive expected utility is not below that of any admissible policy.
14. Deterministic replay and fresh output-directory enforcement.
15. Independent reconstruction of every reported result from raw records.

Compare simulation outcomes with exact theoretical expectations. Investigate unexplained discrepancies rather than adjusting the model to force agreement.

## 13. Execution commands

Create a new isolated output directory outside the repository.

Implement the following interfaces:

```bash
python -m unittest discover -s . -p 'test_*.py' -v

python exact_analysis.py "$JOB/as-p02-theory"

python run_pilot.py "$JOB/as-p02-smoke" --smoke

python run_pilot.py "$JOB/as-p02-results" --pilot

python audit_results.py "$JOB/as-p02-results"

python plot_results.py "$JOB/as-p02-results" "$JOB/figures"
```

These interfaces are requirements for newly implemented scripts.

Lock the protocol and analysis plan before implementation. Record actual UTC timestamps and local commit hashes.

Lock the implementation before executing evaluation seeds.

Use one CPU process. Stop and investigate if numerical execution exceeds 15 minutes or memory exceeds approximately 2 GB.

No additional parameter sweeps are authorised.

## 14. Acceptance and interpretation

Technical acceptance requires complete data, passing tests, valid controls, matching analytical calculations, reproducible provenance and successful independent raw-data reconstruction.

Scientific conclusions must be reported separately for each cost regime.

A negative or inconclusive result is acceptable.

The exact theoretical optimum must not be presented as evidence of emergent intelligence or learning.

The experiment measures the utility of designed information-acquisition and stopping policies. It does not test evolution, intergenerational information transfer, lifetime learning or biological navigation.

The computational cost of reasoning itself is not modelled. Only movement and sensing costs are included.

## 15. Return package

Produce:

`Archean_AS_P02_Review.zip`

Include:

- AS-P01 exact analytical follow-up script and report.
- AS-P02 protocol, analysis plan and source.
- Full raw observation and reward schedules.
- Raw per-episode trajectories.
- Per-seed and per-condition summaries.
- Primary paired contrasts and confidence intervals.
- Exact theoretical expectations and adaptive benchmark.
- Independent audit report.
- All regression and implementation-test logs.
- Runtime and memory measurements.
- Environment and execution manifest.
- Protocol and implementation commit hashes.
- Git bundle preserving new commits and their baseline prerequisites.
- SHA-256 manifest.
- Limitations and deviations report.

Required figures:

- `net_energy_by_cost.png`
- `observations_by_cost.png`
- `accuracy_by_cost.png`
- `information_vs_energy.png`
- `adaptive_policy_optimality_gap.png`

Return the ZIP and its checksum to the originating research conversation.

Stop after C03 and C04.

Do not push, merge, publish, edit existing evidence, modify the research register or revise the application documents.

Further experiments require scientific review.