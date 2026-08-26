# Rejected Candidates — RAG / Evidence Attribution / Citation Provenance

**Domain:** retrieval-augmented generation where models must use, select, and visibly attribute external evidence.  
**Search date:** 2026-08-26.  
**Domain verdict:** no survivor promoted from this scan.

## Domain goal

The initially attractive dissociation was:

```text
answer content is correct / grounded
but
visible source attribution is missing, spurious, or points to the wrong source
```

This looks mechanistically decomposable into evidence encoding, claim–source binding, citation selection, and late serialization. After collision audit, however, the citation/attribution space is already unusually crowded, and several remaining mechanism questions fail the repository’s method-closure requirement.

---

# 1. Generic “why does the model cite / fail to cite?”

**Natural question:** Why does an LLM sometimes attach a citation to an answer and sometimes fail to do so even when a relevant document is present?

**Why it initially looked good:**

- citation behavior is directly observable and high-stakes;
- relevant-vs-distractor document pairs provide cheap clean/corrupt contrasts;
- citation decision can be causally manipulated without changing answer correctness.

**Kill evidence:**

`How Do LLMs Cite? A Mechanistic Interpretation of Attribution in Retrieval-Augmented Generation` (ECIR 2026) is already a direct mechanism paper. On Llama-3.1-8B-Instruct it uses activation patching to identify a distributed multi-stage “attributional ensemble” of attention heads and MLPs. Citation decisions rely heavily on shallow entity co-reference matching; targeted amplification repairs over 90% of missed citations and attenuation eliminates 69% of spurious citations on PopQA without harming answer accuracy. The components also move citation rates in the expected direction on HotpotQA.  
https://arxiv.org/abs/2606.28358  
https://doi.org/10.1007/978-3-032-21324-2_35

This already covers behavior → causal mechanism → targeted repair.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** missing citation, spurious citation, “citation token circuit”, “does the answer actually cause the citation?”, and single-document citation faithfulness are the same occupied neighborhood.

**Resurrection condition:** a qualitatively different multi-source binding phenomenon that cannot be explained by the existing citation-presence mechanism.

---

# 2. Correct content, wrong source pointer

**Natural question:** Why can a model correctly use/quote a fact from the retrieved context yet attach the wrong document/chunk ID to that claim?

**Why it initially looked good:**

- this is a much cleaner failure than generic hallucination: semantic content may be right while provenance binding is wrong;
- multi-document contexts can create exact matched swaps of source IDs;
- plausible competing explanations include wrong evidence selection, loss of source identity during copying, and late citation-ID serialization error.

**Kill evidence:**

Public RAG evaluation already directly annotates source attribution. `GaRAGe` contains 2,366 questions and over 35K grounding-passage annotations; across tested models, F1 for attribution to relevant sources reaches only 58.9%, establishing that source attribution is a real and substantial behavior problem.  
https://aclanthology.org/2025.findings-acl.875/

However, the strongest objection is **method closure**. Once the answer claim is generated, claim→passage support can be recomputed externally and the visible citation pointer deterministically/post-hoc reattached, without knowing whether the original internal failure was source-ID binding, evidence selection, or serialization. `CiteGuard` (ACL 2026) explicitly reframes citation evaluation as citation-attribution alignment and uses retrieval-aware validation to improve citation attribution accuracy by 10 points, reaching 68.1% on CiteME.  
https://aclanthology.org/2026.acl-long.282/

Thus several very different internal mechanisms naturally lead to the same practical fix: validate/remap claims against sources after generation. That violates the project’s requirement that mechanism discovery should materially alter the method design.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** “right quote, wrong chunk,” neighboring citation-ID swaps, page-number swaps, citation-index serialization, and claim/source pointer mismatch are not separate topics unless the mechanism changes what the repair must do.

**Resurrection condition:** demonstrate that post-hoc source remapping cannot recover the desired provenance because the generated claim is genuinely synthesized from multiple sources in a way requiring an internal causal account of evidence composition.

---

# 3. Generic source-position / document-order bias in RAG

**Natural question:** Why does moving the same evidence to a different position in the retrieved context change whether it is used or cited?

**Why it initially looked good:**

- exact content-preserving permutations are ideal causal pairs;
- order sensitivity is externally obvious and cheap to test;
- source selection / retrieval-head routing appears mechanistically tractable.

**Kill evidence:**

This area is already heavily occupied behaviorally, mechanistically, and methodologically:

- `Lost in the Middle` established the classic primacy/recency U-shape in multi-document QA.  
  https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long
- EACL 2026 `Beyond Semantics` gives a mechanistic account connecting temporal retrieval bias to induction-style heads/channels and shows that ablating high-induction-score heads reduces retrieval and episodic separation.  
  https://aclanthology.org/2026.eacl-long.355/
