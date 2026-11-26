"""Run with python navigation_baseline.py OUTPUT_DIRECTORY (NumPy and Matplotlib)."""
import argparse
import csv
import json
import platform
from pathlib import Path

import numpy as np

from archean_simulation import ArtificialCell, run_simulation


def evaluate(weights, starts, vent):
    """Evaluate every controller on identical starts until first contact or death."""
    positions = np.broadcast_to(starts, (len(weights), *starts.shape)).copy()
    hits = np.full(positions.shape[:2], -1)
    for step in range(200):
        delta = vent - positions
        reached = np.linalg.norm(delta, axis=2) < 15
        hits[(hits < 0) & reached] = step
        if np.all(hits >= 0):
            break
        inputs = np.empty((*positions.shape[:2], 3))
        inputs[:, :, :2] = delta
        inputs[:, :, 2] = 100 - step * 0.5
        positions += np.tanh(inputs @ weights)
    return hits


def verify_evaluation(weights, starts, vent, hits):
    # Cross-check the batched evaluator against the original scalar movement rule.
    for i in range(min(3, len(weights))):
        for j, start in enumerate(starts[:12]):
            cell = ArtificialCell(start, weights=None)
            cell.weights = weights[i]
            expected = -1
            for step in range(200):
                if np.linalg.norm(vent - cell.position) < 15:
                    expected = step
                    break
                cell.act(vent)
            if expected != hits[i, j]:
                raise AssertionError((i, j, expected, hits[i, j]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    args = parser.parse_args()
    if args.epochs < 1 or len(set(args.seeds)) != len(args.seeds):
        parser.error("Choose a positive epoch count and distinct seeds.")
    args.output.mkdir(parents=True, exist_ok=False)
    starts = np.random.default_rng(20261125).uniform(0, 50, (96, 2))
    vent = np.array([25., 25.])
    outside = np.linalg.norm(starts - vent, axis=1) >= 15
    np.save(args.output / "starts.npy", starts)
    config = dict(python=platform.python_version(), numpy=np.__version__, training_seeds=args.seeds,
                  evaluation_seed=20261125, epochs=args.epochs, steps_per_epoch=200, starts=96,
                  outside_starts=int(outside.sum()), source_base="db28afb06bbaae807a7b9196e8525c3ee9f07964")
    (args.output / "protocol.json").write_text(json.dumps(config, indent=2))
    rows = []
    for seed in config["training_seeds"]:
        np.random.seed(seed)
        def snapshot(epoch, cells):
            weights = np.array([cell.weights for cell in cells]).reshape(-1, 3, 2)
            lineages = np.array([cell.lineage_id for cell in cells], dtype=int)
            np.savez_compressed(args.output / f"seed{seed}_epoch{epoch}.npz",
                                weights=weights, lineages=lineages)
            row = dict(seed=seed, epoch=epoch, cells=len(cells), lineages=len(set(lineages)),
                       largest_lineage_share=max(np.unique(lineages, return_counts=True)[1], default=0)
                       / max(1, len(cells)))
            if epoch in (0, 5, args.epochs) and cells:
                hits = evaluate(weights, starts, vent)
                state = np.random.get_state()
                try:
                    verify_evaluation(weights, starts, vent, hits)
                finally:
                    np.random.set_state(state)
                np.savez_compressed(args.output / f"hits_{seed}_{epoch}.npz", hits=hits)
                external = hits[:, outside]
                successes = external[external >= 0]
                row.update(reach_all=np.mean(hits >= 0), reach_outside=np.mean(external >= 0),
                           median_steps_outside_success=np.median(successes) if successes.size else None)
            rows.append(row)
        run_simulation(args.epochs, 200, snapshot=snapshot, plot=False)
    with (args.output / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
