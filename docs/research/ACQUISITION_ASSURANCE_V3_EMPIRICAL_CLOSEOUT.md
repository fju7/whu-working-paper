# Acquisition Assurance V3 Empirical Evaluation — Terminal Closeout

Date: `2026-09-25`  
Directive: `WHU-ACQUISITION-ASSURANCE-CALIBRATION-AND-HOLDOUT-V3`  
Terminal disposition: `SYNTHETIC_STOPPING_SIGNALS_SHOW_BOUNDED_PREDICTIVE_UTILITY`

## Execution and custody

Fred's explicit `proceed` authorized one deterministic calibration fit and one exactly-once holdout
evaluation. The execution directive was frozen and committed at `77a75e8` before fitting. All ten
reviewed V3 package hashes matched. V1/V2 history and the 1,200-observation V3 dataset, 960/240
partition, hidden labels, protocol, scorer, and independent `PASS` review remained unchanged.

The reviewed scorer fitted only the frozen families on the 960 calibration observations. Every
threshold-family winner and the logistic fit reproduced independently before holdout access. The
frozen calibration-model SHA-256 is
`abf8031fc1ad7ed3dedc200c78b076bbfa42715d668d0217b7f5c75366ddbdf0`, committed at `e09d5d4`.

The holdout path was invoked once. Its exclusive consumption claim binds that model hash and precedes
holdout evaluation. Claim SHA-256 is
`235e596ed1061f6aa8030cdf16f5337170883bd73d65a52f52d9faa64c22d4a4`; result SHA-256 is
`80039b38656235d651e11f4e3ed2ef83d358415344674383f7aba8009de25b3c`. No retry or rerun occurred or
is authorized.

## Holdout results

The untouched holdout contains 240 observations (`Y=0: 147`, `Y=1: 93`). False assurance is always
reported as claim-changing omissions among observations classified `ASSURED`, together with assurance
count and coverage.

| Frozen comparator | Rule | False assurance | Assurance | False withholding among Y=0 | Mean routes / actions / sources among assured |
|---|---|---:|---:|---:|---:|
| `B_SOURCE_COUNT` | `source_count >= 12` | 34/91 = 37.36% | 91/240 = 37.92% | 90/147 = 61.22% | 4.659 / 5.440 / 14.088 |
| `B_BUDGET` | `budget_fraction >= 0.5` | 93/239 = 38.91% | 239/240 = 99.58% | 1/147 = 0.68% | 3.766 / 4.377 / 10.695 |
| `B_RECENT_YIELD` | `recent_marginal_yield <= 0.0` | 5/17 = 29.41% | 17/240 = 7.08% | 135/147 = 91.84% | 6.118 / 7.235 / 10.588 |
| `C_DECISION_TABLE` | coverage `>=1.0`, yield `<=0.15`, unresolved `<=0`, no frontier requirement | 7/27 = 25.93% | 27/240 = 11.25% | 127/147 = 86.39% | 4.963 / 5.667 / 11.630 |
| `C_LOGISTIC` | frozen eight-feature model, cutoff 0.5 | 68/191 = 35.60% | 191/240 = 79.58% | 24/147 = 16.33% | 3.958 / 4.623 / 11.408 |

Overall classification counts `(ASSURED Y=0, ASSURED Y=1, NOT_ASSURED Y=0, NOT_ASSURED Y=1)` were:
source count `(57,34,90,59)`; budget `(146,93,1,0)`; recent yield `(12,5,135,88)`; decision table
`(20,7,127,86)`; and logistic `(123,68,24,25)`.

## Interpretation

On this deterministic synthetic distribution, the multifeature decision table had the lowest observed
false-assurance rate and also higher coverage than the lowest-false-assurance trivial baseline,
`B_RECENT_YIELD`. The logistic candidate supplied a different, high-coverage tradeoff: its observed
false assurance was lower than the source-count and budget proxies, with much higher coverage than the
recent-yield proxy. These descriptive comparisons are evidence that the frozen observable
stopping-state signals contain useful predictive information beyond the frozen trivial proxies on
this synthetic distribution.

No inferential comparison, uncertainty interval, external validation, acceptable deployment
threshold, or production/open-world error rate was prespecified or established. The false-assurance
levels remain substantial, and the lowest-rate decision table withheld assurance from 213/240 rows.
The result does not justify naturalistic, open-world, product, or general research-reliability claims.

## Cost and prohibited work

Semantic/model/provider/search/open-web calls, tokens, and external cost were
`0 / 0 / 0 / 0 / 0`, `0`, and `$0`. No product engineering, outreach, paid human work, publication,
deployment, tuning, refitting, threshold change, alternate selection, or holdout rerun occurred.

Machine-readable results:
[`ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json`](ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json).
