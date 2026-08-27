# 顶会现象型可解释性论文：发现母结构与占位地图

版本：2026-08-28
范围：ACL / EMNLP / NAACL 主会优先，Findings 用于下界校准；ICLR / ICML / NeurIPS 只用于机制与选轴灵感。
索引辅助：[Paper Notes](https://papernotes.org/)；论文结论与撞车判断以 ACL Anthology、PMLR、OpenReview 或 arXiv 原文为准。

这不是完整 survey。它回答两个内部问题：

1. 成熟论文是怎样从一个简单异常长成主会故事的？
2. 哪些宽母现象已经被占领，候选必须再多出什么独特性质？

## 一、反复出现的八种成功母结构

### P1. 内容还在，但被错误路由或读出

行为句式：

> 模型明明内部保留了 A，最终行为却像没有 A，或者把 A 用在了错误槽位。

成熟工作的关键不是“probe 能读出”，而是把 `representation → transport → readout` 拆开并因果裁决。例如 [SelfElicit](https://aclanthology.org/2025.acl-long.448/) 表明相关证据位置在内部可被利用，[Back Attention](https://aclanthology.org/2025.emnlp-main.567/) 把多跳失败定位到特定信息处理阶段，[Language Models Use Lookbacks to Track Beliefs](https://openreview.net/forum?id=6gO6KTRMpG) 则把信念追踪还原为可交换干预的寻址算法。

候选池应优先寻找：

```text
识别正确 / 使用错误
实体内容正确 / 角色绑定错误
局部证据可取 / 全局答案槽错误
状态可解码 / 行动仍沿旧路径
```

只做一个线性 probe 不够；ACL 2026 的 [Linear Probes Detect Task Format, Not Reasoning Mode](https://arxiv.org/abs/2606.02907) 直接提醒，probe 可能读到接口而不是目标计算。

### P2. 两条竞争路径在一个自然条件下改换主导权

行为句式：

> 语义路径明明给出正确结果，但某个结构、角色或先验匹配路径抢先控制了输出。

[Do LLMs Know Tool Irrelevance?](https://arxiv.org/abs/2604.11322) 用“语义无关但参数可填”拆开 semantic checking 与 structural matching；[Stochastic Chameleons](https://aclanthology.org/2025.acl-long.1458/) 显示无关上下文错误不是随机，而有类别组合路径；[How Language Models Conflate Logical Validity with Plausibility](https://arxiv.org/abs/2510.06700) 则把逻辑结构与内容可信性表示的竞争作为对象。

适合候选池的自然冲突包括：

```text
当前状态 vs 历史路径
对象身份 vs 属性相似
证据独立性 vs 表面数量
行动后果 vs 动作可执行性
回答对象 vs 新线索中最显著的邻居
不确定性 vs 必须给答案的 writer
```

### P3. 同一能力的生产、验证和使用并不同构

行为句式：

> 模型会产生 X，却不会验证 X；会说明规则，却不让规则控制行动。

[The Validation Gap](https://aclanthology.org/2025.emnlp-main.1495/) 把算出答案与验证错误分开；[Confidence v.s. Critique](https://aclanthology.org/2025.acl-long.203/) 把自我纠正拆成置信与批评；[Thinking Out Loud: Do Reasoning Models Know When They’re Right?](https://aclanthology.org/2025.emnlp-main.73/) 研究推理模型对自身正确性的可见性。

因此“solve vs verify”“report vs use”本身已经是拥挤母现象。新卡必须再有一个具体而自然的非对称，例如：

- 能主动构造一个有效反例，分类时却仍把同一论证判为有效；
- 能预测工具副作用，执行时却不把预测送入 veto；
- 能准确指出同源证据，决策时却继续按文档数投票。

### P4. 错误不是随机消失，而是落到有结构的邻接状态

行为句式：

> 模型不是忘了答案，而是稳定地变成了某个关系邻居、旧状态、默认槽或竞争类别。

[Stochastic Chameleons](https://aclanthology.org/2025.acl-long.1458/) 的价值就在“错误落点”；本仓库的 [EIRD](../promoted/002_evidence_induced_referent_displacement.md) 也因此比普通增量 QA 掉点更强。

候选验收时必须保存 wrong destination taxonomy：

```text
old state / next state
type / token
whole / part
agent / patient
source / report
plan / outcome
mentioned / asserted
possible / actual
```

### P5. 扫自然进程轴，寻找非线性、迟滞或反常尺度律

行为句式：

> 不是“越难越差”，而是在某个自然边界突然换模式，或规模越大分离越明显。

[Lost in the Middle](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long) 扫位置得到 U 形；[Premise Order Matters](https://proceedings.mlr.press/v235/chen24i.html) 扫等价排列得到 proof-order 结构；[The First Impression Problem](https://arxiv.org/abs/2505.16448) 研究初始内部偏置触发过度思考；ACL 2026 的 *Logical Phase Transitions* 则直接把逻辑推理中的 collapse shape 作为对象。

高价值自然轴：

```text
事件从计划→尝试→完成→撤销
证据从相关→充分→重复→相关但引入新实体
目标从提出→确认→替换→取消
状态从创建→修改→删除→重建
不确定性从未知→部分证据→充分证据
引用/假设 scope 从进入→嵌套→退出
```

### P6. 强模型学会 A，却没有同步学会 B

行为句式：

> 规模提升让中间识别更好，却让下游行为不变或更糟。

这比“小模型不会”更能生存。现有工作里，跨尺寸差异常来自新路径出现而非统一能力增加；[How Context Shapes Truth](https://arxiv.org/abs/2601.06599) 甚至观察到不同规模用不同几何量区分上下文。我们的来源谱系候选也显示“识别共同来源随规模提高、加权却不提高”的可能模式。

候选卡必须预先写出为何 A 和 B 接受不同训练信号，例如：

- 知识增长强化现实性表征，却不要求输出始终服从该表征；
- 指令理解强化目标 reader，却不保证 action writer 维护事务语义；
- 代码训练强化值相等判断，却未必强化对象身份/别名追踪；
- 长上下文检索强化定位，却未必强化证据角色绑定。

### P7. 老问题给出概念分解，公开数据给出自然刺激

[Mechanistic Interpretability of Emotion Inference](https://aclanthology.org/2025.findings-acl.679/) 用成熟 appraisal 理论组织表示；[Reasoning Circuits in Language Models](https://aclanthology.org/2025.findings-acl.525/) 用古典三段论提供可证明结构；[Meaning Beyond Truth Conditions](https://aclanthology.org/2025.acl-long.432/) 用 anaphora accessibility 检查话语层意义；ACL 2026 的 [Experiments or Outcomes?](https://arxiv.org/abs/2604.18786) 把科学“实验可做”与“结果可得”拆开。

正确借法：老问题只提供 `A ≠ B` 与天然极端反例，不预设模型一定复现某个人类 bias。

### P8. 机制不是论文尾部装饰，而应推出新预测或选择性修复

[Llama See, Llama Do](https://aclanthology.org/2025.acl-long.791/) 从 contextual entrainment 走到 head-level 消融；[Back Attention](https://aclanthology.org/2025.emnlp-main.567/) 从瓶颈定位导出方法；[Output-Centric Feature Descriptions](https://aclanthology.org/2025.acl-long.288/) 强调 feature 描述必须用输出因果作用审计。

所以每张卡要在实验前写机制分叉：

```text
若内容未形成 → 训练/表示方法
若内容形成但路由失败 → routing/patch 方法
若 late binding 错 → binding-aware readout
若 gate 选择错路径 → selective gate
若历史未 canonicalize → state compaction/rollback normalization
```

## 二、已经拥挤或基本占领的宽叙事

下表不是说这些领域不能做，而是说不能只重复宽结论。

| 宽母现象 | 占位例子 | 仅重复什么会撞车 | 必须额外出现什么才保留 |
|---|---|---|---|
| 证据位置影响长上下文 | Lost in the Middle 及大量后续 | 再画一次位置曲线 | 新错误落点、路径/角色交互、迟滞或新机制 |
| 前提顺序影响推理 | Premise Order Matters；ACL 2026 *Lost in the Prompt Order* | 等价 permutation 掉点 | proof execution 之外的新结构、跨阶段机制 |
| 无关上下文使答案变差 | Stochastic Chameleons；RAG distractor 工作 | generic distractor drop | 错误落点、局部能力解离或选择性 gate |
| context 与参数知识冲突 | Astute RAG、FaithfulRAG、context-faithfulness 大量工作 | context/parametric 二选一 | world/source/identity/path 的独特 factorial 或内部路由失配 |
| 证据重复/来源偏好 | Whose Facts Win、GroupQA、CAMA | 多份重复证据更有说服力 | 识别—使用解离、反常 scaling、可因果路由修复 |
| 普通 ToM / false belief 准确率 | ToMi/FANToM/BigToM 大量工作；Lookbacks | 再测一阶/二阶 false belief | belief 与行动/承诺/共同知识的特定解离，且避开已做 binding mechanism |
| 现实/虚构表征 | fact/fiction/forecast 与 Hamdi ontology 线 | famous real vs fictional probe | 不同概念轴，如 scope exit、事件 actuality、引用承诺；必须与现实性表示正交 |
| solve–verify / self-correction | Validation Gap、Confidence v.s. Critique、自纠错文献 | 会做但不会检查 | 一个新对象和决定性转移方向，最好可主动构造反例却不用 |
| 逻辑有效性受可信内容污染 | belief bias / plausibility 表征论文 | 可信内容让 invalid 看起来 valid | 新的 computation dissociation 或自然应用，不只是另一三段论模板 |
| 泛化的量词/三段论 fallacy | NAACL/EMNLP 系统三段论研究 | 某个 invalid syllogism 错 | rule-induced switch、counterexample-use gap 等独特 signature，且机制超出现有电路 |
| 泛型被当作全称 | *Exceptions, Instantiations, and Overgeneralization*；Generics and Default Reasoning | “鸟会飞”过度推广 | 与身份、异常实例更新或行动阈值的独特解离 |
| 事件 factuality / mental simulation 混淆 | MAVEN-Fact、FactBank、CogNarr | planned/imagined 被判 actual | 初始状态可识别、下游复述才丢失的 reuse signature |
| option/label/order bias | MCQA 大量工作 | 换选项顺序掉点 | 与内部知识、验证或尺度的决定性交互 |
| 工具 schema/结构偏差 | BFCL；Tool Irrelevance | 工具名或 schema 顺序影响调用 | 后果预测—执行 veto、事务/回滚、重试身份等更深语义 |
| agent 目标切换困难 | AgentChangeBench | 新目标后仍慢 | 已承认新目标却继续旧行动、已取消目标复活、机制化承诺状态 |
| confidence/abstention 不校准 | 大量 UQ 与 abstention 工作 | 置信和正确率不一致 | 置信可读却不控制行动、证据补足后的迟滞、跨任务 writer gap |
| 多语言知识差距/英文中介 | Paths Not Taken 及跨语知识工作 | 某语言准确率低 | 同一证据跨语言被误算成独立来源、翻译后状态更新不传播等新关系 |
| “attention/probe 表示了 X” | 大量 probing 工作 | probe accuracy 高 | 必要性、充分性、路径因果与选择性 rescue |

## 三、候选晋级的会议尺度检查

### ACL / EMNLP / NAACL Main 对齐

一张卡最终要能长成：

```text
一句话自然 phenotype
→ 至少 3/5 家族和一个三尺寸序列
→ 一个不能被 generic failure 替代的 signature
→ 两个外部设置或一个自然主数据 + 一个原则性 sandbox
→ representation / routing / readout 的因果裁决
→ 机制导出的选择性修复或新预测
```

不要求一开始就有所有证据；要求候选**有清楚路径长成这套证据**。

### Findings 下界

若候选只能做到下列之一，最多按 Findings 预期：

- 经典问题的大规模行为复现；
- 跨家族/尺寸的表示与 steering，但无完整 computation；
- 一个窄任务上的必要/充分电路；
- 新 benchmark 真正解耦旧任务混在一起的变量。

只有“小数据集上一个 drop + probe”低于本项目要求。

## 四、给候选发现者的检索协议

Paper Notes 用于发现术语和邻近论文；正式审计至少做四轮：

1. `exact task + exact manipulation`；
2. `plain-language anomaly + LLM`；
3. `old philosophical/cognitive term + language model`；
4. `candidate mechanism vocabulary + task`。

逐篇比较：

| 字段 | 最近工作 | 本卡 |
|---|---|---|
| mother question |  |  |
| natural source |  |  |
| decisive contrast |  |  |
| error destination / shape |  |  |
| cross-family / scaling law |  |  |
| internal variables |  |  |
| causal intervention |  |  |
| mechanism-derived method |  |  |

只要最近工作已经覆盖同一 decisive contrast、结构 signature 和主要机制问题，卡片标 `OCCUPIED`，不进入模型验证。
