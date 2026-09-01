# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
fresh_register_target: 5
fresh_register_status: OPEN_AFTER_039_DEREGISTRATION
latest_registered_project: 038 unresolved reference representation architecture
latest_deregistered_project: 039 same kind vs go together semantic relation
required_protocol: PAPER-SCALE v2.1
current_target: hard-audit surviving register; then find one genuinely novel replacement without count-filling
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update, or rely on separate/static heuristics? |
| [`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE** | What makes a metaphor behave like comparison vs categorization: conventionality, aptness, or no discrete switch? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |

**当前 authoritative fresh register 是 4/5。** Count 不保护任何题；新 fatal novelty collision、substrate failure 或 frozen-contract failure 都必须立即 demote / archive。

## Deregistered 037

Former [`037_generic_generalization_licensing`](archive/037_generic_generalization_licensing/) is **KILL-NOVELTY / ARCHIVED**. Hu, van Paridon & Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language` (`arXiv:2607.04523`), directly tests the principled-vs-statistical generic-property distinction in language models while controlling prevalence and cue validity. Open-weight causal MI would be too close to behavior/factorization -> mechanism under N2.

Detailed record: [`rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md`](rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md).

## Deregistered 039 — taxonomic vs thematic semantic relation

Former [`039_same_kind_vs_go_together_semantic_relation`](archive/039_same_kind_vs_go_together_semantic_relation/) asked whether LLMs distinguish **same kind / taxonomic similarity** from **go together / thematic relatedness** as a reusable causally used semantic-relation state.

It is now **KILL-NOVELTY / ARCHIVED / GPU NOT AUTHORIZED** after a deeper N2 audit found that the scientific object is already substantially occupied:

- 2026 `Disentangling Similarity and Relatedness in Topic Models` explicitly factorizes taxonomic similarity vs thematic relatedness, uses the same Landrigan–Mirman 659-pair TxThmNorms substrate, evaluates language-model embeddings on both axes, and obtains both-axis judgments from modern LLMs including Qwen;
- CoNLL 2025 `Human-likeness of LLMs in the Mental Lexicon` studies Llama-3.1 semantic-relatedness representations and explicitly includes taxonomic/thematic relation families;
- 2026 cross-cultural-surrogate work directly tests LLaMA/Qwen on taxonomic–thematic forced choice and analyzes taxonomic versus thematic reasoning in model explanations.

Therefore the proposed delta had collapsed to roughly `existing LLM behavior/representation of the same axis -> stronger hidden-state steering/causal MI`, which fails v2.1 N2.

Detailed record: [`rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`](rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md).

## 当前 authority

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议，当前 v2.1**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前 authoritative handoff
3. 本 README — register 计数与入口

执行入口：[`active/README.md`](active/README.md)。失败证据见 [`rejected_candidates/`](rejected_candidates/)；撤销项目见 [`archive/`](archive/)。

## v2.1：严格不等于复杂

031/F8 的教训继续有效：benchmark-removal、N0/N1/N2、真实 substrate、story invariance、禁止 null 后换 headline 都不放松。

Route C 允许：

```text
简单、自然、令人意外的现象或语义属性
→ matched controls 去掉 obvious confound
→ strongest-neighbor novelty
→ accessible open model / data
→ minimal falsifiable causal-use question
→ mechanism 可以在执行中长出来
```

但 Route C **不允许**：

```text
已有工作已经拥有同一个 object / axis
→ 我们只是换 hidden-state probe / SAE / patching / steering
→ 宣称因为“还没人 causal”所以 novel
```

039 是这条边界的最新 canonical negative example。

### Simplicity sanity test

> **不用 LLM / benchmark / activation / SAE / mechanistic interpretability 这些词，能不能一句话把问题讲清楚？**

能讲清楚只是必要条件，不是充分条件；strongest neighbor 仍必须没有拥有同一 scientific object。

## 强论文尺度标尺

- ACL 2025 Outstanding `Llama See, Llama Do`：simple broad phenomenon → causal mechanism → mitigation。
- EMNLP 2025 Outstanding shared filler-gap：成熟理论问题 → causal LM evidence。
- NAACL 2025 taxonomy vs similarity：一个简单 competing axis 就能撑完整 paper。
- NAACL 2025 `Racing Thoughts`：一个强 unified hypothesis → causal validation。
- ACL 2026 Main `Do LLMs Know Tool Irrelevance?`：天然 semantic relevance vs structural match，controlled dataset 只负责解耦。

## 当前项目纪律

- **034 / 035 完全冻结。** 除非发现新的致命 novelty collision，不重审、不改 headline。
- **036 / 038 当前仍在 register，但必须接受这一轮同等级 hard re-audit。** 不因为过去写过 PASS 就保护。
- fresh search 的目标重新变成 **找到 1 个真正比 039 更安全的 replacement**，但必须先完成 surviving-register audit；不能为了恢复 5/5 草率升题。
- serious candidate 一旦 KILL，立即写 `rejected_candidates/`。

## 029–033 re-audit

- 029 — ARCHIVE / SCALE+PROVENANCE。
- 030 — ARCHIVE / VLM target mismatch。
- 031 — TERMINAL / V3 measurement + canonical F8 scope-drift lesson。
- 032 — ARCHIVE / mother-mechanization scale。
- 033 — ARCHIVE / N2 delta width + data gap。

## 仍保留的旧工作

- [`active/014_alias_entrainment_transfer`](active/014_alias_entrainment_transfer/)：已有正式结果，属于 paper development，不计入 fresh register。

## One-line discipline

> **Simple is good, but object reuse is not novelty. 先证明问题自然，再证明 strongest prior 没拥有这个 object，最后才谈 MI。当前状态诚实地是 4/5。**
