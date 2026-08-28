# 第二批十题 shortlist V2：第四刀 item-level N0 后（2026-08-28）

状态：`REVIEWER-MODE-N0-SURVIVOR / AWAITING EXTERNAL INDEPENDENT SIGN-OFF / NOT DISPATCHABLE`

```yaml
batch: 2
revision: 2
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
survivor_count: 10
supersedes_for_current_shortlist: BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md
```

本文件是第二批**当前**十题 shortlist。旧版保留为第三刀历史快照；第四刀发现 `Retrieval-Practice-Induced Forgetting` 在标准 transformer runtime 中缺少可独立保持的 retrieval-operation state，因此正式撤出。详细死亡与替补审计见：

- [`audits/BATCH2_FOURTH_PASS_ITEM_LEVEL_2026-08-28.md`](audits/BATCH2_FOURTH_PASS_ITEM_LEVEL_2026-08-28.md)
- [`audits/BATCH2_THIRD_PASS_ATTACK_2026-08-28.md`](audits/BATCH2_THIRD_PASS_ATTACK_2026-08-28.md)
- [`BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md`](BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md)

这里的 `SURVIVOR` 不是 formal `N0-PASS`，更不授权 smoke。

---

## 当前十题

| # | 题目 | decisive contrast | 独立 operator |
|---:|---|---|---|
| 1 | **Burden-Placement Null-Case Reversal** | 事实两边都 unresolved、burden 也读对，只交换 burden holder，default disposition 却不翻转 | unresolved-state → losing-side default allocator |
| 2 | **Short-Circuit Side-Effect Leakage** | RHS 被正确判定“不执行”、return value 也正确，post-state 仍加入 RHS mutation/call | shared execution gate → value/effect 双通道 |
| 3 | **Correlation → Agreement / Interchangeability Promotion** | high correlation 与 poor absolute agreement 都读对，仍宣称两方法可互换；`+c` 保持 r 却恶化 agreement | association metric → interchangeability relation gate |
| 4 | **Noninferiority → Equivalence Collapse** | 合法 NI design、margin/CI 与单侧含义都读对，模型自己仍把 `noninferior` 升格为对称 `equivalent` | one-sided relation → symmetric relation promotion |
| 5 | **Surrogate → Clinical-Outcome Promotion** | surrogate role 与 validation status 都正确，仍把 surrogate improvement 升级成患者 clinical benefit | endpoint role/validation → allowable target-claim gate |
| 6 | **Harmless-Error → Remedy Collapse** | error existence 与 prejudice/harmlessness 都判断正确，remedy 仍退化成 `error=true → reverse` | violation finding × prejudice → remedy entitlement |
| 7 | **SQL UNKNOWN Interface Collapse** | predicate 正确算成 `UNKNOWN`，各 interface 规则单独也会说，却把 WHERE/CHECK 的 UNKNOWN 映射成同一 policy | truth state → interface-specific designated-value gate |
| 8 | **Subgroup-Significance → Interaction Promotion** | A subgroup 显著、B 不显著，interaction 明确不显著且模型读对，仍宣称 treatment effect 随 subgroup 不同 | within-group tests → between-effect interaction relation |
| 9 | **Competing-Event → Censoring Collapse** | competing event 被正确识别为阻止 target event，最终 risk-set/estimator 仍把它当 ordinary censoring | event role → survival risk-set transition operator |
| 10 | **Stock–Flow Correlation Intrusion** | `ΔS=I−O` 与每段净流量符号都正确，stock trajectory/peak 却追随 inflow 表面走势 | net-flow integration → stock accumulator |

---

# 1. Burden-Placement Null-Case Reversal

**Natural invariant.** Burden of proof 不告诉事实真假，而规定证据未解决争议时谁承担不利后果。

**Admission test.** 必须先验收：`E ⊬ P`、`E ⊬ ¬P`、burden holder 正确、burden rule 正确；随后交换 burden placement 才看 disposition。

