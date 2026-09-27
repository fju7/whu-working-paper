# Cross-Model Semantic Replication — Terminal Closeout

Date: 2026-09-25

Terminal disposition: `CROSS_MODEL_SEMANTIC_REPLICATION_INVALID`

## Authority and frozen inputs

- directive: `WHU-CROSS-MODEL-SEMANTIC-REPLICATION-V1`;
- frozen directive SHA-256: `28934c6020d4b820aa6ddc131d71a58fcde0f51fa66122b58f727caffabfc649`;
- protocol SHA-256: `b7e073adf803ef00dc7b4f595db0a833b24598aa141e157690f0fbeb27c5bdcf`;
- results SHA-256: `90b534e51f73215bd1c574ed2df4bb5c89a1b4b359b77cae4a8350cb8ecd230c`.

Both exact model identifiers were present in authenticated provider catalogs before freeze. All 11
frozen file hashes matched; all 24 source cases and answer keys reconstructed; answer fields were
absent from model packets; and focused current/prior tests passed `18/18`. The protocol preserved all
three prior case sets, prompts, claim ladders, answer keys, case order, and scorers.

## What executed

Three structured-output `gpt-6-astra` calls at medium reasoning completed: complete-evidence claim
calibration (10 cases), known-gap consequentiality (5 cases), and falsifier identification (9 cases).
The first `claude-fable-5-1` request was attempted and returned HTTP 400 before a scoreable response.
The frozen no-retry/no-repair rule then required terminal closure. No subsequent Fable call occurred.

## What was measured

The partial Astra evidence was valid and scoreable:

- calibration: `15/15` exact, `0` overshoots, `0` unnecessary weakenings;
- consequentiality sensitivity: passed;
- genuine falsifiers identified: `10/10`;
- false falsifiers: `0` (rate `0.0`);
- missed consequential falsifiers: `0`;
- correct weakening level: `10/10`;
- exact falsifier cases: `9/9`.

This includes exact identification of both separate equal-minimum packages in
`FI03_STRONG_POSITIVE_MULTIPLE_MINIMA`, the case on which the prior Luna run missed one package.

No Fable semantic result was measured. Therefore `VALID_SCOREABLE_REPLICATION` could not be evaluated
across both named models and no cross-model replication conclusion is warranted. The invalid
disposition is a protocol-valid consequence of the provider request failure and frozen stop rule, not
a negative capability result for Fable.

## What was not measured

No acquisition, search, open-web evidence, open-world discovery, naturalistic claim, repeated-run
reliability, Fable capability, or general research reliability was measured. The Astra result is one
run on deterministic synthetic tasks and does not imply acquisition or general research competence.

## Calls, tokens, and cost

- successful scoreable semantic calls: `3`;
- semantic requests attempted: `4` of `6` authorized;
- successful-call tokens: `2,719` input, `1,315` output, `4,034` total;
- conservative accounted cost for successful calls: `$0.185880` of `$5.00` authorized;
- external search/acquisition calls: `0`.

The failed Fable request returned no usage receipt, so no token cost is attributed to it. Exact packets,
responses, response identifiers, usage, scores, partial summary, and terminal error are preserved in
`benchmark-results/cross-model-semantic-replication-v1.json`.

## Preserved history and next-step eligibility

All Luna results remain unchanged and unrescored. No repair, retry, model substitution, prior-stage
rerun, acquisition work, product engineering, human work, publication change, deployment, or outreach
occurred. No successor is authorized. Product engineering remains `PAUSED`; external outreach remains
`GENERALIZATION_EVIDENCE_INSUFFICIENT_FOR_EXTERNAL_OUTREACH`.
