# WHU working-paper deterministic reproduction guide

These instructions reproduce package artifacts and verify reported values from frozen repository
sources. They do not repeat model/provider calls, reopen a consumed holdout, access the unopened
convergence holdout, or reproduce historical external services.

## Environment

- CPython 3.11 or newer. The package metadata requires `>=3.11`.
- No network access is required for the checks below.
- The working-paper builder and verifiers use only the Python standard library.
- Optional repository tests use the versions bounded in `pyproject.toml` (`pytest>=8,<9`,
  `ruff>=0.8,<1`) and therefore require a previously prepared environment or an owner-approved
  dependency installation. Dependency installation is not part of the offline reproduction claim.

Record the release tag or manifest hash and `python3 --version` before running the checks.

## Required public-package checks

Run from the repository root:

```sh
python3 tools/verify_working_paper.py
python3 tools/verify_working_paper_release.py --strict-tree
python3 tools/verify_working_paper_custody.py
python3 tools/recompute_working_paper_empirical_results.py
python3 tools/verify_working_paper_rebuild.py
```

Expected results are `PASS` for all exact-number entries, all six figures, all six tables, the
required evidence boundaries, the public artifact inventory, integrity hashes, link/path checks, the
privacy/security deny-list, the unopened-holdout custody evidence, independent recomputation of the
V3 and convergence V2 empirical results, and byte-identical derived artifacts.

## Deterministic artifact rebuild

The single rebuild verifier snapshots the designated outputs in memory, rebuilds the six SVG figures,
the exact-number manifest, and the HTML, and compares the resulting bytes without requiring
Git metadata:

```sh
python3 tools/verify_working_paper_rebuild.py
```

A passing byte comparison demonstrates deterministic reconstruction of those derived artifacts. It is not a new
experiment and does not validate the source results beyond their recorded designs.

## Internal-test boundary

The former 49-test focused suite is not a public reproduction command. Its complete prospective
classification, paper-claim mapping, and public substitute checks are in
`WHU_WORKING_PAPER_PUBLIC_TEST_CLASSIFICATION.md`. Most tests exercise fabricated scorer inputs,
historical provider adapters, or prospective design rules. The public recomputation tool instead
recomputes the published V3 result from released synthetic calibration and consumed-evaluation rows,
and the convergence V2 calibration result from released calibration-only rows and labels. The V2
holdout remains unopened and absent.

## Intentionally excluded actions

Do not run the historical provider/model runners, request a replacement Fable response, rerun the V3
holdout, inspect/evaluate the unopened convergence V2 holdout, refit models, tune thresholds, or query
external sources. Those actions would exceed reproduction of the frozen public package and, in some
cases, violate the recorded custody boundary.
