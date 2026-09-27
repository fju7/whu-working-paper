# Closed-Universe Evidence-Acquisition V1.4 Terminal Closeout

Date: `2026-09-25`  
Disposition: `ACQUISITION_EXPERIMENT_COMPLETE__PRIMARY_GATE_FAILED`

The final pre-semantic apparatus milestone completed as authorized. The non-benchmark synthetic
rehearsal used the exact structured-history request, tool-response append, parser, persistence, and
scorer-ingestion path. It passed in six provider turns with two SEARCH round trips, four STOP calls,
zero retries, no benchmark content, and no external search. Fresh independent closure then passed all
three required conditions and cleared one fresh benchmark execution.

The already frozen four-case experiment executed once from case/slot 1 through that same path. It
completed 27 semantic turns with zero semantic or transport retries, no provider incompatibility, and
a schema-valid result for every case. The persisted transcript was reloaded and rescored exactly.

## Result

The primary gate failed.

- Consequential evidence recall: `0.875` (required `1.0`). EA02 and EA04 each scored `0.75`.
- Irrelevant acquisition burden: `0.5458333333333333` (required at most `0.25`).
- Falsifier-directed search: `0/4` (required `4/4`).
- Final acquired-state claim calibration: `4/4` exact, with zero overshoots.
- Adequacy decisions: `4/4` exact.
- Known-gap reporting: `4/4` exact.
- Premature stops: `0`.
- Over-searching: `0`.

This is a bounded negative acquisition-capability result for this exact frozen interface, four cases,
model, configuration, and single run. It does not establish open-world or general research
reliability. The exact claim-calibration and stopping results do not cure the failed acquisition gate.

## Usage and custody

The benchmark used 114,846 input tokens and 2,047 output tokens (116,893 total), conservatively
accounted at `$0.250162`. The rehearsal used 13,815 input and 399 output tokens (14,214 total),
conservatively accounted at `$0.031620`. Both used `gpt-5.6-luna`, medium reasoning, `store: false`,
no hosted tools, no open web, and no external search.

Product engineering remains paused. External outreach and paid humans remain unauthorized. No retry,
repair, rerun, or successor is authorized by this closeout.

## Durable execution artifacts

The authoritative execution artifacts are preserved under
`docs/research/closed-universe-evidence-acquisition-v1.4/`:

- `requests-and-raw-responses.json` — SHA-256
  `1484fe0a8f6d5116cb6809668ec9eb35a4d51a6c95671ff92f78b51ba65cfbc0`;
- `transcripts.json` — SHA-256
  `2bb4766c633d7a302441ff7de97a70e7bd42efe4aed25834bcc4931df8c488df`;
- `results.json` — SHA-256
  `b5cb8646a5976332cdf2af1e886f4e576fa5d5b0b11b00e29e2875189dc9843d`;
- `execution-receipt.json` — SHA-256
  `e94bec2d3b06f2d900f350d5b97f45c7c0d53f6776237f2546a5fe83d3039ce1`;
- `scorer-ingestion-receipt.json` — SHA-256
  `73bd1d83c5fd62a955c91db4a555197a085b2ed403df039319370cd5dd1dad96`.

The terminal receipt is
`docs/research/CLOSED_UNIVERSE_EVIDENCE_ACQUISITION_V1_4_TERMINAL_RECEIPT.json`. These recovered
artifacts are the original execution outputs; no experiment or provider call was rerun.
