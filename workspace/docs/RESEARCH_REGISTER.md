# Project Archean — Living research register

**Edition:** 1.2 · 28 November 2026 (C11 closeout)
**Evidence baseline:** [v2.3.1 results](../experiments/v2_3_lifetime_learning/RESULTS.md) (original publication checkpoint `4fa6bd7ecd3a59fe0d31e0d3dfa3f5239e09e740`).
**Purpose:** Preserve questions, inspirations, hypotheses, counterarguments, scoped findings and milestones as the research develops. This is an index of evidence and uncertainty, not a claim that the research programme is complete.

[Research agenda and biological motivations](FUTURE_DIRECTIONS.md) · [Original research programme](RESEARCH.md) · [Project overview](../../README.md)

[Experiment knowledge index](EXPERIMENT_KNOWLEDGE_INDEX.md) · [Research branches](RESEARCH_BRANCHES.md) · [Evidence catalogue](research_knowledge/EVIDENCE.md)

## 1. Status and maintenance rules

Scientific status (independent of implementation progress):

| Status | Meaning |
| --- | --- |
| VERIFIED WITHIN SCOPE | A specified result is supported by documented evidence under stated conditions. Not universal proof. |
| EXPLORATORY EVIDENCE | A descriptive observation, pilot, post-hoc analysis or secondary outcome; confirm on fresh independent seeds where appropriate. |
| ANALYTICAL FINDING | A derivation or exact model calculation scoped to its assumptions. |
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
| F-008 | Action-contingent assistance can produce different signalling behaviour than matched open-loop replay. | VERIFIED WITHIN SCOPE | E05: final-eight signalling 87.0% vs 29.1%; supplied mechanisms. Not evidence of identifying an external causal source. |
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
| H-005 | Self-maintenance and reproduction can select for heritable information-processing mechanisms without a task-specific intelligence score. | HYPOTHESIS | F-003/F-005/F-011 motivate but do not establish it; evolving vs non-evolving and drift controls, measure descendants and mechanism ablations. [C11](research_knowledge/C11.md): C11-A fresh-seed confirmation and C11-B controlled results support this hypothesis within the supplied-model scope; no general or spontaneous intelligence claim. |
| H-006 | Intermediate, learnable environmental variability can favour plasticity more than stable or unpredictable conditions. | HYPOTHESIS | E08 inspiration, F-012 motivation; factorial change frequency, predictability, cue reliability and cost, including counterexamples. No assumed optimum. |
| H-007 | Cheap fixed strategies can outperform costly learning in some stable or unpredictable environments. | HYPOTHESIS | E08; compare evolved fixed, reactive and adaptive strategies with matched information and real costs. |
| H-008 | Selection can favour a heritable capacity to learn, rather than only fixed behaviour or copied learned state. | HYPOTHESIS | F-011 establishes designed learning benefit only; allow zero/nonzero plasticity, compare selection vs drift. [C11](research_knowledge/C11.md): C11-B supports selection on a supplied learning capacity at fixed sensing and zero overhead, including without mutation; evolution of learning rules remains untested. |
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
| Q-012 | Do behavioural results imply consciousness, subjective experience or awareness of externally caused perturbations? | OPEN QUESTION | No current Archean test establishes these; operational prediction and behaviour are not sufficient evidence. No status promotion from navigation or signalling alone. |
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
| M-005 | v2.3.1 lifetime learning | INTEGRATED | Results checkpoint `4fa6bd7` is an ancestor of public main merge `80a6739` (PR #2). E07 and F-011–F-015 retain their original evidence and scientific classifications. |
| M-006 | v2.3.2 continuous spatial learning | PROPOSED | Q-002; matched controls, held-out maps, local/noisy sensing, energy/movement invariants. |
| M-007 | v2.4 heritable plasticity and memory | PROPOSED | H-008/H-009/Q-005/Q-006; mutation and pedigree validation, selection vs drift, fixed/blank controls. |
| M-008 | v2.5 life history and lineage persistence | PROPOSED | H-010/Q-007/Q-008/Q-018; energy-conserving reproduction, genealogy, viable descendants. |
| M-009 | v2.6 costs and environmental variability | PROPOSED | H-006/H-007/H-011/H-012/Q-003/Q-004; factorial environmental and cognitive costs. |
| M-010 | v2.7 evolvable cognitive architecture | PROPOSED | H-015; bounded structural mutations, viability, causal ablations. |
| M-011 | v2.8 ecology, social/cultural mechanisms and perimeter validation | PROPOSED | H-013/H-014/H-017/Q-009/Q-013/Q-014/Q-019; validate mechanisms separately, stable resource accounting, checkpoint/resume, reproducible world configuration. |
| M-012 | v3.0 Autonomous evolutionary ecosystem | PROPOSED | Q-010/Q-019; after environment validation, minimal founders, continuous many-generation evolution, bounded compute, no researcher rescue/culling for desired outcomes, multiple independent worlds and controls, extinction/equilibrium retained. |
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
| 2026-11-26 | H-001–H-004, F-011–F-015, M-005 | Initial registration of completed study | [Reviewed protocol](../experiments/v2_3_lifetime_learning/PROTOCOL.md) and [results](../experiments/v2_3_lifetime_learning/RESULTS.md); original lock and publication identifiers in [technical provenance](PUBLIC_TECHNICAL_PROVENANCE.md). H-001 primary supported; H-002–H-004 exploratory; audit is computational, not fresh-seed replication. |
| 2026-11-26 | H-005–H-017, Q-001–Q-020, M-006–M-014 | Initial prospective registration | E08, original research programme and project discussions. No designated studies executed for these hypotheses; new protocols and review required. |
| 2026-11-26 | Q-021–Q-047 | Initial prospective registration | Foundational research consolidation; 27 distinct open questions, 9 linked refinements. No change to existing scientific statuses or milestone states. |

| 2026-11-27 | M-005 | PUBLISHED ON REVIEW BRANCH → INTEGRATED | Ancestry verified from `4fa6bd7` to `80a6739`. The prior milestone row is preserved below. |
| 2026-11-27 | F-016–F-031, H-018–H-019, Q-048–Q-050 | Initial registration | Scoped C02–C07 outcomes, analytical observations and hypotheses. See section 10. |

Prior M-005 record, retained verbatim:

> | M-005 | v2.3.1 lifetime learning | PUBLISHED ON REVIEW BRANCH | E07, F-011–F-015; protocol committed, implemented, executed, audited and published at `4fa6bd7`; main integration pending at this baseline. |

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
| Q-042 | Can life-like organisation emerge before a programmer-defined agent exists? (Exploratory pre-agent organisation.) | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-030--q-042) |
| Q-043 | Can an inherited information-bearing structure both store information and perform a functional role? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-031--q-043) |
| Q-044 | How do environment-level reproduction, variation and inheritance affect nested artificial ecosystems? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-032--q-044) |
| Q-045 | Can functional continuity after duplication or restoration be distinguished from structural similarity and subjective identity? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-033--q-045) |
| Q-046 | What functional indicators and ethical review thresholds are appropriate as capabilities increase? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-034--q-046) |
| Q-047 | What architecture is necessary, sufficient, advantageous or redundant for a specified capability? | OPEN QUESTION | [Details and sources](foundations/RESEARCH_QUESTIONS.md#c-035--q-047) |

## 10. C02–C07 cumulative evidence

The [evidence catalogue](research_knowledge/EVIDENCE.md) identifies the archived runs. The [relationship table](research_knowledge/relationships.csv) links their findings and predecessor records.

| ID | Record | Scientific status | Evidence and related IDs |
|---|---|---|---|
| F-016 | **Matched-cost AS-P01 comparison.** With three compulsory visits and supplied likelihoods, both empirical entropy-gain intervals crossed zero. Resource accuracy was similar. This does not establish equivalence. | INCONCLUSIVE | [Evidence](research_knowledge/evidence/C02/AS_P01_RESULTS.md) · F-005, Q-004 |
| F-017 | **Entropy reduction and patch accuracy diverge.** In the post-hoc AS-P01 tree, greedy and optimal entropy policies gave 0.752834 bits versus 0.745251 for fixed, with the same 94.10% choice accuracy as fixed. The model gives a scoped exact expectation. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C03/AS_P01_EXACT_REPORT.md) · F-016, Q-004 |
| F-018 | **Cost-sensitive sensing under the AS-P02 schedule.** Cost-sensitive sensing averaged +0.1360 final energy versus best fixed at quarter cost, with exact expectation +0.1418625. The original and high cost comparisons tie in exact expectation. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C04/AS_P02_RESULTS.md) · F-017, H-007, Q-004 |
| F-019 | **Compulsory information can reduce retained energy.** At original AS-P02 cost, compulsory sampling produced 94.49% accuracy and 14.74 expected final energy, while no sensing achieved 49.34% and retained 15.96. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C04/AS_P02_RESULTS.md) · F-017, H-007, Q-004 |
| F-020 | **Myopic stopping misses jointly valuable free observations.** In C05 with three free visits and full reliability, cost-sensitive minus best fixed was −0.1568 in exact expected net energy. One-step decisions can stop when observations have value only jointly. The fresh-seed result supported the direction. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C05/C05_RESULTS.md) · F-018, H-011 |
| F-021 | **Cost and reliability bound the advantage of optional sensing.** Across the 120 C05 grid settings the myopic policy beat best fixed in 3, tied in 109 and lost in 8. It matched the adaptive benchmark in 107. Grid counts describe the specified design. The fresh-seed quarter-cost comparison extends F-018. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C05/C05_RESULTS.md) · F-018, F-020, H-007 |
| F-022 | **One-episode survival-first abstention at four units.** All C06 four-unit survival-first policies abstained with survival of one and zero acquisitions. The model does not charge maintenance after this terminal action. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C06/RESULTS.md) · F-021, H-012 |
| F-023 | **Expensive sensing can make return survival reward-dependent.** With eight energy in C06 at the highest cost, immediate travel had 100% survival. Task-first compulsory entropy sampling gave 74.5% with full reliability or 50% with null cues. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C06/RESULTS.md) · F-019, F-021, H-012 |
| F-024 | **Planning and fixed routines can tie on completion with different energy.** Under task-first priorities, adaptive planning tied the best fixed sequence on completion in all 108 exact settings, improved final energy in 14, and improved completion over myopic sensing in six. The 64-unit exact energy results agree with C05. | ANALYTICAL FINDING | [Evidence](research_knowledge/evidence/C06/RESULTS.md) · F-020, F-021, H-011 |
| F-025 | **Adaptive lifetime sensing improves stable performance.** At 24 energy in the stable condition, adaptive learning added 5.7325 and 4.9694 periods alive versus adaptive frozen and fixed learning. At 512 energy it improved late accuracy by 11.3945 points versus adaptive frozen. The three paired intervals are exploratory and unadjusted. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C07/primary_contrasts.csv) · F-011, F-014, H-004 |
| F-026 | **Fixed learners change confidence while matched actions coincide.** All 50 C07 seed archives show zero differences between P2 and P4 in sites, readings, actions, rewards, return steps and energy. Beliefs differ. One reading under equal resource priors and maximum-posterior choice leaves the action invariant to a positive estimate of sensor reliability. | ANALYTICAL FINDING | [Evidence](research_knowledge/C07.md#learning-changed-beliefs-without-changing-fixed-policy-behaviour) · F-017, F-025, Q-026 |
| F-027 | **Costly lifetime sensing can shorten survival despite better choices.** At stable eight energy and 2.5 sensing cost, adaptive learners had 72.17% conditional accuracy against 49.73% for no sensing but averaged 3.555 versus 6.970 periods alive. See F-031 for the null control. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C07/condition_means.csv) · F-019, F-023, H-007 |
| F-028 | **Full-trip energetic break-even bound.** Post-hoc full-trip accounting gives expected net 5.6a − 3.8 − c and 112.5% break-even accuracy at c=2.5. This applies when the full trip is charged or as a counterfactual charge to all attempts. Mortality can select successful rewards among completed trips. The bound gives neither a survival probability nor an unconditional expectation among observed survivors. | ANALYTICAL FINDING | [Evidence](research_knowledge/C07.md#accuracy-above-chance-can-be-insufficient-to-pay-for-sensing) · F-018, F-027, Q-004 |
| F-029 | **Learning shows no clear survival advantage under unpredictable mappings.** At 24 energy the unpredictable P5−P3 estimate was −0.226 periods, with interval [−1.060,+0.609]. Independent redraws remove the predictive value of previous mappings. The interval does not establish equivalence. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C07/secondary_contrasts.csv) · F-012, F-025, H-002, H-006 |
| F-030 | **Belief recovery and resource choice can rank policies differently.** After reversal at high energy, adaptive learners had higher overall choice accuracy but 8.03 versus 7.88 restricted mean periods to the recovery criterion for fixed learners. This descriptive comparison uses distinct outcomes and time windows. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C07/condition_means.csv) · F-012, F-025, H-002 |
| F-031 | **Uninformative sensing spent energy with identical actions.** At q=0.50 and 512 units, all policies made identical paired choices and received identical rewards. Ordinary learned beliefs remained at 0.5. The five sensing groups spent 15 additional units over 48 periods versus no sensing. | VERIFIED WITHIN SCOPE | [Evidence](research_knowledge/evidence/C07/RESULTS.md) · F-019, F-027, H-003 |
| H-018 | **Repeated safe abstention may deplete reserves.** AI-assisted derivation after C06 selected for follow-up. Recurring maintenance can make perennial waiting costly, while informed risk can support persistence. Access to better future opportunities and lethal acquisition risk are competing explanations. C07 imposes affordable attempts. | HYPOTHESIS | [Evidence](research_knowledge/SENSING_AND_MORTALITY.md#staying-safe-for-an-episode-versus-sustaining-reserves) · F-022, F-023, H-012 |
| H-019 | **Episode-level energy savings may improve later opportunities.** With equal completion, reserves saved by selective planning may aid later maintenance, foraging or reproduction. Free planning, finite episodes and environmental persistence can explain different outcomes. | HYPOTHESIS | [Evidence](research_knowledge/DESIGN_GOVERNANCE.md#variability-and-lifetime-investment) · F-024, H-010, Q-007 |
| Q-048 | **When can confidence alter action and survival?.** With sensor scheduling held fixed, would multiple readings, unequal rewards, or confidence-dependent abstention make the belief changes from C07 causally useful? | OPEN QUESTION | [Evidence](research_knowledge/C07.md#learning-changed-beliefs-without-changing-fixed-policy-behaviour) · F-026, Q-004, Q-026 |
| Q-049 | **When is sensing optional and energetically worthwhile?** Can lifetime agents learn to stop buying information before spending reserves needed to return alive? Match learning opportunity and charge sensing and computation explicitly. | OPEN QUESTION | [Evidence](research_knowledge/DESIGN_GOVERNANCE.md#variability-and-lifetime-investment) · F-027, F-028, Q-004 |
| Q-050 | **Does early mortality limit access to useful feedback?.** Separate initial reserve arithmetic and early reward luck from learner inefficiency, while retaining all deaths in the primary denominator. | OPEN QUESTION | [Evidence](research_knowledge/C07.md#early-mortality-and-access-to-feedback) · F-025, F-027, H-004 |

## 11. Extensions to existing evidence

| Existing IDs | Evidence extension |
|---|---|
| F-001, F-002, Q-009 | Preserve historical v1.0 and v1.1 descriptions as retrospective. Document v1.2 population cap, per-cell food gain, reset, tie ordering, division accounting and the survivor-age trace. [Details](research_knowledge/EARLY_MODEL.md) |
| F-003, F-004, F-006, Q-047 | Add conditional first-contact timing, lineage concentration, residency as an alternative and the rationale for isolating cue effects before changing architecture. [Details](research_knowledge/EARLY_MODEL.md) |
| F-007, F-008, H-009, Q-020 | Link persistent energetic effects of inherited memory, replay and help withdrawal. [Details](research_knowledge/LEARNING_AND_INHERITANCE.md) |
| F-010, F-015 | Link C01 computational reconciliation as a separate archive audit. [Details](research_knowledge/EVIDENCE.md) |
| H-002, H-004, H-006, H-007, Q-004 | Link tested conditions and alternative explanations for sensing cost, reversals and survival. [Details](research_knowledge/C07.md) |
| Q-015, Q-016, Q-032 | Link the scoped comparative literature queue and governance refinements. [Details](research_knowledge/DESIGN_GOVERNANCE.md) |

## 12. Required experiment documentation

Before protocol authorisation, complete [PRIOR_EVIDENCE_REVIEW.md](research_knowledge/templates/PRIOR_EVIDENCE_REVIEW.md) with earlier findings, unresolved contradictions, controls and expected relationships. After execution, include [CROSS_EXPERIMENT_COMPARISON.md](research_knowledge/templates/CROSS_EXPERIMENT_COMPARISON.md), [RESEARCH_BRANCH_CANDIDATES.md](research_knowledge/templates/RESEARCH_BRANCH_CANDIDATES.md) and register update candidates. Record minor observations, negative findings, failures, surprises and conversation-derived hypotheses. Use the [cumulative workflow](research_knowledge/FUTURE_EXPERIMENT_WORKFLOW.md). Add newly recovered historical evidence through dated append-only updates.

## 13. C08 reviewed evolutionary evidence

27 November 2026 · Protocol lock `5092881`, implementation lock `a5031b0`. Research planning independently reconstructed all primary measures with zero discrepancy. Scientific effects remain exploratory. [Scoped results, limits and branch ancestry](research_knowledge/C08.md). Earlier register records and scientific statuses are retained.

| ID | Record | Scientific status | Evidence and related IDs |
|---|---|---|---|
| F-032 | **Stable, cheap informative sensing enriches the heritable joint trait.** At reward 8 and zero overhead the active-minus-passive difference was +30.78 percentage points of possible population-slot occupancy. Both prespecified matched contrasts were positive. | VERIFIED WITHIN SCOPE | [Evidence](research_knowledge/evidence/C08/primary_contrasts.csv) · F-025, H-005, H-008 [C11](research_knowledge/C11.md): C11-A confirms all three prespecified directions and >5 pp adjusted lower bounds on 64 fresh blocks: +24.3713, +23.8839, +24.4990 pp. Original C08 estimates remain exploratory; magnitude not reproduced exactly. |
| F-033 | **Sensing and mapping learning diverge under unpredictable mappings.** Cheap reward-8 sensing yielded small positive joint enrichment with near-half learning prevalence and poorer mapping calibration for L1 S1 than L0 S1. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C08/genotypes.csv) · F-029, H-006 [C11](research_knowledge/C11.md): C11-A replicates stable-minus-unpredictable joint occupancy enrichment; calibration and intermediate-variability claims remain exploratory/unresolved. |
| F-034 | **Expensive sensing can favour simpler genotypes or coexist with extinction.** Stable reward-8 expensive worlds all went extinct despite accurate L1 S1 choices. At reward 12, unpredictable expensive worlds with overhead persisted with a majority of no-sensing organism-periods. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C08/conditions.csv) · F-021, F-023, F-027, F-028, H-007 [C11](research_knowledge/C11.md): C11-A replicates cheap-minus-expensive enrichment and 64/64 expensive-world extinctions; reward-12 observations remain exploratory. |
| F-035 | **Null cues and unused learning overhead affect trait composition.** Null cues left beliefs at one half. Unused learning capacity was still charged where specified. Joint depletion was clearer with positive overhead. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C08/genotypes.csv) · F-031, Q-004 [C11](research_knowledge/C11.md): C11-B matched reward-8 null control: frozen/learner parity is a validation invariant, all 256 null worlds extinct. Positive-overhead observations are not replicated. |
| F-036 | **Higher reward preserves founder lineages while reducing measured joint enrichment.** With stable cheap sensing, reward 12 preserved more founder lineages and near-cap abundance than reward 8. The cap was held fixed. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C08/conditions.csv) · F-001, H-005, Q-007, Q-041 [C11](research_knowledge/C11.md): C11-B cap saturation remains a competing explanation; no cap or reward manipulation in C11. |
| F-037 | **Longer observed lifetimes can accompany fewer births per at-risk period.** In the zero-overhead free-sensing setting L1 S1 lived longer on average but produced fewer births per at-risk period than L0 S1. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C08/genotypes.csv) · F-025, Q-007 [C11](research_knowledge/C11.md): C11 supplementary demographic and right-censored longevity summaries do not replicate the original free-sensing comparison or establish causal mediation. |
| F-038 | **Demographic occupancy limits conditional joint-trait enrichment.** The absolute active-minus-passive contrast is bounded by filled-slot fraction. Genotype share among living organisms has a different denominator. | ANALYTICAL FINDING | [Evidence](research_knowledge/C08.md#denominators-and-scope) · F-001, H-005, Q-009 [C11](research_knowledge/C11.md): C11 reports D, U and G separately; B-P2 uses living-frequency enrichment, which still depends on ecological duration. |

## 14. C09 reviewed evidence and proposed reproductive branches

27 November 2026 · Protocol `cc40e90`; implementation `12f1263`. C09 primary demographic reconstruction passed. Effects remain exploratory. [Evidence and scope](research_knowledge/C09.md). Two reproductive branches are registered as proposals, not findings.

| ID | Record | Scientific or milestone status | Evidence and related IDs |
|---|---|---|---|
| F-039 | **Stable free retention enriches nonblank acquired-information receptivity.** At reward 8 and cheap sensing, +7.14 pp [3.25,11.03] slot occupancy versus passive; stable minus reversal +7.77 pp [4.06,11.49]; stable minus unpredictable +6.98 pp [3.13,10.82]. n=20 paired worlds, exploratory unadjusted intervals. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/primary.csv) · F-007, F-032, F-038, H-009 |
| F-040 | **Early offspring accuracy and population abundance can diverge.** Full versus blank under reversal: +7.94 pp first-choice success (original birth cohorts), −7.73 mean organisms. Stable comparison +14.12 pp and +1.77 organisms. Exposure and costs may differ. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/RESULTS.md) · F-025, F-027, F-037 |
| F-041 | **Donor source and environmental persistence change information quality.** Stable parent versus other surviving donor Brier 0.071 vs 0.136; unpredictable 0.372 vs 0.290. Reproductive filtering and survivor sampling confound ancestry; 18 donor fallbacks. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/RESULTS.md) · F-007, H-009, Q-006 |
| F-042 | **Partial retention can moderate mismatch after reversal.** Reversal partial vs full newborn Brier 0.192 vs 0.208; blank 0.250. Under unpredictable mapping blank 0.250 vs partial 0.295/full 0.365. Descriptive, not a universal optimum. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/alleles.csv) · F-007, F-029, H-009, Q-006 |
| F-043 | **Transfer can incur cost without transmitting useful information.** At q=0.50 beliefs stay 0.5 and free blank/full comparable action and energy trajectories match. Costly full transfer spent 7701 units across 20 worlds. This is a model/accounting check; fitness consequences exploratory. | VERIFIED WITHIN SCOPE | [Evidence](research_knowledge/evidence/C09/RESULTS.md) · F-031, F-035, Q-004 |
| F-044 | **Extreme sensing expenditure can overwhelm inherited information.** All 80 extreme cost world-population runs extinct; only five seeds with births in fixed comparisons. Do not infer effect of inheritance from sparse cohorts. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/conditions.csv) · F-001, F-027, F-028, F-034 |
| F-045 | **Apparent inherited-belief revision depends on exposure and censoring.** Free reward-8 reversal C: 1071/1237 contradictory newborn beliefs aligned within initial segment before censoring; observed alignments averaged 4.27 periods. Redraw can cause alignment without learning. | EXPLORATORY EVIDENCE | [Evidence](research_knowledge/evidence/C09/RESULTS.md) · F-030, Q-050 |
| Q-051 | **When do recombination and dual-parent acquired information improve survival?.** Researcher-originated C10; isolate genetic recombination, mutation, pooling, conflicting evidence, mate constraints and energy costs. Neither mode assumed superior. | OPEN QUESTION | [Evidence](research_knowledge/evidence/C09/RESEARCH_BRANCH_CANDIDATES.md) · H-009, H-010, Q-006, Q-008, F-041 |
| Q-052 | **Can reproductive mode itself evolve under survival and demographic pressure?.** AI-assisted extension retained as a prospective research question: fixed single-parent, fixed two-parent, or facultative switching, with costs and demographic controls. Distinct from C10. | OPEN QUESTION | [Evidence](research_knowledge/EVOLVABLE_REPRODUCTION.md) · Q-051, H-005, H-009, H-010, Q-007, Q-008, Q-018, Q-041 |
| M-015 | **C10 controlled recombination and dual-parent information assay.** | AUDITED | [C10 reviewed evidence](research_knowledge/C10.md) · Q-051, F-046–F-053. Computational audit, not scientific replication. |
| M-016 | **Evolution of reproductive strategy including facultative switching.** Separate branch, after controlled C10 comparisons and new authorisation. | PROPOSED | [Evidence](research_knowledge/EVOLVABLE_REPRODUCTION.md) · Q-052, M-015 |

