# AS-P02 results

Technical validation passed. All 76,800 condition-assigned episodes across thirty conditions and 20 independent seed blocks passed the raw-data audit.

| Informative cost | Mean paired energy difference | Sample SD | Exploratory 95% interval | Exact difference |
|---|---:|---:|---:|---:|
| low | +0.136011 | 0.245941 | [+0.020907, +0.251115] | +0.141862 |
| original | -0.024062 | 0.207876 | [-0.121352, +0.073227] | +0.000000 |
| high | +0.000000 | 0.000000 | [+0.000000, +0.000000] | +0.000000 |

At low cost, the myopic policy used additional visits selectively and improved expected energy over the best fixed routine. At the original cost, the policies tie in exact expectation and the interval spans zero. At high cost, both skipped sensing and agreed episode by episode. In these specified conditions the myopic policy attains the exact adaptive energy benchmark for all costs and observation regimes.

| Regime | Cost | Policy | Expected energy | Realised energy | Correct choice | Visits | Exact adaptive gap |
|---|---|---|---:|---:|---:|---:|---:|
| informative | low | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 1.78936 |
| informative | low | fixed | 17.66281 | 17.68437 | 0.85273 | 1.00000 | 0.14186 |
| informative | low | random | 17.60594 | 17.62500 | 0.84258 | 1.00000 | 0.14186 |
| informative | low | entropy | 17.55406 | 17.59062 | 0.94492 | 3.00000 | 0.25726 |
| informative | low | cost_sensitive | 17.79882 | 17.83601 | 0.91523 | 1.68477 | 0.00000 |
| informative | original | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.71000 |
| informative | original | fixed | 16.72531 | 16.74687 | 0.85273 | 1.00000 | 0.00000 |
| informative | original | random | 16.66844 | 16.68750 | 0.84258 | 1.00000 | 0.00000 |
| informative | original | entropy | 14.74156 | 14.77812 | 0.94492 | 3.00000 | 1.99040 |
| informative | original | cost_sensitive | 16.70125 | 16.73750 | 0.84844 | 1.00000 | 0.00000 |
| informative | high | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| informative | high | fixed | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| informative | high | random | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| informative | high | entropy | 10.99156 | 11.02812 | 0.94492 | 3.00000 | 5.03040 |
| informative | high | cost_sensitive | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | low | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | low | fixed | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | low | random | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | low | entropy | 15.02531 | 14.97188 | 0.49336 | 3.00000 | 0.93750 |
| uninformative | low | cost_sensitive | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | original | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | original | fixed | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | original | random | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | original | entropy | 12.21281 | 12.15938 | 0.49336 | 3.00000 | 3.75000 |
| uninformative | original | cost_sensitive | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | high | no_sensing | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | high | fixed | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | high | random | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |
| uninformative | high | entropy | 8.46281 | 8.40938 | 0.49336 | 3.00000 | 7.50000 |
| uninformative | high | cost_sensitive | 15.96281 | 15.90938 | 0.49336 | 0.00000 | 0.00000 |

The uninformative control passed. All beliefs stayed at 0.5 and patch choices and rewards matched across policies. Only compulsory entropy seeking spent energy on sensing. No mortality occurred. The comparisons and condition means CSVs report secondary paired contrasts, reward rates, visit and sequence distributions, sensing and travel costs, entropy, Brier score, log loss and early stopping.
