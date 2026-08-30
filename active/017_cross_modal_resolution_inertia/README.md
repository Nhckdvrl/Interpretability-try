# 017 — Cross-Modal Resolution Inertia

**中文一句话：** 文字一开始有歧义，模型先形成了一个解释；后来图片已经把正确意思定死了，它会不会还被最初那个解释拖着走？

**Status:** `REGISTERED / DATASET-READY-SHAPE / MULTIMODAL`
**Created:** 2026-08-30
**Top-10 rank:** #4

---

## 1. 研究问题

人会先根据文字形成一个 provisional interpretation，之后看到图片再修正。例如：

```text
Text: He is standing by the bank.
```

单看文字，`bank` 可以是银行，也可以是河岸。如果随后看到一张明确的河边图片，最终解释应该变成“河岸”。

MUCAR 已经告诉我们：MLLM 在静态的 image+text ambiguity resolution 上仍然很难。

本项目不重复问“图像能不能帮助消歧”。我们问一个更具体的动态问题：

> **如果模型在图像出现之前已经处理过 ambiguous text，甚至已经表达了某个 interpretation，那么同一张 disambiguating image 后到时，旧 interpretation 会不会继续影响最终判断？**

即：**cross-modal resolution 是否存在 history-dependent inertia。**

---

## 2. Mother paper：MUCAR

Wang et al., EMNLP 2025 Main, *MUCAR: Benchmarking Multilingual Cross-Modal Ambiguity Resolution for Multimodal Large Language Models*。

Paper: https://aclanthology.org/2025.emnlp-main.760/
ArXiv: https://arxiv.org/abs/2506.17046

MUCAR 两个重要部分：

1. ambiguous textual expression + visual context，视觉唯一化文本；
2. dual-ambiguity：image 与 text 单独都 ambiguous，但组合后只有一个清晰 interpretation。

论文在 19 个 MLLM 上显示明显的人机差距。

这意味着“静态 cross-modal ambiguity resolution 很难”已经不是我们的 novelty。

---

## 3. Novelty boundary

### 已经被 MUCAR 做掉的

```text
ambiguous text + image -> 能不能选对 interpretation？
```

这个不能重新包装。

### 我们要测的

最终输入证据相同，只改变信息到达顺序：

```text
SIMULTANEOUS:
image + ambiguous text -> final interpretation

TEXT-FIRST:
ambiguous text -> provisional response
then same image -> final interpretation
```

如果 `TEXT-FIRST` 比 `SIMULTANEOUS` 更容易维持旧 interpretation，才叫 **Resolution Inertia**。

更强的版本：只分析第一轮确实 committed 到一个、且这个 interpretation 与最终 MUCAR gold 不同的 item，然后看图片到达以后是否改得回来。

**Working novelty hypothesis:** MUCAR 研究 cross-modal disambiguation 能力，但没有把“先处理一个 modality 形成旧 interpretation”作为独立 treatment、并与 simultaneous final evidence 做因果对照。投稿前必须继续核查 multimodal conversational correction / anchoring 文献。

---

## 4. 数据

### Primary: MUCAR dual-ambiguity subset

理想结构：

```text
ambiguous text T
ambiguous image I
gold interpretation y(T,I)
```

dataset 自己定义组合后的唯一 interpretation，因此我们不需要人工给 image-text pair 标 sense。

优先使用 dual-ambiguity，因为单 modality 本来就 ambiguous，更适合测试“先形成 provisional state，后被另一 modality 更新”。

### 备选：multilingual text-disambiguated-by-image subset

作为 cross-language confirmatory，不应一开始就混入主 D0。

---

## 5. 自动构造

对每个 MUCAR item：

### A. SIMULTANEOUS

直接给 `(image, text)`，要求在 source-provided interpretations 中选择唯一答案。

### B. TEXT_ONLY

只给 text，让模型在 candidate interpretations 中选择或明确表示 uncertain。

这一步不是最终评分，而是用来得到 initial state。

### C. TEXT_FIRST_THEN_IMAGE

Conversation：

```text
User: [text only]
Assistant: [model's first interpretation / uncertainty]
User: [same image] Use the image to settle the intended meaning.
Assistant: [final forced choice]
```

