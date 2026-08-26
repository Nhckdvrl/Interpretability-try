# Research failure postmortems

这个文件记录已经实际消耗研究与算力预算的失败。目的不是替失败叙事找补，而是把导致浪费的决策变成以后不可绕过的流程约束。

## 006 — Bayesian latent inference → downstream use gap

**结论：** 当前题目不成立。项目暂停，custom mechanism 路线终止。

### 我们实际拥有什么

- 在自构造闭式 Bayesian prompt 上，Qwen2.5-14B 能较好报告 posterior，但直接动作错误较多；显式提供 posterior 后动作被 rescue。
- 在同一自构造框架上，Gemma3-12B 基本能直接做对，Qwen3-8B 的报告与动作都不稳定。
- Qwen2.5 的显式-belief bridge 内，替换完整数字 span 可以转移动作。

这些只说明一个 checkpoint 在一个人工接口上的条件性现象，以及该 bridge prompt 内部对显式数字的处理。它们没有证明自然的 belief/use dissociation，也没有证明 direct prompt 中存在“知道但没有使用”的 posterior。

### 核心失败

1. **把 custom task 当成了现象证据。** 数据、规则、report 接口、action 接口和 bridge 都由我们定义，缺少官方任务或独立数据锚点。
2. **在跨模型复现之前做了机制。** Qwen2.5 单点结果被过早称为 anchor phenotype，并触发 probe 和 activation interchange。
3. **把复现失败重写成一般性。** Gemma、Qwen3 表现不同，本应首先判定目标 phenotype 未跨模型成立；我们却尝试把它升级为“report/use 能力普遍解耦”的 quadrant 叙事。
4. **低估了接口 artifact。** 后续 meta-G0 出现单标签坍缩和低 mapping consistency，说明自定义 label、排列和 prompt comprehension 足以生成看似有意义的差异。
5. **发现 narrative collision 后仍继续。** BayesBench 已经明确提出 latent inference 的提升不稳定地转化为 downstream prediction。我们虽在计划中引用了它，却没有在昂贵实验前把宽叙事判为 collision。
6. **机制结果被错误地赋予外延。** 显式数字 span 的因果效应只属于 bridge computation，不能解释原始 direct failure，更不能弥补行为现象缺乏外部有效性。

### 正确的停止时点

最迟在第一轮三模型 G0 完成时就应暂停：同一 operationalization 没有产生同一 failure。此时正确动作应是立即迁移到官方 benchmark，而不是继续扩大人工 factorial、缓存 activation、训练 probe 和扫描 layer。

### 以后必须执行的反事实流程

```text
先定位官方 / 独立数据上的已知 failure
→ 用原始 evaluation 复现
→ 至少两个模型家族复现同一预注册 phenotype
→ 做 prompt、label、tokenization 和 task-comprehension audit
→ 完成 nearest-paper narrative collision audit
→ 冻结 stop-loss 与机制预算
→ 才允许第一轮白盒实验
```

任何一步失败，停止。自构造数据可以在此后用于机制对照，但不能替代此前任何一步。

### 006 的唯一复活条件

只有同时满足以下条件才允许重开：

1. 使用未经我们重写的 BayesBench 官方 evaluation；
2. 在至少两个公共数据环境复现目标 inference/use gap；
3. 在至少两个模型家族或有说服力的跨尺寸序列上出现同一预注册 phenotype；
4. 新贡献明确限定为已有现象的因果机制与选择性修复，并证明机制跨官方任务迁移。

否则直接归档。不得再通过改 prompt、挑 checkpoint、挑 subset 或放宽现象定义救题。
