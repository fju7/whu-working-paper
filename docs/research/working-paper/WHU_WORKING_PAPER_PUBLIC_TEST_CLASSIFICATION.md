# Working-paper public test classification

Date: `2026-09-27`

This map prospectively classifies every test in the 49-test internal focused suite that existed at
commit `50a6d4c62fafb011c46675ad4ccd02bdc001ba9a`. Classification changes the public reproduction
contract, not the manuscript, result files, scientific conclusions, frozen protocols, prior audits,
or custody history.

## Contract

- `PUBLIC_RESULT_REPRODUCTION`: must run from the public snapshot because it rebuilds or checks a
  published quantitative result, figure, table, or rendered manuscript.
- `PUBLIC_PROVENANCE_INTEGRITY`: must run publicly because it verifies source hashes, exact locators,
  evidence roles, dispositions, or the public evidence for an intentionally unopened holdout.
- `INTERNAL_CUSTODY_ONLY`: intentionally cannot run from the public snapshot because its execution
  requires protected/private labels or custody-controlled runtime material. The public substitute is
  a hash commitment, receipt, stop status, and a check that no paper result depends on the contents.
- `NON_PAPER_OR_HISTORICAL`: validates a scorer edge case, provider adapter, prospective design, or
  historical apparatus but does not reproduce a quantity or substantive claim in the paper.

The 49 tests are unit and contract tests. None is the computation that produced the frozen provider
responses or historical observations. Public result reproduction is instead performed by
`tools/build_working_paper_artifacts.py`, `tools/render_working_paper.py`, and
`tools/verify_working_paper.py`; public custody/provenance integrity is performed by
`tools/verify_working_paper_release.py` and `tools/verify_working_paper_custody.py`.

## Classification of all 49 internal tests

