# Candidate Audit & Dispatch Registry

版本：2026-08-29  
状态：`AUTHORITATIVE`

> **唯一模型调用授权源。** 本文件只负责已经正式注册项目的 dispatch，不负责替 candidate pool 补 novelty 或找数据。

## v4 registration policy

对 **新项目**，写入 registry 之前必须已经在 discovery 阶段完成：

```yaml
n0_breadth_verdict: PASS
n1_depth_verdict: PASS
d0_source_feasibility_verdict: PASS
```

正式注册后只允许 materialize/freeze 已锁定 D0；不允许再普通地搜索新数据源或补一轮 routine N1。

现有 003/007/013 是 v4 之前的 legacy entries，不要求为了形式机械重跑 N1；只有 claim/source 实质变化或出现具体新 collision 才 refresh。

当前未注册候选的 survival queue 只看 [`CURRENT_SURVIVORS_2026-08-29.md`](CURRENT_SURVIVORS_2026-08-29.md)；该文件没有 dispatch 权。

## Dispatch

| project | status | authorized |
|---|---|---:|
| `active/007_weak_evidence_backfire` | legacy `D0-PASS / READY-TO-SMOKE` | **true** |
| `active/013_publicness_coordination_dissociation` | legacy `HOLD-D0` | false |
| `active/003_diagnostic_counterevidence_revision` | legacy `PRE-CANDIDATE / G0-NOT-RUN` | false |
| `archive/012_source_discount_recovery` | `TERMINAL-KILLED` | false |

## Registered contracts

```yaml
active/007_weak_evidence_backfire:
  policy_generation: legacy-v3
  canonical_shortlist_number: 10
  d0_verdict: PASS
  d0_items: 30
  frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
  validation_authorized: true

active/013_publicness_coordination_dissociation:
  policy_generation: legacy-v3
  canonical_shortlist_number: 3
  d0_verdict: HOLD
  validation_authorized: false

archive/012_source_discount_recovery:
  policy_generation: legacy-v3
  canonical_shortlist_number: 9
  behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
  validation_authorized: false
```

项目科学细节只在 project README / D0 audit / FINAL_VERDICT 维护。

## Canonical shortlist #1–#10

| # | topic | current status | path |
|---:|---|---|---|
| 1 | First-Negative-Evidence Harm | `KILLED-v4-REAUDIT / ROUTE` | — |
| 2 | Packed–Unpacked Event Splitting | archived | `archive/009_packed_unpacked_event_splitting/` |
| 3 | Publicness–Coordination Dissociation | legacy HOLD-D0 | `active/013_publicness_coordination_dissociation/` |
| 4 | Existential Witness Collapse | archived | `archive/011_existential_witness_collapse/` |
| 5 | Inadmissible-Evidence Persistence | archived | `archive/010_inadmissible_evidence_persistence/` |
| 6 | Habitual → Episode Actualization | `CONTINUE-DISCOVERY-v4` | `candidate_pool/CURRENT_SURVIVORS_2026-08-29.md` |
| 7 | Mixed-Status Event Attraction | `CONTINUE-DISCOVERY-v4` | `candidate_pool/CURRENT_SURVIVORS_2026-08-29.md` |
| 8 | Dissent → Holding Role Swap | `CONTINUE-DISCOVERY-v4 / HOLD-DATA-GOLD` | `candidate_pool/CURRENT_SURVIVORS_2026-08-29.md` |
| 9 | Source-Discount Recovery | archived | `archive/012_source_discount_recovery/` |
| 10 | Weak-Evidence Backfire | legacy READY-TO-SMOKE | `active/007_weak_evidence_backfire/` |

运行前仍必须确认 project README、config、D0 SHA 与本表一致。旧 result 不得跨 contract/D0 SHA 继承 verdict；terminal project 不得续命。
