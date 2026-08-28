# Batch-2 第三刀：strongest-neighbor / mother-inclusion 再攻击（2026-08-28）

状态：`THIRD-PASS COMPLETE / 10 REMAIN REVIEWER-MODE SURVIVORS / NO FORMAL N0 / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
third_pass_survivors: 10
third_pass_kills: 0
```

本文件不是再次为候选辩护，而是对 [`../BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md`](../BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md) 做第三轮反方攻击。重点不是搜同名，而是找一篇能把候选的 decisive contrast **逻辑上包进去** 的 strongest neighbor。

结论：本轮没有出现足以直接 KILL 的 exact/mother collision，但风险分层发生变化。**RIF、Short-Circuit、Surrogate/NI** 仍是最应该优先交给真正独立 reviewer 的四条；**SQL UNKNOWN、Competing-Risk、Stock–Flow** 的 operator 边界目前相对最硬。

---

## 1. Retrieval-Practice-Induced Forgetting — `SURVIVE / HIGH MOTHER RISK`

### strongest neighbor

EMNLP 2025 Main:

- Yan & Jia, [Promote, Suppress, Iterate: How Language Models Answer One-to-Many Factual Queries](https://aclanthology.org/2025.emnlp-main.815/)

该文已经给出非常具体的 one-to-many factual retrieval 机制：模型先 promote 所有可能答案，再利用**previous answer tokens** 抑制已经生成的答案，并用 causal tracing / Token Lens / knockout 定位 attention 与 MLP 的贡献。

因此以下宽主张已经死亡：

```text
生成一个答案会改变其他答案的 logit
one-to-many recall 存在 answer suppression
前文答案 token 会控制后续列表检索
```

### 为什么 RIF 暂时仍独立

RIF 的 manipulation 不是“刚刚生成 A 后继续生成 B”，而是：

```text
active retrieval practice of Rp+
vs matched passive restudy of Rp+
→ delay / context break
→ test related-unpracticed Rp-
```

必须同时满足：

1. `active retrieval` 比 `restudy` 产生额外损失；
2. 损失选择性落在同类别 `Rp−`，不是 unrelated item；
3. 不是当前 list generation 的 repetition avoidance；
4. 改 cue / recognition-vs-free-recall / delay 后出现与 inhibition vs competition 理论不同的结构。

本轮 exact search 未发现 LLM 论文完整使用心理学 RIF 的 `retrieval-practice / restudy / Rp+ / Rp− / Nrp` paradigm。

### hard-kill refresh

若 Yan & Jia appendix/code 中存在**外部提供 previous answers、跨任务 delay 后未提示 competitor 持续下降、且 passive restudy control 已做**，RIF 直接 KILL；不能靠换成 QAMPARI 续命。

---

## 2. Short-Circuit Side-Effect Leakage — `SURVIVE / HIGH MOTHER RISK`

### strongest neighbor

ACL 2026 Findings:

- Gao et al., [CoRE: A Fine-Grained Code Reasoning Benchmark Beyond Output Prediction](https://aclanthology.org/2026.findings-acl.460/)

CoRE 已经定义两个宽问题：implementation invariance 与 process transparency；其核心发现之一是 **Superficial Execution**：模型 final output 正确，但 intermediate execution states 错误。它使用 Arithmetic / Logic / State / Boundary 四类 intermediate probes。

另有 ACL 2026 Main `ExecVerify` 与 NeurIPS 2025 static-analysis CoRe 等代码执行/控制依赖邻居。

### mother-inclusion attack

若我们的现象只写成：

> 模型最后 return value 对，但某个 state 错。

则已经被 CoRE 的 `superficial execution` 完整包含，不能 standalone。

### 为什么暂时仍独立

唯一可保留合同必须锁死为**同一个 short-circuit gate 的双通道路由不一致**：

```text
model: LHS already decides expression       ✓
model: RHS is not executed                   ✓
model: expression return value               ✓
model: post-state/call-count contains RHS effect   ✗
```

也就是模型不是“不会执行代码”，而是 explicit execution decision 已正确，却只有 `effect-store updater` 像 eager execution。

这产生 CoRE 宽现象没有规定的结构预测：

- pure RHS 与 side-effectful RHS 应选择性分离；
- value path patch 不一定修 effect path；
- RHS call token 对 post-state 的 causal effect 应在 short-circuit condition 下仍异常保留；
- matched `if` / ternary / guard / `&&` / `||` 可检验是否共享 execution gate。

本轮在 CoRE 文本中未检到 `short-circuit`、`side effect`、`mutation` 的 exact cross-channel contrast。

### hard-kill refresh

若 independent reviewer 在 CoRE/REval/ExecVerify appendix 或 dataset 找到：

```text
RHS non-execution recognized
+ final return correct
+ side-effect/post-state wrong
```

并已作为 process-transparency failure 分析，则 standalone KILL，最多作为 CoRE 外部机制 case study。

---

## 3. Burden-Placement Null-Case Reversal — `SURVIVE / MEDIUM MOTHER RISK`

### strongest neighbors

- LEGALSCOPE: legal real-case rubric 已把 burden of proof 纳入 `constraint extraction`，并记录 condition omission / conclusion jump 等错误；
- `2CANLEGALRAGBENCH` error taxonomy 甚至出现 reasoning 找到 burden、conclusion 却错误说证据不足的例子；
- `Judicial Requirements for Generative AI in Legal Reasoning` 把正确适用 burden of proof 明确列为司法推理要求；
- 2026 legal reasoning/test-time-scaling 工作也报告 specialized concepts 如 burden of proof 仍会造成错误。

因此“LLM 会漏用 burden of proof”已经不能作为 discovery claim。

### 为什么暂时仍独立

本题只保：

```text
E neither establishes P nor establishes ¬P
burden holder correctly identified
burden rule correctly stated
```

然后只比较 null-case/default disposition。

burden 在这里不是事实证据，也不是 confidence scalar，而是 `unresolved → loser` 的离散 allocator。只要 evidence 有方向、burden 本身没读对、或结论只是泛 argument-validity 失败，都不计入。

本轮未找到 same-evidence `burden swap × unresolved → disposition` factorial。

---

## 4. Harmless-Error → Remedy Collapse — `SURVIVE / MEDIUM MOTHER RISK`

广泛 legal-reasoning benchmarks 已覆盖 rule application、constraint extraction、argument validity 和 conclusion jump，但本轮没有找到把：

```text
error existence correct
prejudice/harmlessness correct
→ remedy entitlement wrong
```

作为分阶段 matched phenotype 的 LLM 工作。

法律学术中的 `harmless AI error` 是讨论法院如何对 AI 相关错误适用 harmless-error doctrine，不是评估 LLM 自己能否维持 `error ≠ automatic reversal`。

**边界：** 若只发现模型漏读 harmlessness 或不懂 doctrine，题死；必须是 remedy head 绕过已正确的 prejudice gate。

---

## 5. Noninferiority → Equivalence Collapse — `SURVIVE / HIGH DOMAIN-MOTHER RISK`

### strongest mother

临床 NLP 已长期研究 trial-reporting spin。2020 BioNLP 自动 spin 工作已经检测：

- 非显著结果被错误解释为 treatment similarity；
- trial design 是否允许 similarity/equivalence claim；
- within-group comparison 等。

2025 CHIL/PMLR:

- Yun et al., [Caught in the Web of Words: Do LLMs Fall for Spin in Medical Literature?](https://proceedings.mlr.press/v287/yun25a.html)

更直接证明 22 个 LLM 会受 RCT abstract spin 影响，并把 spin 传播到 plain-language summary；模型还能显式识别 spin，却仍受其影响。

所以“模型会过度解读 trial / 能识别问题却仍在 summary 传播”这个宽故事已被占领。

### 为什么 NI 题暂时仍独立

唯一可保留 operator 是：

```text
NI design correctly identified
margin + CI correctly read
model explicitly states NI is one-sided and does not establish equivalence
neutral/raw trial result (not source spin manipulation)
→ downstream relation becomes symmetric `equivalent`
```

这是 `one-sided relation → symmetric relation promotion`，不是“原文有 spin 所以模型跟着 spin”。

本轮未找到 LLM paper 把该 exact relation promotion 系统化。但它是高风险题：如果 clinical spin 数据/appendix 已专门包含 NI success→equivalence 且有 recognition-intact control，直接 KILL。

---

## 6. Surrogate → Clinical-Outcome Promotion — `SURVIVE / HIGH DOMAIN-MOTHER RISK`

### strongest mother

Yun et al. 的 spin work 同样占据了“LLM 能识别 spin 但 interpretation/summary 仍被影响”的宽叙事。

2026 `SurroPilot` 已把 LLM 引入 heterogeneous surrogate endpoint evaluation，但目的是用 LLM 辅助统计工作流，不是评估错误 promotion。

FDA/BEST 明确把 surrogate 分为 candidate / reasonably likely / validated；surrogate 本身不是 direct clinical benefit，并且 reasonably-likely surrogate 仍需 confirmatory evidence。

### 为什么暂时仍独立

只允许：

```text
surrogate role correct
validation status correct
no direct target-outcome evidence
model explicitly states allowable inference boundary
→ later summary/action invents target clinical benefit
```

这里错误不是 generic optimism，而是**endpoint-role/validation gate → claim-level** 的越界。

若原始文本自己已经声称 clinical benefit，或模型没读懂 surrogate/validation，均不计入。

---

## 7. Subgroup-Significance → Interaction Promotion — `SURVIVE / MEDIUM-LOW COLLISION RISK`

经典统计学原则很硬：

> `A subgroup significant` + `B subgroup non-significant` 并不等于 A/B treatment effects 显著不同；必须直接检验 interaction。

临床 trial reporting 的 subgroup overclaim/spin 是成熟人类问题；2025 的 LLM medical-spin mother paper会提高母题风险。但本轮没有找到 LLM work 直接做：

```text
p_A significant
p_B non-significant
interaction p-value explicitly non-significant and read correctly
→ model nevertheless declares subgroup treatment-effect heterogeneity
```

独立 operator 是 `within-subgroup tests → between-effect interaction`，其数学 wrong destination 唯一。

**hard kill：** 若只给两组 p-value 而不提供/验收 interaction test，这只是统计能力题；必须让 model 先读对 interaction result。

---

## 8. SQL UNKNOWN Interface Collapse — `SURVIVE / LOW-MEDIUM COLLISION RISK`

2026 SQL benchmark/bug taxonomy 已经直接记录：

- NULL handling errors；
- three-valued logic errors；
- `NOT(a=b)` 与 `a!=b` 在 NULL 下不等价等。

因此“LLM 不懂 SQL NULL/3VL”已经不是新题。

本题唯一独立合同是：

```text
predicate = UNKNOWN                         ✓
WHERE rule stated correctly                 ✓
CHECK/interface rule stated correctly       ✓
same UNKNOWN fed into two interfaces
→ execution policy incorrectly collapsed    ✗
```

也就是 truth state 本身已存在，失败发生在 `truth-state → interface policy`。本轮未找到 WHERE/CHECK matched cross-interface contrast。

---

## 9. Competing-Event → Censoring Collapse — `SURVIVE / LOW COLLISION RISK`

统计学母现象极稳定：competing event 会阻止 target event；把 competing event 当 ordinary censoring 会违反目标风险估计语义，并常造成 cumulative incidence 高估。

2025–2026 的 competing-risk papers主要是方法/估计器/公平性/软件：它们直接强调该统计错误，但本轮未找到**LLM reasoning behavior/mechanism**论文。

因此可保留的现象是：

```text
competing event type identified correctly
model states it precludes target event
censoring meaning separately correct
→ estimator/risk-set construction still routes competing events into censoring
```

如果模型只是“不知道 competing risk 是什么”，立即 KILL。

---

## 10. Stock–Flow Correlation Intrusion — `SURVIVE / LOW-MEDIUM COLLISION RISK`

### natural mother

Cronin, Gonzalez & Sterman 等系统动力学研究把 **stock–flow failure** 作为稳定人类 reasoning phenomenon；核心解释之一是 correlation heuristic：把 stock 的形状错误地当成与 flow 表面走势同步，而忽略 stock 是 net flow 的积分。

### LLM prior

2023 MetaSD 有非正式博客把 ChatGPT 用在 Department Store stock-flow problem；另有 industrial-ecology 博客讨论 ChatGPT stocks/flows。它们必须作为 prior informal evidence 承认，不能声称“从没人试过 LLM”。

但本轮未找到 ACL/EMNLP/NAACL/ICLR/ICML/NeurIPS 或正式 LLM mechanism paper 系统研究 stock-flow failure。

`FinIndices` 一类 2026 finance work 中的 `stock-flow caliber mismatch` 是财务比率里 stock variable 与 flow-period/average-stock 的对齐问题，不等于经典 accumulation operator。

### 为什么题仍独立

不能只问最终 stock 数值。必须先验收：

```text
ΔStock = inflow - outflow                   ✓
net-flow sign at each interval               ✓
inflow/outflow values                        ✓
```

目标错误是 stock trajectory / peak / turning point 仍系统追随 salient inflow curve，而不是累积 net flow。

这直接预测：当 inflow 下降但仍大于 outflow 时，模型会过早预测 stock 已下降；将 net-flow curve 显式化应选择性修复；改变 inflow/outflow 的视觉/文本 salience 可测试 correlation heuristic。

---

# 第三刀风险排序

### Highest mother-inclusion risk

1. **RIF** — EMNLP 2025 已有非常具体 promote/suppress 机制；必须靠 active-retrieval delayed aftereffect 独立。
2. **Short-Circuit** — CoRE 已占 `correct output + wrong intermediate state`；必须靠同 gate 的 value/effect cross-channel dissociation 独立。
3. **NI → Equivalence** — clinical spin 已经是成熟 NLP/LLM mother；必须锁 one-sided→symmetric relation promotion。
4. **Surrogate → Clinical** — 同样受 medical-spin mother 压迫；必须锁 validation-gated endpoint promotion。

### Medium

5. **Burden** — legal constraint extraction 已占；null-case allocator 仍未见 exact。
6. **Harmless Error** — broad legal conclusion-jump 已占；error×prejudice→remedy operator 尚独立。
7. **Subgroup Interaction** — clinical spin mother近，但数学 operator具体。

### Lower current collision risk

8. **SQL UNKNOWN Interface** — NULL/3VL broad occupied，cross-interface gate未见。
9. **Stock–Flow** — 有非正式 ChatGPT prior，正式 LLM mechanism空位仍大。
10. **Competing Risk** — statistics mother很成熟，但目前未见 LLM behavior/mechanism研究。

---

# 当前结论

第三刀**没有因为维持十题而降低门槛**；如果按本轮能查到的 strongest-neighbor 正文/摘要/可搜索 PDF，尚无一题达到 `exact phenotype already studied` 或 `mother logically covers all decisive controls` 的硬杀条件。

但这仍不是 formal independent N0。下一步真正值得投入的不是继续给十题加正面引用，而是：

```text
RIF: inspect PSI appendix/code around previous-answer injection and persistence
Short-Circuit: inspect CoRE / REval / ExecVerify datasets item-level for side-effect probes
NI/Surrogate/Subgroup: inspect medical-spin dataset annotation taxonomy at item level
Burden/Harmless: inspect LEGALSCOPE/FocalLaw/CourtReasoner items, not only paper taxonomy
SQL: inspect Squirrel-Semantic/BIRD null-error items for cross-interface pairs
```

只要 item-level audit 发现 exact factorial，立即改 final shortlist 并从 reserve 补位。