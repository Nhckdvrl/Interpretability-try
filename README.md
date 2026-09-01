# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、自然、清楚、题目幅度正常且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
CURRENT_HARD_AUDIT_TOPICS: 1
fresh_register_target: 5
fresh_register_status: OPEN_ONE_SLOT
required_protocol: PAPER-SCALE v2.1
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
remaining_needed: 1
```

## Fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / HARD RE-AUDIT PASSED** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |
| [`040_numerical_identity_vs_qualitative_sameness`](active/040_numerical_identity_vs_qualitative_sameness/) | **PASS-REGISTER / GPU AUTHORIZED** | If two things are exactly alike, does the model still know whether they are literally the same individual or merely two different things of the same kind? |

**Current honest fresh PASS register: 4/5. Count does not protect any topic.**

## 040 — newly registered after deep audit

Frozen object:

> **Numerical identity** (`literally the same individual`) versus **qualitative/type sameness** (`same kind / same properties`).

Why it survives:

- independent human scientific object, including Cognition 2023 work explicitly distinguishing two senses of sameness;
- natural human event substrate with the crucial double dissociation: **same token despite substantial state change** versus **different token despite same type/high similarity**;
- Davis & Altmann 2021 LSTM/RNN work is treated as a serious computational precursor, not ignored;
- modern entity-binding/tracking work studies binding or state propagation after individuation is supplied, and even exposes same-label duplicate failures, but does not make numerical-vs-qualitative identity the causal scientific object;
- 040 is killed if it reduces to `the vs another`, generic coreference/binding, or the old RNN event-specific result.

The first causal contract is frozen around **token-specific history transfer vs preserved shared type knowledge**.

See [`active/040_numerical_identity_vs_qualitative_sameness/README.md`](active/040_numerical_identity_vs_qualitative_sameness/README.md).

## 036 — still not counted

[`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) remains:

**HARD AUDIT / CONTINUE-PAPER-SCALE / GPU PAUSED / NOT PASS-REGISTER.**

The selector question (`conventionality vs aptness -> comparison vs categorization`) survives novelty, but the former causal metric was underidentified. It may return only after a clean two-signature route-identification contract is frozen.

## 037 / 039

- 037: **KILL-NOVELTY / ARCHIVED**.
- 039: **KILL-NOVELTY / ARCHIVED** after deeper object-ownership audit. Taxonomic-vs-thematic relation type was already directly studied in language-model representations/behavior; stronger MI alone was not enough.

Canonical lesson:

> **Object ownership, not title ownership.**

## Discovery / dedupe discipline

Before HARD AUDIT, check:

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — v2.1 authoritative protocol;
2. [`rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`](rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md) — semantic dedupe memory;
3. `rejected_candidates/` + `archive/` aliases;
4. strongest-neighbor paper bodies, not title wording.

Changing model, dataset, language, probe, SAE, patching or steering does not create a new scientific object.

## How to grow a surviving topic into a Main-paper package

See [`phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`](phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md).

Evidence-based pattern learned from ACL/EMNLP/NAACL strong papers:

```text
phenomenon / natural object
→ broad characterization / clean factorization
→ abstraction or cross-setting transfer
→ causal use / specificity
→ mechanism-derived falsifiable prediction
→ targeted behavioral confirmation
→ optional mitigation / architecture generalization
```

Do not pre-invent later stages. Stop at the last stage earned by evidence.

## Current authority

1. `phenomenon_miner/FINDING_RULES.md` — sole discovery protocol, v2.1
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — current handoff
3. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md` — audit state
4. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md` — execution flow
5. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md` — post-selection evidence ladder
6. this README — register count and entrypoint

## One-line discipline

> **Simple is good. Trivial is not. Method-only novelty is not. A PASS needs a new object/question plus an experiment that identifies causal use. Current honest state: 4/5.**
