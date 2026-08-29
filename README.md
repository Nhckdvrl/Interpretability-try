# Interpretability Topic Search

这个仓库用于寻找和验证 **LLM 可解释性研究题目**。核心原则是：先把题目本身查透、数据路径做实，再投入模型预算；不是先建 active 项目以后再慢慢补 novelty、找数据或找机制故事。

> 目标尺度：ACL / EMNLP / NAACL Main 级别的 mother question + decisive contrast + mechanism fork + 可落地自然数据 + natural method opening。

## 当前状态

| lane | project | status | model calls |
|---|---|---|---|
| behavioral validation | [`active/007_weak_evidence_backfire/`](active/007_weak_evidence_backfire/) | legacy registered project；当前 30-case frozen D0 | **authorized** |
| blocked legacy | [`active/013_publicness_coordination_dissociation/`](active/013_publicness_coordination_dissociation/) | `HOLD-D0` | no |
| pre-candidate legacy | [`active/003_diagnostic_counterevidence_revision/`](active/003_diagnostic_counterevidence_revision/) | `G0-NOT-RUN` | no |
| discovery | [`phenomenon_miner/candidate_pool/`](phenomenon_miner/candidate_pool/) | 新题必须在这里完成 N0+N1+D0 feasibility | no |
| terminal history | [`archive/`](archive/) | 已停止项目与最终证据链 | no |

**唯一模型调用授权源是 [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md)。**

## 新题现在怎么走

```text
idea / mother question
→ N0 breadth novelty audit
→ N1 depth novelty audit
→ D0 source-feasibility audit
→ DISCOVERY-PASS
→ formal registration
→ materialize + freeze 已锁定 D0
→ smoke
→ generality
→ mechanism
```

关键变化：

- **N0/N1 都在选题阶段做完。** 不再规定 smoke 后常规再查一次 novelty。
- **数据搜索也在选题阶段做完。** source/version/license/gold/unit/count/构造 recipe 都要先有答案。
- `active/` 不再用来继续“完善题目”。新题没通过 discovery package，就留在 candidate pool。
- 注册以后 D0 只做 materialization/freeze；若必须换数据源或核心 recipe，退回 discovery。

## 权威入口

1. [`phenomenon_miner/PROCESS.md`](phenomenon_miner/PROCESS.md) — 新版完整状态机。
2. [`phenomenon_miner/REQUIREMENTS.md`](phenomenon_miner/REQUIREMENTS.md) — 选题、novelty、data feasibility、behavior/generality 硬门槛。
3. [`phenomenon_miner/NOVELTY_GATE.md`](phenomenon_miner/NOVELTY_GATE.md) — N0 breadth + N1 depth 的前置审计规则。
4. [`PHENOMENON_MINING_GUIDE.md`](PHENOMENON_MINING_GUIDE.md) — 精简后的找题执行指南。
5. [`phenomenon_miner/candidate_pool/README.md`](phenomenon_miner/candidate_pool/README.md) — Batch 与长期 idea inventory。
6. [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md) — 当前模型调用授权。

公开数据集索引见 [`DATASET_CATALOG.md`](DATASET_CATALOG.md)，失败复盘见 [`FAILURE_POSTMORTEMS.md`](FAILURE_POSTMORTEMS.md)。

## 不变规则

- Behavior first；现象没过行为与一般性，不靠 hidden-state evidence 救题。
- custom-only 不能独立承担 paper-level naturalness / generality。
- terminal failure 不靠换弱模型、subset、readout、阈值或名字续命。
- claim 或 source 若实质改变，退回 discovery，而不是在 active 中悄悄换 contract。
- novelty 只在出现具体新 collision 或 claim 实质变化时 targeted refresh，不做流程性重复搜索。
