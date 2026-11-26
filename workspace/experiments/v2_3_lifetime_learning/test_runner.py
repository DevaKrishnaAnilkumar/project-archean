import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from model import SEEDS, ARMS, WORLDS, BUDGETS
from run_study import interval, primary, contrasts, run, SMOKE_SEEDS

class RunnerTests(unittest.TestCase):
    def test_interval(self):
        a=np.arange(40,dtype=float)/100
        r=interval(a)
        self.assertAlmostEqual(r['mean'],.195)
        self.assertAlmostEqual(r['lower_95'],.195-2.02269092*a.std(ddof=1)/np.sqrt(40))
        self.assertAlmostEqual(r['upper_95'],.195+2.02269092*a.std(ddof=1)/np.sqrt(40))
        self.assertEqual(interval(np.zeros(40))['lower_95'],0)
        with self.assertRaises(ValueError): interval(a[:39])
        a[0]=np.nan
        with self.assertRaises(ValueError): interval(a)

    def test_contrasts(self):
        rows={}
        for a in ARMS:
            for w in WORLDS:
                for b in BUDGETS:
                    rows[a,w,b]=dict(late_acquisition_correct_all=.75 if a=='adaptive' else .5,
                        early_reversal_correct_all=.25,late_reversal_correct_all=.5 if w=='reversed' else .75,
                        survival=.75 if a=='adaptive' else .5,final_energy=10 if a=='adaptive' else 5)
        self.assertEqual(primary(rows),.25)
        c=contrasts(rows)
        self.assertEqual(c['reversal_late_minus_early'],.25)
        self.assertEqual(c['reversal_late_minus_stable'],-.25)
        self.assertEqual(c['genuine_minus_blind_late_acquisition'],.25)
        self.assertEqual(c['stable_24_adaptive_minus_frozen_final_energy'],5)
        self.assertEqual(len(c),20)

    def test_smoke_output_and_no_overwrite(self):
        self.assertTrue(set(SEEDS).isdisjoint(SMOKE_SEEDS))
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'study'
            with patch('run_study.git',return_value=tmp+'/repository'):
                r=run(out,smoke=True)
                self.assertEqual(r,dict(mode='smoke',seed_count=2,condition_rows=24))
                with self.assertRaises(FileExistsError): run(out,smoke=True)
            m=json.loads((out/'manifest.json').read_text())
            self.assertEqual(m['seeds'],list(SMOKE_SEEDS))
            self.assertEqual(len(list((out/'raw').rglob('*.npz'))),26)
            self.assertEqual(json.loads((out/'COMPLETE.json').read_text())['raw_archives'],26)
            with np.load(out/'raw/101/schedules.npz',allow_pickle=False) as s:
                self.assertEqual(s['reward_draw'].shape,(32,4,2))
            with np.load(out/'raw/101/adaptive_stable_160.npz',allow_pickle=False) as d:
                self.assertEqual(d['memory'].shape,(33,4,2,2))
            with (out/'trial_aggregate.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),384)
            self.assertTrue(all(int(r['scheduled'])==8 for r in rows))
            self.assertTrue(all(float(r['correct_all'])==int(r['correct'])/8 for r in rows))
            with (out/'death_counts.csv').open() as f: self.assertEqual(len(list(csv.DictReader(f))),6144)

    def test_research_requires_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'study'
            with patch('run_study.research_checkpoint',return_value='verified'):
                with self.assertRaises(ValueError): run(out,smoke=False,checkpoint=None)
            self.assertFalse(out.exists())

if __name__=='__main__': unittest.main()
