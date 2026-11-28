# Project Archean — C09: Evolution of acquired-information inheritance

## Authorisation and baseline

C09 is confirmed for execution.

Resume from the accepted C08 closeout:

`dcc6ad6699763a1a6e114d7de8657c87b5adf3bb`

Use the existing local repository or recover it using Archean_C08_Research_Closeout.zip and START_HERE.md.

Closeout archive SHA-256:

`2fc23f7a57d03148cba745ae920aaeb035ff6037fa585e84b26fcb54942d57af`

Create branch:

`research/c09-information-inheritance-local`

Experiment directory:

`workspace/experiments/c09_acquired_inheritance/`

Reuse the validated C08 implementation where appropriate without modifying its historical source or evidence.

## 1. Research objective

Determine whether survival and differential reproduction favour retaining, partially retaining or discarding acquired parental information.

Test whether the usefulness of inherited experience depends on environmental stability, information-transfer costs, energetic constraints and the source of inherited information.

Do not directly reward intelligence, learning, inheritance or accuracy.

## 2. Mandatory prior evidence review

Consult the complete 121-entry research register and 40 cross-experiment relationships.

Specifically address:

- v1 extinction and population constraints.
- F-007: Benefits and harms of inherited experience.
- H-009: Selective transmission and forgetting.
- C05: Conditional value of information.
- C06: Information acquisition and mortality.
- C07: Lifetime learning, energetic limits and behavioural relevance.
- F-032–F-038: C08 evolutionary findings and limitations.
- H-018: Risk avoidance, which remains a separate unresolved hypothesis.

Prepare PRIOR_EVIDENCE_REVIEW.md before locking the protocol.

## 3. Population and environment

Retain C08's validated mechanics:

- 60 founders.
- Maximum population of 120.
- 240 global periods.
- Founder energy: 24.
- Offspring energy: 12.
- Reproduction threshold: 32.
- Baseline maintenance: 1 unit per period.
- Reproduction cost: 1 unit plus offspring energy transfer.
- Resource round-trip cost: 4.
- Reward probabilities: 0.85 and 0.15.
- Reliable sensor accuracy: 0.85 unless specified.
- Assumed mapping-switch hazard: 0.05.
- Permanent death and persistent extinction.
- Randomised reproduction ordering.
- Population cap blocks births but never culls living organisms.

All organisms have the same C07 Bayesian learning mechanism and always sense when eligible.

Hold learning and sensing traits fixed in C09 to isolate information inheritance.

Do not introduce acquired-state inheritance into the historical C08 module.

## 4. Acquired information and inheritance

Each organism maintains its learned probability p concerning the currently reliable sensor.

Introduce an inherited retention allele T:

- T=0: blank memory.
- T=0.5: partial retention.
- T=1: full retention.

At birth:

p_child = 0.5 + T × (p_donor − 0.5)

This is confidence shrinkage towards an uninformative prior, not a literal percentage of memory bits.

Use the donor's final belief after the current period's learning update.

Newborns first act in the following period and undergo the normal C08 belief-transition rule.

Founders always begin with p=0.5.

The retention locus determines offspring receptivity to acquired information, not an independently evolving parental donation mechanism.

## 5. Four experimental populations

A — Fixed blank inheritance.

All organisms have T=0. No retention-locus mutation.

B — Fixed full parental inheritance.

All organisms have T=1. No retention-locus mutation.

C — Evolvable parental inheritance.

Start with 20 founders per retention allele. At birth, independently mutate T with probability 0.02, choosing uniformly between the other two alleles.

The donor is the actual parent.

D — Evolvable other-organism inheritance.

Same founder composition, mutation and transmission costs as C.

Choose the donor uniformly from other surviving adults in a frozen post-action, pre-reproduction population snapshot.

Exclude the actual parent and newborns. If no alternative donor exists, transmit a blank belief and record the fallback.

Do not describe these donors as necessarily genetically unrelated.

This control distinguishes parental transmission from receiving population-level experience.

## 6. Transmission costs

Test two transmission-cost coefficients:

- Free: 0.
- Costly: 1 energy unit.

The additional cost of a birth is coefficient × offspring T.

Deduct this cost from the parent alongside ordinary reproduction costs.

Charge the transmission mechanism even when the donated belief happens to be 0.5.

Retain exact energy accounting.

This represents a modelled cost of information transfer, not measured biological or computational expenditure.

## 7. Parameter grid

Core factorial:

- Environmental regimes: stable, reversal every 24 periods, unpredictable each period.
- Resource rewards: 8, 12.
- Transmission-cost coefficients: 0, 1.
- Sensing cost: 0.3125.
- Reliable sensor accuracy: 0.85.

