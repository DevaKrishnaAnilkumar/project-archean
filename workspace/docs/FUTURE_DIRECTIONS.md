# Project Archean — Research questions and future directions

**Status:** Prospective research agenda, 26 November 2026. These are proposals and open questions, not completed experiments, approved protocols or claims of novelty.

For the current evidence and milestone status of each research item, see the [living research register](RESEARCH_REGISTER.md).

## Central question

Under what environmental and evolutionary conditions do measurable cognitive capacities become more advantageous than simpler survival strategies, and when does their value persist across generations?

The broader hypothesis is that useful information-processing mechanisms may evolve as a consequence of self-maintenance, reproduction and heritable variation. A second, applied hypothesis is that ecological evolution could become a useful way to develop adaptive AI agents. Both hypotheses remain open. Evolution is not a search with intelligence as its predetermined destination.

## Evidence so far

- The original spatial model explores metabolic selection and population bottlenecks, with important limitations in its original claims.
- v2.0–v2.1 and the 20-seed replication measure evolved navigation and dependence on meaningful local cues.
- v2.2 tests explicitly supplied parental experience and controlled information transfer in a discrete assay. It does not show that inheritance of acquired information evolved.
- [v2.3.1](../experiments/v2_3_lifetime_learning/RESULTS.md) demonstrates a designed learning rule's benefit in a spatial resource-choice assay; its 40-seed primary difference is +36.43 percentage points (95% CI +35.61 to +37.25). Reversal recovery and survival are exploratory. No reproduction or evolution occurs in this assay.

## Human evolution as inspiration, not a target

