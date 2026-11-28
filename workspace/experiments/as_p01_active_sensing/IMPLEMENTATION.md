# Implementation

Each seed has five independent SeedSequence children. Fixed starting sides alternate by episode index, so each seed is balanced and observations cannot influence starting side. All policies use the same posterior update and final choice. Each trajectory records 14 movement events, three sensing events and one reward event. Energy and positions include the initial state. The runner validates its commit and a clean checkout before pilot execution. Results are written outside the source tree. Evaluation is limited to the declared seeds.
