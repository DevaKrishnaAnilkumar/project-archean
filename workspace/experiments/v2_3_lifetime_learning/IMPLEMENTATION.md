# v2.3.1 — Pre-execution implementation decisions

Companion to `PROTOCOL.md` (protocol commit `f484a1f`). This document
resolves operational details before any designated research seed is run.
It does not change the hypotheses, sample size, budgets or primary endpoint.

## Environment, organism and pairing

- Patch 0 is at (-4, 0); patch 1 is at (4, 0). All motion is along the x axis;
  the y coordinate is always zero. Position is explicitly advanced by one
  spatial unit per movement step. Locomotion is fixed, not learned.
- The initial correct patch is the genuine cue XOR the organism's binary
  mapping assignment. The mapping assignment is balanced 32/32 per seed.
  Both cues occur eight times in each phase for each organism.
- Five independent generator streams derived from the seed generate the
  balanced mapping, genuine cues, uninformative cues, potential reward draws
  indexed by patch, and three choice draws (tie, exploration gate, random
  action). Cue-blind cues are independent Bernoulli(0.5), not forced balanced.
- Each condition uses the same stored schedules. Stable and reversed worlds
  are identical through encounter 16, including resulting organism states.
  The reversal switches only reward probabilities, not observed genuine cues.
- The policy sees only the selected observed cue, memory and random choice
  draws. True correct-patch labels and potential rewards are environment-side
  data, not policy inputs. No memory is transmitted to other organisms.

## Boundaries and raw record conventions

Each encounter starts at the junction if alive. Every attempted movement step
advances position and charges 0.5 units. Death at zero takes precedence over
reward or return completion, including at the fourth or eighth step. At the
fourth step, a living organism observes the selected patch outcome, receives
8 units on success, and updates its selected estimate if adaptive. A living
organism returns to the junction on step eight. Death on the return trip
retains any reward and update already experienced. Dead states remain fixed;
no subsequent choices, motion, feedback or memory updates occur.

Records include action (-1 means no choice), reward (-1 means no observation,
0 means an observed failure, 1 means an observed success), movement-step
count, death step (0 means no death in that encounter), completed-trip flag,
correct patch, observed cue, potential outcomes for both patches, and state
at the start of the first encounter and end of every scheduled encounter:
energy, alive, x position and all four memory entries. Death time can be
reconstructed from encounter and step; y is identically zero. The original
random schedules are retained separately when executing the full study.

## Pre-execution analysis conventions

- Primary contrast uses the stable world, 160-unit budget, encounters 9–16,
  genuine-cue adaptive minus genuine-cue frozen. Reversed-world observations
  in this interval are identical and are not counted again. Average paired
  differences over the 40 independent seeds with a two-sided Student t
  interval (39 degrees of freedom, t critical 2.02269092). Support requires
  a strictly positive lower bound. No seed or dead organism is dropped.
- Correct choice is assessed at the time of decision, even if the organism
  subsequently dies before reaching the patch. All-scheduled choice rates
  use all scheduled encounters, with missing choices scored zero. Conditional
  rates divide by the number of actual choices; zero denominator is reported
  as missing (NaN), not as zero. Choice counts are retained.
- Acquisition rate means successful rewards per scheduled encounter. Report
  survival as fraction alive after encounter 32, mean final energy including
  zero for deaths, and mean completed trips per initially assigned organism.
  Death encounter and movement step are available in the raw records.
- Reversal windows are encounters 17–20 and 25–32. Compare adaptive late
  minus early reversal, and late reversed versus matched stable performance.
  Compare genuine versus blind late acquisition and both budgets' survival
  and energy across arms. These secondary outcomes are exploratory; report
  negative and inconclusive results, and do not substitute them for the
  primary endpoint. Seed-level contrasts, rather than pooled individuals,
  are the unit of inference.

## Validation and limits

The implementation tests use synthetic schedules and non-study seeds 101–103.
They check deterministic scheduling, balance, policy selection, memory
updates, frozen and blind cue handling, energetic accounting, death boundaries,
pre-reversal pairing and mortality-sensitive denominators. They are software
checks, not results of the 40-seed experiment. Fixed locomotion and designed
learning make this a spatial choice assay; it is not yet continuous local
navigation, competitive population evolution or emergent learning.
