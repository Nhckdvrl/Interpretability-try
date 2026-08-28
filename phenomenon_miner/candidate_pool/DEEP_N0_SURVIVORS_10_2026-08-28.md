# 深度 N0 审计后保留的 10 个现象题（2026-08-28）

状态：`PROPOSER-N0-SURVIVOR / AWAITING INDEPENDENT N0 / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
```

这份文件替代 `PREN0_BATCH_10_2026-08-28.md` 作为**当前十题 shortlist**，但不替代 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) 的正式裁决。旧 PRE-N0 文件保留作为失败/演化记录。

这里的门槛比普通 ideation 高：每一题都经过本轮 proposer-side 对抗式 N0，要求同时满足：

1. targeted exact-phenotype search 未找到完整覆盖；
2. 最强邻近论文不能用一个更宽母命题完整吸收本题；
3. `why_not_a_rename` 不能只是“换数据/换领域/换 readout”；
4. 有一个独立 decisive contrast 或 operator，若成立可产生结构 signature；
5. 有自然母现象或现实工作流、公共数据落点与客观/可冻结关系；
6. 至少两个有不同 causal prediction 的机制；
7. 失败条件明确，后续 independent N0 可以直接推翻。

**重要：`PROPOSER-N0-SURVIVOR` 不等于正式 `N0-PASS`。** 正式 N0 仍要求独立 adversarial auditor、citation chaining/全文 appendix 检查与时间戳 refresh。任何一题在独立审计中发现 exact collision 或 mother inclusion，立即 KILL/ROUTE，不为维持“十题”数量续命。

---

## 总览

| # | 描述性题目 | 当前最强近邻 | 为什么仍不是换皮 | proposer N0 |
|---:|---|---|---|---|
| 1 | 一条真实负证据先害、更多负证据再救 | Anchored Confabulation；EoT；contextual entrainment | 负证据只删除不可能选项，不提供正向中间链；必须超出 mention-only 与 physical deletion | **SURVIVE** |
| 2 | 同一事件展开成互斥穷尽子事件后总概率膨胀 | Support Theory / probability consistency | 独立 extensionality/partition operator，有 branch-count、repacking、focal/alternative 预测 | **SURVIVE** |
| 3 | 人人一阶知识相同，公开宣布仍未改变协调 | DEL-ToM / common-ground / coordination work | 固定一阶知识，只测 public observability 产生的 coordination consequence | **SURVIVE** |
| 4 | 两个独立“有人”被下游计划合成一个共同 witness | quantifier/binding work | 不是量词答错，而是局部 binding 正确后发生未经授权的 entity join | **SURVIVE** |
| 5 | 源头撤回只杀源节点，不沿已知转载链失效 | correction/CIE；misinformation propagation | 独立的是 provenance-graph transitive invalidation，同时保留 independent source | **SURVIVE** |
| 6 | 证据已判不可采，却仍改变判决 | LegalBench/hearsay；generic rule-use gap | 有 `never-seen` counterfactual 与 content-independent admissibility mask | **SURVIVE** |
| 7 | 已识别为习惯/泛指的事件被时间线实例化成一次具体经历 | genericity；MAVEN-Fact | 独立 kind→token ontology error，不是 factuality label 低准确率 | **SURVIVE** |
| 8 | 两个事件 factuality 各自正确，组合后向邻居 status 定向塌缩 | MAVEN-Fact / EFP | 独立 pairwise status-attraction/composition signature，而非 EFD 主效应 | **SURVIVE** |
| 9 | 明知谁在 dissent，holding 却精确变成 dissent proposition | legal authority / Sycophants in the Courtroom | 独立 proposition↔authority-role binding 错误，有明确 wrong destination | **SURVIVE** |
| 10 | 低可信来源仍被记得且仍被判低可信，但其折扣随上下文距离失效 | Whose Facts Win?；Evidence-to-Belief；source-memory work | 独立 temporal source–message coupling / cue-reinstatement 反转，不是静态 source preference | **SURVIVE** |

---