| Internal test | Category | Exact paper claim/result/artifact supported | Why public execution is or is not required |
|---|---|---|---|
| `test_claim_strength_stage_a.py::test_frozen_ground_truth_is_deterministically_reconstructed` | `NON_PAPER_OR_HISTORICAL` | §4.1 Stage A design; Table 2 Stage A | Tests oracle construction, not the reported 10/10 and 0/10 output; those values rebuild from the frozen result JSON. |
| `test_claim_strength_stage_a.py::test_model_packet_withholds_expected_claims` | `NON_PAPER_OR_HISTORICAL` | §3 hidden-answer design | Prospective packet-leakage unit check; no paper quantity depends on executing it. |
| `test_claim_strength_stage_a.py::test_primary_metric_counts_overshoot_before_other_errors` | `NON_PAPER_OR_HISTORICAL` | §3 scoring definitions | Synthetic scorer precedence check, not an empirical result. |
| `test_claim_strength_stage_a.py::test_unnecessary_weakening_is_separate_from_overshoot` | `NON_PAPER_OR_HISTORICAL` | §3 scoring definitions | Synthetic scorer taxonomy check, not an empirical result. |
| `test_claim_strength_stage_bc.py::test_frozen_full_universes_and_safe_answers_reconstruct` | `NON_PAPER_OR_HISTORICAL` | §4.1 Stage B/C design; Table 2 | Tests oracle construction; reported B/C counts rebuild from the frozen result JSON. |
| `test_claim_strength_stage_bc.py::test_packets_are_matched_and_withhold_full_universe_and_answers` | `NON_PAPER_OR_HISTORICAL` | §3 matched B/C design | Prospective packet-isolation check, not a published output. |
| `test_claim_strength_stage_bc.py::test_overshoot_and_weakening_are_separate` | `NON_PAPER_OR_HISTORICAL` | §3 scoring definitions | Synthetic scorer taxonomy check. |
| `test_claim_strength_stage_bc.py::test_gate_requires_disclosure_condition_improvement` | `NON_PAPER_OR_HISTORICAL` | §4.1 `STAGE_BC_GAP_DISCLOSURE_GATE_FAILED` | Tests the generic gate rule; the actual failed-gate value is in the public result JSON and exact-number manifest. |
| `test_known_gap_robustness.py::test_all_required_states_and_ground_truth_reconstruct` | `NON_PAPER_OR_HISTORICAL` | §4.1 known-gap design; Table 2 | Oracle-construction check; actual 5/5 result rebuilds from the public frozen result. |
| `test_known_gap_robustness.py::test_model_packet_excludes_answers_and_consequentiality_labels` | `NON_PAPER_OR_HISTORICAL` | §3 hidden-answer design | Packet-leakage unit check, not a paper output. |
| `test_known_gap_robustness.py::test_scoring_separates_overshoot_weakening_and_sensitivity` | `NON_PAPER_OR_HISTORICAL` | §3 metric definitions | Synthetic scorer taxonomy check. |
| `test_known_gap_robustness.py::test_performance_is_not_required_for_informative_primary_gate` | `NON_PAPER_OR_HISTORICAL` | §3 gate semantics | Prospective gate-semantics check, not an observed result. |
| `test_falsifier_identification.py::test_ground_truth_reconstructs_for_all_nine_cases` | `NON_PAPER_OR_HISTORICAL` | §4.1 falsifier design; Table 2 | Oracle-construction check; observed 9/10 result rebuilds from the public frozen result. |
| `test_falsifier_identification.py::test_model_packet_excludes_answer_keys` | `NON_PAPER_OR_HISTORICAL` | §3 hidden-answer design | Packet-leakage unit check, not a paper output. |
| `test_falsifier_identification.py::test_exact_response_scores_all_metrics` | `NON_PAPER_OR_HISTORICAL` | §3 falsifier metric definitions | Scores a fabricated exact response rather than the empirical response. |
| `test_falsifier_identification.py::test_false_missed_and_wrong_level_are_separate` | `NON_PAPER_OR_HISTORICAL` | §3 falsifier metric definitions | Synthetic scorer taxonomy check. |
| `test_falsifier_identification.py::test_invalid_candidate_fails_scoreability_gate` | `NON_PAPER_OR_HISTORICAL` | §3 validity controls | Invalid-input unit check, not a paper result. |
| `test_falsifier_identification.py::test_performance_is_not_required_for_informative_gate` | `NON_PAPER_OR_HISTORICAL` | §3 gate semantics | Prospective gate-semantics check, not an observed result. |
| `test_closed_universe_evidence_acquisition_design.py::test_design_is_valid_and_execution_is_forbidden` | `NON_PAPER_OR_HISTORICAL` | §5 acquisition design history | Tests the pre-execution protocol state; the paper reports the later authorized run from `results.json`. |
| `test_closed_universe_evidence_acquisition_design.py::test_agent_packet_hides_oracle_and_search_mapping` | `NON_PAPER_OR_HISTORICAL` | §3 acquisition blinding | Prospective packet-leakage unit check. |
| `test_closed_universe_evidence_acquisition_design.py::test_oracle_event_logs_pass_every_frozen_metric` | `NON_PAPER_OR_HISTORICAL` | §3 acquisition scorer | Scores fabricated oracle transcripts, not the published four-case execution. |
| `test_closed_universe_evidence_acquisition_design.py::test_alternative_sufficient_set_allows_ea03_early_closure` | `NON_PAPER_OR_HISTORICAL` | §3 acquisition adequacy rule | Scorer edge-case check, not an observed paper result. |
| `test_closed_universe_evidence_acquisition_design.py::test_event_response_tampering_is_rejected` | `NON_PAPER_OR_HISTORICAL` | §3 frozen-interface control | Tamper unit check, not an empirical output. |
| `test_closed_universe_evidence_acquisition_design.py::test_duplicate_and_superseded_versions_do_not_double_count` | `NON_PAPER_OR_HISTORICAL` | §3 acquisition metric definition | Scorer edge-case check. |
| `test_closed_universe_evidence_acquisition_design.py::test_conflicting_family_version_meaning_is_rejected` | `NON_PAPER_OR_HISTORICAL` | §3 protocol validation | Invalid-input unit check. |
| `test_closed_universe_evidence_acquisition_design.py::test_dynamic_adequacy_marks_early_stop_unresolved` | `NON_PAPER_OR_HISTORICAL` | §3 adequacy definition | Scorer edge-case check. |
| `test_closed_universe_evidence_acquisition_design.py::test_universal_unresolved_policy_cannot_pass` | `NON_PAPER_OR_HISTORICAL` | §3 gate semantics | Fabricated-policy check, not an observed result. |
| `test_closed_universe_evidence_acquisition_design.py::test_search_all_routes_policy_exceeds_budget` | `NON_PAPER_OR_HISTORICAL` | §3 budget rule | Fabricated-policy check, not an observed result. |
| `test_closed_universe_evidence_acquisition_design.py::test_duplicate_case_empty_reason_and_unresolved_falsifier_are_rejected_or_fail` | `NON_PAPER_OR_HISTORICAL` | §3 validity controls | Invalid-input unit check. |
| `test_closed_universe_evidence_acquisition_design.py::test_designated_route_without_weakening_intent_gets_no_credit` | `NON_PAPER_OR_HISTORICAL` | §4.2 directed-search definition | Scorer edge-case check; actual 0/4 metric rebuilds from the public result. |
| `test_closed_universe_evidence_acquisition_design.py::test_unrelated_falsifier_basis_gets_no_credit` | `NON_PAPER_OR_HISTORICAL` | §4.2 directed-search definition | Scorer edge-case check; actual 0/4 metric rebuilds from the public result. |
| `test_closed_universe_evidence_acquisition_design.py::test_duplicate_acquisition_counts_as_wasted_burden` | `NON_PAPER_OR_HISTORICAL` | §4.2 burden definition | Scorer edge-case check; actual burden rebuilds from the public result. |
| `test_closed_universe_evidence_acquisition_execution.py::test_owner_amendment_changes_only_execution_configuration` | `NON_PAPER_OR_HISTORICAL` | §4.2 provider-compatibility history | Historical amendment-integrity check; no paper quantity requires the adapter. |
| `test_closed_universe_evidence_acquisition_execution.py::test_provider_surface_has_only_frozen_actions_and_no_hosted_tools` | `NON_PAPER_OR_HISTORICAL` | §3 specialized interface | Provider-adapter shape check, not a result computation. |
| `test_closed_universe_evidence_acquisition_execution.py::test_search_schema_omits_unsupported_unique_items_without_changing_other_tools` | `NON_PAPER_OR_HISTORICAL` | §5 provider-compatibility history | Historical compatibility check. |
| `test_closed_universe_evidence_acquisition_execution.py::test_smoke_request_uses_exact_repaired_search_schema_without_benchmark_packet` | `NON_PAPER_OR_HISTORICAL` | §5 provider-compatibility history | Historical smoke-request check; would not reproduce a paper result. |
| `test_closed_universe_evidence_acquisition_execution.py::test_duplicate_search_basis_is_preserved_as_host_validation_rule` | `NON_PAPER_OR_HISTORICAL` | §5 provider-compatibility history | Adapter validation check. |
| `test_closed_universe_evidence_acquisition_execution.py::test_execution_configuration_is_stateless_medium_luna_without_retries` | `NON_PAPER_OR_HISTORICAL` | §3 acquisition run configuration | Historical configuration check; model output cannot be regenerated offline by this test. |
| `test_acquisition_assurance_v3.py::test_v3_satisfiability_passes_without_fitting` | `NON_PAPER_OR_HISTORICAL` | §5 V3 design readiness | Pre-fit satisfiability check, not the published holdout result. |
| `test_acquisition_assurance_v3.py::test_frozen_dataset_reproduces_and_is_separated` | `NON_PAPER_OR_HISTORICAL` | §3 V3 dataset separation; §4.3 V3 result provenance | The consumed V3 synthetic rows, generator, scorer, and a direct result-recomputation check are public. This older test regenerates the same fixture but is not the designated public computation. |
| `test_acquisition_assurance_v3.py::test_partition_is_disjoint_and_seed_complete` | `NON_PAPER_OR_HISTORICAL` | §3 V3 960/240 partition | The released rows and public recomputation check verify 960/240 separation directly; the older unit test is redundant. |
| `test_acquisition_assurance_v3.py::test_scorer_fails_closed_without_authorization` | `NON_PAPER_OR_HISTORICAL` | §3 V3 authorization control | Scorer security unit check, not a result computation. |
| `test_acquisition_assurance_v3.py::test_scorer_detects_binding_tamper` | `NON_PAPER_OR_HISTORICAL` | §3 V3 hash binding | Synthetic tamper check; public source/result hashes are checked directly by the release verifier. |
| `test_acquisition_assurance_v3.py::test_scorer_detects_consumed_holdout` | `NON_PAPER_OR_HISTORICAL` | §3 and §4.3 V3 consumed-once status | Security behavior of the historical scorer; the consumed synthetic rows and result are public, while the receipt establishes the historical status. |
| `test_acquisition_assurance_v3.py::test_holdout_claim_is_atomic_and_precedes_access` | `NON_PAPER_OR_HISTORICAL` | §3 V3 exactly-once custody | Tests a temporary-file implementation property and does not establish the historical access ordering. |
| `test_independent_acquisition_convergence_v2.py::test_v2_satisfiability_reproduces_without_evaluation` | `INTERNAL_CUSTODY_ONLY` | §3 V2 satisfiability; §4.3 calibration-only boundary | The original builder is bound to both partitions and would derive protected V2 holdout material, so both it and the full seed/partition recipe are excluded. Public calibration blueprints/rows/labels and the receipt expose the paper-relevant calibration evidence without doing so. |
| `test_independent_acquisition_convergence_v2.py::test_structural_non_exhaustion_is_arithmetic_and_observed` | `INTERNAL_CUSTODY_ONLY` | §3 V2 maximum union 20, minimum universe 30, observed exhaustion zero | The original test invokes the dual-partition builder. The released calibration rows and receipt independently expose the arithmetic and observed calibration witness. |
| `test_independent_acquisition_convergence_v2.py::test_frozen_files_and_untouched_holdout_match_receipt` | `INTERNAL_CUSTODY_ONLY` | §4.3 `CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED` | Directly hashes the protected holdout labels. Public verification checks the published commitment, stop receipt, exclusion from the manifest, and absence of a holdout-derived claim. |
| `test_independent_acquisition_convergence_v2.py::test_scorer_refuses_hash_mismatched_authorization` | `NON_PAPER_OR_HISTORICAL` | §3 V2 authorization control | Synthetic tamper check, not a reported result or historical custody proof. |

