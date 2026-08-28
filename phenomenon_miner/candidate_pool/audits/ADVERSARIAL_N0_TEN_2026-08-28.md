# 十题第二轮对抗式 N0 审计（2026-08-28）

状态：`ADVERSARIAL-N0-SURVIVOR / AWAITING INDEPENDENT SIGN-OFF / NOT DISPATCHABLE`

```yaml
validation_authorized: false
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
```

## 审计目的

这不是普通候选池复述，也不把“没搜到同名标题”当新颖性。本文对十题执行第二轮 adversarial N0：

1. 找最强 exact / near-exact 邻居；
2. 尝试用更宽母命题完整吸收本题；
3. 检查 `why_not_a_rename` 是否依赖真正独立的 operator / decisive contrast，而不是换数据、换领域或换 readout；
4. 写出一条能让后续 independent auditor 直接杀题的 hard kill condition。

**本轮由同一 proposer-side 审计链完成，因此不能冒充仓库流程要求的“独立 auditor”。** 这里的 `PASS` 只表示：截至 2026-08-28，本轮针对性检索与母命题压缩未能把该题完整杀死。正式 `N0-PASS` 仍须另一独立审计者做 citation chaining、全文/appendix 检查和时间戳 refresh。

---

## 最终十题

| # | 题目 | 第二轮结论 | 独立 operator / decisive contrast |
|---:|---|---|---|
| 1 | First-Negative-Evidence Harm | **PASS-TO-INDEPENDENT-N0** | fixed option set 中的真实 negative subtraction；必须区别于 mention、positive anchor、physical deletion |
| 2 | Packed–Unpacked Event Splitting | **PASS-TO-INDEPENDENT-N0** | exhaustive partition / extensionality operator；branch-count、focal/alternative、repacking 可反证 |
| 3 | Publicness–Coordination Dissociation | **PASS-TO-INDEPENDENT-N0** | matched first-order knowledge 下仅 public observability 改变 coordination consequence |
| 4 | Existential Witness Collapse | **PASS-TO-INDEPENDENT-N0** | independent existential referents 到 downstream joint-witness join 的非法操作 |
| 5 | Inadmissible-Evidence Persistence | **PASS-TO-INDEPENDENT-N0** | admissibility mask + `never-seen` counterfactual；不是一般 rule-use gap |
| 6 | Habitual → Episode Actualization | **PASS-TO-INDEPENDENT-N0** | event-kind / habitual 被实例化为 dated/countable event token |
| 7 | Mixed-Status Event Attraction | **PASS-TO-INDEPENDENT-N0** | component factuality 全对后，邻接事件间出现有方向的 status pooling / attraction |
| 8 | Dissent → Holding Role Swap | **PASS-TO-INDEPENDENT-N0** | proposition 与 juridical authority-role 脱绑定，wrong destination 精确落到 dissent proposition |
| 9 | Source-Discount Recovery | **PASS-TO-INDEPENDENT-N0** | source identity/credibility 仍在，但 source→message discount coupling 随距离衰减并可 cue-reinstate |
| 10 | Weak-Evidence Backfire | **PASS-TO-INDEPENDENT-N0** | `E supports H` 已确认，但 `P(H|E) < P(H)` 的真正 sign reversal |

---

# 1. First-Negative-Evidence Harm

## 最强邻居

