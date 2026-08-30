# Active Projects

`active/` 保存**当前仍值得继续投入**的项目、HOLD-redesign 项目，以及少量历史 provenance。目录存在不等于 paper claim 成立；模型调用权限仍以 [`../phenomenon_miner/AUDIT_REGISTRY.md`](../phenomenon_miner/AUDIT_REGISTRY.md) 为准。

2026-08-30 对已完成 Top-6 做了独立 post-run audit。完整逐题审查见 [`../phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md`](../phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md)。

## 当前真正值得继续的主线

| project | scientific status | 下一步 |
|---|---|---|
| [`014_alias_entrainment_transfer`](014_alias_entrainment_transfer/) | **ESTABLISHED / CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC** | 整理论文：broad learned-relation spillover + structure gradient + phase-2 shared upstream cause + phase-3 lexical boundary；禁止 reference-specific rescue |
| [`018_stock_flow_correlation_intrusion`](018_stock_flow_correlation_intrusion/) | **HOLD-D0-MEASUREMENT-FAILURE / SCIENTIFIC STATUS UNKNOWN** | 先冻结不依赖 A/B 位置的 semantic/numeric net-recognition D0 v2；不允许 positive-net-only rescue |
| [`020_incremental_clue_backfire`](020_incremental_clue_backfire/) | REGISTERED / not yet adjudicated | 先做内部 Evidence-Induced Referent Displacement collision，再决定是否跑 |
| [`021_task_switch_carryover`](021_task_switch_carryover/) | REGISTERED / not yet adjudicated | 只认 old-rule-specific wrong destination；普通 task-switch drop 不算 novelty |
| [`022_local_success_global_composition_failure`](022_local_success_global_composition_failure/) | REGISTERED / not yet adjudicated | 必须超出 Press et al. compositionality gap：中间事实显式给出后仍组合错 |
| [`023_description_experience_gap`](023_description_experience_gap/) | REGISTERED / not yet adjudicated | exact-frequency / EV capability-gated D0 |

## Top-6 审完后已归档

以下项目的**当前注册科学合同已经被诊断性实验否掉**，完整代码、数据合同、raw result 与报告已整体移入 `archive/`：

- `archive/015_clarification_resolution_lag` — ambiguity-history effect 被 matched neutral history 解释；三个家族 ambiguity-specific residual 均为 null。
- `archive/016_mixed_status_event_attraction` — `MIXED-LOCAL` 表面效应被 same-status context 解释；三家族 `MIXED-SAME` 主对比不成立。
- `archive/017_cross_modal_resolution_inertia` — 最强的 Llama text-first effect 被 masked-choice history 几乎完全复制；不需要旧 interpretation identity。
- `archive/019_abstention_hysteresis` — 三家族、两 source、生成和连续概率 readout 均强烈朝假设反方向；neutral history 解释大部分 recovery。

这些项目不能通过换模型、prompt、subset、threshold 或 readout 在原项目名下复活。若未来出现真正不同的 scientific object，必须新建 contract。

## 018 为什么没有一起归档

018 的数据 bank 本身很好，但 D0 的 net-flow capability gate 依赖 A/B forced choice。负 net cells 在 Llama 上出现 canonical 约 99–100%、reversed 0% 的极端位置效应，Qwen/Gemma 也有严重 presentation bias。因此完整 2×2 estimand 根本没有合法 denominator。

这叫 **measurement failure / inconclusive**，不能写成“Stock–Flow Intrusion 不存在”。下一版若做，必须保留四个自然语义 cell，只替换 recognition instrument。

## 旧 provenance

- `003_diagnostic_counterevidence_revision/` — legacy pre-candidate。
- `007_weak_evidence_backfire/` — TERMINAL HARD KILL；目录仍在 active 仅因历史 raw/code provenance，后续可再统一物理归档。
- `013_publicness_coordination_dissociation/` — PARKED / HOLD-DATA。

## 运行纪律

```text
clean behavioral positive
+ fatal controls survive
+ source/scope valid
+ exact collision closed
-> full validation / mechanism
```

`NO-PROMOTE` 不能机械等于 scientific null：若 capability/measurement denominator 从未建立，应标 `INCONCLUSIVE/HOLD-REDESIGN`；只有诊断性对照真正否掉 registered claim 才进入 archive。
