# Candidate Audit & Dispatch Registry

版本：2026-08-29  
状态：`AUTHORITATIVE`

> **唯一模型调用授权源。** 只有本文件明确写为 `READY-TO-SMOKE` 且 `validation_authorized: true` 的 project 可以运行模型。

## Dispatch

| project | status | authorized |
|---|---|---:|
| `active/007_weak_evidence_backfire` | `N0-PASS / D0-PASS / READY-TO-SMOKE` | **true** |
| `active/013_publicness_coordination_dissociation` | `N0-PASS / HOLD-D0` | false |
| `active/003_diagnostic_counterevidence_revision` | `PRE-CANDIDATE / G0-NOT-RUN` | false |
| `archive/012_source_discount_recovery` | `TERMINAL-KILLED` | false |

## Registered contracts

```yaml
active/007_weak_evidence_backfire:
  canonical_shortlist_number: 10
  formal_n0_verdict: PASS
  d0_verdict: PASS
  d0_items: 30
  d0_domains: 2
  manual_audit: 20/20 PASS
  frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
  validation_authorized: true

active/013_publicness_coordination_dissociation:
  canonical_shortlist_number: 3
  formal_n0_verdict: PASS
  d0_verdict: HOLD
  hold_reason: insufficient independent natural scenario pairs and adaptation/license constraints
  validation_authorized: false

archive/012_source_discount_recovery:
  canonical_shortlist_number: 9
  formal_n0_verdict: PASS
  d0_verdict: PASS
  behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
  validation_authorized: false
```

007 的 contract/result lineage 只在 [`../../active/007_weak_evidence_backfire/README.md`](../../active/007_weak_evidence_backfire/README.md) 维护；012 的 terminal evidence 只在 [`../../archive/012_source_discount_recovery/FINAL_VERDICT.md`](../../archive/012_source_discount_recovery/FINAL_VERDICT.md) 维护；013 的 D0 blocker 只在其 project README / D0 audit 维护。

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
| 10 | Weak-Evidence Backfire | `N0-PASS / D0-PASS / READY-TO-SMOKE` | `active/007_weak_evidence_backfire/` |

## Scope & discipline

已知人类母现象本身不构成 LLM collision；collision 要求已有 LLM 工作覆盖 exact/near-exact phenotype、decisive contrast 或核心机制。完整 N0/N1 规则见 [`../NOVELTY_GATE.md`](../NOVELTY_GATE.md)。

- 运行前确认 project README、config、D0 SHA 与本表一致。
- 旧 result 不得跨 contract / D0 SHA 继承 verdict。
- terminal project 不得通过换 readout、阈值、模型或名字续命。
- Batch survivor / domain idea card 都没有实验授权。
