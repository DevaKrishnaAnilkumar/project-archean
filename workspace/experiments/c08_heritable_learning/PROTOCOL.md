# Project Archean — C08: Evolution of heritable learning and sensing

## Research authorisation

The research planning conversation accepts the integrated knowledge base through C07.

Proceed with C08 as a bounded exploratory evolutionary experiment.

Starting checkpoint:

`55b75131f53fa0d9730cf920b7670145e403dc61`

Parent experimental checkpoint:

`220478317ba0191adbbf710add238bc1fb0e82ce`

Knowledge integration review archive SHA-256:

`91a1bdfec9cbfb6bf59bd3ff198c4f8ca6c94167a02ca9de3529ed096a6015d6`

Verify the complete local history, bundle prerequisites and documentation integration before proceeding.

Use the previously approved Linux environment.

New local branch:

`research/c08-evolution-local`

New experiment directory:

`workspace/experiments/c08_heritable_learning/`

## 1. Mandatory prior evidence review

Complete PRIOR_EVIDENCE_REVIEW.md using the integrated knowledge base before locking the protocol.

At minimum address:

F-001, F-003, F-005, F-007, F-014, F-020, F-024, F-025–F-031, H-005–H-009, H-018, Q-004–Q-009, Q-049 and Q-050.

Explain how the experimental design incorporates earlier successes, failures, limitations and competing explanations.

Do not claim that C08 resolves acquired-state inheritance, planning evolution or the risk-avoidance hypothesis.

## 2. Research question

Under what environmental and energetic conditions does survival and differential reproduction favour heritable learning and sensory investment?

Competing outcomes include selection favouring learning, selection favouring reduced cognitive investment, neutral drift, coexistence and complete extinction.

There must be no direct fitness bonus for learning, intelligence, accuracy, information acquisition or complexity.

## 3. Population dynamics

Initial population: 60 organisms.

Maximum simultaneous population: 120.

Duration: 240 global periods.

Initial founder energy: 24 units.

Each organism has a unique individual ID, birth period, parent ID, founder-lineage ID, inherited genotype, internal belief and current energy.

Carry energy and acquired beliefs continuously across periods.

Do not reset surviving organisms between periods.

Apply permanent death at zero or negative energy. Do not replace dead organisms except through ordinary reproduction.

Do not rescue extinct populations.

The population cap blocks additional births when full. It must never remove living organisms according to energy rankings.

## 4. Heritable traits

Introduce two independently inherited loci.

Locus L — lifetime learning:

- 0: Frozen sensory-mapping belief.
- 1: C07 Bayesian sensory-mapping learning.

Locus S — sensing propensity:

- 0: Never voluntarily sense.
- 0.5: Sense with probability 0.5 per eligible period.
- 1: Always sense when eligible.

Initialise ten founders of each of the six genotype combinations.

Randomise founder ordering independently of genotype.

All agents begin with a blank sensory-mapping belief of 0.5.

Offspring inherit genotype, but not acquired sensory beliefs.

This isolates the heritable capacity to learn from acquired-state inheritance.

At each birth, independently mutate each locus with probability 0.02.

When a mutation occurs, select uniformly among the other permitted alleles.

Record every mutation and parent–offspring genotype transition.

## 5. Environment

Use C07's abstract resource geometry and sensory-mapping mechanism.

Each individual encounters an independently sampled binary resource state per period.

The hidden sensory mapping M is shared across a world at a given global period.

Environmental regimes:

- Stable: M remains unchanged.
- Periodic reversal: M switches every 24 periods.
- Unpredictable: M is independently sampled each period.

The reliable sensor reports the hidden resource state correctly with probability q.

The unreliable sensor reports either state with equal probability.

Ordinary organisms do not receive H, M or unrealised outcomes.

Use q=0.85 in the informative settings.

The good resource patch yields a reward with probability 0.85; the other yields it with probability 0.15.

Use resource rewards of either 8 or 12 units.

These reward levels vary energetic resource availability, not physical resource density or depletion.

Resource opportunities are not depleted by other organisms in this initial evolutionary assay.

## 6. Maintenance and behaviour

