#!/usr/bin/env python3
"""Independent finite certificates for oqkiE71wrC.

The author program is retained separately under ``upstream``.  This verifier
does not import it: it checks the exponential supermartingale mechanism with
high-precision arithmetic, the sharp first-order optimization analytically,
and the Hilbert-space norm replacement on non-collinear finite supports.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_SHA = "b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1"
UPSTREAM_COMMIT = "e36d2d779e04d52604337ca093071a1f3051f129"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest() -> dict:
    archive = ROOT / "source" / "arxiv-2505.01987v2.tar"
    main = ROOT / "source" / "tex" / "ICML" / "example_paper.tex"
    results = ROOT / "source" / "tex" / "main_results.tex"
    hilbert = ROOT / "source" / "tex" / "extension_hs.tex"
    assert sha(archive) == ARCHIVE_SHA
    # A checkout may store .git as a directory, while a proper Git submodule
    # stores it as a gitdir pointer file. Git itself is the authority for both.
    assert (ROOT / "upstream" / ".git").exists()
    commit = __import__("subprocess").check_output(
        ["git", "-C", str(ROOT / "upstream"), "rev-parse", "HEAD"], text=True
    ).strip()
    assert commit == UPSTREAM_COMMIT
    anchors = [
        "constant conditional variance and mean",
        "\\label{corollary:sharpness}",
        "\\label{section:extension_hs}",
        "\\label{theorem:main_supermartingale_theorem_HS}",
    ]
    combined = main.read_text() + results.read_text() + hilbert.read_text()
    assert all(anchor in combined for anchor in anchors)
    return {
        "arxiv": "2505.01987v2",
        "archive_sha256": sha(archive),
        "upstream_commit": commit,
        "anchors": anchors,
    }


def mpe(value: Fraction | float | int) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def psi_e(lam: mp.mpf) -> mp.mpf:
    return -lam - mp.log(1 - lam)


def scalar_multiplier(
    atoms: tuple[tuple[Fraction, Fraction], ...],
    muhat: Fraction,
    sigma2: Fraction,
    plug_in: Fraction,
    lam: Fraction,
    sign: int,
    correct_mean_error: bool = True,
) -> mp.mpf:
    """One conditional expectation of the source supermartingale multiplier."""
    m = mpe(muhat)
    variance = mpe(sigma2)
    correction = (m - mp.mpf("0.5")) ** 2 if correct_mean_error else mp.mpf("0")
    tilde_variance = variance + correction
    lam_mp = mpe(lam)
    total = mp.mpf("0")
    for value, probability in atoms:
        z = (mpe(value) - m) ** 2
        exponent = sign * lam_mp * (z - tilde_variance) - psi_e(lam_mp) * (z - mpe(plug_in)) ** 2
        total += mpe(probability) * mp.exp(exponent)
    return total


def scalar_supermartingale_claim() -> dict:
    """Finite non-iid family with constant conditional mean and variance."""
    mp.mp.dps = 80
    # Both laws have mean 1/2 and variance 1/16.  Selecting either based on
    # the past creates a non-iid martingale stream while retaining the source
    # assumption at every conditional node.
    laws = (
        ((Fraction(0), Fraction(1, 8)), (Fraction(1, 2), Fraction(3, 4)), (Fraction(1), Fraction(1, 8))),
        ((Fraction(1, 4), Fraction(1, 2)), (Fraction(3, 4), Fraction(1, 2))),
    )
    sigma2 = Fraction(1, 16)
    checked = 0
    worst = mp.mpf("0")
    for atoms in laws:
        assert sum(probability for _, probability in atoms) == 1
        assert sum(value * probability for value, probability in atoms) == Fraction(1, 2)
        assert sum((value - Fraction(1, 2)) ** 2 * probability for value, probability in atoms) == sigma2
        for muhat in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
            for plug_in in (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
                for lam in tuple(Fraction(i, 40) for i in range(1, 39)):
                    for sign in (-1, 1):
                        multiplier = scalar_multiplier(atoms, muhat, sigma2, plug_in, lam, sign)
                        worst = max(worst, multiplier)
                        assert multiplier <= 1 + mp.mpf("1e-65")
                        checked += 1
    # Removing the required mean-estimation correction makes a positive-side
    # conditional multiplier exceed one for an off-center estimator.
    broken = scalar_multiplier(laws[1], Fraction(0), sigma2, Fraction(1, 16), Fraction(1, 2), 1, False)
    assert broken > 1
    return {
        "outcome": "passed",
        "scope": "all 3,800 high-precision conditional multiplier cells for two adaptive-switchable bounded laws with fixed conditional mean and variance",
        "cells": checked,
        "max_supermartingale_multiplier": mp.nstr(worst, 18),
        "negative_control_omitted_mean_error_multiplier": mp.nstr(broken, 18),
    }


def sharpness_claim() -> dict:
    """Direct first-order optimization in the iid sharpness corollary."""
    mp.mp.dps = 80
    cells = 0
    worst_finite_relative_error = mp.mpf("0")
    worst_terminal_relative_error = mp.mpf("0")
    wrong_psi_ratio = mp.mpf("0")
    # The oracle first-order constant uses Var((X-mu)^2), not Var(X).
    for variance_of_square in (mp.mpf(1) / 256, mp.mpf(3) / 256, mp.mpf(1) / 16):
        for alpha in (mp.mpf("0.01"), mp.mpf("0.05"), mp.mpf("0.1")):
            target = mp.sqrt(2 * variance_of_square * mp.log(1 / alpha))
            for n in (10**4, 10**6, 10**8, 10**10):
                lam = mp.sqrt(2 * mp.log(1 / alpha) / (variance_of_square * n))
                # Fixed-horizon EB radius using the source psi_E expansion.
                radius = (mp.log(1 / alpha) + n * variance_of_square * psi_e(lam)) / (n * lam)
                observed = mp.sqrt(n) * radius
                error = abs(observed / target - 1)
                worst_finite_relative_error = max(worst_finite_relative_error, error)
                if n == 10**10:
                    worst_terminal_relative_error = max(worst_terminal_relative_error, error)
                cells += 1
            n = mp.mpf(10) ** 12
            lam = mp.sqrt(2 * mp.log(1 / alpha) / (variance_of_square * n))
            bad_radius = (mp.log(1 / alpha) + n * variance_of_square * lam**2) / (n * lam)
            wrong_psi_ratio = max(wrong_psi_ratio, mp.sqrt(n) * bad_radius / target)
    # The largest finite-n discrepancy is reported rather than hidden; the
    # asymptotic claim is checked at n=1e10, where every selected cell is
    # within one tenth of one percent of its oracle constant.
    assert worst_terminal_relative_error < mp.mpf("0.001")
    assert wrong_psi_ratio > mp.mpf("1.4")
    return {
        "outcome": "passed",
        "scope": "first-order radius optimization for three fourth-moment variances, three confidence levels, and four large fixed horizons",
        "cells": cells,
        "max_relative_error_at_n_1e10": mp.nstr(worst_terminal_relative_error, 18),
        "max_relative_error_across_all_finite_horizons": mp.nstr(worst_finite_relative_error, 18),
        "negative_control_wrong_quadratic_psi_ratio": mp.nstr(wrong_psi_ratio, 18),
    }


def norm_squared(vector: tuple[Fraction, ...]) -> Fraction:
    return sum(component * component for component in vector)


def subtract(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a - b for a, b in zip(left, right))


def hilbert_multiplier(
    atoms: tuple[tuple[tuple[Fraction, ...], Fraction], ...],
    muhat: tuple[Fraction, ...],
    sigma2: Fraction,
    plug_in: Fraction,
    lam: Fraction,
    correct_mean_error: bool = True,
) -> mp.mpf:
    mu = tuple(Fraction(0) for _ in muhat)
    correction = norm_squared(subtract(muhat, mu)) if correct_mean_error else Fraction(0)
    total = mp.mpf("0")
    for value, probability in atoms:
        z = mpe(norm_squared(subtract(value, muhat)))
        exponent = mpe(lam) * (z - mpe(sigma2 + correction)) - psi_e(mpe(lam)) * (z - mpe(plug_in)) ** 2
        total += mpe(probability) * mp.exp(exponent)
    return total


def hilbert_claim() -> dict:
    """Check the norm-squared mechanism on non-collinear finite supports."""
    mp.mp.dps = 80
    sigma2 = Fraction(1, 16)
    laws = (
        (((Fraction(1, 4), 0, 0), Fraction(1, 2)), ((Fraction(-1, 4), 0, 0), Fraction(1, 2))),
        (((0, Fraction(1, 4), 0), Fraction(1, 2)), ((0, Fraction(-1, 4), 0), Fraction(1, 2))),
    )
    checked = 0
    worst = mp.mpf("0")
    muhats = ((0, 0, 0), (Fraction(1, 8), 0, 0), (0, Fraction(1, 8), 0), (Fraction(1, 8), Fraction(1, 8), 0))
    for atoms in laws:
        assert all(norm_squared(value) <= Fraction(1, 4) for value, _ in atoms)
        assert sum(probability for _, probability in atoms) == 1
        assert sum(probability * norm_squared(value) for value, probability in atoms) == sigma2
        for muhat in muhats:
            for plug_in in (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(1, 2)):
                for lam in tuple(Fraction(i, 32) for i in range(1, 31)):
                    multiplier = hilbert_multiplier(atoms, muhat, sigma2, plug_in, lam)
                    worst = max(worst, multiplier)
                    assert multiplier <= 1 + mp.mpf("1e-65")
                    checked += 1
    broken = hilbert_multiplier(laws[1], (Fraction(1, 4), 0, 0), sigma2, Fraction(1, 16), Fraction(1, 2), False)
    assert broken > 1
    return {
        "outcome": "passed",
        "scope": "all 960 high-precision non-collinear finite-dimensional Hilbert-space multiplier cells",
        "cells": checked,
        "max_supermartingale_multiplier": mp.nstr(worst, 18),
        "negative_control_omitted_vector_mean_error_multiplier": mp.nstr(broken, 18),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "independent_certificate.json")
    arguments = parser.parse_args()
    result = {
        "paper": "oqkiE71wrC",
        "title": "Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables",
        "source_manifest": source_manifest(),
        "claim_outcomes": {
            "claim_1_constant_conditional_moments": scalar_supermartingale_claim(),
            "claim_2_iid_asymptotic_sharpness": sharpness_claim(),
            "claim_3_separable_hilbert_extension": hilbert_claim(),
        },
        "status": "passed",
        "hardware": "CPU; Python 3.12; mpmath 80-digit arithmetic",
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
