# Locked C06 protocol

Locked 2026-11-27T09:20:05Z.

# PROJECT ARCHEAN — C06: Energy scarcity, mortality and planning

## 1. Research decision

C05 has passed scientific review for its scoped exploratory findings.

Independent reconstruction verified all 928,000 archived simulated episodes and reproduced the reported primary contrasts.

Proceed with C06, the mortality-aware extension previously designated Phase C.

Do not update the CV, research proposal, public repository or permanent research register yet.

## 2. Starting checkpoint

Public repository:
https://github.com/DevaKrishnaAnilkumar/project-archean

Public baseline:
80a67397c3d21921d1f4f5537bd93b676b279a41

C05 protocol:
2a3e2f2d998e95d528221b62af3870d8dc52ae14

C05 implementation:
3c062032202e270756d40ce7498dc9e2e7b56297

C05 review archive:
Archean_AS_P02_Parameter_Exploration_Review.zip

SHA-256:
2a899594f08e9a6a97c6a4da953fe7243b6f0f26200c5c636c1db412333f7f49

Preserve the entire existing local commit chain.

Verify C05's incremental bundle against its required AS-P02 baseline:
12a62b92c1a47374480d81bc64937c4eb7150a87

Verify the original AS-P02 review archive against its recorded SHA-256:
67d164290567bf7ce7ff265f1b7d732a4f0d024300f5c55e2886e47b604e6b06

Return the C03/C04 evidence package as well if it has not already been returned to the research conversation.

If the required source history cannot be restored, stop rather than fabricating previous commits.

Continue in an isolated local branch:

`research/c06-mortality-local`

Create the new module under:

`workspace/experiments/c06_mortality/`

Use the approved Linux environment and previous execution safeguards.

## 3. Research questions

1. When does gathering additional information improve resource acquisition under limited energy reserves?
2. When does information gathering increase mortality or prevent task completion?
3. Does longer-horizon planning outperform myopic decision-making under energetic constraints?
4. How do survival-prioritising and task-completion-prioritising objectives affect behaviour?
5. Under what conditions are simpler fixed strategies sufficient?

Classification: prospectively specified exploratory experiment.

Do not assume a positive outcome.

## 4. Environment

Retain the AS-P02 geometry:

- Junction: (0,0).
- Observation locations: (-1,0) and (1,0).
- Resource locations: (0,-4) and (0,4).
- Balanced hidden binary resource state.
- Prior probability: 0.5.
- Resource reward: 8 units.
- Reward probabilities: 0.85 at the correct patch and 0.15 at the incorrect patch.
- Resource movement cost: 0.5 units per step.
- Maximum three observation visits.

Retain the original observation likelihoods:

A: P(O=1|H=0)=0.90, P(O=1|H=1)=0.20.

B: P(O=1|H=0)=0.20, P(O=1|H=1)=0.90.

Interpolate likelihoods toward 0.55 using the C05 reliability multiplier.

## 5. Energy and mortality rules

Use explicit action-by-action energy accounting.

- Observation outward movement costs 0.5 × sensing cost multiplier.
- Observation event costs 0.25 × multiplier.
- Observation return movement costs 0.5 × multiplier.
- Resource outward and return travel each require four movement steps at 0.5 per step.
- Grant resource reward only after arrival alive.
- A debit that leaves energy at zero or below causes immediate, irreversible death.
- Clamp energy at zero on death.
- Dead organisms cannot observe, move, receive rewards or make further decisions.

A sensing trip is admissible only when its entire expenditure leaves strictly positive energy.

A resource attempt is admissible only when the agent can reach the patch with strictly positive energy.

The resource return does not need to be prepaid. An agent may depend on the uncertain reward to survive the return journey.

Permit abstention at the junction. Abstention ends the episode without resource acquisition.

For this experiment, no waiting or maintenance costs occur after abstention.

This is intentionally a finite episodic task, not a model of indefinite biological survival.

## 6. Outcome definitions

Record separately:

- Survival at the end of the episode.
- Resource attempt.
- Arrival at a resource patch alive.
- Resource reward received.
- Completed resource round trip alive.
- Reward received and returned alive.
- Abstention.
- Death before acquisition.
- Death during return.
- Death location and action stage.
- Final energy, including zero for dead agents.
- Net energy change.
- Observations acquired.
- Actual sensing and movement expenditure.
- Posterior belief and entropy.

