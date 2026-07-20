#!/usr/bin/env python3
"""Read back and audit the unmodified released simulation artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
COMMIT = "e36d2d779e04d52604337ca093071a1f3051f129"
FILES = ("uniform.npy", "beta.npy", "beta1.npy")
TRUE_STANDARD_DEVIATIONS = {
    "uniform.npy": 1 / np.sqrt(12),
    "beta.npy": np.sqrt(1 / 48),
    "beta1.npy": np.sqrt(1 / 44),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rate(mask: np.ndarray) -> float:
    return float(np.mean(mask))


def analyse_array(name: str, values: np.ndarray) -> dict:
    if values.shape != (100, 49, 12):
        raise ValueError(f"{name}: expected (100, 49, 12), got {values.shape}")
    proposed = values[:, :, 3:9]
    if not np.isfinite(proposed).all():
        raise ValueError(f"{name}: released proposed EB columns 3:9 contain non-finite values")

    truth = TRUE_STANDARD_DEVIATIONS[name]
    mp_lower, mp_upper = values[:, :, 2], values[:, :, 0]
    eb_lower, eb_upper = values[:, :, 5], values[:, :, 3]
    upsilon_lower = values[:, :, 7]
    mp_width = mp_upper - mp_lower
    eb_width = eb_upper - eb_lower
    hybrid_width = eb_upper - upsilon_lower
    if (mp_width < 0).any() or (eb_width < 0).any() or (hybrid_width < 0).any():
        raise ValueError(f"{name}: an interval has negative width")

    decoupled = values[:, :, 9:12]
    return {
        "true_standard_deviation": float(truth),
        "shape": list(values.shape),
        "cells": int(values[:, :, 0].size),
        "finite_fraction_proposed_columns_3_to_8": rate(np.isfinite(proposed)),
        "coverage": {
            "maurer_pontil": rate((mp_lower <= truth) & (truth <= mp_upper)),
            "empirical_bernstein": rate((eb_lower <= truth) & (truth <= eb_upper)),
            "empirical_bernstein_bennett_lower_hybrid": rate((upsilon_lower <= truth) & (truth <= eb_upper)),
        },
        "mean_interval_width": {
            "maurer_pontil": float(np.mean(mp_width)),
            "empirical_bernstein": float(np.mean(eb_width)),
            "empirical_bernstein_bennett_lower_hybrid": float(np.mean(hybrid_width)),
        },
        "median_interval_width": {
            "maurer_pontil": float(np.median(mp_width)),
            "empirical_bernstein": float(np.median(eb_width)),
            "empirical_bernstein_bennett_lower_hybrid": float(np.median(hybrid_width)),
        },
        "empirical_bernstein_width_vs_maurer_pontil": {
            "mean_ratio": float(np.mean(eb_width) / np.mean(mp_width)),
            "cell_win_fraction": rate(eb_width < mp_width),
            "cell_tie_fraction": rate(eb_width == mp_width),
        },
        "decoupled_comparator_nonfinite_fraction_columns_9_to_11": rate(~np.isfinite(decoupled)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifact-dir", type=Path,
        default=ROOT / "outputs" / "author_full_protocol",
        help="directory containing manifest.json and the three .npy artifacts",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "author_full_analysis.json")
    args = parser.parse_args()
    artifact_dir = args.artifact_dir.resolve()
    manifest_path = artifact_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("paper") != "oqkiE71wrC" or manifest.get("commit") != COMMIT:
        raise ValueError("manifest does not identify the audited paper and pinned author commit")
    if manifest.get("entrypoint") != "main.py":
        raise ValueError("manifest does not identify the released main.py entrypoint")

    results = {}
    for name in FILES:
        path = artifact_dir / name
        file_manifest = manifest.get("files", {}).get(name)
        if file_manifest is None or not path.is_file():
            raise FileNotFoundError(f"missing declared artifact {name}")
        if path.stat().st_size != file_manifest["bytes"] or sha256(path) != file_manifest["sha256"]:
            raise ValueError(f"hash or byte-size mismatch for {name}")
        results[name] = analyse_array(name, np.load(path, allow_pickle=False))

    report = {
        "paper": "oqkiE71wrC",
        "source_commit": COMMIT,
        "artifact_manifest": manifest,
        "protocol": "unmodified pinned author main.py: three distributions x 100 trials x 49 sample sizes",
        "method_columns": {
            "0_to_2": "Maurer-Pontil upper, center, lower standard-deviation interval",
            "3_to_6": "released empirical-Bernstein upper, center, lower, center",
            "7_to_8": "released empirical-Bernstein-Bennett lower and center",
            "9_to_11": "released decoupled comparator upper, center, lower",
        },
        "distributions": results,
        "status": "passed_artifact_integrity_and_descriptive_audit",
        "disclosure": "The source simulation is descriptive evidence, not a universal-coverage proof. Non-finite comparator values are retained and reported rather than filtered.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
