# 027 — Questions That Assert

**Working title:** *Questions That Assert: Separating Rhetorical Force from Implied Stance in Language Models*
**Status:** `NATURAL-QUESTION PASS / N0 PASS / N1 PASS / PARK-DATA / NO MODEL CALL`
**Created:** 2026-08-31

## 1. 一句话问题

> **模型知道一句话“这是个修辞问句”，不等于模型知道说话人借这个问句到底在断言什么。LLM 内部会把 rhetorical force 和 implied assertion/stance 分开表示吗？**

例子：

> “Why should we force students to wear these garments anyway?”

理解它至少有三层：

1. 表面是 interrogative；
2. 在这个上下文里不是认真索取未知信息，而是 rhetorical/assertive speech act；
3. 说话人借它表达的是类似 “we should not force the students to wear them” 的立场。

只做到第 2 层，不代表真正理解了第 3 层。

## 2. 为什么这是自然 NLP 问题

人类对问句的理解从来不只是 `?` 后面要回答什么。政治辩论、社交媒体、采访、争论里，问句可以：

- 真正询问信息；
- challenge 对方要求理由；
- 在问句形式下公开表达自己的观点；
- 以修辞问句完成一个 assertion / persuasion move。

所以这个题在不提 LLM、不提 probe 的情况下已经是标准 pragmatics / discourse question：

> **speech-act force 和 propositional contribution 是怎么组合的？**

LLM 恰好提供了一个可以直接检查内部 computation 的系统。

## 3. Mother 1 — contextual rhetorical ambiguity

Ikumariegbe, Blanco & Riloff, **Studying Rhetorically Ambiguous Questions**, EMNLP 2025 Main.

https://aclanthology.org/2025.emnlp-main.1553/

SRAQ 的核心价值：

- 很多同/近似 surface question 只有看 context 才知道是 rhetorical 还是 informational；
- 现有 LMs 对这种 context-sensitive rhetorical interpretation 仍然困难。

它已经证明：**rhetorical force 是真实、context-sensitive、模型并不总能处理好的语言现象。**

## 4. Mother 2 — internal rhetorical representation

Yao et al., **Rhetorical Questions in LLM Representations: A Linear Probing Study**, ACL 2026 Main.

https://aclanthology.org/2026.acl-long.5/

它已经证明：

- rhetorical signal 很早就能从 hidden representation 读出来；
- last-token representation 尤其稳定；
- cross-dataset AUROC 可达约 0.7–0.8；
- 不存在一个简单普适的单一 RQ direction；不同数据 probe 强调 discourse-level stance、local syntax 等不同 cue。

因此我们不能再做“RQ 是否有 representation”。

## 5. Independent linguistic anchor

Hautli-Janisz et al., **Questions in argumentative dialogue**, Journal of Pragmatics 2022:

https://doi.org/10.1016/j.pragma.2021.10.029

其 IAT-based taxonomy 区分：

- Pure Questioning
- Challenge Questioning
- Rhetorical Questioning
- Assertive Questioning

关键定义：**Rhetorical Questioning 是用 question 的形式做 assertion；Assertive Questioning 则在询问的同时公开表达自己的 opinion。**

这说明我们要分的对象不是自己为了实验制造的。

QT30：
https://aclanthology.org/2022.lrec-1.352/

提供 19,842 个自然 broadcast-debate utterances、280k words 和 IAT 式 argument/dialogue annotation，可作为真实 discourse source 之一。

另有 US presidential debate RQ 工作观察到大量 addressor self-answers 会显式确认 implied answer，可作为 source-authored implied-content 子集，而非人工重标 benchmark。

## 6. N0 — mother inclusion

### 已经被做掉

- RQ vs information-seeking detection；
- context-dependent rhetorical ambiguity；
- RQ recognition errors；
- rhetorical status / rhetoricality hidden-state probing；
- “RQs can signal stance/persuasion”；
- 单一 universal rhetorical direction。

### 新 scientific object

我们的目标是：

```text
surface interrogative content
        ↓
context-sensitive speech-act force
        ↓
implied proposition / speaker commitment / stance target
        ↓
downstream response or argumentative interpretation
```

要问：这些阶段是同一个 bundle，还是模型内部有可分的 computation？

**N0 verdict: PASS.**

内部仓库搜索没有发现 rhetorical/implied-assertion 相关 active/archive scientific object。它也不属于已经杀掉的 garden-path、generic negation、Stroop 等 psycholinguistic family。

## 7. N1 — strongest-neighbor attack

搜索：

```text
rhetorical question implied assertion LLM
rhetorical force implied stance language model representation
rhetorical question implied answer LLM mechanistic
speaker commitment rhetorical question LLM
argumentative question implicit stance LLM
```

最强邻居：

1. ACL 2026 RQ representation：只把 rhetoricality 当 target，没有重建 asserted proposition；
2. EMNLP 2025 SRAQ：RQ/IQ behavior，不做 implied proposition mechanism；
3. argument-mining / IAT：有 speech-act 与 proposition graph，但不是 LLM MI；
4. 2026 argument-classification work：报告 RQ/implicit criticism 导致分类失败，但不做 causal factorization。

目前没有找到 work 同时做：

```text
rhetorical force state
vs
implied assertion content
+ causal double dissociation
```

**N1 verdict: PASS.**

## 8. 最重要的 anti-narrowing：不能变成 polarity trick

最危险的坏路线是：

> RQ 通常就是把问题 polarity 取反，所以做 yes/no pair。

这会立刻把一个 ACL/EMNLP 级 pragmatics 题缩成一个小逻辑模板。

真实 RQs 是 heterogeneous：