**Strongest mother.** FocalLaw / LegalScope 已证明真实 legal reasoning 有 dispute-focus/constraint-extraction bottleneck，burden 不是空白领域。因此不能声称“LLM 不会 burden”。

**why_not_a_rename.** 本题只研究 `unresolved → default loser` 的离散 allocator；不是 confidence、authority 或普通 rule omission。

**Mechanism split.** (A) verdict head 没有 null-case gate；(B) gate 存在但 party↔claim binding 错；(C) procedural rule只进解释 writer。

**Hard kill.** burden/readout 不稳、现实 matched gold 不可冻结、或已有 benchmark 完整做 `unresolved × burden swap → disposition`。

---

# 2. Short-Circuit Side-Effect Leakage

**Natural invariant.** `A || B`/`A && B` 的 RHS 若被短路，不仅不能改变 return value，也根本不能产生 side effect。

**Admission test.** LHS、RHS non-execution、return value 三项先全部正确；只有 post-state/call count 允许错。

**Strongest mother.** ACL 2026 Findings CoRE 已发现 `correct final output + wrong intermediate state` 的 Superficial Execution。故宽“执行过程错”已被占领。

**why_not_a_rename.** 本题要求**同一个 execution gate 对 value path 正确、对 effect path 失效**，并可跨 `&&/||/guard/ternary` 检验共享 gate。

**Mechanism split.** (A) effect updater eager-executes显式 call；(B) trace正确、state summarizer lexical-reconstruct；(C) RHS effect在 gate 前已写 state。

**Hard kill.** CoRE/ExecVerify item-level 已包含 exact cross-channel condition，或 RHS non-execution/return 本身就错。

---

# 3. Correlation → Agreement / Interchangeability Promotion

**Natural invariant.** 高 correlation 只说明共同变化/排序关系，不保证 absolute agreement 或 methods interchangeable。`y' = y + c` 可保持 Pearson r 完全不变，同时把 method bias 增加 c。

**Admission test.** correlation、Bland–Altman bias/LoA（或 CCC/absolute ICC）全部读对，并能口头说“correlation alone does not establish agreement”；最后 method-comparison conclusion 仍因高 r 宣称 interchangeable 才计入。

**Strongest mother.** 2025–2026 很多 LLM evaluation 论文已经把 correlation、kappa/ICC、Bland–Altman 分开使用，甚至观察到高 rank correlation 与差 categorical/absolute agreement并存；这些研究测的是**LLM与人类是否一致**，不是 LLM 自己是否做错误 metric→relation promotion。

**why_not_a_rename.** 不是 generic metric confusion：`+c` / scale transformation 给出 correlation-preserving、agreement-changing 的严格不变量；interchangeability judgment 若跟 r 而非 agreement 走，就有结构 signature。

**Mechanism split.** (A) single “methods-match” goodness scalar；(B) metric-role binding错，interchangeability query误读 association；(C) high-r salience晚层压过 LoA/bias path。

**D0.** 真实 paired measurement/device/lab/rater data + Bland–Altman/CCC 计算 oracle；至少一处分布来自非医学 measurement comparison。

**Hard kill.** agreement metric本身读不对、仅教材模板有效、或已有 LLM paper 做 recognition-intact→interchangeability wrong 的 exact phenotype。

---

# 4. Noninferiority → Equivalence Collapse

**Natural invariant.** NI success 是单侧的 `not worse than comparator by more than Δ`；不自动等于对称 equivalence。

**Admission test.** 必须是真正合法 NI design；model 正确读 margin/CI、正确解释 `NI ≠ equivalence`，中性原始 trial material 不带该 spin；模型自己在 downstream summary 才对称化。

**Strongest mother.** MedLitSpin / `Caught in the Web of Words` 已经直接包含 `Claim equivalence/non-inferiority versus control for a (-) endpoint` 的 clinical-spin label，并证明模型会识别 spin 但仍被影响。因此“无显著差异→等效/非劣”的宽故事已经不能做。

