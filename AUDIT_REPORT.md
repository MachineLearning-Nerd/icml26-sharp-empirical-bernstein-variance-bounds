# Reproduction audit report

## Executive result

The three-claim evidence-release gate is `PASSED`, with overall status `VERIFIED_SCOPED`. The strict paper-level gate is `NOT_READY` because finite high-precision certificates and released simulations do not replace universal proofs.

## Claim-to-evidence matrix

| Claim | Producer | Primary artifact | Destructive control | Final status |
| --- | --- | --- | --- | --- |
| C1 | `verify_empirical_bernstein.py::scalar_supermartingale_claim` | `outputs/independent_certificate.json` | Omitted mean correction gives multiplier `1.1117485324` | `VERIFIED_SCOPED` |
| C2 | `verify_empirical_bernstein.py::sharpness_claim` | `outputs/independent_certificate.json` | Wrong `ψ_E` quadratic gives ratio `1.5` | `VERIFIED_SCOPED` |
| C3 | `verify_empirical_bernstein.py::hilbert_claim` | `outputs/independent_certificate.json` | Omitted vector correction gives multiplier `1.0309652701` | `VERIFIED_SCOPED` |
| Full-scale descriptive audit | `analyze_author_full.py` | `outputs/author_full_analysis.json` | Strict shape/hash/finite-column checks; comparator non-finites retained | `VERIFIED_SCOPED` |

## Reproduction boundary

The independent verifier checks the pinned source anchors before evaluating the declared finite cells. The author arrays are accepted only after manifest and numerical-integrity checks. The release does not convert coverage observed in 14,700 simulations into a universal coverage theorem.
