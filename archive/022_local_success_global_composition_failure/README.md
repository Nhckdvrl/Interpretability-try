# 022 — Local Success, Global Composition Failure

**中文一句话：** 两个子问题模型都会，甚至正确答案已经摆在上下文里，最后让它把两步接起来时却还是答错。

**Status:** `REGISTERED / STRONG-COLLISION / MUST-GO-BEYOND-COMPOSITIONALITY-GAP`
**Created:** 2026-08-30
**Top-10 rank:** #9

---

## 1. 先承认最重要的 collision

Press et al., Findings EMNLP 2023, *Measuring and Narrowing the Compositionality Gap in Language Models* 已经明确研究：

> 模型所有 sub-problems 都答对，但最终 composed multi-hop question 仍答错。

他们把这个比例直接命名为 **compositionality gap**，并发现 GPT-3 family 随规模增大，single-hop 提升快于 multi-hop，gap 不会自然消失；self-ask / CoT 能缩小 gap。

Paper: https://aclanthology.org/2023.findings-emnlp.378/

所以：

**“每步都会，合起来不会”本身绝对不是本项目 novelty。**

如果最后只复现这个结果，本题必须 KILL/ROUTE。

---

## 2. 我们还能问什么？

把知识缺失和 decomposition difficulty 再拿掉一层。

我们真正想测试：

> **如果模型刚刚在同一条 conversation 里亲口正确回答了所有必要 subanswers，这些中间事实现在已经显式写在上下文中，它最终仍会不会把它们组合错？**

例如：

```text
User: Who is Alice's father?
Assistant: Bob.

User: Where was Bob born?
Assistant: Paris.

User: So where was Alice's father born?
Assistant: London.   <- composition failure despite explicit local answers
```

这比普通 compositionality gap 更强，因为：

- 不要求模型重新检索第一跳；
- 不要求模型隐式 decomposition；
- 两个中间答案就在上下文里；
- 最终只剩 binding / variable substitution / composition。

暂名：**Externalized Composition Failure** 也可以，README 先保留 Top-10 原名。

---

## 3. 相邻数据工作

### MuSiQue

Trivedi et al., TACL 2022, *MuSiQue: Multi-hop Questions via Single-hop Question Composition*。

Repo: https://github.com/StonyBrookNLP/musique

它由 single-hop questions 组合出 multi-hop questions，并释放 source single-hop question IDs；数据 CC BY 4.0，非常适合自动恢复 decomposition。

### 2WikiMultiHopQA

Ho et al., COLING 2020, *Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps*。

Repo: https://github.com/Alab-NII/2wikimultihop

它提供 reasoning/evidence 信息，可作为第二 source family。

---

## 4. Novelty boundary

### 已知，不可写

- multi-hop 比 single-hop 难；
- subquestions 都对而 whole question 错；
- self-ask 能改善 composition；
- decomposition 有帮助。

### 只有下面这个对象才可能新

最终答案前，把 source-grounded intermediate results **显式外置并冻结在同一 context**：

```text
FACT_1 = correct
FACT_2 = correct
...
FINAL_COMPOSE(FACT_1, FACT_2) = wrong
```

而且必须证明错误不是因为模型忘了前面的文本。

我们要研究的是：

> **正确局部事实已经在 working context 中可读，为什么 relation composition/readout 仍失败？**

**Working novelty hypothesis:** Press et al. 已覆盖普通 compositionality gap；当前尚不确定其 self-ask analysis 是否已经完全覆盖“teacher-/self-produced correct intermediate answers 被显式放在同一 context 后仍发生 final failure”的强条件。N1 必须逐实验核对，而不是只看摘要。如果已做同样实验，则本题直接变 mechanism follow-up。

---

## 5. 数据自动构造

### Primary: MuSiQue

从 dataset/source single-hop mapping 构造：

```text
q1 -> a1
q2(a1) -> a2
...
q_final -> a_final
```

不人工写 decomposition。

### Conditions

#### A. DIRECT_MULTI

只问原 multi-hop question。

#### B. SEPARATE_LOCAL_GATE

独立问所有 source single-hop questions，确认模型具备 local knowledge/reasoning。

