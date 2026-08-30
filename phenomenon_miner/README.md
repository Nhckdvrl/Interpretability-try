# Phenomenon Miner

版本：2026-08-30  
状态：`v5 / POST-TOP6-AUDIT / PHENOMENON-FIRST`

本目录负责找题、快速证伪、记录失败模式，以及区分 behavioral evidence 与 mechanism。

## 当前入口

- [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) — 当前还值得继续投入的题。
- [`TOP6_RESULT_REVIEW_2026-08-30.md`](TOP6_RESULT_REVIEW_2026-08-30.md) — 015/016/014/017/018/019 的独立 post-run 审查。
- [`../active/README.md`](../active/README.md) — 当前项目入口。
- [`../archive/README.md`](../archive/README.md) — 已被诊断性实验终止的项目。
- [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) — 唯一 model-call authorization。
- [`FAILED_TOPICS.md`](FAILED_TOPICS.md) — anti-revival lessons。
- [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) — population / attrition / factor-not-filter。
- [`FINDING_RULES.md`](FINDING_RULES.md) — phenomenon-first 与 promotion 规则。

## Top-6 审完后的状态

### Positive

**014 Alias Entrainment Transfer**：broad cross-surface learned-relation spillover 成立；reference-specific salience 不成立。继续做 paper synthesis，不再救 entity claim。

### Inconclusive because measurement failed

**018 Stock–Flow Correlation Intrusion**：ResOpsUS source design 有效，但 A/B forced-choice net-recognition gate 被极端 option-position bias 破坏。不能把它归档成 scientific null；状态为 `HOLD-D0-MEASUREMENT-FAILURE`，新 D0 v2 contract 冻结前禁止 rerun。

### Archived

- 015 Clarification Resolution Lag
- 016 Mixed-Status Event Attraction
- 017 Cross-Modal Resolution Inertia
- 019 Abstention Hysteresis

这四个不是“差一点过线”，而是各自 preregistered fatal control 真正解释掉 / 否掉了 registered phenotype。

## 尚未裁决

- 020 Incremental Clue Backfire — collision-first
- 021 Task-Switch Carryover — old-rule-specific wrong destination only
- 022 Local Success, Global Composition Failure — must exceed known compositionality gap
- 023 Description–Experience Gap — exact-frequency / EV capability gated

## 新增的判定纪律

### `NO-PROMOTE` 不自动等于 `KILL`

D0 失败后必须再分类：

```text
A. diagnostic scientific failure
   fatal control explains effect / well-powered clean null
   -> ARCHIVE

B. measurement or capability failure
   intended estimand never had a legal denominator
   -> INCONCLUSIVE / REDESIGN
```

018 是 B；015/016/017/019 是 A。

### Archive 不等于“宇宙中绝对不存在任何相近现象”

Archive 的含义是：**当前 scientific identity + current registered causal contrast 已经终止**。以后如果换成真正不同的问题，必须新建项目，不能用新 prompt / subset / readout 偷偷复活旧题。

## 不变原则

> **phenomenon before mechanism；diagnostic controls before story；measurement failure is not scientific falsification；clean falsification is not an invitation to search for a favorable subset.**
