# ACL 系列可解释性现象的题目尺度审计

版本：2026-08-28
范围：ACL / EMNLP / NAACL 2025–2026 的代表性主会与 Findings 论文。
用途：校准本项目的题目尺度，不把“扫得多”误当作“问题够大”。这是一份代表性审计，不是完整文献计量。

## 核心结论

ACL 系列会议接受的现象通常并不宽泛。优秀论文往往只有一个非常简单的行为命题：

```text
上下文里出现过的 token 会被无条件抬高概率。
工具虽然不相关，只要参数能对上，模型就想调用。
无关上下文不是随机污染答案，而是触发一种有结构的类别组合。
多跳推理失败集中发生在关系属性提取阶段。
```

题目的“主会尺度”主要不是来自多列几个 bias 或 benchmark，而来自五层证据的闭环：

```text
一句话 phenotype
→ 跨模型 / 跨设置稳定性
→ 决定性对照和结构 signature
→ 因果机制定位
→ 机制导出的干预、修复或新预测
```

## 代表性论文

| 工作 | Venue | 一句话对象 | 行为厚度 | 机制/方法厚度 | 对我们的启示 |
|---|---|---|---|---|---|
| [Llama See, Llama Do](https://aclanthology.org/2025.acl-long.791/) | ACL 2025 Main, Outstanding | 任何在上下文出现过的 token 都会得到 logit 增益 | 多模型、随机 token、事实/反事实与多 prompt | 定位 entrainment heads，消融后效应减弱 | 一个低层 logit 现象也能成为大题，前提是结构纯、跨设置、因果闭环 |
| [Stochastic Chameleons](https://aclanthology.org/2025.acl-long.1458/) | ACL 2025 Main | 无关上下文错误具有 class-based composition 结构 | Llama、Mistral、Pythia，39 类事实关系 | 低层类别形成、高层答案细化、两条竞争路径 | “错误有规律地落到哪里”比平均 hallucination rate 更重要 |
| [Do LLMs Know Tool Irrelevance?](https://aclanthology.org/2026.acl-long.1473/) | ACL 2026 Main | 工具语义无关，但参数结构能对齐时模型仍调用 | 新数据集把语义相关性与参数可填性拆开 | semantic checking 与 structural matching 两条竞争路径 | 一个真实工作流中的单一冲突足够支撑主会，不必覆盖整个 agent failure taxonomy |
| [Back Attention](https://aclanthology.org/2025.emnlp-main.567/) | EMNLP 2025 Main | 多跳失败集中在 relation attribute extraction | 5 个模型、5 个推理数据集 | 四阶段 logit flow；机制导出 back attention 并提升表现 | 现象可以是 computation stage 的选择性瓶颈，但必须产生可验证方法 |
| [Paths Not Taken](https://aclanthology.org/2025.emnlp-main.762.pdf) | EMNLP 2025 Main | 多语事实回忆借道英文，再翻译回目标语言 | 多语言事实一致性 | 区分“未进入英文可靠路径”和“回译失败”；两种向量干预 | 好题常把一个宽 failure 拆成两个可因果区分的错误源 |
| [METER](https://aclanthology.org/2026.acl-long.1668/) | ACL 2026 Main | 因果层级上升时，模型逐渐背离给定情境 | 统一上下文覆盖 causal ladder | 信息流追踪、无关事实干扰与情境忠实度下降 | 若邻近论文已做信息流和干预，单纯再做“该能力下降”没有空间 |
| [Mechanistic Interpretability of Emotion Inference](https://aclanthology.org/2025.findings-acl.679/) | Findings ACL 2025 | 情绪判断由特定 appraisal 表征支持 | 多家族、多尺寸、稳健性检查 | 以认知评价理论组织表征并因果 steering | 老心理理论可以提供轴和机制假设，但不能只复刻人类 bias |
| [Reasoning Circuits in Language Models](https://aclanthology.org/2025.findings-acl.525/) | Findings ACL 2025 | 三段论通过 middle-term suppression 实现 | 多 syllogistic schemes、尺寸与架构 | 找到必要且充分电路，并分析 belief-bias contamination | Findings 也要求超越 probe：必要性、充分性和跨结构泛化非常有分量 |
| [Reasoning–Memorization Interplay](https://aclanthology.org/2025.findings-acl.1111/) | Findings ACL 2025 | 推理与记忆调用的平衡由线性方向调节 | reasoning / memory 条件 | 方向可操纵并因果改变任务表现 | `A 与 B 的竞争方向` 是可接受的窄机制对象，但行为 contrast 必须先站稳 |
| [The Validation Gap](https://aclanthology.org/2025.emnlp-main.1495.pdf) | EMNLP 2025 Main | 模型能算出结果，却不能同样可靠地验证同类算术错误 | 多种算术 operation 与模板 | 错误检测的机制分析 | 原则性构造可以发表，但要有清楚能力解离、系统模板和机制，而非几个手写例子 |
| [Whose Facts Win?](https://aclanthology.org/2026.acl-long.1357/) | ACL 2026 Main | 来源身份、可信度与重复共同改变冲突答案 | 13 个开源模型、不同家族与尺寸 | source preference 与提示/缓解分析 | 已有跨 13 模型的行为占位时，我们必须贡献新的结构性质，而非再报一次偏差 |
| [GroupQA](https://aclanthology.org/2026.findings-acl.2003/) | Findings ACL 2026 | 改写重复可能比真正独立证据更有说服力 | 1,635 问题、15,058 文档 | 主要为行为分析，机制留作未来工作 | 数据规模可以让纯行为工作成立，但也会占领宽母现象 |
| [Exploring the Choice Behavior of LLMs](https://aclanthology.org/2025.findings-acl.270/) | Findings ACL 2025 | 选择同时受内在注意偏好与外部社会影响 | 基于经典理论的虚拟 QA，4 个 GPT/Llama 模型 | 通过自报告区分路径 | 构造并非禁区，但必须由成熟理论和完整实验条件支撑；自报告机制的标准低于我们的目标 |
| [Simple Factuality Probes](https://aclanthology.org/2025.findings-emnlp.880/) | Findings EMNLP 2025 | 长文本生成的 hidden state 已含可预测 factuality 信号 | 开源模型最高到 405B，长文本 hallucination | 轻量 probe，计算成本对比 | 规模很大但因果解释较弱；适合说明“表征存在”，不足以单独证明 computation mechanism |
| [Output-Centric Feature Descriptions](https://aclanthology.org/2025.acl-long.288/) | ACL 2025 Main | 输入侧 feature 描述不能代表其输出因果效应 | 多种自动解释设置 | steering evaluation 与 output-centric 描述方法 | 解释性贡献必须评价 feature 的因果输出作用，不能只看 activating examples |

## Main、Findings 与本项目的尺度差别

### ACL/EMNLP Main 常见充分包

不要求每篇全部具备，但代表性成功论文通常覆盖：

1. 一个可以命名且一句话解释的 phenotype；
2. 多模型家族、多个设置或多个任务中的至少两类外部有效性；
3. 一个排除 generic robustness / capability 的 decisive contrast；
4. 层、位置、head、MLP、direction 或信息流层面的机制定位；
5. causal ablation / patch / steering，而非只有相关 probe；
6. 机制导出的修复或新预测，并检查副作用；
7. 与最近母现象的边界清楚。

### Findings 常见充分包

Findings 可以接受更窄的任务、经典范式构造或较弱的机制，但通常仍需满足其中一种：

- 行为数据规模很大且现象此前未被系统测量；
- 老理论在模型上产生清楚、稳定的新 dissociation；
- 行为任务较窄，但找到必要/充分电路；
- 表征证据跨家族/尺寸并能做因果 steering；
- 新 benchmark 真正解耦了旧 benchmark 混在一起的变量。

只有“某 perturbation 掉了若干点”通常不足。

## 纳入本项目的论文级要求

本项目保留比会议常见论文更严格的 discovery gate：

1. **一句话自然现象，而非 framework。**
2. **五家族至少三家族成立；至少一个三尺寸序列。** 会议论文有时只用 2–3 个模型，但我们用更宽面板降低选题误判。
3. **至少一个真实/公开 source distribution。** 原则性构造可以作为机制对照，不能是唯一叙事锚点，除非像 Validation Gap 一样有成熟问题和系统验证。
4. **一个不可被 generic failure 替代的 signature。** 例如规律性错误落点、recognition–use gap、特定 interaction、非线性或 scaling dissociation。
5. **明确的最近工作 decisive contrast。** 母现象可以已有，独特性质不能已被完整覆盖。
6. **最低 causal package。** 至少要能设计出 representation、routing、readout 三者的区分实验；正式论文要有一项选择性因果干预。
7. **机制产生方法或新预测。** 不要求把 benchmark 刷高，但干预结果必须证明机制解释比行为描述更有用。

## 对搜索策略的直接改变

### 应该优先

- 从真实工作流里找两个竞争路径：semantic relevance vs parameter matching、query route vs context route、reasoning vs memory；
- 在原始错误中检查错误答案落到哪种关系节点，而不是只统计错；
- 找规模增长产生的 dissociation，而不是默认规模会修复；
- 复用成熟心理学、语言学、法律和系统安全问题来定义轴；
- 用公开自然数据做发现，用可控构造做 causal isolation。

### 应该降级

- 只有一个小 benchmark 和一种 choice interface；
- 只有 prompt wording 敏感性；
- 只有 probe accuracy，没有 intervention；
- 只有母现象的新应用领域，没有新的结构性质；
- 为了凑“大题”堆很多互不相关 transformation；
- 先做完整机制，再发现强模型或邻近论文已经杀死行为 novelty。

## 一句话判据

> 删掉模型名、数据集名和 transformation 名以后，如果仍能说出一个现实世界中重要、反直觉且有两个竞争计算解释的问题，它才可能达到 ACL 系列可解释性论文的题目尺度。