### D. MATCHED_PRIOR_HISTORY

在 image+text 前加入长度接近但无关的先前 turn，控制 conversation length / self-output exposure。

### E. IMAGE_FIRST_THEN_TEXT

顺序反转，检查 inertia 是否是 modality-specific。

---

## 6. 最关键的 phenotype

### Correction failure among initially wrong commitments

定义：

```text
TEXT_ONLY chooses j != gold
SIMULTANEOUS chooses gold
TEXT_FIRST_THEN_IMAGE still chooses j
```

这是最干净的 money cell：

- 模型证明自己联合看 image+text 是会的；
- 第一轮形成了错误旧解释；
- 唯一区别是旧解释是否已经进入 conversation/state；
- final evidence 完全相同。

主指标：

```text
inertia_rate = P(final stays at initial wrong interpretation
                 | initial wrong, simultaneous correct)
```

同时报告 final correct probability drop。

---

## 7. 为什么这不是普通“看图能力差”

必须 gate：

1. `SIMULTANEOUS` 正确；
2. image-only / text-only capability 按 MUCAR category 记录；
3. initial text choice 与 final gold 不同才进入 correction-failure money cell；
4. matched-history 不造成同等下降；
5. option order counterbalance；
6. image preprocessing 在所有 conditions byte-identical。

如果 simultaneous 本来就错，不能拿来证明 inertia。

---

## 8. 潜在替代解释

### Self-generated answer priming

TEXT-FIRST history 里有模型自己写过的旧答案，所以 effect 可能只是 lexical self-priming。

必须加：

- teacher-forced neutral ambiguity response；
- teacher-forced wrong interpretation；
- paraphrased wrong interpretation；
- initial answer string masked / replaced by label。

如果只有 exact old string 重复时才有 effect，更像 lexical entrainment，不是 multimodal state inertia。

### Conversation-format cost

MATCHED_PRIOR_HISTORY 控制。

### Image arrives too late / attention dilution

比较 `IMAGE_FIRST_THEN_TEXT` 与 simultaneous，并控制 token count。

---

## 9. PROMOTE / KILL

### PROMOTE

- 至少两个 MLLM family 在 gated set 上出现明显 inertia；
- initial wrong interpretation 有显著 persistence；
- simultaneous 同 item 明显更好；
- effect 不被 matched history / exact-string priming 完全解释；
- text-first 与 image-first 存在可解释的不对称，或二者都表现为一般 commitment inertia。

### KILL / ROUTE

- simultaneous 与 sequential 无差异；
- effect 完全来自上下文更长；
- 只有 exact old answer string priming；
- denominator 太小（模型 text-only 几乎从不 commit 或 simultaneous 几乎不会做对）；
- MUCAR 的 source labels 无法稳定转成 hard forced-choice。

---

## 10. Mechanistic questions

如果成立，故事可以非常清楚：

```text
文字先形成 sense state S_old
图片提供 disambiguating evidence E_img
最终应形成 S_new
但模型为什么没有 overwrite / rebind？
```

候选机制：

- language-stream representation 先形成稳定 attractor；
- visual tokens 只能调输出 confidence，不能改 language sense state；
- cross-attention 写入太晚；
- self-generated old answer 通过 autoregressive context 强化旧 attractor；
- multimodal fusion 层形成正确 state，但后层 language readout 回到旧 state。

可以做：

- layer-wise sense decoding；
- image-token -> ambiguous-word attention tracing；
- simultaneous activation patch 到 sequential；
- patch/ablate first-turn answer representations；
- compare image-first vs text-first fusion trajectory。

---

## 11. 最小执行顺序

```text
1. 获取 MUCAR data + source interpretation labels
2. 只做 dual-ambiguity subset schema audit
3. 自动生成 simultaneous / text-only / sequential / matched-history
4. 先跑一个支持图像输入的 open MLLM smoke
5. 看 gated denominator 与 inertia transition matrix
6. 若存在再上第二家族
7. N1 collision search
8. 才做 MI
```

本项目**不需要我们重新给图片或文字打 sense label**；人工只检查 builder 对 source label 的映射。
