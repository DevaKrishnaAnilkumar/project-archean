# Project Archean — v2.3.1

## Lifetime learning under spatial and metabolic constraints

Status: Pre-experiment protocol
Date: 2026-11-26

## Research question

Can mutable lifetime memory improve resource-acquisition
decisions and survival in a spatial artificial organism?

## Experimental design

- 40 independent random seeds: 2300–2339.
- 64 matched organisms per seed.
- 32 resource-acquisition encounters per organism.
- Two environmental phases of 16 encounters each.
- Two spatial resource patches at positions (-4, 0)
  and (4, 0), with a central junction at (0, 0).
- Fixed locomotion of one spatial unit per step.
- Each round trip requires eight movement steps.
- Movement costs 0.5 energy units per step.
- Successful resource acquisition provides 8 energy units.
- Reward probabilities: 0.85 and 0.15.
- Initial energy budgets: 160 and 24 units.
- No upper energy cap.
- No reproduction or evolutionary mutation.

## Environmental information

A binary cue is available at the central junction.

The cue determines which patch has the higher reward
probability. The initial cue-to-patch mapping is balanced
across organisms and randomized.

Each phase presents eight occurrences of each cue,
in independently randomized order for each organism.

The stable environment retains its original mapping.

The reversal environment exchanges the rewarding and
less-rewarding patches for each cue after encounter 16.

Organisms receive no explicit reversal notification.

## Memory and learning

Each organism begins with a 2-by-2 memory table,
initialized to 0.5, representing estimated reward
probabilities for each cue-action combination.

The selected memory entry is updated according to:

Q_new = Q_old + 0.3 * (reward - Q_old)

Reward is binary.

Action selection uses epsilon-greedy exploration
with epsilon = 0.2 and random tie-breaking.

Memory is distinct from inherited controller parameters.

## Experimental arms

1. Adaptive memory with genuine cues.
2. Frozen memory with genuine cues.
3. Adaptive memory with independently randomized,
   uninformative binary cues used for both memory
   retrieval and updating.

Each arm is evaluated under stable and reversed
environments and both initial energy budgets.

All matched organisms share potential reward draws,
genuine cue schedules and action-selection random draws.
Randomized control cues use a separate random stream.

## Energy and mortality

Movement costs are deducted before arrival and reward.

If energy reaches zero or below during movement,
the organism dies immediately and receives no further
reward, choices or learning updates.

Reward and memory updating occur only after a living
organism reaches its chosen patch.

Surviving organisms return to the central junction
before another encounter begins.

The high-energy condition prevents mortality even
without reward, allowing direct measurement of learning.

## Primary endpoint

The paired difference in correct patch-choice rate
between adaptive and frozen organisms during
encounters 9–16 in the high-energy condition.

Calculate one paired difference per independent seed.

Report the mean difference and two-sided 95%
paired t confidence interval across the 40 seeds.

Evidence supporting the primary hypothesis requires
the lower confidence bound to exceed zero.

## Secondary endpoints

- Correct choice rate for each encounter.
- Adaptive versus cue-blind performance.
- First four encounters after reversal: 17–20.
- Final eight encounters after reversal: 25–32.
- Reversal recovery relative to the stable control.
- Resource-acquisition rate.
- Final energy, assigning zero to dead organisms.
- Survival probability.
- Completed round trips.
- Encounter and movement step of death.

Mortality-sensitive choice rates use all scheduled
organism encounters as the denominator.

Report survivor-conditional choice rates separately,
along with their denominators.

Secondary outcomes are exploratory and do not
replace the primary endpoint.

## Reproducibility requirements

- Preserve all random seeds and experimental conditions.
- Retain raw per-organism and per-encounter records.
- Preserve potential reward and cue schedules.
- Report seed-level summaries.
- Record Python and NumPy versions.
- Use fresh output directories.
- Test energy conservation and mortality boundaries.
- Test memory updating and frozen-memory invariance.
- Test stable/reversed pairing before reversal.
- Retain negative and inconclusive results.

## Limitations

The learning rule and locomotion are explicitly designed.

The assay tests spatial resource-choice learning,
not emergent navigation, consciousness, general
intelligence or evolution of learning mechanisms.

The resource patches do not deplete, and organisms
do not compete or reproduce.

## Future research

If interpretable, extend the model toward continuous
local-sensing navigation, reproduction, costly memory
and evolution of inheritance mechanisms.
