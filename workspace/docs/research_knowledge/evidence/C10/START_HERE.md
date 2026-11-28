# Project Archean — C10 review and recovery

**Status:** execution complete; independent computational audit passed; scientific review and permanent C10 register integration pending. C09 closeout is already integrated, including Q-051/M-015 (controlled two-parent experiment) and Q-052/M-016 (separate future evolution of reproductive strategy). No public changes and no later simulation.

## Read first

- `RESULTS.md`: primary results, secondary observations, limitations.
- `CROSS_EXPERIMENT_COMPARISON.md` and `RESEARCH_BRANCH_CANDIDATES.md`: cumulative knowledge and ten candidate branches.
- `workspace/experiments/c10_recombination/`: protocol, prior evidence, locked source, analysis, and raw schema.
- `audited/audit.json`, `independent_primary.json`, `results/primary.csv`: exact checks and primary contrasts. `results/conditions.csv` contains every condition; `audited/worlds.csv` contains every world. See `DEVIATIONS_AND_FAILURES.md` for pre-evaluation compilation corrections and archive packing issue.

## Checkpoints

- C09 documentation closeout: `b940c998d744ac9cd4639ca9a6d3b9d8a4cbbde2` (132 records, 50 relationships).
- C10 protocol: `2aadbcf8b7872e9c6f4ee4211aed25474740c201`.
- C10 implementation: `cc34fb3540f594f7bd3ce0a04ba507f470cde45b`.

## Offline recovery

Download this review ZIP **and both raw-evidence parts**, retaining the earlier original experiment archives. Extract the review ZIP to a fresh directory. Place the two raw ZIPs beside `raw_parts.json`. Run:

```sh
 git clone --branch research/c10-recombination-local Archean_C10.bundle project-archean
 git -C project-archean fsck --full --no-dangling
 git -C project-archean rev-parse HEAD
 git -C project-archean status --short
 python restore_raw.py raw_parts.json restored .
```

Expected HEAD is the C10 implementation checkpoint above. Restore script verifies full ZIP hashes and all 12,674 original raw member hashes; restores original binary layouts and both designs. Requires Python and NumPy. Each raw part holds 960 evaluation and 96 smoke worlds. Original action records are encoded losslessly as 30-byte planes in the raw ZIPs.

## Re-run audit and analysis

The validated environment is Linux x86_64, Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8, GCC 14.2.0. Run from the review directory using fresh output paths:

```sh
 export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
 python project-archean/workspace/experiments/c10_recombination/audit.py restored/raw audited_again --mode eval
 python project-archean/workspace/experiments/c10_recombination/analysis.py audited_again results_again
 python recompute_primary.py restored/raw audited_again/worlds.csv results_again/primary.csv
```

All primary and secondary outcomes remain exploratory; a computational audit is not an independent scientific replication. The Git bundle contains source/history, not all earlier raw archives. Original C09 and preceding evidence archives must remain separately preserved. The review ZIP's SHA256SUMS.txt covers all its members except itself. Raw ZIP hashes appear in raw_parts.json.
