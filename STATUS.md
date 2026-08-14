# Status — Sharp Empirical Bernstein Bounds for Variance

## Current release

- Repository target: `MachineLearning-Nerd/icml26-sharp-empirical-bernstein-variance-bounds`
- Paper: *Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables*
- OpenReview: `oqkiE71wrC`
- arXiv: `2505.01987v2`
- Authors: Diego Martinez-Taboada and Aaditya Ramdas
- Evidence-release gate: **PASSED**
- Overall result: **VERIFIED_SCOPED**
- Strict paper-level gate: **NOT_READY**
- External score claimed: **no**

## Claim status

| Claim | Final status | Scope |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | 3,800 high-precision scalar conditional-multiplier cells over two switchable bounded laws |
| C2 | `VERIFIED_SCOPED` | 36 high-precision first-order sharpness cells; finite discrepancy and wrong-`ψ_E` control retained |
| C3 | `VERIFIED_SCOPED` | 960 high-precision non-collinear finite-dimensional Hilbert cells |

## Evidence boundary

The independent certificate supports the mechanism with exact high-precision finite-law checks and an asymptotic optimization route. It does not prove the universal confidence-sequence theorem, the asymptotic limit for every distribution, or the full separable-Hilbert theorem by finite enumeration.

The unmodified author protocol is pinned separately and its 14,700 released proposed-EB cells are audited as descriptive evidence. The proposed columns are finite and narrower than Maurer–Pontil in every released cell, while non-finite comparator entries are retained and reported.

## Branch hygiene

The final remote has one branch, `main`. The branch audit and release metadata are kept on that canonical branch.
