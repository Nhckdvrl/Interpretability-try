# Audit Registry — Model Dispatch

版本：2026-08-30  
状态：`AUTHORITATIVE MODEL-CALL AUTHORIZATION / SCREENING-SEPARATED-FROM-VALIDATION`

本文件现在明确区分两类 model call：

```text
D0 SCREENING
  便宜、behavior-first、用于快速证伪现象。
  可以在 source data materialize + builder sanity 后运行。

FULL VALIDATION / MECHANISM
  用于正式 generality / causal / mechanistic claim。
  仍要求完整 N0/N1/D0/scope/frozen-contract gate。
```

2026-08-30 项目所有者明确要求把当前 Top-10 全部注册进 `active/` 并实际跑。因此，旧的“完成全部 discovery gate 之前连 cheap smoke 都不能调用模型”规则被收紧为：**禁止提前做机制，但允许 owner-approved D0 screening。**

当前：

```yaml
owner_approved_top10_d0_screening: 9   # new projects 015-023 excluding existing 014
full_validation_authorized: 0
mechanism_authorized_new_projects: 0
alias_014_next_d1_authorized: false
```

---

## 1. Top-10 D0 screening dispatch

| project | D0 screening | full validation / MI | pre-run condition |
|---|---:|---:|---|
| `active/015_clarification_resolution_lag` | **true** | false | materialize CondAmbigQA pairs; hard source answer mapping; matched-history control |
| `active/016_mixed_status_event_attraction` | **true** | false | run MAVEN-FACT builder; source/scope audit; freeze factuality verbalization |
| `active/017_cross_modal_resolution_inertia` | **true** | false | obtain MUCAR labels; simultaneous capability gate; identical image preprocessing |
| `active/018_stock_flow_correlation_intrusion` | **true** | false | run ResOpsUS builder; accounting closure/unit sanity |
| `active/019_abstention_hysteresis` | **true** | false | build source-provenance full/ablated/restored triples; no human answerability labels |
| `active/020_incremental_clue_backfire` | **true, after internal collision check** | false | verify archive does not already hard-kill same scientific object; source clue/gold aliases |
| `active/021_task_switch_carryover` | **true, diagnostic only** | false | first reproduce mother effect; do not claim novelty without hard old-rule wrong destination |
| `active/022_local_success_global_composition_failure` | **true, collision-first** | false | read Press et al. exact experimental conditions; run only the stronger externalized-facts contrast |
| `active/023_description_experience_gap` | **true** | false | deterministic exact-frequency generator; frequency/EV capability probes |
| `active/014_alias_entrainment_transfer` | historical phases completed; **new D1 false** | false | materialize r4 broad RedirectQA + ASSOC_ANY + scope/attrition/source audit + SHA |

**Meaning of `D0 screening = true`:** 允许 README 中已经预定义的便宜 behavioral smoke。它不是 PASS，也不能因为出现一个好数字就直接开始 probe/head ablation。

---

## 2. Full-validation promotion rule

任一新项目只有完成以下条件，才可把 `full_validation` 改成 true：

```yaml
external_behavioral_phenotype: PASS
n1_exact_collision_review: PASS
source_population_defined: PASS
hard_or_deterministic_gold: PASS
scope_integrity: PASS
fatal_controls: PASS
frozen_dataset_or_generator_sha: RECORDED
frozen_behavioral_contract: RECORDED
```

如果 mother paper 已经直接做了 headline behavior（尤其 021 / 022），还额外要求：

```yaml
novel_behavioral_signature_beyond_mother: PASS
```

否则只能路由成 `MECH-FOLLOWUP`。

---

## 3. Project-specific stop rules

### 015 Clarification Resolution Lag

必须比较 final evidence 相同的 DIRECT vs prior-ambiguity HISTORY；普通“给 condition 会变好/变差”不算。

