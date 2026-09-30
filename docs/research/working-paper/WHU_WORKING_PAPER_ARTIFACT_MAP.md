# WHU working-paper artifact and evidence map

All paths are repository-relative and must resolve in the release snapshot. Commit `1b2821f451dae0b895eb1c4f46b84e3638cf5636`
is the reviewed manuscript baseline; the eventual release candidate must record its own full commit
hash in the public artifact manifest and release receipt.

## Paper-level map

| Paper component | Evidence role | Durable source(s) | Reproduction/verification |
|---|---|---|---|
| Abstract and integrated conclusion | Noncommensurate stratified observations motivating a matched research question | `docs/research/WHU_WORKING_PAPER_CLAIM_LEDGER.md`; sources below | `python3 tools/verify_working_paper.py` |
| §3.1 governance and custody | `METHODOLOGICAL_HISTORY` / governance | Exact closeouts named in the manuscript and supplementary Table 4 | Inspect exact dispositions; verifier checks required boundaries |
| §4.1 Stage A | `VALID_EMPIRICAL_EVIDENCE` | `benchmark-results/closed-universe-claim-strength-stage-a-v1.json` | Hash/value checks in 81-entry manifest |
| §4.1 Stage B/C | `VALID_EMPIRICAL_EVIDENCE` with failed gate | `benchmark-results/closed-universe-claim-strength-stage-bc-v1.json`; `docs/research/CLOSED_UNIVERSE_CLAIM_STRENGTH_STAGE_BC_FORENSIC_ANALYSIS.md` | Hash/value checks; forensic analysis remains post-result |
| §4.1 known-gap | `VALID_EMPIRICAL_EVIDENCE` | `benchmark-results/known-gap-robustness-v1.json` | Hash/value checks |
| §4.1 falsifier | `VALID_EMPIRICAL_EVIDENCE` | `benchmark-results/falsifier-identification-v1.json` | Hash/value checks |
| §4.1 Astra/Fable cross-model milestone | `DESCRIPTIVE_OBSERVATION` for Astra; `INVALID/INDETERMINATE_EXPERIMENT` overall | `benchmark-results/cross-model-semantic-replication-v1.json`; `docs/research/CROSS_MODEL_SEMANTIC_REPLICATION_CLOSEOUT.md` | No Fable capability result; no retry |
| §4.2 controlled acquisition V1.4 | `VALID_EMPIRICAL_EVIDENCE` with failed gate | `docs/research/closed-universe-evidence-acquisition-v1.4/results.json`; `docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_V1_4_TERMINAL_CLOSEOUT.md` | Verify frozen result and receipt hashes; do not rerun provider calls |
| §4.2 acquisition forensic analysis | `EXPLORATORY_POST_HOC_ANALYSIS` / bounded analysis | `docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_FORENSIC_CLOSEOUT.md` | Exact-quote/hash locators |
| §4.3 V3 holdout | `VALID_EMPIRICAL_EVIDENCE` on one synthetic distribution | `docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json`; `docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_CLOSEOUT.md` | Verify frozen result JSON only; the holdout is consumed and must not be rerun |
| §4.3 selective escalation | `EXPLORATORY_POST_HOC_ANALYSIS` | `docs/research/ACQUISITION_ASSURANCE_SELECTIVE_ESCALATION_ANALYSIS.md` | Verify reported frozen-score sweep outputs; no policy is validated |
| §4.3 convergence V2 calibration | `VALID_EMPIRICAL_EVIDENCE` negative calibration result | `docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_CALIBRATION_RESULT.json`; `docs/research/INDEPENDENT_ACQUISITION_CONVERGENCE_V2_EMPIRICAL_CLOSEOUT.md` | Verify calibration result; the 306-case holdout is unopened and excluded |
| §5 stopped/invalid designs | `INVALID/INDETERMINATE_EXPERIMENT` or `METHODOLOGICAL_HISTORY` | Supplementary Table 4, `docs/research/WHU_WORKING_PAPER_EVIDENCE_INVENTORY.md`, the exact closeouts in the public artifact manifest, and the privacy-safe B2A note `docs/research/working-paper/WHU_WORKING_PAPER_PUBLIC_METHOD_HISTORY.md` | No performance denominator may be inferred |
| §2 related work | External context | `docs/research/WHU_STATE_OF_FIELD_EVIDENCE_ADEQUACY_ADJACENT_WORK_MATRIX.md`; manuscript references, including Howard et al. (PMCID `PMC7700715`) and the capture–mark–recapture study (PMID `23759696`) | Repository-ledger and direct-reference verification; not a systematic review |

## Figures and tables

| Item | Source and boundary |
|---|---|
| Figure 1 | Categorical construct map from the reviewed claim/evidence architecture; not a scale or causal model |
| Figure 2 | Exact terminal dispositions preserved in the manuscript and supplementary Table 4; red and purple are different outcomes |
| Figure 3 | Stage A, B/C, known-gap, falsifier, and Astra values mapped in `WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json`; panels are not pooled |
| Figure 4 | `closed-universe-evidence-acquisition-v1.4/results.json` plus bounded forensic closeout; forensic analysis does not reverse the failed gate |
| Figure 5 | V3 holdout result/closeout and convergence V2 calibration result/satisfiability receipt; base rates and denominator definitions shown; different distributions and no cross-panel comparison |
| Figure 6 | Taxonomy of stopped/invalid episodes; no empirical frequency claim |
| Tables 1–6 | `WHU_WORKING_PAPER_SUPPLEMENTARY_TABLES.md`; all quantitative cells use the exact-number manifest or cited closeouts |

## Quantitative traceability

`WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json` contains the displayed quantitative provenance entries. Each entry records the displayed
value, repository path, JSON pointer or exact Markdown quote, SHA-256 of the frozen source, evidence
role, display transform, and verifier result. `tools/verify_working_paper.py` independently recomputes
the hashes and resolves each locator.

The map establishes provenance and reconstruction, not external validity, truth beyond the frozen
artifacts, or assurance that the historical reference artifacts were themselves complete.