# 1. 真实负证据的单步伤害与多步恢复

**canonical reference：** [`phenomena/002_first_negative_evidence_harm.md`](../phenomena/002_first_negative_evidence_harm.md)

### 一句话矛盾

模型本来答对一道选择题；加入一条确定真实的“C 已被验证为错误”信息后反而答错；继续加入第二、第三条真实排除信息后又恢复。

### 本轮最强碰撞

- ACL 2025 Main, *Exclusion of Thought*: distractor cognitive load / physical option removal；
- ACL 2025, *Llama See, Llama Do*: context-seen token 的 contextual entrainment；
- 2026 preprint, *Anchored Confabulation*: **部分正确证据可先增加 confident wrong，再随完整证据恢复**；
- PoE / elimination-based MCQA 工作：顺序排除错误选项通常作为方法。

### why_not_a_rename

宽叙事“partial evidence can non-monotonically hurt”已经被 *Anchored Confabulation* 占领。因此本题只有在下面更窄的结构成立时才独立：

```text
negative semantic fact:   C is definitely false
mention-only:             C was examined / mentioned
positive/salience:        pay attention to C
physical deletion:        remove C from the option set
```

真实负证据**不补全任何正向 reasoning hop**，只做逻辑上单调安全的 candidate-set subtraction。只有 semantic-negative 相比 mention-only/physical-deletion 产生额外的 `harm → recovery`，本题才不是 Anchored Confabulation 或 contextual entrainment 的 MCQ 子例。

### 必须出现的结构 signature

- 多家族 `baseline-correct → neg1-wrong`；
- neg2/neg3 出现稳定恢复或 cliff；
- wrong destination 不只是被再次 mention 的 C；
- semantic negative 与 mention-only 有可重复差异；
- physical deletion 单调帮助而 semantic exclusion 可先害；
- 若上述任一关键差异消失，**KILL standalone novelty**。

### 机制分叉

1. negative-evidence gate 触发异常 option-set renormalization；
2. option mention/entrainment 与 elimination signal 走竞争路径；
3. 一条 elimination 使模型切入局部 verification 路径，多条 elimination 才切到 reduced-set solver。

### N0 搜索记录

截至 2026-08-28，以 `negative evidence / wrong-option elimination / process of elimination / MCQ / non-monotonic / partial evidence / contextual entrainment` 为核心组合检索，找到上述强近邻，但未找到完整覆盖 **fixed option set + true semantic negative + mention-only control + one-negative harm / multi-negative recovery** 的工作。

---

# 2. 互斥穷尽事件的 packed ↔ unpacked 概率不变量破坏

### 一句话矛盾

模型能确认 `E` 与 `E1 or E2 or E3` 表示同一事件，也能确认三个子事件互斥且穷尽，却在展开以后给这个总事件更高的概率或决策权重。

### 天然母现象

Tversky & Koehler 的 **Support Theory / unpacking effect**：主观概率对事件描述/partition 非外延，展开 focal hypothesis 会提高 judged support；后续工作还有 repacking、partition-size、typicality、ignorance-prior 等结构预测。

### why_not_a_rename

它不是“换句话说模型概率变了”。定义的是硬 extensionality relation：

```math
E = E_1 \lor ... \lor E_k,
E_i \cap E_j = \emptyset,
\bigcup_i E_i = E.
```

模型还必须先正确确认 equivalence / exclusivity / exhaustiveness。只有最终 probability/decision reader 仍随 partition 改变才计入。

这给出 generic paraphrase sensitivity 没有的反事实：

- branch count 应形成结构曲线；
- unpack focal vs unpack alternative 应产生不同方向；
- repacking 应部分/完全恢复；
- non-exhaustive unpacking 不应与 exhaustive case 混为一谈。

### 自然数据落点

ForecastQA/公开 forecasting 问题、体育/天气/选举等有明确 outcome taxonomy 的历史问题；也可从公开多选预测题构造由官方 option set 定义的 exhaustive partition。D0 时必须冻结真正 disjoint/exhaustive 的 partition。

