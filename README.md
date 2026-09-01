# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 3
CURRENT_FRESH_ACTIVE_TOPICS: 3
CURRENT_HARD_AUDIT_TOPICS: 1
fresh_register_target: 5
fresh_register_status: OPEN_AFTER_039_KILL_AND_036_DEMOTION
required_protocol: PAPER-SCALE v2.1
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
current_target: keep surviving science clean; repair 036 only if route identifiability can be frozen, and broad-search replacements without count filling
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update, or rely on separate/static heuristics? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT PASSED** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |

**当前 authoritative fresh PASS register 是 3/5。** Count 不保护任何题。

## 036 — question survives, former PASS does not

[`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) is now:

**HARD AUDIT / CONTINUE-PAPER-SCALE / GPU PAUSED / NOT IN PASS REGISTER.**

The scientific question still looks novel enough:

> What selects comparison versus categorization in metaphor comprehension: vehicle conventionality, topic–vehicle aptness, or neither?

A deeper 2026 audit found that LLM metaphor **aptness** is already an explicit scientific/evaluation object and that conventional/novel metaphor processing is already analyzed internally. However, no direct 2025–2026 LLM work was found that orthogonalizes conventionality × aptness to decide comparison versus categorization.

The fatal issue is instead **measurement/identifiability**: the former first causal statistic treated `X is Y` ↔ `X is like Y` activation non-interchangeability as comparison↔categorization route evidence. That can be caused by the token `like`, syntax, position and generic form processing. Human theory itself uses multiple independent route diagnostics, including grammatical concordance and directionality. Until a two-signature route-calibration contract is frozen, 036 is not GPU-authorized and does not count.

See the rewritten project README and [`phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`](phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md).

## 038 — hard re-audit passed

038 was attacked against:

- `It Depends` persistent referential-ambiguity behavior;
- `Correct-Detect` ambiguity detection/resolution trade-off;
- 2026 generic hidden-state premature commitment;
- EACL 2026 idiom literal/figurative parallel causal pathways;
- Aug 2026 lexical-ambiguity activation patching;
- contextual grammatical-cue activation patching.

No direct work was found that owns the exact representational-format question for a **still unresolved discourse reference**: explicit parallel candidate referents vs a compact underspecified reference state vs one premature commitment. Its existing H1-vs-H2 identifiability kill is also explicit enough to prevent retreat to `ambiguity is represented somewhere`.

Detailed audit: [`active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md`](active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md).

## Deregistered 037

Former [`037_generic_generalization_licensing`](archive/037_generic_generalization_licensing/) is **KILL-NOVELTY / ARCHIVED** after a direct 2026 principled-vs-statistical generic-property collision.

## Deregistered 039 — new canonical N2 negative example

Former [`039_same_kind_vs_go_together_semantic_relation`](archive/039_same_kind_vs_go_together_semantic_relation/) is **KILL-NOVELTY / ARCHIVED / GPU NOT AUTHORIZED**.

The deeper audit found that taxonomic similarity versus thematic relatedness is already studied directly in language-model representations and LLM behavior, including use of the same 659-pair TxThmNorms substrate and explicit taxonomic–thematic LLM choice/reasoning. The remaining delta had collapsed to stronger hidden-state/causal MI on an already-owned object.

Detailed record: [`rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`](rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md).

Canonical lesson:

> **Object ownership, not title ownership.** If prior work already treats the exact natural distinction as an LLM behavior/representation/reasoning axis, `we will causally patch it` is usually not enough for N2.

## 034 / 035 frozen collision scan

A lightweight fatal-collision-only scan found no new LLM work directly occupying their frozen questions. Do not rework their headlines absent new evidence.

## 当前 authority

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议，当前 v2.1**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — current authoritative handoff
3. [`phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`](phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md) — latest hard-audit evidence
4. 本 README — register 计数与入口

## v2.1 one-line discipline

> **Simple is good. Trivial is not. Method-only novelty is not. A PASS requires both a new scientific object/question and an experiment that actually identifies it. Current honest state: 3/5.**
