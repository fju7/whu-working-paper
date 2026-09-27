# OpenEvidence as an acquisition-assurance case study

**Status:** public-source research snapshot, 2026-09-25  
**Scope:** the WHU evidence-acquisition and false-assurance problem, not company diligence or product endorsement  
**Method:** current public web research; no contact with OpenEvidence or any external party. Primary/official sources are preferred for product claims. Independent studies are used for performance claims. Company claims are identified as such.

## Executive finding

OpenEvidence has a credible architecture for reducing two important causes of false assurance: fabricated references and friction in reaching reputable, current clinical literature. It uses retrieval-augmented generation (RAG), returns source-linked citations, and has licensed or society-provided access to full text, guidelines, policies, and treatment algorithms from major publishers and professional bodies. Those are material controls over **evidence fidelity and provenance**.[1–4]

Public evidence does **not** establish an assurance mechanism for the harder WHU question: whether the acquired evidence is adequate for the claim, what consequential evidence was missed, or how much residual risk remains after retrieval. No public technical specification located for this review describes a validated completeness estimate, calibrated case-level confidence, explicit missing-evidence bound, independent falsifier search, or risk-triggered escalation policy. That is an absence-of-public-evidence finding, not proof that no internal mechanism exists.

Independent evaluations make the distinction concrete. OpenEvidence usually produces real, verifiable references, but reference validity is not clinical correctness or completeness. In a 2026 real-clinical-query benchmark, clinicians found incomplete content and safety-critical omissions particularly common in OpenEvidence and Google AI Overview outputs. A complex-subspecialty pilot reported only 34% accuracy for the fast mode and 41% for Deep Consult. A triage benchmark found fewer missed emergencies than a historical ChatGPT Health comparison, but also 68% over-triage on nonurgent home-care presentations.[5–8]

## 1. How does it acquire and select evidence?

The best supported public description is a proprietary RAG system: a clinician's natural-language question triggers retrieval from medical literature, and an LLM synthesizes an answer with references. A 2025 peer-reviewed evaluation states that the system used PubMed articles and FDA drug labels; public product and partner materials now show a broader licensed corpus.[1,5]

The current disclosed source layer includes full-text or rich content from *The New England Journal of Medicine*, JAMA and the JAMA Network, Nature Portfolio, and Cochrane systematic reviews; NCCN treatment algorithms; and collaborations with medical societies. ACEP separately confirms that its clinical policies, point-of-care tools, and educational materials are integrated into the platform. The AMA confirms a JAMA Network content agreement covering full text and multimedia.[1–4]

OpenEvidence also offers a longer-running Deep Consult workflow. The company's release says that its agents analyze and cross-reference hundreds of peer-reviewed studies in parallel; in a 2026 Stanford Medicine interview, co-founder Travis Zack described separating deep patient-record analysis from a research mode intended to identify relevant literature comprehensively. These are company descriptions, not independently audited retrieval specifications.[9,10]

What remains opaque publicly is decisive for assurance: corpus boundaries, inclusion/exclusion rules, source hierarchy, query expansion, ranking and reranking, handling of retractions and conflicting studies, refresh latency by source, stopping rules, and recall measurement. A 2026 *Nature Medicine* comparison likewise notes that the proprietary architecture is inaccessible.[6]

## 2. What does it expose to users that supports trust?

OpenEvidence exposes generated answers with citations and links to the underlying papers. Independent evaluators could follow those links and verify them, and the most recent large reference audit found no confirmed fabricated references among 4,979 citations, although three abstracts had attribution errors.[5,11]

The interface therefore provides useful provenance and makes spot-checking possible. Publisher partnerships additionally permit use of figures, tables, multimedia, and full text that ordinary abstract-only search cannot expose.[1–3]

However, the 4,979-citation audit observed that source types were not distinguished in the generated text: guidelines, regulatory documents, reviews, and primary studies appeared as identical numbered references. The same study expressly did **not** test whether cited references supported the generated clinical claims.[11] Public materials reviewed here did not document claim-level quotations, a structured evidence hierarchy visible to users, calibrated uncertainty, a coverage warning, or systematic presentation of conflicting evidence.

## 3. Fidelity versus adequacy/completeness

OpenEvidence clearly addresses **fidelity**: citations are usually real, source-linked, and drawn from curated/licensed medical content. The public case for **adequacy** is much weaker. A real reference can be irrelevant, can support only part of a claim, can be lower in an evidence hierarchy than an omitted source, or can coexist with missed contrary evidence.

