# Supplementary tables — WHU working paper

These tables implement the frozen figure/table plan. Exact numbers are verified by
`WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json`; study-level statuses and source paths are controlled
by the public-package copy of `docs/research/WHU_WORKING_PAPER_EVIDENCE_INVENTORY.md` and the exact
closeouts included in `WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json`.

## Table 1. Complete evidence inventory

| Study | Question | Model/process | N/partition | Prospective status | Result | Paper role | Prohibited inference | Primary artifact |
|---|---|---|---|---|---|---|---|---|
| B1 reference-rich synthesis | Can a bounded supplied corpus support structured synthesis? | WHU pipeline | B1 program | Frozen program | Bounded feasibility demonstrated | `VALID_EMPIRICAL_EVIDENCE` context | Open-world acquisition or full economics | `B1_PROGRAM_FINAL_SYNTHESIS.md` |
| Stage A | Strongest warranted claim from supplied evidence? | Luna, one run | 10 cases | Frozen | 10/10 exact; 0 overshoot | `VALID_EMPIRICAL_EVIDENCE` | General research reliability | `closed-universe-claim-strength-stage-a-v1.json` |
| Stage B/C | Does truthful finite-gap disclosure reduce overshoot? | Luna, matched conditions | 10 paired cases | Frozen gate | 6/10 vs 10/10 exact; 0 overshoot both; gate failed | `VALID_EMPIRICAL_EVIDENCE` with failed gate | Overshoot-reduction effect | `closed-universe-claim-strength-stage-bc-v1.json` |
| Stage B/C forensic | Why did four cases change? | Deterministic review | Same 10 cases | Post-result bounded analysis | Changes aligned with finite completion bounds | `EXPLORATORY_POST_HOC_ANALYSIS` / valid bounded analysis | Causality or rescore | `CLOSED_UNIVERSE_CLAIM_STRENGTH_STAGE_BC_FORENSIC_CLOSEOUT.md` |
| Known-gap robustness | Can supplied unresolved-evidence bounds be used correctly? | Luna, one run | 5 cases | Frozen | 5/5 exact; consequentiality sensitivity passed | `VALID_EMPIRICAL_EVIDENCE` | Open-world discovery | `known-gap-robustness-v1.json` |
| Falsifier identification | Can offered minimum weakening packages be identified? | Luna, one run | 9 cases; 10 true minima | Frozen | 9/10 true; 0 false; one equal minimum missed | `VALID_EMPIRICAL_EVIDENCE` | Open-world falsifier search | `falsifier-identification-v1.json` |
| Cross-model milestone | Do Astra and Fable replicate frozen families? | Astra and attempted Fable | Three families | No-retry | Astra perfect; Fable HTTP 400; milestone invalid | `DESCRIPTIVE_OBSERVATION` for Astra only | Fable capability or replication | `CROSS_MODEL_SEMANTIC_REPLICATION_CLOSEOUT.md` |
| Acquisition V1.4 | Can an agent acquire enough consequential evidence and stop? | Luna via specialized interface | 4-case execution | Frozen conjunctive gate | Exact terminal outputs; recall .875; burden .5458; directed 0/4; gate failed | `VALID_EMPIRICAL_EVIDENCE` | Broad unreliability or incapability | `CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_V1_4_TERMINAL_CLOSEOUT.md` |
| Acquisition forensic | What did the misses and directed score mean? | Deterministic review | Same 4 cases | Post-result bounded analysis | Misses did not change bands; metric entangled with hidden intent/basis | `EXPLORATORY_POST_HOC_ANALYSIS` / valid bounded analysis | Reverse the gate | `CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md` |
| V3 assurance | Do runtime stopping features predict hidden residual omission? | Frozen decision table and logistic | 240-row holdout | Exactly once | 7/27 at 27/240; 68/191 at 191/240 | `VALID_EMPIRICAL_EVIDENCE` synthetic holdout | Production rate or reliability pass/fail | `ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json` |
| Selective escalation | Could post-hoc score routing lower observed false assurance cheaply? | Frozen-score sweep | Same consumed 240 rows | Post-hoc | No complete-tie point below 10%; best 23/78 with 162/240 escalated | `EXPLORATORY_POST_HOC_ANALYSIS` | Validated policy or cost curve | `ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md` |
| OpenEvidence case | Which public controls are documented? | Bounded public case review | Public sources | External review | Strong access/provenance controls; no reviewed public case-level completeness validation | External context | Product inadequacy audit | `OPENEVIDENCE_ASSURANCE_CASE_STUDY.md` |
| Convergence V2 | Does isolated-process convergence support assurance? | Two scripted processes, sole frozen rule | 1,294 calibration; 306 unopened holdout | Frozen conjunctive gate | 87/281 false assurance; gate failed | `VALID_EMPIRICAL_EVIDENCE` negative calibration | Holdout or open-world performance | `INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json` |

## Table 2. Semantic experiments

