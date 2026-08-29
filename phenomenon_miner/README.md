# Phenomenon Miner

`phenomenon_miner/` 是本仓库的**选题发现、novelty 审计、D0 构造与实验调度中枢**。它是内部研究流程，不是准备投稿的“测试框架贡献”。最终论文对象应是一个自然 scientific question / phenotype、其机制与由机制导出的改进方法。

## 权威文档

| 文件 | 作用 |
|---|---|
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | 选题与晋级硬门槛 |
| [`PROCESS.md`](PROCESS.md) | N0 → D0 → smoke → N1 → panel → mechanism 的唯一合法流程 |
| [`NOVELTY_GATE.md`](NOVELTY_GATE.md) | exact collision、mother inclusion、successor、independent N0/N1 |
| [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md) | **唯一模型调用授权表** |
| [`MODEL_PANEL.md`](MODEL_PANEL.md) | 跨家族 / 跨尺寸 panel |
| [`CONFERENCE_SCALE_AUDIT.md`](CONFERENCE_SCALE_AUDIT.md) | ACL/EMNLP/NAACL 题目尺度校准 |
| [`FAILURE_REVIEW_2026-08-28.md`](FAILURE_REVIEW_2026-08-28.md) | validation 后撞车 / 失败的流程复盘 |

仓库级当前 dashboard：[`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)。

## 当前 discovery lanes

### Batch 3 — 当前优先线：mother-paper extensions

- [`candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md)：10 个 `MOTHER-PAPER-GROUNDED / REVIEWER-MODE-N0-SURVIVOR`；
- [`candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md`](candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md)：>30 条 mother/neighbor line 的 sweep、extension 脑暴与 death ledger。

这批从强 mother paper 已经建立的 scientific object 出发，寻找真正未解决的 scope boundary、missing axis、causal role、mechanism semantics 或 implementation switch。**SURVIVOR 不是 formal N0-PASS，也不授权 smoke。**

### Batch 2 — 次级候选线

- 当前 10 题：[`candidate_pool/BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](candidate_pool/BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md)
- 完整 brainstorm / kill ledger：[`candidate_pool/BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](candidate_pool/BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)
- reviewer working audit：[`candidate_pool/audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](candidate_pool/audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)

旧的 `BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md` 是历史快照，已被 V2 取代。

### Batch 1 — 历史 deep-N0 shortlist

- [`candidate_pool/DEEP_N0_SURVIVORS_10_2026-08-28.md`](candidate_pool/DEEP_N0_SURVIVORS_10_2026-08-28.md)
- [`candidate_pool/audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](candidate_pool/audits/ADVERSARIAL_N0_TEN_2026-08-28.md)

其中部分题已经进入 active / archive，因此旧 shortlist 只用于 provenance，当前状态必须查 registry。

## candidate_pool 应该怎么读

```text
candidate_pool/README.md     当前批次导航
candidate_pool/AUDIT_REGISTRY.md  正式调度权
candidate_pool/BATCH*.md     某轮 shortlist / ledger
candidate_pool/01_...12_...  12 个领域的长期 idea inventory + death backfill
candidate_pool/audits/       N0 工作稿与独立/对抗审计
```

领域文档和 Batch shortlist 都是**研究库存**，不是实验队列。

## 状态词不要混用

- `SURVIVOR`：某轮 proposer/reviewer 搜索暂未杀掉；
- `N0-PASS`：formal novelty / mother-inclusion gate 通过；
- `D0-PASS`：自然数据合同通过；
- `READY-TO-SMOKE`：N0+D0+config 均满足，且 registry 授权；
- `HOLD`：问题可能还值得做，但 blocker 未解除；
- `HARD-KILL / TERMINAL-KILLED`：当前 project/contract 已结束，进入 archive。

一个项目只有 `validation_authorized: true` 才能调用模型。

## 目录角色

```text
phenomenon_miner/
├── REQUIREMENTS.md
├── PROCESS.md
├── NOVELTY_GATE.md
├── MODEL_PANEL.md
├── CONFERENCE_SCALE_AUDIT.md
├── candidate_pool/     # discovery inventory + N0 + authoritative registry
├── phenomena/          # 规范化现象档案（逐步迁移）
├── candidates/         # legacy 长文候选
├── promoted/           # legacy 命名；不自动表示当前可投稿
├── data/ results/ logs/# 历史扫描/验证资产
└── run_*.py            # 历史/当前扫描脚本
```

不为了“目录漂亮”批量移动历史脚本、结果和 raw data，因为这会破坏复现路径。整理的原则是：**当前入口单一化，历史 provenance 原地保留。**