That gap is empirically visible. In the 2025 study of 50 real-world clinical questions, only 24% of all OpenEvidence answers were both relevant and evidence-based and 30% were actionable; among questions judged to have existing literature, 37% were relevant and evidence-based and 48.2% actionable. Its citation hallucination/irrelevance rate was only 2.3%, showing that low citation failure did not imply broad answer adequacy.[5]

No public mechanism located in this review tells a clinician: "the relevant evidence universe is likely incomplete," quantifies acquisition uncertainty, lists likely missing source classes, or states a validated residual probability of a claim-changing omission. Deep Consult's larger search budget may improve breadth, but more citations are not itself a completeness certificate: the pilot found roughly 35 citations per Deep Consult answer versus five in fast mode, while accuracy was 41% versus 34%.[8]

## 4. Challenge, falsifier search, review, escalation, and calibration

Deep Consult is publicly described as agentic and as cross-referencing studies in parallel.[9] That is evidence of broader search and synthesis, not evidence of an **independent challenge channel**. Public sources reviewed here do not establish that a separate model searches specifically for claim-changing contrary evidence, that disagreements are adjudicated by independent experts, or that runtime signals trigger clinician escalation according to a calibrated policy.

Human oversight is instead externalized to the clinician. The platform is physician-facing, independent papers call it clinical decision support, and comparative studies continue to state that physician oversight is necessary.[7,12] Publicly reported refusals can function as a coarse abstention behavior: in the triage study, 6.8% of responses declined to assign a level, all in symptom-only home/routine prompts. The study treated refusal as a distinct outcome whose implications require separate assessment; it did not validate refusal as calibrated confidence.[7]

No prospective public validation located here maps an OpenEvidence confidence signal to observed error, or establishes selective-prediction performance (coverage versus error) for routine clinical use.

## 5. Empirical validation: what has and has not been measured

The following studies measure different constructs and should not be pooled into one "accuracy" number.

| Study | Design and population | Comparator | Measured outcome | Main result | What it does not establish |
|---|---|---|---|---|---|
| Low et al., 2025[5] | 50 clinical questions drawn from or inspired by physician evidence requests; nine physician reviewers | Three general LLMs and an on-demand real-world-data agent | Relevance, evidence quality, actionability; citation review | OE: 24% relevant-and-evidence-based overall, 30% actionable; citation hallucinated/irrelevant in 2.3% | Patient outcomes; representative prevalence; completeness of all relevant evidence |
| Pennington-FitzGerald et al., 2026[12] | 100 validated otolaryngology vignettes | ChatGPT-4, Perplexity, Pathway | Diagnostic accuracy and citation integrity | All models 82–91% accuracy; differences nonsignificant; OE had consistent/verifiable references and high journal CiteScore | Live clinical outcomes; calibrated reliance |
| Reference-quality audit, 2026[11] | 150 standardized prompts, five specialties, 4,979 citations | No clinical-output comparator | Reference existence, attribution, recency and source profile | No confirmed fabricated references; three abstract attribution errors; median unique-reference year 2022 | Whether references entailed claims; clinical correctness; completeness |
| *Nature Medicine*, 2026[6] | 500 MedQA, 500 HealthBench, and 100 de-identified real clinician queries; 12 blinded clinicians for real queries | Three frontier LLMs, UpToDate Expert AI, Google AI Overview | Knowledge; clinician alignment; correctness, completeness, safety, clarity | OE HealthBench 62.6; real-query mean 3.24/4; frontier models higher; incomplete/safety-critical omissions noted | Citation quality, patient outcomes, longitudinal deployment safety |
| Complex subspecialty pilot, 2025 preprint[8] | 100 MedXpertQA subspecialty scenarios; two evaluators | OE fast mode versus Deep Consult and historical model results | Answer accuracy, repeatability, citations | 34% fast-mode and 41% Deep Consult accuracy; evaluator concordance 77% and 72% | Peer-reviewed confirmation; clinical workflow and outcomes |
| Triage benchmark, 2026[7] | 960 prompts from 60 clinician-authored vignettes across 21 domains | Historical ChatGPT Health benchmark | Correct, under-, over-triage, refusal | 71.3% clear-case accuracy; 12.5% emergency under-triage; 68% over-triage for nonurgent home cases | Prospective triage outcomes or clinician-AI team performance |
| Gynecologic oncology benchmark, 2026[13] | 50 de-identified cases, three gynecologic oncologist raters | Baseline GPT-5 and NCCN-anchored GPT-5 RAG | Guideline concordance plus hallucination penalty | NCCN-RAG 0.83, OE 0.70, baseline 0.65; OE and baseline not significantly different | Current post-NCCN OE, clinical safety, patient outcomes |

