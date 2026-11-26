import unittest

import numpy as np

from archean_simulation import ArtificialCell
from local_sensing import batch_receptors, evaluate, receptors, trials


class LocalSensingTest(unittest.TestCase):
    def test_probe_readings_match_four_field_samples(self):
        vent = np.array([13., 29.])
        for point in (vent, vent + [3., -18.], vent + [-36., 9.]):
            def field(offset):
                return 400 * np.exp(-np.sum((point + offset - vent)**2) / 800)
            expected = [field([1, 0]) - field([-1, 0]), field([0, 1]) - field([0, -1])]
            np.testing.assert_allclose(receptors(point, vent), expected, atol=1e-12)
            np.testing.assert_allclose(batch_receptors(vent-point), expected, atol=1e-12)

    def test_local_hits_match_original_cell_dynamics(self):
        starts, vents = trials()
        weights = np.random.default_rng(44).uniform(-1, 1, (4, 3, 2))
        actual = evaluate(weights, starts, vents, "local")
        for i, controller in enumerate(weights):
            for j in range(0, len(starts), 5):
                cell = ArtificialCell(starts[j])
                cell.weights = controller
                first = -1
                for step in range(200):
                    if np.linalg.norm(vents[j] - cell.position) < 15:
                        first = step
                        break
                    cell.act(vents[j], receptors)
                self.assertEqual(first, actual[i, j])