| Row | Exact | Overshoot | Unnecessary weakening / false selection | Status and boundary |
|---|---:|---:|---:|---|
| Stage A | 10/10 | 0/10 | 0/10 | One Luna run; deterministic synthetic; no acquisition |
| Stage B, no gap disclosure | 6/10 | 0/10 | 4/10 unnecessary weakenings | Matched frozen condition |
| Stage C, truthful gap disclosure | 10/10 | 0/10 | 0/10 | Stage B/C gate failed because overshoot reduction was 0 |
| Known-gap | 5/5 | 0/5 | 0/5 | Supplied bounds; one Luna run |
| Falsifier | 8/9 cases exact; 9/10 true minima | n/a | 0 false; 1 equal minimum missed | Offered candidates; one Luna run |
| Astra descriptive inset | 15/15 calibration; 9/9 falsifier cases; 10/10 minima | 0 | 0 | Overall milestone `CROSS_MODEL_SEMANTIC_REPLICATION_INVALID`; no Fable result |

No row is pooled with another. All tasks are deterministic synthetic and test evidence-visible reasoning, not open-world acquisition.

## Table 3. Acquisition and assurance studies

| Study/rule | Partition | Assurance or terminal coverage | False assurance / acquisition metrics | Gate/result | Validity boundary |
|---|---|---:|---|---|---|
| Acquisition V1.4 | Four-case execution | 4/4 exact claims, adequacy, gaps | recall .875; burden .5458; directed 0/4 | `ACQUISITION_EXPERIMENT_COMPLETE__PRIMARY_GATE_FAILED` | Specialized interface; one Luna run |
| V3 decision table | 240-row holdout | 27/240 (11.25%) | 7/27 (25.93%) | Descriptive; no outcome threshold | One deterministic synthetic distribution |
| V3 logistic | 240-row holdout | 191/240 (79.58%) | 68/191 (35.60%) | Descriptive; no outcome threshold | Same holdout; distinct candidate |
| V3 post-hoc routing | Same consumed holdout | 78 retained; 162/240 escalated | 23/78 (29.49%) best complete-tie point | Exploratory only | No validated policy; assumed reviewer scenarios |
| Convergence V1 | Stopped before review/evaluation | n/a | n/a | `OWNER_BLOCKER__CONVERGENCE_DESIGN_FAILS_NON_EXHAUSTION_SATISFIABILITY` | No performance result |
| Convergence V2 sole rule | 1,294-row calibration | 281/1,294 (21.72%) | 87/281 (30.96%); false withholding 512/1,013 | `CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED` | Calibration only; 306-row holdout unopened |

## Table 4. Prospectively failed, stopped, or invalid episodes

| Intended question | Exact controlling disposition | Paper role | Model called? | Invalidating/stopping condition | Valid remainder | Prohibited inference |
|---|---|---|---|---|---|---|
| B2A-v2 acquisition score | `NOT_INTERPRETABLE` | `INVALID/INDETERMINATE_EXPERIMENT` | Yes historically | Missing evaluation denominator and durable-state failure | Method/custody lessons | B2 capability score |
| Architecture viability | `CURRENT_LLM_DRIVEN_ARCHITECTURE_NOT_VIABLE_BUT_WHU_HYPOTHESIS_REMAINS_OPEN` | `METHODOLOGICAL_HISTORY` | Historical program | Composition/authority defects | Bounded architecture decision | General LLM incapability |
| Stronger-model historical counterfactual | `INDETERMINATE` | `INVALID/INDETERMINATE_EXPERIMENT` | Attempts occurred | Reconstruction, leakage, evaluator, provider-equivalence limits | Failure taxonomy | Stronger-model effect |
| Historical task re-execution | `HISTORICAL_COUNTERFACTUAL_PROGRAM_NOT_RECONSTRUCTABLE` | `METHODOLOGICAL_HISTORY` | No valid execution | Authentic task/state unavailable | Reconstructability finding | Model result |
| Prospective boundary benchmark | `STOPPED_BEFORE_MODEL_EXECUTION` | `METHODOLOGICAL_HISTORY` | No | Conflicting specifications and absent evaluator | Design lesson | Semantic capability |
| Warranted Trust V1 | `V1_FRAMEWORK_NOT_USEFUL` | `METHODOLOGICAL_HISTORY` | Not empirical | Construct reduced to existing fields | Terminology decision | Empirical trust result |
| Cross-model semantic replication | `CROSS_MODEL_SEMANTIC_REPLICATION_INVALID` | `INVALID/INDETERMINATE_EXPERIMENT`; Astra subresult descriptive | Astra yes; Fable request failed | Fable HTTP 400 under no-retry rule | Astra frozen scores | Fable capability or replication |
| Claim-changing closure | `OWNER_BLOCKER__PREEXECUTION_REVIEW_NOT_PASSED`; then `CLAIM_CHANGING_CLOSURE_CONCEPT_NOT_OPERATIONALIZED` | `METHODOLOGICAL_HISTORY` | No | Hidden-evaluator oracle and incompatible trajectory | Failure diagnosis | Capability; gate result |
| Assurance execution | `OWNER_BLOCKER__FROZEN_EXECUTION_SPECIFICATION_NOT_DETERMINATE` | `METHODOLOGICAL_HISTORY` | No | Generator/analysis underdetermined; no reviewed runner | Specification lesson | Rate or capability |
| Assurance executable successor | `OWNER_BLOCKER__FROZEN_MATCHED_PERTURBATION_IMPOSSIBLE` | `METHODOLOGICAL_HISTORY` | No | Allowed perturbation cannot change band | Satisfiability proof | Empirical result |
| Assurance prospective revision | `OWNER_BLOCKER__REVISED_DESIGN_DENOMINATORS_NOT_CONSTRUCTIBLE` | `METHODOLOGICAL_HISTORY` | No | Zero strict eligible states; one paired block | Corrected satisfiability result | Empirical result |
| Convergence V1 | `OWNER_BLOCKER__CONVERGENCE_DESIGN_FAILS_NON_EXHAUSTION_SATISFIABILITY` | `METHODOLOGICAL_HISTORY` | No semantic/model call | Union exhausts too many universes | Six passed design checks | Convergence performance |
| Convergence V2 holdout | `CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED` | Governance observation | No holdout call/access | Calibration gate failed | Stopping-rule compliance | Holdout performance |

