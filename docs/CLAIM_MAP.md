# Claim map

This repository treats the three OpenReview-scored claims as distinct
deliverables. It does not use the released Monte Carlo output as a substitute
for a universal theorem.

| Claim | Primary-source anchor | Independent evidence | Full-scale evidence | Scope boundary |
| --- | --- | --- | --- | --- |
| Constant conditional mean and variance | Abstract in ICML/example_paper.tex; Theorem main_supermartingale_theorem in main_results.tex | 3,800 80-digit one-step conditional multipliers over two switchable non-iid laws | Pinned main.py runs the released three-distribution protocol | The finite certificate checks the source exponential mechanism, not every possible predictable policy. |
| IID asymptotic sharpness | Corollary sharpness in main_results.tex | 36 high-precision first-order radius optimizations with terminal relative error below .001 at n=1e10 | The released finite-sample width comparison is read back separately | The finite-n maximum discrepancy is retained; the certificate targets the stated first-order limit, not an exact finite-n equality. |
| Separable Hilbert extension | Section extension_hs; Theorem main_supermartingale_theorem_HS | 960 80-digit norm-squared multiplier cells over non-collinear finite-dimensional supports | No author Hilbert experiment was released | A finite-dimensional Hilbert space is a valid separable-Hilbert special case; it is not a numeric proof for every Hilbert space. |

All three independent certificates contain destructive controls. The scalar
and vector controls omit the mean-error correction and violate the
supermartingale inequality. The sharpness control replaces the source psi_E
term with a quadratic surrogate and changes the limiting constant.
