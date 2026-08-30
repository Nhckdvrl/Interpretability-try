# 019 — Abstention Hysteresis

**中文一句话：** 模型一旦先说过“信息不足 / 我不知道”，后来证据已经补齐了，它会不会仍然更容易继续拒答？

**Status:** `D0 COMPLETE / NO-PROMOTE (2026-08-30)`
**Created:** 2026-08-30
**Top-10 rank:** #6

---

## 1. 研究问题

可靠模型应该在信息不足时 abstain，在信息补齐后恢复回答。

我们要研究的是这个**状态转换**，而不是单独问“会不会拒答”：

```text
Turn 1: evidence insufficient
Model: I cannot determine the answer.

Turn 2: missing evidence is supplied
Model: ?
```

对照是：另一条 conversation 一开始就直接看到同样的完整 evidence。

> **最终证据完全一样时，之前做过一次 abstention 是否会让模型更难重新进入 answer mode？**

如果有，就是 **abstention hysteresis**：当前 evidence 已跨过 answerability boundary，但历史 refusal 仍然影响决策。

---

## 2. 相邻工作

### Abstain-QA / Do LLMs Know When to NOT Answer?

Madhusudhan et al., COLING 2025 研究 LLM 在 answerable / unanswerable questions 上的 abstention 能力，并系统比较 prompting。

Paper: https://aclanthology.org/2025.coling-main.627/

### AbstentionBench

Kirichenko et al., 2025，构建大规模 abstention benchmark：20 datasets、6 类 abstention scenario，并发现 reasoning fine-tuning 甚至可能降低 abstention。

Paper: https://arxiv.org/abs/2506.09038
Code: https://github.com/facebookresearch/AbstentionBench
Dataset: https://huggingface.co/datasets/facebook/AbstentionBench

### Abstain-R1 — 非常近的 2026 工作

Zhai et al., Findings ACL 2026, *Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL*。

它强调：unanswerable query 不只要 abstain，还应该指出缺什么信息，并训练 post-refusal clarification。

Paper: https://aclanthology.org/2026.findings-acl.985/

这是本题必须正面处理的 collision。

---

## 3. Novelty boundary

### 已经做过的

- 模型什么时候该 abstain；
- 模型是否能识别 unanswerable question；
- 如何提示/训练它 abstain；
- refusal 之后如何提出有意义的 clarification request。

### 本项目不做这些

我们不评价“第一轮拒答是否漂亮”，也不训练 refusal policy。

我们冻结最终 evidence，研究：

```text
DIRECT_ANSWERABLE:
complete evidence -> answer

POST_ABSTENTION:
incomplete evidence -> model abstains
missing evidence supplied -> same complete evidence state -> answer
```

核心因果变量是**先前是否进入 abstention state**。

Abstain-R1 的“post-refusal clarification”是模型在信息不足时提出/解释缺失信息；本项目问的是**缺失信息真的随后到达之后，旧 refusal 是否继续抑制正确回答**。

**Working novelty hypothesis:** 当前检索没有发现把这一“answerability boundary crossed, but refusal persists”的 history-dependent hysteresis 作为核心现象并做 mechanistic analysis 的论文；但 2026 abstention literature 很活跃，N1 必须严格查。

---

## 4. 数据不需要新人工标签

我们需要有：

- 完整 evidence；
- source gold answer；
- 可以程序化删除、再恢复的关键 evidence。

### Primary candidate A: HotpotQA / MuSiQue supporting facts

利用 source-provided supporting sentences：

1. 完整 context = answerable；
2. 删除 gold supporting sentence(s) = initial incomplete condition；
3. 第二轮把原句原样补回；
4. final answer 仍使用 dataset gold。

### Primary candidate B: AbstentionBench 中成对构造的 math/science ablations

AbstentionBench 已对 GPQA/GSM8K/MMLU-Math 构造 context-removed unanswerable variants。若能稳定恢复 original pair IDs，则直接使用。

### Secondary: SQuAD 2.0

可以从 answerable examples 中移除包含 answer span 的句子，再恢复；但“移除 answer sentence 后真的不能靠世界知识回答”不一定成立，因此只作为备选。

---

## 5. D0 自动构造

对每个完整样本 `x_full`：

```text
x_missing = x_full - gold supporting evidence
missing_chunk = removed source text
```

### A. DIRECT

```text
User: [x_full]
Assistant: answer
```

### B. TWO_STAGE

```text
User: [x_missing]
Assistant: [model response]
User: Here is the missing information: [missing_chunk]
       Now answer the original question.
Assistant: answer
```

### C. MATCHED_NONABSTENTION_HISTORY

第一轮给一个无关、长度匹配的 answered turn，再给 `x_full`，控制多轮 history。

### D. TEACHER_FORCED_ABSTENTION

不使用模型自己的第一轮文本，而固定：

```text
I cannot determine the answer from the information currently provided.
```

