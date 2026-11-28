# Active sensing, planning and mortality

## Entropy reduction can change without changing the patch decision

- **Origin and evidence** · C02 paired pilot and C03 exact post-hoc tree, including archived protocol, code, outputs and primary contrasts. Numerical evidence with a retrospective interpretation.
- **Observation** · C02's paired entropy intervals span zero. C03 gives 0.752834 bits for both greedy and optimal entropy policies versus 0.745251 fixed, while both choose correctly 94.10% of the time. Random gives 0.745277 bits and 93.925% accuracy.
- **Interpretation and limitations** · A modest expected information change can leave the maximum-posterior action intact. Designed likelihoods, symmetric geometry and three compulsory visits constrain the comparison. Contrasts crossing zero in the pilot are compatible with the exact gap.
- **Status and record** · C03 is a post-hoc analytical finding. Link the adequacy of the prior candidates and extend Q-002/Q-004 by reference. Compare decision boundaries under unequal payoffs or confidence-dependent actions in a separately locked test.

## Joint value of observations and the cost of a compulsory visit

- **Origin and evidence** · C04 `as-p02-theory/expectations.json` and paired seed results, then C05 `exact/exact_expectations.csv`. Experimental and analytical evidence.
- **Observation** · Quarter-cost myopic sampling beats fixed in expectation at full reliability and budget three. At zero cost the advantage reverses. Across C05's 120 settings myopic wins 3, ties 109 and loses 8 against per-setting optimised fixed. A separate example at quarter cost, half reliability and five visits puts both myopic and fixed at +0.667500 net, below the +0.703150 adaptive bound.
- **Interpretation and alternatives** · A one-step strict-improvement rule can stop before a useful sequence. Both myopic and fixed can miss the adaptive optimum. The large tie count depends on the design grid. In expensive or null regimes compulsory sampling consumes energy with little or no additional decision benefit.
- **Status and disposition** · C04/C05 candidates adequately preserve the main comparative claim. Extend Q-004/H-007/H-011 with the half-reliability example and tie-rule dependency. Mortality was absent at 64 units. An unseen geometry with alternative payoffs or positive planning costs would distinguish robust advantages from free-model control.

## Staying safe for an episode versus sustaining reserves

- **Origin and wording** · The assistant derived this hypothesis from C06, and the researcher highlighted it for follow-up. CHAT-13 records the attribution correction. The original wording is retained in the private addendum.
- **Evidence and scope** · C06 exact outcomes show four-unit survival-first agents abstaining through a single episode with no ongoing maintenance. Task-first adaptive ties fixed on completion in 108 settings and improves on myopic completion in six. At eight units and the highest sensing cost, one observation can force a reward-dependent return, reducing task-first compulsory sensing survival from 100% with immediate travel to 74.5% at full reliability or 50% with null cues.
- **Interpretation and alternatives** · Waiting can protect short-term survival but expend reserves in a continuous lifetime. Informed risky action can also kill. When safer opportunities arrive, waiting can remain advantageous. The C07 protocol adds maintenance and mandatory affordable attempts, so it cannot settle the comparison between voluntary risk strategies.
- **Status and disposition** · Assistant-derived hypothesis highlighted by the researcher, already recovered in the C06 branch report. Add the direct ancestry link to H-004, H-012, Q-001, Q-011 and C07. Proposed validation compares perpetual abstention, fixed foraging, reserve thresholds and multi-period planning with a common action set and varying maintenance and hazard. Separate reward acquisition, arrival and safe return.
