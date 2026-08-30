# 023 — Description–Experience Gap in LLM Risk Choice

**中文一句话：** 同一个概率游戏，直接把概率告诉模型，和让它看一串完全等价的历史结果，最后会不会做出系统不同的选择？

**Status:** `REGISTERED / PROGRAMMATIC-DATA / BEHAVIORAL-ECONOMICS-MOTHER`
**Created:** 2026-08-30
**Top-10 rank:** #10

---

## 1. 研究问题

人类风险决策里有一个经典现象叫 **description–experience gap**：

- **description**：直接告诉你“80% 赢 10 元，20% 输 20 元”；
- **experience**：不告诉概率，只让你一次次看到结果，再做选择。

即使底层 gamble 相同，人类的风险选择也可能因为信息获取方式不同而系统变化。

我们想问：

> **LLM 面对同一个 objective outcome distribution，仅仅把概率“写成描述”或“展开成历史经验序列”，是否会形成不同的风险判断与选择？**

如果差异稳定，再问 mechanism：两种输入是否最终形成了不同的 probability/value representation，还是表示相同但 choice readout 不同。

---

## 2. 人类 mother phenomenon

Description–experience gap 是 judgment and decision making 的成熟研究对象。核心定义就是：choice 取决于风险信息是通过 summary description 获得，还是通过 sequential sampling experience 获得。

综述例：Hertwig / Erev 等相关 description-vs-experience literature；可参考：

- *Mind the gap? Description, experience, and the continuum of uncertainty in risky choice* (2013)
- *The description–experience gap: a challenge for the neuroeconomics of decision-making under uncertainty* (2021 review)

Review: https://pmc.ncbi.nlm.nih.gov/articles/PMC7815421/

这给我们一个自然、人类已有的 mother phenomenon，不是为了 LLM 临时造 bias。

---

## 3. LLM 相邻工作

已有大量工作测试 LLM 的 cognitive biases / risky choice：

### Cognitive Bias in Decision-Making with LLMs

Echterhoff et al., Findings EMNLP 2024，构建 BiasBuster，在大量 prompts 上测试多种 cognitive bias。

Paper: https://aclanthology.org/2024.findings-emnlp.739/

### 2026 risk-choice work

已有工作用 Holt–Laury、expected utility 等范式研究 LLM 风险偏好，并发现 reasoning configuration、persona、prompt framing 会明显改变选择。

这意味着“LLM 有风险偏好 / 会受 framing 影响”本身并不新。

---

## 4. Novelty boundary

### 不能声称

- LLM 有 cognitive bias；
- LLM 风险决策不稳定；
- prompt format 会影响 gamble choice；
- LLM 不是稳定 expected-utility agent。

### 本项目真正的 paired object

严格保持 objective distribution 相同：

```text
DESCRIPTION:
80%: +10
20%: -20

EXPERIENCE:
exactly 80 +10 outcomes
exactly 20 -20 outcomes
shown as a sequence
```

然后比较同一 choice。

更严的版本不靠随机 sampling，而是**exact-frequency matched experience**，避免 human literature 中常见的 sampling error / rare-event under-sampling confound。

因此我们研究的是：

> **representation format 本身是否改变 LLM risk choice，即使 empirical experience 与 stated probability 精确一致。**

**Working novelty hypothesis:** 当前找到大量 LLM cognitive-bias / risk-preference work，但尚未找到把经典 description–experience gap 用 exact-frequency-controlled sequences 系统做在 LLM 上并追机制的强相邻论文。该领域 2026 更新很快，正式推广前必须 N1 深搜。

---

## 5. 数据不需要人类标注

这题甚至不需要外部 dataset 才能生成主 stimulus，因为 gamble 是**确定性程序对象**。

但要注意：我们不是为了无限 synthetic data，而是复现经典 human behavioral paradigm。

程序生成 gamble：

```text
Option A: outcomes {(x1,p1), (x2,p2), ...}
Option B: outcomes {(y1,q1), (y2,q2), ...}
```

并自动生成：

### DESCRIPTION

直接写概率。

### EXPERIENCE-EXACT

用一个固定长度 `N`，令每个 outcome 出现次数恰好为 `p*N`。

例如 `p=.8, N=100`：恰好 80 wins + 20 losses。

### EXPERIENCE-SHUFFLES

同一 multiset 多个随机顺序，只改变 recency/order，不改变频率。

### DESCRIPTION-AS-COUNTS

