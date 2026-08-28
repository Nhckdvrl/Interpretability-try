# 第二批：reviewer-mode N0 后的十题 survivor（2026-08-28）

状态：`REVIEWER-MODE-N0-SURVIVOR / AWAITING EXTERNAL INDEPENDENT SIGN-OFF / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
batch: 2
survivor_count: 10
```

本文件不是“十个想法”，而是第二批从大规模脑暴、仓库内部去重、exact/near-exact 检索、mother-inclusion attack、D0 预审和 reviewer-mode N0 后留下的 **10 个新 survivor**。第一批十题见 `DEEP_N0_SURVIVORS_10_2026-08-28.md`，本批不复用第一批任何题。

本轮完整找题、死亡、降级与 reserve 记录见：

- `BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`：前半轮脑暴账本；
- `BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md`：本轮 reviewer-mode N0、补题与最终去留；
- `audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`：早期 9 个 survivor 的详细攻击稿。

**`REVIEWER-MODE-N0-SURVIVOR` 仍不等于仓库流程中的 formal `N0-PASS`。** 正式 N0 仍需另一独立 auditor 做 citation chaining、全文/appendix refresh 与时间戳更新；随后还要过 D0 才能进入 `READY-TO-SMOKE`。本文件不授权调用模型。

---

## 最终十题

| # | 题目 | 一句话 decisive contrast | reviewer-mode 结论 |
|---:|---|---|---|
| 1 | **Burden-Placement Null-Case Reversal** | 事实仍 unresolved、burden 归属也识别正确；只交换谁负举证责任，默认裁决却不交换 | `SURVIVE` |
| 2 | **Short-Circuit Side-Effect Leakage** | 模型正确说 RHS 不执行且返回值正确，post-state 却仍加入 RHS 副作用 | `SURVIVE` |
| 3 | **Retrieval-Practice-Induced Forgetting** | 主动检索 Rp+、而非等量重读 Rp+，选择性压低同类别未练习 Rp− | `SURVIVE` |
| 4 | **Noninferiority → Equivalence Collapse** | NI margin/CI 与单侧含义都读对，最终仍把 `noninferior` 升格为对称 `equivalent` | `SURVIVE` |
| 5 | **Surrogate → Clinical-Outcome Promotion** | surrogate 身份与未验证状态均识别正确，摘要仍把 surrogate 改善写成患者临床获益 | `SURVIVE` |
| 6 | **Harmless-Error → Remedy Collapse** | `error=true` 与 `prejudice/harmless` 都判断正确，remedy 仍退化成 `有错→必撤销` | `SURVIVE` |
| 7 | **SQL UNKNOWN Interface Collapse** | 同一个 predicate 正确算成 SQL `UNKNOWN`，却在 `WHERE` 与 `CHECK` 等 interface 使用同一 Boolean policy | `SURVIVE` |
| 8 | **Subgroup-Significance → Interaction Promotion** | subgroup A 显著、B 不显著，但 interaction 不显著且模型也读对；摘要仍宣称 treatment effect 因 subgroup 而异 | `SURVIVE` |
| 9 | **Competing-Event → Censoring Collapse** | competing event 被正确识别为会阻止 target event，最终风险计算/方法仍把它当 ordinary censoring | `SURVIVE` |
| 10 | **Stock–Flow Correlation Intrusion** | `ΔStock = inflow − outflow` 与净流量符号都算对，stock trajectory 却跟着 inflow 的表面趋势而非净流量走 | `SURVIVE` |

---

# 1. Burden-Placement Null-Case Reversal

## 自然母现象

法律、行政、保险、审查和竞赛式判断里，**事实未被证明时谁承担不利后果**由 burden of proof / burden of persuasion 决定。burden 不是证据本身，也不告诉模型 P 或 ¬P 哪个更真实；它定义的是 unresolved/null case 的 default disposition。

## 冻结 contrast

同一证据材料 E：

```text
E does not establish P
E does not establish not-P
burden holder is identified correctly
```

只交换：

```text
burden(P) ↔ burden(not-P)
```

若最终 disposition/default 不随 burden placement 翻转，而持续追随内容 plausibility，才算现象。

## strongest neighbor / N0 边界