At the beginning of every period:

- Deduct one unit of baseline maintenance.
- Deduct the specified learning-capacity overhead from organisms with L=1.
- Apply immediate death if energy reaches zero or below.

The learning overhead is a modelled cost of maintaining a learning capability, not measured computational energy consumption.

Apply C07's belief-transition and observation-feedback equations.

Use the original assumed switching hazard of 0.05 for learning organisms.

Frozen organisms retain belief 0.5.

Organisms use inherited sensing propensity to determine whether to attempt one observation.

Sensing is permitted only if its full trip cost is affordable and leaves sufficient energy to reach the resource patch alive.

When sensing, select the observation location with the greatest expected resource-choice accuracy under the current belief. Resolve ties randomly.

Choose resources through the C07 posterior-based decision rule, or randomly when no observation is collected.

Attempt resource acquisition whenever arrival alive is affordable.

Retain C06/C07 action-by-action movement, reward timing and mortality rules.

Resource round-trip cost remains four energy units.

Abstention ends only the current period. Maintenance continues during later periods.

No organism chooses a risk-taking or waiting strategy through a newly evolved risk policy in C08.

## 7. Reproduction

After all surviving organisms complete their period:

Organisms with at least 32 energy units are eligible to reproduce.

Each eligible organism may produce at most one offspring per period.

A successful birth transfers 12 energy units to the child and deducts one additional reproductive cost unit from the parent.

The parent's reserve therefore decreases by 13 units.

Births require an available population slot.

Process eligible parents in independently randomised order.

Do not prioritise energy, age, genotype or previous reproductive success.

Newborns begin acting in the following period.

A blocked birth incurs no reproductive expenditure.

Log energy accounting and all birth/death events.

No spontaneous creation of offspring, undocumented energy transfer or reproductive subsidy is allowed.

## 8. Passive evolutionary control

For each active evolutionary world, construct a matched demographic replay.

Preserve the chronological number and timing of its births and deaths.

In the passive replay:

- Start with the same balanced genotype frequencies.
- Randomly select a living parent for each recorded birth.
- Randomly select a living individual for each recorded death.
- Apply the identical inheritance and mutation rules.
- Preserve the population count trajectory.

Run eight independent passive replays per active world.

The passive populations do not perform energetic foraging. Their demographic events are inherited from the corresponding active world.

This is a conditional neutral demographic benchmark inspired by Polyworld's passive-evolution methodology, not a second independently surviving ecological population.

Use passive replays to assess trait-frequency changes relative to random inheritance and turnover.

Do not use passive replays to claim that a cognitive mechanism causally improves population survival.

## 9. Parameter exploration

Core factorial grid:

- Three environmental regimes.
- Sensing-trip costs: 0.3125, 1.25, 2.5.
- Resource rewards: 8, 12.
- Learning-capacity overhead: 0, 0.125.
- Sensor accuracy: 0.85.

Total: 36 settings.

Add four prespecified controls:

- Stable, reward 12, sensing cost 0.3125, q=0.50, with each learning overhead.
- Stable, reward 8, free sensing, q=0.85, with each learning overhead.

Total: 40 settings.

Evaluation world seeds: 3600–3619 inclusive.

Smoke seeds: 3590 and 3591.

Use distinct named RNG streams for environmental schedules, individual resource opportunities, observations, rewards, sensing decisions, mutation and reproduction order.

Use matched global environmental schedules and founder-generation random streams where applicable.

Do not describe diverging descendant populations as individually matched.

The independent statistical unit is the world, not an individual organism, birth or period.

## 10. Primary analysis

Measure whether the joint trait combination of learning capability and nonzero sensing propensity becomes enriched relative to passive evolutionary replay.

For each world, calculate:

Sum over all 240 periods of the number of living organisms with L=1 and S>0, divided by 120 × 240.

Use end-of-period living counts after reproduction.

Calculate the difference between the active-world measure and the mean of its eight passive replay measures.

Extinct periods contribute zero to both measures. Do not drop extinct worlds.

Primary comparisons:

