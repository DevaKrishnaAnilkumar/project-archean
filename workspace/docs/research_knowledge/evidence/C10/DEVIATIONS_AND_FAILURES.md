# Pre-evaluation validation record
- Initial C++ compile failed under -Werror (conditional expression narrowing and misleading indentation); fixed before smoke. Explicit L then S crossover RNG order set before smoke. No evaluation access, protocol unchanged.
- C09 integration tooling first hit a syntax error and then a path validation issue due to stripping git status whitespace. Corrected and independently verified documentation-only changes before committing; no source or result changes.
- Environment here Python 3.13.5 instead of previous Codex Python 3.12.14, Linux x86_64, NumPy 2.3.5, Matplotlib 3.10.8, GCC 14.2.0. Historical tests run before evaluation.

- Raw evidence packing call timed out during part 2 verification; completed archive independently reopened and all 6336 original member hashes reconstructed and compared against source bytes. Part 1 verification had completed before timeout. No raw evidence or results changed.
