# Current Topics

日期：2026-08-29  
状态：`AUTHORITATIVE CURRENT TOPIC QUEUE / NOT MODEL-AUTHORIZING`

这是 `phenomenon_miner/` 中**唯一的当前选题清单**。旧 Batch 1/2/3、162-card inventory、`promoted/phenomena/candidates` 标签都不再有当前状态含义。

当前：

```yaml
continue_in_discovery: 19
legacy_continue: 2
new_discovery_pass: 0
new_model_authorization: 0
```

要真正晋级，仍需按 [`FINDING_RULES.md`](FINDING_RULES.md) 完成 N1 closure + exact source/version/license + >=20 real-source feasibility audit。

---

## Tier S — 优先完成 discovery package

这 7 题目前同时具备最清楚的科学问题、novelty 边界和自然数据路径。

| topic | 一句话 scientific object | 数据路径 | 当前唯一 blocker |
|---|---|---|---|
| **Alias Entrainment Transfer** | context 只出现 alias A，未出现的同实体 alias B 会不会也被 entrain？ | Wikidata CC0 entity IDs + 真实 labels/aliases；exact-target / alias-only / semantic-related / unrelated 四路对照 | 20 对人工检查 alias conventionality、歧义与频率分层；禁止自造缩写 |
| **Task-Switch TR/TL Desynchronization** | task switch 后 Task Recognition 已切换但 Task Learning 仍沿用旧 mapping，或反之？ | EMNLP 2024 task-switch repo + ICLR 2026 TR/TL repo 的共同 ICL classification 子集 | 20 switch pairs 排除 context length / label-token artifact；确认 appendix/code 未做过 exact decomposition |
| **GeoTemporal Binding Bottleneck** | geography 与时间算术分别会，joint 失败到底卡在 retrieval、arithmetic 还是 binding？ | GeoTemp CC BY 4.0；同一 item 派生 geography-only / arithmetic-only / joint | 20 joint cases 审计 component view 没改变语义 |
| **Causal Retrieval Schedule** | 当前 hidden state 对未来 retrieval-head schedule 的预测信号是不是 causal plan？ | mother Needle/multi-hop setup + HotpotQA-style support chains | 20 matched chains 做 content-preservation audit；确认母论文没有 pre-activation causal schedule intervention |
| **Correlation → Agreement / Interchangeability Promotion** | 模型明知高 correlation 但 absolute agreement 差，仍说两种 measurement 可互换？ | 真实 paired measurement data；Pearson/Spearman + Bland–Altman/CCC/ICC 本地 oracle | 至少两个应用域、20+ units；“interchangeable”判断必须有明确 hard gold |
| **Subgroup-Significance → Interaction Promotion** | A 显著、B 不显著且 interaction 不显著，模型仍宣称 subgroup effect 不同？ | 公开 RCT subgroup reporting data + interaction tests/claims | 20 trials 核对同一 endpoint/subgroup/timepoint |
| **Stock–Flow Correlation Intrusion** | net flow 已算对，stock trajectory/peak 仍追随 salient inflow 走势？ | Department Store/Bathtub/queue/inventory/reservoir 自然 stock-flow materials；`S_{t+1}=S_t+I_t-O_t` oracle | 20 natural trajectories，至少三类现实场景，不能只复制一种图 |

---

## Tier A — 问题成立，还有一个明确 discovery closure

