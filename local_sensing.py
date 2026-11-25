"""Paired local-sensing experiment. Run: python local_sensing.py NEW_DIRECTORY"""
import argparse
import csv
import math
from pathlib import Path

import numpy as np

from archean_simulation import run_simulation


def receptors(position, vent):
    """Opposing probes one unit from the cell on each global axis."""
    x, y = position - vent
    exp = math.exp
    return (400 * exp(-y*y/800) * (exp(-(x+1)**2/800) - exp(-(x-1)**2/800)),
            400 * exp(-x*x/800) * (exp(-(y+1)**2/800) - exp(-(y-1)**2/800)))


def batch_receptors(delta):
    x, y = -delta[..., 0], -delta[..., 1]
    exp = np.exp
    return np.stack((400 * exp(-y*y/800) * (exp(-(x+1)**2/800) - exp(-(x-1)**2/800)),
                     400 * exp(-x*x/800) * (exp(-(y+1)**2/800) - exp(-(y-1)**2/800))), axis=-1)


def trials():
    rng = np.random.default_rng(2100)
    starts, vents = [], []
    for vent in [[15, 15], [15, 35], [35, 15], [35, 35]]:
        candidates = rng.uniform(0, 50, (256, 2))
        outside = candidates[np.linalg.norm(candidates - vent, axis=1) >= 15][:24]
        starts.extend(outside)
        vents.extend([vent] * len(outside))
    return np.array(starts), np.array(vents)


def evaluate(weights, starts, vents, mode):
    positions = np.broadcast_to(starts, (len(weights), *starts.shape)).copy()
    hits = np.full(positions.shape[:2], -1, dtype=np.int16)
    rng = np.random.default_rng(2101)
    for step in range(200):
        delta = vents - positions
        reached = np.linalg.norm(delta, axis=-1) < 15
        hits[(hits < 0) & reached] = step
        if mode == "exact":
            cues = delta
        elif mode == "zero":
            cues = np.zeros_like(delta)
        else:
            cues = batch_receptors(delta)
            if mode == "shuffled":
                # Random cyclic shift in a freshly randomized trial order: no self-donors.
                order = rng.permutation(len(starts))
                cues[:, order] = cues[:, np.roll(order, 1)]
        inputs = np.empty((*hits.shape, 3))
        inputs[..., :2] = cues
        inputs[..., 2] = 100 - 0.5 * step
        positions += np.tanh(inputs @ weights)
    return hits


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    starts, vents = trials()
    np.savez(out / "trials.npz", starts=starts, vents=vents)
    np.testing.assert_allclose(batch_receptors(vents-starts),
                               [receptors(p, v) for p, v in zip(starts, vents)], atol=1e-12)
    rows = []
    for seed in range(6):
        for training in ("local", "exact"):
            np.random.seed(seed)

            def snapshot(epoch, cells):
                if epoch not in (0, 5) and cells:
                    return
                rng = np.random.default_rng(2200 + seed + epoch * 100)
                selected = rng.choice(len(cells), min(32, len(cells)), replace=False)
                weights = np.array([cells[i].weights for i in selected]).reshape(-1, 3, 2)
                data = dict(weights=weights, selected=selected)
                modes = ("local", "shuffled", "zero") if training == "local" else ("exact",)
                for mode in modes:
                    hits = evaluate(weights, starts, vents, mode)
                    data[mode] = hits
                    rows.append((seed, training, epoch, len(cells), len(set(c.lineage_id for c in cells)),
                                 mode, np.mean(hits >= 0) if hits.size else None))
                np.savez_compressed(out / f"{training}_{seed}_{epoch}.npz", **data)

            run_simulation(5, 200, snapshot=snapshot, plot=False,
                           sense=receptors if training == "local" else None)
    with (out / "summary.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("seed", "training", "epoch", "population", "lineages", "cue", "reach"))
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
