# Phenomenon Miner

版本：2026-08-29  
状态：`v4 / PHENOMENON-FIRST / DATA-FIRST / N0+N1+D0 BEFORE REGISTRATION`

本目录是当前 LLM 可解释性现象选题的唯一 discovery 工作区。

## 当前规则

正式注册一个新题之前，必须同时完成：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
    └─ dataset scope-integrity PASS
= DISCOVERY-PASS
```

定义与完整流程看 [`FINDING_RULES.md`](FINDING_RULES.md)。数据寻找/构建还必须通过 [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md)。

最重要的三条纪律：

> **phenomenon before mechanism。**
>
> strong mother paper 可以提供 motivation 和 mechanism opening；但如果 mother 已拥有 headline behavior，而我们只剩 `representation → causal? / route? / where?`，它就是 `MECH-FOLLOWUP`，不是新的 phenomenon candidate。

> **data is part of topic selection。**
>
> novelty 不够会杀题；natural source population / hard gold / independent units / license / construct validity 做不实，同样会杀题。不能先注册再想办法造数据。

> **population before clean subset。**
>
> 控制 confound 应靠 contrast、matching、strata 和统计模型，而不是把母问题越筛越窄。理论 moderator 默认 factor-not-filter。

## 当前入口

- [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) — **唯一 authoritative current phenomenon queue**，data-first re-audit 后只保留 7 题。
- [`DATA_REVIEW_2026-08-29.md`](DATA_REVIEW_2026-08-29.md) — 本轮逐题 data/gold/source 裁决与改进后的 D0 recipe。
- [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) — D0 强制 scope gate：scientific population、factor-not-filter、attrition、双轮人工审计、builder regression tests。
- [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) — **唯一 model-call authorization**；当前 authorized calls = 0。
- [`FAILED_TOPICS.md`](FAILED_TOPICS.md) — KILL / ROUTE / HOLD-DATA 与 anti-revival lessons。
- [`FINDING_RULES.md`](FINDING_RULES.md) — N0、N1、D0、behavior-first、strong-model kill、stop-loss 的正式合同。
- [`MODEL_PANEL.md`](MODEL_PANEL.md) — behavioral smoke / generality 的 checkpoint panel 约定。

## 当前调度

### 近期开 D0 数据审计

1. **Mixed-Status Event Attraction** — MAVEN-FACT same-document mixed-status event pairs
2. **Subgroup-Significance → Interaction Promotion** — open-access RCT subgroup estimates + explicit interaction test
3. **Stock–Flow Correlation Intrusion** — ResOpsUS + official population-accounting time series
4. **Harmless-Error → Remedy Collapse** — CourtListener/public appellate opinions with source-grounded error/harmlessness/disposition

### 先做 20-unit source-yield audit

5. **Noninferiority → Equivalence Collapse**
6. **Surrogate → Clinical-Outcome Promotion**
7. **Dissent → Holding Role Swap**

### 特殊轨道

- **Alias Entrainment Transfer (014)** — broad cross-surface phenotype 已成立；entity/reference-specific construct 未成立。下一次模型调用前必须 materialize corrected D1 r4 broad bank、ASSOC control、scope/attrition audit 与 frozen SHA。若 source 无法自然支持 Q2，直接 drop entity claim，不再缩 scope。
- **Publicness–Coordination Dissociation (013)** — `PARKED / HOLD-DATA`。现有 human paradigm 不足以提供 20 independent natural matched scenarios；不靠 paraphrase/participant swap 伪造 sample size。

### 不再占 phenomenon discovery slot

`MECH-FOLLOWUP`：

- Task-Switch TR/TL Desynchronization
- Resolved-Ambiguity Neuron Persistence
- Action-Boundary State Routing
- Predicate-Revision Eager-Flag Staleness（同时 HOLD-DATA）

`HOLD-DATA / PARKED`：

- Training-Recency Conflict Arbitration
- Correlation → Agreement / Interchangeability Promotion
- Habitual → Episode Actualization
- Competing-Event → Censoring Collapse
- Publicness–Coordination Dissociation

`TERMINAL`：

- 007 Weak-Evidence Backfire — frozen two-family smoke 已 HARD KILL。

## 一句原则

> **一个好的可解释性题，应该先有一个外部可定义、自然 source 能承载、hard gold 能裁决的反直觉现象；hidden state 是用来解释它，不是用来替它证明“题存在”。**
