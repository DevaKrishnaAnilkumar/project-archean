"""Independent reconstruction from active and passive event ledgers."""
import argparse
import csv
from pathlib import Path

import numpy as np

ACTION = np.dtype([
    ("t", "<u2"), ("id", "<u2"), ("before", "<i2"), ("after", "<i2"),
    ("hidden", "i1"), ("site", "i1"), ("obs", "i1"), ("patch", "i1"),
    ("got", "u1"), ("returns", "u1"), ("prior", "<f8"), ("belief", "<f8"),
])
EVENT = np.dtype([("t", "<u2"), ("id", "<u2"), ("parent", "<u2"), ("gt", "u1")])
PASSIVE = np.dtype([("id", "<u2"), ("parent", "<u2"), ("gt", "u1")])
N, CAP, FOUNDERS, DEAD = 240, 120, 60, 65535
MASK = (1 << 64) - 1


def mix(value):
    value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & MASK
    value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & MASK
    return value ^ (value >> 31)


def draws(seed, stream, key=0, replay=0):
    state = mix(seed) ^ mix(stream + 0x7fa56e1) ^ mix(key + 0x8b89e11) ^ mix(replay + 0x50ab921)
    while True:
        state = (state + 0x9e3779b97f4a7c15) & MASK
        yield mix(state)


def uniform_index(draw_stream, size):
    threshold = (1 << 64) % size
    return next(value % size for value in draw_stream if value >= threshold)


def mutation(gt, draw_stream, probability):
    l, s = divmod(int(gt), 3)
    if (next(draw_stream) >> 11) * 2**-53 < probability:
        l = 1 - l
    if (next(draw_stream) >> 11) * 2**-53 < probability:
        s = (s + 1 + uniform_index(draw_stream, 2)) % 3
    return l * 3 + s


def roster(founders, ledger, times, audit_parent=True):
    births = ledger["parent"] != DEAD
    new, dead = ledger[births], ledger[~births]
    size = FOUNDERS + len(new)
    assert np.array_equal(new["id"], np.arange(FOUNDERS, size))
    assert np.all(ledger["id"] < size)
    assert len(np.unique(dead["id"])) == len(dead)
    assert np.all(ledger["gt"] < 6)
    birth_times = np.full(size, -1, dtype=int)
    birth_times[FOUNDERS:] = times[births]
    death_times = np.full(size, N, dtype=int)
    death_times[dead["id"]] = times[~births]
    assert np.all(birth_times < death_times)
    gt = np.r_[founders, new["gt"]]
    assert np.array_equal(gt[dead["id"]], dead["gt"])
    # Births occur after active deaths at a time. A passive newborn can parent
    # another passive birth in the same period if its creation preceded it.
    parents = new["parent"]
    assert np.all(parents < new["id"])
    assert np.all(birth_times[parents] <= times[births])
    assert np.all(death_times[parents] > times[births])
    if audit_parent:
        assert np.all(birth_times[parents] < times[births])
    delta = np.zeros((N + 1, 6), dtype=int)
    np.add.at(delta, (np.maximum(0, birth_times), gt), 1)
    np.add.at(delta, (death_times, gt), -1)
    trace = delta.cumsum(axis=0)[:N]
    # Population counts alone can mask an invalid replacement, so retain IDs.
    assert np.all(trace >= 0) and np.all(trace.sum(axis=1) <= CAP)
    return gt, birth_times, death_times, trace


def replay_rng(founders, events, contents, seed, replay, probability):
    parents = draws(seed, 10, replay=replay)
    deaths = draws(seed, 11, replay=replay)
    mutants = draws(seed, 12, replay=replay)
    living = list(range(FOUNDERS))
    genotype = list(founders)
    for event, row in zip(events, contents, strict=True):
        if event["parent"] == DEAD:
            at = uniform_index(deaths, len(living))
            assert row["id"] == living[at]
            living[at] = living[-1]
            living.pop()
        else:
            parent = living[uniform_index(parents, len(living))]
            assert row["parent"] == parent
            # Mutation uses a fresh state from the dedicated passive stream.
            state = next(mutants)

            def child_draws(state):
                while True:
                    state = (state + 0x9e3779b97f4a7c15) & MASK
                    yield mix(state)

            genotype.append(mutation(genotype[parent], child_draws(state), probability))
            assert row["gt"] == genotype[-1]
            living.append(int(row["id"]))


