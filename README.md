# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
fresh_register_target: 5
fresh_register_status: OPEN_AFTER_037_DEREGISTRATION
latest_registered_project: 038 unresolved reference representation architecture
latest_deregistered_project: 037 generic generalization licensing
required_protocol: PAPER-SCALE v2.1
current_target: re-audit 036/038 under simplicity-first standard and find one genuinely stronger replacement topic
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update, or rely on separate/static heuristics? |
| [`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT** | What makes a metaphor behave like comparison vs categorization: conventionality, aptness, or no discrete switch? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |

**当前不是 5/5，而是 4/5。** Former 037 was immediately deregistered after a fatal July-2026 novelty collision was found during the v2.1 re-audit. Count never protects a weak topic.

### Deregistered 037

Former [`037_generic_generalization_licensing`](archive/037_generic_generalization_licensing/) asked whether generic acceptance is licensed by prevalence, cue validity/diagnosticity, or principled/causal conceptual relations.

It is now **KILL-NOVELTY / ARCHIVED** because Hu, van Paridon & Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language` (`arXiv:2607.04523`), directly tests the principled-vs-statistical generic-property distinction in language models while controlling prevalence and cue validity. Adding open-weight causal MI would be too close to behavior/factorization -> mechanism under N2.

Detailed record: [`rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md`](rejected_candidates/generic_generalization_licensing_principled_statistical_collision_2026-09-01.md).

## 当前 authority

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议，当前 v2.1**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / handoff
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
- **036 / 038 正在接受 v2.1 simplicity re-audit。** 复杂 causal contract 本身不是扣分项；真正要看 headline 是否自然、novelty 是否足够宽、substrate 是否可信。
- fresh search 继续寻找一个更简单、更强的新题。为保留 provenance，新 PASS 建议使用下一未使用编号 `039_*`，不复用已归档的 037。
- serious candidate 一旦 KILL，必须立即写 `rejected_candidates/` 记录。

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