### 机制分叉

1. explicit branch 各自触发 support retrieval，随后 support 被重复累加；
2. semantic event 已 canonicalize，但 probability reader 在显式 branch nodes 上求和/向 uniform partition prior 收缩；
3. packed 与 unpacked 根本未映射到同一 latent event identity。

### N0 搜索记录

截至 2026-08-28，以 `unpacking effect / support theory / partition dependence / event splitting + LLM/language model` 检索，未找到完整的 LLM behavior+mechanism study。概率一致性、conjunction/disjunction fallacy 与 generic framing 是近邻，但没有包含 **recognized exhaustive equivalence → partition-dependent judgment + Support-Theory moderators**。

---

# 3. 一阶知识匹配下的 publicness–coordination 解离

**canonical reference：** [`SEC-01`](06_SOCIAL_EVIDENCE_COLLECTIVE.md)

### 一句话矛盾

Alice、Bob、Carol 每个人都知道 P；模型也知道信息是分别私发还是公开广播，但在需要协调时把两种情形当成一样。

### 最强近邻

普通 ToM/FANToM、common-ground 工作、动态 epistemic logic / DEL-ToM、LLM coordination games 都已覆盖高阶信念或协调能力。人类 PNAS 工作明确把 common knowledge/publicness 视为区别于“人人分别知道”的特殊协调状态。

### why_not_a_rename

不能声称“LLM 不懂 common knowledge”。唯一可守合同是：

```text
same proposition
same recipients
same first-order knowledge of every participant
private-to-each vs publicly observable announcement
→ downstream coordination/action
```

必须先验证 channel recognition 和每个人的一阶 belief 全对。现象只允许出现在 publicness/common-knowledge 对 coordination policy 的增益被压平、倒置或出现结构 cliff。

### 机制分叉

1. 没有独立 public-event representation，只写多个 individual belief slots；
2. publicness 表示存在，但 higher-order/common-knowledge closure 未形成；
3. closure 已形成，coordination reader 仍只读取 first-order slots。

### N0 结论

截至本轮检索，public/private epistemic update 本身已经有人做，协调本身也有人做；未找到完整覆盖 **matched first-order knowledge + only public observability differs + same-model consequential coordination readout** 的工作。若 independent audit 找到这个 exact factorial，立即 KILL。

---

# 4. 独立 existential facts 导致未经授权的共同 witness

**canonical reference：** [`RVC-04`](08_REASONING_VERIFICATION_COMPOSITION.md)

### 一句话矛盾

团队里有人会日语，也有人会 CUDA；模型知道这两句话不保证同一个人两样都会，排班时却还是创造出一个“会日语又会 CUDA”的人。

### 规范边界

```math
\exists x P(x),\quad \exists y Q(y)
```

不授权推出：

```math
\exists z(P(z) \land Q(z)).
```

注意不是声称两个 witness 必须不同，而是**没有证据可以把它们认成同一 witness**。

### 最强近邻

quantifier reasoning、variable binding、DRT、logical reasoning 都很拥挤；因此普通“存在量词答错”没有空间。

### why_not_a_rename

本题只统计：

- 模型能解释 independent witnesses need not coincide；
- 局部属性/实体事实正确；
- 最终 staffing/resource/planning **执行一个 illegal join**；
- wrong destination 是可预测的 fused entity/witness，而非随机逻辑错误。

因此独立 computation 是 **anonymous referent identity → downstream join operator**，不是 generic quantifier accuracy。

### 自然数据

FOLIO/LogicBench 做规范锚；真实 staffing、resource assignment、room capability、database-style existential queries 做自然外部分布。

### 机制分叉

1. referent creation 阶段两个 anonymous witnesses 已 merge；
2. 中层仍分开，composition reader 复用同一 salient entity slot；
3. binding 正确，planner 为满足 conjunction 主动执行错误 entity join。

### N0 搜索记录

