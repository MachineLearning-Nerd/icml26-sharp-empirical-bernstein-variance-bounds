# Evidence ledger

This ledger separates independent finite certificates from descriptive author-protocol output. `VERIFIED_SCOPED` records a passing declared contract; it is not a claim that finite computation proves a universal theorem.

## C1 — constant conditional mean and variance

Producer: `repro/src/verify_empirical_bernstein.py::scalar_supermartingale_claim`.

The verifier uses two bounded laws with the same conditional mean `1/2` and variance `1/16`, allowing adaptive switching while preserving the source assumptions. It checks 3,800 conditional multiplier cells at 80-digit precision. The maximum corrected multiplier is `1.0`. Removing the mean-estimation correction produces multiplier `1.1117485324`, which fails the destructive control.

Artifact: `outputs/independent_certificate.json`.

Result: **VERIFIED_SCOPED** for the finite conditional-moment family.

## C2 — IID asymptotic sharpness

Producer: `repro/src/verify_empirical_bernstein.py::sharpness_claim`.

The verifier optimizes the source fixed-horizon radius for three fourth-moment variances, three confidence levels, and four large horizons. At `n=10^10`, the largest relative error from the oracle first-order constant is `.0001619179`; across all finite horizons the largest discrepancy is `.2597273` and is retained. Replacing the source `ψ_E` term by a quadratic surrogate produces a ratio of `1.5`.

Artifact: `outputs/independent_certificate.json`.

Result: **VERIFIED_SCOPED** for the declared first-order optimization cells.

## C3 — separable Hilbert extension

Producer: `repro/src/verify_empirical_bernstein.py::hilbert_claim`.

The scalar squared-deviation mechanism is replaced with squared norms on two non-collinear three-dimensional finite supports. The verifier checks 960 cells at 80-digit precision. The maximum corrected multiplier is `1.0`; omitting the vector mean-error correction produces multiplier `1.0309652701`.

Artifact: `outputs/independent_certificate.json`.

Result: **VERIFIED_SCOPED** for the finite-dimensional Hilbert special cases.

## Full-scale author protocol

Producers: the pinned author `main.py`, `repro/src/analyze_author_full.py`, and `repro/src/run_publication_gate.py`.

The unmodified author protocol uses 3 distributions × 100 trials × 49 sample sizes, yielding 14,700 cells. Every proposed empirical-Bernstein column is finite and its width is strictly below Maurer–Pontil in every released cell. Mean EB/Maurer–Pontil width ratios are `.3360`, `.4111`, and `.3985` for uniform, beta(2,6), and beta(5,5). Empirical coverages are `.999388`, `.999796`, and `1.0`.

The decoupled comparator has non-finite entries in `.3696`, `.3890`, and `.4722` of its entries. They remain in the audit and are not filtered.

Artifact: `outputs/author_full_analysis.json`, backed by `outputs/author_full_protocol/manifest.json`.

Result: **VERIFIED_SCOPED descriptive evidence**.

## Evidence path

```text
source archive + upstream pin → independent producer
→ author artifact readback → destructive controls
→ publication gate
```
