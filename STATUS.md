# Status

Current step: full three-claim publication gate passed, public GitHub evidence
is pushed, and canonical shared-publication queue handoff is complete.

The arXiv v2 source archive and the author implementation are pinned locally.
The primary TeX directly anchors the live contract to the main confidence
sequence corollaries, the iid sharpness corollary, and the Hilbert-space
extension section.

Completed independent evidence:

- Claim 1: 3,800 80-digit conditional multiplier cells across two
  adaptive-switchable, non-iid bounded laws with fixed conditional mean and
  variance. Omitting the required mean-estimation correction produces a
  multiplier of `1.11174853238868829` and is rejected.
- Claim 2: the exact first-order optimization converges to the oracle constant
  in 36 cells; at `n=1e10` the worst relative error is `0.000161917862887`.
  Replacing the source `psi_E` term by the wrong quadratic doubles the leading
  contribution enough to give a `1.5` ratio control.
- Claim 3: 960 non-collinear finite-dimensional Hilbert-space cells pass; the
  omitted vector mean-error correction fails with multiplier `1.0309652701`.
- Four unit tests pass, including strict rejection of a malformed released
  artifact shape.

The first full author run `6a5ded39d216bd6f3a2032a2` completed all three
released 100-trial blocks but could not create its artifact dataset using the
restricted job token, so its ephemeral arrays are not claimed as evidence. The
owner session has now created the empty public artifact dataset. Replacement
CPU-upgrade job `6a5df36abee6ee1cf4ed2364` runs the same unmodified
`main.py` at 3 distributions × 100 trials × 49 sizes and completed in
25m38s. Its three returned arrays and manifest were downloaded from
`DineshAI/oqkiE71wrC-artifacts`, hash-verified, and analyzed locally.

The local readback analyzer now rejects a missing/hash-mismatched artifact,
an unexpected (100, 49, 12) shape, non-finite released EB columns, and negative
interval widths before summarizing coverage and widths without discarding any
non-finite comparator values.

The local Trackio logbook is open at target DineshAI/oqkiE71wrC, has tagged
claim/method/control/conclusion pages, and captures the independent certificate
and four-test run. It is deliberately not published directly: the shared drain
will receive it only after the complete technical gate and GitHub handoff.

The local Git repository is initialized with the official implementation as a
pinned submodule. The source-pin verifier was exercised after this conversion
and supports both standalone clones and standard submodule gitdir pointers.

Read-only diagnostic only: a pre-existing local released-format uniform array
has shape (100, 49, 12), finite proposed EB columns, .999387755 coverage of
the known uniform standard deviation, mean EB width .04237417 versus
Maurer-Pontil .12611035, and 5,433 non-finite decoupled-comparator entries.
It has no durable three-file manifest and is not used as full-scale evidence.

Full results: all 14,700 proposed-EB cells are finite; EB width is strictly
smaller than Maurer-Pontil in every released cell (mean width ratios .3360,
.4111, .3985 for uniform/beta/beta1); EB coverage is .99939, .99980, and 1.0.
The released decoupled comparator retains non-finite values in 36.96%, 38.90%,
and 47.22% of its output entries, which is reported rather than filtered.

Public GitHub: MachineLearning-Nerd/icml26-repro-oqkiE71wrC-empirical-bernstein-variance
at commit 424f83b0a9b949efd5af13dbc94fb9be3829364c. Canonical queue entry 72
(zero-indexed) is owned by the shared drain; this session must not directly
publish the HF Space. Next: wait for shared-drain Space readback, then select
the next eligible high-value paper.