截至 2026-08-28，以 `existential witness / witness identity / existential conjunction / anonymous witness / variable binding / discourse referent fusion + LLM` 检索，未找到以 **component knowledge intact → unlicensed joint witness in downstream composition** 为核心 phenotype 的工作。

---

# 5. 源头撤回没有沿已知 provenance graph 传播

**canonical reference：** [`SEC-06`](06_SOCIAL_EVIDENCE_COLLECTIVE.md)

### 一句话矛盾

原报道 S 撤回了消息；模型知道 S 已撤回，也知道 D1/D2/D3 都是在转载 S，却只把 S 作废，继续把三个转载当有效证据。

### 最强近邻

continued influence / correction / belief revision 已经成熟；2025 misinformation-propagation 工作研究错误信息怎样进入 LLM reasoning 以及 correction 效果；2026 也有工作测试 LLM 是否知道论文已撤稿。来源重复/lineage weighting 又是仓库已有邻域。

### why_not_a_rename

本题不是“模型不听纠正”，也不是“重复来源被多算”。独立 operator 是**依赖图上的 transitive invalidation**：

```text
S -> D1, D2, D3
S recanted
I1, I2 are independent

expected:
invalidate S + descendants(S)
preserve I1, I2
```

只有模型明确识别 provenance edges，而失效 mask 只停在源节点或沿图传播不完整，才计入。

### 机制分叉

1. provenance graph 可报告但 evidence store 不保存 dependency edge；
2. graph/edges 在中层存在，retraction updater 只修改 source node，不做 graph propagation；
3. descendants 已被标 invalid，但 final evidence aggregator 不读取 inherited-invalid mask。

### N0 搜索记录

截至 2026-08-28，以 `source retraction / recantation / provenance graph / copied reports / descendant invalidation / misinformation propagation + LLM` 检索，未找到完整覆盖 **recognized graph + source invalidation + descendant-selective leakage + independent-source preservation** 的研究。

---

# 6. 已判不可采的证据仍进入 verdict accumulator

**canonical reference：** [`UDH-11`](11_UNCERTAINTY_DECISION_HIGH_STAKES.md)

### 一句话矛盾

模型正确说一条证据属于 hearsay/已被法庭排除、不能用于实体判决，也知道它支持哪一方；最终判决仍然随这条不可采证据的内容方向移动。

### 天然母现象与规范关系

法律 evidence doctrine 明确区分 relevance 与 admissibility；被限制/stricken 的证据不能作为相应 purpose 的判决依据。人类 juror 文献也长期研究 **inadmissible evidence 仍持续影响 judgment**。

### 最强近邻

LegalBench 有 hearsay 等分类任务；CourtReasoner/法律 LLM 工作研究综合推理；generic `recognized rule but not used` 又接近仓库 F5。

### why_not_a_rename

本题的 decisive counterfactual 是：

```text
A: evidence never shown
B: same evidence shown and admissible
C: same evidence shown, then explicitly ruled inadmissible/stricken
```

规范上，针对被排除的用途，`C` 应尽量恢复到 `A`，而 `B` 可以改变 verdict。模型必须先正确完成 admissibility、scope、evidence polarity 三个 component judgment；只有 verdict 对 C 的内容仍等变响应才计入。

这比 generic veto failure 多一个 **content-independent admissibility mask + never-seen restoration target**。

### 机制分叉

1. evidence 在 admissibility decision 之前已更新 latent posterior，late instruction 无法 undo；
2. admissibility mask 存在但只有 rationale writer 使用，verdict head 读取全部 evidence；
3. mask 能关闭 evidence node，却无法把 state counterfactually restore 到 never-seen posterior。

### N0 搜索记录

截至 2026-08-28，以 `inadmissible evidence / stricken evidence / hearsay / verdict / evidence admissibility + LLM` 检索，找到 admissibility 分类与法律 reasoning 工作，但未找到完整覆盖 **classification intact → never-seen counterfactual failure → polarity-dependent verdict shift + mechanism** 的研究。

---

# 7. habitual/generic event 被下游实例化成 concrete episode