用于区分“abstention state”与“某个模型自生成长文本的 lexical priming”。

---

## 6. 主分析必须 recognition-gated

不是每个 ablated item 模型都会 abstain。

真正 decisive denominator：

```text
initial x_missing -> model abstains
DIRECT x_full -> model answers correctly
```

只在这些 item 上问：

```text
POST_ABSTENTION x_full -> 是否仍拒答 / 更低正确率？
```

这避免把“模型本来就不会这题”误写成 hysteresis。

---

## 7. Primary metrics

### Refusal persistence

```text
P(abstain at final | prior abstention, full evidence)
-
P(abstain at final | direct full evidence)
```

### Correct-answer suppression

如果能拿 token logits：

```text
log P(gold answer | post-abstention)
-
log P(gold answer | direct)
```

### Wrong destination

最有趣的不是普通错误，而是：

- 再次拒答；
- 继续说“信息不足”；
- 明明引用了新 evidence，却仍拒绝 commit。

---

## 8. Fatal controls

### Final evidence equivalence

DIRECT 与 POST_ABSTENTION 的**最终可访问信息集合**必须相同。差别只能是历史。

### Missing evidence truly matters

我们不需要研究者主观判断“删完肯定 unanswerable”。直接行为 gate：只有模型 initial condition 确实 abstain 的 item 才进入主分析。

### History length

MATCHED_NONABSTENTION_HISTORY 控制。

### Exact refusal string priming

比较 model-generated / teacher-forced / paraphrased abstention。

如果 effect 只在 exact phrase `cannot answer` 重复时出现，更像 lexical entrainment。

### Safety refusal contamination

只做 epistemic abstention，不混安全 policy refusal。

---

## 9. PROMOTE / KILL

### PROMOTE

- 两家族都有足够的 `initial-abstain + direct-correct` denominator；
- prior abstention 显著增加 final abstention 或降低 gold answer；
- matched-history 明显更弱；
- teacher-forced 与 self-generated abstention 至少方向一致；
- effect 跨两个 dataset family 存在。

### KILL

- final evidence 一补齐就完全恢复；
- effect 全部由 context length 解释；
- 只在 exact refusal wording 存在；
- denominator 太低；
- 无法程序化建立 original/ablated pair provenance；
- 必须人工逐条判断“到底够不够回答”才能跑。

---

## 10. Mechanistic story

如果成立，问题非常像一个 state machine bug：

```text
ANSWERABLE state
   ^
   | new evidence
ABSTAIN state
```

理论上 new evidence 应触发 transition，但模型可能形成 sticky abstention attractor。

可以问：

1. answerability representation 是否已经翻转为 answerable？
2. 如果翻转了，为什么 output policy 仍 abstain？
3. self-generated refusal 是否通过 residual stream / KV history 强化 abstain mode？
4. 新 evidence 在哪层成功进入，但被哪层压掉？

实验：

- layer-wise answerability probe；
- abstain-token vs answer-token logit trajectories；
- patch DIRECT final state into POST_ABSTENTION；
- erase first-turn refusal token activations；
- compare teacher-forced vs self-generated history；
- causal trace missing-evidence tokens 到 final answer。

---

## 11. 最小执行顺序

```text
1. 选一个带 source supporting-fact 的 QA dataset
2. 自动生成 full / evidence-ablated / restore triples
3. 核 schema，不人工打 answerability label
4. 跑 initial abstention + direct correctness gate
5. 只在 gated items 跑 post-abstention condition
6. matched-history control
7. 两模型 smoke
8. N1 深搜尤其对照 Abstain-R1 / 2026 abstention work
```

---

## 12. D0 v1 frozen implementation（2026-08-30）

### Two natural supporting-evidence sources

D0 从本地可追溯的 Hugging Face Arrow cache 构造：

- HotpotQA distractor validation，revision `1908d6afbbead072334abe2965f91bd2709910ab`；
- MuSiQue validation，revision `c8f4f8c9465fb69d31a8eae894c3fd509c4ca321`。

只使用 source-provided supporting paragraph provenance。`full_evidence` 保留原始 paragraph 顺序；`incomplete_evidence` 删除全部 supporting paragraphs；第二轮不是只追加删除片段，而是逐字重复完整 evidence payload，因此 DIRECT 与所有 history conditions 的最后一个 user message 完全相同。

为减少“其实仍可从剩余文本抄答案”，只有 normalized gold/alias string 不出现在 incomplete context 的 item 才 eligible。最终 deterministic bank 为 300 items：HotpotQA 150（bridge/comparison 各 75），MuSiQue 150（2/3/4-hop 各 50）。共有 6,737 个 eligible candidates。bank SHA-256 为 `c385061a7757a2e57f6be69a1e82723c64b66c5401878068dc67494a8cdb0a12`。

### Gate and final conditions

先对全部 item 跑：

