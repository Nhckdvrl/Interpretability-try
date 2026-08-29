# Archive Index

`archive/` 保存已经停止的研究项目。归档的目的不是清理掉失败，而是保留：**为什么停止、在哪个 contract 上停止、原始证据是什么、以后为什么不能仅靠换名复活。**

## 当前目录

| path | topic |
|---|---|
| `001_role_value_binding/` | Role–Value Binding |
| `002_facts_vs_shortcuts_arbitration/` | Facts vs Shortcuts Arbitration |
| `003_decoy_dissociation/` | Decoy Dissociation |
| `004_deontic_facilitation/` | Deontic Facilitation |
| `005_anti_inference_discount/` | Anti-Inference Discount |
| `006_bayesian_latent_inference_use_gap/` | Bayesian Latent Inference–Use Gap |
| `007_choice_supportive_ownership_bias/` | Choice-Supportive Ownership Bias |
| `008_reliability_weighted_cue_integration/` | Reliability-Weighted Cue Integration |
| `009_packed_unpacked_event_splitting/` | Packed–Unpacked Event Splitting |
| `010_inadmissible_evidence_persistence/` | Inadmissible-Evidence Persistence |
| `011_existential_witness_collapse/` | Existential Witness Collapse |
| `012_source_discount_recovery/` | Source-Discount Recovery |

每个项目的具体 terminal reason 以其 README / FINAL_VERDICT / result audit 为准，不从目录名猜。

## 最近两个重要终局

### 011 — Existential Witness Collapse

已由真实 behavioral validation 终止。当前 registry 将 canonical shortlist #4 指向该 archive；不得因为重新包装 existential / witness / join 语言而复活。

### 012 — Source-Discount Recovery

`D0-PASS`，108 条 NetEaseCrowd source pairs，20/20 manual audit。r2 的 credibility yes/no probe 被判 instrumentation artifact；r3 只修这一 probe 后完整重跑。终局反事实审计直接 grant memory gate，Qwen3-8B 与 Gemma3-12B-IT 仍都是 `0/108` weighting-capable pairs（冻结要求 20），主 blocker 是 `belief_initial_gap`。最终状态：`HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`。

详见 [`012_source_discount_recovery/FINAL_VERDICT.md`](012_source_discount_recovery/FINAL_VERDICT.md)。

## Legacy 编号重复

早期仓库在“active ID 不复用”规则冻结之前，已经出现过编号重复。例如 archive 中的 `007_choice_supportive_ownership_bias` 与当前 active 的 `007_weak_evidence_backfire` **不是同一个项目**。

因此：

- 不要用数字前缀单独引用项目；
- 写完整目录名；
- canonical shortlist 映射以 `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md` 为准；
- 新项目继续使用新的历史 active 编号，不再复用旧号。

## Archive 与 rejected_candidates 的区别

- `archive/`：曾进入较正式验证流程、已有明确 STOP/HOLD/KILL evidence chain 的项目；
- `rejected_candidates/`：更早期的 rejected idea / brainstorming / postmortem 历史材料。

新的 terminal project 应优先进入 `archive/`，并在这里加一行索引；不要再把正式终局散落到 `rejected_candidates/`。