#### C. EXPLICIT_GOLD_FACTS

直接把 source gold intermediate facts 写进 final prompt：

```text
Relevant facts:
- ... a1 ...
- ... a2 ...
Question: q_final
```

这是最强 capability control。

#### D. SELF_ANSWER_HISTORY

先让模型自己答 subquestions；只有全部正确的 conversation 继续问 final。

#### E. SHUFFLED/IRRELEVANT FACT CONTROL

同长度 facts，但不形成正确 chain，用于区分“多写几句话”的一般效果。

---

## 6. Money cell

最强 money cell 不是 Press 式：

```text
separate q1 correct
separate q2 correct
final wrong
```

而是：

```text
SELF_ANSWER_HISTORY:
q1 correct in same context
q2 correct in same context
final wrong
```

更硬的是：

```text
EXPLICIT_GOLD_FACTS:
all required intermediate facts source-provided in prompt
final wrong
```

如果后者仍有稳定错误，问题就从 knowledge/retrieval/decomposition 收缩到**composition operator / binding**。

---

## 7. Hard scoring

全部用 source gold / aliases：

- local answer exact normalized match；
- final answer exact normalized match；
- 不用 LLM judge。

对于 entity aliases，使用 source aliases / Wikipedia entity IDs；不要自行 fuzzy-match 到“差不多对”。

---

## 8. 最危险的替代解释

### Context wording 没把 facts 写清楚

EXPLICIT_GOLD_FACTS 用简单 canonical triples / sentences；同时保留 natural self-answer history。

### Answer alias bug

entity ID / source aliases。

### Final question 本身不唯一

只用 source benchmark answerable subset，并 cross-check evidence chain。

### Working-memory / long context

只做短 2-hop/3-hop 主分析；matched irrelevant facts 控制。

### Self-generated error contamination

SELF condition 只保留所有 intermediate answers 已正确的 cases；另有 teacher-forced gold facts condition。

---

## 9. PROMOTE / KILL

### PROMOTE

最低要求：

- `EXPLICIT_GOLD_FACTS` 条件仍存在非平凡 final failure；
- 两家族复现；
- 失败显著高于简单 one-hop reformulation control；
- wrong answers 有可解释 binding destination，例如返回中间实体 `a1`、错误变量 role、错误 relation direction；
- N1 证明不是 Press et al. 已直接报告的同一实验。

### KILL / ROUTE

- 一旦把 intermediate gold 写进 prompt，gap 基本归零；
- 只剩普通 Press compositionality gap；
- errors 主要来自 alias/scoring；
- source decomposition 不能可靠恢复；
- only one model / one relation template；
- 文献已做完全同样的 externalized-facts condition。

如果 KILL，不代表 composition mechanism 没价值；可以直接作为 Press mother 的 MECH-FOLLOWUP，但不占新 phenomenon slot。

---

## 10. Mechanistic value

如果 `all local facts explicitly present -> final composition wrong` 成立，机制问题非常干净：

```text
事实 A 表示存在 ✓
事实 B 表示存在 ✓
最后为什么没有执行正确 substitution / relation composition？
```

候选：

1. entity binding 失败；
2. relation direction 在组合时翻转；
3. intermediate entity representation 没被 route 到 final subject；
4. model 有 local facts，但没有形成 composed latent relation；
5. composed relation 已形成，中后层 readout 又被更近的 intermediate answer attract。

实验：

- probe each intermediate entity/relation；
- decode composed answer across layers；
- patch successful vs failed compositions；
- causal swap intermediate entity activations；
- attention path q_final -> explicit fact1 -> fact2；
- compare explicit triples vs natural sentences。

---

## 11. 最小执行顺序

```text
1. 读 Press et al. full paper，核 exact collision（必须先做）
2. 下载 MuSiQue
3. 自动恢复 2-hop source single-hop chain
4. 跑 DIRECT / LOCAL / EXPLICIT_GOLD / SELF_HISTORY
5. 看 explicit-gold 后还剩多少 failure
6. 如果接近 0 -> 直接 KILL/MECH-FOLLOWUP
7. 如果稳定 >0 -> 分析 wrong destination + 第二 family 2Wiki
8. N1 closure 后 MI
```
