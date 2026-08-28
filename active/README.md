# Active Interpretability Projects

`active/NNN_*` 按历史进入 active 的顺序递增；归档后的编号仍不复用。进入 `active/` 不等于可运行，唯一模型调用授权看 `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`。

当前与本轮现象发现相关：

- `007_weak_evidence_backfire/` — **N0-PASS / D0-PASS / READY-TO-SMOKE**。25 条 UCI natural D0（Breast Cancer Wisconsin Diagnostic + Wine），20/20 人工审计通过；harness r5 已允许真实 finite-data neutral cue，且 calibration/held-out 两边都必须近似 non-diagnostic。
- `012_source_discount_recovery/` — **N0-PASS / D0-AUDITING / NOT READY-TO-SMOKE**。NetEaseCrowd/CIFAR-10H source pool 已审计，worker-LR builder 已提交，但尚未 materialize 并人工签署 20+ frozen scenarios。
- `013_publicness_coordination_dissociation/` — **N0-PASS / HOLD-D0 / NOT READY-TO-SMOKE**。找到强 human common-knowledge coordination anchor，但独立 natural scenarios 数量与可适配 license 仍不足，禁止 synthetic 扩写。
- `003_diagnostic_counterevidence_revision/` — 已报告 failure 的 mechanism-followup，不属于本轮新自然现象 discovery shortlist。

重要流程澄清：本项目允许从已知人类/自然现象出发研究 LLM failure；人类母现象已知本身不是 LLM collision。详见 `phenomenon_miner/PROCESS.md`。007/012 的 2026-08-29 duplicate independent-N0 KILL 记录保留作历史 provenance，但已由各自 `N0_RESOLUTION_2026-08-29.md` 和权威注册表 supersede。

行为 G0 未通过前不做 probe / SAE / attention sweep / activation patching；通过后仍必须先做 raw-case 审计和 N1。
