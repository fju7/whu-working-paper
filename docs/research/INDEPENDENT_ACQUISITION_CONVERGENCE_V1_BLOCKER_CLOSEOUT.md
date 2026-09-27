# Independent-Acquisition Convergence V1 — Owner Blocker Closeout

Date: `2026-09-26`
Directive: `WHU-INDEPENDENT-ACQUISITION-CONVERGENCE-V1`
Terminal disposition: `OWNER_BLOCKER__CONVERGENCE_DESIGN_FAILS_NON_EXHAUSTION_SATISFIABILITY`

## Authorized question

Does convergence between genuinely independent evidence-acquisition processes predict hidden
claim-changing evidence adequacy substantially better than previously tested single-process stopping
signals?

Fred's explicit `test it` authorized one bounded experiment, conditional on deterministic
satisfiability and fresh independent review of the actual package before empirical evaluation. V3's
consumed holdout was excluded and remained unchanged.

## Prospective package

The V1 package fixed 1,600 new seeds and a SHA-256 partition yielding 1,295 calibration and 305
holdout universes. Each universe contains 16–28 evidence families and two processes with separate
random domains, route sets, route-selection policies, stopping policies, budgets, and state. Neither
process can inspect the other's routes, trajectory, evidence, claim, or stop state.

Mechanical reconciliation froze family-set Jaccard convergence, pivotal-family Jaccard convergence,
contrary-evidence-presence agreement, claim-band agreement/disagreement, and union evidence. The
assurance rule and three baselines—pooled search volume, pooled marginal yield, and paired
coverage/stopping—were fixed in the protocol before universe generation. The primary outcome was
false assurance among `ASSURED`, always with coverage; secondary outcomes were false withholding,
cost, and disagreement enrichment. The non-vacuity floor required at least 10% holdout assurance and
30 assured holdout cases.

## Satisfiability result

Six of seven checks passed:

- hidden omission outcomes were non-vacuous: calibration `Y=0: 1,052`, `Y=1: 243`; holdout
  `Y=0: 249`, `Y=1: 56`;
- the convergence rule would assure 201 calibration and 46 holdout cases, satisfying non-vacuity;
- claim-band disagreement occurred in 666 calibration and 144 holdout cases;
- independent domains, route sets, route policies, and isolated process execution were present;
- prohibited hidden fields were absent from runtime rows; and
- every requested metric and gate was computable.

The decisive check failed. The union of the two processes exhaustively acquired all evidence in
`234/1,295` calibration universes (18.07%) and `58/305` holdout universes (19.02%). Both exceed the
prospectively frozen maximum of 10%. Thus the design permits too much trivial success by exhaustive
search and cannot cleanly attribute any apparent assurance benefit to independent convergence.

## Stop decision

This is a conceptual design failure, not a scorer defect. Reducing budgets, enlarging universes,
changing route overlap, excluding exhaustive rows, or altering the ceiling would change the
experiment after inspecting its hidden outcomes and is prohibited by the owner's stop-not-repair
instruction.

No scorer or empirical-results path was created. Fresh independent review was not requested because
the prior mandatory satisfiability gate had already failed. No calibration selection, baseline
comparison, holdout evaluation, false-assurance estimate, or success/failure gate was computed. The
holdout is fresh and unevaluated, but the failed package is terminal and may not be reused as a
successor without new owner authorization.

## Preservation and cost

- Protocol: [`independent-acquisition-convergence-v1.json`](../../protocols/independent-acquisition-convergence-v1.json)
- Builder: [`independent_acquisition_convergence_v1.py`](../../tools/independent_acquisition_convergence_v1.py)
- Receipt: [`INDEPENDENT_ACQUISITION_CONVERGENCE_V1_SATISFIABILITY_RECEIPT.json`](INDEPENDENT_ACQUISITION_CONVERGENCE_V1_SATISFIABILITY_RECEIPT.json)
- Frozen blueprint SHA-256: `1ab3cb7ccfc4f942c25024d535c7e7276792a4c62330e38e9e1b5678678c7a82`
- Frozen runtime SHA-256: `9d623b1bfc7a9eb37793a4faad0f7bcea3ecd5d440862780312ce66a1a413441`
- Frozen evaluator SHA-256: `a1558ad5f2192c7757a2850d220b8c7e331f41119296e9eaefbe45d53395cbe8`
- Semantic/model/provider/search/open-web calls: `0 / 0 / 0 / 0 / 0`
- Tokens and external cost: `0 / $0`
- Product engineering, publication, deployment, paid humans, and external outreach: none.

The V3 model, empirical results, holdout-consumption record, and selective-escalation analysis are
unchanged.
