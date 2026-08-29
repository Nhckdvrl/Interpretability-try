# Active Interpretability Projects

`active/NNN_*` 按历史进入 active 的顺序递增；归档后的编号仍不复用。进入 `active/` 不等于可运行，唯一模型调用授权看 `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`。

当前与本轮现象发现相关：

- `007_weak_evidence_backfire/` — **N0-PASS / D0-PASS / READY-TO-SMOKE**。30 条 UCI natural D0（Breast Cancer Wisconsin Diagnostic + Wine），20/20 人工审计通过；harness r5 已允许真实 finite-data neutral cue，且 calibration/held-out 两边都必须近似 non-diagnostic。
- `012_source_discount_recovery/` — **N0-PASS / D0-AUDITING / NOT READY-TO-SMOKE**。NetEaseCrowd release 已下载、哈希并跑通 builder；69 与 126 已在 selection 前排除（后者因首轮人工审计 18/20 PASS、2 条 naturalness HOLD）。pair selection 已从 greedy 扫描升级为全局 matching（cell 内最大匹配，跨 cell 稀缺优先），在不放松任何门槛的前提下得到 108 条候选 scenario、216 个不重复 annotator，机械检查 108/108 通过。注意 capability 52 全库仅 28 个 annotator、53 少有 annotator 能过 2.0 分离，因此 45/4/14/45 已是该 target 下的上限形状，cluster 数固定为 12 个 cell。仍缺重抽的分层固定种子 20 条人工阅读，未签署。
- `013_publicness_coordination_dissociation/` — **N0-PASS / HOLD-D0 / NOT READY-TO-SMOKE**。找到强 human common-knowledge coordination anchor，但独立 natural scenarios 数量与可适配 license 仍不足，禁止 synthetic 扩写。
- `003_diagnostic_counterevidence_revision/` — 已报告 failure 的 mechanism-followup，不属于本轮新自然现象 discovery shortlist。

重要流程澄清：本项目允许从已知人类/自然现象出发研究 LLM failure；人类母现象已知本身不是 LLM collision。详见 `phenomenon_miner/PROCESS.md`。007/012 的 2026-08-29 duplicate independent-N0 KILL 记录保留作历史 provenance，但已由各自 `N0_RESOLUTION_2026-08-29.md` 和权威注册表 supersede。

行为 G0 未通过前不做 probe / SAE / attention sweep / activation patching；通过后仍必须先做 raw-case 审计和 N1。
