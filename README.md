# Sharp Empirical Bernstein Inequalities for the Variance of Bounded Random Variables

Source-pinned reproduction in progress for OpenReview `oqkiE71wrC` / arXiv
`2505.01987v2`.

The live six-point contract has three claims:

1. variance confidence sequences under constant conditional mean and variance;
2. iid asymptotic sharpness with unknown mean and variance;
3. extension to separable Hilbert spaces.

This reproduction will run the pinned author simulations at their released
scale and independently check finite distributions, exact first-order limits,
and finite-dimensional Hilbert-space embeddings. It will not present a small
Monte Carlo sample as proof of the universal confidence-sequence theorem.

Primary source archive SHA-256:
`b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1`.

Pinned author implementation: `DMartinezT/emp_bernstein_variance` at
`e36d2d779e04d52604337ca093071a1f3051f129`.

## Outcome

The complete three-claim publication gate passed. The unmodified author
protocol completed on HF CPU-upgrade in 25m38s and its three output arrays were
read back from [the public artifact dataset](https://huggingface.co/datasets/DineshAI/oqkiE71wrC-artifacts)
using the recorded byte sizes and SHA-256 hashes.

- All 14,700 released proposed-EB cells were finite.
- EB widths were strictly lower than Maurer-Pontil in every released cell.
  Mean EB/MP width ratios were .3360 (uniform), .4111 (beta(2,6)), and .3985
  (beta(5,5)).
- Empirical EB coverage was .99939, .99980, and 1.0, respectively. These
  finite simulations are descriptive evidence, not a proof of the universal
  coverage claim.
- The independent certificates pass 3,800 scalar conditional-moment cells, 36
  sharpness cells, and 960 Hilbert-space cells; all four tests and destructive
  controls pass.

See [the claim map](docs/CLAIM_MAP.md) for the exact source anchors, evidence,
and scope boundaries for each scored claim.

## Reproduce the independent certificate

~~~bash
uv venv --python 3.12
source .venv/bin/activate
python -m pip install -r repro/requirements.txt
python repro/src/verify_empirical_bernstein.py
python -m unittest repro.tests.test_empirical_bernstein -v
~~~

## Reproduce the complete technical gate

The released author protocol is preserved as the upstream submodule. Its
unmodified main.py runs all three released distributions, 100 trials each,
and 49 sample sizes. The complete run produces uniform.npy, beta.npy, and
beta1.npy; place the three files and their hash-recorded manifest in
outputs/author_full_protocol/, then run:

~~~bash
source .venv/bin/activate
bash repro/src/fetch_author_artifacts.sh
python repro/src/run_publication_gate.py --artifact-dir outputs/author_full_protocol
~~~

The gate rechecks the primary-source and implementation pins, artifact
byte-size/SHA-256 values, the expected (100, 49, 12) arrays, numerical
validity of the released empirical-Bernstein columns, independent certificates,
and destructive controls. It records descriptive simulation results separately
from the universal-theorem evidence.