ACL 2026 的 FocalLaw / dispute-focus legal judgment 工作已经表明 LLM 会漏用真实案件中的 burden-of-proof 等争点信息；这是本题最强任务邻居。但其核心 failure 是**没有正确利用/提取争点或 burden**，不是本题冻结的 `burden recognized + evidence unresolved + default action wrong`。

## why_not_a_rename

不是 F7 authority：burden 不是更高权威对低层内容的覆盖。也不是 generic confidence threshold：在两边都未达证明门槛时，burden 是一个**离散 default allocator**。错误的结构预测是：同一 evidential state 下交换 burden 应交换 losing side。

## competing mechanisms

1. burden role 可解码，但 verdict head 没有 null-case/default gate，直接按 proposition plausibility argmax；
2. default gate 存在，但 party↔claim binding 在 late composition 时接反；
3. evidence accumulator 先生成单一 posterior，procedural default 只进入 explanation writer。

## D0 / hard gold

优先从公开司法意见、jury instructions、administrative burden rules 与 FocalLaw/CourtListener 中抽真实 unresolved/dispositive cases；只保 gold 可由正式规则与结果冻结的实例。

## hard kill

- burden readout 本身不稳；
- 只能靠自造法律模板；
- matched burden swap 在法律上改变了其他事实/标准；
- strongest neighbor 已在 appendix 做同一 `unresolved evidence × burden swap → disposition` factorial。

---

# 2. Short-Circuit Side-Effect Leakage

## 自然母现象

主流程序语言的 `A || B` / `A && B`、guard、conditional expression 等存在短路语义：左侧已经决定结果时，右侧不仅“不影响 return value”，而且**不执行，因此副作用不发生**。

## 冻结 contrast

选择 RHS 带可观测 mutation/function call/logging/counter increment 的真实代码片段。先验收：

```text
left operand = correctly evaluated
RHS = correctly stated as not executed
expression return value = correct
```

再问 post-state/call count。如果模型仍加入 RHS side effect，才计入。

## strongest neighbor / N0 边界

现有代码执行、stepwise execution、ExecVerify 等研究覆盖一般执行预测和验证，但本轮检索未发现把 `short-circuit recognized → return value correct → side-effect state still leaks` 作为 phenotype 的工作。

## why_not_a_rename

不是 generic code execution accuracy，也不是 CSS-10 dead-code attraction。独立 operator 是**同一 expression 的 value-path 与 effect-path 应共享同一个 execution gate**；现象要求 value path 已正确短路而 effect path 没短路。

## competing mechanisms

1. value decoder 对 RHS 做 gate，mutation store 对所有显式 call 做 eager update；
2. execution trace 正确，但 final-state summarizer 按 lexical mention 重建 side effects；
3. RHS activation 在 gate 前已写入 persistent state，return-value path 后续才抑制。

## D0 / hard gold

JavaScript/Python/Java/C# 等语言官方语义 + 真实解释器直接给 executable oracle；可从 GitHub/benchmark 中筛短路条件与副作用片段，再最小化。

## hard kill

- expression value/RHS-execution 判断本身就错；
- 只有人工布尔玩具题；
- dead-code/last-write control 完整解释；
- 已有 code MI 工作 exact 做同一 dual-path leakage。

---

# 3. Retrieval-Practice-Induced Forgetting

## 自然母现象

人类记忆中的 retrieval-induced forgetting (RIF) 与普通干扰不同：对一类项目中的部分项目进行**主动 retrieval practice**，可能选择性损害相关、未练习项目；等量重复阅读并不必然产生同型损失。

## 冻结 contrast

对模型本来稳定可取的 related facts：

```text
baseline
passive restudy of Rp+
active retrieval practice of Rp+
unrelated retrieval practice
```

最终只看 related-unpracticed `Rp−`，并用 unrelated `Nrp` 作控制。

## strongest neighbor / N0 边界

ACL 2022 multi-answer QA 已观察一个 valid answer 的生成依赖其他答案证据；EMNLP 2025 *Promote, Suppress, Iterate* 又揭示 one-to-many factual generation 中对**已经生成的 answer token** 的 suppression。本题只有在 `主动 retrieval practice → 后续相关未练习事实受损`、且明显不同于 passive restudy/即时已生成答案 suppression 时才独立。

