# Acquisition Assurance Calibration Design Reset — Terminal Closeout

Date: `2026-09-25`  
Directive: `WHU-ACQUISITION-ASSURANCE-CALIBRATION-DESIGN-RESET-V3`  
Terminal disposition: `CALIBRATION_DATASET_READY_BUT_EMPIRICAL_EVALUATION_NOT_AUTHORIZED`

## Authorization and preservation

Fred's explicit `proceed` authorized one bounded reset after
`OWNER_BLOCKER__REVISED_DESIGN_DENOMINATORS_NOT_CONSTRUCTIBLE`. V1 and V2 designs, reviews, freezes,
blockers, hashes, receipts, and results remain unchanged. V2 was not repaired; its over-specified
matched-denominator design is historical.

## What was frozen

V3 asks whether a small vector of stopping-time observable acquisition signals predicts hidden
residual claim-changing omission. A deterministic generator accepted every seed from 10001 through
11200 exactly once, producing 1,200 `(X,Y)` observations. SHA-256 partitioning fixed 960 calibration
and 240 holdout rows. X contains eight runtime-only features; Y and complete-universe facts are stored
separately.

The frozen future analysis preserves three trivial threshold baselines, a decision-table family, and
an eight-feature logistic candidate. Family-wise calibration selection and identical holdout metrics
are specified. Holdout access is governance-locked, hash-bound, partition-checked, and guarded by an
atomic exactly-once consumption claim created before any holdout-data read.

## Satisfiability and review

- Calibration Y counts: `Y=0: 560`; `Y=1: 400`.
- Holdout Y counts: `Y=0: 147`; `Y=1: 93`.
- Partitions: disjoint and collectively exhaustive (`960 + 240 = 1,200`).
- Seed selection: `1,200 accepted / 0 rejected / 0 replaced`.
- Frozen threshold rules: 85; calibration assured denominators range from 60 to 959.
- Feature replay: 1,200/1,200.
- Satisfiability: `PASS`.
- Independent final package review: `PASS` after bounded prospective implementation corrections.
- Focused tests: 7 V3 tests pass; 2 preserved V2 blocker tests also pass.

## What was not done

No predictor was fitted, selected, tuned, or evaluated. Holdout labels were frozen but not used beyond
the prospectively required class-count and integrity checks. No false-assurance result, capability
result, proof-of-concept result, or production/open-world error rate exists.

Semantic/model/provider/search/open-web calls, tokens, and external cost were `0 / 0 / 0 / 0 / 0`,
`0`, and `$0`. Product engineering, outreach, paid humans, publication, and deployment did not occur.

## Next-step eligibility

Empirical calibration and the single holdout evaluation require a new explicit owner authorization
and a separately frozen execution directive. The current package is dataset-ready only.

Governing artifacts:

- `ACQUISITION_ASSURANCE_CALIBRATION_PROTOCOL_V3.md`
- `ACQUISITION_ASSURANCE_CALIBRATION_DATASET_FREEZE_V3.json`
- `ACQUISITION_ASSURANCE_V3_SATISFIABILITY_RECEIPT.json`
- `ACQUISITION_ASSURANCE_V3_INDEPENDENT_PACKAGE_REVIEW.md`

