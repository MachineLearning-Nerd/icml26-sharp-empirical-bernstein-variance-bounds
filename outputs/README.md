# Output directory

These files are retained evidence rather than scratch output.

- `independent_certificate.json`: high-precision C1–C3 certificates and negative controls.
- `author_full_analysis.json`: hash-checked descriptive analysis of the three released author arrays.
- `author_full_protocol/manifest.json`: artifact byte sizes and SHA-256 values.
- `publication_gate.json`: normalized release decision and claim statuses.
- `PUBLICATION_GATE_PASSED.json`: backward-compatible uppercase gate record.

The `.npy` arrays are not filtered to remove non-finite comparator entries. The analyzer reports those entries separately from the finite proposed empirical-Bernstein columns.
