# Phenomenon Miner

`phenomenon_miner/` 是本仓库的**选题发现、novelty 审计、D0 构造与实验调度中枢**。它是内部研究流程，不是准备投稿的“测试框架贡献”。

## 权威文档

| file | role |
|---|---|
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | 选题与晋级硬门槛 |
| [`PROCESS.md`](PROCESS.md) | N0 → D0 → smoke → N1 → panel → mechanism |
| [`NOVELTY_GATE.md`](NOVELTY_GATE.md) | exact collision、mother inclusion、successor、independent N0/N1 |
| [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md) | **唯一模型调用授权表** |
| [`MODEL_PANEL.md`](MODEL_PANEL.md) | 跨家族 / 跨尺寸 panel |
| [`CONFERENCE_SCALE_AUDIT.md`](CONFERENCE_SCALE_AUDIT.md) | 主会题目尺度校准 |
| [`FAILURE_REVIEW_2026-08-28.md`](FAILURE_REVIEW_2026-08-28.md) | validation 后失败的流程复盘 |

Batch 1 / 2 / 3、brainstorm ledger、领域 idea inventory 与 N0 工作稿统一从 [`candidate_pool/README.md`](candidate_pool/README.md) 进入；这里不再重复列一遍。

```text
candidate_pool/   discovery inventory + N0 workspace + authoritative registry
phenomena/        规范化现象档案（逐步迁移）
candidates/       legacy 长文候选
promoted/         legacy 命名；不自动代表可投稿
data/results/logs 历史扫描与验证资产
run_*.py          历史/当前扫描脚本
```

整理原则：**当前入口单一化，实验与历史 provenance 不为目录美观而批量移动。**