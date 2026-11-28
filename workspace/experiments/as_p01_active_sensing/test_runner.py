import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from audit_results import audit
from run_pilot import run_study


class RunnerTests(unittest.TestCase):
    def test_smoke_reconstruction_and_no_overwrite(self):
        with TemporaryDirectory() as temp:
            output=Path(temp)/'smoke'
            run_study(output,False)
            self.assertEqual(audit(output)['condition_assigned_episodes'],96)
            manifest=json.loads((output/'manifest.json').read_text())
            self.assertEqual(manifest['seeds'],[3090,3091])
            with self.assertRaises(FileExistsError):
                run_study(output,False)

    def test_checkpoint_required(self):
        with TemporaryDirectory() as temp:
            output=Path(temp)/'pilot'
            with self.assertRaises(ValueError):
                run_study(output,True,None)
            self.assertFalse(output.exists())
