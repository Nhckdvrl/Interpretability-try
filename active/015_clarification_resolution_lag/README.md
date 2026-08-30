# 015 — Clarification Resolution Lag

**中文一句话：** 用户已经把歧义解释清楚了，模型会不会还停留在“我不确定你什么意思”的旧状态？

**Status:** `REGISTERED / D0-BUILD-FIRST / BEHAVIOR-FIRST`
**Created:** 2026-08-30
**Top-10 rank:** #1
**Target venues:** ACL / EMNLP / NAACL Main（若行为稳定且能形成清楚机制故事）

---

## 1. 研究问题

现实对话里很多问题一开始确实有歧义，但用户随后会补充一句条件把意思说清楚。例如：

```text
User: How long is a Rainbow Six Siege game?
Assistant: Do you mean one round or a full match?
User: I mean a full ranked match.
```

到最后一轮，问题已经不再含糊。一个理想模型应该立刻切换到唯一解释，并只回答这个解释对应的答案。

我们要测的不是“模型会不会发现歧义”，也不是“给 condition 会不会提升 QA 准确率”。这些已经有人做了。我们真正问的是：

> **当最终可用信息完全一样时，模型如果之前经历过一个 ambiguous state，是否会比“从一开始就看到完整条件”更难进入正确的唯一解释？**

也就是有没有一种 **resolution lag / ambiguity hysteresis**：歧义已经被解除，但旧的 ambiguity state 仍影响后续行为。

---

## 2. 最接近的工作

### 2.1 CondAmbigQA — 直接的数据母体

Li et al., EMNLP 2025 Main, *CondAmbigQA: A Benchmark and Dataset for Conditional Ambiguous Question Answering*：

- 2,000 个 ambiguous queries；
- 每个 query 有多个 `condition -> answer`；
- condition 是显式的上下文约束，用来唯一化问题解释；
- 论文发现：显式提供 condition 能明显提升准确率。

Paper: https://aclanthology.org/2025.emnlp-main.115/
Dataset: https://huggingface.co/datasets/Apocalypse-AGI-DAO/CondAmbigQA-2K

CondAmbigQA 解决的是：**模型是否能利用 disambiguating condition。**

它没有把“最终 condition 相同，但 condition 到达之前的对话历史不同”作为核心因果变量。

### 2.2 PRACTIQ — 多轮 clarification 的直接邻居

Dong et al., NAACL 2025 Main, *PRACTIQ: A Practical Conversational Text-to-SQL dataset with Ambiguous and Unanswerable Queries*：

- 明确构造四轮 conversation：
  `initial ambiguous query -> assistant clarification -> user clarification -> clarified SQL`；
- 有 ambiguous / unanswerable Text-to-SQL；
- 最终 SQL 可执行，因此 gold 很硬。

Paper: https://aclanthology.org/2025.naacl-long.13/
Code: https://github.com/amazon-science/conversational-ambiguous-unanswerable-text2sql

PRACTIQ 证明多轮 clarification 是现实任务，也评估 clarification 后的 SQL 生成；但它的主问题仍是 ambiguous/unanswerable Text-to-SQL 能力，而不是**先前 ambiguity 是否对已解析状态产生持续的历史效应**。

---

## 3. 我们的 novelty 在哪里

### 已知，不可当 novelty

- ambiguous questions 很难；
- 显式 condition 有帮助；
- 模型经常需要 clarification；
- 多轮 clarification 后仍可能答错。

### 本项目真正的新问题

冻结最终 evidence，只改变**它到达之前是否经历过 ambiguity/clarification state**：

```text
DIRECT:
Q + resolving condition -> answer

HISTORY:
Q -> clarification/ambiguity turn -> same resolving condition -> answer
```

最终问题、condition、正确 answer 完全相同。

如果 `HISTORY` 系统性比 `DIRECT` 更差，或更容易：

- 继续追问；
- 同时给多个 interpretation；
- 选择另一个 condition 的 answer；
- 对正确 answer 的 logit/probability 更低；

那么才叫 **Clarification Resolution Lag**。

**Working novelty hypothesis:** 截至 2026-08-30，我们已找到大量 ambiguity resolution / clarification benchmark，但尚未找到把“先前 ambiguous conversational state 对后续已完全 disambiguated judgment 的因果残留”作为核心现象并做 mechanistic follow-up 的工作。正式投稿前必须继续做 N1 collision search，不能把这句话写成已证明的 literature fact。

---

## 4. 数据：尽量不人工标注

### Primary: CondAmbigQA-2K

每条结构近似：

```json
{
  "question": "...",
  "properties": [
    {"condition": "...", "groundtruth": "..."},
    {"condition": "...", "groundtruth": "..."}
  ],
  "ctxs": [...]
}
```

