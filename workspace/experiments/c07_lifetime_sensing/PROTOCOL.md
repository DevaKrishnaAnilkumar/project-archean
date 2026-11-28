# C07 locked protocol

Locked 2026-11-27T09:57:40Z.

# PROJECT ARCHEAN — C07: Lifetime learning under continuous survival pressure

## 1. Research authorisation

C03, C04, C05 and C06 have been accepted within the scope of the research conversation's independent checks.

Proceed with C07 as a controlled lifetime-learning experiment.

The overarching research objective remains survival-driven adaptation. Learning is a candidate survival mechanism, not an independently rewarded achievement.

Do not publish repository changes.

## 2. Starting checkpoint

Repository:
https://github.com/DevaKrishnaAnilkumar/project-archean

Public baseline:
80a67397c3d21921d1f4f5537bd93b676b279a41

Accepted C06 protocol:
0f64a142ea4fb8044c97849d4f04c2a784ccdd36

Accepted C06 implementation:
22dfd6ce97be82a32d1b9275b55bb90f6f57221d

C06 archive SHA-256:
3879f28805f3447ecce36a2e8c7d2fcb7ad3d37d0f03adcdd1b25e7553ed6c43

Verify the complete previous commit chain and preserve all experimental archives.

Create an isolated local branch:

`research/c07-lifetime-sensing-local`

New module:

`workspace/experiments/c07_lifetime_sensing/`

Retain the approved Linux execution environment and previous validation safeguards.

## 3. Research questions

1. Can organisms discover which sensory information sources are useful through their own resource-acquisition experiences?
2. Does learned information improve lifetime survival under continuous energy expenditure?
3. Can organisms revise their knowledge when previously reliable sensory information becomes unreliable?
4. When do simpler strategies outperform learning?
5. Does learning remain advantageous under extreme initial energy scarcity and expensive sensing?

Scientific classification: prospectively specified exploratory experiment.

## 4. Continuous lifetime

Each organism experiences up to 48 consecutive resource-acquisition periods.

Energy carries forward between periods without replenishment or resetting.

At the beginning of every period, deduct one energy unit for metabolic maintenance.

An energy balance of zero or below causes immediate permanent death.

Dead organisms receive no further observations, rewards, actions or learning updates.

There is no energy cap, reproduction or competition in this experiment.

Abstention does not terminate the organism's lifetime. It simply ends the current period, and maintenance expenditure continues in the following period.

## 5. Environment

Retain the previous spatial geometry:

- Junction: (0,0).
- Observation locations A and B: (-1,0) and (1,0).
- Resource locations R0 and R1: (0,-4) and (0,4).

At every period, the hidden resource state H is independently sampled with equal probability.

H identifies the more rewarding resource patch.

Resource reward probabilities remain 0.85 at the better patch and 0.15 at the other.

Successful acquisition provides eight energy units.

Resource travel costs four energy units for a completed round trip.

Apply C06's action-by-action movement, reward and mortality rules.

## 6. Unknown sensory reliability

Introduce a second hidden state M, indicating which observation location is reliable.

The reliable sensor reports H correctly with probability q.

The unreliable sensor reports either observation with equal probability.

Organisms know the two possible sensor models and the value of q, but do not initially know which location is reliable.

Both locations are initially equally plausible.

Use three environmental regimes:

- Stable: the reliable location remains unchanged throughout the lifetime.
- Reversal: the reliable location switches after period 24.
- Unpredictable: the reliable location is sampled independently each period.

Do not notify organisms of environmental changes.

The actual resource state H and sensory reliability state M must remain inaccessible to ordinary agents.

Only the explicitly labelled oracle control receives M.

## 7. Lifetime learning mechanism

Maintain a probability distribution over the two possible values of M.

For learning agents, initialise both hypotheses with probability 0.5.

Between periods, apply a symmetric assumed environmental-switch probability of 0.05 to the learned distribution.

This is a supplied adaptation mechanism, not a learned environmental hazard rate.

Following a sensor observation, calculate the posterior probability of H by marginalising over the agent's current distribution over M.

Choose a resource patch using maximum posterior probability, with common random tie-breaking.

Upon arrival at the resource patch, the organism observes whether it obtained a reward.

Update the probability distribution over M using the observed sensor reading, selected patch and realised reward.

Enumerate both possible hidden resource states in the likelihood calculation.

Never reveal the actual resource state or the unchosen resource outcome.

Do not treat unsuccessful resource acquisition as definitive evidence that the chosen patch was incorrect.

If no observation was collected, the resource outcome does not provide evidence about M under this environment.

Implement the complete Bayesian update independently in the audit.

## 8. Matched comparison policies

Use six policies.

### P1 — No sensing

Collect no observations. Choose resources randomly whenever travel is affordable.

### P2 — Fixed sensing, frozen knowledge

Alternate observation locations according to a predetermined schedule, with balanced starting sides.

Keep the probability distribution over M fixed at 0.5.

### P3 — Adaptive sensing, frozen knowledge

Select the observation location that maximises expected correct resource selection under the current distribution over M.

Since this distribution is frozen at 0.5, resolve equal choices through common random draws.

### P4 — Fixed sensing, lifetime learning

Use the same predetermined sampling schedule as P2.

Update the distribution over M through actual experience.

### P5 — Adaptive sensing, lifetime learning

Update the distribution over M through actual experience.

Select the observation location with the greatest expected correct resource-choice probability.

### P6 — Oracle sensing benchmark

Receive the actual current value of M and choose the reliable sensor.

The oracle must not receive H or any unrealised reward.

It is an explicitly advantaged benchmark, not an ordinary competing organism or a theoretical optimum for lifetime survival.