- Findings ACL 2025 identifies positional hidden-state channels and mitigates position bias by scaling a single hidden-state channel.  
  https://aclanthology.org/2025.findings-acl.316/
- Findings ACL 2026 `RetMask` explicitly uses mechanistically identified retrieval heads to improve long-context performance, including +70% on generation-with-citation.  
  https://aclanthology.org/2026.findings-acl.1380/
- ACL 2026 `Stable-RAG` directly targets retrieval-permutation-induced hallucinations even when the gold document remains fixed at rank 1.  
  https://aclanthology.org/2026.acl-long.1188/

The behavior→mechanism→repair package is no longer open.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** source-order bias, chunk-order bias, citation-order bias, retrieval-rank bias, and “gold document in the middle” are one crowded family.

**Resurrection condition:** a non-positional semantic provenance phenomenon whose decisive contrast survives all document permutations.

---

# 4. Source authorship metadata changes attribution

**Natural question:** Why can identical evidence be cited differently merely because it is labeled as human-written versus AI-written?

**Why it initially looked good:**

- strong counterfactual control: hold document content fixed and change only authorship metadata;
- Findings ACL 2025 reports that adding authorship information changes attribution quality by 3–18%, with a bias toward explicit human authorship;
- potentially surprising because some earlier work reported preference for LLM-generated content.

**Kill evidence:**

The exact behavior is already the core of `Evaluation of Attribution Bias in Generator-Aware Retrieval-Augmented Large Language Models` (Findings ACL 2025).  
https://aclanthology.org/2025.findings-acl.1087/

The nearest causal story is also rapidly closing:

- ACL 2025 `LLMs Trust Humans More, That’s a Problem!` introduces Authority Bias in RAG and proposes a conflict-detection/credibility-based mitigation framework.  
  https://aclanthology.org/2025.acl-long.1400/
- `A Mechanistic View of Authority Hierarchy in LLM Sycophancy` (2026) directly studies graded source authority and reports a late-layer mechanism in which correct-answer representations are actively erased in proportion to perceived authority.  
  https://arxiv.org/abs/2607.00415

A mechanistic paper on “human author metadata makes the source trusted/cited” would likely collapse into an output-specific instance of authority bias rather than establish a new mother question.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** human-vs-AI labels, expert-vs-novice labels, prestigious-vs-obscure outlet labels, author-title labels, and publisher-authority labels are the same family unless they produce a qualitatively different causal dissociation.

**Resurrection condition:** evidence that source metadata changes *visible citation choice while leaving actual evidence use and answer representation invariant*, producing a citation-specific dissociation not explained by authority-induced answer overwriting.

---

# 5. Generic conflicting-source / source-credibility arbitration

**Natural question:** When retrieved sources disagree, why does an LLM trust one source over another, and does it reason about credibility correctly?

**Why it initially looked good:**

- real web evidence naturally conflicts;
- credibility, majority, recency, and textual specificity yield competing cues;
- clear method opening in credibility-aware RAG.

**Kill evidence:**

The behavior/method space is already dense:

- ACL 2026 `ConfRAG` introduces 1,814 real-world questions with an average 9.58 web paragraphs and explicit contradictions in 57.2% of questions.  
  https://aclanthology.org/2026.acl-long.11/
- `CONFACT` (2025) systematically studies conflicting evidence from sources of differing credibility and shows that explicitly incorporating source credibility improves conflict resolution.  
  https://arxiv.org/abs/2505.17762
- ACL 2025 Authority Bias already studies user-vs-database conflict and proposes a mitigation based on conflict detection and credibility assessment.  
  https://aclanthology.org/2025.acl-long.1400/
- Mechanistic authority-hierarchy work in 2026 further occupies the most obvious internal explanation, authority-induced overwriting of correct representations.  
  https://arxiv.org/abs/2607.00415

A generic “credibility representation / source arbitration circuit” project would be difficult to distinguish from these works without a much sharper external phenomenon.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** majority-vs-minority source, trusted-vs-untrusted source, expert-vs-user evidence, web-source conflict, and conflicting citations are not distinct mother questions by themselves.

**Resurrection condition:** identify a counterintuitive source-combination phenomenon whose outcome cannot be predicted by credibility/authority/position/majority alone and whose mechanism implies a different repair.

---

# Domain lesson

RAG attribution is attractive because it provides explicit evidence objects and easy clean/corrupt pairs, but by 2026 the obvious path is unusually saturated:

```text
citation behavior
→ attribution mechanism
→ citation repair
```

and

```text
source conflict / metadata
→ trust or authority bias
→ credibility-aware repair
```

are both already occupied.

The narrower “correct semantic content but incorrect source pointer” dissociation remains scientifically interesting, but currently fails the repository’s P3 test because an external provenance validator can often repair the visible citation irrespective of the internal failure source. **No candidate from this domain is promoted to the final pool in this scan.**