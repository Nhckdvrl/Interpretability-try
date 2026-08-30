# Active Projects

`active/` 保存具体研究项目的 README、数据合同、代码、结果与审计 provenance。

**2026-08-30 owner decision:** 当前 Top-10 全部注册进 `active/`，用于快速 D0 behavioral screening。这里的“active”表示**值得实际动手跑**，不表示已经证明 novelty / phenomenon，也不表示可以跳过数据审计直接做 mechanism。

为了避免以前“目录存在 = 已晋级 = 随便跑”的混乱，现在区分两层：

```text
D0 SCREENING
  允许：materialize source data -> builder sanity -> cheap behavioral smoke
  目的：尽快看现象有没有

FULL VALIDATION / MECHANISM
  仍要求：phenotype + source scope + hard gold + N1 collision closure + frozen contract
```

模型授权状态的最终记录仍看 [`../phenomenon_miner/AUDIT_REGISTRY.md`](../phenomenon_miner/AUDIT_REGISTRY.md)。

---

## 2026-08-30 Top-10 screening slate

| rank | project | 一句话问题 | data shape | 当前风险 |
|---:|---|---|---|---|
| 1 | [`015_clarification_resolution_lag`](015_clarification_resolution_lag/) | 歧义已经解释清楚，模型会不会还停在旧的 ambiguous state？ | CondAmbigQA-2K / PRACTIQ，可程序构造 paired history | novelty 要与 static clarification benchmarks 区分 |
| 2 | [`016_mixed_status_event_attraction`](016_mixed_status_event_attraction/) | 两个 event 单独 factuality 都会，放一起会不会互相带偏？ | MAVEN-FACT source labels，自动 same-document pairing | 必须排除合法 discourse evidence |
| 3 | [`014_alias_entrainment_transfer`](014_alias_entrainment_transfer/) | 看见一个实体名字，会不会把没出现过的 alias 也 entrain？ | phenotype 已成立；RedirectQA + ASSOC construct validation | entity/reference claim 尚未成立 |
| 4 | [`017_cross_modal_resolution_inertia`](017_cross_modal_resolution_inertia/) | 文字先形成旧解释，晚到的图片能不能真正把它改掉？ | MUCAR dual-ambiguity，可自动 sequentialize | static MUCAR failure 已不是 novelty |
| 5 | [`018_stock_flow_correlation_intrusion`](018_stock_flow_correlation_intrusion/) | net flow 算对后，stock 判断还会不会追着 inflow 走？ | ResOpsUS real time series，程序切窗口 | accounting closure / unit sanity |
| 6 | [`019_abstention_hysteresis`](019_abstention_hysteresis/) | 先拒答一次后，证据补齐了还会不会继续拒答？ | supporting-fact QA / AbstentionBench，可自动 ablate+restore | 2026 abstention 文献很近 |
| 7 | [`020_incremental_clue_backfire`](020_incremental_clue_backfire/) | 已经答对后，再加真实同答案 clue 会不会反而改错？ | Quiz Bowl ordered clues，自动 prefix sweep | 必须查内部旧题 collision |
| 8 | [`021_task_switch_carryover`](021_task_switch_carryover/) | 换任务后犯的错是不是还在执行旧规则？ | mother repo + natural multi-attribute source 待定 | aggregate task-switch interference 已被 EMNLP 2024 做过 |
| 9 | [`022_local_success_global_composition_failure`](022_local_success_global_composition_failure/) | 正确中间答案都摆在上下文里了，最后还会不会组合错？ | MuSiQue / 2Wiki decomposition | compositionality gap 已被 Press et al. 2023 做过 |
| 10 | [`023_description_experience_gap`](023_description_experience_gap/) | 同一 gamble 写成概率或展开成等价历史，选择会不会不同？ | deterministic exact-frequency generator | 2026 risk-choice literature 更新快 |

每个 README 都包含：研究问题、最相邻工作、novelty 边界、数据来源、自动 D0 构造、capability gates、fatal controls、PROMOTE/KILL 和 mechanistic follow-up。

---

## 旧 active / provenance 项目

- [`003_diagnostic_counterevidence_revision/`](003_diagnostic_counterevidence_revision/) — legacy pre-candidate，保留 provenance。
- [`007_weak_evidence_backfire/`](007_weak_evidence_backfire/) — **TERMINAL HARD KILL**；目录只保留 code/raw results/audit，不允许换阈值、模型、subset 复活。
- [`013_publicness_coordination_dissociation/`](013_publicness_coordination_dissociation/) — **PARKED / HOLD-DATA**；natural independent scenario source 不足。

