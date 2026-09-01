# Fresh Register Hard Re-Audit — 2026-09-01

Protocol: `FINDING_RULES.md` v2.1  
Current status: **5/5 PASS — target reached after 041 registration**.

```yaml
PASS_REGISTER:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction
HARD_AUDIT_NOT_REGISTERED:
  - 036_metaphor_processing_route_selection
ARCHIVED:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
CURRENT_FRESH_PASS_REGISTER: 5
TARGET: 5
REMAINING: 0
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

The 5/5 register does not change this verdict and provides no reason to force-repair 036.

## 038 — hard re-audit passed

Frozen question:

> Before reference is uniquely resolved, does the model keep multiple candidate referents, an underspecified state, or prematurely commit?

Strongest-neighbor attacks did not find direct ownership of this exact still-unresolved representational-format question. Existing H1-vs-H2 identifiability kill prevents retreat to generic ambiguity representation.

## 040 — PASS after deep novelty + identifiability audit

Frozen question:

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual or merely two different objects of the same kind?**

External scientific object:

```text
numerical identity
!=
qualitative/type sameness
```

Strongest precursor: Davis & Altmann 2021 LSTM/RNN same-token vs different-token-same-type event sensitivity. Therefore 040 cannot claim `neural models distinguish the onion from another onion` as new.

Required N2 delta:

> an **abstract numerical-identity state** in modern LLMs that generalizes across surface/domain windows and causally controls token-specific history inheritance separately from type/category knowledge.

Frozen causal-use contract:

```text
identity intervention
→ changes token-specific HistoryTransferLogit
→ preserves TypeKnowledgeLogit shared by same-type objects
```

Hard kills include event-specific RNN collapse, lexical-cue collapse, generic coreference/binding, no causal specificity, and any new direct collision.

## 041 — fifth PASS after deep N0/N1/N2 + confound audit

Frozen natural question:

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

Frozen scientific object:

> **context-conditioned modifier set restriction / contrastive role** — whether a modifier actually reduces the currently live referent set.

### External scientific substrate

Leffel et al. 2014 provides a clean human semantics/neuroscience object. The same answer phrase can be interpreted with a modifier playing a restricting or non-restricting role solely because the preceding question changes the live set of referents. Their stimulus construction started from 53 manually written sets, naturalness-normed by 105 respondents, retaining 46 sets.

This supports the object but does not itself establish an LLM result.

### Strongest predecessors deliberately conceded

1. **Incremental reference resolution** already models words as progressively reducing a candidate set. So `adjectives eliminate distractors` is not new.
2. **Monroe et al. TACL 2017** and related neural pragmatic-reference work already owns context-sensitive reference and distractor effects.
3. **Fang et al. CogSci 2022** owns neural modifier overmodification/redundancy behavior.
4. **COLING 2020 relative-clause BERT work** includes restrictive/non-restrictive metadata but largely via grammatical form/punctuation; it does not identify a same-lexical context-conditioned modifier-role state.
5. **2025–2026 LLM/VLM reference-generation work** owns pragmatic success/failure, excessive information and reference-production factors, but not the exact causal latent object.

Thus 041 is killed if it becomes `reference resolution`, `informative vs redundant adjective`, `distractor sensitivity`, or `relative-clause punctuation`.

### Exact N2 delta

> **Does a modern pretrained autoregressive LLM construct an abstract, reusable, context-conditioned set-restriction state for a modifier, and causally use that state to decide which modifier should narrow reference while preserving the modifier's ordinary property meaning?**

### Same-world role-swap identifiability design

Canonical finite world:

```text
A = large red circle      # target
B = large blue circle
C = small red circle

target phrase = "the large red circle"
```

All object facts and the target phrase remain fixed.

```text
live candidates {A,B}:
  red   = restricting
  large = non-restricting

live candidates {A,C}:
  large = restricting
  red   = non-restricting
```

This removes the easiest `different scene facts` explanation: the world, target, lexical modifiers, target truths, modifier positions, total entity facts and live-set cardinality are fixed. Only which alternatives are currently live changes.

Gold is deterministic:

```text
Restricts(m) =
  |Compatible(D_without_m, C)|
  >
  |Compatible(D, C)|
```

### Frozen first causal-use contract

```text
SetRestrictionRole intervention
→ changes modifier-specific referent narrowing / ReferentMargin
while
preserving PropertyTruthLogit
```

The primary statistic is a Role × Intervention interaction on held-out lexical/domain families, not best-layer performance.

Mandatory hard controls:

- same-world role swap;
- held-out adjective/property and noun/domain families;
- role-matched / fact-mismatched transfer;
- arbitrary candidate labels and balanced positions;
- modifier-order reversal;
- paraphrased live-candidate introductions;
- raw property-truth and candidate-identity control directions;
- shuffled labels/random subspaces;
- property-truth preservation.

### Hard kills

041 dies if:

- a direct neural/LLM same-lexical contextual set-restriction causal paper is found;
- only generic reference competence survives;
- only `informative modifier > redundant modifier` survives;
- the latent direction is scene facts / candidate identity / salience;
- intervention changes ordinary property truth as much as referent narrowing;
- cross-lexical/domain/surface abstraction fails;
- the contribution reduces to a best layer/head.

Verdict:

```yaml
041:
  route: C
  paper_scale: PASS
  natural_object: PASS
  N0_object_ownership: PASS
  N1_causal_occupancy: PASS
  N2_delta_width: PASS_WITH_HARD_KILLS
  human_scientific_substrate: PASS
  deterministic_gold: PASS
  confound_identifiability: PASS_WITH_HARD_KILL
  frozen_S0_contract: PASS
  frozen_causal_use_contract: PASS
  PASS_REGISTER: true
  GPU_AUTHORIZED: true
```

Full card: `active/041_contextual_set_restriction/README.md`.

## 034 / 035

Remain frozen PASS. No new fatal collision was discovered during the final search.

## Final-search terminal records

Two serious leads were killed before 041 registration:

- **mass/count grammar vs conceptual individuation** — old neural syntax-semantics work plus contextualized nominal-coercion work already owns the attractive object; modern AR + MI alone is N2-thin.
- **means vs side-effect harm** — directly owned as an LLM moral factor by MoCa/OffTheRails-style work; the stronger intentionality-mediation theory variant does not yet have a frozen analyzable-open behavior anchor and is not GPU-authorized.

Detailed records live in `rejected_candidates/` and must remain in semantic dedupe memory.

## Paper-scale expansion discipline

Use `PAPER_EXPANSION_REFERENCE_2026-09-01.md`.

Reference-backed ladder:

```text
phenomenon / object
→ generalization / abstraction
→ causal use / specificity
→ mechanism-derived falsifiable prediction
→ targeted behavioral confirmation
→ optional mitigation / architecture generalization
```

Do not pre-invent later stages.

For 041, only the first three stages are currently earned enough to freeze:

```text
same-world modifier-role behavioral double dissociation
→ cross-lexical/domain/surface abstraction
→ causal referent-narrowing specificity while preserving property truth
```

## Current discipline

The honest state is now **5/5**. The fresh-search target is complete. Do not continue count-filling search by default and do not use the target count to protect any topic from future fatal evidence.
