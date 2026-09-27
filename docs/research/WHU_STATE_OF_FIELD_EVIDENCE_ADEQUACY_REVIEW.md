# State of the field — evidence adequacy, retrieval completeness, and assurance

Date: `2026-09-26`
Disposition: `STATE_OF_FIELD_REVIEW_COMPLETE__OWNER_REVIEW_REQUIRED`
Research type: bounded external literature/context review; **not** a WHU experiment

## Executive conclusion

WHU's central concern is already recognized, but fragmented across fields and usually solved only
after the world has been made bounded enough to score.

The field has mature names and methods for important pieces: grounding and faithfulness for claims
against supplied sources; high-recall or total-recall information retrieval; recall estimation and
statistical stopping for bounded document collections; context sufficiency in RAG; calibrated
abstention and risk–coverage analysis; scalable oversight; trajectory/process monitoring; and
argument-based assurance cases. Frontier research products add persistent browsing, parallel search,
source-linked claims, citation agents, iterative retrieval, and sufficiency checks.

Those developments materially narrow WHU's claim. It would be wrong to say that nobody has noticed
the problem, that completeness assurance is wholly unsolved, or that deployed systems merely reason
over whatever context first appears.

What this review did **not** find is equally specific: public, independently validated evidence that a
general open-world research system can issue a calibrated, case-level assurance that no still-unseen
evidence would materially change its conclusion, for a sophisticated user who cannot audit the work,
while retaining favorable oversight economics. The best validated completeness methods operate over
defined collections with expensive ground truth, human relevance judgments, probability samples, or
externally scorable tasks. Current research-agent benchmarks mainly score answers, citations, known
targets, or final-report quality. They rarely make the hidden consequential omissions—the denominator
WHU used—both knowable to the evaluator and unavailable to the acquisition process.

This is a meaningful integration and validation gap, not a demonstrated novel phenomenon and not a
proof of general model incapability.

## 1. The five questions are different

### 1.1 Correctness conditional on supplied evidence

Google DeepMind's FACTS Grounding is the cleanest prominent example. Its tasks require answers that are
comprehensive and attributable to a supplied document, and its paper explicitly distinguishes
grounding against given context from factuality against external sources and world knowledge. That is
almost exactly WHU's “evidence-visible reasoning” layer. LongFact/SAFE likewise evaluates emitted
facts by searching for supporting evidence.

These are serious measurements. They do not test whether the evidence state supplied to the model is
adequate.

### 1.2 Evidence fidelity and provenance

RAG evaluation, research-agent benchmarks, and deployed products devote substantial attention to
faithfulness, citation accuracy, source attribution, and authoritative corpora. RAGAS separates
retrieval metrics from generation faithfulness. DeepResearch Bench scores citation accuracy and
effective citations. Anthropic uses a separate CitationAgent. OpenAI Deep Research, OpenEvidence, and
CoCounsel expose sources or linked citations.

This layer addresses fabricated or misrepresented support. A perfectly faithful report can still omit
an uncited source that would reverse or materially weaken it.

### 1.3 Evidence acquisition adequacy and completeness

The mature adjacent field is not primarily “AI agents”; it is high-recall information retrieval.
**Total recall** systems, technology-assisted review (TAR), e-discovery, and systematic-review
screening explicitly optimize finding all or nearly all relevant documents while controlling review
burden. Systematic-review authors describe the core difficulty in WHU-like terms: true recall is
unknown before all records are screened because the denominator is unknown.

This literature is highly relevant and defeats a novelty claim. It also exposes a boundary. Most
methods begin with a defined candidate collection. They can estimate missed relevant records within
that collection; they do not establish that the databases, searches, source families, dates, languages,
or grey literature used to construct it were themselves complete.

Evidence-synthesis practice also governs that upstream construction problem procedurally. Cochrane
requires extensive, reproducible multi-source searching within resource limits, and PRESS provides
independent peer review of search strategies. Capture–recapture methods go further by using overlaps
between routes to estimate missed records under statistical assumptions. This is important prior art
for WHU's independent-acquisition work: route overlap as evidence about an unseen population long
predates LLM agents. WHU's narrower difference is labeling hidden items by potential claim change and
testing whether convergence supports an assurance decision; it must not describe convergence itself as
novel.

### 1.4 Assurance that claim-changing evidence was not missed

WHU's distinctive emphasis is not generic recall. It is whether unseen evidence would change the
strongest defensible claim, and whether observable stopping states are calibrated against that hidden
consequence.

The state-of-field review found close partial precedents:

- statistical stopping estimates remaining relevant records and confidence in target recall;
- capture–recapture estimates unseen records from overlaps among search routes;
- ROB-ME/ROB-MEN assess whether entire missing studies or selectively unavailable results could bias
  a specified meta-analysis result;
