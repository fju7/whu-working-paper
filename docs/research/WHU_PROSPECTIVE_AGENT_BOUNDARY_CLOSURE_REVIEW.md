# Prospective agent boundary benchmark — closure review

## Verdict

**PROSPECTIVE_AGENT_BOUNDARY_BENCHMARK_NOT_READY**

The revision resolves most original design findings, but it is not ready to freeze or execute. The
specifications still contradict one another on readiness tokens and the P3 property, and the
repository contains no executable scoring harness for refusal cases that depend on joint
artifact-and-final-answer adjudication.

## Remaining material findings

1. The benchmark protocol authorizes `READY_WITH_LIMITATIONS`, while every task and model
   configuration authorizes only `READY`, `BLOCKED`, or `OWNER_ACTION_REQUIRED`.
2. P3's protected requirement says a token must be consumed atomically, while the scoring document
   and test measure only sequential duplicate-use rejection.
3. No executable harness or evaluator runs all checks, validates hashes, parses the readiness token,
   inspects diffs, applies refusal truth rules, or emits the prespecified measures. Several refusal
   cases require consequential human judgment without a frozen decision table and review procedure.
4. The two repetitions are not fully counterbalanced within model; several matched pairs retain the
   same exposure direction.
5. The human baseline plan leaves eligibility, domain mismatch, assignment, exposure, fatigue, and
   minimum-complete-dataset decisions unresolved.
6. Exact provider requests, tool schemas, adapter versions, and successful smoke receipts were
   promised but absent.

Direct WHU or condition-label leakage was not found in the model-visible trees. The boundary tasks
were inferable rather than verbatim disclosed, but the unresolved contradictions and absent evaluator
prevented execution.
