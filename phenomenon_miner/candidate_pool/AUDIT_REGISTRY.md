# 候选审计与调度注册表

版本：2026-08-29  
状态：`AUTHORITATIVE`

> **本文件是唯一模型调用授权源。** 只有同时写明 `READY-TO-SMOKE` 与 `validation_authorized: true` 的 project 可以运行模型。Batch survivor、active 目录名、旧 result verdict 都不能自行授权。

## 当前调度结论

**READY-TO-SMOKE：1 — `active/007_weak_evidence_backfire`（当前 30-case contract）。**

| project | status | authorization |
|---|---|---:|
| `active/007_weak_evidence_backfire` | `N0-PASS / D0-PASS / READY-TO-SMOKE` | **true** |
| `active/013_publicness_coordination_dissociation` | `N0-PASS / HOLD-D0` | false |
| `active/003_diagnostic_counterevidence_revision` | `PRE-CANDIDATE / G0-NOT-RUN`；不属于本轮 canonical ten 的正式调度项 | false |
| `archive/012_source_discount_recovery` | `TERMINAL-KILLED / HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR` | false |

## 007 contract lineage

当前授权针对：

```yaml
project: active/007_weak_evidence_backfire
canonical_shortlist_number: 10
formal_n0_verdict: PASS
d0_verdict: PASS
d0_items: 30
d0_domains: 2
manual_audit: 20/20 PASS
frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
validation_authorized: true
```

仓库同时保留 `active/007_weak_evidence_backfire/results/smoke_r5/`。那次 smoke 的 execution commit 是 `0ef5ee6...`，使用 **25-case D0 / SHA `b1f6f889...`**，并在该旧 contract 下得到 `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`。之后 `3cbe5e2` 实质修订 D0 provenance、held-out LR verifier 和 builder，当前 project 切到上面的 30-case SHA。

因此：

- 旧 smoke 结果保持有效历史 provenance；
- 旧 hard kill 只属于旧 25-case contract；
- 当前 30-case contract 尚不能引用旧 aggregate 作为结果；
- 新 smoke 必须写入新 result directory，并记录当前 D0 SHA、execution commit、model revisions 与完整性审计。

## 012 terminal registration

```yaml
project: archive/012_source_discount_recovery
canonical_shortlist_number: 9
formal_n0_verdict: PASS
d0_verdict: PASS
d0_source: NetEaseCrowd (CC BY-SA 4.0)
d0_items: 108
d0_primary_items: 101
d0_secondary_items: 7
unique_annotators: 216
manual_audit: 20/20 PASS
frozen_data_sha256: cde7f3fa9dfeb94645fa2e254507013c26cb2ffb01793b9bd889a86668af1c3a
r2_disposition: HOLD-INSTRUMENTATION-ARTIFACT
r3_disposition: TERMINAL-KILLED
behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
qwen_counterfactual_weighting_capable_pairs: 0/108
gemma_counterfactual_weighting_capable_pairs: 0/108
min_weighting_capable_pairs: 20
dominant_blocker: belief_initial_gap
validation_authorized: false
```

r2 的 `source_credibility` yes/no probe 因 always-Yes gold / answer-order artifact 只记 instrumentation hold；r3 只修该 probe 并完整重跑。终局判断不依赖 memory probe：即使直接 grant memory gate，两家族仍都是 0/108 weighting-capable pairs，所以不允许第四枪、换 belief readout、改阈值、N1、扩 panel 或 mechanism 续命。

## 013 registration

```yaml
project: active/013_publicness_coordination_dissociation
canonical_shortlist_number: 3
formal_n0_verdict: PASS
d0_verdict: HOLD
hold_reason: insufficient independent natural scenario pairs and adaptation/license constraints
validation_authorized: false
```

强 natural common-knowledge / coordination anchor 存在，但 D0 不能靠 synthetic filler 补齐；HOLD 解除前不得调用模型。

## Canonical shortlist #1–#10

| # | topic | current status | path |
|---:|---|---|---|
| 1 | First-Negative-Evidence Harm | `ADVERSARIAL-N0-SURVIVOR` | — |
| 2 | Packed–Unpacked Event Splitting | `ARCHIVED / HOLD-OPERATIONALIZATION-ARTIFACT` | `archive/009_packed_unpacked_event_splitting/` |
| 3 | Publicness–Coordination Dissociation | `N0-PASS / HOLD-D0` | `active/013_publicness_coordination_dissociation/` |
| 4 | Existential Witness Collapse | `ARCHIVED / HARD-KILL-NO-ILLEGAL-JOIN` | `archive/011_existential_witness_collapse/` |
| 5 | Inadmissible-Evidence Persistence | `ARCHIVED / TERMINAL-HOLD-D0V3-CONTRACT` | `archive/010_inadmissible_evidence_persistence/` |
| 6 | Habitual → Episode Actualization | `ADVERSARIAL-N0-SURVIVOR` | — |
| 7 | Mixed-Status Event Attraction | `ADVERSARIAL-N0-SURVIVOR` | — |
| 8 | Dissent → Holding Role Swap | `ADVERSARIAL-N0-SURVIVOR` | — |
| 9 | Source-Discount Recovery | `ARCHIVED / TERMINAL-KILLED` | `archive/012_source_discount_recovery/` |
| 10 | Weak-Evidence Backfire | `N0-PASS / D0-PASS / READY-TO-SMOKE` on current 30-case contract | `active/007_weak_evidence_backfire/` |

## N0 scope resolution

2026-08-28 adversarial N0 对 mother inclusion、strongest neighbor、`why_not_a_rename`、decisive contrast 与 hard kill 做过针对性审计。项目允许从已知的人类认知/决策/社会现象出发研究 LLM failure，因此**人类母现象已知本身不构成 LLM collision**。Collision 要求已有 LLM 工作覆盖 exact/near-exact phenotype、decisive contrast 或核心机制。

007/012 后续 duplicate independent audit 因人类 weak-evidence / sleeper-effect 文献给出的 `KILLED-COLLISION` 已被项目级 N0 resolution supersede；历史文件保留作 provenance。Smoke 后的 N1 仍是强制步骤，除非项目已经被真实行为 hard kill 终止。

## 调度纪律

- 只有 `validation_authorized: true` 可以调用模型；当前只有 007 的 **current 30-case contract**。
- 运行前必须确认 project README、config、D0 SHA 与本表一致。
- 旧 result 不能跨 contract version / D0 SHA 继承 verdict。
- 012 已 terminal，不得续命。
- 013 HOLD-D0 未解除前不得 synthetic substitute。
- Batch 1/2/3 survivor 都不是 formal authorization。
