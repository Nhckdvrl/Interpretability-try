# 第二批新题 adversarial / independent-style N0 工作稿（2026-08-28）

状态：`9 CURRENT SURVIVORS / TENTH SLOT OPEN / NOT FORMAL N0-PASS / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
batch2_finalized: false
```

## 审计定位

这份文件是第二批找题的**攻击稿**，不是“九个已经证明新颖”的宣传稿。提出者侧先做一次尽量接近独立审稿人的 N0：

- exact phenotype；
- 同义术语与老问题；
- 最新 ACL/EMNLP/NAACL 与同期 ICLR/ICML/NeurIPS/arXiv/ARR；
- 仓库 162 卡与 F1–F9；
- mother-inclusion；
- D0/gold 可冻结性；
- `why_not_a_rename`；
- hard kill。

正式 `N0-PASS` 仍需要另一个独立 auditor 做 citation chaining、全文/appendix 检查与时间戳 refresh。

完整脑暴和死亡库见 [`../BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](../BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

---

# 1. Burden-Placement Null-Case Reversal

## 自然母问题

在很多法律/政策判断里，证据未能解决事实争议时，结论不是由“最像谁说得对”决定，而是由 **burden of proof / burden of persuasion** 决定。相同 unresolved evidential state，在 burden 落到 A 或 B 时应有相反的 default disposition。

## decisive contrast

冻结同一事实材料 E，并先验收：

```text
model says: E does not establish P
model says: E does not establish not-P
model correctly identifies which party bears burden
```

只交换：

```text
burden(A) <-> burden(B)
```

若模型的 verdict/default 不随 burden placement 翻转，而是始终选择同一内容上更 plausible 的一边，才计入。

## why_not_a_rename

不是 UDH-12 的“threshold bypass”。UDH-12 仍有一个连续/标量证据强度和阈值；这里核心是**证据保持 unresolved 时的 default allocator**。也不是普通 F7 authority：burden 不告诉哪一事实是真的，而规定“未证明时谁输”。

## 竞争机制

A. burden role 可解码，但 verdict head 没有 null-case/default gate，直接做 proposition plausibility argmax。

B. burden/default gate 存在，但 party↔claim binding 在 late composition 时错接。

## hard kill

- 模型无法稳定识别 burden 或 unresolved status；
- 错误只来自法律术语陌生，改写成一般 contest 后消失；
- 已有工作完整做同一 `unresolved evidence × burden swap → verdict` factorial；
- 只能靠自造法律模板，找不到专家任务/真实规则锚点。

当前：`SURVIVE-TO-N0`。

---

# 2. Appellate-Deference Override

## 自然母问题

上诉审查不是“我是否同意下级判断”这么简单。`de novo`、clear-error/abuse-of-discretion 等 review standards 决定上级在何种条件下**可以替换**下级判断。

## decisive contrast

同一 lower-court result、同一事实、同一模型自己的 merits judgment；先验收模型能正确解释 review standard。只改变标准：

```text
de novo <-> deferential
```

目标现象：模型说“在 deferential standard 下，即使我会做不同判断也不能仅因此替换”，最终 disposition 却仍跟自己的 merits choice，而不跟 standard。

## why_not_a_rename

不是 Dissent→Holding 的 authority-role binding，也不是 generic legal rule use。这里的 operator 是：

```text
merits disagreement + review standard -> permissible override/remedy
```

同一 underlying proposition truth judgment 在两个 standards 下允许不同 appellate action。

## 竞争机制

A. 模型只有 merits scalar，没有独立 deference gate。

B. standard representation 完整，但 remedy/action head 重新调用 base merits answer，绕过 procedural gate。

## hard kill

- rule explanation 本身不稳；
- strongest legal benchmark 已做 same-case matched standard swap 与 action；
- effect 只跟 `de novo` 关键词而无自然案例复现；
- 没有可冻结 expert/legal gold。

当前：`SURVIVE-TO-N0`。

---

# 3. Short-Circuit Side-Effect Leakage

## 自然母问题

在常见语言中，`A || B` / `A && B`、conditional expression、guard clause 等会**短路控制流**。如果左侧已经决定结果，右侧不仅“不影响返回值”，而且**根本不执行，因此副作用也不发生**。

## decisive contrast

选择带可观测 RHS side effect 的自然代码片段，例如 function call、counter increment、mutation/logging。先验收：

```text
model correctly evaluates left operand
model correctly says RHS is not executed
model correctly predicts expression return value
```

再问 post-state / call count。如果它加入 RHS mutation/call，才是目标。

## why_not_a_rename

不同于 CSS-04 exception continuation 与 CSS-10 dead-code attraction：这里同一 expression 内存在**value path 与 effect path 的双通道短路**，而且 operator 是语言定义的 execution gate。不是泛“知道控制流但输出错”。

## 竞争机制

A. return-value simulator 正确应用 short-circuit，但 side-effect updater 对所有显式 call 做 eager execution。

B. execution trace 正确，post-state summarizer 按 lexical mention 汇总 side effects。

## hard kill

- output/value prediction也错；
- 只有玩具布尔题、真实代码中不出现；
- 已有 code MI 工作完整做 `short-circuit recognized → side-effect leakage`；
- dead-code/last-write bias controls 可完全解释。

当前：`SURVIVE-TO-N0`。

---

# 4. Retrieval-Practice-Induced Forgetting

## 自然母问题

人类记忆中的 retrieval-induced forgetting（RIF）与单纯 interference 不同：对一个类别中的部分项目进行**主动检索练习**，可能选择性损害同类别、未练习项目；重复阅读/study 并不必然产生同型效应。

## decisive contrast

构造/筛选模型已经能稳定回忆的多个相关事实。比较：

```text
baseline
repeated study of Rp+
active retrieval practice of Rp+
unrelated retrieval practice
```

只看 related-unpracticed `Rp-` 的后续 recall/recognition。目标必须是 retrieval-specific、category-selective suppression，而不是上下文长度下降。

## why_not_a_rename

Fan effect 已被 CoNLL 2024 正面做过；Part-List Cue 也有 one-to-many retrieval 邻居。本题只有**active retrieval operation 相对 passive re-exposure 的选择性后效应**才独立。

## 竞争机制

A. retrieval 时对竞争 trace 发生主动抑制，抑制状态随后保留。

B. 没有抑制；只是 retrieval practice 改变 query/context representation，使后续 routing 偏向 practiced item。

前者预测 recognition/free-recall、cue change 与恢复时间有特定差异；后者更依赖 lexical/query overlap。

## hard kill

- passive repetition 复现同样 drop；
- effect 只是 last-mentioned/recency；
- 不相关事实同幅下降；
- 已有 LLM RIF 论文完整覆盖同一 paradigm；
- 只能靠模型在 context 中临时背诵人工词表。

当前：`SURVIVE-TO-N0`，但 D0 自然性需重点攻击。

---

# 5. Noninferiority → Equivalence Collapse

## 自然母问题

noninferiority (NI) trial 的成功并不等于证明两个处理等效。NI 是相对于预设 margin 的单侧关系；equivalence 通常要求两侧都落在 equivalence margins 内。

## decisive contrast

用公开 trial abstract / structured results 中能冻结 margin、CI 与 conclusion 的实例。先验收：

```text
model correctly explains NI
model correctly says NI success does not by itself establish equivalence
model correctly reads the CI/margin
```

再让它写结论/比较治疗。若从 `noninferior` 系统升级为 `equivalent / same effectiveness`，才计入。

## why_not_a_rename

不是一般统计 literacy 或 relation extraction。核心是**one-sided relation → symmetric relation promotion**，错误 destination 唯一，且可由数学关系严格反证。

## 竞争机制

A. `noninferior` 和 `equivalent` 在 outcome representation 中共享“no meaningful difference”方向，强度不同但未保持方向性。

B. trial design relation 可解码，但 summary/decision writer 把“未证明显著更差”翻译成“相同”。

## hard kill

- 模型不懂 margin/CI；
- 仅发生在媒体标题，不发生在原始 abstract；
- 已有 LLM biomedical paper 专门系统测 NI→equivalence 且同 controls；
- effect 只剩术语 paraphrase，不影响 consequential comparison。

当前：`SURVIVE-TO-N0`。

---

# 6. Surrogate → Clinical-Outcome Promotion

## 自然母问题

生物标志物/替代 endpoint 的改善不自动证明患者重要的临床 outcome 改善；只有经过验证的 surrogate relationship 才允许更强外推。

## decisive contrast

选择 trial/review 中明确区分 surrogate 与 clinical endpoint、并有外部结论的文本。先验收：

```text
model identifies which endpoint is surrogate
model says surrogate improvement alone is insufficient for clinical benefit
model knows no validation/clinical endpoint result is provided
```

随后摘要或建议却写“improves survival / reduces clinical events / benefits patients”才计入。

## why_not_a_rename

不是 generic correlation→causation。这里 operator 是**endpoint role / validation status → allowable outcome level**。即便 causal direction真实，未经验证的 surrogate 也不能自动替代 target endpoint。

## 竞争机制

A. surrogate/clinical roles分开，但同一“improvement”价值方向在 summary writer 中广播。

B. 模型把 surrogate 当 mediator proxy，并在无 validation edge 时默认补一条 surrogate→clinical edge。

## hard kill

- gold 依赖专业争议，不能从 trial/review 原文冻结；
- 只在医学常识不足样本出错；
- 已有 biomedical LLM work exact 做 surrogate promotion；
- 输出只是含糊“promising”，没有明确 clinical promotion。

当前：`SURVIVE-TO-N0`。

---

# 7. Harmless-Error → Remedy Collapse

## 自然母问题

法律错误已经发生，不等于自动获得 reversal/new trial/remedy。许多制度有 harmless-error/prejudice gate：必须判断错误是否影响实质权利或结果。

## decisive contrast

用公开 case/bench 中有 error 与 harmless/prejudicial relation 的材料。先验收：

```text
model: an error occurred
model: identifies harmless/prejudice standard
model: correctly classifies whether prejudice threshold is met
```

如果最终 remedy 仍近似 `error=true -> reverse`，或者反向 `harmless label -> no error existed`，才计入。

## why_not_a_rename

不是 Inadmissible-Evidence Persistence；那里是 evidence mask 是否从 posterior 中撤出。这里是**error finding 与 remedy entitlement 的二阶段 adjudication**。

## 竞争机制

A. legal state encoder 把 error severity 与 error existence 压成单一 violation scalar。

B. 两状态都在，但 remedy head 只读取 binary error flag，不读取 prejudice gate。

## hard kill

- harmless/prejudice 评价本身错误；
- CaseHOLD/LegalBench 最近工作已经同一三阶段 factorial；
- gold 无法从 opinion/专家任务冻结；
- 只在长判决里出现，短原文 control 消失。

当前：`SURVIVE-TO-N0`。

---

# 8. Composite → Component Benefit Projection

## 自然母问题

composite endpoint 把多个 component 合并；总体 composite 改善不蕴含每个 component 都改善。尤其当效果主要由较软/频繁 component 驱动时，把总体 success 广播到死亡、住院等具体 component 是错误投射。

## decisive contrast

优先使用 trial tables/abstracts 同时报告 composite 与 components 的真实结果。先验收：

```text
model knows composite members
model reads component estimates correctly
model explicitly says composite significance need not imply each component benefit
```

然后问具体 component 或生成摘要。如果未显著/方向不同的 component 被写成获益，才计入。

## why_not_a_rename

危险点：很容易被 F6 吸收。因此只有在**composite 作为命名 endpoint/entity 的 representation 被错误 broadcast 到 member outcome**，并出现可预测 component attraction，而不是普通总和/count error 时才独立。

## 竞争机制

A. composite result 绑定到一个 super-node，summary 时默认属性继承给 members。

B. component nodes/values都正确，但 clinical-language decoder 以 composite label 的正向结论覆盖 individual estimates。

## hard kill

- 只是表格读取/数值错误；
- member outcome 未明确报告导致 gold 含混；
- 机制最终只等于 F6 global reducer；
- 已有 biomedical LLM work exact 做 composite→component projection。

当前：`SURVIVE-TO-N0`，但 mother-inclusion 风险高于 #5/#6。

---

# 9. SQL UNKNOWN Interface Collapse

## 自然母问题

SQL 使用三值逻辑：与 NULL 的很多比较产生 `UNKNOWN`。关键不只是会不会算 UNKNOWN，而是**不同 SQL interface 对 UNKNOWN 的接受/过滤规则并不都等同于普通 false**。

例如 `WHERE` 只保留 TRUE；而约束/检查语义存在 interface-specific acceptance 行为。目标不是 SQL trivia，而是 truth-state 表示是否进入正确 interface gate。

## decisive contrast

选择可由真实数据库执行验证的短 SQL/DDL 片段。先验收：

```text
model correctly predicts predicate = UNKNOWN
model correctly explains three-valued logic
model correctly states each interface rule when单独问
```

然后预测 row retention / constraint acceptance / downstream state。如果把 UNKNOWN 在两个 interface 统一映射成同一 Boolean policy，才计入。

## why_not_a_rename

不是 generic unknown→false（F8），因为 SQL UNKNOWN 是**正式第三 truth value**，且异常要求模型正确表示它；不是普通 code execution，因为 same truth state 必须经过不同、规范化的 interface-specific reducer。

## 竞争机制

A. 中层只有 TRUE/FALSE 两个 executable state，解释问题中的 UNKNOWN 来自语言知识旁路。

B. UNKNOWN 可解码，但 code simulator 只有统一 truthiness gate，没有按 interface 选择 policy。

## hard kill

- SQL rule explanation本身不稳；
- error 只由 NULL syntax/DB dialect 知识不足；
- 已有 text-to-SQL/LLM study exact 做 3VL recognized→interface collapse；
- 不同 DB dialect 对规则不一致且无法冻结目标 dialect。

当前：`SURVIVE-TO-N0`。

---

# 10. 第十槽：OPEN

当前没有一个候选达到与前 9 个相同门槛，因此**不写假第十题**。

仍在攻击的候选包括：

- ITT vs per-protocol conclusion routing；
- subgroup significance vs treatment-by-subgroup interaction；
- multiplicity-aware sequential evidence operator；
- competing-risk/censoring 的 event-probability mapping；
- 其他具有硬规范 relation、非 F1–F9 换皮的程序/科学推断算子。

第十题只有满足以下条件才补：

```text
natural mother phenomenon
+ exact collision not found
+ mother cannot fully absorb
+ hard gold / executable oracle
+ ≥2 competing mechanisms
+ conference-scale expansion path
```

否则保持 9。