## why_not_a_rename

不是 fan effect、Part-List Cue、普通 recency 或 one-to-many suppression。独立 manipulation 是 **retrieval operation 本身**，独立 wrong destination 是 `Rp−` 的 delayed accessibility，而不是先前输出 token。

## competing mechanisms

1. retrieval 时主动抑制 category competitors，形成残留 inhibitory state；
2. Rp+ 被强化后在后测中竞争性抢占检索，没有真正抑制 Rp− trace；
3. retrieval practice 改变 query/context representation，造成 category-specific route shift。

## D0 / hard gold

QAMPARI/Wikidata/百科实体多值关系提供自然 related-item sets；先冻结模型 baseline 可知的 gold，再做 retrieval/restudy manipulation。最终 gold 是外部 relation set，不依赖 judge。

## hard kill

- passive restudy 产生同幅下降；
- unrelated items 同幅下降；
- effect 仅限立即继续 list generation；
- 已有 LLM RIF 工作完整覆盖同一 retrieval-practice paradigm；
- 只能靠临时背人工词表出现。

---

# 4. Noninferiority → Equivalence Collapse

## 自然母现象

Noninferiority (NI) 成功只说明新治疗没有比 comparator 差到超过预设 margin；它不是对称 equivalence 证明。equivalence 通常需要两个方向都满足预设界限。

## 冻结 contrast

用真实 RCT 的 margin、CI 与 trial design。先验收：

```text
model identifies NI design
model reads margin/CI correctly
model explicitly says NI success alone ≠ equivalence
```

随后让它写 treatment comparison / clinical summary；若仍系统生成 `equivalent / same effectiveness / no difference`，才计入。

## strongest neighbor / N0 边界

CliniFact 等 clinical-claim verification 数据已包含 noninferiority/equivalence 类别，临床摘要工作也大量存在；但本轮未找到把 **one-sided NI relation 已正确解析，却在 downstream summary 被对称化** 作为研究对象的 LLM 工作。

## why_not_a_rename

不是一般统计 literacy，也不是普通 F6 reducer。错误是一个明确的**relation-type promotion**：

```text
not-worse-than-by-more-than-Δ  →  equal-to
```

方向性被抹掉，并有可数学反证的 wrong destination。

## competing mechanisms

1. `noninferior` 与 `equivalent` 在 outcome representation 中共享“no meaningful difference”方向，direction bit 丢失；
2. trial-design relation 完整，但 summary writer 把“未证明更差”默认翻译成“相同”；
3. margin/CI gate 只供 verifier 使用，不进入 comparative-language decoder。

## D0 / hard gold

ClinicalTrials.gov + PubMed NI RCT + structured margin/CI；优先 trial registration 与原始 abstract 能冻结 design/gold 的实例。

## hard kill

- 模型不懂 margin/CI；
- 只在媒体标题而非原始 trial text 出错；
- strongest biomedical LLM work 已专门系统测 NI→equivalence 且包含 recognition-intact control；
- 输出只是模糊“相近”，无法确认 relation promotion。

---

# 5. Surrogate → Clinical-Outcome Promotion

## 自然母现象

Surrogate endpoint 的改善不自动证明患者重要的 clinical outcome 改善；其可替代程度取决于 surrogate validation 与具体 context of use。

## 冻结 contrast

优先选择 FDA/真实 trial/review 中 surrogate 与 clinical endpoint 明确区分的案例。先验收：

```text
model identifies the endpoint as surrogate
model identifies whether it is validated / only reasonably likely
model states surrogate improvement alone is insufficient for target clinical benefit
```

之后摘要/建议仍写成 `improves survival / reduces clinical events / benefits patients` 才计入。

## strongest neighbor / N0 边界

已有 surrogate evaluation 平台、PICO/clinical summarization、claim verification 等邻近工作，但本轮未发现 exact 做 `surrogate role recognized + validation status correct → target clinical outcome still promoted` 的 LLM phenotype。

## why_not_a_rename

不是 generic correlation≠causation。即使 surrogate 与 clinical outcome 存在因果联系，**是否足以替代 target endpoint** 仍由 validation/context gate 决定；错误是 endpoint-role/validation → allowable claim-level 的非法转换。

