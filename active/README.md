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
- `006_bayesian_latent_inference_use_gap/` — `ACTIVE-MECHANISM`。Qwen2.5-14B 在 posterior-good cases 上有 33.3% natural policy-use error，显式 posterior bridge 后 14/14 全 rescue；研究 inference quality 与 routing quality 的解耦。
- `007_choice_supportive_ownership_bias/` — `ACTIVE-MECHANISM / REFRAMED`。可见旧答案稳定抑制 revision，但 source specificity 跨模型不同：Qwen own≠other，Gemma 对 own/other 都形成 anchor；转为比较 attribution-dependent commitment routing。
- `008_reliability_weighted_cue_integration/` — `ACTIVE-MECHANISM`。Qwen3-VL 几乎完全 text capture；Gemma3 虽随 reliability 调整仍系统性低估 image cue；两路 unimodal readout 均正常。

006–008 的 paper search、入选理由与同轮 kill 记录见：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已归档：

- `002_facts_vs_shortcuts_arbitration/` — 由于近期工作已强覆盖实体数值表示、比较机制与 shortcut/事实竞争相关叙事，停止 active 推进，完整移入 `archive/` 保存失败经验与代码。
- `003_decoy_dissociation/` — Qwen3-8B 与 Gemma3-12B-IT 完成冻结 G0；Gemma strong-reversal rate 仅 1.70%（门槛 5%），Qwen3-8B 为 0%，不满足晋级规则，已 KILLED / ARCHIVED。
- `004_deontic_facilitation/` — 修正后的 24 排列全反平衡 G0 中，Qwen3-8B 与 Gemma3-12B-IT 均为 `0/32` strong pairs，两模型均未达冻结 gate，已 KILLED / ARCHIVED。
- `005_anti_inference_discount/` — outcome-symmetric G0 中，Qwen3-8B 的 natural discount 仅 `0.01343`，Gemma3-12B-IT 仅 `8.1e-7`，两者 bridged effect 均近乎为零，已 KILLED / ARCHIVED。
