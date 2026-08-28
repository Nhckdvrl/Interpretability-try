# Batch-2 第四刀：item-level / identifiability N0（2026-08-28）

状态：`ONE KILL + ONE REPLACEMENT / 10 CURRENT REVIEWER-MODE SURVIVORS / NOT FORMAL N0 / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
fourth_pass_kills: 1
replacement_count: 1
current_survivor_count: 10
```

本轮不再停在论文 abstract/title。重点检查 strongest-neighbor 的公开 repo/data，以及候选 operator 在标准 transformer runtime 中是否**真的可独立操纵和识别**。

---

## 1. Retrieval-Practice-Induced Forgetting — `KILL / OPERATOR NOT IDENTIFIABLE IN STANDARD LLM RUNTIME`

### 文献边界本身尚未 exact collision

EMNLP 2025 Main `Promote, Suppress, Iterate` 的官方代码仓库把 one-to-many factual generation 按 answer step 组织，并直接围绕 `previous answer tokens` 做 causal tracing / knockout。它仍然没有心理学 RIF 所要求的：

```text
active retrieval practice
vs passive restudy
→ delay
→ related-unpracticed Rp− test
```

所以本轮不是因为 exact paper 已经做完而 KILL。

### 真正死亡理由：标准 LLM 的 active-retrieval state 不可独立保持

人类 RIF 依赖“主动检索”本身对记忆系统留下后效应。但对普通 decoder-only transformer：

- 如果 active retrieval 与 passive restudy 在后测前被严格匹配为**相同 role + 相同 token history**，则后续模型看到的条件上下文相同；标准无持久内存 runtime 中不存在一个独立、可持续的“刚才是主动检索而不是读到”的状态变量。
- 如果为了制造差异，保留 `assistant 自己生成 Rp+` vs `user/system 提供 Rp+`、不同 role token、不同措辞或不同轨迹，则 manipulation 同时改变 source/role/self-conditioning，无法把 effect 归因于 retrieval operation。
- 若引入外部 memory module、在线权重更新或 agent state，则研究对象已变成特定 memory architecture，而不是一般 LLM phenomenon。

因此候选最关键的 `why_not_a_rename` 无法在标准 LLM runtime 中被干净识别。即使观察到行为差，也很难排除 source-role/self-generation/context-path 母题。

**裁决：永久移出 Batch-2 十强。** 未来只有在研究显式 recurrent/persistent-memory architecture 时，才能作为 architecture-specific phenomenon 重开；不得以普通 chat history 重新包装。

---

## 2. Correlation → Agreement / Interchangeability Promotion — `REPLACEMENT SURVIVOR`

### 自然母现象

测量学中，高 Pearson/Spearman correlation 不意味着两种测量方法具有足够 agreement，更不意味着可以互换。系统性偏移可以在几乎不改变 correlation 的同时严重破坏 absolute agreement；Bland–Altman、concordance/ICC 等方法正是为此而存在。

现实例子：设备 B 永远比设备 A 高 10 个单位。二者可以 `r≈1`，但对于需要绝对数值的临床/工程使用，它们显然不能直接互换。

### decisive contrast

选择真实 paired measurement / method-comparison data。先验收：

```text
model correctly computes/reads high correlation
model correctly reads Bland–Altman bias / limits of agreement (or CCC/absolute ICC)
model explicitly says correlation alone does not establish agreement/interchangeability
```

然后要求 method-comparison conclusion / deployment decision。目标错误：

```text
high r  →  methods agree / are interchangeable
```

即使 agreement metric 已明确否定。

### 最强结构轴：correlation-preserving agreement destruction

对真实 paired data 做规范变换：

```text
y' = y + c
```

对于常数 c，Pearson correlation `r(x,y') = r(x,y)`，但 mean bias 增加 c，Bland–Altman agreement 明确改变。正比例缩放也可保持 rank/linear correlation 很高而破坏 absolute agreement。

因此候选不是“两个 metric 冲突时模型选错”，而有一个可证明的不变量：

```text
correlation invariant
agreement changes monotonically with offset/scale distortion
```

若模型的 interchangeability judgment 跟 correlation 保持不变而无视 agreement 变化，就形成非常清晰的 structured signature。

### strongest neighbors

2026 已有多篇工作使用 correlation、ICC、kappa、Bland–Altman 来**评价 LLM 与人类评分的一致性**；其中甚至出现“rank correlation 很强但 categorical agreement 很差”的真实结果。这证明母现象和数据分析工具非常成熟。

ACL Findings 2025 `Is LLM an Overconfident Judge?` 也明确把 Spearman correlation 与 kappa agreement 分开作为评估量。

但是这些工作研究的是**LLM outputs 与人类/其他模型的 agreement**，不是让 LLM 自己读 method-comparison evidence 后是否错误把 high correlation 晋升为 interchangeability。当前 exact search 未找到该 behavior/mechanism phenotype。

### why_not_a_rename

不是普通 numeracy，也不只是 F7“熟悉 metric 压过正式 metric”。独立 operator 是：

```text
association / rank preservation
≠
absolute measurement agreement
→
deployment interchangeability
```

并且 `+c` / scale transformation 给出 F7 泛叙事没有的定量不变量和新预测。

### competing mechanisms

1. **single-goodness-scalar collapse**：high correlation 与 high agreement 被压成同一个“methods match”方向，Bland–Altman信息只在解释层可读；
2. **metric-role binding failure**：correlation 与 agreement 数值都正确表示，但 downstream `interchangeable?` query 错路由到 association metric；
3. **salience competition**：熟悉且高值的 r path 在晚层压过 bias/LoA path；改变 metric presentation/salience 应改变效应，而机制 2 更依赖 query role。

