import unittest
import numpy as np
from audit_results import reconstruct
from exact_analysis import COSTS, LIKELIHOODS, POLICIES, outcomes, theory, Q
from model import schedule, simulate, updates


class ModelTests(unittest.TestCase):
    def test_updates_match_exact_outcome_enumeration(self):
        for p in [Q(1,2),Q(1,10),Q(4,5)]:
            sites=LIKELIHOODS['informative']
            on,yes,no=updates(float(p),np.asarray(sites,float))
            for a,l in enumerate(sites):
                ((weight,y),(_,z))=outcomes(p,l)
                np.testing.assert_allclose([on[a],yes[a],no[a]],[float(weight),float(y),float(z)],rtol=0,atol=1e-12)

    def test_all_policy_actions_and_energy(self):
        draws=schedule(3190,8)
        for regime,plans in theory().items():
            for cost,plan in plans.items():
                for policy in POLICIES:
                    raw=simulate(draws,regime,cost,policy,plan)
                    reconstructed=reconstruct(draws,raw,regime,cost,policy,plan)
                    self.assertLessEqual(reconstructed['visits'].max(),3)
                    self.assertGreaterEqual(plan['policies'][policy]['optimality_gap'],0)

    def test_hidden_state_and_unseen_outcomes_do_not_change_actions(self):
        draws=schedule(3191,8)
        plan=theory()['informative']['low']
        for policy in POLICIES:
            raw=simulate(draws,'informative','low',policy,plan)
            alternate={**draws,'hidden':1-draws['hidden'],'rewards':1-draws['rewards'],
                       'observations':1-draws['observations']}
            for i,t in np.argwhere(raw['sides']>=0):
                alternate['observations'][i,t,raw['sides'][i,t]]=.0 if raw['observed'][i,t]==1 else .99
            other=simulate(alternate,'informative','low',policy,plan)
            for key in ('sides','belief','observed','patch'):
                np.testing.assert_array_equal(raw[key],other[key])

    def test_seed_replay(self):
        x,y=schedule(3190,8),schedule(3190,8)
        for k in x:
            np.testing.assert_array_equal(x[k],y[k])
