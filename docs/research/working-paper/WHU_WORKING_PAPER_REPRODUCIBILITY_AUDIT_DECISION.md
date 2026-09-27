# WHU preprint/reproducibility package audit decision

Date: `2026-09-26`

Disposition: `PREPRINT_REPRODUCIBILITY_PACKAGE_READY__PUBLIC_RELEASE_NOT_AUTHORIZED`

The proposed public package passes deterministic and outside-researcher reconstruction checks. A fresh
agent restricted to the public manifest verified 69 files, 81 exact-number entries, 49 tests, all
derived figures/ledger/HTML byte-identically, evidence-role separation, major-claim traceability,
custody boundaries, and privacy/security checks. No scientific inconsistency was detected.

The package is technically ready for an owner-approved final snapshot. It is not authorized for
public release because public author metadata, funding/conflict declarations, licenses, provider-
artifact redistribution choices, final repository/archive metadata, and approval of the exact release
commit remain owner gates.

## Exact release snapshot plan

1. Record the owner-approved public name/affiliation, ORCID choice, funding/conflict statements, and
   licenses without altering scientific claims.
2. Decide whether any raw provider material may be added; default to the audited exclusion set.
3. Regenerate `WHU_WORKING_PAPER_PUBLIC_ARTIFACT_MANIFEST.json` and run both verifiers, all 49 focused
   tests, and the byte-identical builder/HTML checks from a clean worktree.
4. Commit those owner-approved release-only changes once. Record the full commit SHA and manifest
   SHA-256 in a release receipt; tag the commit `whu-wp-2026-09-26-v0.1` or a later owner-approved
   version.
5. Archive that exact commit if desired and add its DOI/repository URL to the citation metadata.
6. Obtain explicit owner authorization for that exact commit before changing visibility, posting,
   submitting, or contacting anyone.

Provisional citation format:

> [Owner-approved author name]. (2026). *Reasoning Over Evidence Is Not Assurance That the Evidence
> Was Acquired: An exploratory empirical and methodological case study from WhatHoldsUp* (Working
> paper `WHU-WP-2026-09-26-v0.1`). [Repository/archive URL and DOI after approval].
