# Inherited experience and perceived control

This companion assay isolates decisions in discrete encounters. The spatial v2.1 populations motivate the question. Agents in this assay share a designed learning rule; neither the rule nor its transmission evolves. All energy values are simulation units.

## Protocol fixed before running

Use seeds 0–39, each with 64 parent families, two equiprobable cues, and 24 encounters per lifetime. Training memories start at 0.5 for both actions. Update the selected cue estimate toward the observed binary outcome with learning rate 0.3. Choose greedily with 20% exploration and random tie breaking. Outcomes have probabilities 0.85 and 0.15. Use identical random decisions and potential outcomes for the three matched offspring conditions. Copy the parent's memory, use a blank memory, or copy a different randomly assigned parent from the same replicate. Balance the rewarding parental cue within each seed and reverse it for every family in the reversed condition. Primary endpoint is first choice before feedback. Secondary endpoints are accuracy in the last eight choices and net energy (three units per reward, one spent per action).

For the intervention assay each family uses the same adaptive rule to estimate pulse probabilities after waiting and signalling. Signals cost one unit and each pulse pays four. The responsive world delivers pulses with probability 0.85 after a signal and 0.05 otherwise. A second independent agent receives exactly the first agent's pulse schedule regardless of action. Measure final-eight signal rates in both. For withdrawal, copy the responsive parent's memory into identical learners and compare continued response with disappearance of all pulses for 24 decisions. Also compare parental, unrelated and blank memory after responsive parents' offspring enter open-loop replay. Keep a separate, one-shot pre-feedback last-unit probe with no exploration. Energy is recorded for a fixed encounter horizon; the probe describes choice given a final spendable unit, not observed extinction or biological fear.

For the self-cost assay, double or halve movement cost for matched agents, while holding resource offers fixed. All agents observe the same calibration movement and realised cost, then predict their energy under a new offer. Compare their own retained cost with a shuffled peer's cost and a fixed default. Evaluate prediction error and net benefit of the chosen action. This tests the usefulness of a supplied internal estimate. It is not a consciousness test.

Average within each seed first, then weight seeds equally. Keep all outcomes, including negative effects. The held-out question for future work is whether natural selection favours mechanisms for copying, revising and using these estimates under resource costs.

## Findings

Forty independent seeds each generated 64 families (2,560 family histories). Each family contributed matched offspring to every condition.

| Starting memory | Stable first choice | Reversed first choice | Stable last eight | Reversed last eight |
|---|---:|---:|---:|---:|
| Own parent | 89.2% | 10.8% | 89.5% | 88.8% |
| Blank | 49.3% | 50.7% | 89.1% | 89.0% |
| Unrelated parent | 48.3% | 51.7% | 89.2% | 89.2% |

Parents began at 49.4% correct and reached 89.6% across their final eight encounters. The cumulative consequence of a stale memory persisted after behaviour recovered. Mean net energy with parental versus blank memory was 31.94 versus 30.17 units in stable conditions and 23.01 versus 30.02 following reversal.

Final-eight signal rates were 87.0% with responsive help and 29.1% with the identical pulse timeline on replay. Following withdrawal they fell to 10.2%, compared with 88.4% under continued response. Offspring entering replay signalled on 88.6% of first choices with responsive-parent memory versus 10.3% with blank memory; the final-eight rates were 33.6% and 27.9%. Unrelated parents in this assay all experienced the same responsive law and also transferred a strong initial signalling bias (88.7%). This control distinguishes shared training history from anything unique to family identity.

On the one-shot probe, 97.3% of responsive-parent offspring would spend one unit signalling, versus 0% with blank memory. The choice function uses expected net energy and has no variable for remaining reserves. This cannot establish heightened risk-taking when close to death. The agent can learn an action–outcome contingency without identifying an external causal source.

When the calibration observation fully revealed an agent's changed action cost, retaining its own observation yielded zero prediction error by construction. Mean net gains were 0.383 units with its own estimate, 0.011 with a shuffled estimate and 0.170 using a default cost. This is a positive control for state information. The fixed cost predictor has fewer active parameters; shuffled cost is the matched-capacity comparison.

## Reproduce

Run `python inherited_experience.py new_results` and `python -m unittest -q`. Each seed archive records trial actions and outcomes, cue mappings, donor identities and cost-probe inputs. The CSV reports seed-level endpoints. The paired design makes first choices complementary under cue reversal and identical across continued response and withdrawal before any feedback.

## Interpretation and remaining research

The assay shows causal effects of passing a particular acquired state via a deliberately implemented channel. It measures neither spontaneous evolution of that channel nor subjective experience. The separate spatial simulation still uses fixed lifetime controllers. Extending its reproduction dynamics to compare costly transmission, individual longevity and surviving descendants, and testing predictive models on held-out ecologies, remain open research questions.
