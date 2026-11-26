import unittest
import numpy as np
from inherited_experience import FAMILIES, replicate


class InheritanceTests(unittest.TestCase):
    def test_pairing_and_first_choice(self):
        for seed in (0, 11):
            metrics, raw = replicate(seed)
            self.assertTrue(np.all(raw['donor'] != np.arange(FAMILIES)))
            for memory in ('parent', 'blank', 'donor'):
                np.testing.assert_array_equal(raw[f'stable_{memory}_actions'][0],
                                              raw[f'reversed_{memory}_actions'][0])
            self.assertAlmostEqual(metrics['stable_parent_first'] + metrics['reversed_parent_first'], 1.)

    def test_energy_schedule_and_withdrawal(self):
        _, raw = replicate(3)
        np.testing.assert_array_equal(raw['responsive_outcomes'], raw['replay_outcomes'])
        np.testing.assert_array_equal(raw['continued_actions'][0], raw['withdrawn_actions'][0])
        self.assertFalse(raw['withdrawn_outcomes'].any())
        self.assertFalse(np.array_equal(raw['responsive_actions'], raw['replay_actions']))

    def test_archived_seed_replays(self):
        from pathlib import Path
        for seed in range(40):
            _, raw = replicate(seed)
            path = Path(__file__).parent / 'inheritance_results' / f'seed_{seed:02}.npz'
            with np.load(path, allow_pickle=False) as stored:
                self.assertEqual(set(raw), set(stored.files))
                for key in stored.files:
                    np.testing.assert_array_equal(raw[key], stored[key])
