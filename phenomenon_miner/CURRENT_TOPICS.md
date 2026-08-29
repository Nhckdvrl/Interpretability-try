# Current Topics

日期：2026-08-29  
状态：`AUTHORITATIVE CURRENT TOPIC QUEUE / NOT MODEL-AUTHORIZING`

这是 `phenomenon_miner/` 中**唯一的当前选题清单**。旧 Batch 1/2/3、162-card inventory、`promoted/phenomena/candidates` 标签都不再有当前状态含义。

当前：

```yaml
continue_in_discovery: 16
legacy_continue: 2
new_discovery_pass: 0
new_model_authorization: 0
```

要真正晋级，仍需按 [`FINDING_RULES.md`](FINDING_RULES.md) 完成：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
= DISCOVERY-PASS
```

**本表的 Tier 只表示 discovery 优先级，不表示 N0/N1/D0 已经通过，更不代表允许调用模型。**

---

## Tier S — 优先补完 N1 + D0 discovery package

这 3 题当前最符合 v4 的 phenotype-first 标准：有自然 mother question、清楚的一句话矛盾、decisive contrast、结构性 wrong destination，并且第一步仍然是现象/construct 审计而不是先做机制。

| topic | 一句话 scientific object | N0 | 当前 discovery blocker |
|---|---|---|---|
| **Task-Switch TR/TL Desynchronization** | task switch 后，Task Recognition 已切到新任务但 Task Learning 仍沿用旧 mapping，或反之？ | **PASS**：task-switch behavior 与 static TR/TL decomposition 各自已有 mother，但 exact dynamic desynchronization 未被占据 | **N1**：完整审 ICLR TR/TL predecessor/successor、appendix/code，确认没有 exact task-transition decomposition；**D0**：20 switch pairs 排除 context length、label-token、task-difficulty artifact |
| **Resolved-Ambiguity Neuron Persistence** | 同一个 ambiguous question 在 resolving context 下已经唯一化后，ambiguity neuron 还编码表面歧义，还是编码当前 unresolved uncertainty？ | **PASS**：mother 用 ambiguous vs disambiguated/re-written questions，不是 `same exact Q + resolving context` | **N1**：补 citation-chain closure，确认 2026 successor 未做 AEN lifecycle/context resolution；**D0**：锁 AmbigQA/AmbigNQ exact-Q triplets，20 cases 排除 answer leakage 与 context dilution |
| **Stock–Flow Correlation Intrusion** | net flow 已算对，但 downstream stock trajectory/peak 仍追随 salient inflow 走势 | **PASS**：经典 correlation heuristic 是强自然 mother；未检索到 exact modern-LLM downstream intrusion phenotype | **N1**：深查 LLM dynamic-system / accumulation / chart-reasoning 文献；**D0**：至少 3 类自然 stock-flow 场景、20+ trajectories，并加 table/text control 排除图表读取 artifact |

### Tier S 共同纪律

- N1 必须留下 strongest 3–5 papers、mother inclusion、mechanism occupancy、scale-survival risk。
- D0 失败就删除或降级，不换 source 救题。
- 不允许因为“机制看起来很漂亮”跳过行为/construct closure。

---

## Tier A — scientific object 强，但还需一项关键 novelty/data closure

| topic | 一句话 scientific object | 当前状态 | blocker |
|---|---|---|---|
| **Subgroup-Significance → Interaction Promotion** | A subgroup 显著、B 不显著且 interaction 不显著，模型仍宣称 subgroup effect 不同 | `N0-PASS / HOLD-N1+D0` | 深查 LLM statistical-reasoning/p-value fallacy literature；20 RCTs 核对同一 endpoint/subgroup/timepoint，gold 必须是“无充分 interaction 证据”，不能误写成“effects equal” |
| **Mixed-Status Event Attraction** | 两个 event factuality 分别判断正确，组合后是否发生有方向的 status pooling/attraction | `N0-PASS / HOLD-N1+D0` | N1 排除更宽 contextual-status aggregation；D0 用 MAVEN-FACT 自然同 discourse event pairs，不能 random concatenate 两个 unrelated events |
| **Noninferiority → Equivalence Collapse** | one-sided NI relation 已读对，downstream summary 是否被对称化成 equivalence | `N0-PASS-WITH-WARNING / HOLD-N1+D0` | 第一优先深审 CliniFact confusion/claim-type analysis；若 NI→equivalence 已是其主 finding，直接 KILL/ROUTE。D0 需 20 neutral true-NI trials + exact design/result provenance |
| **Correlation → Agreement / Interchangeability Promotion** | 模型明知高 correlation 但 absolute agreement 差，仍说两种 measurement 可互换 | `N0-PASS / HOLD-N1+D0` | 至少两个应用域、20+ units；“interchangeable”必须有外部冻结 hard gold（Bland–Altman/CCC/ICC 与预先声明 margin），不能由研究者主观判 |
| **Action-Boundary State Routing** | EBP 改善 boundary behavior，是读出默认已有 boundary representation，还是在前向中创建/强化它？ | `MECH-FOLLOWUP / HOLD-N1+D0` | mother behavior 已经成立，因此不作为新 phenotype 题；完整审 mother appendix/code 是否已有 boundary representation probing/causal routing。若已有 exact fork，KILL-COLLISION |

---

## Construct-validation / existing active project

### Alias Entrainment Transfer

`active/014_alias_entrainment_transfer` 不再被列为“干净 Tier S 新题”。它是一个**已有行为 phenotype、但 construct 解释尚未闭合的 active 特例**。

当前 authoritative reading：

```text
N0 breadth: PASS
N1 depth: NOT PERFORMED (owner waiver, 2026-08-29)
v4 D0 source-feasibility: NOT PERFORMED (owner waiver)
behavior phenotype: survives strongly
entity-level interpretation: NOT EARNED
```

150-pair audit 已发现：compositional 39%、genuine coref_conventional 33%、5% not_coreferent；旧 UNREL builder 有 bug；`ALIAS > SEMREL` 不能排除 pair-specific learned association。Phase 3 又表明 entrainment heads 的 direct write 是 seen-form/lexical，而不是直接写 unseen alias。

**唯一允许的下一步**是已冻结 D1 construct validation：RedirectQA + strongly-associated non-coreferent `ASSOC`，判据 `ALIAS > ASSOC`。若失败，放弃 entity interpretation，不再扩机制故事。

---

## Tier B / HOLD-DISCOVERY — scientific object 仍活，但 blocker 更重

| topic | 为什么还留 | 必须解决后才能晋级 |
|---|---|---|
| **Predicate-Revision Eager-Flag Staleness** | mother filtering work 提供 eager flag / late filter 两种实现，revision question 有意义 | **降级**：先做 N1，确认 predicate update / composition / state revision 没在 mother/successor 被覆盖；20 Wikidata natural-list audit 证明不是玩具 predicate prompt |
| **Training-Recency Conflict Arbitration** | training-time recency metadata 是真 object，冲突选择是否读取它仍未回答 | **降级**：headline 容易退化成“metadata causal 吗”；必须先证明 conflict phenotype 独立重要。D0 需 exposure-balanced conflict 且两条 fact isolation 都 retained |
| **Habitual → Episode Actualization** | generic/habitual 与 episodic occurrence 是真实语义边界 | 20 natural samples 必须证明 dated downstream query 没引入“默认发生一次”的语用 artifact；N1 需排除 event-actuality mother work |
| **Surrogate → Clinical-Outcome Promotion** | endpoint role × validation/context-of-use → allowable claim 是真实决策 gate | 成功链接 >=20 trial → exact FDA surrogate/context-of-use → target outcome；不能把所有 surrogate 一律标成“不支持 clinical benefit” |
| **Harmless-Error → Remedy Collapse** | error finding 与 remedy entitlement 在法律上是明确分离的 operator | 从 COLD/公开判例找到 >=20 同时明确 `error + harmless/no prejudice + disposition/remedy` 的 hard-gold opinions；不能靠主观标注 prejudice |
| **Competing-Event → Censoring Collapse** | event role → survival risk-set transition 有 deterministic oracle | >=20 natural competing-risk units，并先证明强模型具备基础 competing-risk/censoring 能力，否则只是专业知识测试 |
| **Dissent → Holding Role Swap** | majority/dissent proposition 与 controlling role 的 binding 是真实结构 | 必须找到可外部冻结的 holding proposition；若仍需研究者自己摘要 holding，继续 HOLD |

---

## Removed from current high-priority queue after 2026-08-29 N0/N1/D0 re-audit

以下 3 题不再占用当前 discovery 资源；具体理由同步写入 [`FAILED_TOPICS.md`](FAILED_TOPICS.md)。

| topic | verdict | 原因 |
|---|---|---|
| **GeoTemporal Binding Bottleneck** | `ROUTE → MOTHER-MECHANISM-FOLLOWUP` | GeoTemp mother 已经直接建立“geography/time components individually work but composition fails”的 headline；剩余 retrieval/arithmetic/binding localization 是 mother 的 mechanism decomposition，不再有独立 phenotype budget |
| **Causal Retrieval Schedule** | `ROUTE → TARGETED-MECH-FOLLOWUP` | mother 已有 future retrieval-schedule predictive state；剩余问题主要是 correlation→causal-plan validation。它不提供独立自然 behavioral phenotype/D0，且与内部 Topic 15 的“predictive state formed but not used”失败模式高度同型 |
| **Dead-Branch Residue after Invalidation** | `KILL/ROUTE-STANDALONE` | Belief revision / stale premise / stale memory→policy adaptation 邻域已直接占据“新证据使旧 state 失效但 downstream 行为继续沿旧 state”的 mother question；仅把 state 换成 planning branch 不足以形成独立 headline |

---

## Legacy continuing projects

这些是 v4 前已经存在的 project，不重新伪装成新流程 `DISCOVERY-PASS`。

| project | status | next meaning |
|---|---|---|
| `active/007_weak_evidence_backfire` | legacy `D0-PASS / READY-TO-SMOKE` | 当前 frozen 30-case contract authorized；按旧 lineage 执行，除非 claim 改变或出现具体新 collision，否则不补 routine post-smoke N1 |
| `active/013_publicness_coordination_dissociation` | legacy `N0-PASS / HOLD-D0` | scientific question 仍活，但自然独立 scenario 数与 adaptation/license blocker 未解；不得用 participant swap/paraphrase/payoff variant 伪造独立样本 |

`active/003_diagnostic_counterevidence_revision` 仍是 legacy pre-candidate，不属于当前 discovery survivors，也没有模型授权。

---

## 调度纪律

- **本文件只回答“现在值得继续查哪些题”。**
- 新题在完成 N0 + N1 + D0 source-feasibility 前不得创建新的 active project。
- 任一题的 >=20 feasibility audit 失败，直接从本表删除或降级，不通过换数据源救题。
- 已有 mother behavior + 一个很酷的 mechanism question，不自动等于新 phenomenon candidate；必要时单列 `MECH-FOLLOWUP`。
- `Tier S/A/B`、`survivor`、旧 `promoted` 标签都不代表模型授权。
- 真正的模型调用权限只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。
- 被移出的题及死亡原因统一看 [`FAILED_TOPICS.md`](FAILED_TOPICS.md)。
