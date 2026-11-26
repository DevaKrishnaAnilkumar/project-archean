"""v2.3.1 fixed-locomotion lifetime learning; see PROTOCOL.md and IMPLEMENTATION.md."""
import numpy as np

SEEDS = tuple(range(2300, 2340))
ARMS = ('adaptive', 'frozen', 'cue_blind')
WORLDS = ('stable', 'reversed')
BUDGETS = (160, 24)
FAMILIES, TRIALS = 64, 32


def schedules(seed, n=FAMILIES):
    if n <= 0 or n % 2:
        raise ValueError('Balanced mapping requires an even positive cohort size')
    streams = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(5)]
    mapping = streams[0].permutation(np.repeat([0, 1], n // 2))
    cue = np.empty((TRIALS, n), dtype=np.int8)
    for phase in range(2):
        for i in range(n):
            cue[phase*16:(phase+1)*16, i] = streams[1].permutation(np.repeat([0, 1], 8))
    return dict(mapping=mapping, cue=cue,
                blind=streams[2].integers(0, 2, size=(TRIALS, n), dtype=np.int8),
                reward_draw=streams[3].random((TRIALS, n, 2)),
                action_draw=streams[4].random((TRIALS, n, 3)))


def choose(memory, observed, draws):
    q = memory[np.arange(len(observed)), observed]
    # Draws: tie-breaking, exploration gate, exploratory action.
    greedy = np.where(q[:, 0] == q[:, 1], draws[:, 0] < .5, q[:, 1] > q[:, 0])
    return np.where(draws[:, 1] < .2, draws[:, 2] < .5, greedy).astype(np.int8)


def simulate(s, arm, world, budget):
    if arm not in ARMS or world not in WORLDS or budget <= 0:
        raise ValueError('Invalid condition')
    n = len(s['mapping']); ids = np.arange(n)
    shape = (TRIALS, n)
    good = (s['cue'] ^ s['mapping'][None, :]).astype(np.int8)
    if world == 'reversed':
        good[16:] ^= 1
    observed = s['blind'] if arm == 'cue_blind' else s['cue']
    # Potential outcomes are indexed by patch, even for unchosen patches.
    probs = np.where(good[..., None] == np.arange(2), .85, .15)
    potential = s['reward_draw'] < probs
    energy = np.full(n, budget, dtype=float)
    pos = np.zeros(n, dtype=np.int8)
    alive = np.ones(n, dtype=bool)
    memory = np.full((n, 2, 2), .5)
    data = dict(good=good, observed=observed.copy(), potential=potential,
                action=np.full(shape, -1, dtype=np.int8),
                reward=np.full(shape, -1, dtype=np.int8),
                steps=np.zeros(shape, dtype=np.int8),
                death_step=np.zeros(shape, dtype=np.int8),
                completed=np.zeros(shape, dtype=bool),
                energy=np.empty((TRIALS+1,n)),
                position=np.empty((TRIALS+1,n), dtype=np.int8),
                alive=np.empty((TRIALS+1,n), dtype=bool),
                memory=np.empty((TRIALS+1,n,2,2)))
    def record(t):
        data['energy'][t] = energy; data['position'][t] = pos
        data['alive'][t] = alive; data['memory'][t] = memory
    record(0)
    for t in range(TRIALS):
        active = ids[alive]
        if len(active):
            assert np.all(pos[active] == 0)
            a = choose(memory[active], observed[t,active], s['action_draw'][t,active])
            data['action'][t,active] = a
            direction = np.where(a == 0, -1, 1)
            for step in range(1, 9):
                live = alive[active]
                moving = active[live]
                pos[moving] += direction[live] * (1 if step <= 4 else -1)
                energy[moving] = np.maximum(0., energy[moving] - .5)
                data['steps'][t,moving] += 1
                dead = moving[energy[moving] <= 0]
                alive[dead] = False
                data['death_step'][t,dead] = step
                if step == 4:
                    arrived = active[alive[active]]
                    chosen = data['action'][t,arrived]
                    reward = potential[t,arrived,chosen].astype(np.int8)
                    data['reward'][t,arrived] = reward
                    energy[arrived] += 8 * reward
                    if arm != 'frozen':
                        obs = observed[t,arrived]
                        old = memory[arrived,obs,chosen]
                        memory[arrived,obs,chosen] = old + .3 * (reward - old)
            data['completed'][t,active] = alive[active]
        record(t+1)
    return data


def summarise(d):
    chosen = d['action'] >= 0
    correct = chosen & (d['action'] == d['good'])
    reward = d['reward'] == 1
    n = chosen.shape[1]
    row = {}
    for label, start, end in [('late_acquisition',8,16),('early_reversal',16,20),('late_reversal',24,32),('all',0,32)]:
        denom = int(chosen[start:end].sum())
        count = int(correct[start:end].sum())
        row[label+'_correct_all'] = count / ((end-start)*n)
        row[label+'_correct_conditional'] = count / denom if denom else float('nan')
        row[label+'_choices'] = denom
    row.update(survival=float(d['alive'][-1].mean()), final_energy=float(d['energy'][-1].mean()),
               acquisition_rate=float(reward.mean()), mean_completed_trips=float(d['completed'].sum(axis=0).mean()))
    for t in range(TRIALS):
        denom = int(chosen[t].sum()); count = int(correct[t].sum())
        label = f'trial_{t+1:02}'
        row[label+'_correct_all'] = count/n
        row[label+'_correct_conditional'] = count/denom if denom else float('nan')
        row[label+'_choices'] = denom
    return row
