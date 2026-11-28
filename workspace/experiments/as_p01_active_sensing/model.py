"""Matched-cost active sensing in a discrete, simulated environment."""
import numpy as np

POLICIES = ('fixed', 'random', 'information')
REGIMES = {'informative': np.array([[.9, .2], [.2, .9]]),
           'uninformative': np.full((2, 2), .55)}
TOL = 1e-12
JUNCTION = (0, 0)
LOCATIONS = ((-1, 0), (1, 0))
PATCHES = ((0, -4), (0, 4))


def entropy(p):
    p = np.asarray(p)
    q = 1-p
    return -(p*np.log2(np.where(p > 0, p, 1)) + q*np.log2(np.where(q > 0, q, 1)))


def update(p, likelihood, observation):
    l0, l1 = np.where(np.asarray(observation)[..., None], likelihood, 1-likelihood).T
    posterior = p*l1 / ((1-p)*l0+p*l1)
    return np.where(l0 == l1, p, posterior)


def information(p, likelihood):
    p = np.asarray(p)[..., None]
    predictive = (1-p)*likelihood[:, 0] + p*likelihood[:, 1]
    return entropy(p) - predictive*entropy(p*likelihood[:, 1]/predictive) - (
        1-predictive)*entropy(p*(1-likelihood[:, 1])/(1-predictive))


def schedule(seed, n):
    hidden, observations, random, ties, rewards = [
        np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(5)]
    return dict(hidden=hidden.permutation(np.repeat([0, 1], n//2)),
                observation_draws=observations.random((n, 3, 2)),
                random_sides=random.integers(0, 2, (n, 3)),
                tie_sides=ties.integers(0, 2, (n, 4)),
                reward_draws=rewards.random((n, 2)))


def choose(policy, belief, likelihood, visit, fixed, random_side, tie):
    if policy == 'fixed':
        return fixed ^ (visit % 2)
    if policy == 'random':
        return random_side
    gain = information(belief, likelihood)
    difference = gain[:, 1]-gain[:, 0]
    return np.where(abs(difference)<=TOL, tie, difference>0).astype(int)


def run(draws, regime, policy):
    h = draws['hidden']
    n = len(h)
    idx = np.arange(n)
    likelihood = REGIMES[regime]
    potentials = draws['observation_draws'] < likelihood[:, h].T[:, None, :]
    rewards = draws['reward_draws'] < np.where(h[:, None]==[0, 1], .85, .15)
    beliefs = np.full((n, 4), .5)
    locations = np.empty((n, 3), dtype=int)
    observations = np.empty((n, 3), dtype=bool)
    energy = [np.full(n, 16.)]
    position = [np.zeros((n, 2), dtype=int)]

    def event(where, delta):
        position.append(np.broadcast_to(where, (n, 2)))
        energy.append(energy[-1]+delta)

    for t in range(3):
        side = choose(policy, beliefs[:, t], likelihood, t, idx % 2,
                      draws['random_sides'][:, t], draws['tie_sides'][:, t])
        locations[:, t] = side
        observations[:, t] = potentials[idx, t, side]
        event(np.asarray(LOCATIONS)[side], -.5)
        event(position[-1], -.25)
        beliefs[:, t+1] = update(beliefs[:, t], likelihood[side], observations[:, t])
        event(JUNCTION, -.5)
    last = beliefs[:, -1]
    selected = np.where(abs(last-.5)<=TOL, draws['tie_sides'][:, 3], last>.5).astype(int)
    realised = rewards[idx, selected]
    direction = np.asarray(PATCHES)[selected] // 4
    for step in range(1, 5):
        event(direction*step, -.5)
    event(position[-1], 8*realised)
    for step in range(3, -1, -1):
        event(direction*step, -.5)
    return dict(potential_observations=potentials, potential_rewards=rewards,
                locations=locations, observations=observations, beliefs=beliefs,
                selected=selected, realised=realised, energy=np.stack(energy, axis=1),
                positions=np.stack(position, axis=1))
