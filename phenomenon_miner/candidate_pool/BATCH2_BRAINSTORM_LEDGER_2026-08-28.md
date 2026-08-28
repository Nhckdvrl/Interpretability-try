# 第二批找题脑暴账本（2026-08-28）

状态：`DISCOVERY IN PROGRESS / 9 CURRENT SURVIVORS / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
final_batch2_count: 9
final_target_count: 10
```

本文件记录**第二批新的十题**的完整找题过程：不是只保存最后幸存者，也保存被 exact collision、母命题包含、仓库内部重复、自然数据不足或机制空间不足杀掉的主题。目的之一是防止以后把死亡主题换一个名字重新投入。

第一批十题在 [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md)；本批不得用第一批题补数。

本批详细的 adversarial / independent-style N0 工作稿见 [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)。

---

## 1. 本批搜索纪律

每个想法按以下顺序处理：

1. **自然母现象。** 先问这个问题在人类认知、法律、科学推断、程序语义、真实工作流或公共数据中是否本来就成立，而不是为 LLM 拼 prompt。
2. **仓库内部去重。** 对照 162 张历史卡与 F1–F9 母族；若只是 setting replacement，直接 ROUTE/KILL。
3. **exact / near-exact 检索。** ACL/EMNLP/NAACL 为主，ICLR/ICML/NeurIPS 与同期 arXiv/ARR 为补充；搜索同义词、老术语、benchmark 与 appendix 变量。
4. **mother-inclusion attack。** 即使 exact title 不同，也问已有工作是否已经逻辑上覆盖相同行为、controls、错误目的地与机制解释。
5. **`why_not_a_rename`。** 只有能指出独立 operator / decisive contrast，且理由不是“数据不同、领域不同、readout 不同”时才留。
6. **D0 预审。** relation/gold 必须有外部规范、执行 oracle、专家任务或自然数据可冻结；纯模板效应不占十强。

本文件的 `SURVIVE-TO-N0` 仍然不是仓库流程意义上的正式 `N0-PASS`，也不授权跑模型。

---

## 2. 当前 9 个第二批 survivor

这 9 个只是当前已经通过本轮 proposer-side 对抗筛的 finalist；第 10 个尚未找到同等级题，因此**不降低门槛凑数**。

| # | 题目 | 一句话 decisive contrast | 当前理由 |
|---:|---|---|---|
| 1 | **Burden-Placement Null-Case Reversal** | 证据对关键事实保持 unresolved；模型正确识别谁负举证责任，却在相同未决事实下给双方同一个默认结论 | burden-of-proof 是独立 default operator，不是一般 confidence threshold |
| 2 | **Appellate-Deference Override** | 模型正确识别 `de novo` 与 deferential review 标准，也能判断下级结论是否“自己会不同意”；最终是否可替代下级判断却不随 review standard 变化 | review-standard→remedy 是制度化 decision operator，不等于普通 authority bias |
| 3 | **Short-Circuit Side-Effect Leakage** | 模型正确知道 `A || B` / `A && B` 已在左侧决定返回值，也正确说 RHS 不执行；预测世界状态时却加入 RHS 副作用 | value path 与 effect path 的短路 gate 可严格由执行 oracle 验证 |
| 4 | **Retrieval-Practice-Induced Forgetting** | 两个相关事实原本都可回忆；主动反复检索其中一个后，另一个被选择性压低，而单纯重复阅读不产生同型损失 | testing/retrieval operation 对竞争记忆的选择性抑制，不是 fan effect 或普通 context interference |
| 5 | **Noninferiority → Equivalence Collapse** | 模型正确解释 noninferiority 只排除“差得超过界值”，却把 NI success 写成“两个处理等效” | one-sided relation 被非法提升成 two-sided equivalence；规范关系可由试验设计冻结 |
| 6 | **Surrogate → Clinical-Outcome Promotion** | 模型正确说 surrogate endpoint 改善不自动证明患者真正获益，摘要/建议仍把 surrogate success 写成 clinical benefit | surrogate-validation gate 是关系类型转换，不是一般相关≠因果口号 |
| 7 | **Harmless-Error → Remedy Collapse** | 模型正确识别法律错误已发生，也正确识别 harmless/prejudicial 标准，最终却把 `error=true` 直接映射为必须 reversal/remedy | error existence 与 remedy entitlement 是两个正式法律算子 |
| 8 | **Composite → Component Benefit Projection** | 模型正确知道 composite endpoint 由多个 component 组成、总体显著可能由单一 component 驱动，却把 composite benefit 广播到未改善 component | set/composite→member projection 有明确 component-level gold；必须区别于普通 F6 sum/count |
| 9 | **SQL UNKNOWN Interface Collapse** | predicate truth value 正确算为 `UNKNOWN`，模型也会解释 SQL 三值逻辑；在 `WHERE` 与 `CHECK` 等接口中却把 UNKNOWN 用成同一种 Boolean policy | 同一 truth state 到 interface-specific acceptance gate，SQL 执行 oracle 严格可判 |

