# Interpretability Topic Search

这个仓库用于寻找和验证 **LLM 可解释性研究题目**。核心原则是：先确认一个自然、可复现、值得解释的行为对象，再进入机制与方法；不是先选 SAE / attention head / activation patching 再找故事。

> 目标尺度：ACL / EMNLP / NAACL Main 级别的 mother question + decisive contrasts + mechanism fork + natural method opening。

## 当前状态

| lane | project | status | model calls |
|---|---|---|---|
| behavioral validation | [`active/007_weak_evidence_backfire/`](active/007_weak_evidence_backfire/) | `N0-PASS / D0-PASS / READY-TO-SMOKE`，当前为 30-case natural D0 contract | **authorized** |
| blocked | [`active/013_publicness_coordination_dissociation/`](active/013_publicness_coordination_dissociation/) | `N0-PASS / HOLD-D0` | no |
| pre-candidate | [`active/003_diagnostic_counterevidence_revision/`](active/003_diagnostic_counterevidence_revision/) | `PAPER-AUDIT-PASSED / G0-NOT-RUN` | no |
| discovery | [`phenomenon_miner/candidate_pool/`](phenomenon_miner/candidate_pool/) | Batch 3 mother-paper extensions 为当前优先线；survivor 不是 formal N0 | no |
| terminal history | [`archive/`](archive/) | 已停止项目与完整证据链 | no |

**唯一模型调用授权源是 [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md)。** `active/`、`SURVIVE`、`promising` 或旧 result verdict 都不能自行授权。

007 的旧 two-family smoke 使用的是更早的 25-case D0；当前项目已经切换到实质修订后的 30-case contract。两者的 lineage 只在 [`active/007_weak_evidence_backfire/README.md`](active/007_weak_evidence_backfire/README.md) 维护，不在其他入口重复抄写。

## 权威入口

1. [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md) — 当前授权与 canonical mapping。
2. [`phenomenon_miner/PROCESS.md`](phenomenon_miner/PROCESS.md) — N0 → D0 → smoke → N1 → panel → mechanism。
3. [`phenomenon_miner/REQUIREMENTS.md`](phenomenon_miner/REQUIREMENTS.md) — 选题和晋级硬门槛。
4. [`phenomenon_miner/NOVELTY_GATE.md`](phenomenon_miner/NOVELTY_GATE.md) — collision / mother inclusion / successor / N1。
5. [`phenomenon_miner/candidate_pool/README.md`](phenomenon_miner/candidate_pool/README.md) — Batch 1 / 2 / 3 与长期 idea inventory。
6. [`archive/README.md`](archive/README.md) — terminal project 索引。

长版搜索方法见 [`PHENOMENON_MINING_GUIDE.md`](PHENOMENON_MINING_GUIDE.md)，公开数据集见 [`DATASET_CATALOG.md`](DATASET_CATALOG.md)，真实失败复盘见 [`FAILURE_POSTMORTEMS.md`](FAILURE_POSTMORTEMS.md)。

## 目录角色

```text
active/              当前仍可能继续的具体项目；不等于授权
archive/             已终止项目；保留最终证据与复现材料
phenomenon_miner/    选题、N0/D0、candidate pool 与正式调度
preflight/           历史共享 preflight 工具/环境记录
rejected_candidates/ 早期 rejected idea / postmortem 档案
```

## 不变规则

- N0 / D0 在模型调用之前；formal authorization 只看 registry。
- Behavior first；行为 prerequisite 没过，不靠 hidden-state evidence 救题。
- custom-only 不能承担 paper-level naturalness / generality。
- 失败后不换弱模型、subset、readout、阈值或名字续命。
- 若 contract 被独立审计实质修订，旧结果与新 contract 必须按 D0 SHA / version 分开。

历史文本、被 supersede 的 snapshot 和 pre-merge audit 不再为了“看得见”复制到当前树；需要时直接查 Git history。