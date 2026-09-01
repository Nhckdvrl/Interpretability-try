# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、自然、清楚、paper-scale 且可机制化的 LLM scientific questions**。

## Authoritative state — 2026-09-01

```yaml
BASE_PASS_REGISTER: 5
STRICT_EXTENSION_PASS: 3
TOTAL_REGISTERED: 8

base_registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction

strict_extension_registered:
  - 042_uniqueness_vs_familiarity_definite_licensing
  - 044_stage_vs_individual_predication
  - 045_referential_vs_attributive_description_use

hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
  - 043_kind_vs_member_generic_predication

archived:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
```

**The original 5/5 target remains complete. The later 3/3 extension was accepted under a strictly higher bar. Prior PASS never protects a topic from downgrade: 043 was removed from the strict register after the second audit and replaced by 045.**

## Mandatory authority / memory read order

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **v2.1 base authoritative discovery protocol**.
2. [`phenomenon_miner/STRICT_EXTENSION_GATE_2026-09-01.md`](phenomenon_miner/STRICT_EXTENSION_GATE_2026-09-01.md) — mandatory **additive** higher bar for post-base topics 042+; it does not weaken or replace v2.1.
3. [`phenomenon_miner/STRICT_EXTENSION_REGISTER_2026-09-01.md`](phenomenon_miner/STRICT_EXTENSION_REGISTER_2026-09-01.md) — authoritative strict-extension count/status.
4. [`rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`](rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md) — base semantic dedupe memory.
5. [`rejected_candidates/STRICT_EXTENSION_FAILURE_INDEX_ADDENDUM_2026-09-01.md`](rejected_candidates/STRICT_EXTENSION_FAILURE_INDEX_ADDENDUM_2026-09-01.md) — **mandatory 042+ semantic-dedupe addendum**; read together with the canonical index.
6. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — current handoff.
7. [`phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`](phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md) — audit state.
8. [`phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`](phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md) — evidence-based paper growth.

For 042+ the strict overlay requires a new orthogonal scientific object plus hard identifiability, causal specificity with a preserved neighboring capability, held-out abstraction, and at least two of:

- **Lock A:** same-surface / orthogonal role-swap factorization;
- **Lock B:** cross-setting abstraction;
- **Lock C:** two independent theory-grounded consequences.

`owned behavior + newer open model + probe/SAE/patching` is not novelty.

---

# Registered projects

