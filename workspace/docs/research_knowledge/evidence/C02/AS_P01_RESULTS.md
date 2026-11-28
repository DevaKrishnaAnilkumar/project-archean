# AS-P01 results

Technical status: PASS. Scientific classification: mixed or inconclusive.

| Regime | Policy | Entropy gain (bits) | Accuracy | Brier | Log loss | Reward rate | Final energy | Gain per sampling energy |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| informative | fixed | 0.752931 | 0.941016 | 0.051112 | 0.184871 | 0.806250 | 14.700000 | 0.200782 |
| informative | random | 0.747954 | 0.939453 | 0.049865 | 0.170799 | 0.809766 | 14.728125 | 0.199454 |
| informative | information | 0.750513 | 0.939063 | 0.050006 | 0.178767 | 0.809375 | 14.725000 | 0.200137 |
| uninformative | fixed | 0.000000 | 0.504297 | 0.250000 | 0.693147 | 0.501953 | 12.265625 | 0.000000 |
| uninformative | random | 0.000000 | 0.504297 | 0.250000 | 0.693147 | 0.501953 | 12.265625 | 0.000000 |
| uninformative | information | 0.000000 | 0.504297 | 0.250000 | 0.693147 | 0.501953 | 12.265625 | 0.000000 |

| Informative contrast | Mean (bits) | Sample SD | Exploratory 95% paired interval |
|---|---:|---:|---|
| Information minus fixed | -0.002418 | 0.029035 | [-0.016007, +0.011170] |
| Information minus random | +0.002558 | 0.029229 | [-0.011121, +0.016238] |

The uninformative control retained posterior 0.5 with zero information gain and identical choices, rewards and final energy across policies. Each episode cost 3.75 energy for sampling and 4.00 for resource travel. Final energies were 8.25 or 16.25. None of the agents died. Visit frequencies, sequence frequencies and entropy at each visit are in per_seed.csv and condition_means.csv.
