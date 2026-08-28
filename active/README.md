# Active Interpretability Projects

这个目录只放**已经过纸面 collision audit，值得进入 D0 / 行为 G0 实现阶段的题目**。

编号纪律：`active/NNN_*` 按进入 active 的时间顺序递增；**不复用 candidate shortlist 编号，也不与 `archive/` 中历史编号建立一一对应关系。** 历史上已经进入过 active、后来移入 archive 的编号仍视为已占用，因此本轮在 011 之后继续使用 012、013。

进入 `active/` 只表示项目已被选中做正式 D0 / 验证实现，**不等于 `READY-TO-SMOKE`**。模型运行授权仍只看 `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`：必须同时具备 independent N0、D0 和 `validation_authorized: true`。

纪律：

1. 先复用公开数据 / 原作者公开实验；
2. 第一枪只验证自然现象是否真实、稳定、规模足够；
3. 行为 G0 未通过，不做 probe / SAE / attention sweep / activation patching；
4. 不通过换弱模型、主动制造 failure、缩窄到少数特例来续命；
5. 通过 G0 后，才把状态从 `ACTIVE-PREFLIGHT` 升到 `ACTIVE-MECHANISM`。

当前项目：

- `003_diagnostic_counterevidence_revision/` — 使用 MedEinst 的公开 control/trap 成对数据，研究少量决定性反证出现后，模型的诊断修正究竟失败在证据感知、证据—先验仲裁，还是晚期输出回退。它是已有 failure 的 mechanism-followup，不属于本轮新自然现象 discovery shortlist。
- `007_weak_evidence_backfire/` — 对应 2026-08-28 canonical shortlist **#10 Weak-Evidence Backfire**。冻结 bidirectional positive-evidence sign reversal、真正无 case-specific observation 的 baseline、support/likelihood/strong-evidence capability gates、pragmatic-completeness/length/neutral controls、scenario-level paired bootstrap 与 hard-kill 逻辑。状态：`ACTIVE-PREFLIGHT / HARNESS-READY-r4 / NOT READY-TO-SMOKE`。
- `012_source_discount_recovery/` — 对应 canonical shortlist **#9 Source-Discount Recovery**。验证 source identity / credibility / message memory 均保持时，source→message discount coupling 是否随距离恢复，并用 source-cue reinstatement 对 matched-length reminder 做选择性反证。方向 LR、短/长延迟 memory gate、same-delay no-message baseline、belief/action 双接口和 bidirectional scenario pairing 均冻结。状态：`ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`。
- `013_publicness_coordination_dissociation/` — 对应 canonical shortlist **#3 Publicness–Coordination Dissociation**。锁死 same proposition / recipients / first-order knowledge，先验收 publicness 与多层 recursive receipt knowledge，再比较 natural public event 与 explicit-common-knowledge bridge 对 coordination policy 的使用差异，并要求 participant symmetry、paraphrase 与 matched-length controls。状态：`ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`。

006/007 的历史 pre-merge 科学与实现审计见 [`VALIDATION_AUDIT_006_007.md`](VALIDATION_AUDIT_006_007.md)。本轮 007/012/013 的复核与新 harness 审计见 [`VALIDATION_AUDIT_007_012_013.md`](VALIDATION_AUDIT_007_012_013.md)。

已归档：

- `011_existential_witness_collapse/` — 原 active 006 / canonical shortlist #4。完成 independent N0、natural D0 和 two-family smoke 后，Qwen3-8B 在 40/40 capability-gated natural cases 上满足 `HARD-KILL-NO-ILLEGAL-JOIN`；已移入 `archive/011_existential_witness_collapse/`，不再进入 N1 或机制。
- `009_packed_unpacked_event_splitting/` — 当前 operationalization 的 5/5 scenario groups 均未通过 artifact controls；reorder 超差、repacking 不恢复、within-family branch-count slope 反向。状态：`HOLD-OPERATIONALIZATION-ARTIFACT`。
- `010_inadmissible_evidence_persistence/` — r5 修复 polarity/never-seen 并以 pair 为统计单位后，两模型 admitted capability 均为 12/12，但 neutral artifact fraction 为 0.75/0.833。状态：`TERMINAL-HOLD-D0V3-CONTRACT`。
- `002_facts_vs_shortcuts_arbitration/` — 由于近期工作已强覆盖实体数值表示、比较机制与 shortcut/事实竞争相关叙事，停止 active 推进，完整移入 `archive/` 保存失败经验与代码。
- `003_decoy_dissociation/` — Qwen3-8B 与 Gemma3-12B-IT 完成冻结 G0；Gemma strong-reversal rate 仅 1.70%（门槛 5%），Qwen3-8B 为 0%，不满足晋级规则，已 KILLED / ARCHIVED。
- `004_deontic_facilitation/` — 修正后的 24 排列全反平衡 G0 中，Qwen3-8B 与 Gemma3-12B-IT 均为 `0/32` strong pairs，两模型均未达冻结 gate，已 KILLED / ARCHIVED。
- `005_anti_inference_discount/` — outcome-symmetric G0 中，Qwen3-8B 的 natural discount 仅 `0.01343`，Gemma3-12B-IT 仅 `8.1e-7`，两者 bridged effect 均近乎为零，已 KILLED / ARCHIVED。
- `006_bayesian_latent_inference_use_gap/` — custom-only 现象未跨模型成立，且宽叙事与 BayesBench 高度重叠；机制结果仅属于单一人工 bridge prompt，已停止并归档。
- `007_choice_supportive_ownership_bias/` — Qwen 与 Gemma 的 source-specificity 不一致，尚未在第二个公开任务上形成稳定共同 phenotype；本轮不再续救，按组合决策归档，不能记为已被严格证伪。
- `008_reliability_weighted_cue_integration/` — 当前自构造 G0 存在显式文本 mean 对隐式视觉 mean 的 access/copy confound，且 optimal multimodal cue-combination 母题已被公开工作系统覆盖，已停止并归档。
