import unittest
import numpy as np
from fractions import Fraction as Q
from audit import reconstruct
from model import compile_plan,debit,schedule,simulate
from theory import solve,terminal,transition,utility,POLICIES


class MortalityTests(unittest.TestCase):
    def test_terminal_boundaries(self):
        self.assertEqual(terminal(Q(1,2),32,'task_first')[0],0)
        self.assertEqual(terminal(Q(1,2),64,'survival_first')[0],0)
        self.assertEqual(terminal(Q(1,2),65,'task_first')[1][:2],(1,1))

    def test_fatal_debit_is_absorbing(self):
        energy=np.array([8,4])
        alive=np.ones(2,bool)
        spent=np.zeros(2,int)
        debit(energy,alive,spent,np.ones(2,bool),8)
        debit(energy,alive,spent,np.ones(2,bool),8)
        np.testing.assert_array_equal(energy,0)
        np.testing.assert_array_equal(alive,False)
        np.testing.assert_array_equal(spent,8)

    def test_reward_credited_before_return_and_unaffordable_sensing(self):
        s=schedule(3390,8)
        s['reward'][:4]=0
        s['reward'][4:]=.99
        plan=compile_plan(solve(4,4,1,'task_first'))
        raw=simulate(s,4,plan)
        np.testing.assert_array_equal(raw[0],-1)
        np.testing.assert_array_equal(raw[3],4)
        np.testing.assert_array_equal(raw[4][:,:4],128)
        np.testing.assert_array_equal(raw[4][:,4:],0)
        reconstruct(s,4,plan,raw)
        plan=compile_plan(solve(4,4,1,'survival_first'))
        raw=simulate(s,4,plan)
        np.testing.assert_array_equal(raw[1],-1)
        np.testing.assert_array_equal(raw[4],64)
        reconstruct(s,4,plan,raw)

    def test_abstention_at_two_and_guaranteed_return_at_eight(self):
        s=schedule(3391,8)
        s['reward'][:]=.99
        for e,patch,ending in ((2,-1,32),(8,None,64)):
            plan=compile_plan(solve(e,4,0,'task_first'))
            d=simulate(s,e,plan)
            # No-sensing policy.
            if patch is not None:
                np.testing.assert_array_equal(d[1][0],patch)
            else:
                self.assertTrue((d[1][0]>=0).all())
            np.testing.assert_array_equal(d[4][0],ending)
            reconstruct(s,e,plan,d)

    def test_exact_transition(self):
        self.assertEqual(transition(Q(1,2),(Q(9,10),Q(1,5)),1),(Q(11,20),Q(2,11)))
        self.assertEqual(transition(Q(3,7),(Q(11,20),)*2,0),(Q(9,20),Q(3,7)))

    def test_matching_and_optimality(self):
        s=schedule(3390,8)
        for k,v in schedule(3390,8).items():
            np.testing.assert_array_equal(s[k],v)
        for e in (4,8,64):
            for objective in ('task_first','survival_first'):
                p=compile_plan(solve(e,1,0,objective))
                reconstruct(s,e,p,simulate(s,e,p))
                self.assertTrue(all(utility(p['values']['adaptive'],objective)>=utility(p['values'][k],objective) for k in POLICIES))

    def test_high_energy_c05_regression(self):
        import sys
        from pathlib import Path
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'as_p02_sensitivity'))
        from theory import solve as c06
        import importlib.util
        spec=importlib.util.spec_from_file_location('c05_theory',str(Path(__file__).resolve().parents[1]/'as_p02_sensitivity/theory.py'))
        reference=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reference)
        for r in (0,.5,1):
            for c in (0,.25,.5,1,2,4):
                values=reference.solve(c,3,r)[-1]
                for objective in ('task_first','survival_first'):
                    v=c06(64,c,r,objective)['values']
                    self.assertEqual(v['myopic'][:2],(1,1))
                    self.assertAlmostEqual(float(v['myopic'][2])-64,values['cost_sensitive']['expected_net'],places=12)
                    self.assertAlmostEqual(float(v['adaptive'][2])-64,values['cost_sensitive']['optimal_net'],places=12)
