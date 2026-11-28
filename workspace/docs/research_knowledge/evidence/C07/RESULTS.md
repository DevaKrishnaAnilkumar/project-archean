# C07 continuous lifetime learning

Technical validation passed. The six policies were evaluated across 15 settings with 50 independent seed blocks, 32 organisms per seed and 48 scheduled periods. Checks reconstructed 6,912,000 scheduled organism-periods, including 3,876,860 actual resource choices and 75,901 deaths. All seven tests passed. The pilot took 8.28 seconds at 90.8 MiB peak RSS.

| Prespecified contrast | Estimate | Exploratory 95% paired interval |
|---|---:|---:|
| Stable, 24 energy. Adaptive learning minus adaptive frozen, periods completed alive | +5.7325 | [4.8725, 6.5925] |
| Stable, 24 energy. Adaptive learning minus fixed learning, periods completed alive | +4.9694 | [4.1644, 5.7744] |
| Stable, 512 energy. Adaptive learning minus adaptive frozen, correct choices in periods 33–48 | +11.3945 percentage points | [10.6458, 12.1432] points |

At stable 24 energy, survival through period 48 was 66.63% for adaptive learning, 42.13% for adaptive frozen and 43.19% for fixed learning. No agents died at 512 energy, so the late accuracy contrast is available without mortality conditioning. These are three exploratory comparisons with no multiplicity adjustment.

## When learning helped and when it did not

At 24 energy after a scheduled reversal, adaptive learning exceeded adaptive frozen by 5.47 periods completed alive over the full lifetime. At 512 energy, 95.31% of adaptive learners met the sustained correct-mapping recovery criterion after reversal, with an 8.03-period restricted mean delay. Fixed learners met it in 96.50%, with a 7.88-period restricted mean delay. Adaptive sampling improved overall resource decisions in this condition, without a corresponding improvement in this belief-recovery metric.

At 24 energy with unpredictable mappings, adaptive learning minus adaptive frozen was −0.226 periods completed alive, with interval [−1.060, +0.609]. The fixed 0.05 hazard assumption cannot anticipate a mapping independently resampled each period.

At eight energy and a 2.5-unit trip cost in the stable condition, adaptive learners made 72.17% correct choices conditional on reaching a decision, versus 49.73% without sensing. Their mean periods completed alive were 3.555 versus 6.970. All learners in this setting sampled whenever the protocol's affordability rule allowed. The result concerns that rule and its sensing costs.

At q=0.50, ordinary learned beliefs stayed at 0.5. All policies made exactly the same resource choices and received the same rewards episode by episode. The sensing policies spent 15 extra energy units over 48 periods relative to no sensing. Oracle mapping access supplied no information about H in this control.

## Scope

The protocol supplies Bayesian feedback, a fixed switching hazard and mandatory sensing when affordable. It tests updating and using a hidden sensory-mapping belief within one lifetime. It contains no reproduction, evolution, or learned stopping rule. Early death changes which agents contribute to conditional accuracy and belief curves. All scheduled-period metrics include every agent, including those that died. Reversal delay includes unrecovered and dead agents at the 24-period restriction. Raw variables preserve frozen beliefs after death without further updates.
