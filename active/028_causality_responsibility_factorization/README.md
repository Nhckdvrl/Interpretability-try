# 028 — Cause Is Not Blame

**Working title:** *Cause Is Not Blame: Separating Event Causality from Responsibility Framing in Language Models*
**Status:** `NATURAL-QUESTION PASS / N0 PASS / N1 PASS / ACTIVE-PREFLIGHT / NO MODEL CALL YET`
**Created:** 2026-08-31

## 1. 一句话问题

> **“X 导致了 Y”和“X 应该为 Y 负责/受责备/获得功劳”不是同一个判断。不同叙事谈同一事件时，LLM 内部会保留一个相对稳定的 causal event model，再单独表示责任 framing；还是 framing 会直接改写模型认为“什么导致了什么”？**

这个问题在政治、新闻、法律、事故调查和日常解释里都天然存在。

例子：

同一个经济衰退可以被两个叙事共同承认某些事件链：

```text
policy change -> investment decline -> unemployment
```

但一个叙事把责任归给政府，另一个强调外部冲击并 exonerate 政府。它们可能对部分 causality 有共同结构，却对 blame / credit 有完全不同 framing。

## 2. 为什么这是主会级问题

LLM 越来越被用来总结新闻、解释政治事件、写政策分析和回答“为什么发生”。如果模型把 **causal structure** 和 **responsibility frame** 混成一个对象，那么：

- 换一种叙事语言可能不只是改变评价语气，而是改变内部因果图；
- 模型可能把“被责备最多的人”误当“真正 causal contribution 最大的人”；
- cross-lingual/source differences 可能在 causal reasoning 层已经产生，而不是 generation style；
- 所谓“中立因果总结”可能不存在一个可恢复的 source-invariant core。

无论结果是哪一种都值得知道：

```text
factorized → model knows what happened separately from who is blamed
entangled   → framing penetrates causal representation itself
```

## 3. Mother paper

Zhao et al., **Reframing Responsibility: Framing-Aware Event Causality Identification**, ACL 2026 Main.

https://aclanthology.org/2026.acl-long.2173/

FrECI 做了几件关键事情：

- 指出标准 Event Causality Identification 只检测 cause-effect link，无法表示政治叙事中的责任 framing；
- 将 causal explanation 扩成 structured claim，包括：
  - responsibility target；
  - evaluative framing（Blame / Credit / Undermine Credit / Exonerate Blame / Neutral）；
  - source type；
  - epistemic modality/certainty；
- 构造 English/Chinese/Arabic aligned narratives，并使用 shared event anchors；
- causal relations 用 LLM high-recall proposals + human two-pass refinement；
- responsibility/framing attributes 有人工 annotation/refinement；
- prompt LLM baselines 对完整 framed causal claim 仍困难，joint supervised models 明显更好。

Mother 已经把 natural object、数据和行为难点做实。

## 4. Mother 没回答什么

FrECI 把 causality 与 framing 都放到 structured output 里，但没有回答：

> **模型内部是把它们作为两个可以组合的变量，还是从一开始就用 framing-conditioned causal representation？**

它没有做：

- open LLM hidden-state geometry；
- source-invariant causal core test；
- responsibility state 与 causal relation 的 double dissociation；
- activation patching / causal interchange；
- framing 是否只改变 late attribution reader；
- framing 是否重写 earlier event-causal state。

## 5. N0 — mother inclusion

### 已被 mother 做掉

- political causal explanations are framed；
- narratives assign responsibility differently；
- framed causal claim extraction；
- multilingual shared-event dataset；
- LLM baseline errors；
- joint modeling of causal relation + responsibility attributes。

### 我们的新 scientific object

```text
event structure / causal relation
            vs
responsibility / evaluative attribution
```

问的是两者**内部 factorization 和 causal interaction**，不是再做 FrECI score。

**N0 verdict: PASS.**

内部仓库对 `cause / responsibility / blame / framing` 的搜索没有发现 duplicate active/archive。`cognitive_decision_making.md` 的 generic authority/source-status bias kill 不吞并本题，因为：

- source authority/credibility 不是 target；
- source 只是生成 framing 的 contextual variable；
- 我们 target 是 proposition-level event causality 与 responsibility attribution 的关系。

如果最后变成“不同 source 让模型偏向不同答案”，就应 KILL，而不是宣称 028 成立。

## 6. N1 — strongest-neighbor attack

搜索：

```text
cause blame LLM responsibility attribution representation
causal responsibility LLM mechanistic
FrECI internal representation mechanism
responsibility framing event causality language model
causal attribution blame mechanistic interpretability LLM
```

最强邻居：

1. **FrECI / ACL 2026** — structured behavior/data mother，不做内部 factorization；
2. document-level ECI work — 做 causal graph extraction，不包含 responsibility framing；
3. 2026 attribution-bias behavioral work — 检查 LLM 是否有人类式 attribution bias，不 reverse-engineer framed causal narrative computation；
4. human/formal causal-responsibility literature — 比较 human blame 与 actual causality formalism，不研究 LM representation；
5. AI-harm responsibility literature — 问 AI/公司/用户谁应负责，是完全不同 scientific target。

截至本轮搜索，没有找到论文完成：

```text
stable/variable event causal representation
vs
responsibility/blame/credit representation
+ causal internal intervention
```

**N1 verdict: PASS.**

## 7. 为什么不是 generic “framing bias”

我们不能写：

> “framing 会影响 LLM 的责任判断。”

这太宽、太旧，也很容易被 source/language bias literature 吃掉。

真正的 title-level question 是：