## competing mechanisms

1. surrogate 与 target outcome 分开，但同一“improvement”value direction 在 summary writer 中广播；
2. 模型默认补一条未经验证的 surrogate→clinical edge；
3. validation flag 只在 explanation head 可读，clinical-benefit decoder 没有 gate。

## D0 / hard gold

FDA surrogate endpoint resources、accelerated approvals、confirmatory trials、trial abstracts/reviews；只保 validation/status 与 target outcome 能由权威来源冻结的样本。

## hard kill

- gold 本身有医学争议；
- 实际上该 surrogate 在相同 context 已被充分验证；
- 只是领域知识不足；
- 已有 biomedical LLM work exact 做 recognition-intact surrogate promotion。

---

# 6. Harmless-Error → Remedy Collapse

## 自然母现象

法律错误发生，不自动等于 reversal/new trial/remedy。harmless-error / prejudice doctrine 把 `error existence` 与 `remedy entitlement` 明确分成两个阶段。

## 冻结 contrast

真实 appellate materials 中先验收：

```text
error occurred = correctly identified
harmless/prejudice standard = correctly identified
prejudice threshold = correctly classified
```

若最后 disposition 仍近似 `error=true → reverse`，或反向把 `harmless` 写成“根本没有 error”，才计入。

## strongest neighbor / N0 边界

LegalBench、CourtReasoner、FocalLaw、LEGALSCOPE 等覆盖法律规则/争点/论证，但本轮没有找到同一三阶段 `error recognition intact + prejudice intact → remedy collapse` factorial。

## why_not_a_rename

不是第一批的 Inadmissible-Evidence Persistence：后者问 evidence 是否应从 evidential posterior 中剔除；这里问**一个已经成立的 legal error 是否跨过 prejudice gate 获得 remedy**。

## competing mechanisms

1. legal-state encoder 把 error existence 与 severity/prejudice 压成单一 violation scalar；
2. 两个状态都在，但 remedy head 只读取 binary error flag；
3. prejudice gate 仅用于 rationale，不参与 disposition computation。

## D0 / hard gold

公开 appellate opinions / CourtListener 中大量 harmless-error 分析；使用有明确 error、harmless/prejudicial finding 与最终 remedy 的案件。

## hard kill

- prejudice classification 本身不稳；
- 只能在极长 opinions 出错，短 controlled excerpts 消失；
- gold 不能从 opinion/result 冻结；
- existing LLM legal paper exact 覆盖 same three-stage contrast。

---

# 7. SQL UNKNOWN Interface Collapse

## 自然母现象

SQL NULL comparisons 可产生正式第三 truth value `UNKNOWN`。关键不是“UNKNOWN 等于 false 吗”，而是不同 interface 对同一 truth state 的规范映射不同：例如 `WHERE` 只保留 TRUE，而 `CHECK` 的约束接受规则并非简单复用 WHERE 的过滤策略。

## 冻结 contrast

固定一个 predicate，先验收：

```text
predicate = UNKNOWN (correct)
3-valued logic explanation = correct
WHERE rule = correct when asked alone
CHECK rule = correct when asked alone
```

再预测实际 row retention / constraint acceptance。如果在组合执行时把 UNKNOWN 统一映射成一种 Boolean policy，才计入。

## strongest neighbor / N0 边界

Text-to-SQL、verification、NULL robustness 工作很多，但本轮未找到 `UNKNOWN correctly represented → interface-specific reducer collapse` 的 exact LLM study。

## why_not_a_rename

不是 F8 `unknown → false`。这里 `UNKNOWN` 是**正式 truth state**，而且要求模型已正确表示；新 operator 是：

```text
truth state × SQL interface → acceptance/filter policy
```

同一 state 在不同 interface 需要不同 reducer。

## competing mechanisms

1. 中层 explanation 有 ternary state，但 executable simulator 只保留 Boolean truthiness；
2. UNKNOWN state 与 interface representation 都存在，dispatch/reducer 选择失败；
3. 最终 state reconstruction 被通用语言中的 unknown≈false 先验覆盖。

## D0 / hard gold

冻结具体数据库/标准版本；真实 DB engine 直接执行给 oracle，配官方 documentation。

## hard kill

