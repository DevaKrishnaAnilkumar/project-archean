import unittest
import numpy as np
from model import REGIMES, POLICIES, TOL, choose, entropy, information, run, schedule, update


class ModelTests(unittest.TestCase):
    def test_bayes(self):
        likelihood=REGIMES['informative'][0]
        self.assertAlmostEqual(float(update(.5,likelihood,1)),2/11)
        self.assertAlmostEqual(float(update(.5,likelihood,0)),8/9)

    def test_gain(self):
        likelihood=REGIMES['informative']
        for p in (.01,.2,.5,.8,.99):
            for loc,probs in enumerate(likelihood):
                terms=[]
                for v in (0,1):
                    l0,l1=probs if v else 1-probs
                    probability=(1-p)*l0+p*l1
                    terms.append(probability*entropy(p*l1/probability))
                self.assertAlmostEqual(information(p,likelihood)[loc],entropy(p)-sum(terms),places=12)
        gains=information(np.linspace(0,1,101),likelihood)
        self.assertTrue((gains>=-TOL).all())
        self.assertAlmostEqual(*information(.5,likelihood),places=12)
        prefer=np.argmax(information(np.array([.2,.8]),likelihood),axis=1)
        self.assertNotEqual(*prefer)

    def test_policies_use_only_visible_history(self):
        draws=schedule(3090,8)
        original=run(draws,'informative','information')
        altered={**draws,'hidden':1-draws['hidden'],'observation_draws':draws['observation_draws'].copy(),
                 'reward_draws':1-draws['reward_draws']}
        for i in range(8):
            for t in range(3):
                side=original['locations'][i,t]
                altered['observation_draws'][i,t,side]=.0 if original['observations'][i,t] else .99
                altered['observation_draws'][i,t,1-side]=1-draws['observation_draws'][i,t,1-side]
        counterfactual=run(altered,'informative','information')
        for k in ('locations','beliefs','selected'):
            np.testing.assert_array_equal(original[k],counterfactual[k])

    def test_control(self):
        draws=schedule(3091,8)
        first=run(draws,'uninformative','fixed')
        for policy in POLICIES:
            actual=run(draws,'uninformative',policy)
            for key in ('selected','realised','potential_rewards','potential_observations'):
                np.testing.assert_array_equal(first[key],actual[key])
            np.testing.assert_array_equal(actual['beliefs'],.5)
            np.testing.assert_array_equal(actual['energy'][:,-1],8.25+8*actual['realised'])
        np.testing.assert_allclose(information(.5,REGIMES['uninformative']),0,rtol=0,atol=TOL)

    def test_replay(self):
        for k,v in schedule(3090,8).items():
            np.testing.assert_array_equal(v,schedule(3090,8)[k])
