# ICML 2026 — Sharp Empirical Bernstein Bounds for Variance

This repository contains a source-pinned and independently audited reproduction of [*Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables*](https://arxiv.org/abs/2505.01987) by Diego Martinez-Taboada and Aaditya Ramdas.

The official arXiv v2 metadata uses “Bounds.” The pinned TeX archive currently labels the manuscript “Sharp Empirical Bernstein Inequalities”; both references point to the same `2505.01987v2` source archive and are recorded explicitly in [the source audit](docs/SOURCE_AUDIT.md).

## Release status

The evidence-release gate **PASSED**. All three claims are `VERIFIED_SCOPED`. The strict paper-level gate remains **NOT_READY** because the independent certificates cover declared finite laws and an asymptotic optimization route; they do not replace universal proofs. The full author simulation is treated as descriptive evidence, not as proof of universal coverage.

`VERIFIED_SCOPED` means that the declared audit contract and its controls pass. It does not claim that a finite certificate proves a theorem for every admissible process or that this repository is the authors' implementation.

| Claim | Paper statement | Status | Claim producer and evidence |
| --- | --- | --- | --- |
| C1 | Confidence sequences under constant conditional mean and variance | **VERIFIED_SCOPED** | `repro/src/verify_empirical_bernstein.py::scalar_supermartingale_claim`; 3,800 80-digit conditional multiplier cells over two switchable non-iid bounded laws, with omitted-mean-correction control in `outputs/independent_certificate.json` |
| C2 | IID asymptotic sharpness with unknown mean and variance | **VERIFIED_SCOPED** | `repro/src/verify_empirical_bernstein.py::sharpness_claim`; 36 high-precision first-order optimizations, terminal relative error `.000161918` at `n=10^10`, and wrong-`ψ_E` control |
| C3 | Extension to separable Hilbert spaces | **VERIFIED_SCOPED** | `repro/src/verify_empirical_bernstein.py::hilbert_claim`; 960 80-digit non-collinear finite-dimensional cells with omitted-vector-mean-error control |

## How each claim is produced

```text
arXiv/source anchors
  → independent high-precision certificate
  → unmodified pinned-author protocol
  → artifact hash/readback and destructive controls
  → fail-closed publication gate
```

### C1 — constant conditional mean and variance

The independent certificate checks the source exponential-supermartingale multiplier over two bounded laws that can be selected adaptively while preserving conditional mean `1/2` and variance `1/16`. It checks 3,800 cells at 80-digit precision; the maximum multiplier is `1.0`. Removing the required mean-estimation correction produces multiplier `1.1117485324` and fails the negative control.

### C2 — IID asymptotic sharpness

The certificate optimizes the fixed-horizon empirical-Bernstein radius for three fourth-moment variances, three confidence levels, and four large horizons. At `n=10^10`, the largest relative error from the oracle first-order constant is `.0001619179`; across all finite horizons it is `.2597273`, which is retained rather than hidden. Replacing the source `ψ_E` term with a quadratic surrogate produces a limiting ratio of `1.5`.

### C3 — separable Hilbert extension

The certificate replaces scalar squared deviations with squared norms on two non-collinear three-dimensional finite supports. It checks 960 cells at 80-digit precision; the maximum multiplier is `1.0`. Omitting the vector mean-error correction produces multiplier `1.0309652701`.

### Full-scale author protocol

The pinned author implementation is `DMartinezT/emp_bernstein_variance@e36d2d779e04d52604337ca093071a1f3051f129`. Its unmodified `main.py` ran 3 distributions × 100 trials × 49 sample sizes, producing 14,700 proposed empirical-Bernstein cells.

| Distribution | Proposed EB coverage | Mean EB/MP width ratio | Proposed columns finite | Decoupled comparator non-finite fraction |
| --- | ---: | ---: | ---: | ---: |
| Uniform | `.999388` | `.3360` | `1.0` | `.3696` |
| Beta(2,6) | `.999796` | `.4111` | `1.0` | `.3890` |
| Beta(5,5) | `1.0` | `.3985` | `1.0` | `.4722` |

The proposed EB width is strictly below Maurer–Pontil in every released cell. Non-finite comparator values are retained and reported; they are never filtered to improve the comparison.

## Branch map

The repository has one final branch:

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Canonical source pin, independent certificates, author-artifact audit, citation, and release gate |

See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for the final ref check.

## Pinned inputs and provenance

- Paper: [arXiv:2505.01987v2](https://arxiv.org/abs/2505.01987); OpenReview identifier `oqkiE71wrC`.
- Source archive: `source/arxiv-2505.01987v2.tar`, SHA-256 `b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1`.
- Author implementation: `https://github.com/DMartinezT/emp_bernstein_variance`, commit `e36d2d779e04d52604337ca093071a1f3051f129`, tracked as the `upstream` submodule.
- Full-scale artifact manifest: `outputs/author_full_protocol/manifest.json`.
- Environment: Python 3.12 with `repro/requirements.txt`.

The independent verifier does not import the author implementation. The source audit checks the archive hash, submodule commit, and TeX anchors before the finite certificates run. The full-scale artifact analyzer checks shape, byte size, SHA-256, finite proposed columns, widths, coverage, and comparator non-finite values.

## Reproduce the audit

```bash
git clone --recurse-submodules https://github.com/MachineLearning-Nerd/icml26-sharp-empirical-bernstein-variance-bounds.git
cd icml26-sharp-empirical-bernstein-variance-bounds
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/verify_empirical_bernstein.py
.venv/bin/python -m unittest repro.tests.test_empirical_bernstein -v
```

To audit the retained author arrays without rerunning the expensive source job:

```bash
.venv/bin/python repro/src/analyze_author_full.py \
  --artifact-dir outputs/author_full_protocol \
  --output /tmp/author_full_analysis.json
```

The complete gate command reruns the independent certificate, artifact analysis, and four tests:

```bash
.venv/bin/python repro/src/run_publication_gate.py \
  --artifact-dir outputs/author_full_protocol
```

## Documentation

- [Evidence ledger](docs/EVIDENCE.md)
- [Claim map](docs/CLAIM_MAP.md)
- [Source audit](docs/SOURCE_AUDIT.md)
- [Source manifest and citation](SOURCE_MANIFEST.md)
- [Audit report](AUDIT_REPORT.md)
- [Branch audit](BRANCH_AUDIT.md)
- [Publication gate](docs/PUBLICATION_GATE.md)
- [Publication gate](publication_gate.json)
- [Output guide](outputs/README.md)

## Citation

```bibtex
@article{martinez2025sharp,
  title={Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables},
  author={Martinez-Taboada, Diego and Ramdas, Aaditya},
  journal={arXiv preprint arXiv:2505.01987},
  year={2025},
  note={Version 2, 2026; ICML 2026}
}
```

Paper page: [arXiv:2505.01987v2](https://arxiv.org/abs/2505.01987).

## Thank you

Thank you to Diego Martinez-Taboada and Aaditya Ramdas for developing a sharp variance-confidence framework that covers dependent conditional-moment settings, asymptotic adaptation, and Hilbert-space extensions, and for releasing the implementation and source material needed for an independent audit. This repository keeps the finite scope, artifact integrity checks, comparator non-finite values, and negative controls visible.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