- predicate truth 本身算错；
- dialect/engine semantics 未冻结；
- 只有 NULL syntax 知识错误；
- 已有 LLM SQL paper exact 做 recognition-intact interface collapse。

---

# 8. Subgroup-Significance → Interaction Promotion

## 自然母现象

医学统计和实验分析中，一个 subgroup 显著、另一个不显著，并不等于两 subgroup 的 treatment effect 显著不同。真正的 effect heterogeneity 应看 treatment×subgroup interaction（以及预先指定、multiplicity 等条件）。

## 冻结 contrast

真实 trial forest plot/table 中冻结：

```text
subgroup A treatment p < .05
subgroup B treatment p > .05
interaction p > .05
interaction/heterogeneity result read correctly
```

如果模型仍写 `treatment works only in A`、`effect differs by subgroup`、`B does not benefit while A benefits`，才计入。

## strongest neighbor / N0 边界

这是统计报告领域非常经典的错误，但本轮对 ACL/EMNLP/NAACL、biomedical LLM、arXiv/OpenReview 做 exact/synonym 搜索，没有找到以 **interaction 已读对，summary 仍被 subgroup significance pattern 绑架** 为核心的 LLM 现象论文。

## why_not_a_rename

不是 generic p-value literacy。局部 p-value 与 interaction p-value 都必须读对；错误是把两个**within-subgroup significance labels**非法转换成一个**between-subgroup relation**。wrong destination 是明确的 heterogeneity claim。

## competing mechanisms

1. heterogeneity decoder 直接比较 binary significance labels，而不是 effect difference/interaction；
2. interaction representation存在，但 final clinical-language writer更受 `significant/non-significant` lexical states驱动；
3. effect-size vectors正确，但 categorical significance creates subgroup-specific benefit nodes that later get contrasted。

## D0 / hard gold

真实 RCT forest plots、supplement tables、subgroup analyses；优先同时报告 effect estimates、CI、within-subgroup values 与 interaction p 的资料。可程序化核对 interaction gold，避免 judge。

## hard kill

- interaction/p-value extraction本身错；
- 错误来自图表 OCR；
- 没有真实样本，只能自造；
- 已有 LLM study 已做 `one subgroup significant / other not + interaction non-significant → heterogeneity narrative`。

---

# 9. Competing-Event → Censoring Collapse

## 自然母现象

Survival analysis 中 competing event 与 ordinary censoring 不同。competing event 一旦发生，会使 target event 不再可能作为第一事件发生；把它当普通 censoring 后直接用 `1−KM` 估 cumulative incidence 会系统高估 target-event risk。

## 冻结 contrast

用真实或可执行 survival table，先验收：

```text
model identifies event B as competing event
model explains B precludes target event A
model says treating B as ordinary censoring can overestimate cumulative incidence
```

随后 method choice/calculation 仍把 B 当 censoring、用 naive KM complement，才计入。

## strongest neighbor / N0 边界

ICLR 2026 CausalPitfalls 已覆盖多种因果统计陷阱/selection bias，因此“LLM 不懂 competing risk”这种宽题不够；但本轮未发现其或 NLP work 覆盖 **competing-event state recognized → risk-set updater still routes to censoring** 的 exact operator。

## why_not_a_rename

不是 F8 unknown/missingness，也不是 generic censoring literacy。competing event 是一个**已观察到的 absorbing alternative event**；ordinary censoring 是未来 target outcome 未再观察。错误是把两个不同的 risk-set state transition 合并。

## competing mechanisms

1. event-type representation正确，但 survival updater 只有 failure/censor 二态；
2. method-selection head 被 KM lexical prior吸引，绕过 competing-risk tag；
3. cause-specific hazard path被错误读成 cumulative incidence/risk。

## D0 / hard gold

公开 competing-risk datasets + R/Python survival packages；CIF、cause-specific hazard、naive KM 可执行复算，gold 很硬。

## hard kill

- 模型不懂 competing event 定义；
- 只在术语问答失败；
- strongest causal-reasoning work 已扩展到同一 recognition-intact risk-set routing；
- effect 在可执行表格/短文本中不出现。

---

# 10. Stock–Flow Correlation Intrusion

## 自然母现象

