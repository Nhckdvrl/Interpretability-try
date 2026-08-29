# Candidate Pool

版本：2026-08-29  
定位：**discovery inventory / N0 workspace，不是模型实验队列。**

任何候选能否调用模型，只看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。`SURVIVE`、`A+`、`promising`、进入某个 batch，都没有授权效力。

## 当前入口

### Batch 3 — mother-paper extension（当前优先）

- [`BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md) — 当前 10 个 reviewer-mode survivor；
- [`BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md) — mother sweep、reserve、kill、extension death ledger。

当前十题：Alias Entrainment Transfer、Task-Switch TR/TL Desynchronization、Dead-Branch Residue、Training-Recency Conflict Arbitration、Predicate-Revision Eager-Flag Staleness、GeoTemporal Binding Bottleneck、Action-Boundary State Routing、Resolved-Ambiguity Neuron Persistence、Synonym-Saturation Escape、Causal Retrieval Schedule。

全部仍是 `formal_n0_verdict: null / d0_verdict: null / validation_authorized: false`。

### Batch 2 — 当前 V2 shortlist

- [`BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md) — 当前 10 个 reviewer-mode survivor；
- [`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md) — 完整脑暴与死亡账本；
- [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md) — N0 工作稿。

`BATCH2_DEEP_N0_SURVIVORS_10_2026-08-28.md` 是 V2 之前的历史快照，不是当前 shortlist。

### Batch 1 — 历史 deep-N0 shortlist

- [`DEEP_N0_SURVIVORS_10_2026-08-28.md`](DEEP_N0_SURVIVORS_10_2026-08-28.md)
- [`audits/ADVERSARIAL_N0_TEN_2026-08-28.md`](audits/ADVERSARIAL_N0_TEN_2026-08-28.md)

Batch 1 中已有题进入 active / archive；不要依据旧文件里的 `SURVIVE` 判断当前状态。

## 12 个领域文件是什么

`01_...`–`12_...` 保存长期 idea cards、邻近文献、母题、brainstorm 和死亡回填。它们适合：

- 找新方向；
- 查某个旧想法是否已经被 KILL/ROUTE；
- 防止换领域 / 换 readout / 换名字复活旧题。

它们**不适合**直接作为“今天该跑哪个实验”的列表。

## 状态层级

```text
idea card
→ batch survivor
→ formal N0-PASS
→ D0-PASS
→ READY-TO-SMOKE + validation_authorized:true
→ behavioral result
→ N1 / panel
→ mechanism
```

任何一步失败都不能靠下一步机制分析补救。

## 已经进入正式流程的题

当前 canonical shortlist 的 active/archive 映射统一看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。仓库级一页状态看 [`../../CURRENT_STATUS.md`](../../CURRENT_STATUS.md)。