# Acquisition Assurance V3 — Exploratory Selective-Escalation Analysis

Date: `2026-09-25`  
Status: `POST_HOC_DESCRIPTIVE_ANALYSIS__NOT_A_VALIDATED_POLICY`  
Frozen empirical result: `SYNTHETIC_STOPPING_SIGNALS_SHOW_BOUNDED_PREDICTIVE_UTILITY`

## Scope and custody

This analysis answers a routing-economics question after the V3 result. It does **not** alter the
prospective experiment or create a second holdout evaluation. The exactly-once holdout result remains
unchanged: 240 deterministic synthetic observations (`Y=0: 147`, `Y=1: 93`), evaluated once under the
model frozen before holdout access. No model was fitted or refitted; no feature, coefficient, ordering,
threshold-selection rule, label, or frozen artifact was changed.

The only continuous ordering used here is the frozen logistic candidate's probability of `Y=1`,
recomputed directly from its already-frozen feature means, scales, and weights. Lower scores are treated
as lower predicted omission risk. This is not a newly validated risk score: its ranking is inspected on
the same consumed holdout whose labels are used below. Thresholds and target-hitting burdens are
therefore exploratory, outcome-aware descriptions, not prospectively valid policies or performance
estimates. Rows tied at a score are routed together; arbitrary within-tie ordering is not used.

The frozen decision table exposes only a binary output, not a risk ordering. Its one legitimate
descriptive point remains 27/240 automatically assured (11.25% coverage; 88.75% escalated), with 7/27
false assurances (25.93%). No ranking was invented for it.

## Empirical routing tradeoff on the consumed synthetic holdout

For each illustrative logistic score cutoff, rows below the cutoff are automatically assured and rows
at or above it are escalated. These cutoffs were not selected in the V3 protocol. The `0.50` row alone
reproduces the frozen candidate policy.

| Exploratory `P(Y=1)` cutoff | Automatically assured | Escalated | Escalation burden | Observed false assurance among auto-assured |
|---:|---:|---:|---:|---:|
| 0.60 | 233/240 | 7/240 | 2.92% | 90/233 = 38.63% |
| **0.50 (frozen cutoff)** | **191/240** | **49/240** | **20.42%** | **68/191 = 35.60%** |
| 0.45 | 159/240 | 81/240 | 33.75% | 56/159 = 35.22% |
| 0.40 | 91/240 | 149/240 | 62.08% | 29/91 = 31.87% |
| 0.35 | 59/240 | 181/240 | 75.42% | 19/59 = 32.20% |
| 0.30 | 27/240 | 213/240 | 88.75% | 12/27 = 44.44% |
| 0.25 | 9/240 | 231/240 | 96.25% | 5/9 = 55.56% |

More escalation did not monotonically improve the observed rate. Across every score threshold that
kept at least one complete tied-score group in automatic assurance, the lowest post-hoc observed rate
was 23/78 = 29.49%, requiring escalation of 162/240 = 67.50%. Consequently, **no logistic score
threshold achieved even 10% observed false assurance**, and therefore none achieved 5%, 2%, or 1%.
That negative result is more informative than selecting and presenting a favorable-looking threshold.

This threshold sweep must not be compared as if independently validated against the prospectively
selected decision table. It uses holdout outcomes after consumption and would require a new frozen
policy and genuinely untouched evaluation data before any policy claim.

## Hypothetical independent second-review layer

This section is scenario analysis, not empirical measurement. Assume the highest logistic-risk cases
are escalated; an independent reviewer detects and removes a fixed fraction `d` of truly inadequate
(`Y=1`) escalated cases; every escalated `Y=0` case and every missed `Y=1` case returns to the assured
pool. The reviewer has no false positives, its detection rate is constant across risk strata, and its
errors do not affect the first-stage ranking. If the unreviewed group contains `L1` inadequate cases
and the escalated group contains `H1`, the scenario residual rate is:

`[L1 + (1 - d)H1] / [240 - dH1]`.

Under those intentionally favorable assumptions, the minimum score-threshold escalation burden that
meets each illustrative residual target is:

| Assumed detection among escalated `Y=1` | 10% target | 5% target | 2% target | 1% target | Residual if all 240 are reviewed |
|---:|---:|---:|---:|---:|---:|
| 50% | Not achievable | Not achievable | Not achievable | Not achievable | 24.03% |
| 75% | Not achievable | Not achievable | Not achievable | Not achievable | 13.66% |
| 90% | 226/240 = 94.17% | Not achievable | Not achievable | Not achievable | 5.95% |
| 95% | 208/240 = 86.67% | 235/240 = 97.92% | Not achievable | Not achievable | 3.07% |

“Not achievable” means not achievable on these 240 rows under the stated detection assumption even if
every case is escalated. With universal review, reaching residual targets of 10%, 5%, 2%, and 1% would
require assumed detection of at least approximately 82.44%, 91.68%, 96.77%, and 98.40%, respectively,
under the same favorable no-false-positive model.

## Interpretation and limits

On this deterministic synthetic distribution, selective escalation based on the frozen logistic
ordering is economically unattractive: the observed ordering does not isolate a low-risk automatic
assurance region, and stringent residual targets require near-universal review plus unusually high
review detection. The binary decision table lowers observed false assurance relative to the logistic
candidate but already escalates 88.75% of cases and still leaves 25.93% false assurance among the
automatically assured cases.

The second-review table is arithmetic conditional on assumed detection, not evidence that any human,
model, or workflow attains those rates. In practice, reviewer errors may be correlated with first-stage
errors because both layers may miss the same obscure evidence, share sources or retrieval failures, or
use the same cues. Positive dependence would make the independence-style scenarios optimistic.
Detection can also vary by case difficulty and risk stratum; false positives would increase burden and
change the denominator.

Finally, `Y` is a case-level indicator of at least one hidden claim-changing omission in this synthetic
benchmark. A claim-level false-assurance rate does not automatically become a report-level reliability
rate: reports can contain multiple dependent claims, one source can affect several claims, and routing,
aggregation, and severity all change the report-level probability and consequence of failure.

## Provenance and governance disposition

Inputs were read unchanged from:

- `benchmarks/acquisition-assurance-calibration-poc-v3/frozen-calibration-model.json`
  (SHA-256 `abf8031fc1ad7ed3dedc200c78b076bbfa42715d668d0217b7f5c75366ddbdf0`);
- `benchmarks/acquisition-assurance-calibration-poc-v3/runtime-observations.jsonl`;
- `benchmarks/acquisition-assurance-calibration-poc-v3/evaluator-labels.jsonl`; and
- `docs/research/ACQUISITION_ASSURANCE_V3_EMPIRICAL_RESULTS.json` and its terminal closeout.

The calculation made no semantic, model, provider, search, or open-web calls and incurred no token or
external cost. It did not invoke the holdout-evaluation command or write any benchmark/model/result
artifact. This is a subordinate exploratory artifact only. Canonical state records its completion
without changing the frozen empirical disposition or authorizing successor work; the current terminal
V3 directive is unchanged.
