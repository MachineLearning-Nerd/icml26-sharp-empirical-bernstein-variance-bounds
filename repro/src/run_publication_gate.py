#!/usr/bin/env python3
"""Run the complete local technical gate after artifact readback."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(arguments: list[str]) -> None:
    subprocess.run(arguments, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifact-dir", type=Path,
        default=ROOT / "outputs" / "author_full_protocol",
    )
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "outputs" / "PUBLICATION_GATE_PASSED.json",
    )
    args = parser.parse_args()
    independent = ROOT / "outputs" / "independent_certificate.json"
    analysis = ROOT / "outputs" / "author_full_analysis.json"
    run([sys.executable, "repro/src/verify_empirical_bernstein.py", "--output", str(independent)])
    run([
        sys.executable,
        "repro/src/analyze_author_full.py",
        "--artifact-dir", str(args.artifact_dir),
        "--output", str(analysis),
    ])
    run([sys.executable, "-m", "unittest", "repro.tests.test_empirical_bernstein", "-v"])

    independent_result = json.loads(independent.read_text())
    full_result = json.loads(analysis.read_text())
    if independent_result["status"] != "passed":
        raise RuntimeError("independent certificate did not pass")
    if any(value["outcome"] != "passed" for value in independent_result["claim_outcomes"].values()):
        raise RuntimeError("not every independent claim certificate passed")
    if full_result["status"] != "passed_artifact_integrity_and_descriptive_audit":
        raise RuntimeError("full-scale artifact audit did not pass")
    if any(
        details["finite_fraction_proposed_columns_3_to_8"] != 1.0
        for details in full_result["distributions"].values()
    ):
        raise RuntimeError("released proposed empirical-Bernstein output contains non-finite values")

    result = {
        "paper": "oqkiE71wrC",
        "title": "Sharp Empirical Bernstein Inequalities for the Variance of Bounded Random Variables",
        "claim_count": 3,
        "claim_outcomes": independent_result["claim_outcomes"],
        "independent_certificate": str(independent.relative_to(ROOT)),
        "full_scale_author_artifact_analysis": str(analysis.relative_to(ROOT)),
        "full_scale_protocol": full_result["protocol"],
        "tests": "4 unittest cases passed",
        "tests_passed": True,
        "publication_gate_passed": True,
        "disclosure": (
            "The complete released simulation is audited as full-scale descriptive evidence. "
            "The universal claims are supported independently by exact high-precision "
            "finite-law certificates and a separate asymptotic optimization check."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
