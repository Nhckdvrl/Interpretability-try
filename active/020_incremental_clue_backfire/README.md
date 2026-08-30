# 020 — Incremental Clue Backfire

**中文一句话：** 模型本来已经答对了；再给它一条真实、相关、同样指向正确答案的新线索，它反而会不会改错？

**Status:** `REGISTERED / EASY-PROGRAMMATIC-D0 / ARCHIVE-COLLISION-CHECK-REQUIRED`
**Created:** 2026-08-30
**Top-10 rank:** #7

---

## 1. 研究问题

正常情况下，给一个问题增加正确证据，不应该让已经正确的答案变差。

Quiz Bowl 恰好提供天然的 incremental evidence：一道题由多条线索按顺序逐渐展开，所有线索最终都指向同一个 gold answer。

例如：

```text
clue 1 -> model answers Einstein   ✓
clue 1+2 -> model answers Einstein ✓
clue 1+2+3 -> model answers Newton ✗
```

新增的 clue 3 不是噪声、不是错误文档、不是 adversarial distractor，而是原题作者写的真实线索。

我们问：

> **LLM 的回答是否满足一种 evidence monotonicity：在已经答对后，增加同一 gold 的真实 evidence 不应系统性把答案推走？**

如果出现稳定的 `correct -> more true evidence -> wrong`，就是 Incremental Clue Backfire。

---

## 2. 相邻工作

### Quizbowl / Incremental QA

Rodriguez et al., 2019, *Quizbowl: The Case for Incremental Question Answering* 强调 quiz bowl 的逐步线索适合研究 QA、confidence calibration 与 sequential decision making。

Paper: https://arxiv.org/abs/1904.04792
Open quizbowl data: https://github.com/quizbowl/open-data

公开的 progressive-clue 数据也提供：

- original question id；
- clue spans；
- number of clues consumed；
- gold answer / normalized answers。

### Detrimental Contexts in Open-Domain QA

Oh & Thorne, Findings EMNLP 2023, *Detrimental Contexts in Open-Domain Question Answering*：更多 retrieved passages 有时反而会降低 QA performance，通过过滤 detrimental passages 可改善准确率。

Paper: https://aclanthology.org/2023.findings-emnlp.776/

这个工作说明“more context can hurt”已经不是 novelty。

---

## 3. Novelty boundary

### 不能声称

- 更多文本可能降低 QA accuracy；
- incremental QA 很难；
- retrieval distractors 会伤模型。

这些都有人做过。

### 我们要抓的更窄、更硬的 phenotype

新增 evidence 必须同时满足：

1. source-authored；
2. 属于同一原题；
3. gold answer 不变；
4. 不是检索来的无关 passage；
5. 前一个 prefix 模型已经答对；
6. 新 clue 加入后答案朝某个错误实体稳定移动。

所以对象是：

> **strictly gold-consistent incremental evidence 违反 monotonicity。**

这比“长 context 伤性能”更接近认知里的 belief revision / evidence integration failure。

### 内部 archive collision

仓库历史上有过与“加证据后 referent 被带跑”相邻的失败探索。正式 D0 前必须查 `candidate_topics` / `FAILED_TOPICS`，确认不是把已死的 Evidence-Induced Referent Displacement 换名字复活。

如果旧题的失败原因同样覆盖“真实同答案 clue prefix”，则本题直接 ROUTE/KILL；不能因为换 Quiz Bowl 数据就重开。

---

## 4. 数据为什么简单

Quiz Bowl 本身已经给：

```text
question_id
ordered clue text / clue spans
gold answer
acceptable answer aliases
```

程序只需要构造 prefix：

```text
P1 = clue_1
P2 = clue_1 + clue_2
...
Pk = clue_1 + ... + clue_k
```

每个 prefix 的 target gold 都是同一个 source answer。

不需要任何人类新标注。

Primary source candidates：

- `quizbowl/open-data`
- existing progressive-clue dataset mirrors（必须记录 license 与 provenance）

优先使用能明确还原原始 packet / clue boundary 的 source。

---

## 5. D0

### 5.1 Prefix sweep

