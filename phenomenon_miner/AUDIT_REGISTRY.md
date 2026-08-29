# Audit Registry — Model Dispatch

版本：2026-08-29  
状态：`AUTHORITATIVE MODEL-CALL AUTHORIZATION`

本文件只回答一个问题：**哪个正式项目现在可以调用模型？**

它不保存 candidate shortlist、novelty 报告或失败历史；那些分别看 [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md)、[`FINDING_RULES.md`](FINDING_RULES.md)、[`FAILED_TOPICS.md`](FAILED_TOPICS.md)。

## Registration rule

新项目进入本表前必须已经取得：

```yaml
n0_breadth_verdict: PASS
n1_depth_verdict: PASS
d0_source_feasibility_verdict: PASS
```

之后还要 materialize/freeze 已锁定 D0，才能把 `validation_authorized` 设为 true。

## Dispatch

| project | current contract status | authorized |
|---|---|---:|
| `active/007_weak_evidence_backfire` | legacy `D0-PASS / READY-TO-SMOKE` | **true** |
| `active/013_publicness_coordination_dissociation` | legacy `HOLD-D0` | false |
| `active/003_diagnostic_counterevidence_revision` | legacy `PRE-CANDIDATE / G0-NOT-RUN` | false |

## Contract records

```yaml
active/007_weak_evidence_backfire:
  policy_generation: legacy-v3
  d0_items: 30
  frozen_data_sha256: d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a
  validation_authorized: true

active/013_publicness_coordination_dissociation:
  policy_generation: legacy-v3
  d0_verdict: HOLD
  validation_authorized: false

active/003_diagnostic_counterevidence_revision:
  policy_generation: legacy-v3
  status: PRE-CANDIDATE / G0-NOT-RUN
  validation_authorized: false
```

## Discipline

- `active/` 本身不代表授权。
- `Tier S/A/B`、`survivor`、旧 `promoted` 标签都不代表授权。
- 运行前确认 project README、config、frozen D0 SHA 与本表一致。
- 旧 result 不得跨 contract / D0 SHA 继承 verdict。
- terminal project 不得通过换 readout、阈值、模型或名字重新获得授权。