### survivor 的共同约束

- 任何一个若只能在自造短模板出现，退出十强。
- 任何一个若最强近邻已经同时做 `component recognition intact → same downstream operator failure`，退出十强。
- 任何一个若能被 F1–F9 一句话完整解释、没有额外结构预测，退出十强。
- 最终第二批必须凑齐 **10 个同等级 survivor** 后才建立 final shortlist；第十题未出现前保持 9。

---

## 3. 已杀：exact / near-exact behavior 已被直接占领

| 主题 | 裁决 | 死亡理由 / 代表邻居 | 禁止复活条件 |
|---|---|---|---|
| **Imperfective completion / imperfective paradox** | `KILL-EXACT` | ACL 2026 已有 *The Imperfective Paradox in Large Language Models*，且获 Outstanding Paper | 不得改成 event completion/telicity 新名字重开 behavior discovery |
| **Fan effect** | `KILL-EXACT` | CoNLL 2024 *Large Language Model Recall Uncertainty is Modulated by the Fan Effect* 直接测 LLM fan effect | 只能做明确的新机制续作，不能宣称新行为 |
| **Presupposition projection / existential presupposition** | `KILL/OCCUPIED` | ACL Findings 2025、LREC 2026、CoNLL 2026 已直接系统研究 presupposition judgment/projection | 换 conditional / existential trigger 不构成新题 |
| **Scalar implicature cancellation** | `KILL-EXACT/NEAR-EXACT` | 2026 已有 recognition/cancellation 数据与评测；仓库 DPC-07 已停止投入 | 只有完全不同 operator 才能重新进入，不能做 canceled inference 普通复用 |
| **Pluralistic ignorance** | `KILL-EXACT` | 2026 *Everyone Conforms, No One Believes* 已在 8 模型/100 场景直接研究 LLM agent populations | 不得改名为 private/public norm gap |
| **Idempotent retry / duplicate side effects** | `KILL-EXACT` | `IdempotencyBench`（ARR 2026 under review）已用 320 tasks 测 retry 下 duplicate side effects、idempotency keys 与 receipts | agent retry 行为发现线关闭；只允许机制 follow-up |
| **Mental accounting** | `KILL-EXACT` | 2026 *Do LLMs Keep Mental Accounts?* 已研究 hedonic framing、nonfungibility、sunk-cost sensitivity | 不得以钱包/预算/账户换场景复活 |
| **Generic opportunity-cost neglect** | `KILL-OCCUPIED` | 已进入 LLM human-reasoning / cognitive-bias benchmark 类工作 | 除非发现 components-intact 的全新 operator，否则不做“LLM 忽视机会成本” |
| **Generic bystander effect in multi-agent LLMs** | `KILL/NEAR-EXACT` | multi-agent social-bias / responsibility diffusion 工作已经直接逼近 | 不能只把经典社会心理效应搬到 agent population |

---

## 4. 已杀：母命题完整包含 / 只是 F1–F9 换皮

