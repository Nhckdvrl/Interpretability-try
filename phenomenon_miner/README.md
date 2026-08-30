# Phenomenon Miner

版本：2026-08-30  
状态：`v5 / PHENOMENON-FIRST / CHEAP-D0-SCREENING / STRICT-MECHANISM-GATE`

本目录负责三件事：

1. 定义什么题值得跑；
2. 记录当前 Top-10 与失败库；
3. 控制 cheap screening 与正式 validation / mechanism 的边界。

---

## 当前原则

### Phenomenon before mechanism

如果问题离开 probe / neuron / head / representation 就没法讲，它优先算 mechanism follow-up，不算新 phenomenon。

### D0 可以早跑

2026-08-30 owner 决策后，不再要求所有候选必须先完成完整 N1 + D0 文档审查才允许一次 cheap model call。

现在允许：

```text
natural question
+ clear adjacent-work boundary
+ source/deterministic data path
-> register active screening
-> materialize data
-> cheap D0 smoke
```

目的就是快速 kill。

### Mechanism 仍然晚跑

任何 probe / patch / head ablation / causal claim 前仍必须：

```text
behavioral phenotype PASS
+ exact N1 collision closure
+ source population / hard gold
+ scope integrity
+ fatal controls
+ frozen behavioral contract + data/generator SHA
```

### Data should be programmatic where possible

优先：

- source dataset 自带 label；
- source structure 自动配 pair；
- supporting evidence 自动 ablate / restore；
- time series 自动切 diagnostic window；
- deterministic generator 自动算 oracle。

人工只随机检查 builder，不给主数据打新 gold。

### Population before clean subset

不能为了出显著结果不断删 domain/type/direction。理论 moderator 默认 factor-not-filter。

---

## 当前入口

- [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) — **authoritative Top-10 screening queue**。
- [`../active/README.md`](../active/README.md) — 实际项目入口；每题有详细 README。
- [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) — screening / full validation / mechanism 授权。
- [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) — scope / attrition / factor-not-filter 纪律。
- [`FAILED_TOPICS.md`](FAILED_TOPICS.md) — hard kill / route / anti-revival lessons。
- [`FINDING_RULES.md`](FINDING_RULES.md) — 更完整的 finding / promotion 规则；其中与当前 screening policy 冲突的“模型调用时点”以本 README + AUDIT_REGISTRY 2026-08-30 版本为准，机制门槛不变。
- [`DATA_REVIEW_2026-08-29.md`](DATA_REVIEW_2026-08-29.md) — 前一轮 data-first pruning 的历史审查，不再代表当前 Top-10 调度。

---

## Current Top-10

1. [`015 Clarification Resolution Lag`](../active/015_clarification_resolution_lag/)
2. [`016 Mixed-Status Event Attraction`](../active/016_mixed_status_event_attraction/)
3. [`014 Alias Entrainment Transfer`](../active/014_alias_entrainment_transfer/)
4. [`017 Cross-Modal Resolution Inertia`](../active/017_cross_modal_resolution_inertia/)
5. [`018 Stock-Flow Correlation Intrusion`](../active/018_stock_flow_correlation_intrusion/)
6. [`019 Abstention Hysteresis`](../active/019_abstention_hysteresis/)
7. [`020 Incremental Clue Backfire`](../active/020_incremental_clue_backfire/)
8. [`021 Task-Switch Carryover`](../active/021_task_switch_carryover/)
9. [`022 Local Success, Global Composition Failure`](../active/022_local_success_global_composition_failure/)
10. [`023 Description-Experience Gap`](../active/023_description_experience_gap/)

---

## 必须记住的 novelty collisions

### 014 Alias

ACL 2025 Outstanding `Llama See, Llama Do` 已建立 contextual entrainment + entrainment heads。我们的 surviving question 是 cross-surface learned relation 是否进一步支持 reference identity；当前还没证明 entity claim。

### 015 Clarification

CondAmbigQA / PRACTIQ 已研究 ambiguity + clarification。我们只研究**final condition 相同，prior ambiguous history 是否造成 resolution lag**。

### 017 Cross-modal

MUCAR 已证明 static cross-modal ambiguity resolution 很难。我们只研究**先形成旧解释后，晚到 modality 是否更难纠正**。

### 019 Abstention

AbstentionBench / Abstain-R1 已研究什么时候拒答、如何 clarification。我们只研究**证据后来补齐后 prior refusal 是否仍粘着**。

### 020 Incremental clue

“more context hurts”不是新现象；还要先查内部旧 referent-displacement failure 是否覆盖同一对象。

### 021 Task switch

Gupta et al. EMNLP 2024 已证明 task-switch interference。只有 **old-rule-specific wrong destination / decay** 才可能新。

### 022 Composition

Press et al. 2023 已经正式定义 compositionality gap。只有 **correct intermediate facts 已显式在同一 context 里，final composition 仍错** 才可能值得继续。

### 023 Description–Experience

LLM risk-choice / cognitive-bias 文献很多；必须 exact-frequency 控制并深搜最新 2026 工作。

---

## 当前实际跑序

```text
015 -> 016 -> 019 -> 020 -> 018 -> 017 -> 023 -> 021 -> 022
014 独立走 r4 construct validation
```

排序考虑的是“最快得到 informative null / positive”，不是最终 paper rank。

---

## Terminal / parked

- 007 Weak-Evidence Backfire — TERMINAL HARD KILL；
- 013 Publicness–Coordination — PARKED/HOLD-DATA；
- manual-heavy subgroup/legal/medical topics — PARKED；
- Training-Recency / Agreement / Habitual / Competing-Event — HOLD-DATA。

---

## 一句原则

> **便宜行为实验可以早跑，mechanism 不可以早跑。我们现在要的是让程序化 D0 快速告诉我们“这个自然现象到底有没有”，而不是把数据工程或 hidden-state 分析当成选题本身。**
