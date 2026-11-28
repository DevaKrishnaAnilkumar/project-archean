import unittest
import numpy as np
from audit import reconstruct
from model import SETTINGS, feedback, schedule, simulate
from analysis import measures


class LifetimeTests(unittest.TestCase):
    def test_schedule_balance_and_replay(self):
        s=schedule(3490)
        for k,v in schedule(3490).items():
            np.testing.assert_array_equal(s[k],v)
        np.testing.assert_array_equal(np.bincount(s['initial_mapping']),[16,16])
        np.testing.assert_array_equal(np.bincount(s['fixed']),[16,16])

    def test_bayesian_feedback(self):
        p=np.array([.5,.5,.5,.5])
        obs=np.array([1,1,0,0])
        patch=np.array([1,1,1,1])
        got=np.array([True,False,True,False])
        expected=[]
        for match,reward in zip(obs==patch,got):
            r=.15+.70*(.85 if match else .15)
            a=r if reward else 1-r
            expected.append(a/(a+.5))
        np.testing.assert_allclose(feedback(p,1,obs,patch,got,.85),expected,rtol=0,atol=1e-12)

    def test_permanent_death_and_abstention_maintenance(self):
        s=schedule(3490)
        condition=(('stable',3,.85,5),)
        d=simulate(s,condition)
        np.testing.assert_array_equal(d['energy'][:3,0,4,0],[32,16,0])
        np.testing.assert_array_equal(d['energy'][3:],0)
        np.testing.assert_array_equal(d['patch'],-1)
        np.testing.assert_array_equal(d['site'],-1)
        np.testing.assert_array_equal(d['memory'][:,0,4],.5)
        reconstruct(s,d,condition)

    def test_reward_precedes_return_and_fatal_debits(self):
        s=schedule(3491)
        s['reward_draws'][0,:16]=0.
        s['reward_draws'][0,16:]=.99
        condition=(('stable',5,.85,40),)
        d=simulate(s,condition)
        np.testing.assert_array_equal(d['energy'][0,0,0,:16],128)
        np.testing.assert_array_equal(d['energy'][:,0,0,16:],0)
        np.testing.assert_array_equal(d['return_steps'][0,0,0],4)
        np.testing.assert_array_equal(d['return_steps'][1:,0,0,16:],0)
        reconstruct(s,d,condition)

    def test_counterfactual_hidden_state_cannot_change_ordinary_actions(self):
        s=schedule(3490)
        conditions=(('stable',512,.85,5),)
        original=simulate(s,conditions)
        # Force identical observations and rewards along the learner's recorded path.
        altered={**s,'hidden':1-s['hidden'],'initial_mapping':1-s['initial_mapping'],
                 'potential':1-s['potential'],'reward_draws':1-s['reward_draws']}
        for t in range(48):
            for j in range(32):
                site=original['site'][t,0,4,j]
                obs=original['obs'][t,0,4,j]
                patch=original['patch'][t,0,4,j]
                got=original['acquired'][t,0,4,j]
                altered['potential'][t,j,site]=0 if obs==altered['hidden'][t,j] else .999
                altered['reward_draws'][t,j,patch]=0 if got else .999
        counterfactual=simulate(altered,conditions)
        for k,v in original.items():
            np.testing.assert_array_equal(v[:,0,4],counterfactual[k][:,0,4])

    def test_frozen_oracle_and_null_controls(self):
        s=schedule(3491)
        d=simulate(s)
        reconstruct(s,d)
        np.testing.assert_array_equal(d['memory'][:,:,1:3],.5)
        np.testing.assert_array_equal(d['site'][:,0,5][d['site'][:,0,5]>=0],
                                      d['prior'][:,0,5][d['site'][:,0,5]>=0])
        np.testing.assert_array_equal(d['memory'][:,-2:,1:5],.5)
        for array in ('patch','acquired','energy'):
            for p in range(2,6):
                np.testing.assert_array_equal(d[array][:,-2:,p],d[array][:,-2:,1])
        self.assertTrue(np.all(d['energy'][:,[i for i,c in enumerate(SETTINGS) if c[1]==512]]>0))

    def test_energy_conservation(self):
        s=schedule(3490)
        d=simulate(s)
        v,_=measures(s,d)
        # Fatal debit may exceed available reserves. Equality is exact in no-death settings.
        idx=[i for i,c in enumerate(SETTINGS) if c[1]==512]
        np.testing.assert_allclose(v[idx,:,8],512+8*v[idx,:,7]-v[idx,:,9]-v[idx,:,10]-v[idx,:,11],atol=1e-12,rtol=0)
