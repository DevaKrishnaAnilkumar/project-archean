# Local sensing under metabolic selection

## Question and design

Can selection improve first contact with an energy vent when cells sense only spatial differences in a local concentration field? Does removing the link between each cell's observations and its surroundings impair its navigation?

Six training seeds (0–5) each start with 100 founders, in two matched arms. Both use the v2.0.0 population, mutation, feeding, epoch-reset, energy and movement rules. The exact arm keeps the v2.0.0 input. In the local arm four receptors sample a Gaussian field one spatial unit east, west, north and south of the cell. The field is 400 exp(−r²/800), where r is distance to the vent in simulation units. The controller receives east minus west, north minus south, and internal energy. Local observation and movement use the same axis frame. Receptors are noiseless and there is no additional sensing charge. These design choices specify a favourable first test of spatial gradient sensing. Training uses one stationary vent at (25,25) for five epochs of 200 steps each.

At founder and final snapshots, sample up to 32 controllers uniformly without replacement. Evaluate every selected controller on the same 96 outside-zone starts across four displaced vents, for up to 200 pre-movement contact checks. The reach fraction is the fraction of controller/start pairs that reach within 15 units. Keep training seed as the independent replicate. Sampling cells weights families by their abundance.

For every local controller use three paired evaluations: genuine receptor readings, readings reassigned between different trials of the same controller at each step, and both receptor differences set to zero. All retain the energy input. For shuffling, trajectories continue producing prospective readings after first contact so the donor pool stays fixed. Success is scored only once. These controls probe dependence on spatial information. They do not measure acquired memory, learning within one lifetime, noise tolerance or general intelligence.

## Reproduce

Run `python -m unittest -q test_local_sensing` and `OPENBLAS_NUM_THREADS=1 python local_sensing.py my_local_results` in the repository with NumPy and Matplotlib available. Use a new output directory. The summary contains population and founder-lineage counts. NPZ files contain starts and vents or selected indices, frozen weights and first-contact steps (−1 for misses). Exact and local training share seed initialization. Trial generation, controller sampling and shuffling use independent RNGs from training.

## Results

| Seed | Founder local | Evolved local | Evolved shuffled | Evolved zero | Evolved exact arm |
|---|---:|---:|---:|---:|---:|
| 0 | 19.6% | 31.2% | 22.4% | 19.8% | 97.5% |
| 1 | 21.9% | 87.8% | 28.6% | 19.3% | 100.0% |
| 2 | 18.4% | 23.3% | 20.8% | 19.9% | 36.2% |
| 3 | 21.6% | 29.7% | 19.2% | 20.0% | 63.0% |
| 4 | 18.5% | 28.0% | 20.0% | 19.8% | 53.9% |
| 5 | 22.9% | 93.3% | 25.6% | 19.3% | 100.0% |
| Mean | 20.5% | 48.9% | 22.8% | 19.7% | 75.1% |

All six populations persisted through five epochs. Rates summarize 32 sampled controllers per snapshot. The means weight training seeds equally. Separate exact-direction controllers give a reference for performance under a different sensory interface. The matched cue intervention within each local controller is the test of cue dependence. Verified with Python 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8.