“100 次里 80 次赢、20 次输”，控制 probability notation vs count notation。

---

## 6. 为什么没有“正确答案”也可以做

这不是 QA benchmark，目标不是 accuracy，而是**同一 preference problem 的 paired choice consistency**。

我们不需要人工说“应该选 A 还是 B”。

主变量是：

```text
P(choose A | description)
vs
P(choose A | exact experience)
```

如果要增加 normative control，可以构造 stochastic dominance cases：某 option 在所有 outcome 上都不差且至少一处更好。此时有 hard rationality oracle，但它只是 sanity，不是主 phenomenon。

---

## 7. D0 stimulus family

不能只用一个 gamble。程序自动生成多个 predeclared family：

1. rare gain vs common moderate gain；
2. rare loss vs common small loss；
3. mixed gain/loss；
4. equal expected value but different variance；
5. one option stochastically dominates（sanity）；
6. symmetric sign-flip pairs。

每个 gamble 做：

- option-order counterbalance；
- amount scaling；
- sequence shuffle；
- exact frequency；
- no persona / no emotional story 主版本。

不要为了找 effect 后验挑某一种 gamble。

---

## 8. Primary metrics

### Choice gap

```text
DE_gap = P(A | EXPERIENCE_EXACT) - P(A | DESCRIPTION)
```

按 human mother literature 预先定义 rare-event weighting direction；但第一轮也应报告全量 paired transition：

```text
A -> A
A -> B
B -> A
B -> B
```

### Internal probability estimate control

在做 choice 前另开独立 run：

```text
Based on this sequence, what fraction of outcomes were +10?
```

如果模型连 exact frequency 都读错，则 choice gap 可能只是 counting failure。

真正有趣的 gate：

```text
frequency estimate correct
expected value calculation correct
choice still differs by presentation mode
```

---

## 9. Fatal confounds

### Sequence length / memory

Experience 是长输入。必须做 count-description、compressed sequence、不同 N 的 controls。

### Recency

同一 multiset 多 shuffle，报告 last-k composition。

### Sampling error

主分析使用 exact frequency，不随机近似概率。

### Arithmetic

独立 probe empirical frequency / expected value。

### Conversational framing

两条件 instruction 尽量相同，只改变 information format。

### Stable preference assumption

不要说“模型真实偏好”这种强人格化语言。我们测的是 conditional choice policy。

---

## 10. PROMOTE / KILL

### PROMOTE

- 至少两个家族有稳定 description-vs-experience choice gap；
- empirical frequency / EV capability gate 通过后仍存在；
- gap 不被 sequence recency / length 完全解释；
- 多个 gamble family 同方向或形成与 rare/common structure 对应的规律；
- option order / amount scaling 后稳定；
- N1 确认没有近期 LLM paper 已系统做完全相同范式。

### KILL

- exact-frequency experience 与 description 基本一致；
- effect 全由 counting error；
- effect 全由 last few outcomes recency；
- 只有一个 gamble template；
- option order 一换就没；
- 已有相邻工作完整覆盖 phenomenon + mechanism。

---

## 11. Mechanistic questions

如果模型能正确复述概率，却选择不同，故事会很漂亮：

```text
explicit description -> probability/value representation D
experience sequence -> probability/value representation E

D 和 E 是不是不同？
```

候选：

1. experience 形成 recency-weighted latent frequency；
2. explicit percentages 直接激活 symbolic probability circuit；
3. 两种 probability state 最终一样，但 value integration / action readout 不一样；
4. rare outcomes 在 sequence 中被 attention 稀释或被高 salience 放大；
5. reasoning tokens 能显式算对 EV，但最终 choice head 仍使用另一条 heuristic pathway。

可做：

- decode empirical probability across layers；
- compare representation similarity description vs experience；
- patch description probability state into experience choice；
- causal ablate late outcome tokens；
- recency-position interventions；
- separate probability, utility, final action probes。

---

## 12. 最小执行顺序

```text
1. 写 deterministic gamble generator
2. exact-frequency description/experience pairs
3. frequency + EV capability probes
4. 两家族 greedy D0
5. sequence shuffle / N / recency controls
6. stochastic-dominance sanity
7. N1 深搜最新 2026 LLM risk-choice literature
8. phenomenon 稳定后才做 representation / patching
```

本项目不需要人类新标注；唯一“人工设计”的只是经典实验范式参数，而不是逐样本 gold。
