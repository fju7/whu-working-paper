# Outside-researcher reconstruction review

Date: `2026-09-26`
Reviewed candidate commit: `752b7f9faf5c80434504f473bea3843689dfa997`
Context: fresh agent session restricted to the proposed public artifact manifest; no conversation
history, prior methodological review, adjudication, canonical state, hidden repository files, web
research, provider/model call, or holdout access.

## Final result: PASS

- All 69 public files existed and matched the manifest SHA-256 and byte size.
- The 81-entry exact-number ledger, six figures, six tables, and required evidence boundaries passed.
- All 49 focused deterministic tests passed.
- The seven builder outputs and HTML rendering reproduced byte-identically without writing files.
- Major empirical claims and supplementary Table 4 methodological history were traceable from public
  artifacts.
- Evidence roles, V3 consumed-once custody, convergence V2 unopened/no-result custody, and other
  unavailable/non-reproducible boundaries were distinguishable.
- No inaccessible Markdown targets, local/private paths, credentials, email addresses, UUIDs,
  protected identifiers, private keys, subscriber data, or holdout leakage were detected.
- No substantive numerical or scientific inconsistency was detected.

## Defects found and corrected before PASS

The first candidate omitted advertised tests and several artifacts named by the evidence inventory,
included a broad index with non-public link targets, and overstated completed checklist gates. The
second candidate retained two inline dependencies on that excluded index. Corrections added the
required tests and exact closeouts, removed the broad-index dependency, implemented public Markdown
target validation, corrected one OpenEvidence artifact filename, and supplied a privacy-safe,
hash-bound B2A methodological-history note in place of the protected full closeout. Neither correction
changed a scientific result, quantitative value, gate, or conclusion.

Public release was not reviewed or authorized. Owner metadata, declarations, licenses, final release
commit approval, repository visibility, posting, submission, and outreach remain outside this review.
