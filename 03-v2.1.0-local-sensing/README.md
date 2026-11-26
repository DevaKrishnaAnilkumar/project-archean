# v2.1.0 — Local-sensing pilot

[Back to research overview](../README.md) · [Exact historical checkpoint](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/6cad1e4b2931fa685375a3eb8f4d9dd54dd79aa8) · [Tag v2.1.0](https://github.com/DevaKrishnaAnilkumar/project-archean/tree/v2.1.0)

This is a retrospective guide. The `snapshot/` directory preserves the entire tracked tree at commit `6cad1e4b2931fa685375a3eb8f4d9dd54dd79aa8` byte-for-byte, including its original README and relative paths. This is a historical checkpoint, not a newly run experiment.

## Research question
Can selection improve navigation using local concentration differences instead of exact vent offsets, and does removing meaningful cues impair navigation?

Six independent seeds compared exact-direction and local-sensing training. Local controllers were evaluated with genuine, shuffled and zero cues using matched held-out trial geometry.

## Findings
Mean evolved local reach was 48.9% with genuine cues, 22.8% with shuffled cues and 19.7% with zero cues. The separately evolved exact-direction reference averaged 75.1%. All six local populations persisted through five epochs; performance varied substantially between seeds.

## Evidence
- [Original README (unchanged)](snapshot/README.md)
- [Protocol and six-seed results](snapshot/LOCAL_SENSING.md)
- [Experiment source](snapshot/local_sensing.py) and [unit tests](snapshot/test_local_sensing.py)
- [Recorded pilot results](snapshot/local_results/)

## Reproduce
From `snapshot/` with Python, NumPy and Matplotlib installed:

```sh
python -m unittest -q test_local_sensing
OPENBLAS_NUM_THREADS=1 python local_sensing.py ../new_local_results
```

## Limits and next question
The sensors are noiseless, carry no additional cost and share a coordinate frame with movement. This measures cue dependence, not lifetime learning or general intelligence. Variability motivates the [20-seed replication](../04-local-sensing-replication/).
