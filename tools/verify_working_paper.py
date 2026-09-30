#!/usr/bin/env python3
"""Deterministic acceptance checks for the WHU working-paper package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "docs/research/working-paper"


def pointer(doc, ptr):
    cur = doc
    for part in ptr.strip("/").split("/") if ptr != "/" else []:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def main():
    failures = []
    manifest = json.loads((PKG / "WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json").read_text())
    for entry in manifest["entries"]:
        path = ROOT / entry["source_path"]
        if not path.is_file():
            failures.append(f"missing source: {path}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["source_sha256"]:
            failures.append(f"hash mismatch: {entry['cell_id']}")
        locator = entry["source_locator"]
        if isinstance(locator, str):
            actual = pointer(json.loads(path.read_text()), locator)
            if actual != entry["reported_value"]:
                failures.append(f"value mismatch: {entry['cell_id']} expected {entry['reported_value']!r}, got {actual!r}")
        elif locator.get("type") == "markdown_exact_quote":
            if locator["quote"] not in path.read_text():
                failures.append(f"Markdown locator mismatch: {entry['cell_id']}")
        elif locator.get("type") == "derived_ratio_percent":
            doc = json.loads(path.read_text())
            numerator_pointer = locator["numerator_pointer"]
            if isinstance(numerator_pointer, list):
                numerator = sum(pointer(doc, item) for item in numerator_pointer)
            elif isinstance(numerator_pointer, dict) and "subtract" in numerator_pointer:
                minuend, subtrahend = numerator_pointer["subtract"]
                numerator = pointer(doc, minuend) - pointer(doc, subtrahend)
            else:
                numerator = pointer(doc, numerator_pointer)
            denominator = pointer(doc, locator["denominator_pointer"])
            actual = round(numerator / denominator * 100, locator["decimals"])
            if actual != entry["reported_value"]:
                failures.append(
                    f"derived value mismatch: {entry['cell_id']} expected {entry['reported_value']!r}, got {actual!r}"
                )
        else:
            failures.append(f"unsupported locator: {entry['cell_id']}")

    required = [
        "WHU_WORKING_PAPER_MANUSCRIPT.md",
        "WHU_WORKING_PAPER_MANUSCRIPT.html",
        "WHU_WORKING_PAPER_SUPPLEMENTARY_TABLES.md",
        "WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json",
    ] + [f"figures/figure-{i}-{name}.svg" for i, name in [
        (1,"construct-map"),(2,"chronology"),(3,"semantic-panels"),(4,"acquisition-result"),(5,"assurance-panels"),(6,"measurement-failures")
    ]]
    for rel in required:
        if not (PKG / rel).is_file(): failures.append(f"missing package artifact: {rel}")

    manuscript = (PKG / "WHU_WORKING_PAPER_MANUSCRIPT.md").read_text()
    tables = (PKG / "WHU_WORKING_PAPER_SUPPLEMENTARY_TABLES.md").read_text()
    for heading in ["Abstract", "Introduction and research question", "Related work and context", "Methods", "Results", "Methodological failures", "Discussion", "Limitations", "Reproducibility and supplement", "Conclusion", "References"]:
        if heading not in manuscript: failures.append(f"missing section: {heading}")
    for status in [
        "STAGE_BC_GAP_DISCLOSURE_GATE_FAILED",
        "CROSS_MODEL_SEMANTIC_REPLICATION_INVALID",
        "ACQUISITION_EXPERIMENT_COMPLETE__PRIMARY_GATE_FAILED",
        "CLAIM_CHANGING_CLOSURE_CONCEPT_NOT_OPERATIONALIZED",
        "OWNER_BLOCKER__FROZEN_EXECUTION_SPECIFICATION_NOT_DETERMINATE",
        "OWNER_BLOCKER__FROZEN_MATCHED_PERTURBATION_IMPOSSIBLE",
        "OWNER_BLOCKER__REVISED_DESIGN_DENOMINATORS_NOT_CONSTRUCTIBLE",
        "OWNER_BLOCKER__CONVERGENCE_DESIGN_FAILS_NON_EXHAUSTION_SATISFIABILITY",
        "CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED",
    ]:
        if status not in manuscript + tables: failures.append(f"missing exact disposition: {status}")
    if manuscript.count("Figure ") < 6: failures.append("fewer than six figure references")
    for i in range(1, 7):
        if f"## Table {i}." not in tables: failures.append(f"missing table {i}")
    if re.search(r"V3.{0,80}(failed|did not meet).{0,40}(gate|threshold)", manuscript, re.I | re.S):
        failures.append("possible invented V3 reliability gate")
    if "306-case holdout was not accessed and supplies no result" not in manuscript:
        failures.append("missing explicit unopened-holdout boundary")
    if "Fable produced no semantic capability evidence" not in manuscript:
        failures.append("missing Fable boundary")
    for boundary in [
        "do not establish a capability–assurance asymmetry or scaling law",
        "No Bayes-optimal or oracle risk–coverage frontier was prespecified or computed",
        "512 of 706 adequate cases were withheld (72.52%)",
    ]:
        if boundary not in manuscript:
            failures.append(f"missing v1.0.2 correction boundary: {boundary}")

    if failures:
        print("FAIL")
        for failure in failures: print(f"- {failure}")
        raise SystemExit(1)
    print(f"PASS: {len(manifest['entries'])} exact-number entries; 6 figures; 6 tables; required boundaries present")


if __name__ == "__main__":
    main()
