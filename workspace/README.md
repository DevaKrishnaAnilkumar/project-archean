# Project Archean

When does an artificial organism benefit from inheriting what its parent learned? Archean explores this question in Python and NumPy through two models. In a spatial simulation, cells spend energy, reproduce and pass on movement controllers. A separate two-choice experiment tests what happens when offspring explicitly copy a parent's learned preference.

## Experiments

| Study | Finding | Protocol and evidence |
|---|---|---|
| Navigation baseline | With the exact direction to food available, two of three populations reached it from over 99% of outside starts after five epochs. | [Design](docs/RESEARCH.md) · [Data](results/navigation/summary.csv) · [Extended run](results/navigation-seed2/summary.csv) |
| Local sensing | Across 20 fresh populations, mean vent-reaching was 74.5% with genuine local cues and 26.6% when cues were shuffled. | [Pilot](docs/LOCAL_SENSING.md) · [Replication and figure](docs/LOCAL_SENSING_REPLICATION.md) · [Paired results](results/local-sensing-replication/paired_rates.csv) |
| Inherited experience | Across 2,560 simulated families, offspring with parental memory chose correctly on 89.2% of first trials when the cue stayed stable and 10.8% when it reversed. | [Protocol and controls](docs/INHERITANCE.md) · [Seed-level results](results/inheritance/per_seed.csv) |

The copying rule in the inheritance experiment is supplied by design. Whether selection favours copying, revising or discarding experience remains an open research question.

## Run an experiment

From the repository root, with Python, NumPy and Matplotlib installed, choose a fresh output directory.

```sh
python inherited_experience.py my_inheritance_results
python -m unittest -q
```

The protocol for each study gives its reproduction commands. The [model history](docs/MODEL_HISTORY.md) records earlier tuning decisions. The [research programme](docs/RESEARCH.md) describes the original plan.

## Research checkpoints

[Navigation baseline · v2.0.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.0.0) · [Local-sensing pilot · v2.1.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.1.0) · [Inherited experience · v2.2.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.2.0)