| 主题 | 裁决 | 母命题吸收方式 |
|---|---|---|
| **Part–whole double counting** | `ROUTE F6` | 局部 membership 正确、global sum/reducer 错，是 F6 标准实例 |
| **Collective predicate → every member**（宽版本） | `ROUTE OIR/F6` | 仓库 OIR-07/SEC-12 已登记 collective→distributive；普通 group/member 投射不再新开 |
| **Hidden-profile bias**（宽版本） | `NOT-ADDED / ROUTE` | shared/private information pooling 与 SEC/F4/F9 及成熟 hidden-profile paradigm 高度重合；没有独立 operator 时不单列 |
| **Redundant constraint changes choice**（宽版本） | `NOT-TOP10 / F6-F7 RISK` | 若 feasible set/optimum 未严格证明，只是 constraint distraction；若严格证明仍需超出 reducer/authority 母族 |
| **Multiplicity-adjusted significance override** | `NOT-TOP10 / F7-RISK` | “知道正式阈值却回到 .05”容易被 F7 正式规则 vs 熟悉默认完整吸收，目前不占名额 |
| **Unknown→false generic decision** | `ROUTE F8` | 信息不可得/未知被写成 false 已是 F8；没有 interface-specific operator 不新开 |
| **Dead/unreachable-code influence** | `DUPLICATE/ROUTE CSS-10` | 仓库 CSS-10 已完整登记 reachability correct → dead payload affects output；本轮不得再建卡 |
| **Rollback/concurrency generic ghost state** | `ROUTE F3 / existing ATW/CSS` | 当前状态与历史路径分离已有 ATW-09/CSS-09 等；单纯换成 race/concurrency 不够 |
| **Delegation / causative actor confusion**（宽版本） | `ROUTE F2 / AIC-09` | physical actor / causer / responsibility binding 已是 AIC-09 与 F2 类型 |
| **Spatial reference-frame confusion**（宽版本） | `NOT-ADDED` | 若只表现为 viewpoint/coordinate frame accuracy，属于成熟 spatial/reference-frame reasoning；未找到独立 downstream operator |

---

## 5. 已杀或降级：经典 bias 直接搬运，缺少独立 operator

以下主题并非说“没人研究”或“绝对无价值”，而是**本轮找主会可解释性新现象时不够独立**。若未来重新提出，必须带一个全新的 decisive contrast，而不是只复现人类 bias。

| 主题 | 本轮裁决 | 主要问题 |
|---|---|---|
| **Description–experience gap（宽版本）** | `NOT-ADDED` | risky-choice/rare-event 决策与 probability transformation 邻域已有工作；单纯描述 vs 样本序列不足 |
| **Peak-end rule / duration neglect** | `NOT-ADDED` | 经典 sequence-evaluation bias 本身不够；未形成 components-intact 的独立 operator |
| **Einstellung / mental set** | `KILL/OCCUPIED` | ACL 2026 MedEinst 已直接研究医疗 Einstellung/先验压过反事实证据；宽“旧策略固着”也属于 anchoring/plan inertia |
| **Moral outcome bias** | `NOT-ADDED` | outcome/hindsight/moral judgment bias 工作拥挤，且容易只得到 judge preference 效应 |
| **Preference reversal（宽版本）** | `NOT-ADDED` | framing/context-dependent choice 已很拥挤；没有 invariant/operator 时不够 |
| **Denominator neglect / ratio bias** | `NOT-ADDED` | 经典 numeracy/cognitive-bias 复现不足，且可被基础 numeracy failure解释 |
| **Regression-to-the-mean neglect** | `NOT-ADDED` | 很容易退化成统计能力题；未找到能力完好、downstream operator 独立的结构 |
| **Optional stopping / p-hacking（宽版本）** | `NOT-ADDED` | 若只问显著性判断，是统计规则应用；需新的 sequential-evidence operator 才有资格 |
| **Ecological fallacy** | `NOT-ADDED` | aggregation/statistical reasoning 母区拥挤，现阶段缺少不可被 F6/causal benchmark 吸收的机制合同 |
| **Explaining-away / collider（宽版本）** | `NOT-ADDED` | causal reasoning 与 collider/selection-bias benchmarks 已占母题；不能再做“LLM 不懂 collider” |
| **Actual-causality preemption** | `NOT-ADDED` | actual causality/causal reasoning 邻域拥挤，且自然 gold/机制定位成本高 |
| **Sure-Thing / disjunction effect** | `DISCOVERY-OCCUPIED` | 第一批审计已确认已有工作直接以 Savage sure-thing principle 评估 ChatGPT |

---

## 6. 已杀或降级：记忆类脑暴

