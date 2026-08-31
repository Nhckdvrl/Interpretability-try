# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
fresh_register_target: 5
fresh_register_status: COMPLETE
latest_registered_project: 038 unresolved reference representation architecture
latest_terminal_project: 031 within-run graph-state audit
latest_reaudit: continued fresh search with high-mortality PAPER-SCALE + N2 hard audits
current_target: execute frozen registered questions; do not add topics merely to increase count
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED** | Do anaphora and presupposition reuse a shared dynamic local-context update, or rely on separate/static heuristics? |
| [`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) | **PASS-REGISTER / GPU AUTHORIZED** | What selects comparison vs categorization in metaphor comprehension: conventionality, aptness, or no discrete route switch? |
| [`037_generic_generalization_licensing`](active/037_generic_generalization_licensing/) | **PASS-REGISTER / GPU AUTHORIZED** | What licenses a generic generalization: prevalence, flexible probabilistic diagnosticity, or conceptual/causal relation? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED** | When reference remains genuinely unresolved, does the LM maintain parallel candidates, an underspecified state, or prematurely commit? |

**Fresh target 已达到 5/5。** 这不是五个“promising leads”，而是五个已经通过当前 PAPER-SCALE + N0/N1/N2 + substrate + frozen causal-contract gate 的题。后续任何一个若出现新的致命 novelty collision 或 frozen measurement gate 失败，必须按规则终止/撤销；不能因为 target=5 而保题。

**上一轮 029–033 的 `5/5 PASS` 已全部撤销。** 031 在 V3 measurement gate 失败；029/032/033 在新的 topic-scale / novelty-width re-audit 下不再值得继续；030 作为 VLM 题退出当前 LLM 主线。五个目录均已完整移动到 `archive/`，保留代码、结果与 provenance。

## 当前 authority

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议；PAPER-SCALE / N2 / F8 继续有效**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / execution handoff
3. 本 README — fresh register 计数与项目入口

执行入口：[`active/README.md`](active/README.md)。历史项目与失败证据见 [`archive/`](archive/) 和 [`rejected_candidates/`](rejected_candidates/)。

## 当前最重要的修正

过去的协议过度强调：

> strong mother + existing behavior + clean causal test

这还不够。031 证明，一个题即使 mother 很强、phenotype 可复现、causal primitive 能运行，也可能仍然只是**某个 benchmark construct 内部的一条解释缝**。

硬顺序仍然是：

```text
1. PAPER-SCALE natural question
2. strong scientific object / mother
3. concept-level novelty delta
4. legitimate dataset as measurement window
5. existing behavior / natural omitted axis
6. strongest-neighbor + delta-width audit
7. frozen S0 / measurement
8. registration
9. causal MI
```

### 一句话 PAPER-SCALE 标准

> **把 dataset / benchmark / mother 名字删掉以后，这个问题仍然必须像一个正常的 ACL/EMNLP/NAACL scientific question。**

如果删掉 benchmark 后只剩“这个 failure 内部是什么”“行为相似是否机制相似”“哪层坏了”，默认 KILL-SCALE。

## 强论文尺度标尺

- ACL 2025 Outstanding `Llama See, Llama Do`：先有跨模型/设置的 broad phenomenon，再做 causal mechanism。
- EMNLP 2025 Outstanding `Causal Interventions Reveal Shared Structure Across English Filler–Gap Constructions`：成熟理论问题先存在，MI 裁决 shared mechanism。
- NAACL 2025 `Characterizing the Role of Similarity in the Property Inferences of Language Models`：经典 competing theories，dataset 只是测量窗口。
- NAACL 2025 `Racing Thoughts`：统一 processing hypothesis 先于 causal validation。
- ACL 2026 Main `Do LLMs Know Tool Irrelevance?`：天然变量先存在，controlled dataset 用来解耦。

详见 [`FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md)。

## 034–038 one-line frozen objects

- **034 Prospective Memory Retrieval Architecture:** strategic monitoring vs spontaneous cue-triggered retrieval vs dynamic multiprocess switching.
- **035 Shared Dynamic Context Update:** reusable local discourse-context update across anaphora and presupposition vs phenomenon-specific/static computation.
- **036 Metaphor Processing Route Selection:** conventionality vs aptness vs no discrete selector for comparison/categorization processing.
- **037 Generic Generalization Licensing:** prevalence vs flexible prevalence+diagnosticity vs conceptual/causal licensing.
- **038 Unresolved Reference Representation Architecture:** explicit parallel candidate referents vs compact semantic underspecification vs premature commitment.

Each active README contains the frozen S0, causal statistic/signature, story-invariant hypotheses and fatal controls. **Do not silently narrow any headline after a null.**

## 029–033 re-audit

- **029 Human-Like Fallacies — ARCHIVE / SCALE+PROVENANCE.** ETR/PyETR 定义了几乎整个问题；删去 ETR 后问题过泛，保留后又偏窄；论文 383-item final exclusion manifest 也未公开。
- **030 Spatial Reference Frames — ARCHIVE / TARGET MISMATCH.** 科学问题本身不判死，但它是 VLM，不属于当前 LLM 主线。
- **031 Spontaneous Deception → Graph-State Audit — TERMINAL KILL.** V3 best held-out invariant reachability AUROC ~0.53，0 passing layers；更重要的是 headline object 曾随实验结果多次收窄，是 F8 canonical example。
- **032 Temporal Forgetting Mechanism — ARCHIVE / SCALE.** 当前 extension 主要是“哪个 stage/circuit 导致 mother forgetting”；hypotheses 很大程度是 localization taxonomy。
- **033 Opposite-Scaling Entrainment — ARCHIVE / DELTA WIDTH + DATA.** delta 太接近已有 contextual-entrainment mechanism / mother interpretation，且 item-level data gap。

## 仍保留的旧工作

- [`active/014_alias_entrainment_transfer`](active/014_alias_entrainment_transfer/)：已有正式结果，属于 paper development，不属于 fresh 5/5 register。
- 其它旧 active/HOLD 目录只保留 provenance，不自动拥有新实验权限。

## One-line discipline

> **注册不是“这个实验值得试”；注册是“这个问题本身已经值得一篇论文，只差用冻结实验回答”。达到 5/5 以后，这条规则仍然不变。**
