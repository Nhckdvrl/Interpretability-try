# Archive Index

`archive/` 保存已经停止的正式研究项目及其完整复现/裁决证据。为什么这些题不能继续的跨项目规则统一看 [`../phenomenon_miner/FINDING_RULES.md`](../phenomenon_miner/FINDING_RULES.md) 与 [`../phenomenon_miner/FAILED_TOPICS.md`](../phenomenon_miner/FAILED_TOPICS.md)；具体数字仍以各项目 README / PROGRESS / results 为准。

| path | topic | terminal / archive reason |
|---|---|---|
| `001_role_value_binding/` | Role–Value Binding | no natural strict binding failure |
| `002_facts_vs_shortcuts_arbitration/` | Facts vs Shortcuts Arbitration | mother/mechanism follow-up rather than new phenotype |
| `003_decoy_dissociation/` | Decoy Dissociation | preregistered reversal phenotype did not replicate across families |
| `004_deontic_facilitation/` | Deontic Facilitation | matched Wason modality effect failed |
| `005_anti_inference_discount/` | Anti-Inference Discount | bridged residual approximately zero |
| `006_bayesian_latent_inference_use_gap/` | Bayesian Latent Inference–Use Gap | custom/interface artifact + collision |
| `007_choice_supportive_ownership_bias/` | Choice-Supportive Ownership Bias | different model families showed different phenomena |
| `007_weak_evidence_backfire/` | Weak-Evidence Backfire | terminal smoke hard kill |
| `008_reliability_weighted_cue_integration/` | Reliability-Weighted Cue Integration | modality/readout artifact + crowded mother |
| `009_packed_unpacked_event_splitting/` | Packed–Unpacked Event Splitting | structural controls did not support splitting account |
| `010_inadmissible_evidence_persistence/` | Inadmissible-Evidence Persistence | natural D0 source/gold could not be frozen |
| `011_existential_witness_collapse/` | Existential Witness Collapse | clean capability-gated null |
| `012_source_discount_recovery/` | Source-Discount Recovery | downstream weighting capability floor |
| `015_clarification_resolution_lag/` | Clarification Resolution Lag | matched neutral history explains apparent lag |
| `016_mixed_status_event_attraction/` | Mixed-Status Event Attraction | matched same-status context explains shift |
| `017_cross_modal_resolution_inertia/` | Cross-Modal Resolution Inertia | effect not interpretation-specific |
| `019_abstention_hysteresis/` | Abstention Hysteresis | neutral history explains most recovery |
| `020_incremental_clue_backfire/` | Incremental Clue Backfire | internal scientific-object collision |
| `021_task_switch_carryover/` | Task-Switch Carryover | mechanism-shaped subproblem, not independent object |
| `022_local_success_global_composition_failure/` | Local Success, Global Composition Failure | core object already known compositionality gap |
| `029_etr_human_like_fallacy/` | Human-Like Fallacies / ETR mechanism | **ARCHIVE-SCALE + PROVENANCE**: ETR/PyETR defines nearly the whole question; without ETR the claim is generic, with it the extension is narrow; exact 383 final manifest unavailable |
| `030_spatial_reference_frame_transformation/` | Spatial Reference-Frame Transformation | **ARCHIVE-TARGET-MISMATCH**: scientifically plausible, but VLM and outside next LLM-only search; no terminal scientific claim |
| `031_spontaneous_deception_knowledge_action/` | Spontaneous Deception → Within-Run Graph State | **TERMINAL F8 + V3 measurement gate**: best held-out invariant reachability AUROC ~0.53, 0 passing layers; headline object also drifted across failed gates |
| `032_temporal_forgetting_mechanism/` | Temporal Forgetting Mechanism | **ARCHIVE-SCALE**: extension mostly asks which stage/circuit explains an already-owned mother phenomenon; hypotheses are largely localization taxonomy rather than an independent scientific debate |
| `033_contextual_entrainment_opposite_scaling/` | Opposite-Scaling Contextual Entrainment | **ARCHIVE-DELTA-WIDTH + DATA**: ACL'25 Outstanding owns generic entrainment mechanism; ACL'26 mother already frames semantic filtering vs mechanical copying; proposed writer/gate decomposition is too close to mother future work; item-level mother data unavailable |

## 2026-08-31 PAPER-SCALE cleanup

The previous 029–033 `5/5 PASS` slate was revoked after 031 exposed a selection-protocol failure. All five directories were physically moved from `active/` to `archive/` in commit `e9c522e9f078f1968d6567386736584de0efef34`.

This cleanup is intentionally stricter than ordinary experimental failure:

- 031 is a true terminal experiment + topic-scale failure;
- 029/032/033 are **preemptively stopped before more compute** because the novelty/scope delta is not wide enough under the new bar;
- 030 is preserved as a scientifically plausible VLM idea but removed from the current LLM target.

The canonical new rule is F8 `Topic-scale / benchmark-dependence failure` in [`FINDING_RULES.md`](../phenomenon_miner/FINDING_RULES.md).

## Earlier Natural-Question cleanup

After adopting the first Hamdi-style gate, stale/weak entries such as 007/020/021/022 were physically removed from active rather than protected by sunk cost. The 2026-08-31 PAPER-SCALE cleanup applies the same discipline one level earlier: **a runnable mechanism experiment is not enough; the question itself must already have normal conference-paper scope.**

`014_alias_entrainment_transfer` remains active because it already has established results and is in paper development; it is not part of the fresh topic-search slate.