> **When two narratives frame responsibility differently, does the model preserve the same underlying causal relation and alter only responsibility attribution, or does the causal representation itself shift?**

因此 money contrast 必须能把：

```text
causal relation held / shared
responsibility frame varies
```

和：

```text
causal relation genuinely differs
```

区分开。

## 8. Data strategy

### Primary discovery source — FrECI

优点：

- natural political narratives；
- human-refined causal links；
- human responsibility targets/framing effects；
- aligned English/Chinese/Arabic topics；
- shared event anchors；
- blame/credit/exoneration 等不是我们自己写的 synthetic labels。

### Preflight 要做的不是“能下载数据吗”，而是 population audit

需要统计：

1. 是否有**同一 event anchor / causal pair**在多个 narrative/source 下出现；
2. causality label 稳定但 responsibility framing 不同的 matched units 数；
3. causality + framing 都变的 negative controls；
4. source/language held-out support；
5. each framing category 的 cluster 数，而不是 annotation 数；
6. 是否能避免同 topic paraphrase 当独立样本。

### Second source / breadth requirement

ACL/EMNLP-wide claim 不能只靠一个 political corpus 的某一 label。确认阶段至少需要一个：

- 第二个自然 news/political framing corpus；或
- legal/accident narrative attribution source；或
- FrECI 内足够强的 cross-language + source-held-out generalization，并在论文中把 scope 明确为 contested narrative causality。

如果没有第二种支持，title 不能偷偷缩成 `FrECI representation analysis`。

## 9. Behavioral prerequisite

先确认 open model 在两个独立 task 上有 competence：

### A. Causal core task

给 narrative/context + event pair：是否 cause-effect？

### B. Responsibility task

给同一 causal situation：谁被 blame/credit/exonerate？

然后找到 matched frame sets：

```text
same/shared causal relation
frame 1 -> blame A
frame 2 -> exonerate A / blame B
```

我们不要求 model 必须有 giant failure 才允许 MI；但必须有足够 competence，否则 probe 只会读 lexical label。

## 10. Competing mechanisms

### H1 — Factorized causal core + framing head

```text
events
→ causal relation state (relatively source-invariant)
→ framing/responsibility state (source/context-conditioned)
→ final explanation
```

### H2 — Framing rewrites causality early

责任语言/叙事选择直接改变 causal relation representation；不存在可恢复的中立 causal core。

### H3 — Causal core and responsibility both represented, but late reader conflates them

模型中层能分别表示：

```text
X caused Y
X deserves blame
```

但生成 causal explanation 时 reader 用 blame salience 替代 causal strength。

### H4 — Shared actor salience explains both

看起来像 factorization 的 probe 其实只是 actor/source identity。必须用 actor-balanced / event-held-out controls 杀掉。

## 11. Mechanistic plan

通过数据/capability gate 后：

1. layer-wise decode causal relation vs responsibility target/frame；
2. cross-source / cross-language transfer；
3. actor identity residualization；
4. same-event-anchor representation similarity；
5. activation interchange between differently framed narratives；
6. patch responsibility state：是否改变 blame/credit 但保留 causal-link judgment；
7. patch causal state：是否改变 causal relation而不自动改变 moral/evaluative framing；
8. trace final explanation reader：什么时候 responsibility signal 开始影响 causal wording；
9. mechanism-derived mitigation：要求 source-neutral causal summary时，应该 suppress frame reader 还是 restore causal core？

### Money result A — factorization

```text
responsibility patch
→ blame/credit changes
→ causal relation stable

causal patch
→ cause-effect judgment changes
→ responsibility frame does not trivially flip
```

### Money result B — deeper and also publishable

如果发现：

> 同一个 shared-event causal relation 在 early/mid layers 就随 narrative framing 分裂，且不存在 stable causal core

这也是强结论：**framing does not merely color explanations; it reconstructs causality itself.**

## 12. Fatal controls

- actor identity/frequency；
- sentiment/emotional valence；
- explicit blame words；
- source label；
- language；
- event type；
- quotation attribution；
- certainty/modal words；
- causal connective tokens；
- political party/entity memorization。

要有 frame-preserving lexical paraphrase 和 frame-changing minimally matched contrast wherever source permits。

## 13. PROMOTE / ROUTE / KILL

### PROMOTE

- matched natural event anchors 有足够 support；
- ≥2 open model families 有 causal + responsibility competence；
- representation relation跨 source/language/topic 稳定；
- causal intervention 能区分 factorized vs rewritten-causality accounts；
- mechanism 不只是 source/actor/sentiment decoder；
- title 仍然是 cause-vs-responsibility，而非 FrECI-specific probe。

### ROUTE

如果只能得到：

> joint causality + responsibility modeling 比 separate classification 好

route 回 FrECI mother。

### KILL/PARK

- shared-event matched support 太少；
- effect 只由 explicit blame words；
- “causal state”完全是 actor pair identity；
- novelty 必须缩成一个 language/source/type；
- 只能写“political framing biases LLM outputs”。

## 14. Anti-narrowing contract

发现数据不足时，允许：

> `PARK-DATA: natural question survives, current source insufficient`

不允许：

> 从 “cause vs responsibility” 偷偷缩成 “English FrECI Blame-vs-Neutral head in Qwen”。

后者不够 ACL/EMNLP title-level breadth。

## 15. 下一步

```text
1. FrECI artifact/schema/source audit
2. count matched same-event causal-core / different-frame clusters
3. check human-label provenance + leakage
4. identify independent second-source option
5. freeze capability-only D0
6. only after gate passes, run MI
```

**Current model-call authorization: FALSE.**
