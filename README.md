# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、题目幅度正常、自然且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 1
CURRENT_FRESH_ACTIVE_TOPICS: 1
fresh_register_target: 5
latest_registered_project: 034 prospective memory retrieval architecture
latest_terminal_project: 031 within-run graph-state audit
latest_reaudit: initial fresh paper-scale pool hard-audited; all five killed before GPU
current_target: continue fresh LLM search until authoritative register reaches 5
```

## 当前 fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |

**还需要 4 个同等级题目。** 不因为 target=5 降低任何 gate；候选死亡即进 `rejected_candidates/`，继续搜索替代。

**上一轮 029–033 的 `5/5 PASS` 已全部撤销。** 031 在 V3 measurement gate 失败；029/032/033 在新的 topic-scale / novelty-width re-audit 下不再值得继续；030 作为 VLM 题退出当前 LLM 主线。五个目录均已完整移动到 `archive/`，保留代码、结果与 provenance。

## 当前只认三份权威文件

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议；先过 PAPER-SCALE**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / 下一轮执行说明
3. 本 README — 仓库入口

执行入口：[`active/README.md`](active/README.md)。历史项目与失败证据见 [`archive/`](archive/) 和 [`rejected_candidates/`](rejected_candidates/)。

## 当前最重要的修正

过去的协议过度强调：

> strong mother + existing behavior + clean causal test

这还不够。031 证明，一个题即使 mother 很强、phenotype 可复现、causal primitive 能运行，也可能仍然只是**某个 benchmark construct 内部的一条解释缝**。

新的硬顺序是：

```text
1. PAPER-SCALE natural question
2. strong scientific object / mother
3. concept-level novelty delta
4. legitimate dataset as measurement window
5. existing behavior / natural omitted axis
6. strongest-neighbor + delta-width audit
7. S0 measurement
8. registration
9. causal MI
```

### 一句话 PAPER-SCALE 标准

> **把 dataset / benchmark / mother 名字删掉以后，这个问题仍然必须像一个正常的 ACL/EMNLP/NAACL scientific question。**

如果删掉 benchmark 后只剩“这个 failure 内部是什么”“行为相似是否机制相似”“哪层坏了”，默认 KILL-SCALE。

## 强论文尺度标尺

下一轮不是只搜 title collision，而是要主动对齐强 Main / Outstanding 论文的**问题幅度**：

- ACL 2025 Outstanding `Llama See, Llama Do`：先发现跨模型/设置的 contextual entrainment，再做 causal mechanism 与 mitigation。
- EMNLP 2025 Outstanding `Causal Interventions Reveal Shared Structure Across English Filler–Gap Constructions`：成熟理论问题先存在，MI 用来裁决 shared mechanism。
- NAACL 2025 `Characterizing the Role of Similarity in the Property Inferences of Language Models`：经典 taxonomy vs similarity 争论，dataset 只是测量窗口。
- NAACL 2025 `Racing Thoughts`：先有能解释一类 contextualization errors 的统一 hypothesis，再做 causal validation。
- ACL 2026 Main `Do LLMs Know Tool Irrelevance?`：现实中独立的 semantic relevance vs structural match，controlled dataset 只是把两者解耦。

详见 [`FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md)。

## 029–033 re-audit

- **029 Human-Like Fallacies — ARCHIVE / SCALE+PROVENANCE.** ETR/PyETR 定义了几乎整个问题；删去 ETR 后问题过泛，保留后又偏窄；论文 383-item final exclusion manifest 也未公开。
- **030 Spatial Reference Frames — ARCHIVE / TARGET MISMATCH.** 科学问题本身不判死，但它是 VLM，不属于下一轮 LLM 主线。
- **031 Spontaneous Deception → Graph-State Audit — TERMINAL KILL.** V3 best held-out invariant reachability AUROC ~0.53，0 passing layers；更重要的是 headline object 曾随实验结果多次收窄，是新 F8 的 canonical example。
- **032 Temporal Forgetting Mechanism — ARCHIVE / SCALE.** mother 现象很强，但当前 extension 主要是“哪个 stage/circuit 导致 mother 的 forgetting”；H1–H4 很大程度是 localization taxonomy，不够独立于 mother。
- **033 Opposite-Scaling Entrainment — ARCHIVE / DELTA WIDTH + DATA.** ACL'25 Outstanding 已拥有 generic entrainment mechanism，ACL'26 mother 已提出 semantic filtering vs mechanical copying 的功能分离；继续做 writer/gate circuit 更像 mechanizing mother future-work，且 item-level mother data 未释放。

## 仍保留的旧工作

- [`active/014_alias_entrainment_transfer`](active/014_alias_entrainment_transfer/)：已有正式结果，属于 paper development，不是本轮 fresh search。
- 其它旧 active/HOLD 目录只保留 provenance，不自动拥有新实验权限。

## One-line discipline

> **注册不是“这个实验值得试”；注册是“这个问题本身已经值得一篇论文，只差用实验回答”。**