- ACL 2025 Main, [Exclusion of Thought](https://aclanthology.org/2025.acl-long.1051/)：错误选项带来 cognitive load，物理删除 distractor 通常帮助。
- ACL 2025 Main, [Llama See, Llama Do](https://aclanthology.org/2025.acl-long.791/)：context 中再次出现 token 会产生 contextual entrainment，并定位 causal heads。
- 2026 preprint, [Anchored Confabulation](https://arxiv.org/abs/2604.25931)：一个 confirmed intermediate fact 可先提高 confident-wrong，再随更多/完整 evidence 恢复。
- PoE / elimination MCQA 工作已经占领“排除法是否好用”这一宽母题。

## 为什么没有被完整吸收

`Anchored Confabulation` 已经杀掉“部分正确证据可非单调地害模型”这个宽 claim。因此本题只有下面的合同仍可独立：

```text
fixed option set
baseline
+ true semantic negative: C is definitely false
+ mention-only: C was examined
+ positive/salience: pay attention to C
+ physical deletion: remove C
```

negative fact 不提供任何正向中间 hop，只把一个候选从可能集合中删除。若 `semantic-negative` 有独立的 `one-negative harm → multi-negative recovery`，且 physical deletion 单调帮助、mention-only 无法解释，才是不同 computation。

## hard kill

- mention-only 复现主要 effect；或
- wrong destination 主要就是被重新提及的被排除项；或
- semantic-negative 与 Anchored Confabulation 的 partial-positive anchor 无可区分结构；或
- 跨家族没有 `neg1 harm → neg2/3 recovery`。

任一成立，standalone KILL。

---

# 2. Packed–Unpacked Event Splitting

## 母现象与邻居

经典 Support Theory 把 subjective probability 建模成 description-dependent support；unpacking 一个 exhaustive event partition 可导致 subadditivity。概率一致性、conjunction/disjunction fallacy 和 generic framing 当然都很近，但它们没有自动包含下面的 recognized-extensional-equivalence 条件。

参考人类理论/复现：
- Tversky & Koehler 的 Support Theory；
- [Support Theory review](https://journal.psych.ac.cn/adps/EN/abstract/abstract1090.shtml)；
- 2026 Applied Cognitive Psychology 对 unpacking 与后续行为的扩展：https://onlinelibrary.wiley.com/doi/10.1002/acp.70240

## 独立合同

必须先让模型正确确认：

```math
E = E_1 \lor ... \lor E_k,
E_i \cap E_j = \emptyset,
\bigcup_i E_i = E.
```

随后才测 packed vs unpacked 的总 probability / consequential decision。它不是任意 paraphrase，而是**同一个 extension 的 partition 表示**。

可证伪结构：
- branch count 曲线；
- unpack focal hypothesis 与 unpack alternatives 的方向区别；
- repacking 恢复；
- exhaustive 与 non-exhaustive 拆分分离；
- probability 与 frequency judgment 可分离。

截至本轮以 `unpacking effect / support theory / partition dependence / event splitting + LLM` 检索，未找到完整覆盖 `equivalence recognized → partition-dependent LLM judgment + mechanism` 的工作。

## hard kill

若 effect 只等于任意 wording sensitivity，或模型无法稳定确认 partition 的 disjoint/exhaustive/equivalent relation，KILL。

---

# 3. Publicness–Coordination Dissociation

## 最强邻居

- EMNLP 2025 Main, [DEL-ToM](https://aclanthology.org/2025.emnlp-main.573/)：Dynamic Epistemic Logic 下的动态 belief update。
- FANToM / MindGames / common-ground / public-announcement work 已经让“LLM 会不会 higher-order ToM”极度拥挤。
- 人类工作 [Common knowledge, coordination, and strategic mentalizing](https://pmc.ncbi.nlm.nih.gov/articles/PMC6628641/) 显示 public/common knowledge 与 private/shared knowledge 会系统改变协调行为。

## 独立合同

不能写“LLM 不懂 common knowledge”。只允许：

```text
same proposition
same recipients
same first-order knowledge for every participant
separate private delivery  <->  publicly observable announcement
only downstream coordination/action differs
```

先验收 channel recognition 与每个人的一阶 belief；现象必须发生在 publicness/common-knowledge 对 policy 的增益被压平、倒置或呈人数/风险 cliff。

## why_not_a_rename

DEL/ToM 测的是 belief-state computation；这里锁死 first-order state 后，问的是 **public-event operator 是否产生 coordination consequence**。若已有论文同时做这个 matched factorial + same-model consequential action，本题立即死。

## hard kill

若错误可由二阶 ToM 本身失败解释，或 public/private 条件没有严格匹配个体知识，KILL。

---

# 4. Existential Witness Collapse

## 最强邻居

quantifier reasoning、variable binding、DRT 和 discourse anaphora 已很成熟。ACL 2025 Main [Meaning Beyond Truth Conditions](https://aclanthology.org/2025.acl-long.432/) 甚至直接从 dynamic semantics 测 anaphora accessibility。因此不能做“LLM 不懂 existential quantifier”。

## 独立合同

```math
\exists x P(x),\quad \exists y Q(y)
```

不授权：

```math
\exists z(P(z)\land Q(z)).
```

注意这并不声称两个 witness 必须不同；只是没有证据允许把它们识别为同一个。

只有以下错误计入：
- 模型明确知道 independent witnesses need not coincide；
- 局部 entity/property judgments 正确；
- downstream staffing/resource/planning 却执行 joint-witness join；
- wrong destination 是可预测的 fused entity，而非随机逻辑错误。

截至本轮以 `existential witness / witness identity / anonymous witness / existential conjunction / discourse referent fusion + LLM` 检索，未找到该 exact component-correct→illegal-join phenotype。

## hard kill

若强模型在自然 setting 中只剩普通 quantifier parsing error，或必须靠玩具 FOL 模板才能诱发，KILL。

---

# 5. Inadmissible-Evidence Persistence

## 最强邻居

LegalBench、CourtReasoner、hearsay/admissibility classification 与一般 legal authority work 已占领“模型会不会识别法律规则”。本题不能靠“知道规则但没用”四个字求新。

## 独立合同

三条件必须冻结：

```text
A. evidence never seen
B. evidence seen + admissible
C. evidence seen -> explicitly ruled inadmissible / struck
```

模型还必须正确回答：
- admissibility status；
- exclusion scope；
- evidence 对哪一方有利。

规范预测是 C 应尽量回到 A，而 B 可改变 verdict。真正现象是 C 的 verdict 仍随被排除证据的 inculpatory/exculpatory polarity 等变移动。

这比 generic F5 veto 多一个很强的 counterfactual operator：**不是简单“有没有 veto”，而是能否把 latent evidential state 恢复到 never-seen baseline。**

## 机制分叉

1. evidence 在 admissibility gate 前已写入 posterior，mask 太晚；
2. admissibility mask 存在，但只被 rationale writer 读取，verdict accumulator 无视；
3. mask 能抑制显式 evidence node，却不能 counterfactually undo earlier integration。

## hard kill

若只在模型不会分类 hearsay / 不懂 exclusion scope 的样本出错，或 `struck` condition 只是普通 distractor effect，KILL。

---

# 6. Habitual → Episode Actualization

## 最强邻居

Generics 邻域已经很密：
- Findings ACL 2026, [Generics are not quantificational](https://aclanthology.org/2026.findings-acl.1100/)；
- ACL 2026 Main 的 *Discourse Realization of Generics in Human and LLM-generated Texts*；
- generic overgeneralization、event factuality、MAVEN-Fact 等。

因此“模型把泛指当全称”或“genericity 分类不好”都已没有空间。

## 独立合同

本题只保留 ontology transition：

```text
recognizes: sentence is habitual/generic and does not entail a particular occurrence
uses: downstream timeline / memory / count creates a dated, countable event token
```

例如“Lina usually cycles to work”被正确解释为习惯，但 Tuesday timeline 凭空出现一次 cycling event。

这不是 generic→universal，而是 **event kind → phantom event token instantiation**。

## 机制分叉

1. event extraction 先为 salient predicate 建 token node，genericity 只是旁路 label；
2. kind/token 中层分明，但 timeline/memory writer 类型擦除；
3. summary compression 丢 status——若只剩这个解释，则 ROUTE 到 F1 而非 standalone。

## hard kill

若错误只表现为去掉 `usually`、没有时间/计数/因果上的具体 episode consequence，或自然数据无法给 particular-occurrence hard gold，ROUTE/KILL。

---

# 7. Mixed-Status Event Attraction

## 最强邻居

Findings EMNLP 2024 [MAVEN-FACT](https://aclanthology.org/2024.findings-emnlp.651/) 提供 112,276 个 event factuality 标签，并分析 arguments/relations 对 LLM EFD 的作用。ModaFact 等也研究 joint modality/factuality。

## 独立合同

不是多事件更难。只有：

```text
status(A) individually correct
status(B) individually correct
A and B occur in same clause / relation / local context
-> downstream timeline/summary assigns A toward B's status or B toward A's status
```

必须看到**有方向、有局部性、可预测 wrong destination**的 status attraction：例如 actual 邻居使 possible event actualize，或 nonfactual 邻居使 actual event 被漏掉；强度随 sentence distance / coordination / causal edge 改变。

## why_not_a_rename

MAVEN-FACT 是 event-level factuality；本题研究的是 **component labels intact 后的 pairwise composition operator**。如果没有 neighbor-conditioned directional attraction，只是 EFD 平均准确率下降，则被母题完整吸收。

## hard kill

若完整上下文错误是随机 omission、scope parsing、长度效应，或单项 factuality 在 context 内本身就错，KILL。

---

# 8. Dissent → Holding Role Swap

## 最强邻居

ACL 2026 Main [Sycophants in the Courtroom](https://aclanthology.org/2026.acl-long.497/) 已研究法律中的 temporal validity、normative relations、external authority perturbation 与 scaling；因此“LLM 受权威文本影响”已经不是 novelty。

## 独立合同

真实判例中，模型必须：
- 正确认出 majority / dissent；
- 正确复述双方 proposition；
- 正确回答谁 dissent；
- 但最终 holding / controlling rule **精确等于 dissent proposition**。

wrong destination 必须跟 proposition↔role binding 走，而不是一般 false citation / authority confusion。

## why_not_a_rename

Sycophants 研究“外部权威何时适用/误导”；这里固定同一 case 内的 proposition content，只问 **which role owns which proposition, and which role controls the holding**。这是 role-binding operator，不是 prestige/authority strength 主效应。

## hard kill

若错误主要来自不知道 majority/dissent、case 时间/jurisdiction 不清、或只在长判例 retrieval 失败时出现，KILL。

---

# 9. Source-Discount Recovery

## 天然母现象

经典 sleeper-effect / source-monitoring 文献研究低可信来源的折扣随时间衰减；meta-analysis 讨论 discounting cue 与 message trace 的 differential decay：
- [The Sleeper Effect in Persuasion: A Meta-Analytic Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3100161/)；
- [Reading is believing: The truth effect and source credibility](https://pubmed.ncbi.nlm.nih.gov/21978908/)。

NLP 近邻包括 NAACL 2025 [From Evidence to Belief](https://aclanthology.org/2025.naacl-long.531/) 的 evidence reliability/strength，以及静态 source preference/source-memory 工作。

## 独立合同

不能是“模型忘了 source”。必须同时满足：

```text
source identity after delay: correct
source credibility after delay: still judged low
message content: correct
message weight / decision influence: rebounds toward high-credibility baseline
```

再加入 source-cue reinstatement：如果重新提示来源身份/可靠性就恢复 discount，这是 source–message coupling decay 的强反转预测。

## why_not_a_rename

静态 source credibility 研究不包含 **source memory intact but discount coupling weakens with temporal/context distance**。独立算子是 provenance/credibility tag 与 proposition weight 的时间绑定，而不是来源偏好本身。

## D0 风险与控制

不要用“专家/网红”这种主观 prestige。source reliability 必须由显式 track record 或任务内已冻结准确率定义，例如 source A 历史 9/10 正确、source B 2/10 正确。

## hard kill

若 influence rebound 完全由 source identity/credibility 真的被忘记解释，或 cue reinstatement 不产生选择性恢复，KILL。

---

# 10. Weak-Evidence Backfire

## 天然母现象

Fernbach, Darlow & Sloman 2011 [When good evidence goes bad](https://pubmed.ncbi.nlm.nih.gov/21345428/)：人类会把一条单独判断为 positive/supportive 的弱证据加入后，反而比 no-evidence baseline 更不相信 outcome；论文还专门排除了“弱证据暗示强证据不存在”的简单 pragmatic explanation。

最强 NLP 邻居是 NAACL 2025 Main [From Evidence to Belief](https://aclanthology.org/2025.naacl-long.531/)，它系统研究 evidence informativeness/reliability 与 Bayesian confirmation；论文报告 LMs 对 true evidence 的 confirmation assumption 相对较好，但没有把下面这个 exact sign reversal 作为 phenotype。

## 独立合同

必须先独立确认：

```text
model judges E as genuinely probability-raising / supportive for H
```

然后比较：

```math
P(H\mid E) < P(H)
```

或者 consequential choice 对 H 的支持低于 no-evidence baseline。

这不是“弱证据加得不够多”，而是**符号方向错了**：positive likelihood update 被转成 negative posterior movement。

## 必须控制

- no-evidence prior；
- strong positive evidence；
- neutral/irrelevant mention；
- matched wording/length；
- 显式说明“没有更强证据”或提供 alternative-cause completeness control，以排除 pragmatic implicature；
- 最好加入 alternative-cause availability / causal competition 轴，区分 focusing-on-mentioned-cause 与 generic skepticism。

## 机制分叉

1. weak cause 被显式提及后占据 causal explanation slot，模型忽略 alternative causes，像经典 focusing account；
2. evidence strength 被映射为绝对 sufficiency signal，而不是 likelihood ratio：`weak` 被读成“总体不太可能”；
3. posterior computation正确，但 answer/decision writer把“weak support”误映射为 negative stance。

## hard kill

若模型并不认为 E 支持 H，或 backfire 只由 pragmatic absence-of-stronger-evidence 暗示解释，或只在 verbalized confidence 而不在 token probability/choice 上出现，KILL。

---

# 本轮确认淘汰 / 路由

## SEC-06 / Provenance-Graph Retraction Leakage — KILLED-COLLISION/ROUTE

2026 preprint [Grounded Continuation: A Linear-Time Runtime Verifier for LLM Conversations](https://arxiv.org/abs/2605.14175) 明确维护 dependency graph，并让 retraction 沿图传播，检测 stale-premise conclusions。它已经占掉“dependency graph 上的 transitive retraction/invalidation”这个核心 operator。把 payload 换成新闻转载链只剩 domain/provenance flavor，不再作为 standalone 主题。可作为该母题的外部分布/control。

## UDH-03 / same-final-evidence abstention hysteresis — KILLED-MOTHER-OCCUPIED

ACL 2026 Main [Mitigating Lost in Multi-turn Conversation via Curriculum RL with Verifiable Accuracy and Abstention Rewards](https://aclanthology.org/2026.acl-long.1540/) 直接研究 information progressively revealed as instruction shards 下的 multi-turn degradation、solvability 与 abstention。继续把“先 partial 后 full 仍拒答”包装成独立题，只剩 LiC 的一个 error slice，不够。

## Sure-Thing / disjunction violation — NOT ADDED

已有工作直接把 Savage sure-thing principle 用于 ChatGPT/cognitive-task evaluation；即使再做 mechanism，discovery claim 已不够独立。因此不占十题名额。

## 旧 PRE-N0 淘汰保持不变

- Equivalent-Quantity Decision Split：被 2026 quantity-comparison / numeral-unit heuristic 机制工作强覆盖；
- Generation–Reception Trace Asymmetry：self-conditioning/source-monitoring 母区过密；
- Part–Whole Double Counting：ROUTE 到 F6 local→global reducer；
- Confidence-Conditioned Correction Relapse：confidence-conditioned belief persistence/self-correction 邻域过密；
- Part-List Cue 与 Redundant-Constraint：不再占十强名额，保留历史卡但不升格。

---

# 结论与下一步

这十题当前统一状态是：

```text
ADVERSARIAL-N0-SURVIVOR
!= formal N0-PASS
!= READY-TO-SMOKE
```

下一步不是跑十个模型实验，而是把每题交给**真正独立**的 N0 reviewer，要求其不接受本文正面论证，优先找：

1. exact behavior 已在正文/appendix 出现；
2. 本题 decisive contrast 其实是已有论文的自然 corollary；
3. 公开数据无法给客观关系/gold；
4. `why_not_a_rename` 仍只是现有 F1–F9 的一个实例。

只有独立 N0 + D0 都通过，才允许 `AUDIT_REGISTRY.md` 设置 `validation_authorized: true`。