1. Enrichment in stable, low-cost sensing, reward-8, zero-overhead conditions.
2. Stable versus unpredictable environments under the same energetic settings.
3. Low-cost versus expensive sensing in stable reward-8, zero-overhead conditions.

Use matched world-seed contrasts and exploratory 95% t intervals.

Report all primary outcomes regardless of direction.

Also report learning-locus frequencies, sensing-locus frequencies, all six genotype frequencies and population abundance separately.

Enrichment of one genotype does not establish that it universally maximises survival or intelligence.

## 11. Secondary evolutionary outcomes

Report:

- Population survival and extinction timing.
- Total births and deaths.
- Lifetime duration by genotype.
- Reproductive output by genotype, with exposure denominators.
- Founder-lineage persistence.
- Complete genealogies.
- Population size through time.
- Genetic diversity and mutation histories.
- Changes in sensing propensity.
- Changes in learning prevalence.
- Energetic and behavioural outcomes.
- Costs of maintaining unused learning capabilities.
- Accurate beliefs without corresponding behavioural benefit.
- Conditions where simple organisms persist or dominate.
- Differences between active evolution and passive demographic replay.

Distinguish selection, mutation, drift, founder effects and population bottlenecks in interpretation.

## 12. Mandatory validation

Test:

- Exact energy accounting.
- Permanent death.
- Energy-conserving offspring transfer plus reproductive cost.
- Blank acquired beliefs in newborns.
- Valid inherited alleles and mutation transitions.
- Unique individual and parent IDs.
- Pedigree completeness.
- No post-death actions.
- No newborn actions before the next period.
- Unbiased reproduction ordering.
- Capacity blocking without culling.
- Extinction persistence.
- Correct learning and frozen-belief dynamics.
- Uninformative sensory controls.
- Matched passive demographic counts.
- Random parent/death selection in passive replays.
- Independent reconstruction of reported population and genotype statistics.

Check behaviour under zero mutation, disabled reproduction and deterministic reward schedules using separate validation fixtures.

These fixtures are technical tests, not additional evaluation experiments.

## 13. Execution safeguards

Commit the complete prior evidence review, protocol and analysis plan before implementation.

Lock and commit the validated implementation before accessing evaluation-seed outcomes.

Use a single CPU process.

Maintain the existing approximate 2 GB memory and 15-minute numerical execution limits.

Benchmark smoke execution and estimate raw evidence storage.

The evaluation design includes 800 active worlds and 6,400 conditional passive replays.

If the workload cannot fit the limits, return a benchmark and proposed adjustment. Do not silently drop conditions or seeds.

## 14. Required evidence package

Return:

`Archean_C08_Heritable_Learning_Review.zip`

Include:

- PRIOR_EVIDENCE_REVIEW.md.
- Protocol and analysis plan.
- Complete source and Git bundle.
- Raw population, action, energy and reproductive trajectories.
- Complete parent–offspring genealogy and mutation records.
- Passive replay evidence.
- Per-world and condition-level outcomes.
- Primary contrasts and uncertainty intervals.
- Independent audit and regression logs.
- Population and genotype-frequency figures.
- Extinction and lineage-persistence figures.
- Environmental parameter heatmaps.
- CROSS_EXPERIMENT_COMPARISON.md.
- RESEARCH_BRANCH_CANDIDATES.md.
- Knowledge-register update candidates.
- Deviations, limitations, failures and checksums.

Capture all unexpected observations, including minor or negative findings.

## 15. Interpretation boundaries

C08 tests selection on supplied, heritable learning and sensing traits.

It does not demonstrate the spontaneous evolution of a new learning algorithm, neural architecture, acquired-state inheritance, human-like cognition or awareness of external intervention.

The environment contains no shared depleting food stock and no direct ecological interactions beyond birth-capacity constraints.

The experiment establishes a controlled foundation for richer ecology and longer-duration evolutionary studies.

## 16. Stop condition

C08 is confirmed for execution subject to baseline integrity, protocol completeness and technical validation.

Stop after returning its review package.

Do not automatically proceed to C09, publish the repository, revise the CV or modify the research proposal.

Permanent knowledge-register additions require research-planning review.