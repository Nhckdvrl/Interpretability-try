# Fresh Register Hard Re-Audit — 2026-09-01

Protocol: `FINDING_RULES.md` v2.1  
Current status: **4/5 PASS after 040 registration**.

```yaml
PASS_REGISTER:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
HARD_AUDIT_NOT_REGISTERED:
  - 036_metaphor_processing_route_selection
ARCHIVED:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
CURRENT_FRESH_PASS_REGISTER: 4
TARGET: 5
REMAINING: 1
```

## 039 — canonical N2 kill

Taxonomic similarity vs thematic relatedness was already studied directly enough in language-model representations/behavior that the remaining delta collapsed to stronger MI. Keep archived.

Lesson: **object ownership, not title ownership**.

## 036 — question survives, metric still does not

Question:

> What selects comparison versus categorization in metaphor comprehension: conventionality, aptness, or neither?

The exact selector question remains plausible, but the former `X is Y` vs `X is like Y` causal difference does not uniquely identify comparison vs categorization. Reauthorization still requires a clean two-signature route-calibration contract, with at least one signature not defined by grammatical metaphor/simile form.

```yaml
036:
  PASS_REGISTER: false
  GPU_AUTHORIZED: false
  verdict: CONTINUE-PAPER-SCALE / HARD AUDIT
```

## 038 — hard re-audit passed

Frozen question:

> Before reference is uniquely resolved, does the model keep multiple candidate referents, an underspecified state, or prematurely commit?

Strongest-neighbor attacks did not find direct ownership of this exact still-unresolved representational-format question. Existing H1-vs-H2 identifiability kill prevents retreat to generic ambiguity representation.

## 040 — PASS after deep novelty + identifiability audit

Frozen question:

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual or merely two different objects of the same kind?**

### External scientific object

Human cognitive/philosophical work distinguishes:

- **numerical identity** — one and the same individual;
- **qualitative/type sameness** — same properties or same kind.

Dranseika et al. (Cognition 2023) explicitly studies two senses of sameness, including lexical separation in Lithuanian.

Solomon et al. (J Cogn Neurosci 2015) supplies a natural token × state-change design with the critical cross-cases:

```text
same token despite substantial state change
vs
different token of the same type despite high similarity
```

### Strongest precursor

Davis & Altmann (Cognition 2021) is a serious LSTM/RNN predecessor. It shows sensitivity to `the onion` vs `another onion` in event representations. Therefore 040 cannot claim `neural models distinguish same-token vs another-token` as novel.

The required N2 delta is broader:

> an **abstract numerical-identity state** in modern LLMs that generalizes across surface/domain windows and causally controls token-specific history inheritance separately from type/category knowledge.

### Modern entity-tracking neighbors

ICLR 2024, EMNLP 2024, ACL 2026 binding work and ICML 2026 state-change tracking study how already individuated/indexed entities bind or propagate attributes/states.

ICML 2026 is the closest warning: its original data largely make object label sufficient for individuation, and a same-label duplicate stress test exposes failure of a global REMOVE mechanism. This is highly relevant evidence, but it does not factorize numerical identity vs qualitative sameness as the causal scientific object.

### Frozen causal-use contract

Primary test:

```text
identity intervention
→ changes token-specific HistoryTransferLogit
→ preserves TypeKnowledgeLogit shared by same-type objects
```

Mandatory controls include lexical cue, noun repetition, recency, semantic similarity/type, shuffled labels, random directions, and generic coreference/binding.

### Hard kills

040 dies if:

- only the original `the` vs `another` event effect survives;
- cross-surface abstraction fails;
- generic coreference/binding fully explains the result;
- identity intervention changes shared type knowledge as much as token-specific history;
- a new direct modern LLM collision is found.

Verdict: **PASS-REGISTER / GPU AUTHORIZED**.

Full card: `active/040_numerical_identity_vs_qualitative_sameness/README.md`.

## 034 / 035

Remain frozen PASS. No new fatal collision found in lightweight scans.

## Paper-scale expansion discipline

For 040 and future topics, use `PAPER_EXPANSION_REFERENCE_2026-09-01.md`.

Reference-backed evidence ladder:

```text
phenomenon / object
→ generalization / abstraction
→ causal use / specificity
→ mechanism-derived falsifiable prediction
→ targeted behavioral confirmation
→ optional mitigation / architecture generalization
```

Do not pre-invent later stages. Strong papers such as ACL 2025 `Llama See, Llama Do`, NAACL 2025 `Racing Thoughts`, ACL 2026 Tool Irrelevance, EMNLP 2025 filler-gap Outstanding, and ICML 2026 entity tracking all expand only after earlier evidence earns the next step.

## Current discipline

The honest state is **4/5**. One genuine PASS remains. Do not count-fill, and do not reopen canonical failures by renaming them.
