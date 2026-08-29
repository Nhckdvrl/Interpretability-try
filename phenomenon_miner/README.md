# Phenomenon Miner

`phenomenon_miner/` 是本仓库的 **discovery 与 dispatch 中枢**。

## 权威文档

| file | role |
|---|---|
| [`PROCESS.md`](PROCESS.md) | discovery → registration → D0 freeze → behavior → mechanism |
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | 题目、novelty、data feasibility 与一般性硬门槛 |
| [`NOVELTY_GATE.md`](NOVELTY_GATE.md) | registration 前的 N0 breadth + N1 depth |
| [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md) | **唯一模型调用授权表** |
| [`MODEL_PANEL.md`](MODEL_PANEL.md) | 跨家族 / 跨尺寸 panel |

Batch、brainstorm ledger、领域 idea inventory 与 discovery audits 统一从 [`candidate_pool/README.md`](candidate_pool/README.md) 进入。

## 新的目录语义

```text
candidate_pool/  还在“把题目做透”的地方：N0 + N1 + D0 source feasibility
active/          已正式注册的项目；不再用于继续找论文/找数据
archive/         terminal projects
```

新题只有拿到 `DISCOVERY-PASS` 才能从 candidate pool 进入正式 project registration。

如果在 active 里才发现“数据不够、license 不清、需要换 source、最强邻居没读 appendix”，说明 discovery 没做完；新流程要求退回 discovery，而不是继续打补丁。
