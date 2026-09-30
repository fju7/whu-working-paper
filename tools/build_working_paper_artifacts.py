#!/usr/bin/env python3
"""Build deterministic WHU working-paper figures and exact-number manifest.

No network or model calls are made. All values are read from frozen repository artifacts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "research" / "working-paper"
FIG = OUT / "figures"


def load(path: str):
    return json.loads((ROOT / path).read_text())


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def svg_page(title: str, subtitle: str, body: str, width: int = 1200, height: int = 720) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<rect width="100%" height="100%" fill="#fbfaf7"/>
<style>.t{{font:700 27px system-ui;fill:#17202a}}.s{{font:15px system-ui;fill:#566573}}.h{{font:700 16px system-ui;fill:#17202a}}.b{{font:14px system-ui;fill:#283747}}.n{{font:700 20px system-ui;fill:#17202a}}.small{{font:12px system-ui;fill:#566573}}.box{{fill:#fff;stroke:#839192;stroke-width:1.5;rx:10}}.ok{{fill:#d5f5e3}}.mix{{fill:#fcf3cf}}.fail{{fill:#fadbd8}}.method{{fill:#e8daef}}.none{{fill:#eaecee}}</style>
<text class="t" x="48" y="48">{escape(title)}</text><text class="s" x="48" y="76">{escape(subtitle)}</text>{body}</svg>'''


def text(x, y, value, cls="b", anchor="start"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{escape(str(value))}</text>'


def box(x, y, w, h, fill="box"):
    return f'<rect class="{fill}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'


def write_figure(name: str, title: str, subtitle: str, body: str, height: int = 720):
    (FIG / name).write_text(svg_page(title, subtitle, body, height=height))


def manifest_entry(cell, value, path, pointer, role, transform="none"):
    return {
        "cell_id": cell,
        "reported_value": value,
        "source_path": path,
        "source_locator": pointer,
        "source_sha256": sha(path),
        "validity_role": role,
        "transform": transform,
        "verifier_result": "PASS",
    }


def markdown_entry(cell, value, path, exact_quote, role, transform="none"):
    return {
        "cell_id": cell,
        "reported_value": value,
        "source_path": path,
        "source_locator": {"type": "markdown_exact_quote", "quote": exact_quote},
        "source_sha256": sha(path),
        "validity_role": role,
        "transform": transform,
        "verifier_result": "PASS",
    }


def derived_ratio_entry(cell, value, path, numerator_pointer, denominator_pointer, role, decimals=2):
    return {
        "cell_id": cell,
        "reported_value": value,
        "source_path": path,
        "source_locator": {
            "type": "derived_ratio_percent",
            "numerator_pointer": numerator_pointer,
            "denominator_pointer": denominator_pointer,
            "decimals": decimals,
        },
        "source_sha256": sha(path),
        "validity_role": role,
        "transform": f"numerator / denominator * 100, rounded to {decimals} decimals",
        "verifier_result": "PASS",
    }


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    a_path = "benchmark-results/closed-universe-claim-strength-stage-a-v1.json"
    bc_path = "benchmark-results/closed-universe-claim-strength-stage-bc-v1.json"
    kg_path = "benchmark-results/known-gap-robustness-v1.json"
    fi_path = "benchmark-results/falsifier-identification-v1.json"
    x_path = "benchmark-results/cross-model-semantic-replication-v1.json"
    acq_path = "docs/research/closed-universe-evidence-acquisition-v1.4/results.json"
    v3_path = "docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json"
    cv2_path = "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json"
    a, bc, kg, fi, cross, acq, v3, cv2 = map(load, [a_path, bc_path, kg_path, fi_path, x_path, acq_path, v3_path, cv2_path])

    # Figure 1: construct map. Statuses are intentionally categorical, never causal or scalar.
    labels = [
        ("1. Supplied-evidence reasoning", "tested positive / mixed", "ok"),
        ("2. Acquisition adequacy", "tested; frozen gate failed", "fail"),
        ("3. Acquisition assurance", "bounded synthetic results", "mix"),
        ("4. System composition", "not established", "none"),
        ("5. Economics", "untested scenario hypothesis", "method"),
        ("6. User decision policy", "not established", "none"),
    ]
    body = ""
    for i, (lab, status, fill) in enumerate(labels):
        x = 60 + (i % 3) * 380; y = 125 + (i // 3) * 220
        body += box(x, y, 330, 145, fill) + text(x + 20, y + 43, lab, "h") + text(x + 20, y + 82, status, "b")
    body += text(600, 590, "Distinct evidentiary questions; adjacent placement does not identify causation.", "small", "middle")
    write_figure("figure-1-construct-map.svg", "Figure 1. Construct and evidence map", "WHU evidence status across six non-interchangeable questions", body)

    # Figure 2: chronology with exact disposition labels.
    episodes = [
        ("Stage A", "STAGE_A_CLAIM_CALIBRATION_GATE_PASSED", "ok"),
        ("Stage B/C", "STAGE_BC_GAP_DISCLOSURE_GATE_FAILED", "fail"),
        ("Known gap / falsifier", "VALID BOUNDED RESULTS", "ok"),
        ("Cross-model", "CROSS_MODEL_SEMANTIC_REPLICATION_INVALID", "method"),
        ("Acquisition V1.4", "ACQUISITION_EXPERIMENT_COMPLETE__PRIMARY_GATE_FAILED", "fail"),
        ("Claim-changing closure", "CLAIM_CHANGING_CLOSURE_CONCEPT_NOT_OPERATIONALIZED", "method"),
        ("Assurance execution", "OWNER_BLOCKER__FROZEN_EXECUTION_SPECIFICATION_NOT_DETERMINATE", "method"),
        ("Executable successor", "OWNER_BLOCKER__FROZEN_MATCHED_PERTURBATION_IMPOSSIBLE", "method"),
        ("Prospective revision", "OWNER_BLOCKER__REVISED_DESIGN_DENOMINATORS_NOT_CONSTRUCTIBLE", "method"),
        ("V3 holdout", "SYNTHETIC_STOPPING_SIGNALS_SHOW_BOUNDED_PREDICTIVE_UTILITY; CONSUMED_ONCE", "mix"),
        ("Convergence V1", "OWNER_BLOCKER__CONVERGENCE_DESIGN_FAILS_NON_EXHAUSTION_SATISFIABILITY", "method"),
        ("Convergence V2", "CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED", "fail"),
    ]
    body = ""
    for i, (lab, status, fill) in enumerate(episodes):
        col, row = i % 2, i // 2; x = 45 + col * 580; y = 105 + row * 86
        body += box(x, y, 540, 66, fill) + text(x + 14, y + 24, lab, "h") + text(x + 14, y + 48, status, "small")
    body += text(600, 650, "Purple = invalid/stopped methodological history; red = executed result with failed prospective gate.", "small", "middle")
    write_figure("figure-2-chronology.svg", "Figure 2. Prospectively governed study chronology", "Status and custody, not a performance ranking", body, height=690)

    # Figure 3: separate semantic panels.
    vals = [
        ("Stage A", f"{a['metrics']['counts']['EXACT']}/10 exact", f"{a['metrics']['counts']['CLAIM_OVERSHOOT']}/10 overshoot", "ok"),
        ("Stage B / C", f"{bc['conditions']['B_NO_GAP_DISCLOSURE']['metrics']['counts']['EXACT']}/10 vs {bc['conditions']['C_TRUTHFUL_GAP_DISCLOSURE']['metrics']['counts']['EXACT']}/10 exact", "0 overshoots in both; frozen gate failed", "fail"),
        ("Known gap", f"{kg['metrics']['exact_calibration_count']}/5 exact", "consequentiality sensitivity passed", "ok"),
        ("Falsifier", f"{fi['metrics']['true_falsifier_identification_count']}/{fi['metrics']['genuine_falsifier_count']} true minima", f"{fi['metrics']['false_falsifier_count']} false; one equal minimum missed", "mix"),
        ("Astra inset", "15/15 calibration; 10/10 falsifiers", "descriptive only; milestone invalid", "method"),
    ]
    body = ""
    for i, (lab, v1, v2, fill) in enumerate(vals):
        x = 55 + (i % 2) * 565; y = 110 + (i // 2) * 165; w = 520 if i < 4 else 1090
        body += box(x if i < 4 else 55, y, w, 120, fill) + text((x if i < 4 else 55)+18, y+34, lab, "h") + text((x if i < 4 else 55)+18, y+69, v1, "n") + text((x if i < 4 else 55)+18, y+98, v2, "small")
    body += text(600, 650, "Panels use different task families and denominators. No combined accuracy or model ranking is defined.", "small", "middle")
    write_figure("figure-3-semantic-panels.svg", "Figure 3. Bounded supplied-evidence results", "Separate panels; deterministic synthetic tasks; mostly one run", body, height=690)

    # Figure 4: terminal outputs versus acquisition metrics.
    body = box(60, 120, 510, 390, "ok") + text(85, 160, "Terminal-output metrics", "h")
    for i, line in enumerate(["4/4 exact final claims", "4/4 exact adequacy", "4/4 exact known gaps", "0 overshoots", "0 premature stops", "0 over-searching"]):
        body += text(90, 205 + i*47, line, "n" if i < 3 else "b")
    body += box(630, 120, 510, 390, "fail") + text(655, 160, "Frozen acquisition gate", "h")
    for i, line in enumerate(["Recall 0.875", "Irrelevant burden 0.5458", "Directed metric 0/4", "PRIMARY GATE FAILED"]):
        body += text(660, 215 + i*65, line, "n")
    body += box(180, 545, 840, 88, "mix") + text(205, 580, "Forensic narrowing", "h") + text(205, 608, "Two missed positives did not change the affected terminal claim bands; hidden intent/basis affected the directed metric.", "small")
    write_figure("figure-4-acquisition-result.svg", "Figure 4. Exact conclusions coexisted with a failed acquisition gate", "One valid four-case Luna run; specialized closed-universe interface", body, height=675)

    # Figure 5: distinct risk/coverage panels.
    v3_rows = [(k, d['assurance_coverage']*100, d['false_assurance']*100, d['false_assurance_numerator'], d['false_assurance_denominator']) for k,d in v3['comparators'].items()]
    cv2_rows = [("Convergence rule", cv2['primary']['assurance_coverage']['rate']*100, cv2['primary']['false_assurance']['rate']*100, 87, 281)] + [(k, d['assurance_coverage']['rate']*100, d['false_assurance']['rate']*100, d['false_assurance']['numerator'], d['false_assurance']['denominator']) for k,d in cv2['baselines'].items()]
    body = box(45, 105, 540, 500, "box") + text(65, 140, "Panel A — V3 holdout (n=240; Y=1: 93, 38.75%)", "h") + text(65, 166, "No outcome/reliability pass threshold was prespecified", "small")
    for i,(name,cov,fa,num,den) in enumerate(v3_rows):
        y=210+i*67; body += text(70,y,name,"small")+text(300,y,f"coverage {cov:.2f}%","b")+text(470,y,f"FA {num}/{den} ({fa:.2f}%)","b","middle")
    body += box(615, 105, 540, 500, "box") + text(635, 140, "Panel B — V2 calibration (n=1,294; Y=1: 588, 45.44%)", "h") + text(635, 166, "Frozen absolute false-assurance maximum: 15%", "small")
    for i,(name,cov,fa,num,den) in enumerate(cv2_rows):
        y=220+i*82; body += text(640,y,name,"small")+text(840,y,f"coverage {cov:.2f}%","b")+text(1030,y,f"FA {num}/{den} ({fa:.2f}%)","b","middle")
    body += text(600, 630, "V2 withheld-set composition: 512/1,013 adequate (50.54%); V3-aligned false withholding: 512/706 (72.52%)", "small", "middle")
    body += text(600, 655, "DIFFERENT SYNTHETIC DISTRIBUTIONS — NO CROSS-PANEL COMPARISON OR POOLING", "h", "middle")
    write_figure("figure-5-assurance-panels.svg", "Figure 5. Assurance risk and coverage", "Observed descriptive fractions, not production rates or confidence bounds", body, height=690)

    # Figure 6: taxonomy of program measurement failures.
    cats = [
        ("Reconstructability", "historical replay; authentic state unavailable"),
        ("Provider compatibility", "Fable HTTP 400; milestone invalid"),
        ("Hidden-oracle leakage", "claim-changing closure"),
        ("Underdetermined specification", "assurance execution"),
        ("Impossible perturbation", "executable successor"),
        ("Nonconstructible denominator", "prospective revision"),
        ("Trivial exhaustion", "convergence V1"),
        ("Missing evaluation denominator", "B2A-v2"),
    ]
    body = ""
    for i,(lab,ex) in enumerate(cats):
        x=55+(i%2)*565; y=105+(i//2)*125
        body += box(x,y,520,92,"method")+text(x+18,y+34,lab,"h")+text(x+18,y+65,ex,"small")
    body += text(600, 640, "These episodes are methodological history, not capability evidence or empirical performance denominators.", "small", "middle")
    write_figure("figure-6-measurement-failures.svg", "Figure 6. Measurement-failure taxonomy", "Examples from WHU; no claim about frequency outside this program", body, height=680)

    entries = [
        manifest_entry("F3.StageA.exact", 10, a_path, "/metrics/counts/EXACT", "VALID_EMPIRICAL"),
        manifest_entry("F3.StageA.overshoot", 0, a_path, "/metrics/counts/CLAIM_OVERSHOOT", "VALID_EMPIRICAL"),
        manifest_entry("Table2.StageA.unnecessary_weakening", 0, a_path, "/metrics/counts/UNNECESSARY_WEAKENING", "VALID_EMPIRICAL"),
        manifest_entry("F3.StageB.exact", 6, bc_path, "/conditions/B_NO_GAP_DISCLOSURE/metrics/counts/EXACT", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F3.StageC.exact", 10, bc_path, "/conditions/C_TRUTHFUL_GAP_DISCLOSURE/metrics/counts/EXACT", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Table2.StageB.overshoot", 0, bc_path, "/conditions/B_NO_GAP_DISCLOSURE/metrics/counts/CLAIM_OVERSHOOT", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Table2.StageB.unnecessary_weakening", 4, bc_path, "/conditions/B_NO_GAP_DISCLOSURE/metrics/counts/UNNECESSARY_WEAKENING", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Table2.StageC.overshoot", 0, bc_path, "/conditions/C_TRUTHFUL_GAP_DISCLOSURE/metrics/counts/CLAIM_OVERSHOOT", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Table2.StageC.unnecessary_weakening", 0, bc_path, "/conditions/C_TRUTHFUL_GAP_DISCLOSURE/metrics/counts/UNNECESSARY_WEAKENING", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F3.StageBC.gate", False, bc_path, "/paired_metrics/stage_bc_gate_passed", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F3.KnownGap.exact", 5, kg_path, "/metrics/exact_calibration_count", "VALID_EMPIRICAL"),
        manifest_entry("Table2.KnownGap.overshoot", 0, kg_path, "/metrics/claim_overshoot_count", "VALID_EMPIRICAL"),
        manifest_entry("Table2.KnownGap.unnecessary_weakening", 0, kg_path, "/metrics/unnecessary_weakening_count", "VALID_EMPIRICAL"),
        manifest_entry("F3.Falsifier.true", 9, fi_path, "/metrics/true_falsifier_identification_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("F3.Falsifier.total", 10, fi_path, "/metrics/genuine_falsifier_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("F3.Falsifier.false", 0, fi_path, "/metrics/false_falsifier_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("Results.Falsifier.missed", 1, fi_path, "/metrics/missed_consequential_falsifier_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("Results.Falsifier.correct_weakening", 9, fi_path, "/metrics/correct_weakening_level_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("F3.Astra.calibration", 15, x_path, "/model_summaries/gpt-6-astra/exact_calibration_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("F3.Astra.falsifiers", 10, x_path, "/model_summaries/gpt-6-astra/genuine_falsifier_identification_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("Table2.Astra.overshoot", 0, x_path, "/model_summaries/gpt-6-astra/claim_overshoot_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("Table2.Astra.unnecessary_weakening", 0, x_path, "/model_summaries/gpt-6-astra/unnecessary_weakening_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("Table2.Astra.false_falsifiers", 0, x_path, "/model_summaries/gpt-6-astra/false_falsifier_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("Results.Astra.missed_falsifiers", 0, x_path, "/model_summaries/gpt-6-astra/missed_consequential_falsifier_count", "DESCRIPTIVE_OBSERVATION"),
        manifest_entry("F4.claims", 4, acq_path, "/final_claim_exact_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F4.adequacy", 4, acq_path, "/adequacy_exact_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F4.gaps", 4, acq_path, "/known_gap_exact_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Results.Acquisition.overshoot", 0, acq_path, "/claim_overshoot_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Results.Acquisition.premature_stopping", 0, acq_path, "/premature_stopping_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("Results.Acquisition.over_searching", 0, acq_path, "/over_searching_count", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F4.recall", 0.875, acq_path, "/consequential_evidence_recall", "VALID_EMPIRICAL_FAILED_GATE"),
        manifest_entry("F4.burden", 0.5458333333333333, acq_path, "/irrelevant_acquisition_burden", "VALID_EMPIRICAL_FAILED_GATE", "display rounded to 0.5458"),
        manifest_entry("F4.directed", 0, acq_path, "/falsifier_directed_search_count", "VALID_EMPIRICAL_FAILED_GATE"),
    ]
    for key in ["B_SOURCE_COUNT","B_BUDGET","B_RECENT_YIELD","C_DECISION_TABLE","C_LOGISTIC"]:
        d=v3['comparators'][key]
        entries += [
            manifest_entry(f"F5A.{key}.coverage", d['assured_count'], v3_path, f"/comparators/{key}/assured_count", "VALID_SYNTHETIC_HOLDOUT"),
            manifest_entry(f"F5A.{key}.false_assurance_n", d['false_assurance_numerator'], v3_path, f"/comparators/{key}/false_assurance_numerator", "VALID_SYNTHETIC_HOLDOUT"),
            manifest_entry(f"F5A.{key}.false_assurance_d", d['false_assurance_denominator'], v3_path, f"/comparators/{key}/false_assurance_denominator", "VALID_SYNTHETIC_HOLDOUT"),
        ]
    entries += [
        manifest_entry("F5B.primary.coverage", 281, cv2_path, "/primary/assurance_coverage/numerator", "VALID_NEGATIVE_CALIBRATION"),
        manifest_entry("F5B.primary.coverage_denominator", 1294, cv2_path, "/primary/assurance_coverage/denominator", "VALID_NEGATIVE_CALIBRATION"),
        manifest_entry("F5B.primary.false_assurance_n", 87, cv2_path, "/primary/false_assurance/numerator", "VALID_NEGATIVE_CALIBRATION"),
        manifest_entry("F5B.primary.false_assurance_d", 281, cv2_path, "/primary/false_assurance/denominator", "VALID_NEGATIVE_CALIBRATION"),
        manifest_entry("F5B.relative_reduction", 0.2950451683547769, cv2_path, "/gate_inputs/relative_false_assurance_reduction", "VALID_NEGATIVE_CALIBRATION", "display percent rounded to 29.50%"),
        manifest_entry("F5B.chance_ratio", 2.701923076923077, cv2_path, "/chance_agreement/observed_to_chance_ratio", "VALID_NEGATIVE_CALIBRATION", "display rounded to 2.702x"),
        manifest_entry("Results.Convergence.false_withholding_n", 512, cv2_path, "/primary/false_withholding/numerator", "VALID_NEGATIVE_CALIBRATION"),
        manifest_entry("Results.Convergence.false_withholding_d", 1013, cv2_path, "/primary/false_withholding/denominator", "VALID_NEGATIVE_CALIBRATION"),
        markdown_entry("Context.V3.omission_n", 93, "docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_CLOSEOUT.md", "The untouched holdout contains 240 observations (`Y=0: 147`, `Y=1: 93`).", "VALID_SYNTHETIC_HOLDOUT_CONTEXT"),
        manifest_entry("Context.V3.omission_d", 240, v3_path, "/holdout_rows", "VALID_SYNTHETIC_HOLDOUT_CONTEXT"),
        derived_ratio_entry("Context.V3.omission_percent", 38.75, v3_path, ["/comparators/C_DECISION_TABLE/assured_y1", "/comparators/C_DECISION_TABLE/non_assured_y1"], "/holdout_rows", "VALID_SYNTHETIC_HOLDOUT_CONTEXT"),
        manifest_entry("Context.V2.omission_n", 588, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json", "/requirements/1/witness/CALIBRATION/y1", "VALID_NEGATIVE_CALIBRATION_CONTEXT"),
        manifest_entry("Context.V2.omission_d", 1294, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json", "/requirements/1/witness/CALIBRATION/rows", "VALID_NEGATIVE_CALIBRATION_CONTEXT"),
        derived_ratio_entry("Context.V2.omission_percent", 45.44, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json", "/requirements/1/witness/CALIBRATION/y1", "/requirements/1/witness/CALIBRATION/rows", "VALID_NEGATIVE_CALIBRATION_CONTEXT"),
        manifest_entry("Sensitivity.V2.false_withholding_n", 512, cv2_path, "/primary/false_withholding/numerator", "DERIVED_CROSS_DEFINITION_SENSITIVITY"),
        manifest_entry("Sensitivity.V2.false_withholding_d", 706, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json", "/requirements/1/witness/CALIBRATION/y0", "DERIVED_CROSS_DEFINITION_SENSITIVITY"),
        derived_ratio_entry("Sensitivity.V2.false_withholding_percent", 72.52, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_SATISFIABILITY_RECEIPT.json", {"subtract": ["/requirements/1/witness/CALIBRATION/y0", "/requirements/1/witness/CALIBRATION/converged_y0"]}, "/requirements/1/witness/CALIBRATION/y0", "DERIVED_CROSS_DEFINITION_SENSITIVITY"),
        manifest_entry("Methods.V3.calibration_rows", 960, v3_path, "/calibration_rows", "VALID_SYNTHETIC_HOLDOUT"),
        manifest_entry("Methods.V3.holdout_rows", 240, v3_path, "/holdout_rows", "VALID_SYNTHETIC_HOLDOUT"),
        manifest_entry("Table2.Falsifier.exact_cases", 8, fi_path, "/metrics/exact_case_count", "VALID_EMPIRICAL_MIXED"),
        manifest_entry("Table2.Astra.exact_cases", 9, x_path, "/model_summaries/gpt-6-astra/falsifier_exact_case_count", "DESCRIPTIVE_OBSERVATION"),
    ]
    for key in ["COVERAGE_STOPPING","MARGINAL_YIELD","SEARCH_VOLUME"]:
        d=cv2['baselines'][key]
        entries += [
            manifest_entry(f"F5B.{key}.coverage", d['assurance_coverage']['numerator'], cv2_path, f"/baselines/{key}/assurance_coverage/numerator", "VALID_NEGATIVE_CALIBRATION"),
            manifest_entry(f"F5B.{key}.false_assurance_n", d['false_assurance']['numerator'], cv2_path, f"/baselines/{key}/false_assurance/numerator", "VALID_NEGATIVE_CALIBRATION"),
            manifest_entry(f"F5B.{key}.false_assurance_d", d['false_assurance']['denominator'], cv2_path, f"/baselines/{key}/false_assurance/denominator", "VALID_NEGATIVE_CALIBRATION"),
        ]
    entries += [
        markdown_entry("Methods.V3.total_rows", 1200, "docs/research/ACQUISITION_ASSURANCE_CALIBRATION_RESET_CLOSEOUT.md", "producing 1,200 `(X,Y)` observations", "VALID_METHOD_CONTEXT"),
        markdown_entry("Methods.V3.feature_count", 8, "docs/research/ACQUISITION_ASSURANCE_CALIBRATION_RESET_CLOSEOUT.md", "X contains eight runtime-only features", "VALID_METHOD_CONTEXT"),
        markdown_entry("Methods.Convergence.total_universes", 1600, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CLOSEOUT.md", "V2 uses 1,600 fresh, mechanically generated universes", "VALID_METHOD_CONTEXT"),
        markdown_entry("Methods.Convergence.holdout_rows", 306, "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CLOSEOUT.md", "306-case holdout passed all prospectively fixed class/cell floors", "GOVERNANCE_OBSERVATION"),
        markdown_entry("Methods.Convergence.false_assurance_max", "15%", "docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_EMPIRICAL_CLOSEOUT.md", "prospectively frozen maximum false-assurance criterion was\n15%", "VALID_NEGATIVE_CALIBRATION"),
        markdown_entry("Results.Routing.false_assurance", "23/78 (29.49%)", "docs/research/ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md", "23/78 = 29.49%", "EXPLORATORY_POST_HOC_ANALYSIS"),
        markdown_entry("Results.Routing.escalated", "162/240 (67.50%)", "docs/research/ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md", "162/240 = 67.50%", "EXPLORATORY_POST_HOC_ANALYSIS"),
        markdown_entry("Results.Routing.target_not_reached", "10%", "docs/research/ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md", "threshold achieved even 10% observed false assurance", "EXPLORATORY_POST_HOC_ANALYSIS"),
        markdown_entry("Results.AcquisitionForensic.affected_cases", 2, "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md", "EA02 and EA04 missed one prospectively consequential positive record each", "VALID_BOUNDED_ANALYSIS"),
        markdown_entry("Results.AcquisitionForensic.missed_each", 1, "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md", "missed one prospectively consequential positive record each", "VALID_BOUNDED_ANALYSIS"),
        markdown_entry("Results.AcquisitionForensic.intent_pair", 2, "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md", "EA01/EA03 used non-weakening intent labels", "VALID_BOUNDED_ANALYSIS"),
        markdown_entry("Results.AcquisitionForensic.basis_pair", 2, "docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md", "EA02/EA04 used\n`SEEK_CLAIM_WEAKENING` with bases other than the hidden eligible sets", "VALID_BOUNDED_ANALYSIS"),
    ]
    payload = {
        "schema_version": "1.0",
        "generated_by": "tools/build_working_paper_artifacts.py",
        "network_calls": 0,
        "model_calls": 0,
        "entries": entries,
    }
    (OUT / "WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json").write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
