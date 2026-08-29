# Current Topics

日期：2026-08-30  
状态：`AUTHORITATIVE CURRENT TOPIC QUEUE / OFF-THE-SHELF-D0-FIRST / NOT MODEL-AUTHORIZING`

这是 `phenomenon_miner/` 中**唯一的当前 phenomenon discovery 清单**。旧 Batch 1/2/3、162-card inventory、历史 `promoted/phenomena/candidates` 标签都不再有当前状态含义。

最新调度原则进一步收紧：

> **近线 D0 默认只做“公开 dataset 已经提供 natural units + source labels / deterministic quantities，我们最多程序化抽样、配对、切窗口”的题。**
>
> 需要人工逐篇论文、逐个判例、跨多个数据库手工拼 20+ gold units 的题，即使 scientific question 不差，也先 PARK，不与低成本 phenomenon discovery 抢时间。

当前状态：

```yaml
near_term_off_the_shelf_d0: 2
manual_extraction_parked: 5
active_construct_validation: 1
mechanism_followups_or_routed: 4
other_hold_data_or_parked: 5
new_discovery_pass: 0
new_model_authorization: 0
```

真正晋级仍需：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
  + dataset scope-integrity PASS
= DISCOVERY-PASS
```

模型调用只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。

---

## Tier S — 只保留两个“现成 dataset -> 程序化 D0”题

### 1. Mixed-Status Event Attraction

**Phenotype**：两个 event 的 factuality 单独判断都对，但在同一自然 discourse 中联合出现后，是否发生有方向的 status pooling / attraction？

**现成数据**：MAVEN-FACT。数据本身已经提供自然文档、event mentions、event type、sentence position 和 `CT+ / PS+ / PS- / CT- / Uu` factuality labels；不需要自造 scenario 或人工写 gold。

**D0 只做程序化抽取**：

```text
same MAVEN-FACT document
-> flatten source-annotated event mentions
-> enumerate different-factuality event pairs
-> keep factuality direction / sentence distance / event type as factors
-> deterministic source-audit sample
```

Builder 已放到：

`preflight/d0_mixed_status_event_attraction/build_from_maven_fact.py`

它输出 `raw_mentions.jsonl`、`eligible_pairs.jsonl`、`audit_sample.jsonl`、`scope_summary.json` 和 `AUDIT_SAMPLE.md`，不调用模型。

**D0 blocker**：运行 builder 后人工看 >=20 source pairs，确认 mention/label/context 没有 annotation leakage；再看自然 same-document decisive pairs 的数量与覆盖。若 source bank 本身不够，不换 synthetic source 救题。

### 2. Stock-Flow Correlation Intrusion

**Phenotype**：模型已经正确处理 `inflow - outflow` 的 net direction，但 downstream stock trajectory / peak 仍错误追随显眼的 inflow 走势。

**现成数据**：ResOpsUS。官方数据已经提供大量真实 reservoir 的 daily storage、inflow、outflow（以及部分 evaporation/elevation）；不需要写玩具水箱题。

**D0 只做程序化切自然窗口**：

```text
official daily reservoir time series
-> observed storage delta
-> cumulative inflow-outflow
-> retain windows where storage/net agree but inflow trend points opposite
-> keep reservoir/direction/closure/unit as factors
```

Builder 已放到：

`preflight/d0_stock_flow_correlation_intrusion/build_from_resopsus.py`

它要求本地已解压的官方 ResOpsUS archive，自动扫描 CSV、保留所有 schema-valid source files、做 accounting/closure validity check，并生成 `eligible_windows.jsonl`、audit sample 和 scope summary。它不生成 synthetic tank stories。

**D0 blocker**：实际 source audit 必须确认 agency-specific columns/units 没被误识别，而且 qualifying windows 不是 missing-data/closure artifact。

---

## PARKED — 科学问题可能不错，但当前数据工程不值

下面五题**不再是近线 D0**。共同原因不是 novelty 已死，而是目前需要大量人工抽取 / cross-source linking；这不符合当前快速 phenomenon mining 的成本纪律。

| topic | verdict | 为什么先 park |
|---|---|---|
| **Subgroup-Significance -> Interaction Promotion** | `PARK-MANUAL-DATA` | 需要逐篇 open-access RCT 对齐同 endpoint/subgroup/timepoint，并人工核 `P for interaction` / interaction CI；统计 gold 硬，但数据工程重 |
| **Harmless-Error -> Remedy Collapse** | `PARK-MANUAL-DATA` | 需要逐案抽 error finding、harmlessness analysis、final disposition，还要排除其他 reversible grounds |
| **Noninferiority -> Equivalence Collapse** | `PARK-MANUAL-DATA` | 需要逐篇 NI RCT 恢复 margin、effect orientation、CI；不能只读作者 prose |
| **Surrogate -> Clinical-Outcome Promotion** | `PARK-MANUAL-DATA` | 需要 trial -> exact FDA surrogate/context-of-use -> target outcome 的跨源链接 |
| **Dissent -> Holding Role Swap** | `PARK-MANUAL-DATA` | role metadata 容易，但 source-grounded conflicting proposition / holding pair 通常仍要人工抽取 |

若未来找到**已经打包好上述结构的公开 benchmark / structured corpus**，可重新进入 Tier S；否则不花当前时间手搓 20–100 个 units。

---

## Active construct-validation — 014 Alias Entrainment Transfer

`active/014_alias_entrainment_transfer` 的 broad cross-surface phenotype 已经成立；当前未闭合的是 construct，不是“有没有现象”。

当前可支持：

```text
contextual entrainment can transfer across learned surface-form relations
```

当前不能支持：

```text
this transfer is specifically an entity/reference-level salience representation
```

唯一下一步仍是 D1 r4 broad-scope construct validation：RedirectQA broad surface population + `ASSOC_ANY` strong-associated non-coreferent control。任何新 D1 model call 前必须 materialize r4 bank、完成 scope/attrition/source audit 并冻结新 SHA。若 reference-specific Q2 只能靠再次疯狂筛数据才能形成，直接放弃 entity claim。

---

## Routed -> MECH-FOLLOWUP

| topic | verdict | 原因 |
|---|---|---|
| **Task-Switch TR/TL Desynchronization** | `MECH-FOLLOWUP` | mother 已有 task-switch behavior；TR/TL desync 本身由 hidden decomposition 定义 |
| **Resolved-Ambiguity Neuron Persistence** | `MECH-FOLLOWUP` | source data 好，但当前 headline 是 neuron lifecycle；只有先出现 output-only resolution-lag phenotype 才回 discovery |
| **Action-Boundary State Routing** | `MECH-FOLLOWUP` | mother behavior 已成立，剩余是 read-vs-create boundary state |
| **Predicate-Revision Eager-Flag Staleness** | `MECH-FOLLOWUP / HOLD-DATA` | implementation fork 漂亮，但自然 revision phenotype/source 尚未建立 |

---

## Other HOLD-DATA / PARKED

| topic | verdict | 当前问题 |
|---|---|---|
| **Training-Recency Conflict Arbitration** | `ROUTE / HOLD-DATA` | exposure-balanced real training history 很难自然冻结，且 headline 易退化成 `metadata causal?` |
| **Correlation -> Agreement / Interchangeability Promotion** | `HOLD-DATA` | 缺跨领域统一 hard gold；需要 source-declared agreement margin |
| **Habitual -> Episode Actualization** | `HOLD-DATA` | natural habitual labels 有，但 episode actuality 通常没有独立 gold |
| **Competing-Event -> Censoring Collapse** | `HOLD-DATA / CAPABILITY-RISK` | operator 硬，但自然 NLP source + base statistical competence 都太重 |
| **Publicness-Coordination Dissociation (legacy 013)** | `PARKED / HOLD-DATA` | 现有人类 paradigm 不能给 >=20 independent matched natural scenarios；不拿 paraphrase/participant swap 充数 |

---

## Terminal correction

### 007 Weak-Evidence Backfire — HARD KILL

正式 two-family smoke 已证伪当前 operationalization：Qwen 无 recognition-gated denominator；Gemma 仅 1 gated pair 且方向相反。不得继续扩大 panel / 换阈值 / 换 subset。

---

## 当前调度

```text
1. 直接 materialize MAVEN-FACT mixed-status D0
2. 直接 materialize ResOpsUS stock-flow D0
3. 两者谁先通过 source/scope audit，谁先补 N1 closure
4. 手工抽论文/判例的五题全部 park
5. hidden-state-defined 题只作为 mechanism follow-up，不和 phenomenon discovery 抢 slot
```

一句纪律：

> **D0 不是“我们自己写一批看起来合理的题”。优先从已经存在的公开自然数据中把科学对照切出来；如果一个题必须长期靠人工造 gold 才能活，当前就不值得做。**