The [Smithsonian human evolution timeline and family tree](https://humanorigins.si.edu/evidence) provide starting evidence about changing climates, diverse hominin species, locomotion, tools, food, brains and social behaviour. Traits appeared at different times and branches; fossil and archaeological evidence is incomplete. We will not force an ape-to-human sequence or claim to reproduce hominin history. We will test abstract pressures in parallel ecologies, including simpler and nonhuman strategies.

Potts's variability-selection hypothesis motivates testing adaptability under changing conditions [1,2]. Competing/complementary explanations include ecological foraging demands, social complexity, energetic constraints and intergenerational investment [3–6]. These hypotheses are not mutually exclusive and their relative causal importance is debated. Cultural transmission can also expand adaptive information beyond an individual's lifetime [7]. These are biological motivations, not results of Archean.

| Biological motivation | Proposed experimental factor | Main test and comparison |
| --- | --- | --- |
| Variable habitats and seasonal change | Resource turnover, spatial relocation and temporal autocorrelation | Stable vs periodic vs stochastic environments at matched expected supply; fixed vs plastic strategies |
| Dispersed or extractive foods | Resource patch density, depletion/regrowth, access costs and action sequences | Local reactive vs remembered or planned foraging; held-out maps |
| Danger and competition | Safe simulated hazards, competition for finite resources | Reactive vs predictive strategies; match hazard exposure and sensory opportunity |
| Social relationships | Local encounters, shared resources, opportunities for joint access | Solitary vs interacting populations; compare cooperation with selfish and exploitative alternatives |
| Parental investment and extended development | Energy transfer, offspring dependency and delayed maturity | Measure parent costs, offspring survival, reproductive success and descendant persistence |
| Energetic costs of cognition | Charge memory occupancy, sensing, updating and computation separately | Measure marginal benefit and cost; include zero-cost and no-learning controls |
| Cumulative culture | Vertical and horizontal acquisition of learned information | Genetic-only, parental-state, social-learning and combined modes; measure copying error, retention and innovation |
| Environmental modification | Local, persistent alterations to resource access | Compare fixed and alterable worlds; look for niche construction without awarding a tool-use score |

## Open doubts and falsifiable alternatives

1. **Is complexity necessary?** A cheap fixed controller may outperform costly learning in a stable habitat. In highly unpredictable worlds, memory may be unhelpful. A possible intermediate optimum is a hypothesis, not an assumed curve. Separate change frequency, predictability, cue reliability, resource supply and cognitive cost.
2. **What is learning actually doing?** Improvement might reflect a narrow supplied association rule rather than general adaptation. Test memory ablation, shuffled cues, matched fixed heuristics, novel maps and changes in reward contingencies.
3. **Does learning evolve?** Allow plasticity parameters (including zero), memory capacities and update rules to vary heritably. Test whether selection favours plasticity relative to neutral drift and nonplastic controls; use separate ancestry and memory records.
4. **What should be inherited?** Distinguish genetic controller parameters, acquired lifetime state, evolved copying machinery, social learning and the researcher-only archive. Compare blank, parental, unrelated and selectively transmitted states; include copying costs and environmental reversal. Do not equate these channels with biological genetic inheritance.
5. **Individual vs lineage:** Long survival may not increase reproductive success. Selection may favour short-term reproductive success even when descendants fail in the long term. Track birth/death, viable offspring, lineage growth and persistence across specified horizons. Use neutral and relatedness controls; do not assume organisms consciously act for a lineage or award a lineage-persistence bonus in the autonomous world.
6. **Is emergence an artefact of the simulator?** Check energy accounting, scheduling, boundary conditions, population limits, sensor leakage and mutational accessibility. Test whether outcomes depend on artificial epoch resets, top-energy culling or nondepleting resources. Preserve null results, extinction, degeneracy and exploitative strategies.
7. **Does complexity keep increasing?** Mutation and reproduction may yield equilibrium, extinction or a simple dominant strategy. Quantify diversity, novelty and functional adaptation over time, not just neural size or survival. Compare selection with neutral evolution; distinguish exploratory novelty from expansion of functional possibilities.
8. **Can agents predict their own state?** Explore action-dependent resource feedback, retained internal cost estimates, forecast error and behaviour under perturbation; compare with simple feedback controls. Such behaviours are not evidence of subjective experience or identification of an external causal source.
9. **Is this useful for AI?** Compare ecological evolution with supervised/self-supervised, reinforcement-learning and conventional evolutionary baselines where appropriate to the same task. Match training information, interaction and compute budgets, evaluate held-out environments, sample efficiency, robustness and transfer. Do not claim a fundamentally new learning category merely because ecological selection replaces task-specific reward shaping. Within-lifetime learning may still use reinforcement or self-supervised mechanisms.

## Proposed research programme (version labels provisional)

| Track | Question | Gate before advancing |
| --- | --- | --- |
| v2.3.2 Continuous spatial learning | Does acquired state improve locomotion/foraging with local, noisy sensing? | Matched frozen and reactive controls, held-out geometry, movement/energy invariants |
| v2.4 Heritable plasticity and memory | Does selection favour the capacity to learn, retain or transmit? | Mutational variation and pedigree verified; selection vs drift and fixed inheritance |
| v2.5 Life history and lineage persistence | When do reproductive investment and information transfer improve viable descendants? | Energy-conserving reproduction, explicit genealogy, multigenerational outcomes |
| v2.6 Cost and environmental variability | Where does cognition pay for itself? | Factorial comparisons of cost, change rate and predictability; retain noncognitive successes |
| v2.7 Evolvable architecture | Can useful neural connections, memory structures or update rules evolve? | Bounded architecture, viable mutations, complexity and causal ablations |
| v2.8 Ecology and social/cultural mechanisms | How do resource competition, cooperation, social transmission and niche construction interact? | Validate each mechanism separately; independently replicated environments |
| v3.0 Autonomous evolutionary ecosystem (provisional) | What develops from minimal founders in a validated, autonomous evolving world? | Frozen environment/perimeter, tested simulator, independent worlds and predefined observation plan |
| Applied AI track | Can evolved mechanisms transfer to practical tasks? | Matched conventional baselines and held-out benchmarks; possible fictional solar/environmental sensing tasks only after mechanism identification |

Tracks may run in parallel or be reordered as evidence warrants. Each gets a separate prospective protocol, controls, independently chosen seeds, and analysis criteria. The original historical snapshots remain archived separately; public copies may have editorial revisions.

## Long-duration autonomous evolutionary ecosystem

After controlled validation, initialize minimally capable agents in a bounded simulated ecology. Provide physically defined observations, primitive actions, energy accounting, reproduction and mutation rules, but no target intelligence score, task labels, hand-selected lineages, explicit reward for cooperation or manual rescue. Environmental laws impose implicit selection; the experiment is not objective-free. Allow continuous life and reproduction without researcher-driven resets or top-energy culling where feasible. Parameterise and validate resource regeneration, mortality, finite capacity, interaction order, costs and mutational pathways before launch. Computational caps are part of the ecology and their effects must be reported.

Genomes may encode controllers, learning and transmission mechanisms; acquired state remains separate. A researcher-only record stores unique parent/child IDs, birth/death times, mutations, genotypes, acquired state snapshots, ecological state and RNG state. Agents cannot read the archive or access external systems. Use deterministic checkpoint/resume, fixed compute/time budgets, multiple independent worlds, frozen-genotype and neutral-drift comparisons, and predeclared interruption criteria for errors/resource limits. Do not intervene to select a desired outcome. Extinction and equilibrium are valid outcomes. Longer runs do not by themselves establish open-ended evolution.

Measure surviving descendants, reproduction distributions, energetic cost, information use, adaptation to held-out perturbations, behavioural diversity, innovation persistence and causal effects of disabling mechanisms. Define operational measures before each experiment. Post-run exploration must be labelled exploratory and verified on fresh worlds before confirmatory claims.

## Related work and novelty boundary

Avida demonstrated evolution of complex digital functions in a designed environment [8]. Polyworld already explores evolution of neural control in computational ecology [9]; it is especially relevant to the proposed long-duration experiment. Open-ended evolution is an existing and unresolved research area [10]. Archean's candidate contribution is a controlled, traceable investigation linking self-maintenance, learning costs, environmental variability, acquired-information transmission and lineage outcomes, followed by matched evaluation as an AI development method. Novelty and usefulness need further literature review and empirical comparison.

## References and starting points

1. Smithsonian Human Origins Program. [Climate Effects on Human Evolution](https://humanorigins.si.edu/research/climate-and-human-evolution/climate-effects-human-evolution).
2. Potts, R. (2012). [Evolution and Environmental Change in Early Human Prehistory](https://doi.org/10.1146/annurev-anthro-092611-145754). Annual Review of Anthropology.
3. [Why are there so many explanations for primate brain evolution?](https://pmc.ncbi.nlm.nih.gov/articles/PMC5498304/) (2017).
4. [Both Diet and Sociality Affect Primate Brain-Size Evolution](https://pmc.ncbi.nlm.nih.gov/articles/PMC10275546/) (2022).
5. [The economics of brain size evolution in vertebrates](https://www.sciencedirect.com/science/article/pii/S0960982222007357) (2022).
6. Kaplan, H. & Robson, A. J. (2002). [The emergence of humans: The coevolution of intelligence and longevity with intergenerational transfers](https://pmc.ncbi.nlm.nih.gov/articles/PMC126651/).
7. Boyd, R., Richerson, P. J. & Henrich, J. (2011). [The cultural niche: Why social learning is essential for human adaptation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3131818/).
8. Lenski, R. E., Ofria, C., Pennock, R. T. & Adami, C. (2003). [The evolutionary origin of complex features](https://doi.org/10.1038/nature01568).
9. Yaeger, L. S. (2009). [How evolution guides complexity](https://pmc.ncbi.nlm.nih.gov/articles/PMC2801533/).
10. Taylor, T. et al. (2016). [Open-Ended Evolution: Perspectives from the OEE Workshop in York](https://doi.org/10.1162/ARTL_A_00210).

This is a living agenda; revisions should distinguish prior expectations from observations made after data collection.
