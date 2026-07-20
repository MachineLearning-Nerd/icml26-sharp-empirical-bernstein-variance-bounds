# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b87369531a4c", "created_at": "2026-07-20T09:52:34+00:00", "title": "Pinned implementation and released scale"}
-->
Primary arXiv source archive and the official author repository are cryptographically pinned. The released main.py protocol is 3 bounded distributions x 100 trials x 49 sample sizes. It is executed unchanged on an HF CPU-upgrade worker and read back using manifest byte-size and SHA-256 verification.


---
<!-- trackio-cell
{"type": "code", "id": "cell_ac5199e8d227", "created_at": "2026-07-20T10:34:16+00:00", "title": "Full CPU publication gate", "command": ["python", "repro/src/run_publication_gate.py", "--artifact-dir", "outputs/author_full_protocol"], "exit_code": 0, "duration_s": 1.664}
-->
````bash
$ python repro/src/run_publication_gate.py --artifact-dir outputs/author_full_protocol
````

exit 0 · 1.7s


````python title=run_publication_gate.py
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

````


````output
{"claim_outcomes": {"claim_1_constant_conditional_moments": {"cells": 3800, "max_supermartingale_multiplier": "1.0", "negative_control_omitted_mean_error_multiplier": "1.11174853238868829", "outcome": "passed", "scope": "all 3,800 high-precision conditional multiplier cells for two adaptive-switchable bounded laws with fixed conditional mean and variance"}, "claim_2_iid_asymptotic_sharpness": {"cells": 36, "max_relative_error_across_all_finite_horizons": "0.25972734349275493", "max_relative_error_at_n_1e10": "0.000161917862887044265", "negative_control_wrong_quadratic_psi_ratio": "1.5", "outcome": "passed", "scope": "first-order radius optimization for three fourth-moment variances, three confidence levels, and four large fixed horizons"}, "claim_3_separable_hilbert_extension": {"cells": 960, "max_supermartingale_multiplier": "1.0", "negative_control_omitted_vector_mean_error_multiplier": "1.03096527010360196", "outcome": "passed", "scope": "all 960 high-precision non-collinear finite-dimensional Hilbert-space multiplier cells"}}, "hardware": "CPU; Python 3.12; mpmath 80-digit arithmetic", "paper": "oqkiE71wrC", "source_manifest": {"anchors": ["constant conditional variance and mean", "\\label{corollary:sharpness}", "\\label{section:extension_hs}", "\\label{theorem:main_supermartingale_theorem_HS}"], "archive_sha256": "b95e61d7af9dcd5f8a08275e1d88af13fc8af85adc7eeb4d3c64d275de0830c1", "arxiv": "2505.01987v2", "upstream_commit": "e36d2d779e04d52604337ca093071a1f3051f129"}, "status": "passed", "title": "Sharp Empirical Bernstein Inequalities for the Variance of Bounded Random Variables"}
{"artifact_manifest": {"commit": "e36d2d779e04d52604337ca093071a1f3051f129", "entrypoint": "main.py", "files": {"beta.npy": {"bytes": 470528, "sha256": "6292b1f0207441664391bfcba35e14a33f96de0a4805ddca77240ae9d9ef02fd"}, "beta1.npy": {"bytes": 470528, "sha256": "94165af1b0901d777dd31f53af55af32169e6bfc53002687051dd03a1eb18659"}, "uniform.npy": {"bytes": 470528, "sha256": "08f89eef203913e79f5967dab2d9588f655a1fdb73302cdd542f60f21bb3b0e4"}}, "paper": "oqkiE71wrC", "protocol": "unmodified author source; n_experiments=100; sample_size_list=arange(100,5000,100); distributions=uniform,beta(2,6),beta(5,5)", "source_repository": "https://github.com/DMartinezT/emp_bernstein_variance.git"}, "disclosure": "The source simulation is descriptive evidence, not a universal-coverage proof. Non-finite comparator values are retained and reported rather than filtered.", "distributions": {"beta.npy": {"cells": 4900, "coverage": {"empirical_bernstein": 0.9997959183673469, "empirical_bernstein_bennett_lower_hybrid": 0.9997959183673469, "maurer_pontil": 1.0}, "decoupled_comparator_nonfinite_fraction_columns_9_to_11": 0.3889795918367347, "empirical_bernstein_width_vs_maurer_pontil": {"cell_tie_fraction": 0.0, "cell_win_fraction": 1.0, "mean_ratio": 0.41105955083849033}, "finite_fraction_proposed_columns_3_to_8": 1.0, "mean_interval_width": {"empirical_bernstein": 0.05071488399115052, "empirical_bernstein_bennett_lower_hybrid": 0.05592082940759499, "maurer_pontil": 0.12337600206028769}, "median_interval_width": {"empirical_bernstein": 0.02593446599680395, "empirical_bernstein_bennett_lower_hybrid": 0.028186593163065064, "maurer_pontil": 0.09792946107842937}, "shape": [100, 49, 12], "true_standard_deviation": 0.14433756729740643}, "beta1.npy": {"cells": 4900, "coverage": {"empirical_bernstein": 1.0, "empirical_bernstein_bennett_lower_hybrid": 1.0, "maurer_pontil": 1.0}, "decoupled_comparator_nonfinite_fraction_columns_9_to_11": 0.47217687074829934, "empirical_bernstein_width_vs_maurer_pontil": {"cell_tie_fraction": 0.0, "cell_win_fraction": 1.0, "mean_ratio": 0.3984598563514911}, "finite_fraction_proposed_columns_3_to_8": 1.0, "mean_interval_width": {"empirical_bernstein": 0.04927626015330395, "empirical_bernstein_bennett_lower_hybrid": 0.05376418037787066, "maurer_pontil": 0.12366681202092329}, "median_interval_width": {"empirical_bernstein": 0.0250535546957672, "empirical_bernstein_bennett_lower_hybrid": 0.02666611770138, "maurer_pontil": 0.09792946107842937}, "shape": [100, 49, 12], "true_standard_deviation": 0.15075567228888181}, "uniform.npy": {"cells": 4900, "coverage": {"empirical_bernstein": 0.9993877551020408, "empirical_bernstein_bennett_lower_hybrid": 0.9993877551020408, "maurer_pontil": 1.0}, "decoupled_comparator_nonfinite_fraction_columns_9_to_11": 0.36959183673469387, "empirical_bernstein_width_vs_maurer_pontil": {"cell_tie_fraction": 0.0, "cell_win_fraction": 1.0, "mean_ratio": 0.336008674986558}, "finite_fraction_proposed_columns_3_to_8": 1.0, "mean_interval_width": {"empirical_bernstein": 0.04237417221676187, "empirical_bernstein_bennett_lower_hybrid": 0.04540197673155277, "maurer_pontil": 0.12611035181891372}, "median_interval_width": {"empirical_bernstein": 0.02447935671721649, "empirical_bernstein_bennett_lower_hybrid": 0.025235935338145665, "maurer_pontil": 0.09792946107842937}, "shape": [100, 49, 12], "true_standard_deviation": 0.2886751345948129}}, "method_columns": {"0_to_2": "Maurer-Pontil upper, center, lower standard-deviation interval", "3_to_6": "released empirical-Bernstein upper, center, lower, center", "7_to_8": "released empirical-Bernstein-Bennett lower and center", "9_to_11": "released decoupled comparator upper, center, lower"}, "paper": "oqkiE71wrC", "protocol": "unmodified pinned author main.py: three distributions x 100 trials x 49 sample sizes", "source_commit": "e36d2d779e04d52604337ca093071a1f3051f129", "status": "passed_artifact_integrity_and_descriptive_audit"}
test_author_artifact_shape_is_strict (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_author_artifact_shape_is_strict) ... ok
test_corrected_scalar_multiplier_is_supermartingale_step (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_corrected_scalar_multiplier_is_supermartingale_step) ... ok
test_omitting_mean_correction_fails (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_omitting_mean_correction_fails) ... ok
test_psi_is_positive (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_psi_is_positive) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
{"claim_count": 3, "claim_outcomes": {"claim_1_constant_conditional_moments": {"cells": 3800, "max_supermartingale_multiplier": "1.0", "negative_control_omitted_mean_error_multiplier": "1.11174853238868829", "outcome": "passed", "scope": "all 3,800 high-precision conditional multiplier cells for two adaptive-switchable bounded laws with fixed conditional mean and variance"}, "claim_2_iid_asymptotic_sharpness": {"cells": 36, "max_relative_error_across_all_finite_horizons": "0.25972734349275493", "max_relative_error_at_n_1e10": "0.000161917862887044265", "negative_control_wrong_quadratic_psi_ratio": "1.5", "outcome": "passed", "scope": "first-order radius optimization for three fourth-moment variances, three confidence levels, and four large fixed horizons"}, "claim_3_separable_hilbert_extension": {"cells": 960, "max_supermartingale_multiplier": "1.0", "negative_control_omitted_vector_mean_error_multiplier": "1.03096527010360196", "outcome": "passed", "scope": "all 960 high-precision non-collinear finite-dimensional Hilbert-space multiplier cells"}}, "disclosure": "The complete released simulation is audited as full-scale descriptive evidence. The universal claims are supported independently by exact high-precision finite-law certificates and a separate asymptotic optimization check.", "full_scale_author_artifact_analysis": "outputs/author_full_analysis.json", "full_scale_protocol": "unmodified pinned author main.py: three distributions x 100 trials x 49 sample sizes", "independent_certificate": "outputs/independent_certificate.json", "paper": "oqkiE71wrC", "publication_gate_passed": true, "tests": "4 unittest cases passed", "title": "Sharp Empirical Bernstein Inequalities for the Variance of Bounded Random Variables"}

````