Append-only history, 2026-11-27: F-039–F-045, Q-051–Q-052, M-015–M-016 first registered after C09 review. No earlier row or scientific status changed.

## 15. C10 reviewed recombination evidence

28 November 2026. Protocol 2aadbcf; implementation cc34fb3.
Computational audit passed. Scientific effects remain exploratory;
no independent fresh-seed replication is claimed.
See [C10 evidence and dispositions](research_knowledge/C10.md).

| ID | Record | Scientific status | Evidence and related IDs |
|---|---|---|---|
| F-046 | Recombination generated the absent joint learning-and-sensing genotype without mutation in 20/20 worlds versus 0/20 clone worlds. Joint-slot occupancy difference +11.09 pp [9.54,12.65]; with 2% mutation +9.91 pp [8.04,11.77]. | EXPLORATORY EVIDENCE | [C10](research_knowledge/C10.md) · Q-051, H-015 |
| F-047 | Joint-trait novelty also increased under null cues (+8.43 pp). Genotype novelty alone does not establish adaptive intelligence or selection for learning. | EXPLORATORY EVIDENCE | [C10](research_knowledge/C10.md) · F-032, F-038, H-005 |
| F-048 | Standing variation and mutation may modify recombination effects. Balanced founders +1.05 pp with interval crossing zero; complementary founders +9.91 pp at 2% mutation and +5.98 pp at high mutation. Interaction not prospectively tested. | EXPLORATORY EVIDENCE | [C10](research_knowledge/C10.md) · Q-041, Q-051 |
| F-049 | Pooled and one-parent memory had identical total population trajectories in 40 primary matched pairs, while genotype counts differed in 39. Abundance can conceal behavioural or compositional changes. | VERIFIED WITHIN SCOPE | [C10](research_knowledge/C10.md) · F-026, F-036, F-038, F-040 |
| F-050 | Memory pooling under low reward improved slot occupancy by +4.45 pp [0.45,8.45], with four extinctions in each arm. High-reward stable first-choice difference +1.76 pp without an occupancy advantage. Secondary comparisons require confirmation. | EXPLORATORY EVIDENCE | [C10](research_knowledge/C10.md) · F-007, F-041, F-042, H-009 |
| F-051 | Scarce-founder paired versus single-parent occupancy difference -5.32 pp [-12.48,1.85]. Both founder count and initial energy change; equal total birth cost does not isolate parental cost sharing or mate availability. | INCONCLUSIVE | [C10](research_knowledge/C10.md) · H-010, Q-041, Q-051 |
| F-052 | All 160 highest-sensing-cost C10 worlds became extinct across the eight reproductive policies. This does not establish a universal survival threshold. | EXPLORATORY EVIDENCE | [C10](research_knowledge/C10.md) · F-027, F-028, F-034, F-044 |
| F-053 | Complementary clone-only zero-mutation founders lacked the joint functional capacity. Beliefs stayed blank and memory interventions coincided. Component presence does not imply useful integrated processing. | VERIFIED WITHIN SCOPE | [C10](research_knowledge/C10.md) · F-026, Q-047 |