**why_not_a_rename.** 仅保留反向而严格的 operator：**valid one-sided NI relation → model-generated symmetric equivalence**，不是被 source 中错误 equivalence 文案诱导。

**Mechanism split.** direction bit 在 relation representation 中丢失；或 relation完整但 summary decoder 把“not worse”默认翻译为“same”。

**Hard kill.** MedLitSpin/其他数据已有 neutral true-NI cases + recognition-intact equivalence promotion；或 effect 只在 source 本身 spin 时出现。

---

# 5. Surrogate → Clinical-Outcome Promotion

**Natural invariant.** Surrogate endpoint 是对 clinical benefit 的替代/预测指标；是否足以支持目标 clinical claim 取决于 validation 与 context of use。

**Admission test.** surrogate identity、validation status、无 direct target-outcome evidence 三项均正确；模型甚至能陈述 inference boundary，随后才允许观察 clinical promotion。

**Strongest mother.** medical-spin、clinical summarization、surrogate-analysis platform 已很近；因此不能写“LLM 会过度解读 biomarkers”。

**why_not_a_rename.** operator 是 `endpoint role × validation status → allowable claim level`；不是 correlation≠causation，也不是单纯医学知识。

**Mechanism split.** positive “improvement”在 summary writer 广播到 target；或模型默认补 surrogate→clinical validation edge。

**Hard kill.** gold 有专业争议、source 自己已经声称 clinical benefit、或最强工作已 exact 做 recognition-intact promotion。

---

# 6. Harmless-Error → Remedy Collapse

**Natural invariant.** 发现法律错误不等于自动 reversal/new trial；harmless/prejudice gate 决定 remedy entitlement。

**Admission test.** `error=true`、harmless/prejudice standard、当前 error 的 prejudice classification 都先正确；只有 final remedy 允许错。

**Strongest mother.** CourtReasoner/FocalLaw/LegalScope 已覆盖复杂法律 rule/constraint/conclusion reasoning，但公开 repo/data 未见该三阶段 exact phenotype。

**why_not_a_rename.** `rights/error finding` 与 `remedy` 是制度上分离的算子；不是普通 authority 或 rule omission。

**Mechanism split.** binary violation scalar压过 severity/prejudice；或 remedy head只读 error flag。

**Hard kill.** prejudice classification 本身错、案件 gold 不可冻结，或 benchmark 已明确阶段化测试 `error × prejudice → remedy`。

---

# 7. SQL UNKNOWN Interface Collapse

**Natural invariant.** SQL 3VL 的 UNKNOWN 不等同于全局 false。典型 SQL 语义下，WHERE 只保留 TRUE，而 CHECK 只拒绝 FALSE，因此 UNKNOWN 在两种 interface 的 designated-value policy 不同（具体 dialect 必须冻结）。

**Admission test.** predicate=UNKNOWN 正确，各 interface 规则单独问也正确；same UNKNOWN 放到两个接口时 execution prediction 才允许错。

**Strongest mother.** ICLR 2026 under-review Squirrel-Semantic 已明确包含 NULL/three-valued-logic error taxonomy。所以 generic NULL/3VL reasoning 已占领。

**why_not_a_rename.** 独立对象是 `truth state → interface policy`；不是 UNKNOWN→false 的 F8，因为 truth state 本身先验收正确。

**Mechanism split.** executable layer压成二值 truthiness；或 UNKNOWN保留但 interface selector 不进入 reducer。

**Hard kill.** dialect 不一致无法冻结，或 Squirrel/SQL benchmark 已含 same-UNKNOWN WHERE/CHECK matched pair。

---

# 8. Subgroup-Significance → Interaction Promotion

**Natural invariant.** `p_A<.05` 且 `p_B>.05` 不推出 treatment effects 在 A/B 间显著不同；必须直接检验 treatment×subgroup interaction。

