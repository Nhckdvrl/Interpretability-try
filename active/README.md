# Active Projects

`active/` 只表示**当前仍值得投入计算/论文开发**的项目。目录历史存在不等于当前 fresh-search authorization；权威状态看 root README + `phenomenon_miner/FINDING_RULES.md` + current handoff。

## Fresh authoritative register

```yaml
CURRENT_FRESH_ACTIVE_TOPICS: 5
CURRENT_FRESH_PASS_REGISTER: 5
fresh_register_target: 5
fresh_register_status: COMPLETE_AFTER_039_REGISTRATION
required_protocol: PAPER-SCALE v2.1
```

| project | status | note |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Prospective-memory retrieval: strategic monitoring vs spontaneous cue-triggered retrieval vs dynamic switching |
| [`035_shared_dynamic_context_update`](035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Shared dynamic local-context update across anaphora and presupposition vs separate/static computation |
| [`036_metaphor_processing_route_selection`](036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED** | What selects comparison vs categorization in metaphor processing: conventionality, aptness, or no discrete switch? |
| [`038_unresolved_reference_representation_architecture`](038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED** | When reference is unresolved, does the model keep alternatives, underspecify, or prematurely commit? |
| [`039_same_kind_vs_go_together_semantic_relation`](039_same_kind_vs_go_together_semantic_relation/) | **PASS-REGISTER / GPU AUTHORIZED** | Does the model distinguish **same kind** from **go together in an event/scenario** as a reusable, causally used semantic relation? |

The fresh target is now **5/5**, but count is not a protection rule. Any project can still be demoted if a new novelty collision, substrate failure, or frozen falsifier is found.

## Deregistered 037

`037_generic_generalization_licensing` is **not active and does not count**. It was moved to `archive/037_generic_generalization_licensing/` after the 2026-07 direct principled-vs-statistical generic-property collision. Do not recreate it inside the fresh register.

## v2.1 calibration

`FINDING_RULES.md` explicitly states **strict ≠ complicated**. Route C (simple phenomenon / simple latent object first) is legal. N0/N1/N2, benchmark-removal, auditable substrate, story invariance, and anti-post-hoc rules remain strict; universal three-mechanism / two-family / exact-interaction requirements do not.

036 and 038 passed the present v2.1 re-audit: no new fatal direct collision was found, and their natural headline questions remain broader than their individual benchmarks. Their headlines remain frozen.

039 is the clean Route-C example for this round: a natural pre-existing semantic distinction (`same kind` vs `go together`) with dual human ratings on the same word pairs, strongest-neighbor separation, and one minimal causal-use test.

## 当前真正保留的旧工作

| project | status | note |
|---|---|---|
| [`014_alias_entrainment_transfer`](014_alias_entrainment_transfer/) | **ESTABLISHED / PAPER DEVELOPMENT** | 已有正式结果；与 fresh 5/5 register 分离 |

其它仍物理存在于 `active/` 的旧目录只保留历史/HOLD provenance；它们不自动拥有新实验权限，也不计入 fresh slate。

## 029–033 已归档

- `029_etr_human_like_fallacy` — topic-scale + provenance re-audit failed。
- `030_spatial_reference_frame_transformation` — VLM；退出当前 LLM target。
- `031_spontaneous_deception_knowledge_action` — terminal V3 measurement failure + canonical F8 benchmark-dependence/scope-drift lesson。
- `032_temporal_forgetting_mechanism` — mechanistic follow-up scale too close to mother。
- `033_contextual_entrainment_opposite_scaling` — novelty delta too close to prior mechanism/mother interpretation + item-data gap。

## Active discipline

**ACTIVE / PASS-REGISTER 不是“这个实验值得试”，而是“这个问题本身值得一篇论文，并且已有合法实验入口去回答”。** v2.1 允许简单问题，但不允许弱 novelty、behavior lottery 或 null 后换 headline。