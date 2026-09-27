# Acquisition Assurance Executable Specification — Owner Blocker Closeout

Date: `2026-09-25`  
Directive: `WHU-ACQUISITION-ASSURANCE-EXECUTABLE-SPECIFICATION-V1`  
Terminal disposition: `OWNER_BLOCKER__FROZEN_MATCHED_PERTURBATION_IMPOSSIBLE`

## Authorization and isolation

Fred's explicit “proceed” authorized one bounded executable-specification milestone while preserving
the reviewed five-artifact scientific design unchanged. Work began in a new isolated worktree and
branch from the acquisition execution branch's committed base. Only the named acquisition-assurance
and canonical-state artifacts were carried into it. The existing worktree's unrelated uncommitted
research state was not modified, staged, or committed.

All five hashes in `ACQUISITION_ASSURANCE_CALIBRATION_DESIGN_FREEZE.json` verified unchanged before
implementation. The prior independent design-review disposition remains `PASS`.

## New conceptual blocker

The frozen generator cannot produce even one valid matched perturbation:

1. Its frozen contribution multiset is
   `[-2,-1,-1,0,0,0,0,1,1,1,2,2]`, whose sum is `3`.
2. The frozen complete-universe claim function maps every sum from `1` through `3` to `DIRECTIONAL`.
3. The frozen matched-pair rule requires an eligible record to change from `0` to “the smallest
   negative allowed value that changes the complete-universe claim band.”
4. Changing `0` to `-1` changes the total from `3` to `2`; changing it to `-2` changes the total from
   `3` to `1`. Both remain `DIRECTIONAL`.
5. Seed changes only permute the fixed multiset and topology. They cannot change its sum. Therefore
   the frozen pre-outcome seed-rejection loop has no accepting seed.

Resolving this requires changing at least one scientific-design element: the contribution multiset,
the claim-band thresholds, or the matched-perturbation rule. None is merely an executable convention,
and no such redesign is authorized. The required independent executable-package review cannot occur
because no faithful package or valid fixtures can be produced.

## What happened

- Frozen design artifacts verified: `5/5`.
- Isolated successor worktree created: `YES`.
- Experimental universes generated: `0`.
- Frozen runtime trajectories: `0`.
- Frozen evaluator records: `0`.
- Hidden outcomes opened or analyzed: `0`.
- Empirical gate executed: `NO`.
- Semantic/model/provider/search/open-web calls: `0 / 0 / 0 / 0 / 0`.
- Tokens and external cost: `0 / $0`.
- Prior results changed: `NONE`.
- Frozen scientific-design artifacts changed: `NONE`.

An initial local implementation probe reached the mathematically non-terminating seed-acceptance
condition before writing any universe fixture. The incomplete probe was removed; it is not an
executable package and is not frozen.

## What was not measured

No acquisition-assurance signal, false-assurance rate, false-withholding rate, discrimination metric,
proof-of-concept gate, production/open-world error rate, or capability result was measured. No fresh
independent executable-package review was performed because there was no faithful package to review.

## Owner action required

A successor requires prospective owner authorization to revise the frozen scientific design and then
repeat independent design review before executable specification resumes. The smallest candidate
repair must be selected prospectively; this closeout does not choose among changing the contribution
multiset, claim thresholds, or perturbation rule. Empirical execution remains unauthorized.
