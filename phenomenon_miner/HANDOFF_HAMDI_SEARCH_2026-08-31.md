# Hamdi-Style Topic Search — Current Handoff

> **Execution override — 2026-09-04:** 035 is archived after its corrected full-data,
> cross-model recipient gate failed. 040 is archived after its abstraction and causal-use
> gates failed. 034 is kept for mechanistic development; 038 is testing a late-decision
> prediction exposed by the pronoun-state null.

Date: 2026-09-01  
Status: **AUTHORITATIVE CURRENT STATE — BASE 5/5 + STRICT EXTENSION 3/3 = 8 REGISTERED**

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

## Mandatory reads next turn

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md`
3. `phenomenon_miner/STRICT_EXTENSION_GATE_2026-09-01.md`
4. `phenomenon_miner/STRICT_EXTENSION_REGISTER_2026-09-01.md`
5. this handoff
6. `rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`
7. `rejected_candidates/STRICT_EXTENSION_FAILURE_INDEX_ADDENDUM_2026-09-01.md`
8. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md`
9. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`
10. active READMEs for 034/035/036/038/040/041/042/043/044/045
11. hard re-audits for 038/041/042/044/045
12. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`
13. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-09-01.md`

The canonical failure index and strict-extension addendum are **joint mandatory semantic memory** for any new candidate.

## Strict extension standard

Post-base topics do not pass by `old behavior + modern open model + stronger MI`.

A strict topic needs a genuinely orthogonal object and causal specificity with preserved raw content, plus at least two:

- Lock A: same-surface / orthogonal role-swap identifiability;
- Lock B: cross-setting abstraction;
- Lock C: two independent theory-grounded consequences.

If Lock C is used, exact diagnostics are frozen before GPU.

## 041

Retained after second strict audit only for the same-lexical context-conditioned modifier set-restriction role. Weaker descriptor necessity/informativeness is already occupied.

## 042 — STRICT PASS

Question:

> Is a definite description licensed by uniqueness or by strong discourse familiarity?

Strong familiarity = explicit discourse/interlocutor re-mention, not simple antecedent presence.

Preserve:

```text
CandidateStructureLogit
DialogueMentionFactLogit
EntityPresenceLogit
```

## 043 — DOWNGRADED / NOT COUNTED

```yaml
PASS_REGISTER: false
GPU_AUTHORIZED: false
verdict: STRICT HARD AUDIT
```

Blockers: theory-neutrality, insufficient consensus-clear item gold, severe lexical-predicate confound, and no true Lock A.

Frozen diagnostics if resurrected:

```text
MemberInheritance
IndefiniteSingularCompatibility
```

No GPU until its documented resurrection condition is met.

## 044 — STRICT PASS

Question:

> Does a property characterize the individual as such or only a particular stage/situation?

Not temporary vs permanent.

Exact diagnostics:

```text
SituationBoundLogit
DepictiveCompatibilityLogit
```

Same causal state must shift both while preserving `PropertyTruthLogit`.

## 045 — STRICT PASS

Question:

> Does reference follow a person the speaker independently has in mind, or whoever actually satisfies the description?

Functional `DescriptionUseMode`, theory-neutral about semantic-vs-pragmatic analysis.

Exact consequences:

```text
TargetVsSatisfierMargin
DescriptionEssentialityLogit
```

Preserve:

```text
SpeakerTargetFactLogit
DescriptionTruthLogit
EntityFactLogit
```

## 036

Still HARD AUDIT / GPU PAUSED. Do not force-repair.

## Failure memory

Recent strict terminal families include:

- focus/background information structure;
- permission vs ability / deontic vs dynamic modal sense.

Read their individual rejection records and the strict failure addendum. Do not revive through model/language/MI changes.

## Current task boundary

The user-requested extension target is complete at **3/3**. Default next work is execution/prioritization, not automatic count filling.

## One-line instruction

> **Authoritative register is 8: 034, 035, 038, 040, 041, 042, 044, 045. 043 was honestly downgraded after the stronger audit. Count never protects a topic.**
