# Interpretability Topic Search

这个仓库用于寻找和验证 **LLM 可解释性研究题目**。目标不是先选 SAE / attention head / activation patching 再找故事，而是从自然问题、已知现象或强 mother paper 出发，先证明值得解释的行为对象存在，再进入机制与方法。

> **目标尺度：ACL / EMNLP / NAACL Main 级别的 mother question + decisive contrasts + mechanism fork + natural method opening。**

## 先看哪里

如果只想知道“仓库现在到底在做什么”，按下面顺序看：

1. [`CURRENT_STATUS.md`](CURRENT_STATUS.md) — **当前状态总表**；active / blocked / archived / discovery queue 一页看完。
2. [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md) — **唯一有模型调用授权权的调度表**。
3. [`phenomenon_miner/PROCESS.md`](phenomenon_miner/PROCESS.md) — N0 → D0 → smoke → N1 → panel → mechanism 的唯一合法流程。
4. [`phenomenon_miner/REQUIREMENTS.md`](phenomenon_miner/REQUIREMENTS.md) — 选题与晋级硬门槛。
5. [`phenomenon_miner/NOVELTY_GATE.md`](phenomenon_miner/NOVELTY_GATE.md) — exact collision / mother inclusion / successor / N1 规则。
6. [`RESEARCH_CRITERIA.md`](RESEARCH_CRITERIA.md) — 整理前根 README 的**完整详细选题标准快照**，原样保留，不作为当前状态表。
7. [`phenomenon_miner/candidate_pool/README.md`](phenomenon_miner/candidate_pool/README.md) — Batch 1 / 2 / 3 的找题入口。
8. [`archive/README.md`](archive/README.md) — 已终止项目与历史编号说明。

长版搜索方法、relation taxonomy、anomaly signatures 见 [`PHENOMENON_MINING_GUIDE.md`](PHENOMENON_MINING_GUIDE.md)；公开数据集入口见 [`DATASET_CATALOG.md`](DATASET_CATALOG.md)；真实失败经验见 [`FAILURE_POSTMORTEMS.md`](FAILURE_POSTMORTEMS.md)。

## 当前快照（2026-08-29）

| lane | project | 状态 | 能否调用模型 |
|---|---|---|---|
| current behavioral validation | `active/007_weak_evidence_backfire` | `N0-PASS / D0-PASS / READY-TO-SMOKE`，当前 contract 是 30-case natural D0 | **可以，仅限冻结 contract** |
| blocked active | `active/013_publicness_coordination_dissociation` | `N0-PASS / HOLD-D0` | 否 |
| mechanism-oriented pre-candidate | `active/003_diagnostic_counterevidence_revision` | mother failure 已有公开证据，但本项目 G0 尚未运行 | 否 |
| terminal archive | `archive/012_source_discount_recovery` | `HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR` | 否 |
| discovery queue | Batch 3 mother-paper extensions | 10 个 reviewer-mode survivors，**不是 formal N0-PASS** | 否 |

### 007 的历史 smoke 不要和当前 contract 混用

`active/007_weak_evidence_backfire/results/smoke_r5/` 保存了一次真实 two-family smoke，但它运行在 **旧的 25-case D0**（SHA `b1f6...`，execution commit `0ef5...`）上，并得到 hard kill。之后 `3cbe5e2` 对 D0 provenance / held-out LR / builder 做了实质修订，当前项目 README 与 registry 指向 **30-case D0**（SHA `d3ef...`）。

所以：旧 smoke 是有效历史证据，但不是当前 30-case contract 的结果。两套数据和 verdict 不得混算。详见 [`active/007_weak_evidence_backfire/results/README.md`](active/007_weak_evidence_backfire/results/README.md)。

## 目录地图

```text
active/                 当前仍可能继续的项目；进入 active 不等于获得模型调用授权
archive/                已终止项目；保留完整代码、D0、结果与 FINAL_VERDICT/provenance
phenomenon_miner/       现象发现、N0/D0 流程、candidate pool 与正式调度表
preflight/              历史共享 preflight 工具/环境记录，不是当前项目队列
rejected_candidates/    更早期 rejected idea / postmortem 档案，不是当前死亡账本主入口
```

`candidate_pool/01_...`–`12_...` 是领域化想法库存；Batch 文件是某一轮的 shortlist / ledger；**两者都不直接授权实验**。

## 五条不会变的规则

1. **只有 `AUDIT_REGISTRY.md` 中 `validation_authorized: true` 的项目可以调用模型。** 文件夹名字、`SURVIVE`、`promising`、甚至 `active/` 本身都没有调度权。
2. **N0 / D0 在模型调用之前。** 已知人类母现象可以作为 anchor；collision 指已有 LLM 工作覆盖 exact/near-exact phenotype、decisive contrast 或核心机制，不是“人类现象早有人发现”本身。
3. **Behavior first。** 自然行为 prerequisite 没过，不做 probe / SAE / attention sweep / activation patching 来救题。
4. **custom-only 不能晋级。** synthetic 只用于单测、最小控制和 mechanism sandbox；paper-level 行为必须有公开/自然 anchor。
5. **失败不续命。** 不因看到结果后换弱模型、挑 subset、改 readout、改阈值或重命名而复活；如果 contract 因独立审计被实质修订，必须明确记录旧/新 contract 的边界，不能把旧结果当新结果。

## 编号

`active/NNN_*` 的编号表示历史注册序列，原则上不复用。早期仓库在规则冻结前存在 legacy 编号重复，因此 `archive/` 中可能看到相同数字前缀对应不同老项目；不要仅凭数字判断同一 project，始终使用完整目录名与 registry 映射。

---

**日常工作建议：** 新想法先进入 `phenomenon_miner/candidate_pool/`；formal N0/D0 通过且注册后才进入可运行阶段；一旦 terminal kill，完整搬入 `archive/`，并在 `archive/README.md` 和 registry 留一条终局索引。