### D0 / hard gold

- 真实 method-comparison paired datasets（临床设备、实验测量、评分者、传感器）可直接计算 Pearson/Spearman、mean bias、limits of agreement、CCC/absolute ICC；
- 公开论文中大量 paired measurement 数据可作为自然锚点；
- transformation stress test 从真实 paired data 出发，不需要凭空造任务；
- gold 由公式和预先冻结的 acceptable-agreement threshold / 原研究结论共同提供。

### hard kill

- 模型连 correlation/agreement 定义或 Bland–Altman 值都读错；
- 只有抽象 textbook 数字题，没有真实 paired data；
- effect 只在没有显式 agreement metric 时出现；
- strongest neighbor 已做 `correlation recognized + agreement metric recognized + interchangeability wrong`；
- `+c` / scale axis 不产生任何结构，错误只是不稳定的 summary noise。

当前：`REVIEWER-MODE-N0-SURVIVOR / awaiting external independent sign-off`。

---

## 3. MedLitSpin item-level refresh：NI / Surrogate / Subgroup

对 `Caught in the Web of Words` 的公开 `MedLitSpin` repo/data 继续查到：

- 数据确实包含 `Claim equivalence/non-inferiority versus control for a (-) endpoint` 这一 spin label，说明“从非显著 superiority result 错误声称 equivalence/noninferiority”已经是其明确研究对象之一；
- 数据也包含 surrogate/subgroup/interaction 等词的真实 RCT abstracts，但目前没有发现它们被做成我们三个 recognition-intact operator 的 factorial label。

### 对 NI 的影响

NI 候选风险**上升**。不得再写“LLM 会把无差异说成等效/非劣”；该行为已经处于 MedLitSpin 的直接 spin taxonomy 中。

唯一可保留版本必须反向且更精确：

```text
source trial is a legitimate noninferiority design
NI success itself is valid
model correctly recognizes one-sided NI relation
model explicitly rejects equivalence inference
→ model itself later promotes valid NI to symmetric equivalence
```

即：不是“被 source spin 骗”，而是模型在 neutral source 上执行 `one-sided → symmetric` relation promotion。

如果后续 item-level audit 找到 MedLitSpin/其他 clinical benchmark 包含真实 NI trial + neutralized text + downstream equivalence promotion，则 NI 直接 KILL。

### 对 Surrogate / Subgroup 的影响

目前仍是 broad mother risk，而非 exact collision：

- surrogate 必须锁 `role + validation status correct → clinical target claim invented`；
- subgroup 必须锁 `interaction test explicitly non-significant and read correctly → heterogeneity still claimed`。

只要没有 recognition-intact gate，这两题就退化为 medical spin / statistical literacy，不计入现象。

---

## 4. CourtReasoner / legal item-level refresh

公开 CourtReasoner repo 对 `harmless`、`prejudice`、`burden` 的代码搜索均无明确命中。论文/仓库的核心是 goal-oriented judicial reasoning、双向论证、invalid arguments 与 citation relevance，不是分阶段 `error→prejudice→remedy` 或 matched burden-default factorial。

FocalLaw/LegalScope 仍是 Burden 的更强 mother：它们把 dispute focus / constraint extraction（包括 burden）作为真实 legal reasoning bottleneck。但尚未看到 `burden recognized + both factual propositions unresolved → default allocator` exact contrast。

因此 Burden/Harmless 本轮不杀，但 formal N0 仍应读取无法公开的 LegalScope full workbook（若可获授权）或 paper appendix 后再签字。

---

## 5. SQL item-level refresh

ICLR 2026 under-review Squirrel-Semantic 的 appendix 已明确列出 SQL bug taxonomy：包括 `three-valued logic error`、NULL comparison、aggregate NULL 等。故 generic `LLM 不懂 SQL UNKNOWN/NULL` 已明确占领。

目前公开 taxonomy 中没有看到 `same UNKNOWN → WHERE vs CHECK interface-specific designated values` 的 matched task。SQL 的规范本身给出硬 contrast：

```text
WHERE: retain only TRUE; UNKNOWN is rejected
CHECK: reject FALSE; UNKNOWN is accepted (dialect/standard条件需冻结)
```

因此 SQL survivor 继续保留，但必须在特定 DB dialect / standard 下执行验证，不能只靠语言描述。

---

## 6. 当前 Batch-2 十强（第四刀后）

1. Burden-Placement Null-Case Reversal
2. Short-Circuit Side-Effect Leakage
3. **Correlation → Agreement / Interchangeability Promotion**  ← replaces RIF
4. Noninferiority → Equivalence Collapse
5. Surrogate → Clinical-Outcome Promotion
6. Harmless-Error → Remedy Collapse
7. SQL UNKNOWN Interface Collapse
8. Subgroup-Significance → Interaction Promotion
9. Competing-Event → Censoring Collapse
10. Stock–Flow Correlation Intrusion

仍全部：`NOT FORMAL N0-PASS / NOT DISPATCHABLE`。

下一轮优先攻击：NI（因 MedLitSpin item taxonomy 风险上升）→ Short-Circuit（CoRE mother）→ Surrogate → Burden；若任何一题死，从 delayed-entry / immortal-time / prediction-interval 等 reserve 和新脑暴中继续补，不把 RIF 复活。