Do not count abstention as task completion.

Do not count a completed trip without reward as successful resource acquisition.

Retain all episodes in primary denominators, including deaths and abstentions.

Survivor-conditional metrics are supplementary.

## 7. Two decision objectives

Define the expected outcome vector for any policy:

(completed resource round trip alive, survival, final energy)

All three components are expectations conditional on the agent's current belief and available information.

### Objective A — Task-completion-first

Lexicographically maximise:

1. Probability of completing a resource round trip alive.
2. Probability of survival.
3. Expected final energy.

### Objective B — Survival-first

Lexicographically maximise:

1. Probability of survival.
2. Probability of completing a resource round trip alive.
3. Expected final energy.

Use exact rational arithmetic for theoretical calculations where tractable. Specify deterministic tie handling before simulation.

Abstention may be optimal, especially under the survival-first objective.

Do not combine the two objectives into a single undocumented fitness function.

## 8. Six comparison policies

All policies receive the same observations, Bayesian updating rule, action constraints and objective-specific terminal decision procedure.

The terminal procedure selects the best admissible resource attempt or abstention under the assigned objective. It must never access the true hidden state.

### P1 — No sensing

Immediately make the terminal decision.

### P2 — Best fixed sampling

Enumerate all 15 predetermined observation sequences containing zero to three visits.

Select the sequence maximising the assigned objective in exact expectation before generating evaluation data.

If a planned visit is unaffordable, stop sampling and make the terminal decision.

Resolve equivalent plans by preferring fewer observations, then lexicographic location order.

### P3 — Random sampling

Select the predetermined observation count, from zero to three, maximising the assigned objective under uniform random location selection.

Stop earlier only when another visit is unaffordable.

### P4 — Compulsory entropy seeking

Choose affordable observation locations by expected entropy reduction.

Continue until the observation budget is exhausted or another visit is unaffordable.

This policy does not explicitly assess whether another observation improves task completion or survival.

### P5 — Myopic objective-aware exploration

Compare immediate terminal action against each admissible one-observation action followed by immediate terminal action.

Choose another observation only when the resulting expected objective vector strictly improves over stopping now.

Resolve equal sampling choices through shared random tie-breaking.

Repeat until stopping or budget exhaustion.

This is a mortality-aware adaptation of the earlier myopic cost-sensitive mechanism. It is not identical to the original scalar net-energy policy.

### P6 — Finite-horizon adaptive planning

Use exact dynamic programming to evaluate:

- Abstention.
- Admissible resource attempts, enumerating reward and no-reward outcomes.
- Admissible observation actions, enumerating both possible observations and recursively evaluating the remaining budget.

Maximise the assigned lexicographic objective.

Prefer stopping when stopping and further sampling have exactly equal objective values.

Use the same constraints and information access as the other policies.

Simulate this policy as well as calculating its exact theoretical benchmark.

Do not claim that its planning mechanism evolved.

## 9. Phase A — Exact parameter exploration

Cross:

- Initial energy: 4, 8, 16, 32, 64, 128.
- Sensing cost multiplier: 0, 0.25, 0.5, 1, 2, 4.
- Sensory reliability multiplier: 0, 0.5, 1.
- Maximum observation visits: 3.
- Objectives: task-completion-first and survival-first.
- All six policies.

This produces 108 environmental settings, 216 setting-objective combinations and 1,296 policy-condition evaluations.

Calculate exact expected survival, task completion, resource acquisition, final energy and observation count.

Use memoisation or cached finite-horizon policy tables.

Represent energy exactly in multiples of 1/16 unit where applicable.

Retain the full parameter grid.

## 10. Phase B — Fresh-seed simulation

Use the fixed subset:

- All six initial energy levels.
- Cost multipliers: 0, 0.25, 1, 4.
- Reliability multipliers: 0, 1.
- Both objectives.
- All six policies.

This gives 48 environmental settings, 96 setting-objective combinations and 576 policy conditions.

Evaluation seeds:
3400–3449 inclusive.

Episodes per seed:
128, balanced 64/64 across hidden states.

Total planned condition-assigned episodes:
3,686,400.

Smoke seeds:
3390 and 3391, eight episodes per seed.

