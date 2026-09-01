# Hamdi-Style Topic Search — Current Handoff

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

Read in this order:

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1 base protocol
3. `phenomenon_miner/STRICT_EXTENSION_GATE_2026-09-01.md` — additive higher bar for 042+
4. `phenomenon_miner/STRICT_EXTENSION_REGISTER_2026-09-01.md`
5. this handoff
6. `rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`
7. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`
8. active READMEs for 034/035/036/038/040/041/042/043/044/045
9. hard re-audits for 038/041/042/044/045
10. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`
11. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-09-01.md`

## Frozen base register

034 / 035 / 038 / 040 remain frozen unless a genuinely new fatal collision appears.

041 survived a second strict audit only for the narrow object:

> same-lexical context-conditioned modifier set-restriction role, cross-setting and causally specific to referent narrowing while preserving property truth.

Recent descriptor-necessity work owns weaker claims.

## Strict extension standard

Post-base topics do not pass by `old behavior + modern open model + stronger MI`.

Every strict topic must add a genuinely orthogonal object and causal specificity, and pass at least two of:

- Lock A: same-surface / orthogonal role-swap identifiability;
- Lock B: cross-setting abstraction;
- Lock C: two independent theory-grounded consequences.

A neighboring raw capability/fact must be preserved under intervention.

## 042 — PASS after corrected re-audit

Question:

> Is a definite description licensed by uniqueness or by strong discourse familiarity?

Important correction: strong familiarity is explicit interlocutor mention/re-mention, not mere antecedent existence.

Critical source cross:

```text
unique + not strongly familiar
vs
non-unique + strongly familiar
```

Preservation denominators:

```text
CandidateStructureLogit
DialogueMentionFactLogit
EntityPresenceLogit
```

Raw recency/salience collapse is fatal.

## 043 — DOWNGRADED / NOT COUNTED

Question: direct kind predication vs characterizing/member-level generic predication.

Status:

```yaml
PASS_REGISTER: false
GPU_AUTHORIZED: false
verdict: STRICT HARD AUDIT
```

Why paused:

- surrounding generic LLM space is heavily occupied;
- broad formal partition is not fully theory-neutral;
- no sufficiently large consensus-clear model-independent causal inventory was frozen;
- lexical predicate shortcut remains too strong for Lock A.

Frozen diagnostics if resurrected:

```text
MemberInheritance
IndefiniteSingularCompatibility
```

Resurrection needs an auditable consensus-clear inventory, genuine same-lexical factorization, or explicit Route-B theory adjudication.

## 044 — PASS after metric repair

Question:

> Does a true property characterize the individual as such or only a particular stage/situation?

Not temporary vs permanent.

Two exact diagnostics are frozen:

```text
SituationBoundLogit
DepictiveCompatibilityLogit
```

The same causal state must shift both while preserving `PropertyTruthLogit`. No later diagnostic shopping.

## 045 — replacement strict PASS

Question:

> Does the model follow a person the speaker independently has in mind, or whoever actually satisfies the definite description?

Functional object: `DescriptionUseMode` — REFERENTIAL vs ATTRIBUTIVE use.

Same critical description changes role only by discourse context.

Two exact consequences:

```text
MisdescriptionTargetMargin / TargetVsSatisfierMargin
DescriptionEssentialityLogit
```

Preserve:

```text
SpeakerTargetFactLogit
DescriptionTruthLogit
EntityFactLogit
```

045 is theory-neutral about whether Donnellan's distinction is semantically encoded or pragmatically derived. It tests functional causal organization, not the philosophy-of-language label.

## 036

Still HARD AUDIT / GPU PAUSED. Do not force-repair.

## New strict-search deaths

Do not revive:

- focus/background information structure — direct neural object ownership;
- permission vs ability / deontic vs dynamic modal sense — BERT modal-sense representation work already owns abstraction beyond modal words.

Detailed records are in `rejected_candidates/`.

## Current default task

The user explicitly requested the strict extension and it is now complete at **3/3**. Do not keep count-filling automatically.

Next sensible work is:

- execute frozen cheap S0 / implementation for registered topics;
- compare the eight projects and prioritize execution;
- harden/reformulate 036 or 043 only if explicitly requested;
- react to new fatal novelty collisions;
- search further only on explicit instruction.

## One-line instruction

> **Authoritative state is 8 registered: 034, 035, 038, 040, 041, 042, 044, 045. 043 was honestly downgraded after the stricter audit. Count never protects a topic.**