**canonical reference：** `NG-01`，见 [`SECOND_PASS_MTR_DPC.md`](audits/SECOND_PASS_MTR_DPC.md)

### 一句话矛盾

模型知道“Lina 通常骑车上班”描述的是习惯，并不证明她某个具体星期二骑了车；整理星期二时间线或统计经历时却凭空写入一次具体骑车事件。

### 最强近邻

UDS-Genericity/Situation Entities 等研究 genericity；MAVEN-Fact / FactBank 研究 event factuality；ACL 2026 也有 LLM-generated text 中 generics 的 discourse realization 工作。

### why_not_a_rename

普通 factuality/status 错误不足。必须满足：

```text
generic/habitual judgment correct
truth of generic statement can be correct
no particular episode entailed
→ downstream creates dated/countable event token
```

这里独立的本体错误是 **event kind → event token instantiation**，不是 `possible → actual` 或 generic label accuracy。

### 自然数据

UDS-Genericity、Situation Entities、Richer Event Description；用原生 generic/habitual clauses 与 actual SET-member controls，不靠人工模板制造主现象。

### 机制分叉

1. event trigger 一开始就创建 token node，genericity classifier 只是旁路标签；
2. kind/token 中层分离，timeline/memory writer 的 schema 没保留 kind type；
3. writer 为满足 timeline completeness 对 salient predicate 做默认实例化。

### N0 搜索记录

截至 2026-08-28，以 `habitual generic event / timeline / episode / actualization / event token / LLM` 检索，未找到 **genericity recognized → concrete episode created downstream** 的完整机制研究。

---

# 8. mixed-status events 在下游发生定向 factuality attraction

**canonical reference：** `NG-02`，见 [`SECOND_PASS_MTR_DPC.md`](audits/SECOND_PASS_MTR_DPC.md)

### 一句话矛盾

“球队已经到场，之后也许会庆祝。”模型分别问时知道到场=事实、庆祝=可能；生成时间线/事件清单时却把两个事件压成同一个 reality status。

### 最强近邻

MAVEN-Fact 是最强邻居：它有 112k event factuality labels、arguments/relations，并测试 LLM EFD；传统 EFP 也研究 modal/negation scope 和 document-level factuality。ACL 2026 还有 meta-factivity 的 position/roadmap 工作。

### why_not_a_rename

不能只是“多事件上下文让 EFD accuracy 下降”。必须先固定：

- event A status 独立判断正确；
- event B status 独立判断正确；
- mixed context 中两个 local status 仍可行为确认；
- 只有 downstream timeline/summary/state writer 出现**向邻居 status 的定向收缩**；
- effect 跟 event relation/句距/coordination edge 有结构关系。

因此独立问题是 **event-addressable status composition / attraction**，不是单事件 factuality prediction。

### 自然数据

MAVEN-Fact 的原生 mixed-status neighboring events；RED 的 ACTUAL/HYPOTHETICAL/GENERIC/UNCERTAIN + event relations 做外部确认。

### 机制分叉

1. modal/evidential scope 在中层向邻接事件 spill over；
2. event-specific statuses 保持分开，但 late receiver 对 event cluster 做 pooling/majority/maximum-certainty reduction；
3. relation edge 使两个 event 共享一个 status slot。

### N0 搜索记录

截至 2026-08-28，以 `event factuality interference / factuality propagation / mixed factuality events / modality contagion / status attraction + LLM` 检索，只找到 EFP/EFD、relations-as-features 与广义 hallucination，未找到 **component labels intact → pairwise directed status attraction in downstream use** 的工作。

---

# 9. dissent proposition 被错误提升为 controlling holding

**canonical reference：** [`UDH-09`](11_UNCERTAINTY_DECISION_HIGH_STAKES.md)

### 一句话矛盾

模型知道哪位法官写的是 dissent，也准确复述 dissent 与 majority 各自主张什么，问“本案的 controlling holding”时却输出了 dissent 的那条命题。

### 天然规范关系

在普通多数意见结构下，dissent 不具有该案 majority holding 的 binding status。题目只使用 role 明确、无 plurality/fragmented-ratio 歧义的样本。

