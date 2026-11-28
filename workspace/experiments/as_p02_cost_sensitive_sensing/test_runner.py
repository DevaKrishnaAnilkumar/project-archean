from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from audit_results import audit
from run_pilot import execute


class RunnerTests(unittest.TestCase):
    def test_smoke_roundtrip_and_no_overwrite(self):
        with TemporaryDirectory() as temp:
            out=Path(temp)/'smoke'
            execute(out,False)
            self.assertEqual(audit(out)['episodes'],480)
            with self.assertRaises(FileExistsError):
                execute(out,False)

    def test_pilot_requires_clean_checkpoint(self):
        with TemporaryDirectory() as temp, patch.dict('os.environ',{'AS_P02_IMPLEMENTATION':'wrong'}):
            out=Path(temp)/'pilot'
            with self.assertRaises(ValueError):
                execute(out,True)
            self.assertFalse(out.exists())
