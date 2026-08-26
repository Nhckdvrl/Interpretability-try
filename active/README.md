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
- `004_deontic_facilitation/` — Wason 条件推理中的 deontic facilitation。主 G0 使用 same-content matched pairs，只改变 descriptive/deontic rule realization；另保留 EACL 2026 NeuBAROCO 官方数据作为外部复现。先验证现象，再决定是否进入 violation-search routing 机制。
- `005_anti_inference/` — direct vs inferred evidence discount。使用显式匹配 end-to-end reliability 的四领域程序化数据，并用独立理解门排除“模型根本没推出结论”的假阳性。

已归档：

- `002_facts_vs_shortcuts_arbitration/` — 由于近期工作已强覆盖实体数值表示、比较机制与 shortcut/事实竞争相关叙事，停止 active 推进，完整移入 `archive/` 保存失败经验与代码。
- `003_decoy_dissociation/` — Qwen3-8B 与 Gemma3-12B-IT 完成冻结 G0；Gemma strong-reversal rate 仅 1.70%（门槛 5%），Qwen3-8B 为 0%，不满足晋级规则。