### 最强近邻

Legal hallucination/holding extraction、legal authority hierarchy、2026 *Sycophants in the Courtroom* 都研究法律权威、temporal validity、authoritative perturbation；也有工作讨论 ratio/obiter/dissent 的法律 AI 要求。

### why_not_a_rename

不是泛泛“模型怕权威”或“不会抽 holding”。必须看到：

```text
majority/dissent role labels correct
proposition content for each opinion correct
final holding wrong destination == dissent proposition
```

并且错误跟 role swap/position counterbalance 移动，而不是长度、最后出现、文风、citation 数量等 nuisance。

独立 operator 是 **proposition ↔ juridical authority-role binding**。

### 自然数据

SCOTUS/CourtListener 等真实 divided opinions；优先选明确 majority、明确 dissent、holding 可由官方 syllabus/后续可靠 case summary 核验的案件，排除 plurality 与复杂多 ratio 案。

### 机制分叉

1. proposition embedding 与 authority-role tag 在编码时脱绑定；
2. role tag 存在，但 holding extractor 根据 lexical salience/argument strength 重新选 proposition；
3. majority proposition 正确进入 state，但 late authority reducer 错把 dissent node 当 controlling node。

### N0 搜索记录

截至 2026-08-28，以 `dissenting opinion / majority / holding / ratio decidendi / authority role / LLM` 检索，未找到完整覆盖 **role recognition intact + holding exactly becomes dissent proposition + binding mechanism** 的研究。*Sycophants in the Courtroom* 的核心是 authority perturbation、validity 与引用冲突，不是此 exact role-binding phenotype。

---

# 10. source identity/credibility 仍记得，但折扣权重随距离恢复

### 一句话矛盾

模型看到一条来自明确低可信来源的主张，开始时正确降低其权重；经过一段无关上下文后，它仍能准确说“这条主张来自 X，X 低可信”，但决策中这条主张重新获得了接近普通证据的影响力。

### 天然母现象

人类 persuasion/memory 文献中的 **sleeper effect / source-message dissociation**：低可信/discounting cue 的影响可随延迟衰减，即使 source 本身并未完全遗忘；理论核心之一就是 message 与 discounting cue 的 association 变弱，而非简单 item forgetting。

### 最强近邻

- ACL 2026 *Whose Facts Win?*：跨模型 source/repetition preference；
- NAACL 2025 *From Evidence to Belief*：证据 reliability/credibility 等因素；
- 2026 PRISM：memory/instruction/reasoning diagnostic；
- source-memory 与 credibility/RAG 工作。

这些工作占领静态 source credibility、source memory 或 evidence weighting，但本轮未找到**同一主张的 credibility discount 随 delay/source-message binding 变化**的 LLM 机制研究。

### why_not_a_rename

不能只画“距离越远越忘”。必须满足：

```text
source identity recall: correct at immediate and delayed
credibility judgment:   correct at immediate and delayed
message content recall: correct at immediate and delayed

yet evidence weight:
low-cred immediate < low-cred delayed
```

并加入关键 **source-cue reinstatement**：在 delayed query 前重新提醒“该消息来自低可信 X”，如果折扣恢复，支持 source–message coupling/readout 解释；若 source identity 本身忘了，则只是普通 long-context/source-memory failure，KILL。

### 自然数据落点

优先使用公开 claim/source 数据中具有可审计来源 provenance 与独立可信度依据的样本；也可借已有 source-preference/evidence-reliability benchmark 的自然 claim 作主内容，D0 再筛 license 与 credibility gold。研究主轴是 within-item temporal coupling，不要求比较不同话题的绝对 source quality。

### 机制分叉

1. source 与 message 的 binding strength 随 intervening context 衰减，两个 node 本身仍存在；
2. binding 保留，但 evidence aggregator 只在 source cue 局部可访问时应用 reliability weight；
3. message 被重新读取时走 content-only retrieval path，source-conditioned path 被竞争性覆盖。

