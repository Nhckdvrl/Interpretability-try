# Current Topics

日期：2026-08-29  
状态：`AUTHORITATIVE CURRENT TOPIC QUEUE / DATA-FIRST RE-AUDITED / NOT MODEL-AUTHORIZING`

这是 `phenomenon_miner/` 中**唯一的当前 phenomenon discovery 清单**。旧 Batch 1/2/3、162-card inventory、历史 `promoted/phenomena/candidates` 标签都不再有当前状态含义。

2026-08-29 晚间依据 [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) 对现有题重新做 data-first 审查后，当前状态为：

```yaml
phenomenon_discovery: 7
near_term_d0_build: 4
manual_source_audit_first: 3
active_construct_validation: 1
mechanism_followups_or_routed: 4
hold_data_or_parked: 5
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

**Tier 只表示 discovery / data 优先级，不表示模型授权。** 模型调用只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。

完整数据复审见 [`DATA_REVIEW_2026-08-29.md`](DATA_REVIEW_2026-08-29.md)。

---

## Tier S — 现在最值得投入 D0 数据工作的 4 题

这四题都能在 hidden state 之前定义一个独立、自然、可冻结的 phenotype，并已有相对明确的自然 source + 外部/确定性 gold 路径。

| topic | 一句话 scientific object | data path | 当前 blocker |
|---|---|---|---|
| **Mixed-Status Event Attraction** | 两个 event 的 factuality 单独判断都对，放进同一 discourse 后是否发生有方向的 status pooling / attraction？ | **MAVEN-FACT**：自然 document 内 event mentions + factuality labels；只采同文档 mixed-status pairs，document-clustered | D0：审 20+ same-document pairs；确认 pair count、距离/关系覆盖与 prompt 不泄漏 annotation |
| **Subgroup-Significance → Interaction Promotion** | A subgroup 显著、B 不显著且 interaction 不显著，模型是否仍宣称 subgroup treatment effects 不同？ | **开放获取 RCT**：显式 subgroup estimates + `P for interaction` / interaction CI；gold 是“没有充分 interaction evidence”，不是“effects equal” | D0：20+ 独立 trials，锁同 endpoint/subgroup/timepoint；人工双审 provenance |
| **Stock–Flow Correlation Intrusion** | net flow 已算对，但 downstream stock trajectory / peak 是否仍追随 salient inflow 走势？ | **ResOpsUS reservoirs + official population accounting**：真实 stock/inflow/outflow/birth/death/migration time series，可由 balance equation 外部计算 gold | D0：两类 source family 各审自然 windows；要求 source accounting 可闭合；table/text 先行，chart 仅作 modality factor |
| **Harmless-Error → Remedy Collapse** | 模型认出 legal error 且认出 harmless/no prejudice 后，是否仍把 error 推成 reversal/new trial/remedy entitlement？ | **CourtListener / public appellate opinions**：冻结 error finding、harmlessness analysis、final disposition 三个 source spans | D0：20+ 独立 cases；排除存在其他独立 reversible ground 的案件；标准类型只做 factor 不硬过滤 |

### Tier S 的共同数据纪律

- 先冻结 natural scientific population，再构建 matched/control bank。
- 不能用 synthetic story 代替自然行为锚点。
- 不能为了得到“干净 money cell”把 domain、direction、difficulty、relation type 等理论 factor 从 builder 中删掉。
- 20-example source audit 失败就降级/删除，不换 source 续命。

---

## Tier A — 科学问题仍好，但先做 20-unit source-yield audit

| topic | 为什么保留 | data/gold blocker |
|---|---|---|
| **Noninferiority → Equivalence Collapse** | one-sided NI 与 two-sided equivalence / no-difference 是真实且重要的语义/决策边界 | 需 20+ open-access NI RCT，显式 margin + effect CI；gold 从 margin/CI 算，不用作者松散 prose；orientation 不可恢复就 validity-exclude |
| **Surrogate → Clinical-Outcome Promotion** | surrogate endpoint role × validation/context-of-use 决定 allowable clinical claim，是自然决策 gate | 需 20+ exact tuples：trial result → exact FDA surrogate/context-of-use → target clinical outcome；不能把 surrogate 一律标成“不支持 benefit” |
| **Dissent → Holding Role Swap** | local proposition 内容与 controlling legal role 是自然可分离结构，wrong destination 很清楚 | 需 20+ opinions，prefer source-authored syllabus/`Held:` anchor + opinion-role metadata；若 holding 只能研究者自己摘要则不进 D0 |

这三题在 source-yield audit 过关之前，不进入正式 builder。

---

## Active construct-validation — 不与新题竞争 slot

### 014 Alias Entrainment Transfer

`active/014_alias_entrainment_transfer` 的 broad cross-surface phenotype 已经成立；当前未闭合的是**construct**，不是“有没有现象”。

当前可支持的 reading：

```text
contextual entrainment can transfer across learned surface-form relations
```

当前**不能**支持：

```text
this transfer is specifically an entity/reference-level salience representation
```

原因：150-pair audit 显示旧 bank 中 compositional 39%、真正 conventional coreference 仅 33%、5% outright non-coreferent；旧 UNREL builder 有 bug；`ALIAS > SEMREL` 不能排除 pair-specific learned association。Phase 3 又显示 entrainment heads 的 direct write 是 seen-form / lexical。

唯一下一步是已冻结的 **D1 r4 broad scope construct validation**：

- RedirectQA broad surface population；
- all entity types；
- both valid directions；
- surface relation/type/direction 为 factor-not-filter；
- `ASSOC_ANY` = 强关联但不同 referent 的 primary control；
- broad Q1：`ALIAS > ASSOC_ANY`；
- reference-specific Q2：hard-identity-gated `opaque_strict` 上仍 `ALIAS > ASSOC_ANY`。

**在任何新 D1 model call 前必须先 materialize r4 bank、完成 scope/attrition summary + source/ASSOC audit + frozen SHA。** 若 Q2 的 60-entity capability stratum 无法在不继续 convenience-filter 的情况下自然形成，直接放弃 entity/reference-specific claim，不再缩窄 population。

---

## Routed → MECH-FOLLOWUP，不再占 phenomenon queue

| topic | verdict | 原因 |
|---|---|---|
| **Task-Switch TR/TL Desynchronization** | `ROUTE → MECH-FOLLOWUP` | mother 已建立 task-switch external behavior；当前 headline 直接由 TR/TL hidden decomposition 定义。只有先找到 output-only 的 old-task-mapping intrusion 等独立 wrong-destination phenotype 才可重做 phenomenon N0 |
| **Resolved-Ambiguity Neuron Persistence** | `ROUTE → MECH-FOLLOWUP` | AmbigQA/AmbigNQ data 很好，但当前问题是 AEN 在 context resolution 后编码什么，属于 representation lifecycle；若先发现“已唯一化且模型能复述解释，却仍持续 clarify/hedge/multi-sense answer”的 resolution-lag phenotype，才可重返 discovery |
| **Action-Boundary State Routing** | `ROUTE → MECH-FOLLOWUP` | mother behavior 已成立，剩余 fork 是 EBP 读出现有 boundary state 还是创建/强化它 |
| **Predicate-Revision Eager-Flag Staleness** | `ROUTE / HOLD-DATA` | 当前 novelty 主要是 eager-flag vs late-filter implementation switch；自然 list/predicate revision source 尚未建立，不能用 constructed toy prompt 充当新现象 |

---

## HOLD-DATA / PARKED — 暂不投入当前 discovery 资源

| topic | verdict | 当前问题 |
|---|---|---|
| **Training-Recency Conflict Arbitration** | `ROUTE / HOLD-DATA` | headline 容易退化成 `metadata causal?`；真实 exposure-balanced conflict history 很难自然冻结，属于内部 archive 已警告的 identification 型题 |
| **Correlation → Agreement / Interchangeability Promotion** | `HOLD-DATA` | `interchangeable` 没有跨领域统一 hard gold；需要 source-declared acceptable-difference margin / agreement standard，不能只凭高 r + wide Bland–Altman 主观标 |
| **Habitual → Episode Actualization** | `HOLD-DATA` | natural generic/habitual corpora 有，但 dated episode actuality 通常没有独立 annotation；构造 dated query 本身会引入要研究的语用推断 |
| **Competing-Event → Censoring Collapse** | `HOLD-DATA / CAPABILITY-RISK` | 统计 operator deterministic，但自然 NLP source/gold 弱且专业能力门槛高；需先证明 event type + risk-set transition 都能 source-ground |
| **Publicness–Coordination Dissociation (legacy 013)** | `PARKED / HOLD-DATA` | N0 仍有价值，但现有 human paradigm 无法在 clean license/adaptation path 下给 >=20 independent matched scenarios；participant swap/paraphrase/payoff variant 不算新 unit |

---

## Terminal / stale correction

### 007 Weak-Evidence Backfire — HARD KILL

已完成 frozen two-family smoke：

- Qwen3-8B：`0` recognition-gated directions；
- Gemma3-12B-IT：仅 `1` gated pair，且 belief/action movement 为反方向；
- strong-pair / pragmatic / matched-length / bidirectional survival 均失败。

正式 verdict：`HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`。不跑 N1、mechanism 或扩大 panel，不通过换阈值/模型/子集复活。

`active/003_diagnostic_counterevidence_revision` 继续只是 legacy pre-candidate，不属于当前 survivor queue。

---

## 当前调度顺序

按“每单位数据工作能获得的信息量”排序：

1. **Mixed-Status Event Attraction**
2. **Subgroup-Significance → Interaction Promotion**
3. **Stock–Flow Correlation Intrusion**
4. **Harmless-Error → Remedy Collapse**
5. **Noninferiority → Equivalence Collapse**
6. **Surrogate → Clinical-Outcome Promotion**
7. **Dissent → Holding Role Swap**

近期开 builder 只优先考虑前四；5–7 先完成 20-unit manual source-yield audit。

---

## 一句纪律

> **Novelty 过关不等于题过关。自然 source population、外部 hard gold 和 scope integrity 本身就是选题的一部分；数据必须承载原 mother question，而不是把它越筛越窄。**