这意味着我们不需要自己发明 ambiguity，也不用人工判断哪个 interpretation 对。

程序自动做：

1. 只取 `properties >= 2` 的 query；
2. 对每个 target property `i`，从其他 property 中选一个 distractor `j`；
3. 构造 direct / history / matched-history 三个条件；
4. target answer 与 distractor answer 都来自 source dataset；
5. 生成反平衡 A/B forced-choice，同时保留 free-generation 次级 readout。

### Secondary: PRACTIQ

若 Text-to-SQL 版本可直接落地：

- 最终 SQL 可执行；
- clarification turn 已存在；
- 可以比较 `direct clarified query` vs `same clarification after ambiguous conversation`。

PRACTIQ 作为跨任务 confirmatory source，不应在 D0 第一轮就混进主分析。

---

## 5. D0 设计

### 条件 A — DIRECT_RESOLVED

```text
Question: Q
Additional condition: C_i
Choose the answer that matches the clarified question:
(A) answer_i
(B) answer_j
```

### 条件 B — AMBIGUITY_HISTORY

```text
User: Q
Assistant: This question can have more than one interpretation. Please clarify which one you mean.
User: C_i
Assistant: [A/B choice]
```

### 条件 C — MATCHED_HISTORY

加入长度接近、但与 ambiguity 无关的中性历史，用来排除“只是 token 更多 / 多一轮 conversation”的解释。

### 条件 D — WRONG-CONDITION sanity

给 `C_j`，gold 应翻到 `answer_j`。若模型根本不读 condition，本题不能解释为 resolution lag。

---

## 6. Primary phenotype

主指标：

```text
lag = P(correct | DIRECT_RESOLVED) - P(correct | AMBIGUITY_HISTORY)
```

更强、更有诊断性的指标：

```text
old-interpretation attraction =
P(other valid interpretation | HISTORY)
- P(other valid interpretation | DIRECT)
```

只看总体 accuracy drop 不够，因为可能只是历史长度干扰。我们希望看到**错误有方向地回到原来的 ambiguity alternatives**。

---

## 7. Capability / validity gates

每个 item 进入 phenotype 分析前必须满足：

1. `DIRECT_RESOLVED` 正确；
2. `WRONG-CONDITION` 能随 condition 翻转到另一个 source-grounded answer；
3. A/B 顺序反平衡后仍正确；
4. target / distractor answer 不能是明显字符串包含关系；
5. matched-history 不产生同量级下降。

这样 null 才能解释为“没有 lag”，positive 才不是普通长上下文 degradation。

---

## 8. D0 成功 / Kill

### PROMOTE

至少两个开放模型家族出现：

- recognition-gated lag > 0；
- bootstrap 95% CI 不含 0；
- 错误显著偏向 source dataset 中的其他合法 interpretation，而非随机错；
- matched-history effect 明显更小；
- A/B counterbalance 不改变方向。

### KILL / ROUTE

- DIRECT 与 HISTORY 无差异；
- 所有下降都被 matched-length history 解释；
- 模型并不能可靠使用 condition；
- 只有 free-form “多说几句”差异，没有可硬评分的 interpretation shift；
- phenotype 只存在于一个非常窄的 question type。

禁止靠人工筛“看起来歧义最漂亮”的几十条续命。

---

## 9. 如果行为成立，mechanism 问什么

核心 fork 很自然：

```text
A. ambiguity representation 本身没有及时消退
B. representation 已经更新，但 output/readout 仍读取旧 state
C. conversation history 中的 self-generated clarification token 形成了持久 action prior
```

可以做：

- layer-wise answer/interpretation logit lens；
- probe ambiguity-vs-resolved state 的时间轨迹；
- activation patch：DIRECT -> HISTORY；
- patch clarification turn / condition turn；
- attention/path analysis：条件信息在哪一层压过旧 interpretation；
- causal intervention：只擦除前一轮 ambiguity-state component，看 lag 是否恢复。

MI 的目标不是“找到 ambiguity neuron”，而是解释一个已经由 output-level paired contrast 建立的**状态更新失败**。

---

## 10. 当前最小执行顺序

```text
D0.1 下载 CondAmbigQA-2K
D0.2 自动枚举 question × condition pairs
D0.3 source/schema audit + 20 random rows 人工抽查 builder 是否写歪
D0.4 Qwen3-8B + Gemma-3-12B-IT smoke
D0.5 如果有 lag，再加第三家族
D0.6 N1 深搜 exact collision
D0.7 冻结正式 behavioral contract
```

人工抽查只是检查程序和 source mapping，**不产生任何新 gold label**。