## Public checks and claim coverage

| Public check | Category | Coverage |
|---|---|---|
| `python3 tools/recompute_working_paper_empirical_results.py` | `PUBLIC_RESULT_REPRODUCTION` | Refits the frozen V3 calibration model, reselects its threshold rules, recomputes every V3 consumed-evaluation metric, and recomputes every convergence V2 calibration metric/baseline/ratio/gate from released synthetic rows and labels. It has no V2 holdout input. |
| `python3 tools/verify_working_paper_rebuild.py` | `PUBLIC_RESULT_REPRODUCTION` | Rebuilds all six figures, the 81-entry exact-number manifest, and the designated HTML and performs byte comparisons without Git metadata. |
| `python3 tools/verify_working_paper.py` | `PUBLIC_PROVENANCE_INTEGRITY` | Checks all 81 values against exact JSON pointers or exact closeout quotations and source hashes; checks six figures, six tables, and every required evidence status. |
| `python3 tools/verify_working_paper_release.py --strict-tree` | `PUBLIC_PROVENANCE_INTEGRITY` | Requires the physical snapshot to equal the manifest set, then checks hashes, local links, evidence labels, privacy/security deny-list, and forbidden V2 generation paths/signatures. |
| `python3 tools/verify_working_paper_custody.py` | `PUBLIC_PROVENANCE_INTEGRITY` | Checks the V2 holdout commitment, the recorded no-authorization/no-metrics disposition, protected-file exclusion, calibration-result binding, and absence of a holdout-derived paper result. |

The release verifier also fails closed if the dual-partition V2 builder, full deterministic
seed/partition recipe, full runtime, partition manifest, protected labels, or known generation
signatures enter the public candidate.

## What an outside researcher can and cannot reproduce

An outside researcher can rebuild every designated derived paper artifact, verify all 81 quantitative
locators, refit and reproduce the V3 calibration/evaluation outputs from released synthetic rows,
recompute the full convergence V2 calibration result from released calibration-only rows and labels,
recover every valid/descriptive/exploratory/invalid/stopped/methodological status, and verify that V2
stopped on calibration and that its unopened holdout is commitment-bound but excluded and supplies no
result.

An outside researcher cannot regenerate historical provider responses, replay unavailable external
services, or inspect/re-score the unopened convergence V2 holdout. The public package does not claim
raw-provider-response replication, and no quantitative or substantive conclusion is drawn from the
V2 holdout contents.
