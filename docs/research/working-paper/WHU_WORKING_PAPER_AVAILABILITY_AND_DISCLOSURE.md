# Data, code, authorship, and disclosure statement

Status: public release statement for Working Paper v1.0.2.

## Data and code availability

The public snapshot contains the manuscript, deterministic figures, supplementary tables,
the exact-number provenance manifest, the frozen result summaries needed for the paper's
quantitative claims, the relevant closeouts and governance records, and the standard-library build and
verification scripts. Repository-relative paths and SHA-256 hashes are recorded in the artifact
manifest.

The package can reproduce derived figures, provenance checks, and deterministic code/data checks. It
cannot reproduce historical model behavior without new provider calls, and no such call is required
or authorized. Raw provider requests/responses and historical operational artifacts are excluded.
Their existence in the private repository does not imply redistribution permission.

The consumed V3 holdout may be represented by its frozen, already-published-within-repository result
artifact and custody record; it must not be rerun or described as untouched. The convergence V2
holdout remains unopened and is excluded from the public evidence package except for its recorded
size, hash/custody metadata where safe, and the fact that it supplied no result.

## Authorship and contributions

Frederick Ugast, Independent Researcher, is the sole accountable human author. He set owner-level scope and authority,
authorized bounded milestones and experimental execution, accepted or rejected successor work, and
retained publication and outreach control.

AI agents materially assisted with research design, code and artifact construction, execution of
authorized workflows, deterministic scoring, synthesis, drafting, review, and documentation. A fresh
AI-model reviewer examined the manuscript package, identified one material provenance-coverage defect,
and rechecked the corrected provenance manifest. The preprint-package reconstruction test was likewise
performed by a separate AI-agent context using only the proposed public package.

AI systems are not authors, cannot take responsibility for the work, and do not constitute human
expert validation. “Independent review” in this project means a context-separated model review, not
peer review, paid human review, institutional review, or validation by a domain specialist. Shared
model lineage, prompts, repository framing, and artifact selection may create correlated blind spots.

## Funding, conflicts, identity, and licensing

- **ORCID:** omitted; none was provided or supported by the repository record.
- **Funding:** no external funding. Documented model/provider/API expenditures were project costs,
  not funding. Substantial research, implementation, governance, and review labor was not monetized.
- **Conflicts of interest:** none declared.
- **Paper, documentation, and figures:** Fred-owned material is licensed CC BY 4.0 where third-party
  restrictions permit.
- **Code and data:** included for inspection and deterministic verification. The private repository
  had no existing compatible software or data license, so this release does not invent one; copyright
  is retained and no additional reuse license is granted.
- **Third-party material:** remains under its original terms and is not relicensed.
- **Raw provider material:** excluded from the public release.

The manuscript and package have not undergone independent human peer review. The fresh methodological
and reconstruction reviews were context-separated AI reviews and may retain correlated blind spots.