系统动力学中经典 stock–flow failure：stock 的变化由净流量决定，`ΔS = inflow − outflow`。人会因为 inflow 的形状很显眼而使用 correlation heuristic，让 stock trajectory错误地跟随 inflow，而不是积分 net flow。

## 冻结 contrast

固定时间点/时间序列，先验收：

```text
model states ΔS = inflow - outflow
model correctly computes inflow > outflow
model correctly says net flow is positive
```

然后要求画/描述 stock trajectory。若它因为 inflow 本身正在下降，就预测 stock 下降，即使 net flow 仍为正，才计入。

## strongest neighbor / N0 边界

2026 FinIndices 使用“stock-flow caliber alignment”术语，但它研究的是财务指标中 flow variable 与 average stock variable 的口径/比率对齐，以及长报表公式结构；不是动态 accumulation，也没有经典 `net-flow sign correct → stock trend follows inflow shape` 的 correlation-heuristic phenotype。

## why_not_a_rename

不是基础算术，也不是 FinIndices 的财务口径。独立 computation 是**persistent accumulator/integrator vs salient trend matcher**。局部净流量必须正确，只有 trajectory/update operator 出错。

## competing mechanisms

1. 公式/净流量在语言 head 正确，但 trajectory decoder 使用 correlation heuristic；
2. 每步 net flow正确，却没有 persistent stock accumulator，生成下一个状态时重新锚定显眼 flow；
3. accumulator存在，但 derivative/trend features在晚层竞争并压过其输出。

## D0 / hard gold

经典 bathtub/CO2/inventory/backlog/bank-balance 自然 stock-flow systems；可加真实公开 time series。oracle 为逐步积分/差分，跨领域可严格复算。

## hard kill

- 净流量符号/公式本身经常算错；
- 只在图表视觉读取失败；
- 只有一个领域/一个故事模板；
- 现象最终等价 FinIndices 的 variable-caliber mismatch；
- 已有 LLM work exact 做 components-intact stock-flow correlation heuristic。

---

## 本批明确不进十强的强 reserve / 死亡项

- **Composite → Component Benefit Projection**：`KILL/ROUTE F6/OIR`。整体属性广播到成员是仓库已登记的 collective/distributive 母题，医学 composite 只是好 setting，不构成新 operator。
- **Appellate-Deference Override**：`HOLD / D0-WEAK`。暂无 exact collision，但同一案件合法地只交换 `de novo ↔ deferential` 往往不自然，review standard 与 issue type 绑定，难做无混杂 matched D0。
- **Immortal-Time Backfill**：`RESERVE`。future-treated membership 反向污染 earlier person-time 很漂亮，但 ICLR 2026 causal/selection-bias 大母区已强占位；当前不如 competing-risk 的 state-transition operator 独立。
- **ITT vs per-protocol routing**：`NOT-TOP10`。容易被 estimand/selection/causal inference 母题吸收。
- **DNR scope spillover**：`ROUTE F5/F6`。局部 treatment limitation 被错误扩展到所有治疗，本质仍是 scope/veto propagation。
- **Prediction interval vs confidence interval、hazard ratio vs risk ratio、odds ratio vs risk ratio、percentage-point vs percent**：`NOT-TOP10`，过度接近基础 statistical/numeracy literacy。
- **Finally/context-manager/generator cleanup variants**：`ROUTE` 到程序 effect-gating/控制流母线，不与 Short-Circuit 拆多篇。

---

## reviewer-mode 最终门槛

这十题全部满足当前这次 reviewer-mode 的最低条件：

```text
1. 不复用第一批十强；
2. 仓库 162 卡与 F1–F9 中没有 exact duplicate；
3. targeted exact/synonym search 未发现已完整做 decisive contrast 的 LLM 论文；
4. strongest broader neighbor 不能一句话完整逻辑包含该 operator；
5. why_not_a_rename 不是“换数据/换领域/换 readout”；
6. 有外部规范、真实任务或 executable oracle 可以冻结 gold；
7. 至少两个可被因果实验区分的 mechanism；
8. 已写 hard kill，不允许为了维持十题数量续命。
```

正式 independent N0 若杀掉任一题，直接回死亡库，再从 `BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md` 的 reserve 中补位；不得降低标准。