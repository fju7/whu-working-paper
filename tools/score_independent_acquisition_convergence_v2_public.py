#!/usr/bin/env python3
"""Public calibration-only V2 scoring primitives.

This module has no generator, seed/partition recipe, authorization path, or protected partition path.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "protocols/independent-acquisition-convergence-v2-public-calibration.json"
RUNTIME = ROOT / "benchmarks/independent-acquisition-convergence-v2/calibration-runtime-observations.jsonl"
CALIBRATION_LABELS = ROOT / "benchmarks/independent-acquisition-convergence-v2/calibration-labels.jsonl"
CALIBRATION_RESULT = ROOT / "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json"

def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]

def jaccard(left: set[str], right: set[str]) -> float:
    return 1.0 if not left | right else len(left & right) / len(left | right)

def convergence(left: dict[str, Any], right: dict[str, Any], rec: dict[str, Any], rule: dict[str, Any]) -> bool:
    left_contrary = any(r["direction"] == "CONTRARY" for r in left["acquired_records"])
    right_contrary = any(r["direction"] == "CONTRARY" for r in right["acquired_records"])
    return rec["family_jaccard"] >= rule["family_jaccard_min"] and rec["pivotal_jaccard"] >= rule["pivotal_jaccard_min"] and left["x"]["evidence_class_coverage"] >= rule["evidence_class_coverage_min_each"] and right["x"]["evidence_class_coverage"] >= rule["evidence_class_coverage_min_each"] and (not rule["require_claim_band_agreement"] or left["stopped_claim_band"] == right["stopped_claim_band"]) and (not rule["require_contrary_presence_agreement"] or left_contrary == right_contrary)

def decision(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    return convergence(row["process_a"], row["process_b"], row["reconciliation"], rule)

def baselines(spec: dict[str, Any]) -> dict[str, Callable[[dict[str, Any]], bool]]:
    rules = spec["baselines"]
    def marginal(row: dict[str, Any]) -> bool:
        events = [e for p in (row["process_a"], row["process_b"]) for e in p["events"]]
        recent = [p["events"][-1] for p in (row["process_a"], row["process_b"])]
        return sum(e["new_family_count"] for e in recent) / sum(len(e["returned_records"]) for e in recent) <= rules["MARGINAL_YIELD"]["pooled_recent_marginal_yield_max"]
    return {
        "SEARCH_VOLUME": lambda row: row["reconciliation"]["pooled_source_count"] >= rules["SEARCH_VOLUME"]["pooled_source_count_min"],
        "MARGINAL_YIELD": marginal,
        "COVERAGE_STOPPING": lambda row: row["process_a"]["x"]["evidence_class_coverage"] >= rules["COVERAGE_STOPPING"]["evidence_class_coverage_min_each"] and row["process_b"]["x"]["evidence_class_coverage"] >= rules["COVERAGE_STOPPING"]["evidence_class_coverage_min_each"],
    }

def fraction(numerator: int, denominator: int) -> dict[str, Any]:
    return {"numerator": numerator, "denominator": denominator, "rate": None if denominator == 0 else numerator / denominator}

def assurance(rows: list[dict[str, Any]], labels: dict[str, dict[str, Any]], selector: Callable[[dict[str, Any]], bool]) -> dict[str, Any]:
    yes, no = [r for r in rows if selector(r)], [r for r in rows if not selector(r)]
    return {"false_assurance": fraction(sum(labels[r["observation_id"]]["y"] for r in yes), len(yes)), "assurance_coverage": fraction(len(yes), len(rows)), "false_withholding": fraction(sum(1 - labels[r["observation_id"]]["y"] for r in no), len(no))}

def chance_count(rows: list[dict[str, Any]], spec: dict[str, Any]) -> int:
    ordered = sorted(rows, key=lambda r: hashlib.sha256(f"WHU_IAC_V2_CHANCE|{r['observation_id']}".encode()).hexdigest())
    shift, count = spec["chance_agreement_comparator"]["shift"] % len(ordered), 0
    for index, left_row in enumerate(ordered):
        left, right = left_row["process_a"], ordered[(index + shift) % len(ordered)]["process_b"]
        left_ids = {r["source_family_id"] for r in left["acquired_records"]}; right_ids = {r["source_family_id"] for r in right["acquired_records"]}
        left_piv = {r["source_family_id"] for r in left["acquired_records"] if r["magnitude_class"] == "PIVOTAL"}; right_piv = {r["source_family_id"] for r in right["acquired_records"] if r["magnitude_class"] == "PIVOTAL"}
        count += int(convergence(left, right, {"family_jaccard": jaccard(left_ids, right_ids), "pivotal_jaccard": jaccard(left_piv, right_piv)}, spec["convergence_rule"]))
    return count

def score_calibration() -> dict[str, Any]:
    spec = json.loads(SPEC.read_text())
    rows = read_jsonl(RUNTIME)
    labels = {r["observation_id"]: r for r in read_jsonl(CALIBRATION_LABELS)}
    primary = assurance(rows, labels, lambda r: decision(r, spec["convergence_rule"]))
    baseline_results = {name: assurance(rows, labels, fn) for name, fn in baselines(spec).items()}
    disagreement = [r for r in rows if r["reconciliation"]["claim_band_disagreement"] == 1]
    observed, chance = primary["assurance_coverage"]["numerator"], chance_count(rows, spec)
    eligible = {n: v for n, v in baseline_results.items() if v["assurance_coverage"]["rate"] >= spec["primary_gate"]["baseline_minimum_coverage"] and v["false_assurance"]["denominator"]}
    best = min((v["false_assurance"]["rate"] for v in eligible.values()), default=None)
    relative = None if best in (None, 0) else (best - primary["false_assurance"]["rate"]) / best
    chance_ratio = None if chance == 0 else observed / chance
    gate = spec["primary_gate"]
    passed = primary["false_assurance"]["rate"] is not None and primary["false_assurance"]["rate"] <= gate["maximum_false_assurance"] and primary["assurance_coverage"]["rate"] >= gate["minimum_assurance_coverage"] and relative is not None and relative >= gate["minimum_relative_false_assurance_reduction_vs_best_eligible_baseline"] and chance_ratio is not None and chance_ratio >= gate["minimum_convergence_rate_ratio_vs_fixed_permutation_chance"]
    agreement = [r for r in rows if r["reconciliation"]["claim_band_disagreement"] == 0]
    disagreement_rate = fraction(sum(labels[r["observation_id"]]["y"] for r in disagreement), len(disagreement))
    agreement_rate = fraction(sum(labels[r["observation_id"]]["y"] for r in agreement), len(agreement))
    enrichment = None if agreement_rate["rate"] in (None, 0) else disagreement_rate["rate"] / agreement_rate["rate"]
    route_uses = sum(r["process_a"]["x"]["routes_used"] + r["process_b"]["x"]["routes_used"] for r in rows)
    return {"schema_version": "2.0", "experiment_id": spec["experiment_id"], "partition": "CALIBRATION", "primary": primary, "baselines": baseline_results, "disagreement_enrichment": {"disagreement_hidden_omission": disagreement_rate, "agreement_hidden_omission": agreement_rate, "rate_ratio": enrichment}, "acquisition_cost": {"routes_used": route_uses, "observations": len(rows), "mean_routes_per_observation": route_uses / len(rows)}, "chance_agreement": {"observed_convergence": fraction(observed, len(rows)), "fixed_permutation_convergence": fraction(chance, len(rows)), "observed_to_chance_ratio": chance_ratio}, "gate_inputs": {"eligible_baselines": sorted(eligible), "best_eligible_baseline_false_assurance": best, "relative_false_assurance_reduction": relative}, "primary_gate_passed": passed}

if __name__ == "__main__":
    reproduced = score_calibration()
    if canonical(reproduced) != CALIBRATION_RESULT.read_bytes():
        raise SystemExit("FAIL: calibration result mismatch")
    print("PASS: convergence V2 calibration result recomputed")