## 16. Prospective plastic evolution and environmental challenges

Researcher-originated discussion on 28 November 2026,
with assistant-developed experimental formulations.
These questions are not findings or approved protocols.

| ID | Record | Scientific or milestone status | Evidence and related IDs |
|---|---|---|---|
| Q-053 | Can lifetime structural reorganisation of a neural controller improve survival after accounting for computation, maintenance and growth costs? Distinguish weight plasticity from adding or pruning connections and neurons. | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · Q-005, Q-047, H-015 |
| Q-054 | Can heritable learning rules and learning-rate regulation evolve, rather than merely switching a supplied learning mechanism on or off? | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · H-008, H-015, Q-005, Q-032 |
| Q-055 | Can heritable mutation and recombination modifiers coevolve with cognition and reproductive strategy under ecological selection? | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · Q-030, Q-051, Q-052 |
| Q-056 | Do constant, gradual and exponentially increasing environmental pressures favour different adaptive mechanisms, extinction risks or complexity trajectories? | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · Q-003, Q-010, H-006, H-007 |
| Q-057 | Can a predefined population-performance feedback rule generate sustained new challenges without researcher rescue or selecting desired winners? | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · Q-010, Q-019, M-012 |
| Q-058 | How do survival-only selection and explicitly guided cognitive capability objectives differ in generalisation, viability, complexity and computational cost? | OPEN QUESTION | [Proposal](research_knowledge/PLASTIC_EVOLUTION_AND_CHALLENGES.md) · H-005, H-016, Q-016 |
| M-017 | Controlled plastic neural controllers and evolution of learning rules; staged extension of M-010. | PROPOSED | Q-053, Q-054, Q-055; bounded mechanisms, cost controls, fresh protocols |
| M-018 | Constant, progressive, exponential and adaptive environmental challenge comparisons. | PROPOSED | Q-056, Q-057; feasibility and independent-world controls |
| M-019 | Natural versus guided intelligence evolution. | PROPOSED | Q-058; explicitly separate objective functions and matched evaluation |


