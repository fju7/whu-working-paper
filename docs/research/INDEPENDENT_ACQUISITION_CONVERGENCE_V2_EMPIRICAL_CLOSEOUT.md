# Independent-Acquisition Convergence V2 — Calibration-Gate Closeout

Date: `2026-09-26`
Directive: `WHU-INDEPENDENT-ACQUISITION-CONVERGENCE-V2`
Terminal disposition: `CONVERGENCE_V2_CALIBRATION_GATE_FAILED__HOLDOUT_UNOPENED`

Fred explicitly authorized one hash-bound calibration and, only if calibration produced a valid
selectable rule, one evaluation of the untouched holdout. All frozen V2 package hashes were verified
before evaluation. V1 and all earlier results remain unchanged.

V2 permits no tuning, alternate threshold, or rule selection. The sole eligible candidate was the
frozen `CONVERGENCE_FIXED_V2` rule. On all 1,294 calibration cases, it marked 281 cases `ASSURED`
and recorded false assurance of `87/281` (30.96%) at assurance coverage `281/1,294` (21.72%). False
withholding was `512/1,013` (50.54%). The prospectively frozen maximum false-assurance criterion was
15%, so the conjunctive calibration gate failed.

All three single-process-style baselines were eligible at the frozen 10% minimum coverage. Their
false-assurance results were search volume `560/1,234` (45.38%), marginal yield `130/296` (43.92%),
and coverage stopping `520/1,134` (45.86%). Convergence reduced false assurance by 29.50% relative
to the best eligible baseline, exceeding the frozen 25% condition. Observed convergence was
`281/1,294` versus `104/1,294` under the fixed cyclic-shift comparator, a ratio of 2.702. Claim-band
disagreement had hidden-omission rate `454/848` versus `134/446` under agreement, a rate ratio of
1.782. Acquisition used 5,176 routes, exactly four per observation.

Because the false-assurance condition failed, no valid selectable V2 rule remained. Per the owner
instruction, holdout authorization was not issued, the 306 holdout labels were not scored, and no
holdout result exists. There was no tuning, refitting, threshold change, alternate-rule selection,
rerun, or reinterpretation. The holdout remains untouched and eligible only under a new owner-approved
methodological successor; V2 itself is terminal.

This is a deterministic synthetic closed-universe proof-of-concept calibration result. It is not a
production or open-world error rate. Semantic/model/provider/search/open-web calls, paid humans,
product engineering, external outreach, publication, and deployment were all zero or absent. External
cost was `$0`.

Calibration result SHA-256: `01c5c0146cbea9381f269bfa973419375bde12fde2bd96a6784a394d898e64a2`.
Authorization receipt SHA-256: `30576ec1c12a8361f37f730738a5299b7127b62b0f7b4aa15af2aea97e612e44`.
