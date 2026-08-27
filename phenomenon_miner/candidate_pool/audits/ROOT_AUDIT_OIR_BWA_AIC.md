# OIR / BWA / AIC novelty-first 淘汰审计

日期：2026-08-28。范围 36 张卡。只有 exact signature 尚未被覆盖、有自然客观 gold、结构性错误终点、且行为一旦成立即可进入因果机制工作的候选，才标 `ADVANCE`。

## OIR（12 → 0 个独立候选）

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| OIR-01 | KILL | indefinite identity 的经典语义问题；自然句本身有语用偏好 |
| OIR-02 | KILL | 两次不定引入/共指已有成熟语义与 coreference 母任务 |
| OIR-03 | KILL | 同名跨文档融合就是 entity resolution / disambiguation 核心错误 |
| OIR-04 | KILL | 角色继任与人物同一是 temporal KB / entity tracking 核心能力 |
| OIR-05 | KILL | equality/identity 基础题，没有新错误形状 |
| OIR-06 | MERGE | whole→part 答案迁移是 EIRD 的结构目的地 |
| OIR-07 | KILL | collective/distributive distinction 是成熟形式语义轴 |
| OIR-08 | KILL | 两个描述是否共指直接落在 coreference / entity linking |
| OIR-09 | OCCUPIED | deleted/rollback ghost 已被 semantic rollback 与 cache rollback 正面占位 |
| OIR-10 | MERGE | type↔instance 答案位交换是 EIRD 的错误目的地 |
| OIR-11 | OCCUPIED | relation reversal / subject–object order 已有直接行为和机制工作 |
| OIR-12 | KILL | mention→existence 与 Hamdi 的实体存在性母问题过近 |

[Slot Machines](https://arxiv.org/abs/2604.21139) 已直接研究 current/prior entity slots、关系绑定，以及信息可解码却未被 factual retrieval 使用。当前独立卡没有超出普通 entity binding。

## BWA（12 → 1 个 ADVANCE）

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| BWA-01 | **ADVANCE** | quote speaker 可正确恢复，但 downstream 是否把引语升级成作者承诺，exact dissociation 尚未找到 |
| BWA-02 | OCCUPIED | hypothetical scope / counterfactual leakage 已有系统 benchmark |
| BWA-03 | OCCUPIED | counterfactual backwash 与 unring / imagined-event actuality 重合 |
| BWA-04 | OCCUPIED | mental-event content→world actuality 是现有 event-actuality 线及 Hamdi 邻域 |
| BWA-05 | OCCUPIED | belief report→action prediction 是 ToM benchmark 核心设置 |
| BWA-06 | KILL | wish/prediction/fact 是一般 event factuality/modality 分类 |
| BWA-07 | KILL | 概率词到行动的规范依赖任务损失，客观 gold 不稳定 |
| BWA-08 | OCCUPIED | 否认命题仍被利用属于 negation/factuality/false-premise 密集区 |
| BWA-09 | OCCUPIED | canceled presupposition 已被 NOPE 与 unring 类工作覆盖 |
| BWA-10 | KILL | 无特殊错误终点时只是 scope contamination |
| BWA-11 | HOLD | unknown→certain memory 易退化成普通 hallucination |
| BWA-12 | OCCUPIED | hearsay/source reliability 已被来源偏好与 persuasion 文献占位 |

### 来源归因—作者承诺解离

> 模型能准确说出一句话是谁说的，也能说文章正在反驳它；到摘要、事实抽取或裁决时，却把这句话写成作者承诺的事实。

晋级要求 attribution/refutation probe 正确，错误只发生在 `quoted/refuted proposition → author commitment → downstream use`。FactBank 已标注 author 与 nested source 的 factuality holder；[Towards Generative Event Factuality Prediction](https://aclanthology.org/2023.findings-acl.44/) 明确以 holder、target、factuality 为任务。可接 QuoteBank/DirectQuote speaker span 与人工 fact-check verdict。

现有工作分别研究引语归因（如 [AttriBench](https://arxiv.org/abs/2604.05224)）、嵌套来源 factuality、摘要 factual consistency 与 source framing；本轮未找到把 `reader 正确 → author commitment 错 → quoted/refuted payload 稳定复活 → source-scope routing 因果机制` 放在同一 item 的工作。

竞争机制：`carrier loss`（传播 proposition 时丢失 speaker/sign）与 `commitment override`（speaker/sign 可读，但 content path 覆盖 gate）。若 reader 错误与 downstream 错误重合，或错误不特别落在被引 payload，立即 KILL。

## AIC（12 → 0 个候选）

| 卡 | 裁决 | 决定性理由 |
|---|---|---|
| AIC-01 | KILL | promise/intention→completion 是基本 event factuality |
| AIC-02 | KILL | intention/expectation 混线与 modality/ToM 重合 |
| AIC-03 | OCCUPIED | EMNLP 2025 agent early-exit 已报告完成后继续探索与冗余步骤 |
| AIC-04 | OCCUPIED | AgentChangeBench、AdaPlanBench 与 evolving-intent 直接测 goal shift |
| AIC-05 | OCCUPIED | ACL/EACL 2026 access control 与 SafeMCP 已覆盖权限/撤销 |
| AIC-06 | KILL | generic planner/selector gap |
| AIC-07 | KILL | permission→obligation 是经典 deontic logic 错误 |
| AIC-08 | KILL | can→should 是成熟 deontic / moral reasoning 区域 |
| AIC-09 | KILL | delegation→personal execution 需要人为场景规范 |
| AIC-10 | KILL | 与一般 condition following 重合 |
| AIC-11 | OCCUPIED | PRESTO、Repair-QA、BlockWorld-Repairs 已系统研究修正 |
| AIC-12 | OCCUPIED | interruption 与 evolving user intent / task repair 已有 benchmark |

代表性占位：[PRESTO](https://aclanthology.org/2023.emnlp-main.667/)、[Repair-QA](https://aclanthology.org/2023.sigdial-1.52/)、[BlockWorld-Repairs](https://aclanthology.org/2024.emnlp-main.643/)、[SafeMCP](https://aclanthology.org/2026.acl-long.522.pdf)、[AdaPlanBench](https://arxiv.org/abs/2606.05622)。
