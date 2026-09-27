# WHU working paper: reproducibility package

Release status: **public working-paper release**.

Version: **Working Paper v1.0.1, September 2026**

Author: **Frederick Ugast, Independent Researcher**

Canonical repository: <https://github.com/fju7/whu-working-paper>

Immutable release tag: `working-paper-v1.0.1`

This directory contains the reviewed working paper *Reasoning Over Evidence Is Not Assurance That the
Evidence Was Acquired* and the public repository package that supports it. The paper is an
exploratory empirical and methodological case study, not a general verdict on frontier models and not
a validated deployment policy.

## Start here

1. Read [`WHU_WORKING_PAPER_MANUSCRIPT.md`](WHU_WORKING_PAPER_MANUSCRIPT.md).
2. Use [`WHU_WORKING_PAPER_ARTIFACT_MAP.md`](WHU_WORKING_PAPER_ARTIFACT_MAP.md) to trace each major
   claim, section, figure, and table to frozen repository evidence.
3. Follow [`WHU_WORKING_PAPER_REPRODUCTION.md`](WHU_WORKING_PAPER_REPRODUCTION.md) for offline,
   deterministic checks. These commands do not call a model or provider, do not use the network, and
   do not reopen either consumed or unopened holdouts.
4. Read [`WHU_WORKING_PAPER_AVAILABILITY_AND_DISCLOSURE.md`](WHU_WORKING_PAPER_AVAILABILITY_AND_DISCLOSURE.md)
   for data/code availability, authorship, AI contribution, licensing, and redistribution boundaries.
5. Read [`WHU_WORKING_PAPER_LIMITATIONS_REGISTER.md`](WHU_WORKING_PAPER_LIMITATIONS_REGISTER.md) for
   items that cannot be fully reconstructed or reproduced.
6. Read [`WHU_WORKING_PAPER_PUBLIC_TEST_CLASSIFICATION.md`](WHU_WORKING_PAPER_PUBLIC_TEST_CLASSIFICATION.md)
   for the claim-by-claim classification of all 49 internal focused tests and the public substitute
   checks.
7. Read [`WHU_WORKING_PAPER_FRESH_INDEPENDENT_PUBLIC_REVIEW_2026_09_27.md`](WHU_WORKING_PAPER_FRESH_INDEPENDENT_PUBLIC_REVIEW_2026_09_27.md)
   and its [`adjudication`](WHU_WORKING_PAPER_PUBLIC_REVIEW_ADJUDICATION_2026_09_27.md) for the final
   outside-researcher review.

Citation and third-party-content boundaries are recorded in
[`WHU_WORKING_PAPER_CITATION_AND_LICENSE_AUDIT.md`](WHU_WORKING_PAPER_CITATION_AND_LICENSE_AUDIT.md).

The release inventory and integrity hashes are machine-readable in
[`WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json`](WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json).
The release checklist and terminal audit decision are in
[`WHU_WORKING_PAPER_PREPRINT_RELEASE_CHECKLIST.md`](WHU_WORKING_PAPER_PREPRINT_RELEASE_CHECKLIST.md) and
[`WHU_WORKING_PAPER_REPRODUCIBILITY_AUDIT_DECISION.md`](WHU_WORKING_PAPER_REPRODUCIBILITY_AUDIT_DECISION.md).
The earlier public-package-only reconstruction is recorded in
[`WHU_WORKING_PAPER_OUTSIDE_RECONSTRUCTION_REVIEW.md`](WHU_WORKING_PAPER_OUTSIDE_RECONSTRUCTION_REVIEW.md).
The v1.0 release candidate uses the redesigned public contract and adds a separate custody verifier.

## How to read status labels

- `VALID_EMPIRICAL_EVIDENCE`: executed under a frozen design and reconstructable within the stated
  task, model, run, and partition. It does not imply generalization.
- `DESCRIPTIVE_OBSERVATION`: separately scoreable observation from a milestone that was invalid
  overall. It cannot validate the intended comparison.
- `EXPLORATORY_POST_HOC_ANALYSIS`: analysis performed after results were known. It may narrow or
  generate hypotheses but is not confirmatory.
- `INVALID/INDETERMINATE_EXPERIMENT`: the intended inference is unsupported because of design,
  execution, custody, provider-compatibility, evaluator, or reconstruction failure.
- `METHODOLOGICAL_HISTORY`: a stopped design or review episode used to document measurement and
  governance lessons, not model performance.

The manuscript and supplementary Table 1 apply these labels to every included study. Supplementary
Table 4 lists invalid, indeterminate, and stopped episodes and their prohibited inferences.

## Release boundary

This public snapshot contains only the reviewed release inventory. It excludes raw provider
requests/responses, the unopened convergence V2 holdout, credentials, subscriber or publication
administration data, local receipts, conversation history, and unrelated product/repository history.
See the availability statement and license notice for the exact reuse boundaries.
