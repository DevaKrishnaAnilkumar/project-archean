# Inheritance, intervention and spatial lifetime learning

## Late recovery leaves an early energy deficit

- **Origin and source** · E05 `per_seed.csv` columns `stable_parent_net`, `stable_blank_net`, `reversed_parent_net`, `reversed_blank_net`, and corresponding first/last-eight metrics. Experimental evidence.
- **Observation and context** · The own-parent versus blank average net was 31.9430 versus 30.1711 under stability, and 23.0145 versus 30.0211 under reversal. After reversal the corresponding late accuracies converged near 89%.
- **Interpretation** · An initial bias can have a cumulative cost after decision accuracy recovers. Aggregate net energy combines early errors and later behaviour, so different trajectories can yield equal late accuracy.
- **Status and disposition** · Exploratory extension of F-007/H-009/Q-006. C07 links post-change belief recovery to another outcome but has no memory inheritance. Test recovery of both behaviour and resource deficit with prospective endpoints and matched budgets. The copying channel was designed.

## Matching energy pulses makes signalling costs visible

- **Origin and source** · E05 `per_seed.csv`, `responsive_net`, `replay_net`, `withdrawn_net` and child replay fields. Experimental evidence.
- **Observation** · Responsive signalling exceeded replay signalling while net energy averaged 46.0125 versus 56.5301 units. The paired replay gets the same pulse stream independent of its own actions. Withdrawal dropped late signalling and mean net to −5.5262. Under child replay, own-parent memory averaged 53.2078 units versus 56.5863 for blank. Last-unit signalling was 97.27% for own and unrelated responsive-parent memory versus zero for blank.
- **Interpretation and alternative** · Replay breaks contingency while preserving received pulses. Differences in signalling expenditure can account for the energy ranking. The last-unit probe uses decision value without modelling an agent's remaining reserve.
- **Status and disposition** · Extend F-008/H-009/Q-011/Q-020 as scoped secondary evidence. The own-cost calibration result is already covered by F-009. C04/C07 provide parallel accuracy or information-versus-energy comparisons on distinct models. Independently cross contingency, resource reserves and action costs with yoked replay and matched training history.

## Computational replay and biological-style learning evidence

- **Origin and source** · E06 `workspace/docs/REPRODUCIBILITY.md`, E07 `results/per_seed.csv`, `death_counts.csv`, phase discussions and C01 archive audit. Experimental and computational evidence.
- **Observation** · The E06 near-zero ARM64 differences occurred in offer arrays; the archived decision summaries reconciled. E07 has separately recorded trial-specific, conditional-on-choice and scheduled-denominator accuracy, cause of death and completed trips. C01 reconciled E07's 257,048 values and all 40 primary seed contrasts from archived sequences with no discrepancy.
- **Interpretation and limitation** · This supports traceability. Conditioning on a surviving choice can mask failures caused by exhausted energy. Reconstructing an archive does not regenerate fresh experimental cohorts. Git dates establish a recorded sequence, with no independent time certification.
- **Status and disposition** · F-010/F-011/F-015 adequate as stated. Link E07/ C07 stratified ranges in the inventory as further evidence for F-012–F-014, H-002–H-004 and M-014. To test transfer, use new seed blocks, explicit censoring and decision/maintenance/death denominators. The fixed-route associative task differs from C07's choice of a sensor.
