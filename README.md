# Interpretability Topic Search

这个仓库现在只做一件事：

> **寻找从具体现象 / 具体问题 / 自然概念出发、真正需要可解释性手段来回答、题目尺度与 novelty package 对齐 ACL / EMNLP / NAACL Main，并且能够自然导出后续方法的研究问题。**

本仓库不是“先挑一个 SAE / attention head / activation patching 工具，再去找能解释什么”的仓库；也不是“看到某个模型在某个 benchmark 上掉分，就把掉分本身包装成机制题”的仓库。

当前原则来自连续多轮选题与失败实验，后续新题默认必须遵守。若某个候选与 README 冲突，以 README 为准。

---

# 1. 三条最高优先级要求

## P1 — 题目尺度必须对齐 ACL / EMNLP / NAACL 的正常宽窄

题目不能太宽：

- LLM 为什么会推理？
- LLM 的记忆机制是什么？
- 模型为什么会犯错？

也不能太窄：

- 某个 checkpoint 某层为什么出现一个奇怪方向？
- 某个 benchmark 某种 prompt 为什么掉 5 分？
- 把已有 circuit 换成另一个模型再做一次。

合适的题通常应该能自然形成：

```text
1 个清楚的 mother question
+ 2–4 个自然因素 / competing explanations
+ 一套统一 operationalization
+ 2–4 条能写进 abstract 的 headline findings
+ 至少一个 generalization / boundary-condition 轴
+ 一个由发现自然推出的方法口
```

我们追求的是正常 ACL / EMNLP / NAACL Main 论文的叙事宽幅，不是做一个只够 workshop note 的局部现象。

---

## P2 — Novelty 看“整套叙事”，不是要求每个零件都没人做过

**不要求：**

- 用的方法从没人用过；
- 现象的每个局部都没人观察过；
- benchmark、probe、patching、SAE、训练方法全部全新；
- 必须与所有已有工作完全没有重叠。

这是不现实的，也不是我们筛题的标准。

**真正要求：**

> **我们的 mother question、关键对照（decisive contrast）和整体 narrative package 不能已经被已有工作完整覆盖。**

允许：

- component overlap；
- 技术工具 overlap；
- 局部现象 overlap；
- 使用已有 benchmark / circuit / representation 作为技术基础。

不允许：

- 别人已经提出基本相同的核心问题；
- 别人已经用基本相同的竞争解释和关键干预回答完；
- 我们只能靠换模型、换语言、换领域、换数据集来维持“新颖性”。

如果 decisive contrast 已经被做完，直接 KILL，不靠压窄续命。

---

## P3 — 必须天然留下方法口

研究不能停在：

> “我们证明模型内部有 X。”
>
> 然后呢？

在正式进入实验前，就应该至少能写出：

```text
如果结果支持 A → 应该修哪个环节 / 设计什么目标；
如果结果支持 B → 方法方向为什么不同；
如果发现某个稳定 failure condition → 系统应怎样针对性改善。
```

方法可以是：

- 新训练目标；
- 数据构造策略；
- routing / decoding / inference policy；
- 特定模块设计；
- targeted fine-tuning；
- representation / intervention based repair。

但是方法必须由前面的科学发现推出，不能为了“论文要有方法”最后随便塞一个 steering vector 或 LoRA。

---

# 2. 可解释性选题的额外硬门槛

## I1 — 从具体问题 / 自然现象出发，而不是从解释工具出发

优先对象应该是一句话就能让人理解的外部问题，例如：

- 一个自然、稳定的模型 failure；
- 一个已有认知 / NLP / 推理 / 系统概念；
- 一个现实任务中长期存在的约束或冲突；
- 一个已有 benchmark 已经反复观察到的行为差异。

不要求一定是 Hamdi 的风格，也不要求一定是语言学问题。

我们尤其偏好：

> **普通人一听就明白“模型到底哪里奇怪 / 哪里需要解释”的场景。**

可解释性是为了回答这个问题，不是题目存在的原因。

---

## I2 — Behavior first，mechanism second

健康路径：

```text
自然问题 / 已知现象
→ 公开数据或极低成本 operationalization
→ 便宜、直接、可杀的行为 G0
→ competing explanations
→ representation / circuit / causal intervention
→ method
```

危险路径：

```text
先造数据
→ 再训练 probe
→ 扫层 / SAE / attention
→ 做大量 patching
→ 最后才发现自然行为现象根本不存在
```

**行为 prerequisite 不成立，禁止靠 hidden-state evidence 救题。**

---

## I3 — G0 成本必须低，优先复用已有 benchmark / 公开轨迹

可解释性题最大风险是：先投入大量数据与机制分析，最后发现没有稳定机制。

因此优先级如下：

### 最优

```text
公开 benchmark
+ 目标 failure 已经被论文明确观察到
+ 最好有公开原始输出 / 轨迹
+ 开源模型可跑
+ 最好已有局部 representation / circuit 技术基础
```

### 可以接受

```text
公开数据
+ 只需少量自动化变体
+ gold 可程序化得到
```

### 谨慎

```text
需要自行构造较大数据集
但无需人工标注且 G0 很快
```

### 原则上不做

```text
自己定义 construct
+ 大量造数据 / 人工标注
+ 再赌自然现象是否存在
+ 再赌内部是否有可解释机制
```

在提出机制题之前，尽可能先看到**目标 failure 本身的实际错误样本和规模**，不能只因为 benchmark 总分低就猜“里面应该有我们想研究的错误”。

---

## I4 — 必须有至少两个可区分的机制解释

“哪个 layer 可以 probe 出 X？”通常不是一个完整科学问题。

