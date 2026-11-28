# C05 parameter sensitivity

Locked 2026-11-27T08:46:17Z. Exploratory extension of AS-P02 at 12a62b9.

Phase A evaluates the full factorial of cost multipliers 0, 0.25, 0.5, 1, 2, 4, visit budgets 1, 2, 3, 5, and reliability 0, 0.25, 0.5, 0.75, 1. Likelihoods interpolate toward 0.55. Each visit costs 1.25 times the multiplier, split into outward movement, sensing and return in the proportions 0.4, 0.2 and 0.4. Final resource travel costs 4 and pays 8 on acquisition. Correct and wrong patches pay with probabilities 0.85 and 0.15. Start at 64 energy. Preserve the AS-P02 geometry, inference, policy objectives and tie rules. Optimise fixed and random plans in expectation before sample generation. Compulsory entropy seeking uses the full budget. The Bellman recursion allows stopping or another sample.

Phase B takes the union of the six cost settings at reliability 1 and budget 3, five reliability settings at cost 1 and budget 3, four budgets at cost 1 and reliability 1, and the interaction {0.25,1,4} × {0,0.5,1} × {1,5}. Include all five policies. Use 128 balanced and matched episodes per seed, seeds 3300–3349. Independent named streams provide states, potential observations, random locations, ties and potential resource outcomes. Smoke uses seeds 3290–3291 and eight episodes across all Phase B conditions. Within-seed matching extends across conditions, with potential draws indexed by visit and location. Final tie-breaking uses a dedicated draw. One CPU process, at most 2 GB and 15 minutes.

Phase C is design only. Keep original AS-P02 evidence separate. Do not tune conditions after viewing evaluation.
