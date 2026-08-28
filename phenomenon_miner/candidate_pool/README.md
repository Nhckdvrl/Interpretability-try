# 现象候选池

版本：2026-08-28
状态：`162 CARDS / 12 DOMAINS — LITERATURE-GROUNDED IDEATION — 未经行为验证`

这里保存的是**待审计的研究假设库存**，不是已经成立的现象，也不是可直接 smoke 的队列。任何候选先看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)；只有其中明确写为 `READY-TO-SMOKE` 且 `validation_authorized: true` 才能调用模型。

本目录与其他目录的分工：

```text
candidate_pool/   研究前的候选假设、数据锚点、碰撞边界与证伪路线
phenomena/        已经获得行为证据的规范化档案
candidates/       历史长备忘
promoted/         历史命名；不自动代表当前可投稿
results/          原始模型输出
```

## 2026-08-28 找题批次入口

### 第一批深度 N0 shortlist

- [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md)：第一批十题 reviewer/adversarial shortlist；
- [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)：逐题最强邻居、`why_not_a_rename` 与 hard kill。

### 第二批新十题（当前 V2）

- [`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)：前半轮大规模脑暴、死亡库与早期 survivor；历史过程账本；
- [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)：早期 proposer-side 攻击稿；
- [`BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md`](BATCH2_INDEPENDENT_N0_LEDGER_2026-08-28.md)：继续脑暴、reviewer-mode N0、淘汰/Reserve 与补题总账本；
- [`audits/BATCH2_THIRD_PASS_ATTACK_2026-08-28.md`](audits/BATCH2_THIRD_PASS_ATTACK_2026-08-28.md)：strongest-neighbor / mother-inclusion 第三刀；
- [`audits/BATCH2_FOURTH_PASS_ITEM_LEVEL_2026-08-28.md`](audits/BATCH2_FOURTH_PASS_ITEM_LEVEL_2026-08-28.md)：公开 repo/data item-level 与 operator-identifiability 第四刀；RIF 在此正式 KILL；
- [`BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md)：**第二批当前 10 个** `REVIEWER-MODE-N0-SURVIVOR`；
- [`BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md)：第三刀历史快照，已被 V2 取代为当前 shortlist，不删除以保留审计时间线。

两个批次里的 `SURVIVOR` 都**不等于 formal `N0-PASS`**，更不授权 smoke。真正调度权仍只来自 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。任何独立 reviewer 发现 exact collision / mother inclusion / D0 failure 后都应直接 KILL/ROUTE，不为维持“十题”数量降低门槛。

## 为什么新增这一层

现有 [`PHENOMENON_MINING_GUIDE.md`](../../PHENOMENON_MINING_GUIDE.md) 和
[`DATASET_CATALOG.md`](../../DATASET_CATALOG.md) 已经覆盖大量 relation、axis 与数据集，
但其中不少条目仍是“在数据集 X 上做变换 Y”。本目录把它们提升为研究问题：

```text
一个基本而自然的人类问题
→ 一句话反直觉矛盾
→ 模型可能混合或分离的两个计算
→ 原生公开数据中的发现机会
→ 最近论文已经占领什么
→ 哪一种结构结果才值得继续
```

## 领域划分

领域不是按 benchmark 或变换类型划分，而是按可能被模型错误分解的基本计算划分：

| 文档 | 母问题 | 状态 |
|---|---|---|
| [`01_ONTOLOGY_IDENTITY_REFERENCE.md`](01_ONTOLOGY_IDENTITY_REFERENCE.md) | 类型、个体、同一性、指称、部分与整体 | 12卡，已初筛 |
| [`02_BELIEF_WORLDS_ATTITUDES.md`](02_BELIEF_WORLDS_ATTITUDES.md) | 知道、相信、假设、想象、引用、现实性 | 12卡，已初筛 |
| [`03_AGENCY_INTENTION_COMMITMENT.md`](03_AGENCY_INTENTION_COMMITMENT.md) | 想做、承诺、获准、能做与实际行动 | 12卡，已初筛 |
| [`04_MEMORY_TIME_REVISION.md`](04_MEMORY_TIME_REVISION.md) | 当前状态、历史路径、撤回、时间与事件 | 14卡，已初筛 |
| [`05_DISCOURSE_PRAGMATICS_COMMUNICATION.md`](05_DISCOURSE_PRAGMATICS_COMMUNICATION.md) | 字面内容、言语行为、共同语境与话语焦点 | 14卡，已初筛 |
| [`06_SOCIAL_EVIDENCE_COLLECTIVE.md`](06_SOCIAL_EVIDENCE_COLLECTIVE.md) | 证言、共识、来源、群体知识与规范 | 12卡，已初筛 |
| [`07_KNOWLEDGE_RAG_EVIDENCE.md`](07_KNOWLEDGE_RAG_EVIDENCE.md) | 检索到、相信、整合、引用和输出答案 | 14卡，已初筛 |
| [`08_REASONING_VERIFICATION_COMPOSITION.md`](08_REASONING_VERIFICATION_COMPOSITION.md) | 求解、验证、反例、局部步骤与全局结论 | 14卡，已初筛 |
| [`09_AGENTS_TOOLS_WORKFLOWS.md`](09_AGENTS_TOOLS_WORKFLOWS.md) | 计划、工具语义、执行结果、回滚与重试 | 15卡，已初筛 |
| [`10_CODE_STRUCTURED_STATE.md`](10_CODE_STRUCTURED_STATE.md) | 程序语义、对象别名、状态变化与结构化接口 | 15卡，已初筛 |
| [`11_UNCERTAINTY_DECISION_HIGH_STAKES.md`](11_UNCERTAINTY_DECISION_HIGH_STAKES.md) | 不确定性、拒答、证据更新和行动阈值 | 14卡，已初筛 |
| [`12_MULTILINGUAL_CROSS_CULTURAL.md`](12_MULTILINGUAL_CROSS_CULTURAL.md) | 同一命题跨语言后的身份、来源和推理路径 | 14卡，已初筛 |

[`00_MASTER_INDEX.md`](00_MASTER_INDEX.md) 仅保留历史 ideation 与去重信息，不再作为分派排序。当前裁决与唯一调度入口见 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。顶会选题母结构与已占领叙事见 [`LITERATURE_PATTERNS.md`](LITERATURE_PATTERNS.md)。
给便宜 agent 的可复制单卡任务见 [`SMALL_AGENT_HANDOFF.md`](SMALL_AGENT_HANDOFF.md)。

## 候选不是“预言”

每张候选卡必须区分：

- `hypothesis`：可能出现什么异常；
- `promotion signature`：只有观察到什么结构才值得研究；
- `kill condition`：什么结果立即终止；
- `collision risk`：哪篇最近工作可能已经占位。

候选池允许大量失败，但不允许把未经测试的方向写成事实。

## 卡片最低规格

每张候选卡至少包含：

1. 普通人一句话矛盾；
2. 不含数据集名的自然例子；
3. 为什么不是普通低准确率；
4. 首选公开数据与至少一个外部分布；
5. 原生轴或最小、规范有效的 relation；
6. 只有什么结构结果才晋级；
7. 为什么更大模型未必自然消失；
8. 至少两个有不同因果预测的机制；
9. 最近母现象、exact collision 风险与可能独特性质；
10. 最便宜的证伪实验和停止条件。

统一模板见 [`CARD_SCHEMA.md`](CARD_SCHEMA.md)。

## 分派纪律

小 agent 每次只领取**一张卡**，先做 relation/data/literature 审计，再决定是否调用模型。不得把一个领域文档里的候选一次性全跑。

```text
文献 exact collision
→ 数据是否真实可得
→ 抽样读 20 个原始案例
→ 冻结 scorer 与 kill condition
→ 30–50 个样本 × 两家族 smoke
```

任何卡被证伪后，在原卡追加日期、证据和 `KILL/HOLD`，不删除；这样候选池同时也是去重和止损记忆。
