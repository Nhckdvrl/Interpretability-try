# Phenomenon Miner

这是本仓库的**现象发现与选题档案库**。它既保存寻找现象的要求和过程，也保存成功、待定与失败的候选。

`phenomenon_miner` 是内部矿镐，不是准备投稿的 “metamorphic testing framework”。最终论文的对象应当是从这里发现的自然 phenotype、它的机制以及由机制导出的方法。

## 从这里开始

- [`REQUIREMENTS.md`](REQUIREMENTS.md)：已经冻结的现象筛选要求与晋级门槛。
- [`PROCESS.md`](PROCESS.md)：唯一合法的分阶段流程；N0/D0 在任何模型调用之前。
- [`NOVELTY_GATE.md`](NOVELTY_GATE.md)：全文级 collision、母现象包含、独立复核与 N1 协议。
- [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md)：唯一有调度权的候选状态表。
- [`FAILURE_REVIEW_2026-08-28.md`](FAILURE_REVIEW_2026-08-28.md)：验证后才撞车的流程复盘。
- [`MODEL_PANEL.md`](MODEL_PANEL.md)：Qwen、Gemma、Phi、Llama、Mistral 五家族验证面板与 checkpoint 来源。
- [`CONFERENCE_SCALE_AUDIT.md`](CONFERENCE_SCALE_AUDIT.md)：ACL/EMNLP/NAACL 可解释性现象的主会与 Findings 尺度校准。
- [`candidate_pool/`](candidate_pool/)：按 12 个领域保存的历史假设库存，不是实验队列；旧 Tier 不再授权分发。
- [`phenomena/`](phenomena/)：统一的现象档案；每个现象分别记录行为、证据、边界、撞车和下一状态。
- [`../PHENOMENON_MINING_GUIDE.md`](../PHENOMENON_MINING_GUIDE.md)：完整搜索指南、领域、relation 与 anomaly signature。
- [`../DATASET_CATALOG.md`](../DATASET_CATALOG.md)：领域到公开数据集的索引。
- [`../FAILURE_POSTMORTEMS.md`](../FAILURE_POSTMORTEMS.md)：已经实际消耗研究预算的失败复盘。

## 状态必须分开记录

任何候选不得只写一个含糊的 `promising` 或 `promoted`。至少分别记录：

| 维度 | 可用状态 |
|---|---|
| 行为证据 | `UNTESTED / PILOT / VERIFIED / FAILED` |
| 一般性 | `ONE_MODEL / CROSS_SIZE / CROSS_FAMILY / BROAD` |
| 新颖性 | `UNAUDITED / OPEN / NARROWED / COLLISION` |
| 可解释性 | `UNCLEAR / HYPOTHESES / FEASIBLE / DEMONSTRATED` |
| 总体决策 | `MINE / HOLD / ADVANCE / REJECT / ARCHIVE` |

因此，“行为真实”不等于“现象全新”；“有机制空间”也不能弥补行为不自然或跨模型失败。

## 当前目录约定

```text
phenomenon_miner/
├── REQUIREMENTS.md         # 冻结的选择标准
├── PROCESS.md              # 发现、验证、审计和止损过程
├── MODEL_PANEL.md          # 五家族与跨尺寸验证面板
├── CONFERENCE_SCALE_AUDIT.md # 会议题目尺度审计
├── candidate_pool/         # 未验证候选、总排序、去重与分发合同
├── phenomena/              # 规范化现象档案
├── candidates/             # 历史候选长文，逐步迁移
├── promoted/               # 历史命名；不再自动表示可投稿
├── data/                   # 本地数据与缓存
├── results/                # 原始输出与汇总
├── logs/                   # 运行日志
└── run_*.py                # 当前扫描与验证脚本
```

在要求冻结前，不批量移动历史脚本和结果，以免破坏复现路径。新想法先写入 `candidate_pool/`；只有获得行为证据后才进入 `phenomena/` 建档。
