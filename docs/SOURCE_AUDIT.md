# Source audit

## Paper identity

- Official arXiv v2 title: *Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables*.
- Authors: Diego Martinez-Taboada and Aaditya Ramdas.
- Paper: [arXiv:2505.01987v2](https://arxiv.org/abs/2505.01987).
- OpenReview identifier: `oqkiE71wrC`.

The pinned TeX source uses the title “Sharp Empirical Bernstein Inequalities for the Variance of Bounded Random Variables.” The arXiv metadata title is used for the repository name, README, citation, and publication gate; the source wording is retained here so the identity difference is auditable.

## Source pins

| Artifact | Pin | Purpose |
| --- | --- | --- |
| arXiv source archive | `source/arxiv-2505.01987v2.tar`; SHA-256 `b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1` | Paper anchors and released plots |
| Author implementation | `DMartinezT/emp_bernstein_variance@e36d2d779e04d52604337ca093071a1f3051f129` | Unmodified full-scale protocol |
| Author arrays | `outputs/author_full_protocol/manifest.json` | Byte-size and SHA-256 readback |

The author implementation is a Git submodule at `upstream`. `verify_empirical_bernstein.py::source_manifest` checks the archive hash, submodule commit, and anchors in `example_paper.tex`, `main_results.tex`, and `extension_hs.tex` before the independent certificate is accepted.

## Provenance boundary

The independent certificate imports no author implementation. The full-scale protocol is explicitly the unmodified pinned author `main.py`. These are separate evidence paths: the first tests the mathematical mechanism under declared finite laws, while the second audits the released simulations.

The universal claims are not promoted to literal finite-simulation proofs. Non-finite comparator values are retained, and the finite sharpness discrepancy is recorded rather than rounded away.
