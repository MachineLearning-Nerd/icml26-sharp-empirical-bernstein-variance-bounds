# Source manifest and citation

## Paper citation

```bibtex
@article{martinez2025sharp,
  title={Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables},
  author={Martinez-Taboada, Diego and Ramdas, Aaditya},
  journal={arXiv preprint arXiv:2505.01987},
  year={2025},
  note={Version 2, 2026; ICML 2026}
}
```

Official paper page: [arXiv:2505.01987v2](https://arxiv.org/abs/2505.01987).

## Source archive

```text
path:   source/arxiv-2505.01987v2.tar
sha256: b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1
```

## Author implementation

```text
repository: https://github.com/DMartinezT/emp_bernstein_variance.git
commit:     e36d2d779e04d52604337ca093071a1f3051f129
entrypoint: main.py
protocol:   3 distributions × 100 trials × 49 sample sizes
```

## Author artifact hashes

Manifest: `outputs/author_full_protocol/manifest.json`

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `uniform.npy` | `470528` | `08f89eef203913e79f5967dab2d9588f655a1fdb73302cdd542f60f21bb3b0e4` |
| `beta.npy` | `470528` | `6292b1f0207441664391bfcba35e14a33f96de0a4805ddca77240ae9d9ef02fd` |
| `beta1.npy` | `470528` | `94165af1b0901d777dd31f53af55af32169e6bfc53002687051dd03a1eb18659` |

## Source anchors

The independent certificate checks the source text for constant conditional variance and mean, the sharpness corollary, the Hilbert-space extension section, and `main_supermartingale_theorem_HS`.
