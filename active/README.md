# Active Projects

`active/` 只表示**当前仍值得投入计算/论文开发**的项目。目录历史存在不等于当前 fresh-search authorization；权威状态看 root README + `phenomenon_miner/FINDING_RULES.md` + current handoff。

## Fresh authoritative register

```yaml
CURRENT_FRESH_ACTIVE_TOPICS: 4
CURRENT_FRESH_PASS_REGISTER: 4
fresh_register_target: 5
fresh_register_status: OPEN_AFTER_039_DEREGISTRATION
required_protocol: PAPER-SCALE v2.1
```

| project | status | note |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Prospective-memory retrieval: strategic monitoring vs spontaneous cue-triggered retrieval vs dynamic switching |
| [`035_shared_dynamic_context_update`](035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Shared dynamic local-context update across anaphora and presupposition vs separate/static computation |
| [`036_metaphor_processing_route_selection`](036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE** | What selects comparison vs categorization in metaphor processing: conventionality, aptness, or no discrete switch? |
| [`038_unresolved_reference_representation_architecture`](038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE** | When reference is unresolved, does the model keep alternatives, underspecify, or prematurely commit? |

The fresh target is **4/5**. Count is not a protection rule. Any project can still be demoted if a new novelty collision, substrate failure, or frozen falsifier is found.

## Deregistered 037

`037_generic_generalization_licensing` is **KILL-NOVELTY / ARCHIVED** under `archive/037_generic_generalization_licensing/` after the 2026 direct principled-vs-statistical generic-property collision.

## Deregistered 039

`039_same_kind_vs_go_together_semantic_relation` is **KILL-NOVELTY / ARCHIVED / GPU NOT AUTHORIZED** under `archive/039_same_kind_vs_go_together_semantic_relation/`.

The deeper hard audit found that taxonomic similarity vs thematic relatedness is already directly studied in language-model representations/LLM behavior, including use of the same TxThmNorms substrate and explicit taxonomic–thematic LLM choice/reasoning. The remaining 039 delta was primarily stronger causal MI on an already-owned object, so it fails v2.1 N2.

Detailed failure record: [`../rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`](../rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md).

## v2.1 calibration

`FINDING_RULES.md` explicitly states **strict ≠ complicated**. Route C is legal, but the new 039 failure makes one boundary explicit:

> **simple new object = potentially strong; simple already-owned object + stronger MI = still KILL.**

N0/N1/N2, benchmark-removal, auditable substrate, story invariance, and anti-post-hoc rules remain strict.

036 and 038 remain active while their present hard re-audit is completed. Their prior PASS is not a shield against new fatal evidence.

## 当前真正保留的旧工作

| project | status | note |
|---|---|---|
| [`014_alias_entrainment_transfer`](014_alias_entrainment_transfer/) | **ESTABLISHED / PAPER DEVELOPMENT** | 已有正式结果；与 fresh register 分离 |

其它仍物理存在于 `active/` 的旧目录只保留历史/HOLD provenance；它们不自动拥有新实验权限，也不计入 fresh slate。

## 029–033 已归档

- `029_etr_human_like_fallacy` — topic-scale + provenance re-audit failed。
- `030_spatial_reference_frame_transformation` — VLM；退出当前 LLM target。
- `031_spontaneous_deception_knowledge_action` — terminal V3 measurement failure + canonical F8 benchmark-dependence/scope-drift lesson。
- `032_temporal_forgetting_mechanism` — mechanistic follow-up scale too close to mother。
- `033_contextual_entrainment_opposite_scaling` — novelty delta too close to prior mechanism/mother interpretation + item-data gap。

## Active discipline

**ACTIVE / PASS-REGISTER 不是“这个实验值得试”，而是“这个问题本身值得一篇论文，并且已有合法实验入口去回答”。** 当前诚实状态是 4/5；不要为了恢复 5/5 草率注册 replacement。
