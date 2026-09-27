#!/usr/bin/env python3
"""Recompute published results from released synthetic rows only."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(loaded)
    return loaded


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def v3() -> list[str]:
    errors: list[str] = []
    scorer = module("public_v3", ROOT / "tools/acquisition_assurance_v3_score.py")
    runtime = {r["observation_id"]: r for r in rows(scorer.RUNTIME_PATH)}
    labels = {r["observation_id"]: r for r in rows(scorer.EVALUATOR_PATH)}
    if set(runtime) != set(labels):
        return ["V3 runtime/evaluator join mismatch"]
    joined = [{**runtime[key], "y": labels[key]["y"]} for key in sorted(runtime)]
    calibration = [r for r in joined if r["partition"] == "CALIBRATION"]
    evaluation = [r for r in joined if r["partition"] != "CALIBRATION"]
    if (len(calibration), len(evaluation)) != (960, 240):
        errors.append("V3 partition sizes do not reproduce as 960/240")
    spec = json.loads(scorer.SPEC_PATH.read_text())
    frozen = json.loads(scorer.MODEL_PATH.read_text())
    rules = scorer.threshold_rules(spec)
    candidates: dict[str, list[tuple[float, float, str]]] = {
        "B_SOURCE_COUNT": [], "B_BUDGET": [], "B_RECENT_YIELD": [], "C_DECISION_TABLE": []
    }
    for rule_id, rule in rules.items():
        metric = scorer.metrics(calibration, [rule(r["x"]) for r in calibration])
        if metric["assurance_coverage"] >= spec["selection_rule"]["minimum_calibration_coverage"]:
            family = next(name for name in candidates if rule_id.startswith(name + "__"))
            candidates[family].append((metric["false_assurance"], -metric["assurance_coverage"], rule_id))
    selected = {family: min(values)[2] for family, values in candidates.items()}
    if selected != {family: value["rule_id"] for family, value in frozen["selected_threshold_rules"].items()}:
        errors.append("V3 calibration threshold selection does not reproduce")
    if canonical(scorer.fit_logistic(calibration, spec["features"])) != canonical(frozen["logistic"]):
        errors.append("V3 logistic calibration does not reproduce")
    threshold_results = {}
    for family, selection in frozen["selected_threshold_rules"].items():
        rule = rules[selection["rule_id"]]
        threshold_results[family] = {"id": selection["rule_id"], "metrics": scorer.metrics(evaluation, [rule(r["x"]) for r in evaluation])}
    recorded = json.loads(scorer.RESULT_PATH.read_text())
    reproduced = {
        "schema_version": "3.0", "authorization": recorded["authorization"],
        "calibration_freeze_id": frozen["freeze_id"], "threshold_rules": threshold_results,
        "logistic": {"metrics": scorer.metrics(evaluation, [scorer.logistic_decision(r["x"], frozen["logistic"]) for r in evaluation])},
        "holdout_evaluations": 1,
    }
    if canonical(reproduced) != canonical(recorded):
        errors.append("V3 published evaluation result does not reproduce")
    return errors


def v2() -> list[str]:
    scorer = module("public_v2", ROOT / "tools/score_independent_acquisition_convergence_v2_public.py")
    spec = json.loads(scorer.SPEC.read_text())
    runtime = rows(ROOT / "benchmarks/independent-acquisition-convergence-v2/calibration-runtime-observations.jsonl")
    labels = {r["observation_id"]: r for r in rows(ROOT / "benchmarks/independent-acquisition-convergence-v2/calibration-labels.jsonl")}
    if len(runtime) != 1294 or set(labels) != {r["observation_id"] for r in runtime}:
        return ["V2 public calibration rows/labels do not form the 1,294-row partition"]
    primary = scorer.assurance(runtime, labels, lambda r: scorer.decision(r, spec["convergence_rule"]))
    baseline = {name: scorer.assurance(runtime, labels, fn) for name, fn in scorer.baselines(spec).items()}
    disagreement = [r for r in runtime if r["reconciliation"]["claim_band_disagreement"] == 1]
    agreement = [r for r in runtime if r["reconciliation"]["claim_band_disagreement"] == 0]
    observed = primary["assurance_coverage"]["numerator"]
    chance = scorer.chance_count(runtime, spec)
    eligible = {name: value for name, value in baseline.items() if value["assurance_coverage"]["rate"] >= spec["primary_gate"]["baseline_minimum_coverage"] and value["false_assurance"]["denominator"]}
    best = min(value["false_assurance"]["rate"] for value in eligible.values())
    relative = (best - primary["false_assurance"]["rate"]) / best
    chance_ratio = observed / chance
    gate = spec["primary_gate"]
    passed = primary["false_assurance"]["rate"] <= gate["maximum_false_assurance"] and primary["assurance_coverage"]["rate"] >= gate["minimum_assurance_coverage"] and relative >= gate["minimum_relative_false_assurance_reduction_vs_best_eligible_baseline"] and chance_ratio >= gate["minimum_convergence_rate_ratio_vs_fixed_permutation_chance"]
    dr = scorer.fraction(sum(labels[r["observation_id"]]["y"] for r in disagreement), len(disagreement))
    ar = scorer.fraction(sum(labels[r["observation_id"]]["y"] for r in agreement), len(agreement))
    route_uses = sum(r["process_a"]["x"]["routes_used"] + r["process_b"]["x"]["routes_used"] for r in runtime)
    reproduced = {
        "schema_version": "2.0", "experiment_id": spec["experiment_id"], "partition": "CALIBRATION",
        "primary": primary, "baselines": baseline,
        "disagreement_enrichment": {"disagreement_hidden_omission": dr, "agreement_hidden_omission": ar, "rate_ratio": dr["rate"] / ar["rate"]},
        "acquisition_cost": {"routes_used": route_uses, "observations": len(runtime), "mean_routes_per_observation": route_uses / len(runtime)},
        "chance_agreement": {"observed_convergence": scorer.fraction(observed, len(runtime)), "fixed_permutation_convergence": scorer.fraction(chance, len(runtime)), "observed_to_chance_ratio": chance_ratio},
        "gate_inputs": {"eligible_baselines": sorted(eligible), "best_eligible_baseline_false_assurance": best, "relative_false_assurance_reduction": relative},
        "primary_gate_passed": passed,
    }
    recorded = ROOT / "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json"
    return [] if canonical(reproduced) == recorded.read_bytes() else ["V2 published calibration result does not reproduce"]


def main() -> None:
    errors = v3() + v2()
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS: V3 calibration/evaluation and convergence V2 calibration results recomputed")


if __name__ == "__main__":
    main()