| topic | 一句话 scientific object | 数据路径 | blocker |
|---|---|---|---|
| **Predicate-Revision Eager-Flag Staleness** | predicate P 先触发 eager flags，随后改成 Q，模型能否迁移到新实现并清掉旧 flags？ | mother filtering tasks + Wikidata natural entity lists/attributes | 20 Wikidata natural-list audit，证明不是玩具 predicate prompt |
| **Training-Recency Conflict Arbitration** | training-order recency direction 是可读 metadata，还是 conflict 时真正的 priority signal？ | `Fresh in memory` training recipe + Wikidata relation triples | 冻结 exposure-balanced conflicts，并证明两条 fact isolation 都 retained |
| **Resolved-Ambiguity Neuron Persistence** | ambiguity neuron 编码表面歧义，还是当前 unresolved ambiguity？ | AmbigQA/AmbigNQ + same exact question / resolving context | 先闭合 reuse/license；20 cases 排除 context-length/attention dilution |
| **Dead-Branch Residue after Invalidation** | 原本 valid 的 planning branch 被 state update 关闭后，是被退休、抑制还是继续污染行动？ | ALFWorld MIT + PDDL/game state/admissible commands | 20 goal-preserving minimal branch closures；排除 generic stale-text effect |
| **Mixed-Status Event Attraction** | 两个 event factuality 分别判断正确，组合后是否发生有方向的 status pooling？ | MAVEN-FACT event factuality + arguments/relations/evidence | 20 natural event pairs；确认 directional attraction 而非 context parsing |
| **Habitual → Episode Actualization** | 模型知道 habitual/generic 不蕴含具体 occurrence，却在 timeline/memory 中凭空创建 episode token？ | UDS/Decomp genericity 等自然 habitual/generic sentences | 20 samples 证明 downstream dated query 没引入“默认发生一次”的语用 artifact |
| **Noninferiority → Equivalence Collapse** | one-sided NI relation 已读对，downstream summary 是否被对称化成 equivalence？ | CliniFact 作为 locator → ClinicalTrials.gov/PubMed true-NI trials | 20 neutral true-NI trials；专查 MedLitSpin/clinical-claim work 是否已覆盖 exact phenotype |

---

## Tier B / HOLD-DISCOVERY — scientific object 仍活，但 blocker 更重

| topic | 为什么还留 | 必须解决后才能晋级 |
|---|---|---|
| **Surrogate → Clinical-Outcome Promotion** | endpoint role × validation/context-of-use → allowable claim 是真实决策 gate | 成功链接 >=20 trial → exact FDA surrogate/context-of-use → target outcome；不能把所有 surrogate 一律标成“不支持 clinical benefit” |
| **Harmless-Error → Remedy Collapse** | error finding 与 remedy entitlement 在法律上是明确分离的 operator | 从 COLD/公开判例找到 >=20 同时明确 `error + harmless/no prejudice + disposition/remedy` 的 hard-gold opinions；不能靠主观标注 prejudice |
| **Competing-Event → Censoring Collapse** | event role → survival risk-set transition 有 deterministic oracle | >=20 natural competing-risk units，并先证明强模型具备基础 competing-risk/censoring 能力，否则只是专业知识测试 |
| **Dissent → Holding Role Swap** | majority/dissent proposition 与 controlling role 的 binding 是真实结构 | 必须找到可外部冻结的 holding proposition；若仍需研究者自己摘要 holding，继续 HOLD |
| **Action-Boundary State Routing** | mother behavior 很自然，representation-exists-but-not-routed vs EBP-creates-representation 是有意义 fork | 先完整审 mother appendix/code；若已经做 boundary representation probing/causal routing，直接 KILL-COLLISION |

---

## Legacy continuing projects

这些是 v4 前已经存在的 project，不重新伪装成新流程 `DISCOVERY-PASS`。

| project | status | next meaning |
|---|---|---|
| `active/007_weak_evidence_backfire` | legacy `D0-PASS / READY-TO-SMOKE` | 当前唯一 authorized smoke；只按冻结 30-case contract 运行 |
| `active/013_publicness_coordination_dissociation` | legacy `HOLD-D0` | scientific question 仍活，但自然独立 scenario 数与 adaptation/license blocker 未解 |

`active/003_diagnostic_counterevidence_revision` 仍是 legacy pre-candidate，不属于这 19 个 discovery survivors，也没有模型授权。

---

## 调度纪律

- **本文件只回答“现在值得继续查哪些题”。**
- 新题在完成 discovery package 前不得创建新的 active project。
- 任一题的 >=20 feasibility audit 失败，直接从本表删除或降级，不通过换数据源救题。
- 真正的模型调用权限只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。
- 被移出的题及死亡原因统一看 [`FAILED_TOPICS.md`](FAILED_TOPICS.md)。
