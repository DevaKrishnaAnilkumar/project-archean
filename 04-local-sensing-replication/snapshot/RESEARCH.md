# Archean research programme

The research programme asks when self-maintenance and reproduction favour a measurable adaptive capacity, and which information an offspring can use. The phases below are proposals beyond the navigation baseline.

## 1. Direct-navigation reference experiment

Run `python navigation_baseline.py new_results` from the repository root with Python, NumPy and Matplotlib installed. Choose a fresh output directory. Three independently seeded populations evolve for five epochs under the original rules. The simulation's global NumPy generator is seeded separately from the generator used for held-out starting positions. Each controller is frozen for evaluation and tested from every one of 96 shared starts. At the start of each live step (0–199), a distance strictly below 15 counts as contact, matching the simulation's feeding check. Outside starts exclude free successes at step zero. Time to contact is conditional on success and must be read alongside reach rate. The independent evolutionary replicate is the seed. The thousands of controller/start pairs within a seed share ancestry and starting positions.

Each epoch archive aligns controller weights with founder lineage IDs by row. These IDs enable family counts but do not reconstruct individual parent-child pedigrees. The raw hit matrices contain first-contact steps, with -1 for failure. The original age plot measures the mean current age of survivors at an epoch boundary. The controller observes exact vent offsets and internal energy. The feeding zone does not deplete and the energy cost is constant per step.

## 2. Is local sensing sufficient?

Keep the original controller as an exact-offset comparison. Introduce local concentration measurements from a specified field, matched numbers of inputs and equal sensory budgets. Compare with shuffled-cue and unguided controls. Evaluate across held-out vent positions and starts with more independent training seeds. Report extinction and lineage collapse. Confirm that cue removal degrades navigation before claiming local chemotaxis.

## 3. Can lifetime learning make inherited experience useful?

Give a cell a small mutable memory and verify cue learning and reversal within one lifetime. Test genetically identical offspring under parental, blank and unrelated-parent memory with matched capacity, energy and opportunity. Cross memory condition with stable and reversed cue mappings. Measure first choice before feedback, trials to adapt, energy use and descendants. Sweep memory and sensing costs. Keep a researcher-only lineage archive distinct from memory an agent can access. Defer topology evolution (NEAT) until the fixed-controller comparisons are interpretable.

## 4. What does survival pressure preserve?

Compare selection for individual longevity with selection for surviving descendants when division costs energy. Record division rates and inherited warning responses after simulated hazards disappear. Compare predictable external energy interventions with random and action-contingent interventions entirely inside the simulation. Quantify false alarms, missed danger, and time to revise a learned warning. Predicting a perturbation supports a behavioural claim; identification of its causal source requires independent evidence.

## 5. Can selective inheritance help a human task?

After identifying a transferable mechanism, compare selective inheritance, fresh learning and full transfer on fictional solar-monitoring traces. Use held-out sites, a regime change such as new shading, and injected faults. Compare detection delay at matched false-alarm rates and compute budgets. Resource-limited environmental sensing is another candidate. Application claims depend on evaluation in the intended setting.

## First checkpoint

Outside-zone success at epochs 0 and 5 was 32.4% → 99.2% (seed 0), 37.7% → 99.8% (seed 1), and 31.6% → 37.5% (seed 2). The largest family accounted for 98.2%, 100%, and 19.8% of the final populations respectively. In an exploratory extension (`python navigation_baseline.py extended_results --epochs 10 --seeds 2`), seed 2 reached 43.3% with 21 lineages left. Family dominance is a correlate here; whether it causes higher reach rates requires further trials. Exact held-out positions from the earlier pilot were unavailable. These figures are a new run under the recorded protocol.
