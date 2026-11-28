# Project Archean
### A research programme in artificial life, survival-driven adaptation and inherited experience

**Research question:** Under what conditions can measurable adaptive capabilities emerge from self-maintenance and reproduction, and when does inheriting acquired information help or harm an offspring?

Project Archean explores this question through Python/NumPy and C++ simulations. It starts with a spatial population under metabolic constraints, progresses to controlled navigation and local-sensing experiments, then isolates the effects of inherited experience in a separate decision-making model. The broader hypothesis that selection may favour useful cognitive mechanisms is a research direction, not an established conclusion.

## Research progression

| Stage | Question and principal finding | Evidence |
| --- | --- | --- |
| [01 — Original model](01-original-model/) | Early tuning explored extinction, uncontrolled replication and a finite population bottleneck. | [Historical model overview](01-original-model/snapshot/README.md) · [Age plot](01-original-model/snapshot/evolution_plot.png) |
| [02 — v2.0.0: Navigation baseline](02-v2.0.0-navigation/) | Given exact vent offsets, two of three populations exceeded 99% outside-start reach after five epochs; the third reached 37.5%. | [Protocol](02-v2.0.0-navigation/snapshot/RESEARCH.md) · [Data](02-v2.0.0-navigation/snapshot/baseline_results/summary.csv) |
| [03 — v2.1.0: Local-sensing pilot](03-v2.1.0-local-sensing/) | Six-seed pilot: genuine local cues yielded 48.9% mean reach versus 22.8% with shuffled cues. | [Protocol and results](03-v2.1.0-local-sensing/snapshot/LOCAL_SENSING.md) |
| [04 — Local-sensing replication](04-local-sensing-replication/) | Twenty fresh seeds: genuine cues yielded 74.5% mean reach versus 26.6% with shuffled cues, with an advantage in every seed. | [Report](04-local-sensing-replication/snapshot/LOCAL_SENSING_REPLICATION.md) · [Paired data](04-local-sensing-replication/snapshot/replication_results/paired_rates.csv) |
| [05 — v2.2.0: Inherited experience](05-v2.2.0-inherited-experience/) | Across 2,560 matched family histories, own-parent memory yielded 89.2% correct first choices with stable cues and 10.8% after reversal. | [Protocol and controls](05-v2.2.0-inherited-experience/snapshot/INHERITANCE.md) · [Data](05-v2.2.0-inherited-experience/snapshot/inheritance_results/per_seed.csv) |

![Genuine versus shuffled local sensing in the replication](04-local-sensing-replication/snapshot/replication_results/paired_reach.png)

## What the evidence does and does not show

The spatial studies measure navigation and cue dependence under defined selection and sensory rules. The inheritance study causally compares supplied memory states in a separate model with a designed learning and copying mechanism. The historical age plot is not a direct navigation measure. None of these experiments establishes the emergence of general intelligence, consciousness or the evolution of an inheritance channel.

## Current research — through C11

The programme investigates when adaptive information processing is favoured by survival and reproduction, rather than directly rewarding intelligence. The current studies select among supplied mechanisms; they do not establish spontaneous learning-rule evolution or general intelligence.

| Study | Main result and evidence maturity |
|---|---|
| [v2.3.1 / E07](workspace/experiments/v2_3_lifetime_learning/RESULTS.md) | Designed learning improved late resource choice by 36.43 percentage points (95% paired CI 35.61–37.25, 40 seeds); prospective primary result, no reproduction. |
| [C01–C06](workspace/docs/EXPERIMENT_KNOWLEDGE_INDEX.md) | Computational reconstruction, controlled sensing, costs and mortality; exact analyses and exploratory comparisons show that fixed strategies can match adaptive ones. |
| [C07](workspace/docs/research_knowledge/C07.md) | Stable adaptive lifetime sensing benefits; expensive sensing can reduce survival despite higher accuracy. Exploratory effects and structural controls. |
| [C08](workspace/docs/research_knowledge/C08.md) | Exploratory joint learning/sensing enrichment under stable cheap cues. Three contrasts subsequently confirmed by C11-A. |
| [C09](workspace/docs/research_knowledge/C09.md) | Acquired-information retention can enrich under persistent conditions; transfer costs and changing mappings qualify benefit. Exploratory. |
| [C10](workspace/docs/research_knowledge/C10.md) | Recombination generates absent supplied trait combinations; memory pooling effects depend on conditions. Exploratory; novelty is not adaptation. |
| [C11](workspace/docs/research_knowledge/C11.md) | Three fresh-seed confirmation contrasts and two new controlled learning contrasts. See below. |