A 2026 systematic review found 11 eligible early studies and concluded that results were generally strongest in guideline-based settings but variable in complex scenarios; it emphasized small samples, heterogeneity, product drift, and the need for prospective real-world studies.[14] None of the studies above is a randomized trial of patient outcomes or a prospective test of whether clinician use improves care.

## 6. Failure modes found independently

The strongest observed failure modes are not fabricated bibliography:

- **Incomplete or safety-critical content despite grounded retrieval.** The real-clinician-query study found these problems particularly common for OpenEvidence and Google AI Overview.[6]
- **Clinical error in difficult reasoning cases.** The subspecialty pilot's 34–41% accuracy occurred despite responses containing multiple references, and Deep Consult's much larger reference count did not make it reliably correct.[8]
- **Over-cautious triage.** OpenEvidence missed fewer emergencies than the historical consumer comparator but over-triaged 68% of nonurgent home cases; objective clinical data improved both under- and over-triage.[7]
- **Guideline access matters.** In the gynecologic oncology benchmark, an NCCN-anchored RAG configuration outperformed the then literature-anchored OpenEvidence implementation. The authors explicitly cautioned that the result predated OpenEvidence's NCCN integration.[13]
- **Source-profile opacity and concentration.** The citation audit found that source types were not labeled and that journal concentration varied substantially by specialty; for cardiology, one journal supplied 21.1% of unique references.[11]
- **Attribution can fail even when a reference exists.** The 4,979-citation audit found three attribution errors.[11]

These failures show why "the citation is real" and "the answer is safe to rely on" are separate propositions.

## 7. Expected clinician use and oversight

OpenEvidence is positioned as a physician-facing medical search and decision-support platform, not a validated autonomous care system. Its main site says access is free to verified U.S. health professionals; ACEP describes point-of-care decision support; the triage study calls it physician-facing; and the cervical-spine comparison concludes that physician oversight remains essential.[2,7,15]

The public validation record assumes a clinician remains responsible for interpreting applicability, resolving conflicts, supplying patient context, and deciding whether to act. Yet the evidence base mostly evaluates model outputs in isolation, not clinician-plus-tool teams. It therefore cannot quantify automation bias, verification behavior under time pressure, or whether prominent citations cause unjustified reliance.

## 8. Is it solving the same problem as WHU?

**Mostly a narrower problem, with partial overlap.** OpenEvidence reduces the cost of finding and synthesizing high-quality sources and sharply reduces fabricated citations. Deep Consult attempts broader acquisition. Those are real components of WHU's evidence pipeline.[1,5,9,11]

WHU's assurance question is stricter: can observable runtime state warrant a case-level conclusion that no hidden, claim-changing evidence was missed? Public evidence does not show that OpenEvidence measures or validates that property. Its citations make evidence inspectable; they do not bound the unseen remainder. Its curated corpus improves priors; it does not establish recall for a particular question. Its agentic breadth is a search strategy; it is not yet a demonstrated assurance rule.

## 9. Design lessons for WHU, and the remaining gap

Useful lessons:

1. **Acquire primary and full-text material under explicit source agreements.** Full text, guidelines, treatment algorithms, and society policies are stronger acquisition primitives than open-web snippets.[1–4]
2. **Make provenance cheap to inspect.** Source-linked citations reduce fabrication and let a human verify claims.[5,11]
3. **Separate fast lookup from deep acquisition.** Different time/compute budgets are appropriate for point-of-care reminders and consequential synthesis.[9,10]
4. **Treat guidelines as a distinct evidence class.** The oncology benchmark suggests direct guideline anchoring can materially affect performance.[13]
5. **Evaluate constructs separately.** Citation existence, citation entailment, answer correctness, completeness, calibration, clinician behavior, and patient outcomes need separate tests.[5–8,11–14]
6. **Measure abstention and over-caution explicitly.** Refusal, under-triage, and over-triage have different costs and should not collapse into one accuracy score.[7]
7. **Expect product drift.** Access partnerships and model behavior change faster than conventional validation cycles; time-stamped, versioned evaluation is essential.[6,13,14]

