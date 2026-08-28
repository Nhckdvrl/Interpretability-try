# 第二批找题：reviewer-mode N0 总账本（2026-08-28）

状态：`DISCOVERY CLOSED AT 10 REVIEWER-MODE SURVIVORS / NOT FORMAL N0-PASS / NOT DISPATCHABLE`

```yaml
batch: 2
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
final_survivor_count: 10
```

这份文件承接：

- [`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)：前半轮大规模脑暴、死亡库与最初 9 个 survivor；
- [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)：最初 9 个的 proposer-side 攻击稿；
- [`BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md)：本轮最终 10 个 reviewer-mode survivor。

本文件记录**第二阶段继续脑暴、反方 reviewer 攻击、母题压缩、补题与死亡理由**。目的不是证明这些题一定新颖，而是防止以后只记住 survivor、忘掉为什么其他题死掉，再用新名字复活。

`reviewer-mode` 的含义：同一研究链内部刻意切换成反方 reviewer，优先寻找能杀题的 exact / near-exact work、appendix variable、F1–F9 母题和 D0 缺陷。它不等于真正独立研究者的 formal N0 sign-off。

---

## 1. 这轮重新设定的门槛

第二批不能靠“没有同名论文”存活。最终十题每题都必须同时满足：

```text
自然母现象/硬规范在 LLM 之前就存在
+ exact phenotype 未发现被直接做完
+ strongest neighbor 不能逻辑上包含 decisive contrast
+ why_not_a_rename 不是“换领域/换数据/readout不同”
+ 对 F1–F9 至少多一个独立 operator 或结构预测
+ gold 能由法律规则、试验设计、统计公式、执行器或自然 relation 冻结
+ 至少两个会产生不同干预预测的机制
+ 有明确 hard kill，而不是任何掉点都算现象
```

同时新增一条实际执行纪律：**若一个候选只能依靠自造短模板出现，即使逻辑漂亮，也不占最终十强。** 模板只能做 mechanism isolation，不能承担 discovery 的全部证据。

---

## 2. reviewer-mode 重新攻击后最终保留的 10 个

| # | 题目 | 独立 operator | 最主要邻居/攻击 | 为什么暂时没被吸收 |
|---:|---|---|---|---|
| 1 | **Burden-Placement Null-Case Reversal** | unresolved evidence 下的 default allocator | FocalLaw / legal judgment 中 burden/dispute focus | 必须冻结 `burden recognized + neither side established`，只测 null-case disposition；不是漏读 burden |
| 2 | **Short-Circuit Side-Effect Leakage** | 同一 execution gate 同时控制 value path 与 effect path | code execution / ExecVerify / dead-code attraction | 要求 RHS non-execution 与 return value 都已正确，只有 mutation/post-state 泄漏 |
| 3 | **Retrieval-Practice-Induced Forgetting** | active retrieval 对竞争 trace 的 delayed selective suppression | fan effect；one-to-many `promote→suppress`；Part-List Cue | manipulation 必须是 active retrieval vs matched restudy，target 必须是 delayed `Rp−`，不是已生成 token |
| 4 | **Noninferiority → Equivalence Collapse** | one-sided relation → symmetric relation promotion | clinical claim verification / trial summarization | NI design、margin、CI、`NI ≠ equivalence` 均先验收后，summary 才发生对称化 |
| 5 | **Surrogate → Clinical-Outcome Promotion** | endpoint-role/validation → allowable claim-level gate | surrogate evaluation / clinical summarization | causal relation本身不够；必须在 surrogate identity 和 validation status 已正确时非法升级 target outcome |
| 6 | **Harmless-Error → Remedy Collapse** | error existence × prejudice → remedy entitlement | generic legal rule following / judgment | error 与 harmlessness/prejudice 均先验收，只看 remedy head 是否只读 binary error |
| 7 | **SQL UNKNOWN Interface Collapse** | same 3VL truth state → interface-specific acceptance gate | text-to-SQL / NULL reasoning | `UNKNOWN` 与单个 interface 规则都能说对，但 `WHERE`/`CHECK` 等实际执行映射错误 |
| 8 | **Subgroup-Significance → Interaction Promotion** | within-group tests → between-effect interaction gate | causal/subgroup analysis LLM；经典 subgroup reporting | 直接验收 interaction p-value 不显著；错误只允许是“显著/不显著差异”非法晋升成 heterogeneity |
| 9 | **Competing-Event → Censoring Collapse** | absorbing competing event → target-risk risk-set operator | survival-analysis QA / causal pitfalls | competing event 身份与“precludes target”均正确后，仍把它送进 ordinary censoring estimator |
| 10 | **Stock–Flow Correlation Intrusion** | flow integration / accumulator operator | FinIndices stock-flow caliber alignment；general numeracy | 要求 `ΔS=I−O` 和 net-flow sign 都算对，只允许 stock trajectory 跟 salient inflow pattern 而错 |

