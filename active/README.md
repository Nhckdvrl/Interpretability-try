# Active Projects

`active/` 只表示“当前仍可能继续处理”，**不表示已经获准调用模型**。唯一授权源是 [`../phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](../phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md)。

## 当前目录

| project | 当前定位 | 调度状态 |
|---|---|---|
| [`003_diagnostic_counterevidence_revision/`](003_diagnostic_counterevidence_revision/) | mechanism-oriented pre-candidate；MedEinst mother behavior 已有公开证据，本项目 G0 未跑 | NOT AUTHORIZED |
| [`007_weak_evidence_backfire/`](007_weak_evidence_backfire/) | 当前 30-case natural D0 contract，N0/D0 PASS | **READY-TO-SMOKE / AUTHORIZED** |
| [`013_publicness_coordination_dissociation/`](013_publicness_coordination_dissociation/) | N0 PASS，但 natural D0 数量 / license 不足 | HOLD-D0 / NOT AUTHORIZED |

## 007 result lineage

007 目录里同时存在“当前可运行 contract”和“旧 contract 的失败结果”，这是目前最容易误读的地方：

- `results/smoke_r5/`：2026-08-29 在 execution commit `0ef5...` 上运行，使用 25-case D0（SHA `b1f6...`），two-family verdict 是 hard kill；
- 后续 `3cbe5e2` 实质修订 D0 provenance / held-out LR / builder；
- 当前 README / registry 指向 30-case D0（SHA `d3ef...`），因此旧 smoke 只属于旧 contract，不是当前 30-case verdict。

见 [`007_weak_evidence_backfire/results/README.md`](007_weak_evidence_backfire/results/README.md)。任何汇总都必须按 D0 SHA / contract version 分开。

## 根目录里的两个 validation audit

- [`VALIDATION_AUDIT_006_007.md`](VALIDATION_AUDIT_006_007.md)
- [`VALIDATION_AUDIT_007_012_013.md`](VALIDATION_AUDIT_007_012_013.md)

它们是**历史 cross-project provenance**，不是当前状态表。006、012 的后续终局已经进入 archive；当前状态请看本 README、project README 和 authoritative registry。

## 编号说明

active 编号按历史注册序列使用，新的编号不复用。仓库早期在规则冻结前出现过 legacy 编号重复，所以 archive 中可能有相同数字前缀但不同题目；完整目录名才是 project identity。