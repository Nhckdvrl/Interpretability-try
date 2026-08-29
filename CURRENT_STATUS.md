# Current Research Status

更新时间：2026-08-29  
本文件是**人类阅读用 dashboard**；真正的模型调用权限仍只由 [`phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`](phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md) 决定。

## 1. 当前项目

### 007 — Weak-Evidence Backfire

- 路径：[`active/007_weak_evidence_backfire/`](active/007_weak_evidence_backfire/)
- 当前权威状态：`N0-PASS / D0-PASS / READY-TO-SMOKE`
- 当前 D0：30 natural scenarios，Breast Cancer Wisconsin Diagnostic + Wine
- 当前 frozen D0 SHA256：`d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a`
- `validation_authorized: true`

**历史结果边界：** `results/smoke_r5/` 跑的是更早的 25-case D0，SHA `b1f6f889...`，不是当前 30-case contract。那次 Qwen3-8B / Gemma3-12B-IT smoke 得到 capability-floor hard kill；结果保留，但不能替代当前 contract 的 smoke。详见 [`active/007_weak_evidence_backfire/results/README.md`](active/007_weak_evidence_backfire/results/README.md)。

### 013 — Publicness–Coordination Dissociation

- 路径：[`active/013_publicness_coordination_dissociation/`](active/013_publicness_coordination_dissociation/)
- 状态：`N0-PASS / HOLD-D0 / NOT READY-TO-SMOKE`
- strong human common-knowledge / coordination anchor 已找到
- blocker：独立 natural scenario 数量不足 + adaptation/license 条件不足
- `validation_authorized: false`
- 禁止用 synthetic filler 凑 D0

### 003 — Diagnostic Counterevidence Revision

- 路径：[`active/003_diagnostic_counterevidence_revision/`](active/003_diagnostic_counterevidence_revision/)
- 类型：mechanism-oriented pre-candidate，不属于当前 natural-phenomenon shortlist 的 formal registration
- mother behavior：MedEinst 已公开报告 counterevidence fixation
- 本项目状态：`PRE-CANDIDATE / PAPER-AUDIT-PASSED / G0-NOT-RUN`
- 下一合法动作：先复现官方 behavior G0；在此之前不做机制分析
- 无 registry 授权

## 2. 最近 terminal 项目

### 012 — Source-Discount Recovery

- 路径：[`archive/012_source_discount_recovery/`](archive/012_source_discount_recovery/)
- D0：PASS，108 NetEaseCrowd source pairs，20/20 manual audit
- r2：`HOLD-INSTRUMENTATION-ARTIFACT`
- r3 / terminal：`HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`
- decisive counterfactual audit：直接 grant memory gate 后，Qwen3-8B 与 Gemma3-12B-IT 都是 `0/108` weighting-capable pairs，对比冻结门槛 20
- 不再跑第四枪、N1、扩 panel 或 mechanism

其他历史终止项目统一从 [`archive/README.md`](archive/README.md) 进入。

## 3. Discovery queue

### Batch 3 — 当前优先找题线

入口：

- [`phenomenon_miner/candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](phenomenon_miner/candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md)
- [`phenomenon_miner/candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md`](phenomenon_miner/candidate_pool/BATCH3_HAMDI_MOTHER_PAPER_LEDGER_2026-08-29.md)

10 个 reviewer-mode survivor：

1. Alias Entrainment Transfer
2. Task-Switch TR/TL Desynchronization
3. Dead-Branch Residue after Invalidation
4. Training-Recency Conflict Arbitration
5. Predicate-Revision Eager-Flag Staleness
6. GeoTemporal Binding Bottleneck
7. Action-Boundary State Routing
8. Resolved-Ambiguity Neuron Persistence
9. Synonym-Saturation Escape in Semantic BM25
10. Causal Retrieval Schedule

这些只是 `MOTHER-PAPER-GROUNDED / REVIEWER-MODE-N0-SURVIVOR`，**formal N0 verdict 仍为空，D0 仍为空，不可调用模型。**

### Batch 2 — 已有 10 个 reviewer-mode survivor，保留作为次级候选线

当前 shortlist：[`phenomenon_miner/candidate_pool/BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md`](phenomenon_miner/candidate_pool/BATCH2_DEEP_N0_SURVIVORS_10_V2_2026-08-28.md)。

完整脑暴 / death ledger：[`phenomenon_miner/candidate_pool/BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](phenomenon_miner/candidate_pool/BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

### Batch 1 — 历史 deep-N0 shortlist

入口：[`phenomenon_miner/candidate_pool/DEEP_N0_SURVIVORS_10_2026-08-28.md`](phenomenon_miner/candidate_pool/DEEP_N0_SURVIVORS_10_2026-08-28.md)。其中部分题已经进入 active/archive，当前状态必须回查 registry，不能再看旧 shortlist 的 `SURVIVE` 字样判断。

## 4. 权威性顺序

出现冲突时按以下优先级解释：

```text
1. AUDIT_REGISTRY.md            # 当前调度权
2. 当前 project README/config   # 当前 contract
3. FINAL_VERDICT / result audit # 对应某个明确 contract 的结果
4. batch shortlist / ledger     # discovery 历史
5. domain idea inventory        # brainstorming 历史
```

一个旧 result 只有在 **D0 SHA、contract version、prompt/scorer/gates 与当前 project 一致**时，才能被当成当前 verdict。