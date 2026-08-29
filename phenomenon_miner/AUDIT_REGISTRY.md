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
| `active/014_alias_entrainment_transfer` | `PHASE-1-PROMOTE / PHASE-2-MECHANISM-B / PHASE-3-SEEN-FORM-ONLY-WRITE`, discovery prerequisites waived by owner | **true** |

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

active/014_alias_entrainment_transfer:
  policy_generation: legacy-v3, accepted into v4 by owner waiver
  note: >
    phase 1 (3 families) and phase 2 head ablation (2 families) were run on
    2026-08-29 under the then-current candidate_pool/AUDIT_REGISTRY.md, before
    the v4 rules existed.
  n0_breadth_verdict: PASS (Batch-3 adversarial audit, SURVIVE-A)
  n1_depth_verdict: WAIVED by project owner 2026-08-29 (not performed)
  d0_source_feasibility_verdict: WAIVED by project owner 2026-08-29 (not performed)
  waiver_scope: >
    The two v4 discovery prerequisites -- the 20-pair human audit of alias
    conventionality/ambiguity/frequency stratification required by
    CURRENT_TOPICS.md Tier S, and N1 closure -- were not performed. The project
    owner reviewed this on 2026-08-29 and elected to proceed. Recorded as a
    waiver, not as completed audits, so the distinction survives in the record.
    What WAS done during D0 construction: two rounds of sample inspection, which
    drove the SEMREL selection constraint, the orthographic strata, and the
    discovery of the NED frame leak.
  frozen_data_sha256: c744ae319600fc79e80195ca5b5774b0af6b812714371812e0f61259dae37239
  phase3_contract: 2026-08-29-r3, frozen before any phase-3 forward pass
  phase3_result: >
    SEEN-FORM-ONLY-WRITE in 4/4 cells (the pre-registered negative). Direct logit
    attribution of the phase-2 entrainment heads reproduces their write toward a
    SEEN token strongly (dDLA_EXACT +0.56/+2.84 vs random +0.13/-0.05) but shows
    nothing above a similarity-matched control for the unseen alias in the clean
    stratum (+0.021 / +0.088, CIs include 0). The alias DLA scales monotonically
    with orthographic overlap (opaque_strict +0.02/+0.09 -> opaque +0.20/+0.72 ->
    partial +0.38/+1.15) while dDLA_EXACT is flat across the same strata, so the
    heads' direct write generalizes lexically, not by entity.
  phase3_reading: >
    phase 2 (ablation removes the alias effect) and phase 3 (direct write does not
    carry it) together imply the entity component is routed through these heads
    INDIRECTLY. That joint inference is not itself tested; path patching from these
    heads into later layers is what would test it.
  phase3_validation: DLA implementation checked against per-head ablation on
    last-layer heads, r=0.959, slope=0.938
  results: active/014_alias_entrainment_transfer/results/
  validation_authorized: true
```

## Discipline

- `active/` 本身不代表授权。
- `Tier S/A/B`、`survivor`、旧 `promoted` 标签都不代表授权。
- 运行前确认 project README、config、frozen D0 SHA 与本表一致。
- 旧 result 不得跨 contract / D0 SHA 继承 verdict。
- terminal project 不得通过换 readout、阈值、模型或名字重新获得授权。
