#!/usr/bin/env python3
"""Verify the public evidence for the deliberately unopened convergence V2 holdout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs/research"
PACKAGE = RESEARCH / "working-paper"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures: list[str] = []
    receipt_path = RESEARCH / "INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json"
    result_path = RESEARCH / "INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json"
    closeout_path = RESEARCH / "INDEPENDENT_ACQUISITION_CONVERGENCE_V2_EMPIRICAL_CLOSEOUT.md"
    manuscript_path = PACKAGE / "WHU_WORKING_PAPER_MANUSCRIPT.md"
    receipt = json.loads(receipt_path.read_text())

    holdout_commitment = receipt.get("frozen_hashes", {}).get("holdout_labels", "")
    if len(holdout_commitment) != 64 or any(c not in "0123456789abcdef" for c in holdout_commitment):
        failures.append("missing or invalid holdout-label SHA-256 commitment")
    requirement = next(
        (item for item in receipt.get("requirements", []) if item.get("id") == "calibration_holdout_disjoint_and_untouched"),
        None,
    )
    if not requirement or requirement.get("status") != "PASS":
        failures.append("missing passing calibration/holdout custody requirement")
    else:
        witness = requirement.get("witness", {})
        if witness.get("evaluation_authorized") is not False or witness.get("holdout_metrics_computed") is not False:
            failures.append("receipt does not record an unevaluated holdout")

    protected_path = ROOT / "benchmarks/independent-acquisition-convergence-v2/holdout-labels.jsonl"
    manifest = json.loads((PACKAGE / "WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json").read_text())
    public_paths = {item["path"] for item in manifest["files"]}
    if protected_path.relative_to(ROOT).as_posix() in public_paths:
        failures.append("protected holdout labels are present in the public manifest")

    result_hash = sha256(result_path)
    closeout = closeout_path.read_text()
    normalized_closeout = " ".join(closeout.split())
    if f"Calibration result SHA-256: `{result_hash}`" not in closeout:
        failures.append("calibration result is not hash-bound by the empirical closeout")
    for statement in (
        "holdout authorization was not issued",
        "the 306 holdout labels were not scored",
        "no holdout result exists",
    ):
        if statement not in normalized_closeout:
            failures.append(f"closeout missing custody statement: {statement}")
    manuscript = manuscript_path.read_text()
    if "306-case holdout was not accessed and supplies no result" not in manuscript:
        failures.append("manuscript does not exclude the unopened holdout from its results")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("PASS: unopened convergence V2 holdout is commitment-bound, excluded, and supplies no paper result")


if __name__ == "__main__":
    main()