好的机制题应该至少存在类似：

```text
机制 A：信息本身没有形成 / 被污染；
机制 B：信息形成正确，但 routing / selection 阶段没有使用；
机制 C：前面都正确，最终 readout / serialization 才出错。
```

不同解释必须对 observable / intervention 有不同预测。

如果最后只能得到：

> 某层 AUROC 高；
> 某个 head 很重要；
> 某个 SAE feature 能 steer；

但无法裁决重要的 competing explanations，论文价值很有限。

---

## I5 — Probe 能读出 ≠ 模型真的在用

可解码性只能作为辅助证据。

正式机制 claim 必须尽可能包含因果证据，例如：

- activation patching；
- causal tracing；
- activation interchange；
- targeted ablation；
- causal subspace intervention；
- 其他能够改变目标内部变量的干预。

并且因果干预要有**选择性控制**：

> 改变目标行为，同时保持不相关语义 / 任务变量尽量不变。

如果 steering 只让模型整体更愿意回答、更服从、更输出某个 token，而无法选择性改变目标 construct，不算强机制证据。

优先 on-manifold / matched-pair intervention，警惕用极端 activation addition 把隐藏状态推到分布外后产生伪因果。

---

## I6 — 最好利用已有机制基础，而不是从零盲扫

特别欢迎这种结构：

```text
已有工作：正常情况下某 computation / representation 已经大致定位
我们的题：真实 failure 出现时，到底是哪一步坏了？
```

这比从零开始：

```text
28 层 × 32 heads 全扫
→ 找最显著 component
→ 再编机制故事
```

稳健得多。

已有 circuit / representation 与我们有 overlap 不一定是坏事；只要我们的 mother question 和 decisive contrast 没有被做完，它反而可以显著降低实验风险。

---

# 3. 强制研究链条

每个候选原则上按以下顺序推进：

## Step A — Mother question

先用不超过 2–3 句话说清楚：

- 外部问题是什么？
- 为什么不依赖某个具体模型也有意义？
- 为什么必须/适合用可解释性回答？

如果删掉“hidden state / probe / SAE / attention”之后题目就不存在，通常不合格。

## Step B — Collision audit

广泛检索近年论文，尤其 2024–2026：

- ACL / EMNLP / NAACL；
- ICLR / ICML / NeurIPS；
- Findings；
- arXiv 最新预印本；
- 与该现象相邻的认知 / NLP / 系统研究。

审查的是**母问题和关键对照是否被覆盖**，不是简单数关键词重合。

## Step C — Cheap G0

第一枪只回答：

> **我们要解释的自然现象到底稳定存在吗？**

尽量使用：

- public benchmark；
- official model outputs；
- deterministic evaluation；
- programmatic gold。

G0 失败就归档，不进入机制。

## Step D — Mechanism prerequisite

行为成立以后，再确认：

- 是否存在明确 competing explanations；
- 是否有足够 clean / corrupt matched pairs；
- 是否存在可定义的中间变量；
- 干预结果能否具有选择性；
- 至少一个 confirmation model 是否可行。

## Step E — Mechanism

再进入：

- probes（辅助）；
- representation geometry；
- patching / tracing；
- ablation；
- SAE（只有真的需要时）；
- causal mediation / subspace intervention。

不默认 SAE，也不默认 attention head 是最佳解释单位。

## Step F — Method closes the loop

根据最终支持的机制，设计真正针对 failure source 的方法。

如果方法无论机制 A/B/C 都一样，那说明前面的机制分析很可能没有真正影响方法设计。

---

# 4. 晋级 / 停止规则

每个项目在实验前必须预先写出 STOP gate。

推荐状态：

```text
PRE-CANDIDATE   纸面上值得验证，但尚未过自然现象 G0
ACTIVE          已过行为 G0，值得投入机制分析
HOLD            科学问题还可能成立，但当前 prerequisite / artifact 不够
KILLED          关键自然现象 / decisive contrast / novelty 不成立
ARCHIVED        已终止并保存代码、结果和失败原因
```

禁止的续命方式：

- 自然现象为零后，人工合成大量样本把现象“造出来”；
- 换越来越弱的模型直到出现 failure；
- 换一个更窄 benchmark 只为捞到几个正例；
- 行为 G0 失败后继续做 SAE / probe / attention；
- decisive contrast 已被论文做完后靠换语言/模型维持 novelty；
- 只有单模型、单模板成立却声称一般机制。

失败应该快速、便宜，并且被记录下来。

---

# 5. 当前仓库结构

```text
README.md
archive/
  001_role_value_binding/
    README.md
    ORIGINAL_README.md
    docs/
    src/
    scripts/
    tests/
    pyproject.toml
```

后续项目建议：

```text
projects/<NNN_topic_name>/
```

只有过了纸面 collision audit、值得实际跑 G0 的题，才建立项目目录。

失败后整体移动到：

```text
archive/<NNN_topic_name>/
```

并在归档 README 里记录：

- mother question；
- frozen G0；
- 实际结果；
- STOP verdict；
- 为什么不能续命；
- 哪些经验影响下一轮找题。

---

# 6. 当前状态

**ACTIVE interpretability project：暂无。**

第一个尝试 `role-value binding in structured generation` 已于 2026-08-26 归档：BFCL V4 `simple_python` 公共预检中，Qwen3-4B 与 Gemma3-4B 在 174 个 eligible 样本上都得到 **0 个严格自然 binding failure**，因此按预注册 STOP gate 终止，不进入本地模型、SAE 或 attention 分析。

详见：`archive/001_role_value_binding/README.md`。
