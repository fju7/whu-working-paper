#!/usr/bin/env python3
"""Build or verify the bounded public working-paper release manifest.

Standard-library only. This tool never calls a network, model, provider, or experiment runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "docs/research/working-paper"
MANIFEST = PKG / "WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json"

PUBLIC_FILES = [
    "README.md",
    "CORRECTIONS.md",
    "LICENSE.md",
    "CITATION.cff",
    "pyproject.toml",
    "tools/build_working_paper_artifacts.py",
    "tools/render_working_paper.py",
    "tools/verify_working_paper.py",
    "tools/verify_working_paper_release.py",
    "tools/verify_working_paper_rebuild.py",
    "tools/verify_working_paper_custody.py",
    "tools/recompute_working_paper_empirical_results.py",
    "tools/acquisition_assurance_v3.py",
    "tools/acquisition_assurance_v3_score.py",
    "tools/score_independent_acquisition_convergence_v2_public.py",
    "protocols/acquisition-assurance-calibration-poc-v3.json",
    "protocols/independent-acquisition-convergence-v2-public-calibration.json",
    "benchmarks/acquisition-assurance-calibration-poc-v3/generator-blueprints.jsonl",
    "benchmarks/acquisition-assurance-calibration-poc-v3/runtime-observations.jsonl",
    "benchmarks/acquisition-assurance-calibration-poc-v3/evaluator-labels.jsonl",
    "benchmarks/acquisition-assurance-calibration-poc-v3/frozen-calibration-model.json",
    "benchmarks/acquisition-assurance-calibration-poc-v3/holdout-results.json",
    "benchmarks/independent-acquisition-convergence-v2/generator-blueprints.jsonl",
    "benchmarks/independent-acquisition-convergence-v2/calibration-runtime-observations.jsonl",
    "benchmarks/independent-acquisition-convergence-v2/calibration-labels.jsonl",
    "benchmark-results/closed-universe-claim-strength-stage-a-v1.json",
    "benchmark-results/closed-universe-claim-strength-stage-bc-v1.json",
    "benchmark-results/cross-model-semantic-replication-v1.json",
    "benchmark-results/falsifier-identification-v1.json",
    "benchmark-results/known-gap-robustness-v1.json",
    "docs/research/ACQUISITION_ASSURANCE_CALIBRATION_RESET_CLOSEOUT.md",
    "docs/research/ACQUISITION_ASSURANCE_CALIBRATION_EXECUTION_BLOCKER_CLOSEOUT.md",
    "docs/research/ACQUISITION_ASSURANCE_EXECUTABLE_SPECIFICATION_BLOCKER_CLOSEOUT.md",
    "docs/research/ACQUISITION_ASSURANCE_PROSPECTIVE_REVISION_BLOCKER_CLOSEOUT.md",
    "docs/research/ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md",
    "docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_CLOSEOUT.md",
    "docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json",
    "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md",
    "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_V1_4_TERMINAL_CLOSEOUT.md",
    "docs/research/CLAIM_CHANGING_CLOSURE_ADJUDICATION_CLOSEOUT.md",
    "docs/research/CROSS_MODEL_SEMANTIC_REPLICATION_CLOSEOUT.md",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CLOSEOUT.md",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_EMPIRICAL_CLOSEOUT.md",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V1_BLOCKER_CLOSEOUT.md",
    "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V1_SATISFIABILITY_RECEIPT.json",
    "protocols/independent-acquisition-convergence-v1.json",
    "tools/independent_acquisition_convergence_v1.py",
    "docs/research/CLOSED_UNIVERSE_CLAIM_STRENGTH_STAGE_BC_FORENSIC_ANALYSIS.md",
    "docs/research/CLOSED_UNIVERSE_CLAIM_STRENGTH_STAGE_BC_FORENSIC_CLOSEOUT.md",
    "docs/research/B1_PROGRAM_FINAL_SYNTHESIS.md",
    "docs/research/OPENEVIDENCE_ASSURANCE_CASE_STUDY.md",
    "docs/research/WHU_STATE_OF_FIELD_EVIDENCE_ADEQUACY_ADJACENT_WORK_MATRIX.md",
    "docs/research/WHU_STATE_OF_FIELD_EVIDENCE_ADEQUACY_REVIEW.md",
    "docs/research/WARRANTED_TRUST_V1_DECISION.md",
    "docs/research/WHU_CONTINUE_STOP_DECISION.md",
    "docs/research/WHU_CONVENTIONAL_ENGINEERING_COUNTERFACTUAL.md",
    "docs/research/WHU_HISTORICAL_TASK_REEXECUTION_CLOSEOUT.md",
    "docs/research/WHU_PROSPECTIVE_AGENT_BOUNDARY_CLOSURE_REVIEW.md",
    "docs/research/WHU_WORKING_PAPER_CLAIM_LEDGER.md",
    "docs/research/WHU_WORKING_PAPER_EVIDENCE_INVENTORY.md",
    "docs/research/closed-universe-evidence-acquisition-v1.4/results.json",
    "docs/research/working-paper/README.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_ARTIFACT_MAP.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_AVAILABILITY_AND_DISCLOSURE.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_CITATION_AND_LICENSE_AUDIT.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json",
    "docs/research/working-paper/WHU_WORKING_PAPER_LIMITATIONS_REGISTER.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_MANUSCRIPT.html",
    "docs/research/working-paper/WHU_WORKING_PAPER_MANUSCRIPT.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_OUTSIDE_RECONSTRUCTION_REVIEW.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_METHOD_HISTORY.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_TEST_CLASSIFICATION.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_CONTRACT_REDESIGN.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_ONLY_RECONSTRUCTION_2026_09_27.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_FRESH_INDEPENDENT_PUBLIC_REVIEW_2026_09_27.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_REVIEW_ADJUDICATION_2026_09_27.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_PREPRINT_RELEASE_CHECKLIST.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_REPRODUCTION.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_REPRODUCIBILITY_AUDIT_DECISION.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_REPRODUCIBILITY_AUDIT_ADJUDICATION.md",
    "docs/research/working-paper/WHU_WORKING_PAPER_SUPPLEMENTARY_TABLES.md",
    *[
        f"docs/research/working-paper/figures/figure-{i}-{name}.svg"
        for i, name in [
            (1, "construct-map"),
            (2, "chronology"),
            (3, "semantic-panels"),
            (4, "acquisition-result"),
            (5, "assurance-panels"),
            (6, "measurement-failures"),
        ]
    ],
]

DENY_PATTERNS = {
    "private temporary path": re.compile(r"/private/tmp/|/tmp/"),
    "local Codex path": re.compile(r"(?:/Users/[^/]+/\.codex|chatgpt-conversation://|codex://)"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "generic secret assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"
    ),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "UUID": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
}

FORBIDDEN_V2_PUBLIC_PATHS = {
    "tools/independent_acquisition_convergence_v2.py",
    "tools/score_independent_acquisition_convergence_v2.py",
    "protocols/independent-acquisition-convergence-v2.json",
    "benchmarks/independent-acquisition-convergence-v2/runtime-observations.jsonl",
    "benchmarks/independent-acquisition-convergence-v2/holdout-labels.jsonl",
    "benchmarks/independent-acquisition-convergence-v2/partition-manifest.json",
}
FORBIDDEN_V2_GENERATION_SIGNATURES = (
    "WHU_IAC_V2_PARTITION",
    "holdout-labels.jsonl",
    '"seed_start"',
    '"seed_count"',
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict:
    files = []
    for rel in PUBLIC_FILES:
        path = ROOT / rel
        files.append({"path": rel, "sha256": digest(path), "bytes": path.stat().st_size})
    return {
        "schema_version": "1.0",
        "candidate_identifier": "WHU-WP-2026-09-30-v1.0.2",
        "reviewed_manuscript_baseline_commit": "1b2821f451dae0b895eb1c4f46b84e3638cf5636",
        "audit_parent_commit": "bdb618a9fab611c2e88684822381071394f46650",
        "release_authorized": True,
        "network_calls": 0,
        "model_or_provider_calls": 0,
        "files": files,
        "excluded_classes": [
            "raw provider requests and responses pending redistribution review",
            "unopened convergence V2 holdout contents",
            "subscriber or publication-administration data",
            "local receipts containing private paths, identities, or credentials",
            "conversation history and local Codex/ChatGPT state",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument(
        "--strict-tree",
        action="store_true",
        help="require the physical snapshot to contain exactly the manifest-listed files plus the manifest",
    )
    args = parser.parse_args()
    failures = []
    missing = [rel for rel in PUBLIC_FILES if not (ROOT / rel).is_file()]
    failures.extend(f"missing public candidate: {rel}" for rel in missing)
    if not missing:
        public_set = set(PUBLIC_FILES)
        for forbidden in sorted(public_set & FORBIDDEN_V2_PUBLIC_PATHS):
            failures.append(f"V2 holdout-capable artifact in public candidate: {forbidden}")
        scan_set = set(public_set)
        if args.strict_tree:
            actual_set = {
                path.relative_to(ROOT).as_posix()
                for path in ROOT.rglob("*")
                if path.is_file()
                and ".git" not in path.relative_to(ROOT).parts
                and "__pycache__" not in path.relative_to(ROOT).parts
                and path.suffix != ".pyc"
            }
            expected_set = public_set | {MANIFEST.relative_to(ROOT).as_posix()}
            for rel in sorted(actual_set - expected_set):
                failures.append(f"unlisted file in strict public snapshot: {rel}")
            for rel in sorted(expected_set - actual_set):
                failures.append(f"missing file in strict public snapshot: {rel}")
            scan_set = actual_set
        for forbidden in sorted(scan_set & FORBIDDEN_V2_PUBLIC_PATHS):
            failures.append(f"V2 holdout-capable artifact present in snapshot: {forbidden}")
        for rel in sorted(scan_set):
            path = ROOT / rel
            text = path.read_text(errors="replace")
            if "independent-acquisition-convergence-v2" in rel or "independent_acquisition_convergence_v2" in rel:
                for signature in FORBIDDEN_V2_GENERATION_SIGNATURES:
                    if signature in text and rel not in {
                        "tools/verify_working_paper_release.py",
                        "tools/verify_working_paper_custody.py",
                    }:
                        failures.append(f"V2 holdout-generation signature in {rel}: {signature}")
        for rel in PUBLIC_FILES:
            text = (ROOT / rel).read_text(errors="replace")
            for label, pattern in DENY_PATTERNS.items():
                if rel == "tools/verify_working_paper_release.py" and label in {
                    "private temporary path",
                    "local Codex path",
                }:
                    continue
                if pattern.search(text):
                    failures.append(f"{label} in {rel}")
            if rel.endswith(".md"):
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    if target.startswith(("https://", "http://", "#", "mailto:")):
                        continue
                    target = target.split("#", 1)[0]
                    resolved = ((ROOT / rel).parent / target).resolve()
                    try:
                        target_rel = resolved.relative_to(ROOT).as_posix()
                    except ValueError:
                        failures.append(f"out-of-repository Markdown target in {rel}: {target}")
                        continue
                    if target_rel not in public_set and target_rel != MANIFEST.relative_to(ROOT).as_posix():
                        failures.append(f"non-public Markdown target in {rel}: {target_rel}")

    if args.write_manifest:
        if failures:
            for failure in failures:
                print(f"- {failure}")
            raise SystemExit("refusing to write manifest: release scan failed")
        MANIFEST.write_text(json.dumps(payload(), indent=2) + "\n")
        print(f"WROTE: {MANIFEST.relative_to(ROOT)}")
        return

    if not MANIFEST.is_file():
        failures.append("missing public artifact manifest")
    elif not missing:
        recorded = json.loads(MANIFEST.read_text())
        expected = payload()
        if recorded != expected:
            failures.append("public artifact manifest differs from current candidate files")

    manuscript = (PKG / "WHU_WORKING_PAPER_MANUSCRIPT.md").read_text()
    for label in [
        "VALID_EMPIRICAL_EVIDENCE",
        "DESCRIPTIVE_OBSERVATION",
        "EXPLORATORY_POST_HOC_ANALYSIS",
        "INVALID/INDETERMINATE_EXPERIMENT",
        "METHODOLOGICAL_HISTORY",
    ]:
        if label not in manuscript:
            failures.append(f"missing evidence label in manuscript: {label}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    strict = "; strict physical tree verified" if args.strict_tree else ""
    print(f"PASS: {len(PUBLIC_FILES)} public-candidate files; hashes, paths, labels, and deny-list verified{strict}")


if __name__ == "__main__":
    main()
