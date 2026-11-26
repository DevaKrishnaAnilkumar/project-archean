# Cross-platform reproducibility audit

## Audit date

26 November 2026.

## Scope

Reproduction of the archived v2.2.0 inherited-experience
experiment following repository reorganisation.

## Verification environment

- Architecture: Apple Silicon (ARM64)
- Python: 3.9
- NumPy: 2.0.2
- Matplotlib: 3.9.4

## Results

| Check | Result |
|---|---:|
| Independent seeds evaluated | 40 |
| Archived arrays checked | 1,360 |
| Exactly matching arrays | 1,320 |
| Floating-point tolerance matches | 40 |
| Significant array mismatches | 0 |
| Summary metrics verified | 2,000 |
| Maximum array difference | 2.220446049250313e-16 |
| Maximum metric difference | 5.551115123125783e-17 |

All observed array discrepancies were confined to the
floating-point resource-offer variable (`offer`).

## Regression test policy

The replay test retains exact equality for all arrays
except `offer`, which permits an absolute tolerance of
two float64 machine epsilons, with zero relative tolerance.

Array shapes and data types must remain identical.

Archived summary metrics are checked with an absolute
tolerance of 1e-12 and zero relative tolerance.

## Preservation of research evidence

No historical simulation logic, archived results or
research tags were modified during this audit.

## Limitations

This audit supports numerical and behavioural reproducibility
of the archived inherited-experience experiment in the
specified environment.

It is not an independent scientific replication, nor
does it establish reproducibility across every platform,
dependency version or experimental condition.
