# Active Interpretability Projects

这个目录只放**已经过纸面 collision audit，值得进入 D0 / 行为 G0 实现阶段的题目**。

编号纪律：`active/NNN_*` 按进入 active 的时间顺序递增；**不复用 candidate shortlist 编号，也不与 `archive/` 中历史编号建立一一对应关系。**

进入 `active/` 只表示项目已被选中做正式 D0 / 验证实现，**不等于 `READY-TO-SMOKE`**。模型运行授权仍只看 `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`：必须同时具备 independent N0、D0 和 `validation_authorized: true`。

纪律：

1. 先复用公开数据 / 原作者公开实验；
2. 第一枪只验证自然现象是否真实、稳定、规模足够；
3. 行为 G0 未通过，不做 probe / SAE / attention sweep / activation patching；
4. 不通过换弱模型、主动制造 failure、缩窄到少数特例来续命；
5. 通过 G0 后，才把状态从 `ACTIVE-PREFLIGHT` 升到 `ACTIVE-MECHANISM`。

当前项目：

- `003_diagnostic_counterevidence_revision/` — 使用 MedEinst 的公开 control/trap 成对数据，研究少量决定性反证出现后，模型的诊断修正究竟失败在证据感知、证据—先验仲裁，还是晚期输出回退。当前只保留研究计划，尚未开始 G0 代码。
- `004_packed_unpacked_event_splitting/` — 对应 2026-08-28 canonical shortlist **#2 Packed–Unpacked Event Splitting**。已冻结 extensionality recognition gate、packed/paraphrase/strict-subset/repacking controls、branch-count signature、概率与 consequential decision 双 readout，以及跨模型汇总代码。状态：`ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`。
- `005_inadmissible_evidence_persistence/` — 对应 2026-08-28 canonical shortlist **#5 Inadmissible-Evidence Persistence**。已冻结 `never_seen / admitted / struck` counterfactual、admissibility/scope/polarity gate、bidirectional evidence polarity、neutral-struck artifact control 与 undo-ratio 指标。状态：`ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`。
- `006_existential_witness_collapse/` — 对应 2026-08-28 canonical shortlist **#4 Existential Witness Collapse**。先用 `exists P / exists Q / shared-witness-not-entailed / identity-underdetermined` 四项 recognition gate 验收局部量词理解，再测 identity-unknown 的 downstream single-witness join；同时冻结 natural paraphrase、explicit-same、explicit-distinct、neutral-context 与 relation-reminder controls。状态：`ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`。
- `007_weak_evidence_backfire/` — 对应 2026-08-28 canonical shortlist **#10 Weak-Evidence Backfire**。冻结 target/other 双向 evidence polarity、support/likelihood recognition、strong-evidence capability、no-evidence matched baseline、pragmatic-completeness、matched-length、neutral mention，以及 belief + consequential action 双 readout；正式 phenotype 必须是正证据的双向 sign reversal，而非“weak”词义或缺失强证据暗示。状态：`ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`。

历史旧 006–008 候选的 paper search、入选理由与同轮 kill 记录见：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已归档：

- `002_facts_vs_shortcuts_arbitration/` — 由于近期工作已强覆盖实体数值表示、比较机制与 shortcut/事实竞争相关叙事，停止 active 推进，完整移入 `archive/` 保存失败经验与代码。
- `003_decoy_dissociation/` — Qwen3-8B 与 Gemma3-12B-IT 完成冻结 G0；Gemma strong-reversal rate 仅 1.70%（门槛 5%），Qwen3-8B 为 0%，不满足晋级规则，已 KILLED / ARCHIVED。
- `004_deontic_facilitation/` — 修正后的 24 排列全反平衡 G0 中，Qwen3-8B 与 Gemma3-12B-IT 均为 `0/32` strong pairs，两模型均未达冻结 gate，已 KILLED / ARCHIVED。
- `005_anti_inference_discount/` — outcome-symmetric G0 中，Qwen3-8B 的 natural discount 仅 `0.01343`，Gemma3-12B-IT 仅 `8.1e-7`，两者 bridged effect 均近乎为零，已 KILLED / ARCHIVED。
- `006_bayesian_latent_inference_use_gap/` — custom-only 现象未跨模型成立，且宽叙事与 BayesBench 高度重叠；机制结果仅属于单一人工 bridge prompt，已停止并归档。
- `007_choice_supportive_ownership_bias/` — Qwen 与 Gemma 的 source-specificity 不一致，尚未在第二个公开任务上形成稳定共同 phenotype；本轮不再续救，按组合决策归档，不能记为已被严格证伪。
- `008_reliability_weighted_cue_integration/` — 当前自构造 G0 存在显式文本 mean 对隐式视觉 mean 的 access/copy confound，且 optimal multimodal cue-combination 母题已被公开 BayesBench 系统覆盖，已停止并归档。
