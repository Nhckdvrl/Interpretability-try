# Active Interpretability Projects

这个目录只放**已经过纸面 collision audit，值得实际运行行为 G0 的题目**。

纪律：

1. 先复用公开数据 / 原作者公开实验；
2. 第一枪只验证自然现象是否真实、稳定、规模足够；
3. 行为 G0 未通过，不做 probe / SAE / attention sweep / activation patching；
4. 不通过换弱模型、主动制造 failure、缩窄到少数特例来续命；
5. 通过 G0 后，才把状态从 `PRE-CANDIDATE` 升到 `ACTIVE-MECHANISM`。

当前项目：

- `003_diagnostic_counterevidence_revision/` — 使用 MedEinst 的公开 control/trap 成对数据，研究少量决定性反证出现后，模型的诊断修正究竟失败在证据感知、证据—先验仲裁，还是晚期输出回退。当前只保留研究计划，尚未开始 G0 代码。

006–008 的 paper search、入选理由与同轮 kill 记录见：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已归档：

- `002_facts_vs_shortcuts_arbitration/` — 由于近期工作已强覆盖实体数值表示、比较机制与 shortcut/事实竞争相关叙事，停止 active 推进，完整移入 `archive/` 保存失败经验与代码。
- `003_decoy_dissociation/` — Qwen3-8B 与 Gemma3-12B-IT 完成冻结 G0；Gemma strong-reversal rate 仅 1.70%（门槛 5%），Qwen3-8B 为 0%，不满足晋级规则，已 KILLED / ARCHIVED。
- `004_deontic_facilitation/` — 修正后的 24 排列全反平衡 G0 中，Qwen3-8B 与 Gemma3-12B-IT 均为 `0/32` strong pairs，两模型均未达冻结 gate，已 KILLED / ARCHIVED。
- `005_anti_inference_discount/` — outcome-symmetric G0 中，Qwen3-8B 的 natural discount 仅 `0.01343`，Gemma3-12B-IT 仅 `8.1e-7`，两者 bridged effect 均近乎为零，已 KILLED / ARCHIVED。
- `006_bayesian_latent_inference_use_gap/` — custom-only 现象未跨模型成立，且宽叙事与 BayesBench 高度重叠；机制结果仅属于单一人工 bridge prompt，已停止并归档。
- `007_choice_supportive_ownership_bias/` — Qwen 与 Gemma 的 source-specificity 不一致，尚未在第二个公开任务上形成稳定共同 phenotype；本轮不再续救，按组合决策归档，不能记为已被严格证伪。
- `008_reliability_weighted_cue_integration/` — 当前自构造 G0 存在显式文本 mean 对隐式视觉 mean 的 access/copy confound，且 optimal multimodal cue-combination 母题已被公开 BayesBench 系统覆盖，已停止并归档。
