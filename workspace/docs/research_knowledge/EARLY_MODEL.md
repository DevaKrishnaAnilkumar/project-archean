# Early model and navigation evidence

## Extinction and runaway tuning history

- **Origin and wording** · The original repository README, preserved at `01-original-model/snapshot/README.md` and `db28afb`, records “Extinction at Gen 0” for v1.0 and “200,000+ agents by Gen 1” for v1.1. Repository-author retrospective statement. No chat transcript or run record establishes the result independently.
- **Observation and conditions** · The README attributes extinction to harsh metabolic cost, then describes reducing metabolic decay and enlarging the vent radius together. The exact old parameter values, seeds, time series and configurations are missing.
- **Interpretation and alternatives** · Two changes confound causal attribution. Effective food density, initial positions, parent–child accounting and the absence of a population ceiling could also influence the result.
- **Status and disposition** · Unverified retrospective description. This detail extends F-001 and E01 within their original scope and status. Earlier and later anchors include the founding statement, the v1.2 cap and E02 navigation. A separate factorial replay from a documented reconstruction could test plausibility. It could never verify the historical run.

## What the v1.2 population cap regulates

- **Origin and evidence** · Source inspection at `3f592ec:archean_simulation.py`. The same source survives at `db28afb`. Retrospective Codex code analysis.
- **Operational observation** · Start with 100 agents in [0,50]², energy 100, vent (25,25), strict radius 15, gain 15 before movement, cost 0.5 per step, division threshold 200 and Gaussian weight mutation SD 0.05. The cap sorts by energy and retains up to 500 each step. Position, energy and age reset between epochs. No seed was set for the historical plot.
- **Minor implementation details** · Food gain is per qualifying cell with no stock depletion. Birth appends the child before its parent and Python sorting is stable, so equal energies preserve input order. Parent retains half its post-movement energy and a child receives the constructor default of 100. At a crossing above 200 the combined reserve can fall short of the pre-division total. This is a source-level deduction, with no measured impact in the archived run.
- **Interpretation and alternatives** · The cap is explicit selection on current energy. It can amplify early position and scheduler advantages. The comment labelled active inference describes a direct weighted mapping from exact offsets and energy to bounded movement. The original claims about predictive models and efficient gradient navigation exceed what the code and survivor-age plot establish.
- **Status and disposition** · Source behaviour verified within scope. Causal impact open. Extend F-001, F-002 and Q-009 by linking this record. The next test would isolate finite shared resources, shuffled tie ordering and explicit energy-conserving division in separate locked variants. Retain the original unchanged for comparison.

## First-contact gains coexist with slower successful contacts

- **Origin and evidence** · E02 and extended seed 2, archived `workspace/results/navigation*/summary.csv` and first-hit matrices. Origin is experimental evidence plus retrospective analysis.
- **Observation and scope** · The median first-contact time among successful outside starts rose 9→16, 9→12 and 8→9 steps at epoch five for seeds 0, 1 and 2. Seed 2 retained a median of 9 at epoch ten. Epoch-five dominant-lineage shares were 98.2%, 100% and 19.8%. Seed 2 reached 33.8% dominance at epoch ten and 21 surviving lineages, versus 31 at epoch five.
- **Interpretation and alternatives** · Higher reach can bring formerly failed, difficult starts into the successful group, increasing its conditional median. It could also reflect slower routes. Co-occurrence of dominance and reach gives no causal direction.
- **Status and links** · Exploratory evidence. Extend F-003/F-004 and Q-009. E01 supplies the early baseline and E03/E04 remove exact offsets during local-sensing evaluation. Compare paired start-specific time-to-event curves including non-arrivals, then test family, retention and between-world transfer on new seeds.

## Local cue interventions test dependence on supplied information

- **Origin and evidence** · E03/E04 raw archives, archived protocols, `paired_rates.csv`, and C01 audit. Experimental evidence.
- **Observation** · In the fresh 20-seed replication the weakest and strongest paired genuine advantages were +8.50 and +70.48 percentage points. Both the early six seeds and later 20 include populations with weak absolute reach. Shuffling donors changes the relation between the observations and the agent's location. Zeroing leaves energy input intact.
- **Interpretation, alternatives and limits** · Genuine cue advantage can reflect controller use of engineered directional differences, a smooth Gaussian field and shared test axes. The controls test cue use under matched starts. They do not ask whether a sensor or a sampling movement emerged.
- **Status and disposition** · F-005/F-006 and prior reports already document the main outcome. Preserve raw seed extrema in the numeric inventory as an extension by reference. Compare rotated/noisy fields and changed geometry with shared initial states. C02 studies a different choice-time sampling mechanism.

## Residence versus navigation and the order of complexity

Retrospective methodological analysis (25 November 2026): The population cap could favour agents already near the vent. That causal explanation remains open. Log residence time, match starts, randomise retention and relocate whole populations while preserving pedigree labels to test it. Offsets, component capacity, selection and founder variation deserve separate controls before adding structural evolution. This is a methodological rationale linked to F-003/F-004/Q-009/Q-047/M-010.

The unverified informal navigation figures are preserved in the private addendum. They do not match the tracked summary's all-start founder rates (54.96%, 58.46%, 54.40%) and are distinct from the audited outside-start endpoint. The old pilot's exact cohort and start geometry were unavailable. No existing numerical claim should be replaced.

## The original survivor-age plot has a transient early collapse

- **Origin and evidence** · Visual inspection of `01-original-model/snapshot/evolution_plot.png`, renamed byte-for-byte from `graph1.png` at `db28afb`. Retrospective Codex observation.
- **Original observation** · The trace briefly drops to roughly 81 steps near epoch three, recovers toward 190 within a few epochs, and stays in a comparatively narrow band thereafter. Coordinates are read visually. No logged age series or original seed is available.
- **Interpretation and alternatives** · A burst of younger surviving offspring, repositioning, loss of older individuals, or energy-based truncation could affect mean age. A population-wide collapse is a separate claim requiring count records. The plot measures current survivor age at an epoch boundary.
- **Status and disposition** · Exploratory visual observation. Link F-002/Q-009 and the cap mechanics above. In a future documented run, log birth timing, age distribution, culling and complete counts together. This observation does not justify reconstructing the missing plot data or attributing the early drop to any one mechanism.