| project | status | frozen question/object |
|---|---|---|
| [`034`](active/034_prospective_memory_retrieval_architecture/) | **PASS / GPU / FROZEN** | Prospective memory: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035`](active/035_shared_dynamic_context_update/) | **PASS / GPU / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update? |
| [`038`](active/038_unresolved_reference_representation_architecture/) | **PASS / GPU / HARD RE-AUDIT PASSED / FROZEN** | Before reference resolves, multiple candidates, underspecification, or premature commitment? |
| [`040`](active/040_numerical_identity_vs_qualitative_sameness/) | **PASS / GPU / FROZEN** | Same individual vs merely same kind/qualities. |
| [`041`](active/041_contextual_set_restriction/) | **STRICT RE-AUDIT PASS / GPU / FROZEN** | Which modifier currently narrows the live referent set, separately from property truth? |
| [`042`](active/042_uniqueness_vs_familiarity_definite_licensing/) | **STRICT-PASS / GPU / HARD RE-AUDIT PASSED** | Is `the X` licensed by uniqueness or strong discourse familiarity? |
| [`044`](active/044_stage_vs_individual_predication/) | **STRICT-PASS / GPU / HARD RE-AUDIT PASSED** | Does a property characterize the individual or only a particular stage? |
| [`045`](active/045_referential_vs_attributive_description_use/) | **STRICT-PASS / GPU / HARD RE-AUDIT PASSED** | Does a description follow an independently intended speaker-target or whoever satisfies the description? |

---

## 041 — contextual modifier set restriction

041 survived a second strict audit only for:

> **same-lexical context-conditioned modifier set-restriction role**, transferable across property/domain/surface families and causally affecting referent narrowing while preserving property truth.

Recent descriptor-necessity work owns weaker claims.

Causal specificity:

```text
SetRestrictionRole intervention
→ changes referent narrowing / ReferentMargin
while preserving PropertyTruthLogit
```

## 042 — uniqueness vs strong familiarity

Important correction: `+Familiarity` is **strong discourse familiarity via explicit interlocutor mention/re-mention**, not simple antecedent presence.

Critical cross:

```text
unique + not strongly familiar
vs
non-unique + strongly familiar
```

Causal source edits must preserve:

```text
CandidateStructureLogit
DialogueMentionFactLogit
EntityPresenceLogit
```

Raw recency/mention-count/salience collapse is fatal.

## 043 — downgraded after second audit

**STRICT HARD AUDIT / GPU PAUSED / NOT REGISTERED.**

The question remains scientifically promising, but:

- the surrounding generic LLM family is heavily occupied;
- the broad formal partition is not fully theory-neutral;
- no sufficiently large consensus-clear model-independent causal inventory is frozen;
- predicate lexical semantics still defeats true Lock A.

Frozen diagnostics if resurrected:

```text
MemberInheritance
IndefiniteSingularCompatibility
```

Resurrection requires an auditable consensus-clear inventory, a genuine same-lexical factorization, or explicit Route-B theory adjudication. **No GPU now.**

## 044 — stage-level vs individual-level

Not temporary vs permanent. Same-adjective shifts and anti-duration counterexamples are mandatory.

Two exact diagnostics are frozen before GPU:

```text
SituationBoundLogit
DepictiveCompatibilityLogit
```

The same causal state must move both while preserving `PropertyTruthLogit`; systematic diagnostic dissociation kills the unified object.

## 045 — referential vs attributive use

Frozen functional object:

> **DescriptionUseMode** — does reference follow a particular speaker-target independently established by context, or whoever actually satisfies the description?

045 is theory-neutral about whether Donnellan's distinction is semantic or pragmatic.

Two exact consequences:

```text
TargetVsSatisfierMargin
DescriptionEssentialityLogit
```

Causal edit must preserve:

```text
SpeakerTargetFactLogit
DescriptionTruthLogit
EntityFactLogit
```

Generic ToM, salience or coreference collapse is fatal.

---

# Non-registered boundary

- **036:** HARD AUDIT / GPU PAUSED. Metaphor route-identification contract remains under-repaired.
- **043:** STRICT HARD AUDIT / GPU PAUSED. Do not count it and do not run GPU merely because it was once provisionally registered.
- **037 / 039:** archived terminal deaths.

Recent strict-search terminal families include focus/background information structure and permission-vs-ability modal sense. Their individual records plus the strict failure addendum are mandatory semantic memory.

---

# Failure-library discipline

Every new serious candidate:

```text
one-sentence object
→ aliases
→ canonical index + strict addendum
→ individual rejected/archive records
→ strongest-neighbor BODY / appendix
→ N0/N1/N2
→ real substrate
→ confound identifiability
→ causal specificity
```

Changing model, dataset, language, probe, SAE, steering, patching or architecture does not create a new scientific object.

---

# Paper expansion

```text
phenomenon / natural object
→ broad characterization / clean factorization
→ abstraction / cross-setting transfer
→ causal use / specificity
→ mechanism-derived falsifiable prediction
→ targeted behavioral confirmation
→ optional mitigation / architecture generalization
```

Do not invent later stages before earlier evidence earns them.

## One-line discipline

> **Current honest state is 8 registered projects: base 5/5 plus strict extension 3/3 = 042, 044, 045. The stricter search explicitly downgraded 043 rather than protecting its previous PASS. Simple is good; method-only novelty is not; causal specificity must preserve the neighboring raw capability.**