# v2.2.0 — Inherited experience and perceived control

[Back to research overview](../README.md) · [Exact historical checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/0775ab4256dec5c15ee56ea536c112436041cf04) · [Tag v2.2.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.2.0)

This is a retrospective guide. The `snapshot/` directory preserves the entire tracked tree at commit `0775ab4256dec5c15ee56ea536c112436041cf04` byte-for-byte, including its original README and relative paths. This is a historical checkpoint, not a newly run experiment.

## Research question
When does transferring a parent's acquired state help or harm an offspring? Can agents learn action-dependent resource contingencies and benefit from retained internal cost information?

A separate discrete-encounter assay uses 40 independent seeds with 64 matched parent families each. Offspring receive own-parent, blank or unrelated-parent memory under stable and reversed cue mappings. Companion assays test responsive versus replayed interventions and retained versus shuffled action-cost estimates.

## Findings
- Own-parent memory: 89.2% correct first choices under stable cues and 10.8% under reversed cues; blank memory achieved 49.3% and 50.7%.
- Mean net energy with parental versus blank memory was 31.94 versus 30.17 units when stable and 23.01 versus 30.02 after reversal.
- Final-eight signalling rates were 87.0% under responsive help versus 29.1% under matched open-loop replay.
- A supplied own-cost estimate improved action choice; zero prediction error follows from the fully revealing calibration by construction.

## Evidence
- [Original README (unchanged)](snapshot/README.md)
- [Protocol, controls, results and interpretation](snapshot/INHERITANCE.md)
- [Experiment source](snapshot/inherited_experience.py) and [unit tests](snapshot/test_inherited_experience.py)
- [Seed-level data](snapshot/inheritance_results/per_seed.csv) and [raw archives](snapshot/inheritance_results/)

## Reproduce
From `snapshot/` with Python, NumPy and Matplotlib installed:

```sh
python inherited_experience.py ../new_inheritance_results
python -m unittest -q
```

## Limits and future research
Learning and copying are supplied by design. The assays do not demonstrate the evolution of transmission mechanisms, consciousness, representation of an outside designer, or integration of lifetime learning into the spatial model. Test whether selection favours costly mechanisms for copying, revising or discarding acquired information in changing environments. See the [original research programme](snapshot/RESEARCH.md).
