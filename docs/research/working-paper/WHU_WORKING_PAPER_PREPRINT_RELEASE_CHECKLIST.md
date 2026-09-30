# Preprint release checklist

Status: owner-authorized Working Paper v1.0 release.

## Proposed public contents

- [x] authoritative Markdown manuscript and review HTML;
- [x] six deterministic SVG figures and six supplementary tables;
- [x] public landing README, artifact/evidence map, and offline reproduction guide;
- [x] quantitative provenance manifest and deterministic verifier;
- [x] frozen result summaries and exact closeouts named in the public artifact manifest;
- [x] evidence-status legend and explicit valid/descriptive/exploratory/invalid/history boundaries;
- [x] limitations/non-reproducible-items register;
- [x] data/code and AI/authorship/contribution disclosure;
- [x] machine-readable public inventory with SHA-256 hashes;
- [x] citation/source-ledger and third-party-content review record;
- [x] independent outside-researcher reconstruction report and adjudication.

## Must remain private or excluded unless separately approved

- [x] conversation history and local Codex/ChatGPT state;
- [x] unopened convergence V2 holdout contents and labels;
- [x] subscriber, publication-administration, and outreach data;
- [x] credentials, environment files, service-role/admin material, and local-path receipts;
- [x] raw provider requests/responses pending explicit redistribution and terms review;
- [x] protected-reference identities or non-public personal data;
- [x] unrelated repository/product history not required to reconstruct the paper.

## Deterministic release gates

- [x] clean final release commit and immutable tag recorded on the public repository and canonical receipt;
- [x] `tools/verify_working_paper.py` passes all entries and paper boundaries;
- [x] `tools/verify_working_paper_release.py` passes inventory, hash, path, label, and deny-list checks;
- [x] figures and exact-number manifest rebuild with no diff;
- [x] review HTML rebuilds with no diff;
- [x] every former focused test is prospectively classified and mapped to its paper claim/artifact;
- [x] all checks classified public pass without provider/model calls or holdout access;
- [x] all public links are repository-relative or public external URLs; no local paths remain;
- [x] candidate files contain no detected credentials, email addresses, UUIDs, private keys, local
  Codex/ChatGPT paths, or private temporary paths;
- [x] outside-researcher reconstruction test can trace the major claims and distinguish evidence roles;
- [x] outside-researcher reconstruction test can execute the designated offline checks.

## Owner gates before any public action

- [x] confirm public author name and affiliation;
- [x] confirm ORCID omission;
- [x] approve funding statement;
- [x] approve conflict-of-interest statement;
- [x] apply CC BY 4.0 to Fred-owned paper/documentation/figures; do not invent a software/data license;
- [x] exclude all raw provider artifacts;
- [x] approve citation metadata, repository URL, no-DOI release plan, and immutable release tags;
- [x] give explicit authorization for the exact clean release commit.

No DOI was created because no already configured archive integration was available. Journal or
conference submission and external outreach remain outside this release authorization.
