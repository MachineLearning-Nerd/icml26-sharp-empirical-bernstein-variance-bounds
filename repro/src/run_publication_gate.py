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
        "schema_version": 2,
        "paper": {
            "openreview_id": "oqkiE71wrC",
            "title": "Sharp Empirical Bernstein Bounds for the Variance of Bounded Random Variables",
            "arxiv": "2505.01987v2",
            "authors": ["Diego Martinez-Taboada", "Aaditya Ramdas"],
        },
        "repository": {
            "owner": "MachineLearning-Nerd",
            "original_name": "icml26-repro-oqkiE71wrC-empirical-bernstein-variance",
            "target_name": "icml26-sharp-empirical-bernstein-variance-bounds",
            "default_branch": "main",
        },
        "evidence_release_gate": "PASSED",
        "overall_status": "VERIFIED_SCOPED",
        "strict_paper_gate": "NOT_READY",
        "recorded_local_tests_passed": True,
        "substantive_claims": 3,
        "claims_verified_scoped": 3,
        "claims_falsified": 0,
        "claims_blocked": 0,
        "claim_results": {
            "C1": "VERIFIED_SCOPED_CONSTANT_CONDITIONAL_MOMENTS",
            "C2": "VERIFIED_SCOPED_IID_ASYMPTOTIC_SHARPNESS",
            "C3": "VERIFIED_SCOPED_SEPARABLE_HILBERT_EXTENSION",
        },
        "independent_certificate": str(independent.relative_to(ROOT)),
        "full_scale_author_artifact_analysis": str(analysis.relative_to(ROOT)),
        "full_scale_protocol": full_result["protocol"],
        "publication": {
            "status": "PUBLIC_GITHUB_HANDOFF_ONLY",
            "external_score_claimed": False,
        },
        "scope": (
            "Independent certificates cover declared finite laws and an asymptotic optimization route. "
            "The author simulation is descriptive evidence; no universal theorem proof or author-code "
            "equivalence is claimed."
        ),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = args.output if args.output.is_absolute() else ROOT / args.output
    for path in (output, ROOT / "publication_gate.json", ROOT / "outputs" / "publication_gate.json"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