The unsolved gap is a prospective, externally valid assurance layer that estimates residual acquisition risk for the individual case, searches adversarially for disconfirming evidence, accounts for source dependence and coverage gaps, and routes uncertain cases to independent review under a validated escalation policy.

## 10. Bottom-line assessment of false-assurance reduction

**Credible for reduction, unproven for assurance.** The architecture credibly reduces false assurance caused by invented sources and improves access to reputable evidence. Multiple independent studies support low reference-fabrication rates.[5,11,12]

It cannot, on public evidence, support the stronger claim that a cited answer is adequately complete or safe to rely on without clinician verification. Independent studies document incomplete content, safety-critical omissions, limited accuracy on complex cases, and severe over-triage even where the system is grounded in real sources.[6–8] There is no public prospective evidence of a calibrated case-level assurance score, an independent falsifier-review pathway, a validated escalation threshold, improved clinician decisions in routine practice, or improved patient outcomes.

Accordingly, OpenEvidence is best treated as a strong evidence-access and provenance system that can lower some important error modes. It is not, on the public record, a solution to WHU's evidence-adequacy problem.

## Sources

1. OpenEvidence, [TakeHome / content partnerships](https://takehome.openevidence.com/) (current product claims: NEJM, JAMA, NCCN, Nature, Cochrane, societies).
2. American Medical Association, [More than 80% of physicians use AI professionally](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey) (JAMA content agreement and scope).
3. American Medical Association, [2026 informational report](https://www.ama-assn.org/system/files/a26-handbook-informational-reports.pdf) (records JAMA Network content licensing agreement with Open Evidence Inc.).
4. American College of Emergency Physicians, [ACEP and OpenEvidence expand access to emergency medicine resources](https://www.acep.org/news/acep-newsroom-articles/acep-and-openevidence-expand-access-to-emergency-medicine-resources) (ACEP policies and educational content integration).
5. Low YS et al., [Answering real-world clinical questions using large language model, retrieval-augmented generation, and agentic systems](https://doi.org/10.1177/20552076251348850), *Digital Health* (2025).
6. [General-purpose large language models outperform specialized clinical AI tools on medical benchmarks](https://www.nature.com/articles/s41591-026-04431-5), *Nature Medicine* (2026).
7. Jia E et al., [OpenEvidence errs on the safe side in a structured test of triage recommendations](https://pubmed.ncbi.nlm.nih.gov/42673790/), *International Journal of Medical Informatics* (2026).
8. Jagarapu J et al., [The accuracy and repeatability of OpenEvidence on complex medical subspecialty scenarios: a pilot study](https://www.medrxiv.org/content/10.64898/2025.11.29.25341091v1), medRxiv preprint (2025; not peer reviewed).
9. OpenEvidence release distributed by Healthcare IT Today, [OpenEvidence announces DeepConsult](https://www.healthcareittoday.com/2025/08/04/openevidence-the-fastest-growing-application-for-physicians-in-history-announces-210-million-round-at-3-5-billion-valuation/) (company description of agentic workflow).
10. Stanford Medicine, [Travis Zack on OpenEvidence and the future of medical AI](https://medicine.stanford.edu/news/stories/episodes/travis-zack-medical-ai.html) (2026 interview; company account of Deep Consult design direction).
11. [Reference quality of OpenEvidence across five medical specialties](https://pmc.ncbi.nlm.nih.gov/articles/PMC13538487/) (2026).
12. Pennington-FitzGerald W et al., [Diagnostic accuracy and citation integrity of four large language models on otolaryngology vignettes](https://pubmed.ncbi.nlm.nih.gov/42120572/), *European Archives of Oto-Rhino-Laryngology* (2026).
13. Dukes D et al., [Guideline-anchored retrieval-augmented generation outperforms baseline and literature-only configurations in gynecologic oncology decision support](https://pubmed.ncbi.nlm.nih.gov/42462288/), *Gynecologic Oncology* (2026).
14. [OpenEvidence clinical question-answering platform: systematic review of early evaluations](https://www.nature.com/articles/s41746-026-03077-4), *npj Digital Medicine* (2026).
15. Avrumova F et al., [Evolution of generative artificial intelligence in clinical practice: comparative performance of OpenEvidence 2.0 and ChatGPT-4o](https://www.sciencedirect.com/science/article/pii/S1529943026006315), *The Spine Journal* (2026).

