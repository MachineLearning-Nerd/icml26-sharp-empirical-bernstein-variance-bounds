# Negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_7c7d96db00f8", "created_at": "2026-07-20T09:52:34+00:00", "title": "Falsification criteria"}
-->
The gate rejects an omitted scalar or vector mean correction, a wrong quadratic psi term, malformed or hash-mismatched artifacts, non-finite proposed empirical-Bernstein outputs, and invalid interval widths. Comparator NaNs are retained as observations, never filtered.


---
<!-- trackio-cell
{"type": "code", "id": "cell_1a017674eaa8", "created_at": "2026-07-20T09:52:59+00:00", "title": "Unit tests and artifact-shape rejection", "command": ["python", "-m", "unittest", "repro.tests.test_empirical_bernstein", "-v"], "exit_code": 0, "duration_s": 0.208}
-->
````bash
$ python -m unittest repro.tests.test_empirical_bernstein -v
````

exit 0 · 0.2s


````output
test_author_artifact_shape_is_strict (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_author_artifact_shape_is_strict) ... ok
test_corrected_scalar_multiplier_is_supermartingale_step (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_corrected_scalar_multiplier_is_supermartingale_step) ... ok
test_omitting_mean_correction_fails (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_omitting_mean_correction_fails) ... ok
test_psi_is_positive (repro.tests.test_empirical_bernstein.EmpiricalBernsteinTest.test_psi_is_positive) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK

````