**Admission test.** subgroup p-values、effect estimates、interaction test 都提供；model 明确读出 interaction 不显著，最后才看是否仍宣称 heterogeneity。

**Strongest mother.** trial spin/subgroup overclaim 是成熟医学统计问题；MedLitSpin 宽 mother 占领“临床摘要被 spin 影响”。目前其公开文本/labels 未见 recognition-intact non-significant interaction→heterogeneity exact factorial。

**why_not_a_rename.** 数学 operator 唯一：`within-group hypothesis tests` 不能替代 `between-effect interaction test`。

**Mechanism split.** significance labels进入 categorical contrast heuristic；或 interaction result只进 verifier、不进 summary relation decoder。

**Hard kill.** 不提供 interaction test、interaction本身读错、或已有 clinical LLM error taxonomy exact 做该 contrast。

---

# 9. Competing-Event → Censoring Collapse

**Natural invariant.** Competing event 已发生后会阻止 target event；把它当 ordinary independent censoring 会错误构造风险集/CIF。

**Admission test.** competing-event type、其 preclusion relation、censoring meaning均先正确；只有 estimator/risk-set routing 允许错。

**Strongest mother.** competing-risk统计/ML方法极成熟，2026仍有 benchmark/calibration 工作；当前 exact search 未找到 LLM reasoning/mechanism paper测试该错误。

**why_not_a_rename.** 不是 generic censoring knowledge：错误必须发生在 `absorbing event role → risk-set transition`。

**Mechanism split.** event label正确但 risk-set builder只有 event/censored二值槽；或 cause-specific representation存在但 estimator selector走普通 KM/Cox 默认路径。

**Hard kill.** 模型不知道 competing risk；或 LLM survival benchmark 已阶段化做 recognition-intact estimator routing。

---

# 10. Stock–Flow Correlation Intrusion

**Natural invariant.** Stock 的变化由净流量积分决定：`ΔS=I−O`。Inflow 即使正在下降，只要仍大于 outflow，stock 仍在增加。

**Admission test.** 公式、每段 inflow/outflow、net-flow sign 先全部正确；只看 stock trajectory、turning point、peak 是否仍跟 salient inflow pattern 走。

**Strongest mother.** 人类 stock–flow failure/correlation heuristic 文献成熟；2023 有非正式 ChatGPT Department Store 尝试。2026 FinIndices 的 `stock-flow caliber` 指财务 ratio 的 period/average-stock 对齐，不是 accumulation operator。当前未见顶会 LLM mechanism paper正面占位。

**why_not_a_rename.** 不是 generic arithmetic/trend extrapolation：必须在 net flow 已正确的情况下，stock readout仍追随单一 flow 的 shape。

**Mechanism split.** correlation heuristic path直接把 salient inflow映射到 stock trend；或 net-flow计算存在但 accumulator/temporal integration receiver没消费。

**D0.** Department Store/queue/inventory/reservoir等成熟 stock-flow tasks + 真实时序；外部 oracle按差分/积分严格计算。

**Hard kill.** net flow 本身算错、只在图表读数出错、或正式 LLM stock-flow paper 已做 components-intact correlation-heuristic phenotype。

---

## 当前风险顺序

按下一轮最可能死亡排序：

1. **Noninferiority → Equivalence** — MedLitSpin item taxonomy 已非常近；
2. **Short-Circuit Side-Effect Leakage** — CoRE mother 强；
3. **Surrogate → Clinical Outcome** — medical spin/summarization mother 强；
4. **Burden Null-Case** — legal constraint extraction mother 强；
5. **Harmless Error**；
6. **Subgroup Interaction**；
7. **Correlation→Agreement**；
8. **SQL UNKNOWN Interface**；
9. **Stock–Flow**；
10. **Competing Risk**。

任一题出现 exact/mother coverage 立即 KILL/ROUTE；优先从 reserve/new discovery 补，不复活 RIF。