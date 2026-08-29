# 候选审计与调度注册表

版本：2026-08-29
状态：`AUTHORITATIVE`

## 调度结论

**当前 `READY-TO-SMOKE`：1 — `active/007_weak_evidence_backfire`.**

- 007：`N0-PASS / D0-PASS / READY-TO-SMOKE`，30 个 frozen natural scenarios，20/20 manual audit，`validation_authorized: true`。
- 012：**`ARCHIVED / TERMINAL-KILLED / HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`**。D0 保持 PASS。r2 是 instrumentation hold；r3 只修 credibility capability probe 后完整重跑。决定性审计在直接 grant memory gate 后仍得到 Qwen **0/108**、Gemma **0/108** weighting-capable pairs，对比冻结门槛 20，主因 `belief_initial_gap`。`validation_authorized: false`；不再进入 N1、generalization panel 或 mechanism。
- 013：`N0-PASS / HOLD-D0 / NOT READY-TO-SMOKE`，强自然 anchor 已找到，但独立 scenario 数量与 adaptation/license 条件不足。

## N0 范围决议

2026-08-28 的十题 adversarial N0 已对 strongest neighbor、mother inclusion、`why_not_a_rename`、decisive contrast 和 hard kill 做过针对性审计。本项目决定接受该审计作为 007/012/013 的 pre-smoke N0 basis，不再要求形式上重复同一套大规模检索。

本仓库从人类认知/决策/社会行为中的自然现象出发寻找 LLM failure，因此**人类母现象已知不是 collision 本身**。Collision 要求已有 LLM 工作覆盖 exact/near-exact phenotype、decisive contrast 或机制。007/012 在后续 duplicate independent audit 中因为人类 weak-evidence/sleeper-effect 文献而得到的 `KILLED-COLLISION` 判定已经 superseded；历史文件保留作 provenance，权威状态以本表和各项目 N0 resolution 为准。

N1 仍在 smoke 后、扩模型前强制执行；已经由真实行为 hard kill 终止的项目不进入 N1。

## 当前十题

| # | 题目 | 当前状态 | 实现 / 归档 | 授权 |
|---:|---|---|---|---|
| 1 | First-Negative-Evidence Harm | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 2 | Packed–Unpacked Event Splitting | `ARCHIVED / HOLD-OPERATIONALIZATION-ARTIFACT` | `archive/009_packed_unpacked_event_splitting/` | false |
| 3 | Publicness–Coordination Dissociation | `N0-PASS / HOLD-D0 / ACTIVE-PREFLIGHT` | `active/013_publicness_coordination_dissociation/` | false |
| 4 | Existential Witness Collapse | `ARCHIVED / HARD-KILL-NO-ILLEGAL-JOIN` | `archive/011_existential_witness_collapse/` | false |
| 5 | Inadmissible-Evidence Persistence | `ARCHIVED / TERMINAL-HOLD-D0V3-CONTRACT` | `archive/010_inadmissible_evidence_persistence/` | false |
| 6 | Habitual → Episode Actualization | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 7 | Mixed-Status Event Attraction | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 8 | Dissent → Holding Role Swap | `ADVERSARIAL-N0-SURVIVOR` | — | false |
| 9 | Source-Discount Recovery | `ARCHIVED / TERMINAL-KILLED / HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR` | `archive/012_source_discount_recovery/` | false |
| 10 | Weak-Evidence Backfire | `N0-PASS / D0-PASS / READY-TO-SMOKE` | `active/007_weak_evidence_backfire/` | true |

## Registrations

```yaml
active/007_weak_evidence_backfire:
  canonical_shortlist_number: 10
  status: READY-TO-SMOKE
  harness: READY-r5-natural-d0
  formal_n0_verdict: PASS
  n0_basis: 2026-08-28 adversarial audit accepted by project resolution 2026-08-29
  d0_verdict: PASS
  d0_items: 30
  d0_domains: 2
  manual_audit: 20/20 PASS
  frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
  validation_authorized: true

archive/012_source_discount_recovery:
  canonical_shortlist_number: 9
  status: ARCHIVED / TERMINAL-KILLED
  harness: READY-r3
  formal_n0_verdict: PASS
  n0_basis: 2026-08-28 adversarial audit accepted by project resolution 2026-08-29
  d0_verdict: PASS
  d0_source: NetEaseCrowd (CC BY-SA 4.0)
  d0_items: 108
  d0_primary_items: 101
  d0_primary_cells: 8
  d0_secondary_items: 7
  d0_capabilities: 4
  unique_annotators: 216
  manual_audit: 20/20 PASS
  frozen_data_sha256: cde7f3fa9dfeb94645fa2e254507013c26cb2ffb01793b9bd889a86668af1c3a
  r2_disposition: HOLD-INSTRUMENTATION-ARTIFACT
  r3_disposition: TERMINAL-KILLED
  behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
  qwen_counterfactual_weighting_capable_pairs: 0/108
  gemma_counterfactual_weighting_capable_pairs: 0/108
  dominant_blocker: belief_initial_gap
  min_weighting_capable_pairs: 20
  validation_authorized: false

active/013_publicness_coordination_dissociation:
  canonical_shortlist_number: 3
  status: ACTIVE-PREFLIGHT / HOLD-D0
  harness: READY-r1
  formal_n0_verdict: PASS
  d0_verdict: HOLD
  hold_reason: insufficient independent natural scenario pairs and adaptation/license constraints
  validation_authorized: false
```

## 012 terminal evidence

r2 的 two-family first shot 因 `source_credibility` yes/no probe 的 always-Yes gold 和巨大 answer-order artifact，被保留为 instrumentation hold，而不是科学 kill。r3 只把这个 probe 改成 counterbalanced `more reliable / less reliable` content-choice，其余 bank、101/7 stratification、cell bootstrap、support probes、belief/action readout、`p_target` aggregation 和 thresholds 全部冻结，并对 Qwen3-8B / Gemma-3-12B-IT 全量重跑。

r3 普通 summarizer 仍先停在 memory floor，但项目终局不依赖该 probe：直接将 memory gate 视为通过后，只应用冻结的 support gate、immediate-influence floors 与 initial-gap thresholds，Qwen 仅 9/216 direction entries 通过、Gemma 8/216；双方向成 pair 后两家族均为 **0/108**，冻结要求至少 20。故 012 终止于 source-weighting capability floor，不解释 recovery/reinstatement，不再修改 belief readout、阈值、bidirectionality 或模型以续命。详见 `archive/012_source_discount_recovery/FINAL_VERDICT.md`。

## 已终止 / 归档项目

原有 KILL/ROUTE/HOLD 记录继续以其 archive/audit 文件为准，包括 OIR/AIC/ATW/CSS 全系、MTR-13/14、SEC-06、UDH-03、Existential Witness Collapse、Packed–Unpacked Event Splitting、Inadmissible-Evidence Persistence，以及历史 active 002–010 的各自失败记录。不得因为后续流程澄清而复活已由**真实行为结果、数据合同失败或 exact LLM collision**终止的项目。

## 调度纪律

- 只有 `validation_authorized: true` 可调用模型；当前注册表中为 007。
- 012 已终止且归档；D0 虽为 PASS，但 `validation_authorized: false`，不得第四次重跑、修改 readout/阈值救题或进入 N1 / mechanism。
- 013 在 HOLD-D0 解除前不得造 synthetic substitute。
- 007 后续行为按其冻结合同与独立结果记录执行。
