# Active Projects

`active/` 只保存尚未 terminal 的具体项目，**目录存在不等于模型调用授权**。

当前：

- [`003_diagnostic_counterevidence_revision/`](003_diagnostic_counterevidence_revision/) — legacy pre-candidate
- [`007_weak_evidence_backfire/`](007_weak_evidence_backfire/) — legacy registered / current frozen contract authorized
- [`013_publicness_coordination_dissociation/`](013_publicness_coordination_dissociation/) — legacy HOLD-D0
- [`014_alias_entrainment_transfer/`](014_alias_entrainment_transfer/) — **`KEEP / HOLD-FOR-CONSTRUCT-VALIDATION`**。phase 1–3 已跑完且 phenotype 稳固（audit-clean ∧ opaque_strict：+2.06/+1.31/+2.25 nats，三家族 CI 均不含 0），但 2026-08-29 的 150 对别名审计发现 D0 construct 有洞（compositional 39%，真正同指仅 33%，5% 完全不同指），且 `ALIAS > SEMREL` 排除不了 pair-specific learned association。因此 entity 解释**尚未成立**，`mechanism_B` 更正为 shared upstream cause。phase 4 被 `configs/contract_d1.yaml` 阻塞：需先做 RedirectQA 独立 bank + `ASSOC` 对照，判据 `ALIAS > ASSOC`。

当前研究队列统一看 [`../phenomenon_miner/CURRENT_TOPICS.md`](../phenomenon_miner/CURRENT_TOPICS.md)；模型调用授权只看 [`../phenomenon_miner/AUDIT_REGISTRY.md`](../phenomenon_miner/AUDIT_REGISTRY.md)。

具体 scientific contract、D0、result lineage 与下一步只在各 project README / audit 中维护。
