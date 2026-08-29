# Phenomenon Miner

版本：2026-08-29  
状态：`v4 / DISCOVERY-FIRST / N0+N1+D0 BEFORE REGISTRATION`

本目录是当前 LLM 可解释性选题的唯一 discovery 工作区。

## 当前规则

正式注册一个新题之前，必须同时完成：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
= DISCOVERY-PASS
```

定义与完整流程看 [`FINDING_RULES.md`](FINDING_RULES.md)。

最重要的纪律：

> **phenomenon before mechanism。**
>
> strong mother paper 可以提供 motivation、behavioral object 和 mechanism opening；但如果 mother 已经拥有 headline behavior，而我们只剩 `representation → causal? / route? / where?`，它应被标成 `MECH-FOLLOWUP`，不能伪装成新的 phenomenon candidate。

## 当前入口

- [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) — **唯一 authoritative current queue**。2026-08-29 re-audit 后，Tier S 只保留优先补完 N1+D0 的 phenotype-first 题；Alias 单列 construct-validation；Action Boundary 单列 mechanism follow-up；GeoTemporal / Causal Retrieval / Dead-Branch 已移出高优先级队列。
- [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md) — **唯一 model-call authorization**。Tier S/A/B、active directory、survivor 等标签都不代表模型授权。
- [`FAILED_TOPICS.md`](FAILED_TOPICS.md) — KILL / ROUTE / HOLD-DATA 与 anti-revival lessons。新一轮搜索必须先查这里。
- [`FINDING_RULES.md`](FINDING_RULES.md) — N0、N1、D0、behavior-first、strong-model kill、stop-loss 的正式合同。
- [`MODEL_PANEL.md`](MODEL_PANEL.md) — behavioral smoke / generality 的 checkpoint panel 约定。

## 2026-08-29 re-audit 后的调度

当前最优先完成 discovery package：

1. **Task-Switch TR/TL Desynchronization**
2. **Resolved-Ambiguity Neuron Persistence**
3. **Stock–Flow Correlation Intrusion**

下一梯队：

- Subgroup-Significance → Interaction Promotion
- Mixed-Status Event Attraction
- Noninferiority → Equivalence Collapse
- Correlation → Agreement / Interchangeability Promotion

特殊轨道：

- **Alias Entrainment Transfer** — 已有 phenotype，但 N1/v4 D0 曾被 owner waiver；当前只允许完成冻结的 construct validation，entity interpretation 未成立。
- **Action-Boundary State Routing** — 明确标为 `MECH-FOLLOWUP`，不占新的 behavioral-phenomenon slot。

不再占当前高优先级 discovery 资源：

- GeoTemporal Binding Bottleneck → `ROUTE / MOTHER-MECHANISM-FOLLOWUP`
- Causal Retrieval Schedule → `ROUTE / TARGETED-MECH-FOLLOWUP`
- Dead-Branch Residue after Invalidation → `KILL/ROUTE-STANDALONE`

具体理由见 [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md) 与 [`FAILED_TOPICS.md`](FAILED_TOPICS.md)。

## 一句原则

> **找题阶段的目标不是尽快拥有一个题，而是尽快知道这个题是否值得存在。GPU 负责证伪现象，不负责替 N0/N1/D0 收拾残局。**