2026-08-30 D0 v1：400 CondAmbigQA pairs、Qwen3-8B、Gemma-3-12B-IT 与
Llama-3.1-8B-Instruct 已完成。三个家族的 neutral matched-history effect 与
ambiguity-history effect 同量级，关键 `MATCHED_HISTORY - AMBIGUITY_HISTORY` 的 95%
question-cluster bootstrap CI 均跨 0。
判定 `NO-PROMOTE / MATCHED-HISTORY FATAL CONTROL NOT PASSED`；full validation 与
mechanism 继续为 false，不按 subtype 收窄续跑。

### 016 Mixed-Status Event Attraction

必须出现 toward-neighbor-status 的 directional error；只有 context 变长后 accuracy 下降不算。

2026-08-30 D0 v1：MAVEN-FACT train + validation 全 scope bank 与 576-pair direction-balanced
cost layer 已冻结；Qwen3-8B、Gemma-3-12B-IT、Llama-3.1-8B-Instruct 均完成。表面
`MIXED - LOCAL` 效应被 same-status matched context 解释，关键 `MIXED - SAME` 主顺序
document-bootstrap CI 三家族均跨 0，toward-neighbor 离散转移不稳定。判定
`NO-PROMOTE / SAME-STATUS FATAL CONTROL NOT PASSED`；full validation 与 mechanism 为
false，不按 `PS+ -> CT+` 或其他单方向收窄续跑。

### 017 Cross-Modal Resolution Inertia

MUCAR 已经证明 static cross-modal ambiguity resolution 很难。只有 `simultaneous correct + text-first initial wrong + sequential final sticks to old interpretation` 才是新 money cell。

### 018 Stock–Flow Correlation Intrusion

只有在 net-flow 已答对后，stock 错误仍特别跟随 inflow，才解释为 correlation intrusion。

### 019 Abstention Hysteresis

只分析 `initial missing -> abstain` 且 `direct full -> correct` 的 items；安全 refusal 不混进 epistemic abstention。

### 020 Incremental Clue Backfire

先查内部失败库；不能把旧 Evidence-Induced Referent Displacement 换 Quiz Bowl 数据重新注册。如果 archive 覆盖同一 scientific object，立即 route/kill。

### 021 Task-Switch Carryover

Gupta et al. EMNLP 2024 已证明 task-switch interference。只有错误显著朝 old-rule hard prediction 移动，才有新 phenotype。

### 022 Local/Global Composition

Press et al. 2023 已定义 compositionality gap。只有 correct intermediate facts 已经显式存在于同一 context 后仍 final-compose wrong，才值得继续。

### 023 Description–Experience Gap

主分析必须 exact-frequency match，且 frequency / expected-value probe 正确；否则只是 counting/recency failure。

---

## 4. Existing provenance projects

### `active/007_weak_evidence_backfire`

```yaml
terminal_verdict: HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR
screening_authorized: false
full_validation_authorized: false
mechanism_authorized: false
```

禁止换模型、阈值、subset、prompt、readout 复活。

### `active/013_publicness_coordination_dissociation`

```yaml
status: PARKED-HOLD-DATA
screening_authorized: false
reason: insufficient independent natural scenarios under clean source/license path
```

### `active/014_alias_entrainment_transfer`

历史 phase 1–3 保留有效 provenance。当前可支持的是 cross-surface learned-relation transfer / shared upstream cause，**不是已证明 entity-level salience**。

Canonical next contract: `active/014_alias_entrainment_transfer/configs/contract_d1_r4.yaml`

任何新 D1 call 前：

- materialize broad r4 raw bank；
- materialize ASSOC_ANY matched control；
- source-population audit；
- ASSOC/control audit；
- scope/attrition summary；
- 检查 Q2 hard-reference stratum 能否不靠 convenience narrowing 达到 preregistered floor；
- freeze/record dataset SHA。

做不到就 drop entity/reference claim，不用 mechanism 救 construct。

---

## 5. Discipline

- `active/` = 值得实际跑，不等于论文 claim 成立。
- D0 smoke 是为了**快速 kill**，不是为了找最漂亮 subset。
- README 里的 fatal controls 必须在看正式结果前固定。
- source factor 默认 factor-not-filter。
- 能 exact / deterministic score 就不用 LLM judge。
- mechanism evidence 永远不能救一个失败的 behavioral/data construct。
