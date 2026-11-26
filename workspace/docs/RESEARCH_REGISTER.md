# Project Archean — Living research register

**Edition:** 1.0 · 26 November 2026
**Evidence baseline:** [v2.3.1 publication checkpoint `4fa6bd7`](https://github.com/DevaKrishnaAnilkumar/project-archean/commit/4fa6bd7ecd3a59fe0d31e0d3dfa3f5239e09e740).
**Purpose:** Preserve questions, inspirations, hypotheses, counterarguments, scoped findings and milestones as the research develops. This is an index of evidence and uncertainty, not a claim that the research programme is complete.

[Research agenda and biological motivations](FUTURE_DIRECTIONS.md) · [Original research programme](RESEARCH.md) · [Project overview](../../README.md)

## 1. Status and maintenance rules

Scientific status (independent of implementation progress):

| Status | Meaning |
| --- | --- |
| VERIFIED WITHIN SCOPE | A specified result is supported by documented evidence under stated conditions. Not universal proof. |
| EXPLORATORY EVIDENCE | A descriptive observation, pilot, post-hoc analysis or secondary outcome; confirm on fresh independent seeds where appropriate. |
| HYPOTHESIS | A testable prediction not yet established by the required evidence. |
| OPEN QUESTION | An unresolved question, doubt or competing explanation. |
| PROPOSED EXPERIMENT | A candidate study or engineering research direction, not an approved protocol. |
| INCONCLUSIVE | The available evidence is insufficient or cannot distinguish alternatives. |
| NOT SUPPORTED | A specified hypothesis failed its predefined support criterion; this alone does not establish its negation. |
| CONTRADICTED WITHIN SCOPE | Evidence contradicts a precisely stated prediction in the tested setting. |
| SUPERSEDED | A formulation was replaced; retain its history and successor ID. |

Milestone states: PROPOSED, PROTOCOL RECORDED, IMPLEMENTED, EXECUTED, AUDITED, PUBLISHED ON REVIEW BRANCH, INTEGRATED, or BLOCKED. A completed milestone is not evidence of a successful hypothesis. Evidence maturity (pilot, controlled test, fresh-seed replication, computational audit, external literature) is stated separately in the evidence column. No item is marked verified solely because a paper motivates it, a program runs, or an experiment has been planned.

**Update procedure:** Give each new item an immutable ID; never recycle IDs. Record the date, original wording, type, status, source, scope, and what evidence could change the status. A hypothesis receives its own prospective protocol and criterion before study execution. Link new findings to their parent question and hypothesis IDs; do not silently convert a question into a result. Update the current status and append a dated transition with the old status, new status, reason and commit/evidence link. Keep negative, null and conflicting outcomes. Record post-run inspiration as post-run, not as a prior prediction. If wording changes substantially, create a new ID and link the predecessor. Do not edit historical snapshots or locked protocols. Use Git to preserve revisions; no automatic status promotion or implied consensus.

As the register grows, retain this file as the canonical index and move detailed entries into topic files under `docs/research_register/` with stable IDs and links. Maintain one status per ID, not duplicate copies. Add a dated history entry per checkpoint. Milestone order and version labels are provisional.

## 2. Evidence anchors

These identifiers refer to the recorded research sources, not new experiments.

| Anchor | Source and maturity |
| --- | --- |
| E01 | [Original model](../../01-original-model/README.md): retrospective account, final early-model snapshot; no separately archived v1.0/v1.1 runs. |
| E02 | [Navigation baseline](../../02-v2.0.0-navigation/README.md): three independent evolutionary seeds and exploratory seed-2 extension. |
| E03 | [Local-sensing pilot](../../03-v2.1.0-local-sensing/README.md): six-seed controlled cue interventions. |
| E04 | [Local-sensing replication](../../04-local-sensing-replication/README.md): twenty fresh seeds, matched cue interventions; threshold selected after pilot. |
| E05 | [Inherited experience](../../05-v2.2.0-inherited-experience/README.md): 40 seeds, paired designed memory-transfer and companion assays. |
| E06 | [Cross-platform reproducibility](REPRODUCIBILITY.md): 40 archived inheritance seeds, 1,360 arrays, 2,000 metrics; computational replay, not fresh-seed replication. |
| E07 | [Lifetime learning](../experiments/v2_3_lifetime_learning/RESULTS.md), [protocol](../experiments/v2_3_lifetime_learning/PROTOCOL.md), [analysis plan](../experiments/v2_3_lifetime_learning/ANALYSIS.md), [audit](../experiments/v2_3_lifetime_learning/audit.json): 40 designated seeds, pre-specified primary comparison, exploratory secondary outcomes, independent computational reconstruction of archived schedules. |
| E08 | [Human evolution, related work and future directions](FUTURE_DIRECTIONS.md): external literature starting points and prospective proposals; not experimental verification by Archean. |

## 3. Findings and evidence boundaries

| ID | Finding or claim | Scientific status | Evidence and scope / remaining test |
| --- | --- | --- | --- |
| F-001 | Early metabolic selection and population bottleneck were implemented. | VERIFIED WITHIN SCOPE | E01, source and final early checkpoint. Earlier extinction/runaway tuning narratives are retrospective. |
| F-002 | The original survivor-age plot establishes improved chemotaxis. | INCONCLUSIVE | E01 measures mean current survivor age, not navigation. Direct held-out navigation measures were introduced later. |
| F-003 | Under the exact-offset baseline, evolved controllers can improve held-out navigation. | VERIFIED WITHIN SCOPE | E02: three seeds 32.4→99.2%, 37.7→99.8%, 31.6→37.5%; heterogeneous performance, supplied exact offsets and epoch resets. |
| F-004 | Family dominance causes navigation improvement. | INCONCLUSIVE | E02 reports correlation; pedigree and causal controls required. |
| F-005 | Genuine local cues benefit evolved navigation compared with shuffled cues. | VERIFIED WITHIN SCOPE | E03 pilot 48.9% vs 22.8%; E04 fresh-seed replication 74.5% vs 26.6%, advantage in 20/20 seeds. Noiseless cues, shared axes, fixed lifetime controller. |
| F-006 | The local controller reliably exceeds an 85% reach threshold. | EXPLORATORY EVIDENCE | E04: 10/20 seeds exceeded 85%; threshold chosen after pilot. Does not establish universal reliability. |
| F-007 | Supplied parental memory can improve first choices in stable environments and impair them after reversal. | VERIFIED WITHIN SCOPE | E05: 89.2% stable / 10.8% reversed, blank 49.3% / 50.7%. Learning and copying explicitly designed; separate discrete assay. |
| F-008 | Action-contingent assistance can produce different signalling behaviour than matched open-loop replay. | VERIFIED WITHIN SCOPE | E05: final-eight signalling 87.0% vs 29.1%; supplied mechanisms. Not evidence of designer attribution. |
| F-009 | Retaining a fully revealing own-cost calibration can improve choices in the cost assay. | VERIFIED WITHIN SCOPE | E05: zero prediction error follows from calibration by construction; not evolved self-awareness. |
| F-010 | Archived inheritance outputs can be replayed on the tested ARM64 environment. | VERIFIED WITHIN SCOPE | E06: 1,320 exact arrays, 40 `offer` arrays differ at most 2.22e-16, 2,000 summary metrics matched within tolerance. Not a fresh-seed replication. |
| F-011 | Designed mutable memory improves spatial resource choice relative to frozen memory. | VERIFIED WITHIN SCOPE | E07, pre-specified primary: 87.05% vs 50.62%, +36.43 pp, 95% paired CI +35.61 to +37.25, n=40 seeds. Fixed locomotion, no reproduction. Resolves H-001 in this assay. |
| F-012 | Previously learned choices become maladaptive immediately after reversal and improve later. | EXPLORATORY EVIDENCE | E07: 16.86% early to 74.20% late reversal, +57.35 pp; late stable 89.05%. H-002 needs confirmatory follow-up. |
| F-013 | Informative cues benefit adaptive learning relative to random cues. | EXPLORATORY EVIDENCE | E07: late acquisition +40.42 pp vs cue-blind. H-003 secondary. |
| F-014 | Designed learning improves survival and retained energy at low initial energy. | EXPLORATORY EVIDENCE | E07: stable survival 98.48% vs 71.80% frozen; reversed 93.98% vs 71.05%; final energy includes deaths as zero. H-004 secondary, no extra cognition cost. |
| F-015 | v2.3.1 archived dynamics and summary results are computationally reproducible from saved schedules. | VERIFIED WITHIN SCOPE | E07: 520 archives, 257,048 table values, zero maximum table discrepancy at reported precision; independent scalar audit, not fresh-seed replication or independent RNG replay. |

## 4. Hypotheses and competing predictions

| ID | Hypothesis | Scientific status | Linked evidence / decisive next test |
| --- | --- | --- | --- |
| H-001 | Adaptive memory improves late acquisition relative to frozen memory in the specified v2.3.1 high-energy stable condition. | VERIFIED WITHIN SCOPE | F-011, predeclared primary criterion met. Generalisation remains Q-002. |
| H-002 | Designed learners recover after unannounced contingency reversal. | EXPLORATORY EVIDENCE | F-012; predefine recovery endpoint and test independent seeds. |
| H-003 | Genuine cues improve learning compared with uninformative cues. | EXPLORATORY EVIDENCE | F-013; confirm with fresh schedules and cue reliabilities. |
| H-004 | Learning improves survival or net energy in energy-limited environments. | EXPLORATORY EVIDENCE | F-014; confirm with cognition costs and simpler matched strategies. |
| H-005 | Self-maintenance and reproduction can select for heritable information-processing mechanisms without a task-specific intelligence score. | HYPOTHESIS | F-003/F-005/F-011 motivate but do not establish it; evolving vs non-evolving and drift controls, measure descendants and mechanism ablations. |
| H-006 | Intermediate, learnable environmental variability can favour plasticity more than stable or unpredictable conditions. | HYPOTHESIS | E08 inspiration, F-012 motivation; factorial change frequency, predictability, cue reliability and cost, including counterexamples. No assumed optimum. |
| H-007 | Cheap fixed strategies can outperform costly learning in some stable or unpredictable environments. | HYPOTHESIS | E08; compare evolved fixed, reactive and adaptive strategies with matched information and real costs. |
| H-008 | Selection can favour a heritable capacity to learn, rather than only fixed behaviour or copied learned state. | HYPOTHESIS | F-011 establishes designed learning benefit only; allow zero/nonzero plasticity, compare selection vs drift. |
| H-009 | Selective transmission or forgetting can outperform indiscriminate copying when environmental correlations change. | HYPOTHESIS | F-007 motivation; evolve transfer/retention rules, include costs and blank/parent/unrelated controls. |
| H-010 | Costly parental investment can increase viable descendants under some ecological conditions. | HYPOTHESIS | E08; energy-conserving reproduction and relatedness/beneficiary controls across generations. |
| H-011 | Spatially dispersed, depleting or extractive resources can favour memory and planning over reactive locomotion. | HYPOTHESIS | E08; held-out maps, matched sensors and simple baselines; no direct planning score. |
| H-012 | Learnable hazards and competition can favour predictive risk assessment. | HYPOTHESIS | E08; vary hazard predictability, compare reactive and predictive controls, match exposure. |
| H-013 | Social interdependence can favour cooperation and communication under specified conditions. | HYPOTHESIS | E08; compare solitary, selfish, exploitative and cooperative alternatives; no cooperation bonus. |
| H-014 | Vertical or horizontal social learning can accumulate useful information beyond a lifetime. | HYPOTHESIS | E08 and F-007 motivation; distinguish copying, innovation, genetic changes and cultural accumulation. |
| H-015 | Ecological evolution can discover useful cognitive mechanisms via structural mutation. | HYPOTHESIS | H-005; bounded evolvable architecture, neutral controls, novel task-independent behavioural measurements and ablation. |
| H-016 | Ecologically evolved agents may provide a useful alternative AI development method. | HYPOTHESIS | E08; matched conventional training and neuroevolution baselines, independent held-out tasks and compute/interaction budgets. Not a claim of a new learning category. |
| H-017 | Environmental modification can produce persistent advantages without directly rewarding tool use. | HYPOTHESIS | E08; compare alterable and fixed environments, include resource and action cost controls. |

## 5. Open questions, doubts and alternative explanations

| ID | Question / doubt | Scientific status | What could resolve it? |
| --- | --- | --- | --- |
| Q-001 | Under what environmental and evolutionary conditions does intelligence-like information processing outperform simpler survival strategies? | OPEN QUESTION | H-005–H-015; operational measures, cost–benefit surfaces and descendant outcomes. |
| Q-002 | Does the v2.3.1 mechanism generalise beyond the supplied two-choice association and fixed movement? | OPEN QUESTION | M-006; continuous local sensing, novel geometry, noise, matched reactive/frozen strategies. |
| Q-003 | Is there an optimum of environmental predictability and variability, or several regimes? | OPEN QUESTION | H-006/H-007; separate entropy, autocorrelation, severity, supply and costs. |
| Q-004 | Which components of sensing, memory, updating and computation are worth their metabolic cost? | OPEN QUESTION | M-009; independent cost sweeps, no-learning and zero-cost controls. |
| Q-005 | Can learning itself emerge from evolution rather than being explicitly programmed? | OPEN QUESTION | H-008/H-015; distinguish evolved rates, mechanisms and genuinely novel capacities. |
| Q-006 | What should offspring inherit: genotype, acquired state, the capacity to learn, selective state, or none? | OPEN QUESTION | H-009; compare channels, error, reliability, cost and reversals. Researcher-only archive never agent-accessible. |
| Q-007 | When do individual survival, immediate reproduction and multigenerational lineage persistence align or conflict? | OPEN QUESTION | M-008; viable descendants over specified horizons, relatedness and neutral controls; no assumed conscious lineage goal. |
| Q-008 | Could reproduction and parental energy transfer evolve without researcher-imposed lineage rewards? | OPEN QUESTION | H-010; explicit genealogy, finite energy and ecology. |
| Q-009 | Are effects driven by simulator shortcuts: exact information, epoch resets, top-energy culling, nondepleting resources or scheduling? | OPEN QUESTION | E01–E04 limitations; sensitivity tests, continuous life, energy and capacity invariants, sensor leakage audit. |
| Q-010 | Does complexity continue increasing, or do extinction, equilibrium or cheap dominant strategies prevail? | OPEN QUESTION | M-012; independent worlds, novelty/persistence measures, drift controls; extinction is a result. |
| Q-011 | Can organisms predict internal costs, hazards and consequences of actions beyond simple feedback? | OPEN QUESTION | F-008/F-009 partial motivation; held-out perturbations, forecast errors and feedback baselines. |
| Q-012 | Do behavioural results imply consciousness, subjective experience or awareness of an external designer? | OPEN QUESTION | No current Archean test establishes these; operational prediction and behaviour are not sufficient evidence. No status promotion from navigation or signalling alone. |
| Q-013 | How far can human evolutionary pressures guide artificial ecology design without imposing a human endpoint? | OPEN QUESTION | E08; treat branching human history, variability selection, social/diet/energy hypotheses as external inspiration; test abstract pressures and nonhuman strategies. |
| Q-014 | Can cooperation, communication and cumulative culture develop without explicit behavioural rewards? | OPEN QUESTION | H-013/H-014; validate local interactions, alternative strategies, persistence and causal ablations. |
| Q-015 | How does the system compare with Avida, Polyworld, evolved plasticity, Baldwin effect, POET and open-ended evolution research? | OPEN QUESTION | E08 starting literature; systematic related-work review and comparisons needed before novelty claims. |
| Q-016 | Does ecological evolution outperform or complement supervised/self-supervised/RL/conventional evolution on a fair AI benchmark? | OPEN QUESTION | H-016; no task leakage, matched compute/interaction/training information, transfer and sample efficiency. |
| Q-017 | Can evolved mechanisms transfer to useful tasks such as fictional solar monitoring or resource-limited sensing? | OPEN QUESTION | RESEARCH.md and E08; held-out sites, faults and distribution changes, matched false-alarm rates and compute. |
| Q-018 | Does selection for a lineage require kin structure or ecological feedback rather than explicit long-horizon fitness? | OPEN QUESTION | Q-007/H-010; contrast relatedness, local interactions, individual costs and descendant outcomes. |
| Q-019 | What is the minimal initial information and mutational accessibility sufficient for a viable autonomous world? | OPEN QUESTION | M-011/M-012; founder ablations, viability and neutrality checks, predeclared world bounds. |
| Q-020 | Can an acquired warning persist after hazards disappear, and when should it be forgotten? | OPEN QUESTION | RESEARCH.md; measure false alarms, missed danger and revision time across generations. |

## 6. Research milestones and proposed experiments

All future rows are proposals (not verified findings or approved protocols). Completion status refers to the work product, not the truth of a scientific hypothesis.

| ID | Track | Milestone state | Evidence / gate and related IDs |
| --- | --- | --- | --- |
| M-001 | Original homeostatic model | INTEGRATED | E01; early historical snapshot, F-001/F-002. |
| M-002 | v2.0 navigation baseline | INTEGRATED | E02; F-003/F-004. |
| M-003 | v2.1 local sensing and twenty-seed replication | INTEGRATED | E03/E04; F-005/F-006. |
| M-004 | v2.2 inherited experience and portability audit | INTEGRATED | E05/E06; F-007–F-010. |
| M-005 | v2.3.1 lifetime learning | PUBLISHED ON REVIEW BRANCH | E07, F-011–F-015; protocol committed, implemented, executed, audited and published at `4fa6bd7`; main integration pending at this baseline. |
| M-006 | v2.3.2 continuous spatial learning | PROPOSED | Q-002; matched controls, held-out maps, local/noisy sensing, energy/movement invariants. |
| M-007 | v2.4 heritable plasticity and memory | PROPOSED | H-008/H-009/Q-005/Q-006; mutation and pedigree validation, selection vs drift, fixed/blank controls. |
| M-008 | v2.5 life history and lineage persistence | PROPOSED | H-010/Q-007/Q-008/Q-018; energy-conserving reproduction, genealogy, viable descendants. |
| M-009 | v2.6 costs and environmental variability | PROPOSED | H-006/H-007/H-011/H-012/Q-003/Q-004; factorial environmental and cognitive costs. |
| M-010 | v2.7 evolvable cognitive architecture | PROPOSED | H-015; bounded structural mutations, viability, causal ablations. |
| M-011 | v2.8 ecology, social/cultural mechanisms and perimeter validation | PROPOSED | H-013/H-014/H-017/Q-009/Q-013/Q-014/Q-019; validate mechanisms separately, stable resource accounting, checkpoint/resume, reproducible world configuration. |
| M-012 | v3.0 Primordial autonomous evolutionary ecosystem | PROPOSED | Q-010/Q-019; after environment validation, minimal founders, continuous many-generation evolution, bounded compute, no researcher rescue/culling for desired outcomes, multiple independent worlds and controls, extinction/equilibrium retained. |
| M-013 | Applied AI training comparison | PROPOSED | H-016/Q-015/Q-016/Q-017; literature/novelty review, fair baselines, held-out transfer and task metrics. |
| M-014 | Confirmatory follow-ups for v2.3.1 secondary results | PROPOSED | H-002–H-004; predefine endpoints, fresh independent seeds, preserve original observations. |

## 7. Research governance and open-ended evolution guardrails

- Test environmental laws, sensing, resource depletion/regeneration, energy conservation, reproduction, genealogy, mutation pathways, scheduling and finite-capacity effects before autonomous integration. Keep the environment versioned and fixed during a declared run unless variation itself is part of the protocol.
- Preserve a researcher-only archive of genomes, acquired state, individual parent-child IDs, births/deaths, mutations, world states and RNG state. Agents receive only their defined observations; no archive access, external systems or researcher intervention selecting winners.
- Define operational cognitive and lineage measures before testing; do not equate complexity, longevity or novelty with intelligence. A long run alone does not demonstrate open-ended evolution.
- Compare independent worlds with non-evolving and appropriate drift/restricted-evolution controls. Retain failures, extinction, simple strategies and unexpected innovations. Explicitly report computational and ecological limits.
- Future ideas enter the register immediately as questions, hypotheses or proposals. Any unexpected result is exploratory until a separate test warrants stronger wording. External biological literature is inspiration and evidence about biological systems, not confirmation of Archean mechanisms.

## 8. Append-only status history

| Date | IDs | Transition | Evidence / reason |
| --- | --- | --- | --- |
| 2026-11-26 | F-001–F-010, M-001–M-004 | Initial retrospective registration | E01–E06; scoped evidence and explicit historical limitations. Not retroactive pre-registration. |
| 2026-11-26 | H-001–H-004, F-011–F-015, M-005 | Initial registration of completed study | [Locked pre-execution checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/commit/091731949bb5ad5eac74c0257d05a98c8d1a4786) and [publication checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/commit/4fa6bd7ecd3a59fe0d31e0d3dfa3f5239e09e740). H-001 primary supported; H-002–H-004 exploratory; audit is computational, not fresh-seed replication. |
| 2026-11-26 | H-005–H-017, Q-001–Q-020, M-006–M-014 | Initial prospective registration | E08, original research programme and project discussions. No designated studies executed for these hypotheses; new protocols and review required. |
| 2026-11-26 | Q-021–Q-047 | Initial prospective registration | Foundational handover consolidation; 27 distinct open questions, 9 linked refinements. No change to existing scientific statuses or milestone states. |

For later changes, append a row with date, exact ID, previous and new status, evidence link/commit and reason. If an item is split or superseded, link the new IDs and preserve the original. Use experiment-specific reports for details, not ever-growing duplicated result tables.

## 9. Foundational question additions (26 November 2026)

[Foundational index](foundations/INDEX.md) · [Full candidate dispositions](foundations/RESEARCH_QUESTIONS.md). All 36 candidates have a disposition; existing IDs are not renumbered or reclassified. The following are distinct prospective questions, not findings.

| ID | Question | Scientific status | Detail |
| --- | --- | --- | --- |
| Q-021 | Comparative evolutionary forecasting of visual receptors, anatomy and behaviour; estimate conditional future adaptations rather than a unique next species. | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-001--q-021) |
| Q-022 | Can sensing range, modality, sensitivity and actuator morphology coevolve with controllers? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-002--q-022) |
| Q-023 | When does a selective, incomplete representation outperform a more accurate or comprehensive one? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-003--q-023) |
| Q-024 | Can agents infer hidden environmental variables and distinguish stable causal rules from temporary noise or coincidence? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-004--q-024) |
| Q-025 | Do event-based time, internal oscillators, temporal memory or prediction offer advantages under recurring or irregular conditions? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-005--q-025) |
| Q-026 | Does adaptive weighting of expectations and observations improve control following shifts or under noisy cues? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-007--q-026) |
| Q-027 | Does an explicit persistent internal state enable useful memory without a neural network? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-009--q-027) |
| Q-028 | Can selection favour memory consolidation or offline simulation despite missed resource acquisition opportunities? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-012--q-028) |
| Q-029 | Can inherited records be compressed, selectively retrieved or reinterpreted without sacrificing novel-environment adaptation? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-014--q-029) |
| Q-030 | What transmission fidelity, repair, redundancy and mutation rates support cumulative adaptation under information damage? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-015--q-030) |
| Q-031 | How do multiple competing physiological requirements and harmful resource excess create priorities? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-017--q-031) |
| Q-032 | Can regulation of regulation, metabolic flexibility or dynamic internal processing become selectively beneficial? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-018--q-032) |
| Q-033 | When does persistence, goal revision or counterfactual planning outperform immediate response? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-019--q-033) |
| Q-034 | Can metacognitive confidence estimates and recursive self-evaluation improve adaptation? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-020--q-034) |
| Q-035 | Can agents distinguish self-caused versus externally caused changes and maintain useful self-models? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-021--q-035) |
| Q-036 | Do global access or selective broadcasting improve coordination over local, centralized or distributed alternatives? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-022--q-036) |
| Q-037 | Can initially incidental traces become useful cues and later controllable signals through exaptation? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-023--q-037) |
| Q-038 | Can culturally transmitted symbols acquire functional meaning and cumulative utility? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-024--q-038) |
| Q-039 | Can independently viable components form higher-order evolutionary individuals? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-026--q-039) |
| Q-040 | Can resource recycling, niche construction and emergent ecosystem recovery arise, or does increased capability cause collapse? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-027--q-040) |
| Q-041 | Can population bottlenecks, migration, unequal reproduction and catastrophes change adaptive potential independently of population size? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-029--q-041) |
| Q-042 | Can life-like organisation emerge before a programmer-defined agent exists? (Genesis exploratory branch.) | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-030--q-042) |
| Q-043 | Can an inherited information-bearing structure both store information and perform a functional role? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-031--q-043) |
| Q-044 | How do environment-level reproduction, variation and inheritance affect nested artificial ecosystems? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-032--q-044) |
| Q-045 | Can functional continuity after duplication or restoration be distinguished from structural similarity and subjective identity? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-033--q-045) |
| Q-046 | What functional indicators and ethical review thresholds are appropriate as capabilities increase? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-034--q-046) |
| Q-047 | What architecture is necessary, sufficient, advantageous or redundant for a specified capability? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-035--q-047) |
