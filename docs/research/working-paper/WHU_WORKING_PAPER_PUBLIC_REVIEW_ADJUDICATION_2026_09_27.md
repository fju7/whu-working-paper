# Public reproduction review adjudication

Date: `2026-09-27`

Three bounded pre-release findings were accepted and corrected. No scientific result or manuscript
claim changed.

1. Aggregate-only V3/V2 verification did not reproduce the empirical results. The consumed V3
   synthetic rows and calibration apparatus, plus V2 calibration-only rows/labels/scoring contract,
   were released and a standard-library recomputation check was added.
2. The first corrected candidate exposed enough deterministic V2 generation machinery to derive the
   unopened holdout. That candidate was never published; the reviewer did not execute the derivation.
   The dual-partition builder and complete seed/partition recipe were removed and a calibration-only
   contract replaced them.
3. The release verifier initially ignored unlisted physical files. Strict-tree verification now
   requires physical/declarative inventory equality and scans the actual snapshot for forbidden V2
   paths and signatures. Regression injections fail as required.

Full fresh re-review of the corrected isolated package returned `PASS` with no material findings.