### N0 搜索记录

截至 2026-08-28，以 `sleeper effect / source credibility / delay / source-message dissociation / source memory / evidence weighting + LLM/language model` 检索，未找到 LLM exact phenotype。发现的 2026 “source credibility + LLM”人类实验研究的是**人从 LLM 学习时的 source memory**，不是 LLM 自身的 evidence weighting，因此不构成 exact collision。

---

# 本轮永久淘汰/路由，不再用于补十题

下列旧 PRE-N0 卡不应因为最终十题再次失败而原名复活：

| 旧卡 | 裁决 | 原因 |
|---|---|---|
| Equivalent-Quantity Decision Split | `KILL-COLLISION` | 2026 quantity-comparison work 已直接发现 number-specific/unit-specific heuristics，并做 causal intervention；换成 recommendation readout 不够 |
| Generation–Reception Trace Asymmetry | `KILL-MOTHER-INCLUSION` | self-bias/source monitoring/self-authored evidence 邻域过完整，只剩 downstream metric 差异 |
| Part–Whole Double Counting | `ROUTE-F6` | parent/child inclusion 知道但 sum 错是 F6 local→global reducer 的标准实例，没有独立 operator |
| Confidence-Conditioned Correction Relapse | `KILL-MOTHER-INCLUSION` | confidence-conditioned persistence/self-correction/context-vs-parametric belief 已过密，delayed relapse 只是时间切片 |
| Part-List Cue Suppression | `HOLD-NOT-TOP10` | one-to-many factual retrieval 的 promote/suppress 机制已有强近邻；只有 part-list 理论 moderators 全成立才可复审 |
| Redundant-Constraint Distortion | `HOLD-NOT-TOP10` | exact contrast 仍可能新，但自然 D0 与 generic constraint salience/distraction 边界尚未达到十强门槛 |
| NG-03 Partial-Answer QUD Closure | `HOLD/ROUTE` | 2026 adaptive interviewer 已直接把 multi-part question 只答一部分→应 follow-up 作为核心行为需求；只剩 reader→state updater gap 不够强 |
| MCC-01 translation double vote | `ROUTE-F4/LINEAGE` | 跨语言只是 same-source lineage weighting 的 setting，不能另立母题 |
| MCC-10/MCC-11 | `NOT-TOP10` | 仓库曾 PROMOTE，但当前按更严格 mother-inclusion 标准仍容易被 F3/F9 或 F1/F9 吸收；不靠 multilingual setting 制造独立性 |

---

# 下一步：真正的 independent N0，而不是跑模型

这 10 个的下一步统一为：

```text
1. 交给独立 auditor，不看本文件的正面结论，重新搜 exact phenotype；
2. 对每题打开 3–8 篇最强近邻全文与 appendix，逐项对 decisive contrast；
3. 做 citation chaining：references + forward citations + 2026 recent arXiv refresh；
4. 写 mother-inclusion attack：如果审稿人说“这只是 X”，我们是否有非 readout/setting 的反事实回应；
5. 只有 independent N0 PASS 后进入 D0：dataset/license/gold/20-case audit；
6. `AUDIT_REGISTRY.md` 未授权前禁止 smoke。
```

当前建议 independent N0 顺序：

1. Packed ↔ Unpacked Event Splitting；
2. First-Negative-Evidence Harm（优先攻击 Anchored Confabulation 包含关系）；
3. Provenance-Graph Retraction Leakage；
4. Publicness–Coordination Dissociation；
5. Existential Witness Collapse；
6. Mixed-Status Event Attraction；
7. Habitual→Episode Actualization；
8. Inadmissible-Evidence Persistence；
9. Dissent→Holding Role Swap；
10. Source-Discount Recovery（重点先解决 D0 的 credibility gold，但 N0 先查 temporal source-weight work）。

这份 shortlist 的目标不是保证十题最终都活，而是保证**任何一题被 independent N0 杀掉都需要一个具体强碰撞/包含理由，而不是因为 proposer 一开始就没查文献或只做了换皮。**