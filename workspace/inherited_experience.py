"""Run the paired artificial-life companion assays with python inherited_experience.py NEW_DIR."""
import argparse
import csv
from pathlib import Path

import numpy as np

FAMILIES, STEPS = 64, 24
IDS = np.arange(FAMILIES)


def draw_schedule(rng):
    return rng.random((STEPS, FAMILIES, 5))


def choices(memory, draws, price, payout, explore=True):
    difference = payout * (memory[:, 1] - memory[:, 0]) - price
    action = np.where(difference == 0, draws[:, 0] < .5, difference > 0)
    if explore:
        action = np.where(draws[:, 1] < .2, draws[:, 2] < .5, action)
    return action.astype(int)


def encounters(initial, draws, probabilities, price=0., payout=3., replay=None):
    memory = initial.copy()
    actions, outcomes = [], []
    for t, random in enumerate(draws):
        action = choices(memory, random, price, payout)
        pulse = (random[IDS, 3 + action] < probabilities[IDS, action]
                 if replay is None else replay[t])
        memory[IDS, action] += .3 * (pulse - memory[IDS, action])
        actions.append(action)
        outcomes.append(pulse)
    return np.array(actions), np.array(outcomes), memory


def replicate(seed):
    rng = np.random.default_rng(seed)
    blank = np.full((FAMILIES, 2), .5)
    order = rng.permutation(FAMILIES)
    donor = np.empty_like(order)
    donor[order] = np.roll(order, 1)
    good = rng.permutation(IDS) % 2
    food = np.where(np.arange(2) == good[:, None], .85, .15)
    control = np.broadcast_to([.05, .85], blank.shape)
    raw = dict(donor=donor, good=good)
    metrics = {}

    def record(label, actions, rewards, target):
        raw[label + '_actions'] = actions
        raw[label + '_outcomes'] = rewards
        for window, selected in [('first', actions[:1]), ('last8', actions[-8:])]:
            metrics[label + '_' + window] = (selected == target).mean()

    train = draw_schedule(rng)
    acts, rewards, parent = encounters(blank, train, food)
    record('parent_food', acts, rewards, good)
    raw['parent_food_memory'] = parent
    offspring = draw_schedule(rng)
    for world, target in [('stable', good), ('reversed', 1-good)]:
        probs = food if world == 'stable' else food[:, ::-1]
        for name, memory in [('parent', parent), ('blank', blank), ('donor', parent[donor])]:
            label = world + '_' + name
            acts, rewards, _ = encounters(memory, offspring, probs)
            record(label, acts, rewards, target)
            metrics[label + '_net'] = (3 * rewards.sum(axis=0) - STEPS).mean()

    def signal(label, memory, draws, schedule=None):
        acts, pulses, final = encounters(memory, draws, control, price=1, payout=4, replay=schedule)
        record(label, acts, pulses, 1)
        metrics[label + '_net'] = (4*pulses.sum(axis=0) - acts.sum(axis=0)).mean()
        return pulses, final

    schedule, responsive = signal('responsive', blank, draw_schedule(rng))
    signal('replay', blank, draw_schedule(rng), schedule)
    test = draw_schedule(rng)
    signal('continued', responsive, test)
    signal('withdrawn', responsive, test, np.zeros_like(schedule))
    # Use an independent family's responsive timeline as the exogenous broadcast.
    for name, memory in [('parent', responsive), ('blank', blank), ('donor', responsive[donor])]:
        signal('child_replay_' + name, memory, test, schedule[:, donor])
        metrics['last_unit_' + name] = choices(memory, test[0], 1, 4, explore=False).mean()

    actual = np.where(rng.permutation(IDS) % 2, 2., .5)
    offer = rng.uniform(.55, 1.95, FAMILIES)
    raw.update(cost=actual, offer=offer, responsive_memory=responsive)
    # One forced calibration move, then the same new offer for each matched learner.
    observed_cost = 10 - (10 - actual)
    for name, estimate in [('own', observed_cost), ('shuffled', observed_cost[donor]),
                           ('fixed', np.ones(FAMILIES))]:
        move = offer > estimate
        metrics['cost_' + name + '_mae'] = np.abs(actual-estimate).mean()
        metrics['cost_' + name + '_gain'] = np.mean(move * (offer-actual))
    return metrics, raw


def main(directory):
    directory.mkdir(parents=True, exist_ok=False)
    with (directory / 'per_seed.csv').open('w', newline='') as f:
        for seed in range(40):
            metrics, raw = replicate(seed)
            if seed == 0:
                writer = csv.DictWriter(f, fieldnames=['seed', *metrics], lineterminator='\n')
                writer.writeheader()
            writer.writerow(dict(seed=seed, **metrics))
            np.savez_compressed(directory / f'seed_{seed:02}.npz', **raw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    main(parser.parse_args().directory)
