#!/usr/bin/env python3
"""Build the prospectively frozen independent-acquisition convergence dataset."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "protocols/independent-acquisition-convergence-v1.json"
DATA_ROOT = ROOT / "benchmarks/independent-acquisition-convergence-v1"
BLUEPRINT_PATH = DATA_ROOT / "generator-blueprints.jsonl"
RUNTIME_PATH = DATA_ROOT / "runtime-observations.jsonl"
EVALUATOR_PATH = DATA_ROOT / "evaluator-labels.jsonl"
RECEIPT_PATH = ROOT / "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V1_SATISFIABILITY_RECEIPT.json"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Stream:
    def __init__(self, seed: int, domain: str):
        self.seed = seed
        self.domain = domain
        self.counter = 0
        self.buffer = b""

    def _bytes(self, count: int) -> bytes:
        while len(self.buffer) < count:
            material = f"WHU_IAC_V1|{self.seed}|{self.domain}|{self.counter}".encode()
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


def observable(record: dict[str, Any]) -> dict[str, Any]:
    contribution = record["contribution"]
    return {
        "source_family_id": record["source_family_id"],
        "evidence_class": record["evidence_class"],
        "direction": "CONTRARY" if contribution < 0 else "SUPPORTIVE" if contribution > 0 else "NEUTRAL",
        "magnitude_class": "PIVOTAL" if abs(contribution) >= 2 else "ORDINARY",
    }


def make_blueprint(seed: int, spec: dict[str, Any]) -> dict[str, Any]:
    generator = spec["generator"]
    shape = Stream(seed, "SHAPE")
    record_count = shape.randint(*generator["record_count"])
    class_count = shape.randint(*generator["evidence_class_count"])
    route_count = shape.randint(*generator["route_count"])
    route_width = min(shape.randint(*generator["route_width"]), record_count)
    contributions = Stream(seed, "CONTRIBUTIONS")
    classes = Stream(seed, "CLASSES")
    records = [
        {
            "source_family_id": f"F{index:02d}",
            "evidence_class": f"E{classes.randint(1, class_count)}",
            "contribution": weighted_contribution(contributions, spec),
        }
        for index in range(1, record_count + 1)
    ]
    processes = {}
    for process_id in ("A", "B"):
        stream = Stream(seed, spec["processes"][process_id]["random_domain"])
        routes = []
        family_ids = [record["source_family_id"] for record in records]
        for index in range(route_count):
            chosen = stream.shuffle(family_ids)[:route_width]
            routes.append({
                "route_id": f"{process_id}Q{index + 1}",
                "route_family": generator["route_families"][stream.randbelow(3)],
                "source_family_ids": sorted(chosen),
                "public_priority": stream.randbelow(1000),
            })
        processes[process_id] = {
            "route_budget": min(stream.randint(*generator["route_budget"]), route_count),
            "routes": routes,
            "route_policy": spec["processes"][process_id]["route_policy"],
            "stop_policy": spec["processes"][process_id]["stop_policy"],
        }
    return {
        "schema_version": "1.0",
        "seed": seed,
        "observation_id": f"IAC1-{seed}",
        "partition": partition(seed, spec),
        "public_required_evidence_class_count": class_count,
        "records": records,
        "processes": processes,
    }


def run_process(blueprint: dict[str, Any], process_id: str) -> dict[str, Any]:
    record_map = {record["source_family_id"]: record for record in blueprint["records"]}
    config = blueprint["processes"][process_id]
    remaining = list(config["routes"])
    acquired: set[str] = set()
    events = []
    while remaining and len(events) < config["route_budget"]:
        if process_id == "A":
            def key(route: dict[str, Any]) -> tuple[int, int, str]:
                classes = {record_map[item]["evidence_class"] for item in route["source_family_ids"]}
                seen = {record_map[item]["evidence_class"] for item in acquired}
                return (len(classes & seen), route["public_priority"], route["route_id"])
            selected = min(remaining, key=key)
        else:
            def key(route: dict[str, Any]) -> tuple[int, int, str]:
                novelty = len(set(route["source_family_ids"]) - acquired)
                return (-novelty, route["public_priority"], route["route_id"])
            selected = min(remaining, key=key)
        remaining.remove(selected)
        returned = set(selected["source_family_ids"])
        new = returned - acquired
        acquired.update(returned)
        events.append({
            "route_id": selected["route_id"],
            "route_family": selected["route_family"],
            "returned_records": [observable(record_map[item]) for item in sorted(returned)],
            "new_family_count": len(new),
            "acquired_source_family_ids": sorted(acquired),
        })
        if process_id == "A" and len(events) >= 2 and all(event["new_family_count"] == 0 for event in events[-2:]):
            break
        acquired_classes = {record_map[item]["evidence_class"] for item in acquired}
        if process_id == "B" and len(acquired_classes) == blueprint["public_required_evidence_class_count"] and events[-1]["new_family_count"] == 0:
            break
    acquired_records = [record_map[item] for item in sorted(acquired)]
    return {
        "process_id": process_id,
        "policy_id": config["route_policy"],
        "stop_policy_id": config["stop_policy"],
        "route_budget": config["route_budget"],
        "events": events,
        "acquired_records": [observable(record) for record in acquired_records],
        "stopped_claim_band": band(sum(record["contribution"] for record in acquired_records)),
        "frontier_exhausted": len(events) == config["route_budget"],
        "unresolved_candidate_count": 0,
    }


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def process_features(process: dict[str, Any], required_classes: int) -> dict[str, Any]:
    records = process["acquired_records"]
    classes = {record["evidence_class"] for record in records}
    yields = [event["new_family_count"] / max(1, len(event["returned_records"])) for event in process["events"][-2:]]
    return {
        "source_count": len(records),
        "evidence_class_coverage": round(len(classes) / required_classes, 8),
        "recent_marginal_yield": round(sum(yields) / len(yields), 8),
        "routes_used": len(process["events"]),
        "frontier_exhausted": int(process["frontier_exhausted"]),
    }


def reconcile(blueprint: dict[str, Any], left: dict[str, Any], right: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    record_map = {record["source_family_id"]: record for record in blueprint["records"]}
    left_ids = {record["source_family_id"] for record in left["acquired_records"]}
    right_ids = {record["source_family_id"] for record in right["acquired_records"]}
    union_ids = left_ids | right_ids
    left_pivotal = {record["source_family_id"] for record in left["acquired_records"] if record["magnitude_class"] == "PIVOTAL"}
    right_pivotal = {record["source_family_id"] for record in right["acquired_records"] if record["magnitude_class"] == "PIVOTAL"}
    left_contrary = {record["source_family_id"] for record in left["acquired_records"] if record["direction"] == "CONTRARY"}
    right_contrary = {record["source_family_id"] for record in right["acquired_records"] if record["direction"] == "CONTRARY"}
    left_x = process_features(left, blueprint["public_required_evidence_class_count"])
    right_x = process_features(right, blueprint["public_required_evidence_class_count"])
    stopped_total = sum(record_map[item]["contribution"] for item in union_ids)
    stopped_band = band(stopped_total)
    omitted = set(record_map) - union_ids
    minimum = None
    for size in (1, 2):
        for package in combinations(sorted(omitted), size):
            candidate_band = band(stopped_total + sum(record_map[item]["contribution"] for item in package))
            order = {"OPPOSITE": 0, "UNRESOLVED": 1, "DIRECTIONAL": 2, "STRONG": 3}
            if order[candidate_band] < order[stopped_band]:
                minimum = size
                break
        if minimum is not None:
            break
    convergence = {
        "family_jaccard": round(jaccard(left_ids, right_ids), 8),
        "pivotal_jaccard": round(jaccard(left_pivotal, right_pivotal), 8),
        "contrary_presence_agreement": int(bool(left_contrary) == bool(right_contrary)),
        "claim_band_agreement": int(left["stopped_claim_band"] == right["stopped_claim_band"]),
        "claim_band_disagreement": int(left["stopped_claim_band"] != right["stopped_claim_band"]),
    }
    runtime = {
        "schema_version": "1.0",
        "observation_id": blueprint["observation_id"],
        "seed": blueprint["seed"],
        "partition": blueprint["partition"],
        "required_evidence_class_count": blueprint["public_required_evidence_class_count"],
        "process_a": {**left, "x": left_x},
        "process_b": {**right, "x": right_x},
        "reconciliation": {
            "union_source_family_ids": sorted(union_ids),
            "pooled_source_count": len(union_ids),
            "pooled_recent_marginal_yield": round((left_x["recent_marginal_yield"] + right_x["recent_marginal_yield"]) / 2, 8),
            "stopped_claim_band": stopped_band,
            **convergence,
        },
    }
    evaluator = {
        "schema_version": "1.0",
        "observation_id": blueprint["observation_id"],
        "partition": blueprint["partition"],
        "y": int(minimum is not None),
        "complete_band": band(sum(record["contribution"] for record in blueprint["records"])),
        "omitted_count": len(omitted),
        "minimum_weakening_package_size": minimum,
        "exhaustive_union": int(not omitted),
    }
    return runtime, evaluator


def convergence_decision(row: dict[str, Any], spec: dict[str, Any]) -> bool:
    rule = spec["convergence_rule"]
    reconciliation = row["reconciliation"]
    return (
        reconciliation["family_jaccard"] >= rule["family_jaccard_min"]
        and reconciliation["pivotal_jaccard"] >= rule["pivotal_jaccard_min"]
        and row["process_a"]["x"]["evidence_class_coverage"] >= rule["evidence_class_coverage_min_each"]
        and row["process_b"]["x"]["evidence_class_coverage"] >= rule["evidence_class_coverage_min_each"]
        and reconciliation["pooled_recent_marginal_yield"] <= rule["pooled_recent_marginal_yield_max"]
        and (not rule["require_claim_band_agreement"] or reconciliation["claim_band_agreement"] == 1)
        and (not rule["require_contrary_presence_agreement"] or reconciliation["contrary_presence_agreement"] == 1)
        and (not rule["require_no_unresolved_candidates"] or (
            row["process_a"]["unresolved_candidate_count"] == 0
            and row["process_b"]["unresolved_candidate_count"] == 0
        ))
    )


def baseline_decisions(row: dict[str, Any], spec: dict[str, Any]) -> dict[str, bool]:
    baselines = spec["baselines"]
    reconciliation = row["reconciliation"]
    return {
        "SEARCH_VOLUME": reconciliation["pooled_source_count"] >= baselines["SEARCH_VOLUME"]["pooled_source_count_min"],
        "MARGINAL_YIELD": reconciliation["pooled_recent_marginal_yield"] <= baselines["MARGINAL_YIELD"]["pooled_recent_marginal_yield_max"],
        "COVERAGE_STOPPING": (
            row["process_a"]["x"]["evidence_class_coverage"] >= baselines["COVERAGE_STOPPING"]["evidence_class_coverage_min_each"]
            and row["process_b"]["x"]["evidence_class_coverage"] >= baselines["COVERAGE_STOPPING"]["evidence_class_coverage_min_each"]
            and (not baselines["COVERAGE_STOPPING"]["require_both_frontier_exhausted"] or (
                row["process_a"]["x"]["frontier_exhausted"] == 1
                and row["process_b"]["x"]["frontier_exhausted"] == 1
            ))
        ),
    }


def build(write: bool = True) -> dict[str, Any]:
    spec = json.loads(SPEC_PATH.read_text())
    blueprints, runtime_rows, evaluator_rows = [], [], []
    for seed in range(spec["seed_start"], spec["seed_start"] + spec["seed_count"]):
        blueprint = make_blueprint(seed, spec)
        left = run_process(blueprint, "A")
        right = run_process(blueprint, "B")
        runtime, evaluator = reconcile(blueprint, left, right)
        blueprints.append(blueprint)
        runtime_rows.append(runtime)
        evaluator_rows.append(evaluator)
    labels = {row["observation_id"]: row for row in evaluator_rows}
    class_counts = {part: {"0": 0, "1": 0} for part in ("CALIBRATION", "HOLDOUT")}
    for row in evaluator_rows:
        class_counts[row["partition"]][str(row["y"])] += 1
    assured_counts = {part: 0 for part in ("CALIBRATION", "HOLDOUT")}
    disagreement_counts = {part: 0 for part in ("CALIBRATION", "HOLDOUT")}
    exhaustive_counts = {part: 0 for part in ("CALIBRATION", "HOLDOUT")}
    for row in runtime_rows:
        part = row["partition"]
        assured_counts[part] += int(convergence_decision(row, spec))
        disagreement_counts[part] += row["reconciliation"]["claim_band_disagreement"]
        exhaustive_counts[part] += labels[row["observation_id"]]["exhaustive_union"]
    partition_counts = {part: sum(row["partition"] == part for row in runtime_rows) for part in assured_counts}
    minimums = spec["non_vacuity"]
    class_pass = all(class_counts[part][label] >= minimums["minimum_y_each_partition"][part] for part in class_counts for label in ("0", "1"))
    assurance_pass = (
        assured_counts["HOLDOUT"] >= minimums["minimum_assured_count_holdout"]
        and assured_counts["HOLDOUT"] / partition_counts["HOLDOUT"] >= minimums["minimum_assurance_coverage"]
    )
    disagreement_pass = disagreement_counts["HOLDOUT"] >= minimums["minimum_disagreement_count_holdout"]
    exhaustive_pass = all(exhaustive_counts[part] / partition_counts[part] <= minimums["maximum_exhaustive_union_fraction"] for part in partition_counts)
    prohibited = set(spec["prohibited_runtime_fields"])
    leakage_pass = all(not prohibited.intersection(json.dumps(row).split('"')) for row in runtime_rows)
    independence_pass = all(
        blueprint["processes"]["A"]["routes"] != blueprint["processes"]["B"]["routes"]
        and blueprint["processes"]["A"]["route_policy"] != blueprint["processes"]["B"]["route_policy"]
        for blueprint in blueprints
    )
    requirements = [
        {"id": "both_omission_outcomes_adequate", "status": "PASS" if class_pass else "FAIL", "witness": class_counts},
        {"id": "convergence_non_vacuous", "status": "PASS" if assurance_pass else "FAIL", "witness": assured_counts},
        {"id": "disagreement_non_vacuous", "status": "PASS" if disagreement_pass else "FAIL", "witness": disagreement_counts},
        {"id": "convergence_not_trivial_exhaustion", "status": "PASS" if exhaustive_pass else "FAIL", "witness": exhaustive_counts},
        {"id": "independent_process_mechanisms", "status": "PASS" if independence_pass else "FAIL", "witness": {"separate_domains": [spec["processes"]["A"]["random_domain"], spec["processes"]["B"]["random_domain"]]}},
        {"id": "hidden_labels_absent_from_runtime", "status": "PASS" if leakage_pass else "FAIL", "witness": {"prohibited_fields": sorted(prohibited)}},
        {"id": "metrics_and_gates_computable", "status": "PASS", "witness": {"rows": len(runtime_rows)}},
    ]
    receipt = {
        "schema_version": "1.0",
        "experiment_id": spec["experiment_id"],
        "overall": "PASS" if all(item["status"] == "PASS" for item in requirements) else "FAIL",
        "requirements": requirements,
        "empirical_holdout_evaluation_performed": False,
        "semantic_or_model_calls": 0,
    }
    if write:
        DATA_ROOT.mkdir(parents=True, exist_ok=True)
        for path, rows in ((BLUEPRINT_PATH, blueprints), (RUNTIME_PATH, runtime_rows), (EVALUATOR_PATH, evaluator_rows)):
            path.write_bytes(b"".join(canonical(row) for row in rows))
        receipt["frozen_hashes"] = {
            "spec": file_hash(SPEC_PATH),
            "builder": file_hash(Path(__file__)),
            "blueprints": file_hash(BLUEPRINT_PATH),
            "runtime": file_hash(RUNTIME_PATH),
            "evaluator": file_hash(EVALUATOR_PATH),
        }
        RECEIPT_PATH.write_bytes(canonical(receipt))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "check"])
    args = parser.parse_args()
    receipt = build(write=args.command == "build")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if receipt["overall"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
