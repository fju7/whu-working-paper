#!/usr/bin/env python3
"""Prospectively specified V3 scorer. Execution is governance-locked.

This file is reviewable apparatus, not authorization. The current directive prohibits
running either command and no authorization token is issued by this repository state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "protocols/acquisition-assurance-calibration-poc-v3.json"
RUNTIME_PATH = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3/runtime-observations.jsonl"
EVALUATOR_PATH = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3/evaluator-labels.jsonl"
MODEL_PATH = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3/frozen-calibration-model.json"
RESULT_PATH = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3/holdout-results.json"
CLAIM_PATH = ROOT / "benchmarks/acquisition-assurance-calibration-poc-v3/holdout-consumption-claim.json"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def joined_rows(partition: str) -> list[dict[str, Any]]:
    runtime = {row["observation_id"]: row for row in read_rows(RUNTIME_PATH)}
    labels = {row["observation_id"]: row for row in read_rows(EVALUATOR_PATH)}
    if set(runtime) != set(labels):
        raise ValueError("runtime/evaluator join mismatch")
    if any(runtime[key]["partition"] != labels[key]["partition"] for key in runtime):
        raise ValueError("runtime/evaluator partition mismatch")
    return [
        {**runtime[key], "y": labels[key]["y"]}
        for key in sorted(runtime)
        if runtime[key]["partition"] == partition and labels[key]["partition"] == partition
    ]


def threshold_rules(spec: dict[str, Any]) -> dict[str, Callable[[dict[str, Any]], bool]]:
    thresholds = spec["candidate_thresholds"]
    rules: dict[str, Callable[[dict[str, Any]], bool]] = {}
    for value in thresholds["source_count"]:
        rules[f"B_SOURCE_COUNT__{value}"] = lambda x, value=value: x["source_count"] >= value
    for value in thresholds["budget_fraction"]:
        rules[f"B_BUDGET__{value}"] = lambda x, value=value: x["budget_fraction"] >= value
    for value in thresholds["recent_marginal_yield"]:
        rules[f"B_RECENT_YIELD__{value}"] = lambda x, value=value: x["recent_marginal_yield"] <= value
    for coverage in thresholds["evidence_class_coverage"]:
        for marginal in thresholds["recent_marginal_yield"]:
            for unresolved in thresholds["unresolved_candidate_count"]:
                for frontier in thresholds["frontier_exhausted"]:
                    rule_id = f"C_DECISION_TABLE__{coverage}__{marginal}__{unresolved}__{frontier}"
                    rules[rule_id] = lambda x, c=coverage, m=marginal, u=unresolved, f=frontier: (
                        x["evidence_class_coverage"] >= c
                        and x["recent_marginal_yield"] <= m
                        and x["unresolved_candidate_count"] <= u
                        and (not f or x["frontier_exhausted"] == 1)
                    )
    return rules


def metrics(rows: list[dict[str, Any]], decisions: list[bool]) -> dict[str, Any]:
    assured = [row for row, decision in zip(rows, decisions, strict=True) if decision]
    y0 = [row for row in rows if row["y"] == 0]
    withheld_y0 = sum(not decision and row["y"] == 0 for row, decision in zip(rows, decisions, strict=True))
    return {
        "assured_count": len(assured),
        "assurance_coverage": len(assured) / len(rows),
        "false_assurance_numerator": sum(row["y"] == 1 for row in assured),
        "false_assurance_denominator": len(assured),
        "false_assurance": None if not assured else sum(row["y"] == 1 for row in assured) / len(assured),
        "false_withholding_numerator": withheld_y0,
        "false_withholding_denominator": len(y0),
        "false_withholding_given_y0": None if not y0 else withheld_y0 / len(y0),
        "mean_routes": sum(len(row["events"]) for row in assured) / len(assured) if assured else None,
        "mean_actions": sum(row["action_count"] for row in assured) / len(assured) if assured else None,
        "mean_source_count": sum(row["x"]["source_count"] for row in assured) / len(assured) if assured else None,
    }


def fit_logistic(rows: list[dict[str, Any]], features: list[str]) -> dict[str, Any]:
    means = {name: sum(row["x"][name] for row in rows) / len(rows) for name in features}
    scales = {}
    for name in features:
        variance = sum((row["x"][name] - means[name]) ** 2 for row in rows) / len(rows)
        scales[name] = math.sqrt(variance) or 1.0
    weights = [0.0] * (len(features) + 1)
    # Frozen full-batch gradient descent: 2,000 steps, learning rate 0.05.
    for _ in range(2000):
        gradient = [0.0] * len(weights)
        for row in rows:
            values = [1.0] + [(row["x"][name] - means[name]) / scales[name] for name in features]
            score = sum(weight * value for weight, value in zip(weights, values, strict=True))
            probability = 1.0 / (1.0 + math.exp(-max(-35.0, min(35.0, score))))
            for index, value in enumerate(values):
                gradient[index] += (probability - row["y"]) * value
        weights = [weight - 0.05 * value / len(rows) for weight, value in zip(weights, gradient, strict=True)]
    return {"features": features, "means": means, "scales": scales, "weights": weights, "cutoff": 0.5}


def logistic_decision(x: dict[str, Any], model: dict[str, Any]) -> bool:
    values = [1.0] + [(x[name] - model["means"][name]) / model["scales"][name] for name in model["features"]]
    score = sum(weight * value for weight, value in zip(model["weights"], values, strict=True))
    probability_y1 = 1.0 / (1.0 + math.exp(-max(-35.0, min(35.0, score))))
    return probability_y1 < model["cutoff"]


def require_authorization(value: str | None) -> None:
    if not value or not value.startswith("OWNER_AUTHORIZED_"):
        raise SystemExit("empirical fitting/evaluation is not authorized by the current directive")


def bound_hashes() -> dict[str, str]:
    paths = {
        "runtime": RUNTIME_PATH,
        "evaluator": EVALUATOR_PATH,
        "spec": SPEC_PATH,
        "scorer": Path(__file__).resolve(),
    }
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}


def verify_model_bindings(model: dict[str, Any]) -> None:
    if model.get("bound_hashes") != bound_hashes():
        raise ValueError("calibration freeze does not match current dataset/spec/scorer bytes")
    if model.get("holdout_evaluated") is not False:
        raise ValueError("holdout already consumed")
    if model.get("freeze_id") != "WHU-ACQUISITION-ASSURANCE-CALIBRATION-MODEL-V3":
        raise ValueError("unknown calibration freeze")


def claim_holdout(authorization: str, model: dict[str, Any]) -> None:
    claim = {
        "schema_version": "1.0",
        "status": "HOLDOUT_CONSUMED__RESULT_MAY_BE_PENDING_OR_FAILED",
        "authorization": authorization,
        "calibration_freeze_id": model["freeze_id"],
        "calibration_model_sha256": hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest(),
        "recovery": "OWNER_ACTION_REQUIRED_NO_AUTOMATIC_RETRY",
    }
    # Exclusive creation is the atomic claim. It occurs before any holdout row is read.
    with CLAIM_PATH.open("xb") as handle:
        handle.write(canonical(claim))


def calibrate(authorization: str) -> None:
    require_authorization(authorization)
    spec = json.loads(SPEC_PATH.read_text())
    rows = joined_rows("CALIBRATION")
    candidates: dict[str, list[tuple[float, float, str, dict[str, Any]]]] = {
        "B_SOURCE_COUNT": [],
        "B_BUDGET": [],
        "B_RECENT_YIELD": [],
        "C_DECISION_TABLE": [],
    }
    for rule_id, rule in threshold_rules(spec).items():
        result = metrics(rows, [rule(row["x"]) for row in rows])
        if result["assurance_coverage"] >= spec["selection_rule"]["minimum_calibration_coverage"]:
            family = next(name for name in candidates if rule_id.startswith(name + "__"))
            candidates[family].append(
                (result["false_assurance"], -result["assurance_coverage"], rule_id, result)
            )
    winners = {family: min(values) for family, values in candidates.items()}
    logistic = fit_logistic(rows, spec["features"])
    payload = {
        "schema_version": "3.0",
        "freeze_id": "WHU-ACQUISITION-ASSURANCE-CALIBRATION-MODEL-V3",
        "authorization": authorization,
        "selected_threshold_rules": {
            family: {"rule_id": winner[2], "calibration_metrics": winner[3]}
            for family, winner in winners.items()
        },
        "logistic": logistic,
        "bound_hashes": bound_hashes(),
        "holdout_evaluated": False,
    }
    with MODEL_PATH.open("xb") as handle:
        handle.write(canonical(payload))


def evaluate_holdout(authorization: str) -> None:
    require_authorization(authorization)
    spec = json.loads(SPEC_PATH.read_text())
    model = json.loads(MODEL_PATH.read_text())
    claim_holdout(authorization, model)
    verify_model_bindings(model)
    rows = joined_rows("HOLDOUT")
    rules = threshold_rules(spec)
    threshold_results = {}
    for family, selection in model["selected_threshold_rules"].items():
        rule = rules[selection["rule_id"]]
        threshold_results[family] = {
            "id": selection["rule_id"],
            "metrics": metrics(rows, [rule(row["x"]) for row in rows]),
        }
    payload = {
        "schema_version": "3.0",
        "authorization": authorization,
        "calibration_freeze_id": model["freeze_id"],
        "threshold_rules": threshold_results,
        "logistic": {"metrics": metrics(rows, [logistic_decision(row["x"], model["logistic"]) for row in rows])},
        "holdout_evaluations": 1,
    }
    with RESULT_PATH.open("xb") as handle:
        handle.write(canonical(payload))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["calibrate", "evaluate-holdout"])
    parser.add_argument("--authorization")
    args = parser.parse_args()
    if args.command == "calibrate":
        calibrate(args.authorization)
    else:
        evaluate_holdout(args.authorization)


if __name__ == "__main__":
    main()
