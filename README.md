# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然、反直觉、可机制化的问题**。

2026-08-30 Top-6 实跑暴露了一个根本问题：之前的流程过度奖励“能构造漂亮 factorial experiment”，却没有把 **scientific question 本身是否自然、是否高 existence-prior** 放在最前面。

因此现在的顺序是：

```text
natural question
→ strong mother / external concept anchor
→ Hamdi-style mother-inclusion N0
→ data as measurement instrument
→ cheap behavioral/capability contract
→ controls
→ mechanistic interpretability
```

而不是从 dataset 或 probe 反推题目。

核心规则：[`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)。

## 当前研究主线

### 014 Alias Entrainment Transfer — established / paper development

Broad cross-surface learned-relation spillover 已经成立；reference-specific/entity-salience interpretation 不成立。论文主线固定为 cross-surface transfer 的 structural gradient 与 lexical/reference boundary，不再救 reference-positive subset。

### 018 Stock–Flow Correlation Intrusion — bounded D0-v2 redesign

科学问题保留；D0-v1 是 A/B recognition measurement failure，不是 scientific null。下一轮只允许修 semantic/numeric net-recognition instrument，保持原 600 natural windows 和完整 2×2 population。

### 024 Alignment: Descriptive Social Model vs Normative Readout — N0 PASS

强 mother 已经证明 alignment 会让模型更 normative、较不 descriptive；ACL 2025 也已证明 descriptive/prescriptive influence 并存。

所以我们不 claim “两个成分存在”，而问更下一层：

> **alignment 到底把模型对真实人类行为的 descriptive social model 改坏了，还是该知识仍在，只是 normative signal / late readout 在输出时赢了？**

详细合同：[`active/024_alignment_descriptive_normative_arbitration/`](active/024_alignment_descriptive_normative_arbitration/)。

### 025 World-Indexed Truth — N0 PASS

不是再比较 fictional truth 与 factual truth，也不是 context-vs-memory conflict。

> **同一个 proposition 在 actual world 和明确 stipulated local world 下具有不同 truth value 时，模型是否把 truth 绑定到 world index，并能同时保留两种 valuation？**

详细合同：[`active/025_world_indexed_truth/`](active/025_world_indexed_truth/)。

三条新轴的完整 mother-inclusion audit：[`phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md)。

## 本轮 novelty 直接杀掉

**Superseded Truth ≠ Never-True Falsehood** 不注册。

2026 *The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations* 已经覆盖 temporal validity/drift 独立轴、stale-recall vs confabulation、cross-cutoff、MLP dynamics 和 steering；继续换数据/命名没有独立叙事。

记录：[`rejected_candidates/temporal_validity_superseded_vs_never_true.md`](rejected_candidates/temporal_validity_superseded_vs_never_true.md)。

## 2026-08-31 active cleanup

以下旧项目已移到 `archive/`：

- 007 Weak-Evidence Backfire — terminal hard kill，纠正 stale active provenance；
- 020 Incremental Clue Backfire — 被 `candidate_topics` Topic 28 同一 scientific object 完整吞并；
- 021 Task-Switch Carryover — current refinement 只是已有 mother 的 diagnostic/mechanism subproblem；
- 022 Local Success, Global Composition Failure — core object 已是 known compositionality gap。

`023 Description–Experience Gap` **没有一起归档**：它本身是长期自然认知现象，保留 `HOLD-N0-REAUDIT`，但目前无 model call。

## 关键入口

- [`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md) — pre-discovery gate。
- [`phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md) — 最新 mother-inclusion N0。
- [`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md) — authoritative focus queue。
- [`active/README.md`](active/README.md) — active / HOLD 项目入口。
- [`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md) — 唯一 model-call authorization。
- [`archive/README.md`](archive/README.md) — 正式归档。
- [`rejected_candidates/README.md`](rejected_candidates/README.md) — novelty / pre-registration 负知识。

## One-line discipline

> **像 Hamdi 一样：先从一个已经重要的母问题自然走出一个新的科学对象，再用可解释性回答“模型内部到底把什么当成变量”；不要再从实验设计倒推现象。**