def verify_world(path, row, check_rng):
    fixture, q = int(row["fixture"]), float(row["q"])
    fee, prize, overhead, seed = [int(row[key]) for key in ("fee_ticks", "reward_ticks", "overhead_ticks", "seed")]
    founder = np.fromfile(path / "founders.bin", "u1")
    map_trace = np.fromfile(path / "mapping.bin", "u1")
    actions = np.fromfile(path / "actions.bin", ACTION)
    events = np.fromfile(path / "events.bin", EVENT)
    assert np.array_equal(np.bincount(founder), np.full(6, 10))
    assert map_trace.shape == (N,) and np.all(map_trace < 2)
    map_rng = draws(seed, 1)
    initial = uniform_index(map_rng, 2)
    random_maps = np.array([uniform_index(map_rng, 2) for _ in range(N)])
    expected_maps = [np.full(N, initial), initial ^ (np.arange(N)//24 % 2), random_maps]
    assert np.array_equal(map_trace, expected_maps[int(row["regime"])])
    assert np.all(events["t"][1:] >= events["t"][:-1])
    gt, born, died, trace = roster(founder, events, events["t"])
    birthed = events[events["parent"] != DEAD]
    death_events = events[events["parent"] == DEAD]
    t, aid = actions["t"], actions["id"]
    assert len(np.unique(aid.astype("i8") * N + t)) == len(actions)
    assert np.all(t < N) and np.all(t > born[aid]) and np.all(t <= died[aid])
    exposure = np.minimum(died, N-1) - born
    assert np.array_equal(np.bincount(aid, minlength=len(gt)), exposure)
    assert np.array_equal(death_events["id"], aid[actions["after"] == 0])
    assert np.array_equal(death_events["t"], t[actions["after"] == 0])
    assert np.all(t[1:] >= t[:-1])

    order = np.lexsort((t, aid))
    sorted_actions = actions[order]
    sorted_ids = aid[order]
    first = t[order] == born[sorted_ids] + 1
    expected_energy = np.where(first, np.where(sorted_ids < FOUNDERS, 384, 192),
                               np.roll(sorted_actions["after"], 1))
    parent_key = birthed["parent"].astype("i8") * N + birthed["t"]
    action_key = sorted_ids.astype("i8") * N + t[order]
    assert len(np.unique(parent_key)) == len(parent_key)
    parent_rows = np.searchsorted(action_key, parent_key)
    assert np.array_equal(action_key[parent_rows], parent_key)
    assert np.all(sorted_actions["after"][parent_rows] >= 512)
    previous_key = action_key - 1
    expected_energy -= 208 * (~first & np.isin(previous_key, parent_key))
    assert np.array_equal(expected_energy, sorted_actions["before"])
    expected_previous = np.where(first, .5, np.roll(sorted_actions["belief"], 1))
    learning = gt[aid] >= 3
    maintenance = actions["before"] - 16 - learning.astype("i2") * overhead
    alive_after_maintenance = maintenance > 0
    sampled, attempted = actions["site"] >= 0, actions["patch"] >= 0
    assert np.all((actions["hidden"]>=0) == alive_after_maintenance)
    assert np.all(actions["hidden"]<=1) and np.all(actions["site"]<=1) and np.all(actions["patch"]<=1)
    assert np.all(actions["got"]<=1) and np.all(actions["returns"]<=4)
    assert np.array_equal(actions["obs"]>=0, sampled) and np.all(actions["obs"]<=1)
    assert np.all(~sampled | ((maintenance > fee+32) & (gt[aid]%3 > 0)))
    assert np.all(sampled | (maintenance <= fee+32) | (gt[aid]%3 != 2))
    assert np.array_equal(attempted, maintenance - fee*sampled > 32)
    assert np.all(attempted | (actions["got"]==0))
    if fixture in (2, 3):
        assert np.all(actions["got"][attempted] == fixture-2)
    after_reward = maintenance - fee*sampled - 32*attempted + prize*actions["got"]
    steps = np.where(attempted, np.minimum(4, (after_reward+7)//8), 0)
    assert np.array_equal(steps, actions["returns"])
    assert np.array_equal(np.maximum(0, after_reward-8*steps), actions["after"])
    learn_live = learning[order] & alive_after_maintenance[order]
    expected_prior = np.where(learn_live, .05+.9*expected_previous, expected_previous)
    assert np.allclose(sorted_actions["prior"], expected_prior, rtol=0, atol=1e-12)
    directed = sampled & (np.abs((q-.5)*(2*actions["prior"]-1)) > 1e-12)
    assert np.array_equal(actions["site"][directed], (actions["prior"][directed]>.5).astype("i1"))
    action_accuracy = .5+(q-.5)*np.where(actions["site"]==1, actions["prior"],1-actions["prior"])
    use_cue = sampled & (action_accuracy-.5 > 1e-12)
    assert np.array_equal(actions["patch"][use_cue], actions["obs"][use_cue])
    prior = actions["prior"]
    posterior = prior.copy()
    selected = sampled & learning
    cue, site, patch, got = [actions[name][selected] for name in ("obs","site","patch","got")]
    likelihoods = []
    for m in (0, 1):
        accuracy = np.where(site == m, q, .5)
        h0 = np.where(cue == 0, accuracy, 1-accuracy)
        h1 = 1-h0
        w0 = np.where((patch == 0) == got.astype(bool), .85, .15)
        likelihoods.append((h0*w0+h1*(1-w0))*.5)
    weighted = prior[selected]*likelihoods[1]
    posterior[selected] = weighted / ((1-prior[selected])*likelihoods[0]+weighted)
    assert np.allclose(posterior, actions["belief"], rtol=0, atol=1e-12)
    if q == .5:
        assert np.allclose(actions["belief"], .5, rtol=0, atol=1e-12)

    eligible = actions["after"] >= 512
    available = CAP-np.bincount(t[actions["after"]>0], minlength=N)
    eligible_count = np.bincount(t[eligible], minlength=N)
    birth_count = np.bincount(birthed["t"], minlength=N)
    if fixture != 1:
        assert np.array_equal(birth_count, np.minimum(available, eligible_count))
    else:
        assert not len(birthed)
    if fixture == 2:
        assert np.all(trace.sum(axis=1)[24:] == 0)
    if fixture == 3:
        assert np.any(trace.sum(axis=1) == CAP)
    probability = 0 if fixture == 0 else .02
    if check_rng:
        # Independently replay individual exogenous draws for an evenly spaced
        # deterministic sample of action rows from every audited world.
        for i in np.linspace(0, len(actions)-1, min(128, len(actions)), dtype=int):
            if not alive_after_maintenance[i]:
                continue
            key = int(t[i])*65536+int(aid[i])
            hidden = uniform_index(draws(seed, 3, key), 2)
            assert actions["hidden"][i] == hidden
            site_rng = draws(seed, 7, key)
            site_tie, patch_tie = (uniform_index(site_rng, 2) for _ in range(2))
            sample_draw = (next(draws(seed, 6, key)) >> 11)*2**-53
            assert sampled[i] == (maintenance[i] > fee+32 and sample_draw < (gt[aid[i]]%3)*.5)
            if sampled[i]:
                site = int(actions["site"][i])
                assert directed[i] or site == site_tie
                obs_draw = (next(draws(seed, 4, 2*key+site)) >> 11)*2**-53
                chance = q if site == map_trace[t[i]] else .5
                assert actions["obs"][i] == (hidden if obs_draw < chance else 1-hidden)
            if attempted[i]:
                patch = int(actions["patch"][i])
                assert use_cue[i] or patch == patch_tie
                reward_draw = (next(draws(seed, 5, 2*key+patch)) >> 11)*2**-53
                chance = .85 if patch == hidden else .15
                expected = int(reward_draw < chance) if fixture not in (2,3) else fixture-2
                assert actions["got"][i] == expected
        for period in np.flatnonzero(birth_count):
            ids = aid[eligible & (t==period)].tolist()
            rng = draws(seed, 9, int(period))
            for i in range(len(ids), 1, -1):
                j = uniform_index(rng, i)
                ids[i-1], ids[j] = ids[j], ids[i-1]
            matches = birthed[birthed["t"]==period]
            assert np.array_equal(matches["parent"], ids[:birth_count[period]])
            for b in matches:
                assert b["gt"] == mutation(gt[b["parent"]], draws(seed, 8, int(b["id"])), probability)
    elif fixture == 0:
        assert np.array_equal(gt[birthed["parent"]], birthed["gt"])

    passive_values, passive_traces = [], []
    for replay in range(8):
        contents = np.fromfile(path / f"passive{replay}.bin", PASSIVE)
        assert len(contents) == len(events)
        assert np.array_equal(events["parent"]==DEAD, contents["parent"]==DEAD)
        _, _, _, passive_trace = roster(founder, contents, events["t"], audit_parent=False)
        assert np.array_equal(passive_trace.sum(axis=1), trace.sum(axis=1))
        passive_values.append(passive_trace[:,4:].sum()/(CAP*N))
        passive_traces.append(passive_trace)
        if check_rng:
            replay_rng(founder, events, contents, seed, replay, probability)

    founder_line = np.full(len(gt), -1, dtype=int)
    founder_line[:FOUNDERS] = np.arange(FOUNDERS)
    for b in birthed:
        founder_line[b["id"]] = founder_line[b["parent"]]
    lineage = np.zeros((N+1, FOUNDERS), dtype=int)
    np.add.at(lineage, (np.maximum(0,born), founder_line), 1)
    np.add.at(lineage, (died, founder_line), -1)
    lineage = (lineage.cumsum(axis=0)[:N]>0).sum(axis=1)
    pop = trace.sum(axis=1)
    assert np.all(pop[np.flatnonzero(pop==0)[0]:]==0) if np.any(pop==0) else True
    margin = trace[:,4:].sum()/(CAP*N)
    info = {**row, "active":margin, "passive_mean":np.mean(passive_values), "delta":margin-np.mean(passive_values),
            "extinction":int(np.flatnonzero(pop==0)[0]) if np.any(pop==0) else N,
            "births":len(birthed), "deaths":len(death_events), "mean_population":pop.mean(),
            "final_population":pop[-1], "final_lineages":lineage[-1],
            "lineage_periods":lineage.sum(), "blocked_births":int((eligible_count-birth_count).sum()),
            "mut_l":int((gt[birthed["parent"]]//3 != birthed["gt"]//3).sum()),
            "mut_s":int((gt[birthed["parent"]]%3 != birthed["gt"]%3).sum())}
    for i, value in enumerate(passive_values):
        info[f"passive_{i}"] = value
    exposure_gt = gt[aid]
    for g in range(6):
        subset = exposure_gt == g
        counts = trace[:,g]
        endings = died[gt==g]
        info.update({
            f"periods_g{g}": int(counts.sum()), f"final_g{g}": int(counts[-1]),
            f"exposure_g{g}": int(subset.sum()), f"individuals_g{g}": int((gt==g).sum()),
            f"births_parent_g{g}": int((gt[birthed["parent"]]==g).sum()),
            f"offspring_g{g}": int((birthed["gt"]==g).sum()),
            f"censored_g{g}": int((endings==N).sum()),
            f"attempts_g{g}": int((subset&attempted).sum()),
            f"samples_g{g}": int((subset&sampled).sum()),
            f"correct_g{g}": int((subset&attempted&(actions["patch"]==actions["hidden"])).sum()),
            f"rewards_g{g}": int(actions["got"][subset].sum()),
            f"net_action_ticks_g{g}": int((actions["after"][subset]-actions["before"][subset]).sum()),
            f"overhead_ticks_g{g}": int(subset.sum()*overhead*(g>=3)),
            f"sensing_ticks_g{g}": int((subset&sampled).sum()*fee),
            f"mapping_brier_sum_g{g}": float(((prior[subset]-map_trace[t[subset]])**2).sum()),
        })
    transitions = np.bincount(6*gt[birthed["parent"]]+birthed["gt"], minlength=36)
    info.update({f"transition_{k//6}_{k%6}": int(value) for k, value in enumerate(transitions)})
    return info, np.column_stack((trace,lineage,np.sum(passive_traces,axis=0)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--rng", action="store_true")
    args = parser.parse_args()
    with (args.raw/"design.csv").open() as f:
        design = list(csv.DictReader(f))
    seen, stats, curves = set(), [], []
    for row in design:
        key = int(row["setting"]), int(row["seed"])
        assert key not in seen
        seen.add(key)
        try:
            summary, trace = verify_world(args.raw/row["path"], row, args.rng)
        except AssertionError as error:
            raise AssertionError(f"Audit failure in setting {key[0]}, seed {key[1]}") from error
        stats.append(summary)
        curves.append(trace)
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out/"worlds.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)
    np.save(args.out/"curves.npy", np.asarray(curves, dtype=np.int16))
    print(f"PASS {len(stats)} active worlds and {8*len(stats)} replay pedigrees. Exact tick accounting, demographic and genotype traces, Bayesian feedback and fixture conditions checked.")
    if args.rng:
        print("PASS independent seeded action draws sampled per world; reproduction order, mutations, and uniform passive selections replayed.")


if __name__ == "__main__":
    main()