12 environmental settings.

Add three extreme and negative-control settings:

1. Stable, reward 8, sensing cost 2.5, transmission cost 0, q=0.85.
2. Stable, reward 12, sensing cost 0.3125, transmission cost 0, q=0.50.
3. Stable, reward 12, sensing cost 0.3125, transmission cost 1, q=0.50.

Total: 15 settings.

Evaluation seeds: 3700–3719.

Smoke seeds: 3690 and 3691.

Four populations × 15 settings × 20 seeds = 1,200 active worlds.

Use matched environmental schedules and founder random streams. Do not claim that diverging descendant populations remain individually matched.

## 8. Neutral evolutionary benchmark

For each Population C world, generate eight independent passive demographic replays using the validated C08 methodology.

Replay the exact chronological birth and death event counts, with randomly selected parents and deaths and identical retention-locus mutation rules.

Total: 2,400 passive replays.

These are conditional demographic controls, not independently surviving ecological populations.

They provide a benchmark for retention-trait selection relative to random turnover.

## 9. Primary analysis

Use the independent world as the statistical unit.

Primary outcome:

Time-integrated occupancy of T>0 organisms divided by all possible population-period slots.

Compare Population C against its mean passive replay.

Prespecified contrasts:

1. Stable, reward 8, cheap sensing, free transmission: active-minus-passive enrichment.
2. Stable versus periodic reversal under the same energetic conditions.
3. Stable versus unpredictable under the same energetic conditions.

Report paired world-level differences and exploratory 95% t intervals.

Retain extinct worlds with zero occupancy after extinction.

Also report allele frequencies among realised living organisms separately from population-slot occupancy.

All three comparisons remain exploratory and unadjusted for multiplicity.

## 10. Secondary outcomes

Compare all four active populations on:

- Population persistence and extinction.
- Time-integrated population abundance.
- Retention allele frequencies.
- Births and deaths.
- Founder-lineage persistence.
- Offspring survival duration.
- Reproductive success and births per at-risk period.
- First resource-choice accuracy of offspring.
- Initial inherited belief calibration.
- Accuracy and mortality immediately following environmental reversals.
- Time required to revise outdated inherited beliefs.
- Energy spent on information transfer.
- Parent versus other-organism information quality.
- Conditions favouring partial or blank inheritance.

Retain the original birth cohorts as denominators for early offspring outcomes. Separately label survivor-conditional analyses.

Distinguish selective advantages from drift, mutation, capacity blocking and demographic effects.

## 11. Mandatory validation

Test inherited beliefs at T=0, 0.5 and 1.

Verify newborn timing, donor identity, mutation, reproductive energy accounting, permanent death, capacity constraints and complete pedigrees.

Confirm that ordinary agents cannot access hidden mappings or unobserved outcomes.

In uninformative environments, beliefs must remain at 0.5.

In the free, uninformative control, fixed blank and full inheritance should produce identical behavioural and energetic trajectories under identical random schedules.

Preserve all previous regression tests.

Independently reconstruct population statistics, inheritance events, donor beliefs, transmission costs and primary contrasts from raw evidence.

## 12. Execution and closeout

Codex usage is limited. Prioritise:

1. Prior evidence review.
2. Locked protocol and analysis plan.
3. Validated implementation.
4. Smoke benchmark.
5. Complete evaluation and independent audit.
6. Scientific results and research closeout.

Commit protocol before implementation and implementation before evaluation.

Reuse C08's efficient compiled execution approach if suitable.

Use one CPU process, approximately 2 GB maximum memory and 15 minutes maximum numerical execution.

If blocked, return recoverable partial evidence rather than silently reducing conditions.

Return:

`Archean_C09_Acquired_Inheritance_Review.zip`

Include source, complete raw trajectories, pedigrees, donor records, per-world results, primary and secondary contrasts, figures, audit, environment, Git bundle and checksums.

Mandatory knowledge documents:

- PRIOR_EVIDENCE_REVIEW.md
- CROSS_EXPERIMENT_COMPARISON.md
- RESEARCH_BRANCH_CANDIDATES.md
- Proposed knowledge-register updates

Capture minor findings, contradictions, unexpected outcomes, failures and limitations.

Do not assign permanent research IDs before scientific review.

Stop after C09. Preserve a clean recoverable checkpoint.

Do not execute C10, publish changes or revise application documents.

## Scientific boundaries

C09 tests selection on a supplied information-retention mechanism. It does not establish spontaneous evolution of memory architecture, consciousness, autonomous intelligence or awareness of external intervention.

Acquired beliefs and genetic inheritance must remain explicitly distinct.

All outcomes, including loss of inheritance, neutrality and extinction, are scientifically informative.