### Latest primary results (C11)

| Contrast | Mean (percentage points) | Adjusted confidence interval |
|---|---:|---:|
| A-P1 stable cheap joint-slot enrichment | +24.37 | [20.83, 27.91] |
| A-P2 stable minus unpredictable enrichment | +23.88 | [20.37, 27.40] |
| A-P3 cheap minus expensive enrichment | +24.50 | [20.97, 28.03] |
| B-P1 learning-only minus frozen-only population occupancy | +82.06 | [81.45, 82.66] |
| B-P2 informative minus null learning-frequency enrichment | +42.41 | [40.41, 44.41] |

Each study uses 64 matched seed blocks. A uses a separate three-comparison Bonferroni family; B uses a two-comparison family. A confirms direction and practical effect in three original settings, not exact magnitudes. B is new controlled evidence with fixed sensing, zero extra learning overhead and supplied Bayesian updating. It is not independently replicated. All 430 extinct evaluation worlds are retained, including all 256 B null-cue worlds. No external peer review has occurred.

[Cross-experiment scientific synthesis](workspace/docs/research_knowledge/CROSS_EXPERIMENT_SYNTHESIS.md) · [Evidence catalogue and checksums](workspace/docs/research_knowledge/EVIDENCE.md) · [C11 protocol](workspace/experiments/c11_learning_confirmation/PROTOCOL.md) · [C11 analysis](workspace/experiments/c11_learning_confirmation/ANALYSIS.md).

## Research direction

Under what environmental and evolutionary conditions do measurable cognitive capacities become more advantageous than simpler survival strategies, and when does their value persist across generations? The [research agenda and open questions](workspace/docs/FUTURE_DIRECTIONS.md) record human-evolution-inspired hypotheses, heritable plasticity, lineage persistence, cognitive costs, social learning, a proposed autonomous evolutionary ecosystem and eventual AI-training comparisons. These are prospective directions, not established findings. See also the [original research programme](02-v2.0.0-navigation/snapshot/RESEARCH.md).

The [living research register](workspace/docs/RESEARCH_REGISTER.md) distinguishes scoped verified findings, exploratory evidence, hypotheses, unresolved questions and milestone progress, with stable IDs and a dated status history. Follow the [experiment knowledge index](workspace/docs/EXPERIMENT_KNOWLEDGE_INDEX.md) and [cross-experiment branch map](workspace/docs/RESEARCH_BRANCHES.md) to the evidence and open questions.

## Explore and reproduce

Each numbered folder has a stage-specific README containing the question, findings, limitations and reproduction instructions. Its `snapshot/` directory is a curated copy of the historical checkpoint, with revised documentation and source annotations. Executable logic, available tests and recorded results are retained. Exact original versions remain separately archived. Later snapshots intentionally contain earlier files because those were part of the checkpoint and may be dependencies. No root-level simulation files are needed to run a snapshot.

The [workspace](workspace/) preserves the previously organised cross-experiment working layout (updated documentation, tests and results paths). Use it for continued development; use a numbered stage for checkpoint-specific reproduction. Run experiments with fresh output directories and never overwrite recorded evidence.

## Publication and reproducibility scope

This curated scientific snapshot preserves the integrated source, protocols, findings, negative outcomes and summary evidence through C11. Full raw C01–C11 archives and original prospective-lock Git history are preserved separately in the private research archive. The historical lock hashes in reports identify those original private checkpoints; they are not all reachable from this public snapshot. This publication does not itself provide all raw-ledger files required to independently reconstruct every result. The evidence manifest identifies the available extracts and their source archives. No raw private conversation archive is included.

## Versioned research record

The existing tags are retained: [v2.0.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.0.0), [v2.1.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.1.0), [v2.2.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.2.0). The [May model](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/db28afb06bbaae807a7b9196e8525c3ee9f07964) and [replication](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/769c9052e856cddc86228d58dbd9bbbf978f6484) are pinned by commit. The [cleanup checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/79e5bd308e13a2206e1c1723df6e7022afc89a75) was imported byte-for-byte into the workspace during reorganisation. Subsequent workspace-only validation changes are documented in the [reproducibility audit](workspace/docs/REPRODUCIBILITY.md). Historical scientific evidence remains unchanged; selected documentation and source annotations are editorially revised. See the [public editorial policy](workspace/docs/PUBLIC_EDITORIAL_POLICY.md) for scope and provenance.

*Independent, ongoing research by Devakrishna Anilkumar.*