对每道题依次跑所有 prefixes：

```text
P1 -> answer
P2 -> answer
...
Pk -> answer
```

forced short answer，不要求 CoT。

### 5.2 Transition table

记录相邻 prefix：

```text
wrong -> correct
correct -> correct
wrong -> wrong
correct -> wrong   <- money transition
```

### 5.3 Gold answer scoring

优先 exact / normalized aliases；不要用 LLM judge。

如果 free-generation 很难 exact score，则附加 closed-set version：

- gold answer；
- model 上一步错误 answer；
- same-category distractors；

但主现象应尽量在原始 answer generation 上复现。

---

## 6. 关键指标

### Backfire transition rate

```text
P(A_{k+1} wrong | A_k correct)
```

但单独这个数字不够，因为任何模型都可能偶尔随机波动。

更诊断：

```text
Δ log P(gold) = log P(gold | P_{k+1}) - log P(gold | P_k)
```

要求新增 clue 后 gold probability 系统下降。

### Wrong-destination concentration

如果新 clue 提到某个 salient entity `e`，错误答案是否特别容易变成 `e` 或与该 clue 局部关联的实体？

这一层可以程序化做 NER / Wikipedia-link，不允许人工挑“看起来像吸引子”的例子作为主分析。

---

## 7. Fatal controls

### New clue 必须真的 gold-consistent

Quiz Bowl 作者可能故意使用 misleading early clues，但整道题仍指向同一答案。我们不能主观假设每一条局部 clue 单独都唯一支持 gold。

所以主 claim 不是“新 clue 单独无歧义”，而是：它是**source-authored member of a question whose official gold is unchanged**。

若要声称“正确证据反而伤害”，更严格的 secondary stratum 需要 external entity linking / retrieval 验证 clue 与 gold 的关系。

### Context length

加入同长度 neutral continuation / duplicate earlier clue，区分 generic length degradation。

### Position

把新增 clue 前置/后置，测试 recency。

### Generation stochasticity

D0 用 greedy / temperature 0；必要时记录 logits。

### Answer aliases

统一 source alias normalization，避免表面字符串变化被误算为 wrong。

---

## 8. PROMOTE / KILL

### PROMOTE

- 两模型家族都有稳定 `correct -> wrong` 超过 matched-length baseline；
- gold logprob 在新增 gold-consistent clue 后系统下降；
- backfire 不只集中在少数 packet / category；
- 至少部分错误有可程序化识别的 late-clue attractor；
- archive collision 审查确认科学对象没有被旧失败直接覆盖。

### KILL

- transition rate 与普通长度/随机波动一样；
- 新 clue 实际经常改变问题 interpretation 或 source gold 有问题；
- effect 只靠人工挑最怪例子；
- 旧失败库已经以同一对象做过并证伪；
- free generation 的“错误”主要是 alias scoring bug。

---

## 9. Mechanistic follow-up

如果成立，候选解释：

1. **late-evidence overwrite**：新 clue 在后层覆盖早先正确 entity state；
2. **recency attractor**：最后出现的 entity/features 权重过高；
3. **confidence reset**：新 clue 触发重新搜索，而不是在已有正确 belief 上增量更新；
4. **entity competition**：gold 与 late-clue-associated distractor 在 residual stream 中竞争；
5. **representation correct / readout wrong**：gold state 仍在，但生成 head 被新 clue route 到错误实体。

可做：

- prefix-to-prefix activation delta；
- layer-wise gold/distractor decoding；
- patch P_k state 到 P_{k+1}；
- ablate late clue token pathways；
- attention from answer position to newly added clue；
- counterfactual replace late clue with another clue for same gold。

---

## 10. 最小执行顺序

```text
1. 先查 FAILED_TOPICS / candidate_topics collision
2. 获取有 ordered clue spans + gold aliases 的 Quiz Bowl source
3. 自动 materialize all prefixes
4. greedy prefix sweep on Qwen3-8B / Gemma-3-12B-IT
5. 算 transition matrix + gold logprob
6. matched-length / position controls
7. 若 phenomenon 清楚，再扩 model family
8. N1 外部 collision search
```