- Google classifies whether retrieved context is sufficient for the question and iterates if it is not;
- legal statutory benchmarks compare systems with expensive expert-built reference sets intended to be
  exhaustive, while later error analysis shows that those references can themselves omit requirements;
- selective prediction calibrates when a system should answer or abstain;
- assurance cases organize the claim, evidence, assumptions, and defeaters for a system property.

But topical relevance, answer sufficiency, and claim-changing consequentiality are not interchangeable.
A missed relevant study might not affect the conclusion; one obscure controlling source might. Public
research-agent evaluations generally do not label a complete hidden universe by contribution to a
final claim and then calibrate a runtime assurance decision against residual consequential omissions.

The missing-evidence-bias literature is an important exception to any suggestion that consequence is
ignored. ROB-ME and ROB-MEN direct structured judgments at a particular synthesis result and ask whether
known or assumed missing studies/results matter, given selection mechanisms tied to direction or
magnitude. This is closer to decision-relative consequentiality than retrieval recall. It is not an
open-world acquisition certificate: the judgment is synthesis-specific and depends on what missingness
is known or assumed, study-registration/search information, and reporting-bias reasoning.

This absence statement is bounded: it means no such validated general method was identified in the
major lines and actors reviewed. It does not mean no unpublished system, specialized method, or paper
outside the search exists.

### 1.5 Escalation and oversight economics

Selective prediction supplies the right formal shape: risk versus coverage. High-recall IR supplies
work-saved-versus-recall trade-offs. Scalable oversight asks whether weaker humans/models can judge
stronger work. Multi-agent research increases token and coordination costs; Google reports that more
agents can help parallelizable tasks and hurt sequential ones. Professional systems narrow sources and
keep domain experts in the verification loop.

The field therefore recognizes the economic problem, but no reviewed public source establishes a
general curve from research-agent stopping signals to residual claim-changing risk plus real expert
review cost. WHU's selective-escalation analysis fits this gap, within its synthetic and exploratory
limits.

## 2. What major actors are measuring and building

### METR

METR's task-completion time horizon estimates success probability as task duration increases. This is
a mature long-horizon capability measure on scorable technical tasks, not an assurance measure for
open-ended evidence synthesis. METR's separate work on algorithmic versus holistic evaluation is a
useful warning that benchmark grades can miss deployment-relevant quality. It supports WHU's layer
separation but does not validate WHU's acquisition construct.

### OpenAI

BrowseComp measures persistent acquisition of a hard-to-find target. It deliberately uses short,
verifiable answers and calls itself incomplete. Deep Research demonstrates substantial browsing and
synthesis capability with source-linked outputs. The BrowseComp paper's confidence results are
especially relevant: browsing performance and self-confidence calibration need not move together.
OpenAI does not publicly claim a per-report open-world completeness guarantee in the reviewed sources.

### Anthropic

Anthropic's Research architecture attacks coverage through parallel subagents, adaptive search, a
lead agent, and a CitationAgent. This is important contrary evidence: a serious deployed system is
explicitly engineered for breadth, dynamic effort, and attribution. Yet the public description leaves
“sufficient information” as an agent decision and does not show calibration against a hidden set of
consequential omissions. Parallelism is a coverage mechanism, not by itself an assurance certificate.

### Google DeepMind / Google Research

Google spans all three nearby layers: FACTS/SAFE for grounding and factuality; sufficient-context and
agentic RAG for iterative retrieval; and multi-agent/AI-for-science systems for search, hypothesis
generation, reflection, and validation. Its sufficient-context work is the closest prominent term to
WHU's local adequacy question. The important boundary is that context can be sufficient to answer from
the retrieved/indexed material without establishing open-world closure.

### Academic and independent work

High-recall IR, systematic-review stopping, and missing-evidence-bias assessment provide the strongest
mature theory and validated methods. Deep-research benchmarks evaluate final reports and citations.
Scalable-oversight studies measure judging stronger systems. Assurance-case work provides governance
structure. Legal benchmarks show that expert-built reference denominators make completeness-like
evaluation more tractable while remaining vulnerable to reference omissions. Together they
cover most of WHU's components, but not the complete open-world composition.

## 3. Deployed high-stakes systems

OpenEvidence and CoCounsel matter because they demonstrate the dominant practical strategy:

1. restrict or privilege authoritative corpora;
2. improve retrieval over those corpora;
3. ground outputs in retrievable sources;
4. expose citations for professional verification;
5. retain humans with domain accountability.

That is a defensible approach to risk. It also does not solve WHU's stated user case, because the user
in that case cannot independently audit the full work. The Stanford legal work is particularly
instructive: completeness-like evaluation becomes more tractable when researchers invest in a
multi-month expert attempt to enumerate controlling statutory material, but later audit found
significant omissions by the reference authors themselves. Reference construction is therefore an
expensive assurance layer that also needs its own validation.

## 4. Established terminology

No single reviewed term exactly denotes WHU's whole construct. Better practice is to use established
terms for each component:

- **grounding / faithfulness / citation accuracy** for evidence fidelity;
- **high-recall retrieval / total recall** for near-exhaustive acquisition in a collection;
- **recall estimation / statistical stopping / residual relevant documents** for stopping assurance;
- **context sufficiency** for whether retrieved context answers a known question;
- **selective prediction / abstention / risk–coverage** for escalation decisions;
- **scalable oversight** for supervision across a capability gap;
- **assurance case** for a structured system-level claim supported by evidence and defeaters.

“Evidence adequacy” remains useful if explicitly defined as decision-relative sufficiency, not total
relevance recall. “Acquisition assurance” is acceptable as a WHU compositional shorthand, provided it
is not presented as new. “Capability–assurance gap” should be prose, not a coined scientific result.
“Assurance horizon” should be avoided because it lacks a validated metric and is liable to be confused
with METR's task-completion time horizon.

## 5. Where WHU fits

WHU's empirical work is best positioned as a small, synthetic bridge between otherwise separated
literatures:

- supplied-evidence reasoning tasks correspond to grounding/conditional reasoning;
- its acquisition task corresponds to high-recall retrieval but uses claim contribution rather than
  topical relevance;
- V3 calibrates observable stopping states against hidden residual consequential omissions;
- convergence V2 tests an independent-acquisition signal rather than answer agreement alone;
- selective-escalation analysis exposes a risk–coverage/review-cost question.

That combination is useful. Its evidentiary weight remains small: deterministic synthetic universes,
few semantic runs, different tasks/scales across layers, failed/invalid predecessor studies, one
consumed holdout for V3, calibration-only convergence, no naturalistic open-world reference, and no
measured expert-review cost/accuracy curve. WHU has not established that its exact construct is the
field's missing master variable or that current systems fail naturally at the rates observed in its
fixtures.

## 6. Strongest objections and adjudication

### “This is just recall.”

Partly correct. The unknown-denominator and stopping problem is old and directly recognized. WHU adds
a decision-relative label—whether an omission changes the warranted claim—and attempts to connect it
to runtime assurance. That is a narrower empirical framing, not a new foundational problem.

### “Bounded stopping methods already solve it.”

Correct within their scope. Random sampling and statistical stopping can support confidence about
recall in a defined collection. They do not automatically certify collection construction, evidence
families, consequentiality, or the open web. WHU should describe a scope-transfer/composition gap, not
an absence of any solution.

### “Agentic RAG and multi-agent research already address coverage.”

Correct as an engineering statement. They broaden and iterate retrieval, detect local insufficiency,
and improve final performance. The remaining question is whether those mechanisms produce a validated
case-level residual-risk statement. Public evidence reviewed here generally evaluates accuracy,
citations, or final quality instead.

### “Literal completeness is the wrong goal.”

Correct. WHU should never demand all relevant evidence. Its defensible target is a declared-scope,
decision-relative bound on the probability or severity of a missed claim-changing item. Even that may
be unattainable generally; narrower source restrictions and human review may be the rational policy.

## 7. Publication implications

A Substack update can responsibly say:

> Research agents are getting better at finding, citing, and reasoning over evidence. Mature adjacent
> fields also know how to estimate recall and stop in bounded collections. What remains weakly
> established is the composition we needed: a validated, affordable way for a non-auditing user to know,
> case by case, that an open-ended research process has not missed evidence that would materially change
> its conclusion.

It should also say that WHU's own experiments are small, synthetic, and non-general; that serious
systems use source restriction, iterative retrieval, parallel agents, citations, and expert oversight;
and that bounded high-recall settings have genuine statistical assurance methods.

Avoid:

- “Nobody has recognized/solved evidence completeness.”
- “RAG or citations do not help.”
- “Deep research systems cannot know when they have enough evidence.”
- “Independent agents do not work.”
- “WHU discovered the capability–assurance gap.”
- “Current frontier models cannot be trusted for research.”
- “OpenEvidence/CoCounsel provide no assurance” (their public controls support narrower assurances).
- “The field has no completeness metrics” (recall and statistical stopping are established).
- “Assurance horizon” or any analogy suggesting a validated time-like measure.

## 8. Review limits

This was a bounded state-of-field review, not a formal systematic review. Searches covered named
organizations and the adjacent literatures in the owner directive, prioritized primary sources, and
followed obvious citation trails. Proprietary product internals, unpublished evaluations, paywalled
details, non-English work, and papers not discoverable under the searched terminology may change the
picture. Accordingly, all absence claims are framed as “no public validated evidence identified,” not
“nobody has done this.”

The claim-by-claim source boundaries are in
[`WHU_STATE_OF_FIELD_EVIDENCE_ADEQUACY_ADJACENT_WORK_MATRIX.md`](WHU_STATE_OF_FIELD_EVIDENCE_ADEQUACY_ADJACENT_WORK_MATRIX.md).