Pre-generate matched schedules for hidden states, potential observations, reward outcomes, random actions and ties.

Match schedules across policies, objectives and environmental settings.

Do not generate evaluation-seed outcomes before locking the protocol and implementation.

## 11. Analysis

Primary comparisons under task-completion-first:

- Myopic versus best fixed.
- Finite-horizon adaptive versus best fixed.
- Finite-horizon adaptive versus myopic.

Primary endpoint:
Probability of completing the resource round trip alive.

Report survival, actual reward acquisition and expected final energy separately.

For the survival-first objective, compare the survival and task-completion trade-off explicitly. Do not interpret abstaining agents as demonstrating superior long-term adaptation.

Report equally weighted seed-level contrasts and exploratory 95% paired t intervals with 49 degrees of freedom.

Report exact theoretical differences alongside simulated differences.

All intervals are exploratory and unadjusted for multiplicity.

Report every setting, not only those showing an advantage for planning.

Identify:

- Conditions where exploration becomes too expensive.
- Conditions where fixed behaviour is sufficient.
- Conditions where longer-horizon planning improves outcomes.
- Conditions where information seeking reduces survival.
- Conditions where risk avoidance prevents resource acquisition.
- Conditions where the objectives produce identical behaviour.

## 12. Mandatory validation

Include deterministic tests for:

- Zero balance and irreversible death.
- Initial energy of 2 units: resource arrival cannot occur alive.
- Initial energy of 4 units without sensing: a successful reward permits return, while no reward causes death on the final return step.
- Initial energy greater than 4 units without sensing: resource round trip can complete even without reward.
- Unaffordable observation trips.
- Correct ordering of acquisition reward and return costs.
- Abstention and incomplete tasks.
- No post-death actions.
- Uninformative observations preserving the prior.
- Exact dynamic-programming transitions.
- Optimal policy not being lexicographically inferior to another admissible policy.
- Matched potential-outcome schedules.
- Exact energy accounting.
- Independent reconstruction of raw trajectories and reported metrics.

At sufficiently high energy, check that survival and completion become assured for feasible resource attempts.

Under these conditions, the myopic and finite-horizon energy-aware policies should reduce to their corresponding AS-P02/C05 decision rules, subject to the specified tie conventions.

Record any genuine differences rather than silently changing either model.

## 13. Compute and evidence boundaries

Commit the dated protocol and analysis plan before implementation.

Commit and hash the complete implementation before evaluation.

Use one CPU process, maximum approximately 2 GB memory and 15 minutes of numerical execution.

Benchmark the smoke workload and estimate output size before starting the full run.

Use compact lossless raw representations with enough information to reconstruct every episode. If needed, store shared schedules once rather than duplicating them across all policies.

If the workload exceeds the limits, stop and return the benchmark and proposed reduction for scientific review.

Do not silently drop conditions, seeds or failures.

## 14. Required return package

Create:

`Archean_C06_Mortality_Review.zip`

Include:

- Dated protocol and analysis plan.
- Exact analytical results for every condition.
- All simulation schedules and raw trajectories.
- Per-seed and per-condition outcomes.
- All paired contrasts.
- Independent audit.
- Regression and validation logs.
- Environment and runtime manifest.
- Source hashes and commit-preserving Git bundle.
- Deviations, failures and limitations.
- SHA-256 checksum.

Required figures:

- Survival versus initial energy.
- Task completion versus initial energy.
- Resource acquisition versus initial energy.
- Abstention versus initial energy.
- Myopic versus finite-horizon planning.
- Energy-cost and reliability heatmaps.
- Survival-first versus task-completion-first comparison.
- Optimality gaps across conditions.

## 15. Scientific limitations

Starting energy measures initial reserves, not ecological resource abundance.

The environment contains independent episodes, supplied likelihoods and designed policies.

There is no ongoing metabolic maintenance after abstention, no reproduction, no lifetime learning and no evolutionary selection.

Computational reasoning itself has no assigned energy cost.

Therefore, the experiment cannot demonstrate the evolution of intelligence or long-term survival strategies.

## 16. Stop condition

C06 is confirmed for execution after baseline integrity validation.

Do not proceed automatically to AS-P03, inheritance evolution, v2.4 or Primordial.

Return the complete evidence package for independent scientific review.

Do not push, merge, publish or revise the application documents.