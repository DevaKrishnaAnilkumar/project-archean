# AS-P02 implementation

Exact expectations use rational transition probabilities and rewards. Entropy terms use floating-point logarithms. The simulator receives the exact fixed sequence and random visit count before generating a seed block. Each independent seed provides five named random streams and shares one schedule across all thirty conditions.

Raw trajectories include padded no-movement events when observation visits are skipped. Sides and observations use -1 for skipped visits. The common resource decision uses the fourth tie draw. Position and energy include the initial state and the full outward, reward, and return sequence. Observation sequences encode absent, A, and B as base-three digits 0, 1, and 2.

The audit independently reconstructs choices, posterior odds, exact movement events, costs and episode metrics from archived arrays. Aggregation reuses the reporting function on independently reconstructed seed metrics. The simulation and benchmark compare expected energy at population level as specified in the analysis plan.
