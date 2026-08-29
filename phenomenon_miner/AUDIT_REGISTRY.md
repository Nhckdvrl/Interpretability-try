# Audit Registry — Model Dispatch

版本：2026-08-29  
状态：`AUTHORITATIVE MODEL-CALL AUTHORIZATION`

本文件只回答一个问题：**哪个正式项目现在可以调用模型？**

当前答案：

```yaml
currently_authorized_model_calls: 0
```

候选排序、数据审查、失败历史分别看 [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md)、[`DATA_REVIEW_2026-08-29.md`](DATA_REVIEW_2026-08-29.md)、[`FAILED_TOPICS.md`](FAILED_TOPICS.md)。

## Registration rule

新项目进入本表前必须已经取得：

```yaml
n0_breadth_verdict: PASS
n1_depth_verdict: PASS
d0_source_feasibility_verdict: PASS
scope_integrity_verdict: PASS
```

之后还要 materialize/freeze 已锁定 D0，并完成 scope summary / attrition audit，才能把 `validation_authorized` 设为 true。

---

## Dispatch

| project | current contract status | authorized |
|---|---|---:|
| `active/003_diagnostic_counterevidence_revision` | legacy `PRE-CANDIDATE / G0-NOT-RUN` | false |
| `active/007_weak_evidence_backfire` | **TERMINAL HARD KILL** — frozen smoke failed evidence-direction capability floor | **false** |
| `active/013_publicness_coordination_dissociation` | `PARKED / HOLD-DATA` — independent natural scenario count/license-adaptation blocker unresolved | false |
| `active/014_alias_entrainment_transfer` | `KEEP / HOLD-FOR-R4-CONSTRUCT-VALIDATION` — phases 1–3 are historical completed work; **next D1 model call blocked** until broad r4 bank + scope/attrition/source audit + frozen SHA are recorded | **false** |

---

## Project records

### active/003_diagnostic_counterevidence_revision

```yaml
policy_generation: legacy-v3
status: PRE-CANDIDATE / G0-NOT-RUN
validation_authorized: false
```

### active/007_weak_evidence_backfire

```yaml
policy_generation: legacy-v3
terminal_verdict: HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR
smoke_result: >
  Qwen3-8B had zero recognition-gated directions. Gemma3-12B-IT had one gated
  pair; its belief/action movement had the opposite sign and failed pragmatic,
  matched-length, neutral and bidirectional survival controls.
continuation_policy: >
  Do not run N1, mechanism work, a broader model panel, alternative thresholds,
  subsets, prompts or readouts to rescue this contract.
validation_authorized: false
results: active/007_weak_evidence_backfire/results/smoke_r5/
```

The project directory is retained only because it contains raw outputs, code and audit provenance. Directory presence is not active scientific status.

### active/013_publicness_coordination_dissociation

```yaml
policy_generation: legacy-v3
d0_verdict: HOLD
current_routing: PARKED-HOLD-DATA
reason: >
  The human common-knowledge coordination paradigm is a strong natural anchor,
  but accessible sources do not currently supply >=20 independent matched
  natural scenarios under a clean adaptation/license path. Participant swaps,
  paraphrases and payoff variants are pseudoreplication, not new units.
validation_authorized: false
```

### active/014_alias_entrainment_transfer

```yaml
policy_generation: legacy-v3, accepted into v4 by historical owner waiver
current_status: KEEP / HOLD-FOR-R4-CONSTRUCT-VALIDATION
historical_model_work:
  phase1: completed before current v4 scope rules
  phase2: completed before current v4 scope rules
  phase3: completed under frozen r3 contract
historical_waivers:
  n1_depth_verdict: WAIVED by project owner 2026-08-29
  d0_source_feasibility_verdict: WAIVED by project owner 2026-08-29
behavior_phenotype: >
  Cross-surface transfer is strong and survives the later 150-pair audit. The
  audit-clean x opaque_strict effect is +2.06 / +1.31 / +2.25 nats across the
  three tested families, with CIs excluding zero.
construct_problem: >
  The original D0 did not establish an entity/reference-specific interpretation:
  compositional pairs were 39%, genuine conventional coreference only 33%, 5%
  were non-coreferent; the old UNREL builder was wrong; ALIAS > SEMREL cannot
  exclude pair-specific learned association. Phase 3 shows entrainment heads'
  direct write is seen-form/lexical, not a direct unseen-alias write.
current_reading: >
  learned cross-surface relation transfer / shared upstream cause; NOT yet a
  proven entity-level salience representation.
canonical_d1_contract: active/014_alias_entrainment_transfer/configs/contract_d1_r4.yaml
r4_scientific_population: >
  broad RedirectQA ordered surface pairs across entity types, surface-structure
  strata and both valid directions. Surface relation/type/direction/capability
  are factors or analysis strata, not hard construction filters.
r4_primary_control: ASSOC_ANY
r4_decisive_questions:
  Q1: broad ALIAS > ASSOC_ANY
  Q2: hard-identity-gated opaque_strict ALIAS > ASSOC_ANY
before_next_model_call:
  - materialize broad r4 raw bank
  - materialize matched ASSOC bank
  - complete source-population audit
  - complete ASSOC/control audit
  - complete scope/attrition summary
  - verify preregistered Q2 capability stratum is source-feasible without convenience narrowing
  - freeze and record r4 dataset SHA
stop_loss: >
  If Q2 cannot be supported without another cascade of convenience filters,
  drop the entity/reference-specific claim. Do not narrow the scientific
  population again and do not use phase-4 mechanism work to rescue the construct.
validation_authorized: false
```

Historical phase-1/2/3 outputs remain valid provenance under their recorded contracts. Setting the **current** authorization to false does not retroactively revoke those runs; it only blocks the next D1/phase-4 call until the corrected data contract is actually materialized and audited.

---

## Discipline

- `active/` directory presence does not imply authorization.
- `Tier S/A/B`, `survivor`, `KEEP`, or historical `promoted` labels do not imply authorization.
- new D0 PASS must include [`DATASET_SCOPE_AUDIT.md`](DATASET_SCOPE_AUDIT.md) scope-integrity PASS.
- old result cannot inherit across contract / dataset SHA changes.
- terminal project cannot regain authorization by changing model, threshold, subset, prompt, readout or name.
- mechanism evidence cannot rescue a failed behavioral/data construct.
