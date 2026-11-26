import unittest
import numpy as np
from model import schedules, simulate, summarise, choose, ARMS, WORLDS, BUDGETS


def fixture(reward=True):
    s = schedules(101, 2)  # synthetic test seed, outside research range
    s['cue'][:] = 0
    s['mapping'][:] = 0
    s['blind'][:] = 1
    s['action_draw'][:] = .9  # ties choose patch 0; no exploration
    s['reward_draw'][:] = 0. if reward else .99
    return s


class SpatialLifetimeTests(unittest.TestCase):
    def test_schedule_balance_and_reproducibility(self):
        s = schedules(102)
        for k, v in schedules(102).items():
            np.testing.assert_array_equal(s[k], v)
        self.assertEqual(s['mapping'].sum(), 32)
        np.testing.assert_array_equal(s['cue'][:16].sum(axis=0), 8)
        np.testing.assert_array_equal(s['cue'][16:].sum(axis=0), 8)

    def test_choice_ties_exploration_and_greedy(self):
        q = np.array([[[.1,.9],[.5,.5]],[[.1,.9],[.5,.5]],[[.5,.5],[.5,.5]]])
        draws = np.array([[.9,.9,.9],[.9,.1,.9],[.1,.9,.9]])
        np.testing.assert_array_equal(choose(q,np.array([0,0,0]),draws),[1,0,1])

    def test_energy_and_memory(self):
        d = simulate(fixture(), 'adaptive', 'stable', 160)
        np.testing.assert_array_equal(d['energy'][1],164.)
        np.testing.assert_array_equal(d['energy'][-1],288.)
        np.testing.assert_allclose(d['memory'][1,:,0,0],.65)
        np.testing.assert_array_equal(d['memory'][1,:,1,:],.5)
        np.testing.assert_array_equal(d['memory'][1,:,0,1],.5)
        self.assertTrue(d['completed'].all())
        self.assertTrue(d['alive'].all())
        np.testing.assert_array_equal(d['position'],0)

    def test_frozen_and_blind(self):
        s = fixture()
        f = simulate(s,'frozen','stable',160)
        b = simulate(s,'cue_blind','stable',160)
        np.testing.assert_array_equal(f['memory'],.5)
        np.testing.assert_array_equal(b['memory'][:,:,0,:],.5)
        np.testing.assert_allclose(b['memory'][1,:,1,0],.65)

    def test_death_on_arrival_prevents_reward(self):
        d = simulate(fixture(), 'adaptive','stable',2)
        np.testing.assert_array_equal(d['death_step'][0],4)
        np.testing.assert_array_equal(d['reward'],-1)
        np.testing.assert_array_equal(d['action'][1:],-1)
        np.testing.assert_array_equal(d['memory'],.5)
        np.testing.assert_array_equal(d['energy'][1:],0.)
        np.testing.assert_array_equal(d['position'][1:],-4)
        self.assertFalse(d['completed'].any())

    def test_death_on_return_retains_observation(self):
        d = simulate(fixture(False),'adaptive','stable',3)
        np.testing.assert_array_equal(d['reward'][0],0)
        np.testing.assert_array_equal(d['death_step'][0],6)
        np.testing.assert_allclose(d['memory'][1,:,0,0],.35)
        np.testing.assert_array_equal(d['memory'][1:], np.broadcast_to(d['memory'][1],d['memory'][1:].shape))
        np.testing.assert_array_equal(d['position'][1:],-2)
        self.assertFalse(d['completed'].any())

    def test_no_reward_low_budget_and_denominators(self):
        d = simulate(fixture(False),'frozen','stable',24)
        np.testing.assert_array_equal(d['death_step'][5],8)
        self.assertTrue(d['completed'][:5].all())
        self.assertFalse(d['completed'][5:].any())
        row = summarise(d)
        self.assertEqual(row['all_choices'],12)
        self.assertEqual(row['survival'],0)
        self.assertEqual(row['mean_completed_trips'],5)
        self.assertTrue(np.isnan(row['late_acquisition_correct_conditional']))
        self.assertEqual(row['late_acquisition_correct_all'],0)

    def test_pairing_and_conservation(self):
        s = schedules(103)
        for arm in ARMS:
            for budget in BUDGETS:
                a = simulate(s,arm,'stable',budget)
                b = simulate(s,arm,'reversed',budget)
                for k in a:
                    stop = 17 if k in ('energy','position','alive','memory') else 16
                    np.testing.assert_array_equal(a[k][:stop],b[k][:stop],err_msg=k)
                np.testing.assert_array_equal(a['good'][16:],1-b['good'][16:])
                for d in (a,b):
                    expected = d['energy'][:-1] - .5*d['steps'] + 8*(d['reward']==1)
                    np.testing.assert_array_equal(d['energy'][1:], expected)
                    if budget == 160:
                        self.assertTrue(d['alive'].all())
                    self.assertTrue(np.all(d['action'][~d['alive'][:-1]] == -1))
                    self.assertTrue(np.all(d['position'][d['alive']] == 0))

if __name__ == '__main__':
    unittest.main()
