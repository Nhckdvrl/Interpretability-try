# Phenomenon Miner

版本：2026-08-30  
状态：`v4 / PHENOMENON-FIRST / OFF-THE-SHELF-D0-FIRST / N0+N1+D0 BEFORE REGISTRATION`

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

完整规则看 [`FINDING_RULES.md`](FINDING_RULES.md) 与 [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md)。

最重要的四条纪律：

> **phenomenon before mechanism。** mother 已有 headline behavior、我们只剩 hidden-state fork 时，标 `MECH-FOLLOWUP`，不占新 phenomenon slot。

> **data is part of topic selection。** natural source / hard gold / independent units 做不实，与 novelty collision 一样可以直接杀题。

> **off-the-shelf D0 first。** 当前近线优先只做公开 dataset 已经提供 natural units + labels / deterministic quantities、我们只需程序化配对或切窗口的题。需要人工逐篇论文/判例拼 20+ gold units 的题先 PARK。

> **population before clean subset。** confound 靠 contrast、matching、strata 和统计控制；理论 moderator 默认 factor-not-filter。

## 当前入口

- [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) — 唯一 authoritative queue；当前近线只剩 2 个 off-the-shelf D0。
- [`DATA_REVIEW_2026-08-29.md`](DATA_REVIEW_2026-08-29.md) — 上一轮逐题 data/gold/source 复审。
- [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) — D0 scope gate。
- [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) — 唯一 model-call authorization；当前 authorized calls = 0。
- [`FAILED_TOPICS.md`](FAILED_TOPICS.md) — KILL / ROUTE / HOLD-DATA 与 anti-revival lessons。

## 当前调度

### 直接 materialize D0

1. **Mixed-Status Event Attraction**
   - source: MAVEN-FACT
   - 现成 natural documents + 112k event factuality annotations
   - builder: `../preflight/d0_mixed_status_event_attraction/build_from_maven_fact.py`
   - 工作只是 same-document mixed-status pair enumeration + source audit，不写 synthetic scenarios。

2. **Stock–Flow Correlation Intrusion**
   - source: ResOpsUS
   - 现成 daily reservoir storage/inflow/outflow records
   - builder: `../preflight/d0_stock_flow_correlation_intrusion/build_from_resopsus.py`
   - 工作只是从真实时序切 `storage/net direction != inflow trend` 的 diagnostic windows，并做 closure/unit audit。

### 暂停人工数据工程

以下五题 scientific object 可继续记着，但当前不手工抽 20+ units：

- Subgroup-Significance -> Interaction Promotion
- Harmless-Error -> Remedy Collapse
- Noninferiority -> Equivalence Collapse
- Surrogate -> Clinical-Outcome Promotion
- Dissent -> Holding Role Swap

只有发现已经结构化打包好的公开 corpus/benchmark 时再回近线。

### 特殊轨道

- **014 Alias Entrainment Transfer** — phenotype 已成立；下一次 D1 模型调用前必须先完成 corrected r4 broad bank + ASSOC + scope/attrition/source audit + frozen SHA。
- **013 Publicness–Coordination** — PARKED/HOLD-DATA，不用 paraphrase/participant swap 充独立样本。

### 不占 phenomenon slot

`MECH-FOLLOWUP`：Task-Switch TR/TL、Resolved-Ambiguity Neuron Persistence、Action-Boundary Routing、Predicate-Revision。

`HOLD-DATA`：Training-Recency、Correlation->Agreement、Habitual->Episode、Competing-Event->Censoring。

`TERMINAL`：007 Weak-Evidence Backfire。

## 一句原则

> **D0 优先从现成自然数据里切科学对照，不把“研究选题”变成“人工造 benchmark 工程”。如果一个题只有靠长期手搓 gold 才能活，当前就不做。**