| 主题 | 裁决 | 原因 |
|---|---|---|
| **Fan effect** | `KILL-EXACT` | CoNLL 2024 已直接做 LLM fan effect |
| **Prospective memory（宽版本）** | `NOT-ADDED` | “记住未来要做的事”过宽，易退化 agent reminder/state tracking；没有独立 operator |
| **Proactive interference（宽版本）** | `NOT-ADDED/ROUTE F3` | old-state interference 与仓库 memory update/path dependence 重合 |
| **Generic retrieval interference** | `NOT-ADDED` | 没有 active retrieval manipulation 时会被 context interference/fan effect 吸收 |
| **Retrieval-practice-induced forgetting** | `SURVIVE-TO-N0` | 只有主动 retrieval 相对 repeated study 的选择性 related-item suppression 版本保留，见上表 #4 |

---

## 7. 已杀或降级：程序 / agent 类脑暴

| 主题 | 裁决 | 原因 |
|---|---|---|
| **Idempotent retry** | `KILL-EXACT` | IdempotencyBench 已正面占位 |
| **Dead code** | `DUPLICATE CSS-10` | 仓库已有完整候选，不重复建卡 |
| **Generic exception happy-path continuation** | `DUPLICATE/ROUTE CSS-04` | 仓库 CSS-04 已登记 exception condition correct → nominal return |
| **Generic concurrency/race confusion** | `NOT-ADDED` | 若只是执行预测失败，不够；自然 benchmark 与 deterministic gold 也不如 short-circuit 干净 |
| **Generic delegation** | `ROUTE AIC-09` | agent/causer/actor responsibility 已有卡 |
| **Short-circuit side-effect leakage** | `SURVIVE-TO-N0` | 由语言执行语义提供严格 value/effect 双通道 gate，见 #3 |
| **SQL UNKNOWN interface collapse** | `SURVIVE-TO-N0` | 同 truth state 在不同 SQL interface 的规范映射不同，见 #9 |

---

## 8. 本轮进一步脑暴但尚未晋级的边缘题

这些不算死亡库，也不算 survivor；继续搜索时可以被正式杀掉或成为第 10 题。

- **ITT vs per-protocol conclusion routing**：需要避免沦为“读错分析集/统计知识题”。
- **Multiplicity-aware sequential evidence**：必须找到比 F7 `.05` default 更独立的 operator。
- **Subgroup interaction vs subgroup significance**：若模型知道 interaction test 与 subgroup p-value 不等价、仍作 treatment-effect heterogeneity 结论，可能有空间；需要 exact audit。
- **Competing-risk / censoring interpretation**：现实重要但统计专业门槛与 gold 构造成本高。
- **Collective/distributive non-Boolean predicates**：宽版本已路由；只有出现与 OIR-07 不同的 semantic operator 才重开。
- **Burden/default、review standard、remedy、surrogate、composite、NI/equivalence**：已进入当前 survivor，详见 N0 工作稿。

---

## 9. 已确认的代表性死亡引用

- ACL 2026 Outstanding Papers：*The Imperfective Paradox in Large Language Models*。
- Roberts et al., CoNLL 2024：*Large Language Model Recall Uncertainty is Modulated by the Fan Effect*。
- Atwell et al., Findings ACL 2025：*Measuring Bias and Agreement in Large Language Model Presupposition Judgments*。
- Wörgötter et al., LREC 2026：*There Is No Spoon: Existential Presupposition in Large Language Models*。
- Azin et al., CoNLL 2026：*Presupposition and Reasoning in Conditionals: A Theory-Based Study of Humans and LLMs*。
- YS, 2026：*Everyone Conforms, No One Believes: Pluralistic Ignorance in LLM Agent Populations*。
- Gopnal Swamy, 2026：*Do LLM Agents Act Exactly Once? Measuring Idempotency Violations Under Retries* / IdempotencyBench，ARR 2026 under review。
- Chen et al., 2026：*Do LLMs Keep Mental Accounts? Empirical Evidence from Hedonic Framing, Nonfungibility, and Sunk Cost Sensitivity*。

正式 independent N0 时仍需逐题做 citation chaining、全文/appendix 检查；本账本不把搜索未发现写成绝对 priority claim。

---

## 10. 下一步

1. 继续从未覆盖母区脑暴，直到有第 10 个达到与当前 9 个相同门槛的题。
2. 对当前 9 个逐题完成最强邻居全文/appendix审查；任何一题死就继续补，不维持数量。
3. 凑齐 10 个后新建 `BATCH2_FINAL_N0_SURVIVORS_10_2026-08-28.md`；在此之前不创建假“final ten”。
4. 所有死亡主题同步回填各领域文档；后续发现新的死亡理由继续追加本账本与领域死亡区。