- opposite-polarity implied answer；
- speaker self-answer；
- evaluative stance；
- argumentative conclusion；
- challenge/assertive hybrid；
- irony/sarcasm 等。

因此数据 preflight 必须证明 source population 能覆盖**多个自然 rhetorical functions**。如果只有 polar RQ 才能得到 gold，本题 PARK/KILL，不允许用宽标题。

## 9. Data strategy

优先 source：

### A. SRAQ

用于 force/context capability：同样 question 在不同 context 下为 rhetorical vs informational。

### B. IAT / AIF corpora

`Questions in argumentative dialogue` 和 QT30 等自然 debate resources 可以提供：

- illocutionary type；
- proposition nodes；
- inference/conflict relations；
- speaker / turn structure。

Preflight 要确认 AIF graph 是否能自动/高精度恢复“question 所完成 assertion 的 propositional target”。不能假设 schema 一定够。

### C. Natural self-answer RQs

政治辩论中 speaker 在 RQ 后自己显式回答，提供 source-authored implied-answer supervision：

```text
RQ: ...?
Speaker: Of course / No / I would ...
```

这一子集特别适合先验证 “force recognized but implied content recovery fails” 是否存在。

### 数据原则

不允许：

- 人工写 500 条 rhetorical questions；
- 用 LLM judge 给 implied stance 当 primary gold；
- 只筛 easy polar questions 后宣称 universal pragmatic mechanism。

## 10. Behavioral prerequisite

建议分三层任务：

### Task A — force

同一/近似 question + context → `information-seeking / rhetorical / assertive / challenge`。

### Task B — implied proposition

给 natural RQ/context → recover speaker commitment / argument proposition。

### Task C — downstream response

给相同 discourse，要求模型：

- 回答 literal question；
- paraphrase speaker's claim；
- identify support/attack target。

寻找真正有解释价值的 dissociation：

```text
force correct
but implied proposition wrong
```

以及：

```text
implied proposition internally readable
but downstream response treats it as literal question
```

## 11. Mechanistic hypotheses

### H1 — fused rhetorical bundle

rhetoricalness 和 stance/content 混成一个 dense state；不同 RQ 类型因此迁移差。

### H2 — force reader → proposition recovery

```text
context
→ speech-act / force state
→ activates pragmatic transformation
→ implied proposition
```

错误可能是 force reader 错，也可能 transformation 错。

### H3 — parallel content and force streams

surface semantic content 一直保留，force state 独立形成，后层 reader 决定按 literal/interpreted content 回复。

这与 ACL 2026 多方向结果非常自然地连接：不同 probe directions 可能不是“噪声”，而是在读不同层次的 pragmatic computation。

## 12. MI plan

只有 behavior/data contract 过后：

1. layer-wise decode force vs implied proposition；
2. same-question cross-context patch：只切 rhetorical force；
3. same-force/different-stance contrast：只切 implied proposition；
4. activation interchange 看是否能将 informational reading 转成 rhetorical reading，同时保持 lexical content；
5. causal patch implied-content state，看 response 是否转向正确 argumentative interpretation；
6. head/SAE analysis只作为解释手段，不可先找 feature 再定义题；
7. test across social media + debates/argumentation，避免 dataset direction。

### Money result

```text
patch force state
→ changes whether question is treated as rhetorical
→ does not decide which stance is asserted

patch implied-assertion state
→ changes recovered stance / argumentative response
→ leaves rhetorical-force classification intact
```

这是一个真正的 causal double dissociation。

## 13. Fatal controls

- question syntax / punctuation；
- sentiment polarity；
- sarcasm markers；
- explicit stance tokens；
- speaker identity / political party；
- answer polarity；
- context length；
- dataset source / genre。

必须 source-held-out / genre-held-out 验证 representation 不是 Qwitter vs Reddit detector。

## 14. PROMOTE / ROUTE / KILL

### PROMOTE

- natural multi-genre source 可定义 implied-content target；
- force 与 content 两个 task 都有足够 competence；
- 存在稳定 dissociation 或 factorized internal computation；
- causal intervention 可分别改变 force/content；
- mechanism 能解释 SRAQ / ACL26 里 heterogeneous representation 的来源。

### ROUTE

如果最终只发现：

> RQ status probe 在另一个 corpus 也工作

直接 route ACL 2026 mother。

### KILL/PARK

- implied content 只能人工主观标；
- 只有 polar RQ 能做；
- effect 完全由 sentiment/party/source 决定；
- 所谓 stance representation 就是普通 sentiment；
- 新 narrative 被迫缩成一个特殊 RQ subtype。

## 15. Source preflight result (2026-08-31)

SRAQ 的 971 条数据只提供 rhetorical/informational force；QT30 的公开
question artifact 覆盖 2,867 条 `Pure/Rhetorical/Assertive Questioning`，但
AIF proposition 是 interrogative semantics，不是 RQ 额外完成的 implied
assertion。公开 response locutions 没有与隐含命题对齐，且大量为空、来自
其他 speaker、或包含多段 response。

因此 source gate 在 central target 上失败，状态为 `PARK-DATA`。没有进行
模型调用；不能用 polarity reversal、任意 next turn 或 LLM-written stance
替代 gold。完整冻结审计见 [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md)，裁决见
[`PREFLIGHT_VERDICT.md`](PREFLIGHT_VERDICT.md)。

## 16. Reopen sequence

```text
1. obtain independently validated implied-proposition / commitment gold
2. verify multi-function and multi-source support
3. freeze force/content capability D0
4. only after D0 passes, start MI
```

**Current model-call authorization: FALSE (`PARK-DATA`).**
