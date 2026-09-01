# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
fresh_register_target: 5
fresh_register_status: COMPLETE_AFTER_039_REGISTRATION
latest_registered_project: 039 same kind vs go together semantic relation
latest_deregistered_project: 037 generic generalization licensing
required_protocol: PAPER-SCALE v2.1
current_target: execute frozen S0/causal contracts; continue fatal-collision monitoring, but do not reopen frozen headlines without new evidence
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update, or rely on separate/static heuristics? |
| [`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED** | What makes a metaphor behave like comparison vs categorization: conventionality, aptness, or no discrete switch? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |
| [`039_same_kind_vs_go_together_semantic_relation`](active/039_same_kind_vs_go_together_semantic_relation/) | **PASS-REGISTER / GPU AUTHORIZED** | When two concepts are related, does the model distinguish **same kind** from **go together in an event/scenario** as a causally usable relation type? |

**当前 authoritative fresh register 是 5/5。** Count 仍然不是保护规则：任何项目如果出现新的 fatal novelty collision、substrate failure 或 frozen-contract falsifier，仍应立即 demote / archive。

### Deregistered 037

Former [`037_generic_generalization_licensing`](archive/037_generic_generalization_licensing/) asked whether generic acceptance is licensed by prevalence, cue validity/diagnosticity, or principled/causal conceptual relations.

It is **KILL-NOVELTY / ARCHIVED** because Hu, van Paridon & Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language` (`arXiv:2607.04523`), directly tests the principled-vs-statistical generic-property distinction in language models while controlling prevalence and cue validity. Adding open-weight causal MI would be too close to behavior/factorization -> mechanism under N2.

Detailed record: [`rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md`](rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md).

## 039 为什么通过 Route C

039 的问题不是从 probe/SAE/benchmark 反推出来的：

> `dog—wolf` 是 **same kind / taxonomic**；`dog—leash` 是 **go together / thematic**。LLM 是否把这两种“相关”表示成不同、可复用且真正影响决策的 semantic relation？

核心 substrate 是 Landrigan & Mirman 的 659 个公开 human-normed word pairs：**同一 pair 同时有 taxonomic rating 与 thematic rating**，并直接给出两者差值。无需 LLM judge，也无需把两个 benchmark 拼成假 2×2。

Hard novelty attack 后保留的 concept-level delta：

- NAACL 2025 causal property-inference work owns **taxonomy vs categorical similarity**，不是 taxonomic vs thematic relation type；
- NeurIPS 2025 TaxonomiGQA 的 `non-taxonomic` negatives 是“不在 WordNet hypernym chain”的概念，不是 thematic matches；
- 2026 taxonomic–thematic LLM triad work owns **cross-cultural simulation fidelity**，不拥有 relation-type representation / causal-use question；
- older taxonomic/thematic embedding work is static embedding probing, not modern autoregressive causal use.

因此 039 允许一个很简单的 frozen first causal test：从 neutral word-pair representations 学 relation-type state，再看它能否双向改变独立 taxonomic-vs-thematic triad choice，同时 generic relatedness / lexical / frequency / co-occurrence controls 不产生同样效果。

完整注册文件：[`active/039_same_kind_vs_go_together_semantic_relation/README.md`](active/039_same_kind_vs_go_together_semantic_relation/README.md)。

## 当前 authority

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议，当前 v2.1**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — current handoff（内容持续更新到 2026-09-01）
3. 本 README — register 计数与入口

执行入口：[`active/README.md`](active/README.md)。失败证据见 [`rejected_candidates/`](rejected_candidates/)；撤销项目见 [`archive/`](archive/)。

## v2.1：严格不等于复杂

031/F8 的教训继续有效：benchmark-removal、N0/N1/N2、真实 substrate、story invariance、禁止 null 后换 headline 都不放松。

但 fresh search 现在增加 **Route C — simple phenomenon / simple latent object first**：

```text
简单、自然、令人意外的现象或语义属性
→ matched controls 去掉 obvious confound
→ strongest-neighbor novelty
→ accessible open model / data
→ minimal falsifiable causal-use question
→ mechanism 可以在执行中长出来
```

不再要求所有题在注册前都必须有三套复杂 mechanism、精确数学 interaction、两个完全匹配的 published families。是否需要这些取决于 claim。

### Simplicity sanity test

> **不用 LLM / benchmark / activation / SAE / mechanistic interpretability 这些词，能不能一句话把问题讲清楚？**

如果不能，优先怀疑题目被过度工程化。

## 强论文尺度标尺

- ACL 2025 Outstanding `Llama See, Llama Do`：simple broad phenomenon → causal mechanism → mitigation。
- EMNLP 2025 Outstanding shared filler-gap：成熟理论问题 → causal LM evidence。
- NAACL 2025 taxonomy vs similarity：一个简单 competing axis 就能撑完整 paper。
- NAACL 2025 `Racing Thoughts`：一个强 unified hypothesis → causal validation。
- ACL 2026 Main `Do LLMs Know Tool Irrelevance?`：天然 semantic relevance vs structural match，controlled dataset 只负责解耦。

## 当前项目纪律

- **034 / 035 完全冻结。** 除非发现新的致命 novelty collision，不重审、不改 headline。
- **036 / 038 已完成本轮 v2.1 simplicity re-audit，继续 PASS。** 没发现新的 direct concept-level collision；复杂 causal contract 本身不是扣分项，执行时仍以冻结 headline 为准。
- **039 按 Route C 注册。** Simple is good; trivial is not. 机制服务于 `same kind vs go together` 这个自然 semantic-relation question，而不是反过来。
- serious candidate 一旦 KILL，必须立即写 `rejected_candidates/` 记录。
- 达到 5/5 后不再为了“继续找更多题”稀释执行；只有新 fatal collision 或明显更强替代项才改 register。

## 029–033 re-audit

- 029 — ARCHIVE / SCALE+PROVENANCE。
- 030 — ARCHIVE / VLM target mismatch。
- 031 — TERMINAL / V3 measurement + canonical F8 scope-drift lesson。
- 032 — ARCHIVE / mother-mechanization scale。
- 033 — ARCHIVE / N2 delta width + data gap。

## 仍保留的旧工作

- [`active/014_alias_entrainment_transfer`](active/014_alias_entrainment_transfer/)：已有正式结果，属于 paper development，不计入 fresh register。

## One-line discipline

> **先找一个简单、自然、值得知道的新 object / axis / phenomenon；再用最简单的实验把它隔离干净，最后才决定需要哪种 MI。注册不是“值得试”，而是“这个问题已经值得一篇论文”。**