## 9. Sensing and resource action constraints

Permit at most one observation visit per period.

For the five sensing policies, collect one observation whenever its entire cost is affordable and the remaining energy permits arrival at a resource patch alive.

Otherwise, skip sensing.

All policies attempt resource acquisition when arrival alive is affordable.

If arrival is unaffordable, abstain for that period.

Apply the uncertain reward before return travel.

Retain C06's immediate death rule.

This experiment isolates the learning and sensor-selection mechanisms. The decision to undertake a resource attempt is fixed by the researcher.

Do not describe agents as having evolved risk preferences or optimal survival strategies.

## 10. Parameter exploration

Core factorial design:

- Environmental regimes: stable, reversal, unpredictable.
- Initial energy: 8, 24, 512.
- Reliable sensor accuracy q: 0.85.
- Observation-trip cost: 0.3125.

Nine core environmental settings.

Add six extreme-condition settings:

1. Initial energy 4, stable, q=0.85, cost 0.3125.
2. Initial energy 4, reversal, q=0.85, cost 0.3125.
3. Initial energy 8, stable, q=0.85, cost 2.5.
4. Initial energy 8, reversal, q=0.85, cost 2.5.
5. Initial energy 512, stable, q=0.50, cost 0.3125.
6. Initial energy 512, reversal, q=0.50, cost 0.3125.

The final two settings are uninformative negative controls.

Total: 15 environmental settings and 90 policy-condition combinations.

Do not add parameters after observing evaluation outcomes.

## 11. Independent seeds

Evaluation seeds: 3500–3549 inclusive.

50 independent seed blocks.

32 matched organisms per seed, with balanced initial sensory mappings.

48 scheduled periods per organism.

Total scheduled organism-periods across all conditions: 6,912,000.

Actual encounters may be fewer because mortality is permanent.

Smoke seeds: 3490 and 3491.

Generate matched hidden resource states, environmental mapping schedules, potential observations, potential resource outcomes and relevant tie-breaking draws across comparison policies.

Use independent named RNG streams.

## 12. Primary outcomes

### Survival endpoint

For the stable environment with 24 initial energy units, q=0.85 and quarter-cost sensing:

Compare P5 against P3 and P4.

Measure restricted mean survival duration as the number of periods completed alive, from zero to 48.

Also report end-of-lifetime survival probability.

### Learning endpoint

For the corresponding stable environment with 512 initial energy units:

Compare P5 against P3 on correct resource selection during periods 33–48.

The high-energy condition prevents mortality and permits direct evaluation of learning.

These are exploratory paired seed-level contrasts.

Average within seeds before calculating equally weighted mean differences and two-sided 95% paired t intervals.

Report all three primary contrasts and acknowledge their multiplicity.

## 13. Secondary outcomes

Report:

- Lifetime survival curves.
- Death timing and causes.
- Cumulative resource acquisition.
- Final energy, assigning zero to dead organisms.
- Maintenance, movement and sensing costs.
- Correct resource decisions across all scheduled periods.
- Accuracy conditional on being alive and making a choice.
- Accuracy before and after environmental reversal.
- Learned probability assigned to the currently reliable sensor.
- Frequency of sampling the reliable sensor.
- Adaptation time following reversal.
- Information calibration.
- Abstention and skipped-sensing counts.
- Differences between learned, frozen and oracle policies.

Separate improved information acquisition from improved survival.

Do not claim that a learner is superior merely because its beliefs become more accurate.

## 14. Mandatory controls

Verify:

- Energy continuity between periods.
- Permanent death.
- Maintenance costs during abstention.
- Correct resource reward timing.
- No access to hidden information by ordinary agents.
- Matched random schedules.
- Exact Bayesian updates against explicit enumeration.
- Frozen-memory invariance.
- Equal sensor reliability when q=0.50.
- No learning about M in uninformative environments.
- Oracle access restricted to M.
- Appropriate behaviour at energy boundaries.
- No mortality in the 512-energy conditions.
- Complete raw-data reconstruction.

Retain negative and inconclusive results.

## 15. Execution and resource limits

Commit the full dated protocol and analysis plan before implementation.

Commit validated source code before evaluation.

Use one CPU process, a maximum of approximately 2 GB memory and 15 minutes of numerical runtime.

Benchmark smoke runs and project raw-output size before executing the full experiment.

If limits cannot be met, stop and submit the benchmark for methodological review.

Do not silently reduce seeds, conditions or lifetime duration.

## 16. Required evidence

Return:

`Archean_C07_Lifetime_Sensing_Review.zip`

Include:

- Protocol, analysis plan and complete source.
- Full matched schedules.
- Raw lifetime trajectories and energy records.
- Learned sensory probability histories.
- Per-seed and per-condition results.
- Primary and secondary paired contrasts.
- Survival and learning curves.
- Environmental reversal recovery figures.
- Energy and sensing-cost comparisons.
- Independent computational audit.
- Test logs.
- Execution manifest and environment.
- Protocol and implementation commit hashes.
- Commit-preserving Git bundle.
- SHA-256 checksum.
- All deviations and failures.

## 17. Stop condition

C07 is confirmed for execution after baseline validation.

Do not proceed automatically to reproduction, inheritance evolution or long-duration ecological experiments.

Return all evidence for independent scientific review.

Do not push, merge or publish.

## 18. Scientific boundaries

This experiment investigates learning a restricted hidden environmental state using a supplied Bayesian mechanism.

It does not demonstrate spontaneous discovery of a learning algorithm, evolution of intelligence, consciousness or understanding of an external world.

It remains a controlled foundation for subsequent selection experiments.