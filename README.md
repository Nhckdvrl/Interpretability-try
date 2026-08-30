# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然反直觉现象**。

2026-08-30 Top-6 实跑之后，仓库做了两次重要修正：

1. `NO-PROMOTE` 必须区分 scientific null 与 measurement failure；
2. 更根本地，**选题不能再从“数据集能构造什么实验”出发，而必须从一个自然、直观、高 existence-prior 的 scientific question 出发。**

新的 pre-discovery 总门：[`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)。

## 当前唯二重点

### 014 Alias Entrainment Transfer — paper development

Broad cross-surface learned-relation spillover 已经成立：三家族、双 frame、双方向稳定超过强 `ASSOC_ANY` different-referent control。

真正被否掉的是 reference-specific/entity-salience interpretation。当前论文应围绕：

```text
cross-surface spillover
→ structural gradient
→ shared upstream causal machinery
→ lexical direct-write boundary
→ opaque-strict reference boundary
```

不再找 reference-positive subset。

### 018 Stock–Flow Correlation Intrusion — D0 v2 redesign

科学问题保留，但 D0 v1 不构成 null：A/B net-recognition gate 被严重 option-position bias 破坏，negative-net cells 没有合法 strict denominator。

下一步只允许替换 recognition instrument 为 semantic `positive/negative` 或 deterministic numeric sign；原 600 ResOpsUS windows、四个 semantic cells、reservoir clustering 和 explicit-correct-net control 全部保持。

## 暂停 020–023

此前尚未裁决的：

- 020 Incremental Clue Backfire
- 021 Task-Switch Carryover
- 022 Local Success, Global Composition Failure
- 023 Description–Experience Gap

全部停止 screening。它们必须先按 Natural-Question Gate 重新证明：问题本身自然、有趣、低/中 absence risk，而且不用复杂 builder 才能表达。

**之前注册过，不再构成继续跑的理由。**

## 已归档的 completed Top-6 failures

- 015 Clarification Resolution Lag
- 016 Mixed-Status Event Attraction
- 017 Cross-Modal Resolution Inertia
- 019 Abstention Hysteresis

完整项目、代码、raw results 和最终裁决都在 [`archive/`](archive/README.md)。逐题独立审查见 [`phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md`](phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md)。

## 关键入口

- [`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md) — **新题第一道门，早于 novelty/data。**
- [`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md) — 当前 focus queue。
- [`active/README.md`](active/README.md) — 当前项目。
- [`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md) — 唯一模型调用授权。
- [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — N0/N1/D0 discovery 规则；现在必须在 Natural-Question Gate 之后执行。
- [`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md) — anti-revival failure library。
- [`phenomenon_miner/DATASET_SCOPE_AUDIT.md`](phenomenon_miner/DATASET_SCOPE_AUDIT.md) — 数据 scope 纪律。

## 新的顺序

```text
natural question
→ one ordinary example
→ existence prior
→ 5–20 example sanity
→ only then novelty search
→ only then dataset/source selection
→ behavioral evidence
→ controls
→ mechanism
```

而不是：

```text
dataset
→ clever factorial construction
→ hope a phenomenon appears
→ mechanism story
```

## One-line discipline

> **问的是自然问题，数据只是测量仪器。去掉数据集和可解释性术语后仍然值得追问，才配进入仓库主线。**
