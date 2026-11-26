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
            path = Path(__file__).resolve().parents[1] / 'results' / 'inheritance' / f'seed_{seed:02}.npz'
            with np.load(path, allow_pickle=False) as stored:
                self.assertEqual(set(raw), set(stored.files))
                for key in stored.files:
                    actual = np.asarray(raw[key])
                    expected = stored[key]

                    self.assertEqual(actual.shape, expected.shape)
                    self.assertEqual(actual.dtype, expected.dtype)

                    if key == 'offer':
                        self.assertEqual(actual.dtype, np.dtype('float64'))
                        self.assertTrue(np.isfinite(actual).all())
                        self.assertTrue(np.isfinite(expected).all())
                        np.testing.assert_allclose(
                            actual, expected,
                            rtol=0,
                            atol=2 * np.finfo(np.float64).eps,
                            equal_nan=False
                        )
                    else:
                        np.testing.assert_array_equal(actual, expected)


    def test_archived_summary_metrics(self):
        import csv
        from pathlib import Path

        path = (
            Path(__file__).resolve().parents[1]
            / 'results' / 'inheritance' / 'per_seed.csv'
        )

        with path.open() as f:
            rows = list(csv.DictReader(f))

        self.assertEqual(len(rows), 40)

        checked = 0
        for seed, row in enumerate(rows):
            self.assertEqual(int(row['seed']), seed)
            metrics, _ = replicate(seed)
            self.assertEqual(set(metrics), set(row) - {'seed'})

            for key, value in metrics.items():
                np.testing.assert_allclose(
                    value, float(row[key]),
                    rtol=0, atol=1e-12,
                    equal_nan=False,
                    err_msg=f'Seed {seed}: {key}'
                )
                checked += 1

        self.assertEqual(checked, 2000)
