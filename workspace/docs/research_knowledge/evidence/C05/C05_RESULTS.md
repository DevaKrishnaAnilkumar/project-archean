# C05 sensitivity results

Phase A evaluated 120 distinct settings with five policies each. Phase B used 29 deduplicated settings and 50 independent seed blocks, with 128 matched episodes per seed. All 928,000 trajectories passed independent, archive-based reconstruction. The net-energy calculation includes all sensing and resource travel. Final energy equals 64 plus net energy.

## Exact grid

| Comparator | Cost-sensitive higher | Exact tie | Cost-sensitive lower |
|---|---:|---:|---:|
| no_sensing | 52 | 68 | 0 |
| fixed | 3 | 109 | 8 |
| random | 7 | 105 | 8 |
| entropy | 91 | 21 | 8 |

The cost-sensitive rule attains the exact adaptive benchmark in 107 of 120 settings. These are design-grid counts and have no probability interpretation.

## Illustrative cases

| Cost multiplier | Budget | Reliability | Best fixed | Cost-sensitive | Compulsory entropy | Adaptive optimum |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 1 | +2.469600 | +2.312800 | +2.469600 | +2.469600 |
| 0.25 | 3 | 1 | +1.647500 | +1.789362 | +1.532100 | +1.789362 |
| 1 | 3 | 1 | +0.710000 | +0.710000 | -1.280400 | +0.710000 |
| 4 | 3 | 1 | +0.000000 | +0.000000 | -12.530400 | +0.000000 |
| 0.25 | 5 | 0.5 | +0.667500 | +0.667500 | +0.134274 | +0.703150 |
| 1 | 5 | 0 | +0.000000 | +0.000000 | -6.250000 | +0.000000 |

At zero sensing cost the myopic rule can stop even when two or more observations together would improve the decision. At high cost no observation may pay, and compulsory entropy seeking still incurs the full expenditure. With uninformative observations the posterior stays at 0.5, all policies use the same final tie draw and receive the same reward outcome for each episode. No agent died.

## Fresh-seed cost sweep at full reliability and three available visits

| Cost multiplier | Cost-sensitive minus fixed | Exploratory 95% paired interval | Exact difference |
|---:|---:|---:|---:|
| 0 | -0.12250 | [-0.15811, -0.08689] | -0.15680 |
| 0.25 | +0.15238 | [+0.11105, +0.19370] | +0.14186 |
| 0.5 | -0.00525 | [-0.05256, +0.04206] | -0.00000 |
| 1 | -0.00525 | [-0.05256, +0.04206] | -0.00000 |
| 2 | -0.00000 | [-0.00000, -0.00000] | -0.00000 |
| 4 | -0.00000 | [-0.00000, -0.00000] | -0.00000 |

All 580 designated theory comparisons passed the prewritten discrepancy check. The archive contains all policy pairs, 50 seed contrasts per pair, condition means and calibration scores. The intervals are exploratory and unadjusted. The settings were selected for controlled exploration. Any subsequent confirmation requires a separate locked protocol and fresh seeds.

Pilot runtime was 33.57 seconds with 41.5 MiB peak resident memory, under the one-process, 2 GB and 15 minute limits.

Protocol commit 2a3e2f2d998e95d528221b62af3870d8dc52ae14. Implementation commit 3c062032202e270756d40ce7498dc9e2e7b56297.

The mortality extension is a candidate protocol for scientific review. The completed 64-unit runs cannot address survival under resource scarcity.