1. `capability_full`：完整 evidence 下短答，source-normalized alias EM 或 token F1 ≥.80 才算正确；
2. `initial_missing`：删除 supporting evidence 后是否产生 epistemic abstention；
3. `direct_full`：abstention-enabled protocol 下直接看到完整 evidence。

家族内主 denominator 冻结为 `capability_full correct AND initial_missing abstains`。只有 gated item 进入五个 history conditions：

- `self_abstention`：保留模型自己第一轮的拒答文本；
- `teacher_abstention`：固定 `ABSTAIN` 文本；
- `paraphrased_abstention`：不含 literal `ABSTAIN` 的同义拒答；
- `neutral_same_context`：相同 incomplete user turn，但 assistant history 不拒答；
- `answered_history`：长度较短的无关 answered turn，控制 generic multi-turn / answer-mode priming。

每个 final condition 同时保存 greedy response、abstention classifier、QA EM/F1，以及 `ANSWER` vs `ABSTAIN` continuation 的 length-normalized probability。冻结 PROMOTE 要求至少两家族、每个来源每家族 ≥50 gated items；self-generated history 相对 direct 的 final abstention 至少增加 5pp 且 paired bootstrap CI 过零，continuation probability CI 同样过零，teacher/paraphrase 方向一致，效应强于 neutral/answered histories，并在两个来源均为正。

### N1 collision boundary

Varshney & Baral 的 *Post-Abstention*（2023）研究 selective QA 系统如何重新尝试低置信度样本；方法包括 question paraphrase ensemble、重排 top-N predictions 与 human intervention，目标是改善 risk–coverage，不保留一次自然语言拒答 history，也不操纵缺失 evidence 的到达。Abstain-R1（Findings ACL 2026）训练 unanswerable query 上的拒答与“指出缺什么”，但不测试缺失证据随后到达后的恢复。更接近的是 *Over-Searching in Search-Augmented Large Language Models*（EACL 2026）：它发现此前若干无关 unanswerable questions 会让固定 final query 更倾向 abstain，并称为 multi-turn snowball。后两项工作已经建立“拒答后的处理”和“abstention 有历史依赖”，所以 019 不能把这些宽泛命题作为 novelty。

019 保留的独立问题更具体：同一个 source-grounded question 从 unanswerable 变为 answerable，完整 supporting evidence 确实恢复，最终 user payload 与 direct condition 逐字相同；因果变量是旧的 self/teacher/paraphrased refusal state，并用 same-incomplete-context neutral history 排除单纯重复上下文。当前检索未发现上述 transition-equivalent design 或其 mechanistic analysis，但 novelty 风险从 moderate 上调为 moderate-to-high，必须由清晰、跨来源、跨家族的效应才能抵消。

---

## 13. D0 v1 result

三家族全部完成。冻结的主结果不是 hysteresis，而是显著、跨家族的 **anti-hysteresis / recovery facilitation**：

| Family | Gate (Hotpot / MuSiQue) | Direct abstain | Self-history abstain | Self − direct | 95% paired CI |
|---|---:|---:|---:|---:|---:|
| Qwen3-8B | 91 (68 / 23) | 46.2% | 5.5% | −40.7pp | [−50.5, −30.8] |
| Gemma-3-12B-IT | 118 (69 / 49) | 13.6% | 2.5% | −11.0pp | [−16.9, −5.1] |
| Llama-3.1-8B-Instruct | 76 (55 / 21) | 25.0% | 1.3% | −23.7pp | [−34.2, −14.5] |

`ANSWER` vs `ABSTAIN` continuation probability 的差也分别为 −43.1pp、−19.0pp、−27.7pp，三个 CI 全部严格小于零。Qwen/Llama 的两个来源均为负；Gemma 为 Hotpot −4.3pp（CI [−10.1, 0.0]）和 MuSiQue −20.4pp（CI [−32.7, −8.2]）。

这不是 refusal-specific attractor 的反转证据。same-incomplete-context neutral history 已使拒答相对 direct 下降 Qwen −37.4pp、Gemma −13.6pp、Llama −19.7pp；teacher 与 paraphrased abstention 同样降低拒答。self 相对 neutral 的额外差只有 −3.3pp、+2.5pp、−3.9pp，跨家族不一致。更合理的解释是：先看到 incomplete version、随后看到完整 version，帮助模型注意新增 supporting evidence；旧 refusal 本身不粘。

所有家族均未通过 promotion。Qwen/Llama 的 MuSiQue gate 只有 23/21；Gemma 为 49，刚低于冻结的 50。更决定性的是所有主效应方向与假设相反，teacher/paraphrase 也相反，self 不稳定地优于 neutral。不能把题目事后改写成“repetition helps”或只保留一个来源；那会收窄原问题且缺少对应 causal design。

完整报告见 `D0_V1_REPORT.md`，联合机器可读结果见 `results/d0_analysis.json`。019 到此停止，不进入 mechanistic 阶段。