### Status history — 28 November 2026

- M-015: PROPOSED → AUDITED; C10 implementation `cc34fb3`, review and computational audit.
- F-046–F-053, Q-053–Q-058, M-017–M-019: initial registration.
- Q-052/M-016 remain separate and proposed.
- Earlier scientific statuses remain unchanged.

Prior M-015 row retained verbatim:

> | M-015 | **C10 controlled recombination and dual-parent information assay.** Prerequisite to separate evolvable reproductive-strategy investigation; new prospective protocol required. | PROPOSED | [Evidence](research_knowledge/evidence/C09/RESEARCH_BRANCH_CANDIDATES.md) · Q-051, F-039, F-041, F-042 |

## 17. C11 — Confirmed learning selection and controlled mechanism investigation

28 November 2026. Researcher approved prospective design and execution; assistant proposed controls, implemented and computationally reviewed. No external peer review.

| ID | Record | Scientific or milestone status | Evidence and related IDs |
|---|---|---|---|
| F-054 | Supplied lifetime learning improves population viability under stable informative cues at fixed S=1 and zero learner overhead: +82.0581 pp [81.4525,82.6637] adjusted 97.5% interval. | VERIFIED WITHIN SCOPE | [C11](research_knowledge/C11.md) · H-005, H-008, F-025, F-038 · B-P1; new controlled evidence, not independently replicated. Population intervention, not individual selection coefficient. |
| F-055 | Selection favours supplied learning from standing heritable variation without mutation: informative-minus-null living-frequency enrichment +42.4144 pp [40.4140,44.4147] adjusted 97.5% interval. | VERIFIED WITHIN SCOPE | [C11](research_knowledge/C11.md) · H-005, H-008, F-032, F-035, F-038 · B-P2; informative G +42.4589 pp, null G +0.0445 pp. All null worlds extinct; duration and conditional replay limitations. |
| F-056 | Learning-locus mutation effect on informative mixed-population enrichment is uncertain: -1.0157 pp [-2.1274,+0.0959] ordinary 95% interval. | INCONCLUSIVE | [C11](research_knowledge/C11.md) · F-055, Q-055 · B4 minus B3; prespecified secondary descriptive contrast, not equivalence. |
| M-020 | C11 targeted fresh-seed confirmation and controlled learning mechanism investigation. | AUDITED | [C11](research_knowledge/C11.md) · F-032, F-054, F-055, F-056, H-005, H-008 · Protocol f3432bd; implementation 3dddc5e; same-workspace scientific acceptance and ledger reconstruction. |

### Status history — C11 closeout, 28 November 2026

- F-032: EXPLORATORY EVIDENCE → VERIFIED WITHIN SCOPE for the three targeted replication contrasts; original C08 estimates and scope preserved.
- F-033–F-038 and H-005/H-008: evidence/limitations extended; status unchanged.
- F-054–F-056 and M-020: initial registration. M-020 AUDITED; scientific acceptance within scope.
- No change to M-014 or M-016–M-019. No new experiment authorised.