最终规范文件：[`BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md)。

---

## 3. reviewer-mode 新杀掉 / 从早期 survivor 移出的题

### 3.1 Composite → Component Benefit Projection

**裁决：`KILL / ROUTE F6 + OIR collective→member`。**

它有非常自然的医学实例：composite endpoint 显著不蕴含每个 component 都显著。但是仓库已经把 collective/global predicate 广播到每个 member 作为 OIR/F6 类型登记；若局部 component value 都读对，summary 把 super-node 的属性继承给 member，本质仍是整体→成员投射。医学 endpoint 只是优质外部 setting，不足以产生新母算子。

禁止复活方式：`overall endpoint → death/hospitalization`、`bundle → every component`、`index → every constituent` 若没有额外非布尔 operator，一律 ROUTE。

### 3.2 Appellate-Deference Override

**裁决：`HOLD / NOT FINAL-10 (D0)`。**

概念上仍有独立 operator：`merits disagreement × review standard → permissible override`。本轮没有发现 exact LLM collision。但现实案件中 de novo / clear-error / abuse-of-discretion 常与 issue type、record posture 一起变化；若人为把完全同一案件只换 review standard，容易构造法律上不自然或不合法的 matched pair。D0 不如最终十题硬，所以不占十强。

可复活条件：找到真实同一/高度 matched legal material，且 review-standard swap 的 gold 能由正式 doctrine 冻结，不依赖自造假案件。

### 3.3 ITT ↔ Per-Protocol Conclusion Routing

**裁决：`NOT-ADDED / causal-estimand mother risk`。**

ITT 与 PP 回答不同 estimand/政策问题，现实意义很强；但若只是“模型知道 ITT/PP 不同仍选错结论”，容易被更宽的 causal estimand / selection bias / analysis-set routing 吸收。且与 NI trial 已在最终十强，领域多样性也差。

可复活条件：找到一个不是“统计术语不懂”的结构性 wrong destination，例如已正确计算两个 estimand，但 policy decision 选择性把 PP treatment effect 写成 assignment-policy effect，并有跨 trial-design 的一致 operator。

---

## 4. 新脑暴后保留为 reserve、但未进十强

### R1. Immortal-Time Backfill

**核心：** treatment/exposure 在未来时点才定义，模型却把必须存活到该时点的过去 person-time 反向归入 treated group。

优点：future membership → past interval 的时间索引错误非常具体；可由真实 cohort definitions 和程序计算冻结。

未进十强原因：ICLR 2026 causal-pitfall/selection-bias 母区已经很拥挤；目前还需证明它不是“selection bias + temporal alignment”普通实例。若以后发现 `treatment-start time correct + immortal interval recognized + group person-time still backfilled` 的稳定 signature，可重新审。

### R2. DNR-Scope Overextension

**核心：** 模型正确解释 DNR/DNAR 只限制 CPR，却把它扩展为“不治疗感染/不输液/不做其他适当治疗”。

自然规范很硬：DNR 与其他治疗 withholding 是不同 scope。临床安全意义高。

未进十强原因：容易与 generic instruction/scope/authority F1/F7 合并，也有现成 clinical-safety work 测 override DNR orders。只有 `scope readout correct → non-CPR care selectively suppressed` 且错误跨真实 note/orders 稳定，才有资格重开。

### R3. Prediction-Interval → Confidence-Interval Collapse

**核心：** 模型知道 CI 针对平均/参数、PI 针对未来个体，实际给单个未来对象做风险范围时仍使用窄 CI。

优点：target quantity 明确、可执行 oracle 强、关系比普通 numeracy 更结构化。

未进十强原因：目前仍像统计知识迁移题，机制独立性弱于 NI/interaction/competing-risk；若发现 `interval type recognition intact + formulas individually correct + downstream target routing systematic`，可再审。

### R4. Hazard → Risk Promotion

**核心：** 模型知道 hazard ratio 不是固定时间窗 absolute risk ratio，却在 patient-facing summary 中把 HR 直接写成“风险降低 X%”。

未进十强原因：医学传播里这个问题过于成熟，也容易退化为术语/统计 literacy。除非出现时间轴结构预测或 internal target-type binding 机制，否则不占题。

### R5. Conditional-Recommendation → Universal-Action Promotion

**核心：** guideline 明确是 conditional/weak recommendation，模型也读对 certainty/strength，却在下游计划中变成“所有人都应当做”。

未进十强原因：很容易被 F7 正式规则 vs 熟悉默认、或 generic modal-to-action routing 吸收。需要独立的 patient-value/conditional branch operator 才能重开。

### R6. Finally/Cleanup Double-Apply

**核心：** 模型正确模拟 `try/finally` 的控制流，却在异常路径/return path 中把 cleanup side effect 执行两次或漏一次。

未进十强原因：与已有 CSS exception/side-effect/transaction 类卡距离过近；可作为 Short-Circuit Side-Effect Leakage 的外部分布，暂不 standalone。

---

## 5. 新一轮大量脑暴：直接死亡/降级

下面主题在本轮继续搜索中出现过，但没有进入 reserve。记录它们是为了防止后续换名复活。

| 主题 | 裁决 | 原因 |
|---|---|---|
| **Prediction interval vs confidence interval（宽版）** | `RESERVE, not top10` | target-type operator尚可，但很容易退化成统计知识；见 R3 |
| **DNR = do-not-treat** | `RESERVE, scope/F7 risk` | 临床规范硬，但泛 scope error 与临床安全工作已近；见 R2 |
| **Hazard ratio = absolute risk reduction** | `NOT-ADDED` | 统计/医学传播常识占位密，缺独立机制 |
| **ITT vs PP** | `NOT-ADDED` | causal estimand / selection-bias 母题可吸收，且 Batch-2 临床题已多 |
| **Per-protocol = real treatment efficacy** | `NOT-ADDED` | 同上，容易成为术语/因果知识题 |
| **Immortal-time bias** | `RESERVE` | future-membership backfill 有独特性，但 selection-bias 母区拥挤 |
| **Censoring = no event** | `ROUTE F8 / survival knowledge` | 若只把 censored 当 event-free/false，就是 known/unknown 混淆；必须像 competing-risk 那样有独立 absorbing-event operator |
| **Cause-specific hazard = cumulative incidence** | `NOT-ADDED` | statistical target confusion；若无 recognition-intact routing 不够 |
| **Confidence interval contains 95% of future observations** | `NOT-ADDED` | textbook misconception，单纯复现不够 |
| **Prediction interval = CI because both 95%** | `RESERVE only` | 只有 target routing intact/usage wrong 才可能升格 |
| **Multiplicity .05 default override** | `ROUTE/F7 risk` | 早期 ledger 已记录；正式 threshold vs familiar .05 太像 F7 |
| **Optional stopping/p-hacking** | `NOT-ADDED` | sequential evidence/statistical rule 母区已有大量工作，缺独立 operator |
| **Stock vs flow caliber in financial ratios** | `OCCUPIED / not our Stock–Flow` | FinIndices 已覆盖 financial caliber alignment；禁止把其换名成 accumulation 新颖性 |
| **Generic trend extrapolation** | `NOT-ADDED` | 如果不冻结 net-flow equation，只是趋势启发式/forecast bias |
| **Queue length vs arrival-rate trend** | `ROUTE Stock–Flow` | 若最终 Stock–Flow 成立，这是其自然外部分布，不另开题 |
| **Inventory vs sales trend** | `ROUTE Stock–Flow` | 同上 |
| **Bank balance vs income trend** | `ROUTE Stock–Flow` | 同上 |
| **Generic subgroup overclaim** | `NOT-ADDED` | 必须锁死 `within-group p values ≠ interaction`; 其他 subgroup reporting 不作为同一题 |
| **Subgroup A significant/B nonsignificant = interaction** | `SURVIVOR as #8` | 只有 interaction value已正确读取仍晋升时才算 |
| **Competing risk = ordinary censoring** | `SURVIVOR as #9` | 只有 competing-event role/preclusion已识别仍送错 estimator 时才算 |
| **Composite endpoint = every component** | `KILL/ROUTE F6` | 场景不同不能救整体→成员广播 |
| **Appellate disagreement = reversal** | `HOLD` | operator独立但 D0 matched design 不够硬 |
| **Legal error = automatic remedy** | `SURVIVOR as #6` | harmless/prejudice gate 可由 doctrine 与 cases 冻结 |
| **Burden holder = more likely wrong** | `NOT-ADDED` | 若 evidence 已有方向，不是 null-case default operator；必须冻结 unresolved |
| **Surrogate improvement = biomarker causal effect** | `NOT-ADDED` | 本题不是因果边存在与否，而是 surrogate validation→target-claim gate |
| **NI = no statistically significant difference** | `NOT-ADDED` | 若模型没读懂 NI design，是基础 trial/statistics error；survivor要求 NI 语义已正确 |
| **SQL NULL = false everywhere** | `ROUTE/F8` | survivor必须先正确表示 UNKNOWN，再错 interface mapping |
| **Short circuit return value wrong** | `NOT OUR PHENOTYPE` | 这是基础执行错误；survivor要求 return/value path 已正确 |
| **RIF = repeated mention forgets others** | `KILL/ordinary interference` | active retrieval vs passive restudy 是硬分界 |

---

## 6. 这轮用于校准 strongest-neighbor / normative edge 的关键资料

以下资料不是“证明新颖”的清单，而是本轮 reviewer-mode 用来**主动压缩题面**的代表性边界：

- ACL/EMNLP/NAACL 的 legal judgment、causal/subgroup、code execution、clinical summarization 邻域；
- `Promote, Suppress, Iterate`：one-to-many factual generation 已存在 answer suppression 机制，因此 RIF 必须是 delayed active-retrieval effect；
- subgroup 统计学经典原则：**一组显著、另一组不显著，不等于两组效果显著不同**，必须做 interaction；
- noninferiority vs equivalence 的一侧/两侧设计差异；
- SQL 三值逻辑：WHERE 只接受 TRUE，而 CHECK 等接口对 UNKNOWN 的处理不同，可由真实 DB oracle 冻结；
- competing risks：把 competing event 当 ordinary censoring 会改变 cumulative incidence interpretation/estimation；
- stock-flow 人类研究的核心是 accumulation 与 surface flow pattern 的分离，不等同于财务报表里的 stock/flow caliber ratio alignment。

正式 independent N0 必须继续做 citation chaining、全文/appendix 搜索；这里的 `未发现 exact` 不写成绝对 priority claim。

---

## 7. 下一步攻击顺序

不是马上跑模型。先给 10 题各找一个真正反方 reviewer，优先顺序按死亡风险而不是喜好：

1. **RIF**：最强近邻很多，先查 active retrieval / delayed competitor suppression 是否已在 appendix 做过；
2. **Surrogate**：搜 clinical summarization / evidence synthesis 中 surrogate→patient benefit 的专门 error taxonomy；
3. **Burden**：读 FocalLaw/LegalBench/CourtReasoner appendix，看是否已有 burden-recognition-intact 的 matched disposition；
4. **Harmless Error**：查 appellate reasoning benchmark 是否把 error/prejudice/remedy 分阶段标过；
5. **Subgroup Interaction**：查 clinical LLM summarization/error analysis 是否已经专门统计过 interaction-overclaim；
6. **Noninferiority**：查 trial summarization/claim verification 是否已有 NI→equivalence structured label；
7. **SQL UNKNOWN**：查 text-to-SQL/SQL execution benchmarks 是否有 WHERE/CHECK same-UNKNOWN cross-interface contrast；
8. **Short Circuit**：查 code-simulation appendix 是否有 non-executed RHS side-effect state question；
9. **Competing Risk**：查 LLM statistical/survival-analysis benchmark 是否覆盖 `competing event recognized → estimator selection`；
10. **Stock–Flow**：查 system-dynamics / quantitative-reasoning LLM papers与 supplement；避免把 human stock-flow failure 直接搬运却没有 LLM 独立机制。

任一项出现 exact/mother coverage：**永久 KILL/ROUTE，再从 reserve 补位，不维持数量。**