## Table 5. Claim and competing-explanation matrix

| Claim | Supporting evidence | Counterevidence | Alternative explanation | Maximum wording |
|---|---|---|---|---|
| Strong supplied-evidence reasoning in small tasks | Stage A; known-gap; falsifier; Stage C; Astra descriptive observations | Mostly one run; synthetic; invalid overall cross-model milestone | Explicit small tasks may be easy or encode designer regularities | Strong in these small deterministic supplied-evidence tasks |
| Correct outputs can coexist with failed acquisition | Four-case acquisition result | Misses did not change bands; metric entanglement | Interface/instruction/evaluator defects | One valid four-case run produced correct terminal outputs while failing its frozen gate |
| V3 stopping features carried signal | Candidate/baseline risk–coverage differences | Substantial false assurance; no outcome gate; one distribution | Synthetic base rates and feature regularities | Descriptive predictive information on one 240-row holdout |
| Convergence V2 carried signal but failed absolutely | Relative baseline reduction; chance ratio | 30.96% false assurance exceeded 15%; no holdout | Correlated routes/priors; synthetic distribution | Calibration-only negative gate result |
| WHU shows an evidence-visible/acquisition-assurance asymmetry | Stratified synthesis of valid results | Different tasks, scales, and models; no causal comparison | Unequal task difficulty and engineering maturity | Bounded within-program qualitative interpretation |
| Field composition not established by bounded review | State-of-field review across adjacent methods | Strong bounded methods and deployed controls exist | Proprietary/specialized/unreviewed methods may exist | Reviewed public evidence did not establish the full economical calibrated open-world composition |

## Table 6. Adjacent literature and WHU boundary

| Literature family | Problem addressed | Assurance object | Validation mode | Residual gap relative to WHU | Relationship to WHU |
|---|---|---|---|---|---|
| Grounding, faithfulness, citation accuracy | Whether output is supported by supplied sources | Claims versus given context | Benchmarks, attribution checks | Adequacy of unseen/source-set evidence | Corresponds to evidence-visible reasoning and provenance |
| High-recall / total-recall retrieval | Find nearly all relevant records in a collection | Recall within a defined corpus | Exhaustive labels, sampling, TAR studies | Upstream collection/source-family completeness and claim consequence | Closest mature retrieval precedent; defeats novelty claim |
| Statistical stopping and capture–recapture | Estimate residual records or recall | Remaining relevant items under assumptions | Probability samples, overlap models | Open-world scope and claim-changing labels | Prior art for stopping and convergence |
| ROB-ME / ROB-MEN | Bias from missing studies/results in a synthesis | Specified synthesis result | Structured judgments and missingness assumptions | General acquisition certificate outside a defined synthesis | Close precedent for decision-relative consequence |
| Context sufficiency / agentic RAG | Whether retrieved context can answer a question | Available/retrieved context | QA benchmarks and iterative retrieval | Open-world closure | Local adequacy analogue; not completeness proof |
| Selective prediction / abstention | When to answer versus defer | Answer error under a score | Calibration and risk–coverage curves | Whether score responds to unseen evidence | Correct framing for escalation economics |
| Scalable oversight | Weaker supervision of stronger systems | Judge/supervisor success | Controlled empirical tasks | Whether all parties missed the same evidence | Addresses audit-capability gap, not acquisition completeness |
| Assurance cases | Structured support for a system property | Claims, evidence, assumptions, defeaters | Process/framework validation | Empirical support for acquisition adequacy | Better umbrella structure than a new trust construct |
| Research-agent evaluations | End-to-end answers, reports, citations, targets | Task accuracy/report quality | Known answers, rubrics, expert references | Hidden claim-changing omissions | Adjacent but usually different target |
| Professional bounded systems | Retrieval and grounded advice in authoritative domains | Defined corpora and accountable workflow | Product studies, professional audit | Generalization to non-auditing/open-web user | Strong counterexample: narrowing and expert review may solve important cases |
