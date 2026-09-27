#!/usr/bin/env python3
"""Build the frozen V3 acquisition-assurance dataset without fitting or evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "protocols/acquisition-assurance-calibration-poc-v3.json"
DATA_ROOT = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3"
BLUEPRINT_PATH = DATA_ROOT / "generator-blueprints.jsonl"
RUNTIME_PATH = DATA_ROOT / "runtime-observations.jsonl"
EVALUATOR_PATH = DATA_ROOT / "evaluator-labels.jsonl"
RECEIPT_PATH = ROOT / "docs/research/ACQUISITION_ASSURANCE_V3_SATISFIABILITY_RECEIPT.json"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Stream:
    def __init__(self, seed: int, domain: str, prefix: str = "WHU_AA_V3"):
        self.seed = seed
        self.domain = domain
        self.prefix = prefix
        self.counter = 0
        self.buffer = b""

    def _bytes(self, count: int) -> bytes:
        while len(self.buffer) < count:
            material = f"{self.prefix}|{self.seed}|{self.domain}|{self.counter}".encode()
            self.buffer += hashlib.sha256(material).digest()
            self.counter += 1
        result, self.buffer = self.buffer[:count], self.buffer[count:]
        return result

    def randbelow(self, upper: int) -> int:
        width = max(1, math.ceil(upper.bit_length() / 8))
        ceiling = (1 << (8 * width)) - ((1 << (8 * width)) % upper)
        while True:
            value = int.from_bytes(self._bytes(width), "big")
            if value < ceiling:
                return value % upper

    def randint(self, low: int, high: int) -> int:
        return low + self.randbelow(high - low + 1)

    def choice(self, values: list[Any]) -> Any:
        return values[self.randbelow(len(values))]

    def shuffle(self, values: list[Any]) -> list[Any]:
        result = list(values)
        for index in range(len(result) - 1, 0, -1):
            selected = self.randbelow(index + 1)
            result[index], result[selected] = result[selected], result[index]
        return result


def band(total: int) -> str:
    if total >= 5:
        return "STRONG"
    if total >= 1:
        return "DIRECTIONAL"
    if total >= -1:
        return "UNRESOLVED"
    return "OPPOSITE"


def partition(seed: int, spec: dict[str, Any]) -> str:
    p = spec["partition"]
    value = int.from_bytes(hashlib.sha256(f"{p['domain']}|{seed}".encode()).digest(), "big")
    return "HOLDOUT" if value % p["holdout_modulus"] == p["holdout_remainder"] else "CALIBRATION"


def weighted_contribution(stream: Stream, spec: dict[str, Any]) -> int:
    values = spec["generator"]["contribution_values"]
    weights = spec["generator"]["contribution_weights"]
    draw = stream.randbelow(sum(weights))
    cumulative = 0
    for value, weight in zip(values, weights, strict=True):
        cumulative += weight
        if draw < cumulative:
            return value
    raise AssertionError("unreachable")


def make_blueprint(seed: int, spec: dict[str, Any]) -> dict[str, Any]:
    generator = spec["generator"]
    shape = Stream(seed, "shape")
    record_count = shape.randint(*generator["record_count"])
    route_count = shape.randint(*generator["route_count"])
    route_width = min(shape.randint(*generator["route_width"]), record_count)
    class_count = shape.randint(*generator["evidence_class_count"])
    candidate_count = min(shape.randint(*generator["candidate_count"]), record_count)
    records = []
    contribution_stream = Stream(seed, "contributions")
    class_stream = Stream(seed, "classes")
    visibility_stream = Stream(seed, "visibility")
    families = [f"F{index:02d}" for index in range(1, record_count + 1)]
    for index, family in enumerate(families, 1):
        records.append({
            "record_id": f"V3-{seed}-R{index:02d}",
            "source_family_id": family,
            "evidence_class": f"E{class_stream.randint(1, class_count)}",
            "contribution": weighted_contribution(contribution_stream, spec),
            "visible": visibility_stream.randbelow(10) < 8,
        })
    route_stream = Stream(seed, "routes")
    routes = []
    visible = [record["source_family_id"] for record in records if record["visible"]]
    if not visible:
        records[0]["visible"] = True
        visible = [families[0]]
    for index in range(route_count):
        pool = route_stream.shuffle(visible)
        chosen = [pool[position % len(pool)] for position in range(route_width)]
        routes.append({
            "route_id": f"Q{index + 1}",
            "route_family": generator["route_families"][index % 3],
            "source_family_ids": sorted(set(chosen)),
        })
    candidate_stream = Stream(seed, "candidates")
    candidate_families = candidate_stream.shuffle(families)[:candidate_count]
    candidates = [
        {"candidate_id": f"C{index + 1}", "source_family_id": family,
         "surface_after_route": candidate_stream.randint(1, route_count)}
        for index, family in enumerate(candidate_families)
    ]
    policy_stream = Stream(seed, "policy")
    route_budget = policy_stream.randint(2, route_count)
    policy = policy_stream.choice(generator["policies"])
    return {
        "schema_version": "3.0",
        "seed": seed,
        "observation_id": f"AA3-{seed}",
        "partition": partition(seed, spec),
        "public_required_evidence_class_count": class_count,
        "policy": policy,
        "route_budget": route_budget,
        "yield_patience": policy_stream.choice([1, 2]),
        "resolve_candidates": bool(policy_stream.randbelow(2)),
        "records": records,
        "routes": routes,
        "candidates": candidates,
    }


def replay_features(runtime: dict[str, Any]) -> dict[str, Any]:
    events = runtime["events"]
    acquired = set(events[-1]["acquired_source_family_ids"]) if events else set()
    yields = [event["new_family_count"] for event in events]
    last_sets = [set(event["returned_source_family_ids"]) for event in events[-2:]]
    if len(last_sets) < 2:
        convergence = 0.0
    else:
        union = last_sets[0] | last_sets[1]
        overlap = len(last_sets[0] & last_sets[1]) / len(union) if union else 0.0
        convergence = 1.0 - overlap
    available_yields = yields[-2:]
    recent = sum(available_yields) / len(available_yields) / runtime["route_width"]
    route_families = {event["route_family"] for event in events}
    evidence_classes = {item for event in events for item in event["acquired_evidence_classes"]}
    zero_patience = len(yields) >= runtime["yield_patience"] and all(
        value == 0 for value in yields[-runtime["yield_patience"]:]
    )
    return {
        "source_count": len(acquired),
        "budget_fraction": round(len(events) / runtime["route_budget"], 8),
        "recent_marginal_yield": round(recent, 8),
        "route_family_coverage": round(len(route_families) / 3, 8),
        "evidence_class_coverage": round(
            len(evidence_classes) / runtime["public_required_evidence_class_count"], 8
        ),
        "unresolved_candidate_count": len(runtime["surfaced_unresolved_candidate_ids"]),
        "route_convergence": round(convergence, 8),
        "frontier_exhausted": int(
            not runtime["surfaced_unresolved_candidate_ids"]
            and (zero_patience or len(events) == runtime["route_budget"])
        ),
    }


def run_trajectory(blueprint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    record_map = {record["source_family_id"]: record for record in blueprint["records"]}
    acquired: set[str] = set()
    surfaced: set[str] = set()
    resolved: set[str] = set()
    events = []
    yields: list[int] = []
    action_count = 0
    for position, route in enumerate(blueprint["routes"][: blueprint["route_budget"]], 1):
        prior = set(acquired)
        returned = set(route["source_family_ids"])
        acquired.update(returned)
        new = acquired - prior
        yields.append(len(new))
        action_count += 1
        for candidate in blueprint["candidates"]:
            if candidate["surface_after_route"] <= position:
                surfaced.add(candidate["candidate_id"])
        resolutions = []
        if blueprint["resolve_candidates"]:
            for candidate in blueprint["candidates"]:
                if candidate["candidate_id"] in surfaced - resolved:
                    resolved.add(candidate["candidate_id"])
                    acquired.add(candidate["source_family_id"])
                    resolutions.append(candidate["candidate_id"])
                    action_count += 1
        events.append({
            "route_id": route["route_id"],
            "route_family": route["route_family"],
            "returned_source_family_ids": sorted(returned),
            "new_source_family_ids": sorted(new),
            "new_family_count": len(new),
            "acquired_source_family_ids": sorted(acquired),
            "acquired_evidence_classes": sorted({record_map[item]["evidence_class"] for item in acquired}),
            "resolved_candidate_ids": resolutions,
        })
        patience = blueprint["yield_patience"]
        zero_yield = len(yields) >= patience and all(value == 0 for value in yields[-patience:])
        coverage = len({record_map[item]["evidence_class"] for item in acquired}) == blueprint[
            "public_required_evidence_class_count"
        ]
        if blueprint["policy"] == "YIELD_PATIENCE" and zero_yield:
            break
        if blueprint["policy"] == "COVERAGE_YIELD" and zero_yield and coverage:
            break
    runtime = {
        "schema_version": "3.0",
        "observation_id": blueprint["observation_id"],
        "seed": blueprint["seed"],
        "partition": blueprint["partition"],
        "policy": blueprint["policy"],
        "route_budget": blueprint["route_budget"],
        "route_width": max(len(route["source_family_ids"]) for route in blueprint["routes"]),
        "yield_patience": blueprint["yield_patience"],
        "public_required_evidence_class_count": blueprint["public_required_evidence_class_count"],
        "events": events,
        "surfaced_unresolved_candidate_ids": sorted(surfaced - resolved),
        "action_count": action_count,
        "durable_stop": True,
    }
    runtime["x"] = replay_features(runtime)
    stopped_total = sum(record_map[item]["contribution"] for item in acquired)
    stopped_band = band(stopped_total)
    omitted = set(record_map) - acquired
    minimum = None
    for size in (1, 2):
        for package in combinations(sorted(omitted), size):
            if band(stopped_total + sum(record_map[item]["contribution"] for item in package)) != stopped_band:
                candidate_band = band(
                    stopped_total + sum(record_map[item]["contribution"] for item in package)
                )
                order = {"OPPOSITE": 0, "UNRESOLVED": 1, "DIRECTIONAL": 2, "STRONG": 3}
                if order[candidate_band] < order[stopped_band]:
                    minimum = size
                    break
        if minimum is not None:
            break
    evaluator = {
        "schema_version": "3.0",
        "observation_id": blueprint["observation_id"],
        "partition": blueprint["partition"],
        "y": int(minimum is not None),
        "stopped_band": stopped_band,
        "complete_band": band(sum(record["contribution"] for record in blueprint["records"])),
        "omitted_count": len(omitted),
        "minimum_weakening_package_size": minimum,
    }
    return runtime, evaluator


def rule_denominators(runtime_rows: list[dict[str, Any]], spec: dict[str, Any]) -> dict[str, int]:
    calibration = [row for row in runtime_rows if row["partition"] == "CALIBRATION"]
    counts: dict[str, int] = {}
    thresholds = spec["candidate_thresholds"]
    for value in thresholds["source_count"]:
        counts[f"B_SOURCE_COUNT__{value}"] = sum(row["x"]["source_count"] >= value for row in calibration)
    for value in thresholds["budget_fraction"]:
        counts[f"B_BUDGET__{value}"] = sum(row["x"]["budget_fraction"] >= value for row in calibration)
    for value in thresholds["recent_marginal_yield"]:
        counts[f"B_RECENT_YIELD__{value}"] = sum(
            row["x"]["recent_marginal_yield"] <= value for row in calibration
        )
    for coverage in thresholds["evidence_class_coverage"]:
        for marginal in thresholds["recent_marginal_yield"]:
            for unresolved in thresholds["unresolved_candidate_count"]:
                for frontier in thresholds["frontier_exhausted"]:
                    rule_id = f"C_DECISION_TABLE__{coverage}__{marginal}__{unresolved}__{frontier}"
                    counts[rule_id] = sum(
                        row["x"]["evidence_class_coverage"] >= coverage
                        and row["x"]["recent_marginal_yield"] <= marginal
                        and row["x"]["unresolved_candidate_count"] <= unresolved
                        and (not frontier or row["x"]["frontier_exhausted"] == 1)
                        for row in calibration
                    )
    return counts


def build(write: bool = True) -> dict[str, Any]:
    spec = json.loads(SPEC_PATH.read_text())
    seeds = range(spec["seed_start"], spec["seed_start"] + spec["seed_count"])
    blueprints, runtime_rows, evaluator_rows = [], [], []
    for seed in seeds:
        blueprint = make_blueprint(seed, spec)
        runtime, evaluator = run_trajectory(blueprint)
        blueprints.append(blueprint)
        runtime_rows.append(runtime)
        evaluator_rows.append(evaluator)
    class_counts = {part: {"0": 0, "1": 0} for part in ("CALIBRATION", "HOLDOUT")}
    for row in evaluator_rows:
        class_counts[row["partition"]][str(row["y"])] += 1
    minimums = spec["minimum_class_counts"]
    class_pass = all(class_counts[part][label] >= minimums[part][label] for part in minimums for label in minimums[part])
    runtime_ids = {row["observation_id"] for row in runtime_rows}
    evaluator_ids = {row["observation_id"] for row in evaluator_rows}
    calibration_ids = {row["observation_id"] for row in runtime_rows if row["partition"] == "CALIBRATION"}
    holdout_ids = runtime_ids - calibration_ids
    replay_pass = all(row["x"] == replay_features(row) for row in runtime_rows)
    prohibited = set(spec["prohibited_runtime_fields"])
    leakage_pass = all(not (prohibited & set(row)) and not (prohibited & set(row["x"])) for row in runtime_rows)
    partition_pass = not (calibration_ids & holdout_ids) and len(runtime_ids) == spec["seed_count"] and all(
        row["partition"] == partition(row["seed"], spec) for row in runtime_rows
    )
    denominators = rule_denominators(runtime_rows, spec)
    denominator_pass = all(value > 0 for value in denominators.values())
    requirements = [
        {"id": "both_y_classes_non_vacuous", "status": "PASS" if class_pass else "FAIL", "witness": class_counts},
        {"id": "hidden_label_separation", "status": "PASS" if leakage_pass else "FAIL", "witness": {"prohibited_fields": sorted(prohibited)}},
        {"id": "feature_replay", "status": "PASS" if replay_pass else "FAIL", "witness": {"replayed": len(runtime_rows)}},
        {"id": "partition_integrity", "status": "PASS" if partition_pass else "FAIL", "witness": {"calibration": len(calibration_ids), "holdout": len(holdout_ids), "intersection": len(calibration_ids & holdout_ids)}},
        {"id": "metric_denominators", "status": "PASS" if denominator_pass else "FAIL", "witness": {"rules": len(denominators), "minimum_assured": min(denominators.values()), "maximum_assured": max(denominators.values())}},
        {"id": "rule_families_fully_specified", "status": "PASS", "witness": {"families": spec["candidate_families"], "threshold_rule_count": len(denominators), "selection_rule": spec["selection_rule"]}},
        {"id": "seed_selection_independence", "status": "PASS", "witness": {"requested": spec["seed_count"], "accepted": len(blueprints), "rejected": 0, "replacement": 0}},
        {"id": "dataset_join_integrity", "status": "PASS" if runtime_ids == evaluator_ids else "FAIL", "witness": {"runtime": len(runtime_ids), "evaluator": len(evaluator_ids)}},
    ]
    receipt = {
        "schema_version": "3.0",
        "design_id": spec["protocol_id"],
        "overall": "PASS" if all(item["status"] == "PASS" for item in requirements) else "FAIL",
        "empirical_evaluation_performed": False,
        "model_fitting_performed": False,
        "requirements": requirements,
    }
    if write:
        DATA_ROOT.mkdir(parents=True, exist_ok=True)
        for path, rows in ((BLUEPRINT_PATH, blueprints), (RUNTIME_PATH, runtime_rows), (EVALUATOR_PATH, evaluator_rows)):
            path.write_bytes(b"".join(canonical(row) for row in rows))
        RECEIPT_PATH.write_bytes(canonical(receipt))
    if receipt["overall"] != "PASS":
        raise SystemExit(json.dumps(receipt, sort_keys=True))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "verify"])
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build(write=True), sort_keys=True))
        return
    expected = {path: file_hash(path) for path in (BLUEPRINT_PATH, RUNTIME_PATH, EVALUATOR_PATH, RECEIPT_PATH)}
    build(write=True)
    actual = {path: file_hash(path) for path in expected}
    if expected != actual:
        raise SystemExit("frozen V3 artifacts do not reproduce")
    print(json.dumps({"overall": "PASS", "verified": {str(path.relative_to(ROOT)): value for path, value in actual.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