---

## 014 特殊说明

[`014_alias_entrainment_transfer/`](014_alias_entrainment_transfer/) 已经不是一个“先跑 D0 看有没有现象”的新题：

- broad cross-surface transfer 已在多家族稳定存在；
- 旧 D0 的 entity/reference interpretation 被 150-pair audit 与 UNREL bug 推翻；
- 当前可支持的是 **learned cross-surface relation transfer / shared upstream cause**；
- 下一步是 r4 broad RedirectQA + `ASSOC_ANY` construct validation；
- r4 已于 2026-08-30 完成；broad transfer 通过，reference-specific Q2 未通过。

014 自己的 README 很长，包含历史 phase 1–3 细节；**最新授权以 AUDIT_REGISTRY 与 r4 contract 为准，若旧 README 中有历史授权措辞，以新 registry 覆盖。**

---

## 运行纪律

### 可以做

- 下载公开 source dataset；
- 写 deterministic builder；
- 自动生成 paired conditions / windows / prefixes；
- 做 schema、license、source-provenance 检查；
- 随机抽 20 条检查 builder 没写歪；
- 在 README 已定义的 hard scoring 下跑便宜 D0 smoke；
- null 就 kill，不救。

### 不可以做

- 人工挑 50 条“最容易出效应”的样本；
- 看结果后换 gold / threshold / prompt 定义；
- 为了显著把 domain/type/direction 大量过滤掉；
- D0 没有清楚 phenotype 就开始 probe / patch / head ablation；
- 把 mother paper 已经建立的行为重新包装成 novelty；
- 用 LLM judge 代替本来可以 exact/deterministic score 的 gold。

---

## 当前建议的实际跑序

按“数据可以最快自动 materialize + novelty 尚有空间”排序：

```text
015 Clarification Resolution Lag
016 Mixed-Status Event Attraction
019 Abstention Hysteresis
020 Incremental Clue Backfire   (先过内部 collision)
018 Stock-Flow Correlation Intrusion
017 Cross-Modal Resolution Inertia
023 Description-Experience Gap
021 Task-Switch Carryover        (先找 natural old-rule oracle)
022 Local/Global Composition     (先核 Press exact collision)
014 Alias                        (独立走 r4 construct validation)
```

这里排序是**实验效率**，不是论文价值最终排序。

### 最新 screening 结果

- `015 Clarification Resolution Lag`：2026-08-30 D0 v1 已完成 Qwen3-8B、
  Gemma-3-12B-IT 与 Llama-3.1-8B-Instruct。`DIRECT - AMBIGUITY_HISTORY` 的小差值
  被 neutral `MATCHED_HISTORY` 解释，关键 `MATCHED - AMBIGUITY` 在三个家族 CI
  均跨 0；当前
  **NO-PROMOTE**，不进入机制实验。详见项目内 `D0_V1_REPORT.md`。
- `016 Mixed-Status Event Attraction`：2026-08-30 D0 v1 已完成 MAVEN-FACT 全 scope
  materialization 与 Qwen3-8B、Gemma-3-12B-IT、Llama-3.1-8B-Instruct。三个家族虽然都
  出现 `MIXED - LOCAL` neighbor-label probability 上升，但同状态匹配 context 产生同量级
  变化；关键 `MIXED - SAME` 主顺序 CI 全部跨 0，离散 toward-neighbor transition 也不稳定。
  当前 **NO-PROMOTE / SAME-STATUS CONTROL NOT PASSED**，不按单方向收窄。详见项目内
  `D0_V1_REPORT.md`。
- `014 Alias Entrainment Transfer`：2026-08-30 D1 r4 已完成 broad RedirectQA +
  `ASSOC_ANY`、Wikipedia sentence cooccurrence 与三家族。Q1 broad 在双 frame、双方向和
  same-type sensitivity 全部强正；但 independent-gated `opaque_strict` 的 Q2 在三个家族均只
  F2 显著、F1 CI 跨 0，未通过预注册 both-frame 标准。最终
  **CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC**；保留 learned-relation spillover 与 lexical
  structure gradient，放弃 entity/reference-specific claim，不做 subset rescue。详见项目内
  `D1_R4_REPORT.md`。
