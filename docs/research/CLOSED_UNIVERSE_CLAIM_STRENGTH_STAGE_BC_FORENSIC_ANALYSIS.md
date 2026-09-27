# Stage B/C unnecessary-weakening forensic analysis

Date: 2026-09-25

Disposition: `STAGE_BC_FORENSIC_ANALYSIS_COMPLETE`

## Scope and preservation

This is a deterministic comparison of the frozen Stage B and Stage C packets and outputs from
`CLOSED_UNIVERSE_CLAIM_STRENGTH_CALIBRATION_STAGE_BC_V1`. It does not rerun or rescore the experiment.
Stage A, the Stage B/C scores, all classifications, and terminal disposition
`STAGE_BC_GAP_DISCLOSURE_GATE_FAILED` remain unchanged.

The four frozen Stage B `UNNECESSARY_WEAKENING` cases are `BC01`, `BC03`, `BC06`, and `BC07`.

## What changed in the model-visible evidence

The acquired scores, claim options, record rule, and selection rule were identical across conditions.
Stage C added four fields per case: `complete_universe_size`, `acquired_count`, `missing_count`, and the
allowed missing-score set `[-1, 0, 1]`. The allowed set repeated a constraint already present in the
shared record rule; the decisive new numeric quantity was the finite missing count, with the universe
and acquired counts providing a consistency identity.

| Case | Identical acquired scores | Stage C-only counts (universe/acquired/missing) | B claim and stated basis | Completion range disclosed in C | C claim and stated basis |
|---|---|---:|---|---:|---|
| `BC01` | `[1,1,1,1]` | `6/4/2` | `UNRESOLVED`; completeness was not established | `[2,6]` | `POSITIVE`; total at least 2, not necessarily 4 |
| `BC03` | `[1,1,1,1,1]` | `7/5/2` | `UNRESOLVED`; no gap disclosure did not prove completeness | `[3,7]` | `POSITIVE`; total at least 3, not necessarily 4 |
| `BC06` | `[-1,-1,-1,-1]` | `6/4/2` | `UNRESOLVED`; no completeness statement guaranteed the complete-universe total | `[-6,-2]` | `NEGATIVE`; total at most -2, not necessarily -4 |
| `BC07` | `[-1,-1,-1,-1,-1]` | `7/5/2` | `UNRESOLVED`; supplied records were not established as complete | `[-7,-3]` | `NEGATIVE`; total at most -3, not necessarily -4 |

The C ranges are transparent consequences of acquired sum ± the two missing records' allowed scores.
They are also restated, with the same limiting bound, in each frozen Stage C reason.

## Supported findings

1. **Stage B expressed uncertainty about completeness, not a specific inferred gap.** All ten Stage B
   claims were `UNRESOLVED`, and every reason referred to absent completeness or possible unacquired
   records. Nothing in the Stage B packet supplied a universe size or an upper bound on missing count.

2. **The Stage B packet did not make the four directional answer keys derivable from model-visible
   information alone.** Given the shared instruction not to treat silence as proof of completeness,
   and no finite bound on possible missing records, an arbitrary number of opposite-sign missing
   scores remained compatible with the packet. The evaluator's four directional labels depended on
   the prospectively frozen but Stage B-hidden missing counts. This is an information-state mismatch,
   not a rescore: the recorded `UNNECESSARY_WEAKENING` classifications remain the experiment's frozen
   classifications.

3. **Stage C supplied sufficient finite bounds for exactly the four corrections.** In `BC01`, `BC03`,
   `BC06`, and `BC07`, the worst allowed two-record completion could not cross zero. In the other six
   cases, the disclosed worst-case range reached zero, so `UNRESOLVED` remained exact. The B→C change
   therefore aligns case by case with whether the newly calculable range guaranteed a sign.

4. **The corrected claims occupy the directional, not strong, rung.** Treating the acquired subset as
   complete would yield `STRONG_POSITIVE` or `STRONG_NEGATIVE` in all four cases. The finite gap bound
   preserved direction but made the strong threshold non-guaranteed, matching each Stage C reason.

## Explanation assessment

### Best supported explanation

The best explanation supported by the durable outputs is **bounded relevance clarification**: Stage C
turned unspecified possible missingness into a finite arithmetic interval. The model's stated reasons
then used the limiting endpoint of that interval and selected the corresponding directional rung.
This explains both the four changes and the six non-changes without altering the frozen scores.

### Supported component, but not a complete causal account

**Implicit incompleteness handling** is directly visible in Stage B's reasons: the model declined every
directional claim because completeness was not established. It is more precise to say the model treated
missingness as possible and unbounded than to say it inferred the experiment's actual hidden gaps.

**Claim-ladder structure** describes the form of all four corrections: `UNRESOLVED` became directional,
while the apparent complete-subset claim would have been strong. The ladder helps characterize the
answer selected after bounding missingness; it does not independently explain why the conditions
differed.

### Consistent but not identified

The explicit `acquisition_gap` object, repeated score range, and completeness counts may have acted as
**format or relevance cues** beyond their numeric content. The run does not isolate field naming,
redundancy, or arithmetic information, so cueing cannot be separated from substantive clarification.

Because Stage B and Stage C were separate calls with one sample per condition, **run noise** also cannot
be excluded. The exact alignment of all ten C reasons with their disclosed ranges is evidence of a
coherent observed pattern, but it is not a repeated-run estimate and cannot establish that disclosure
caused or would reliably reproduce the corrections.

## Bottom line

The four B→C corrections are best described as recovery from an underdetermined Stage B information
state once Stage C supplied a finite missing-record bound. The frozen run supports a descriptive link
between calculable completion ranges and the model's selected claim rung. It does not identify which
prompt feature caused the behavior, establish a stable disclosure effect, or rehabilitate the failed
preregistered overshoot-reduction gate.

Provider/model calls, search/acquisition calls, reruns, rescoring, repairs, new cases, and external cash
cost for this forensic analysis: zero.
