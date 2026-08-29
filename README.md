# Interpretability Topic Search

这个仓库用于寻找、证伪和解释 **LLM / agent 的自然反直觉现象**。原则是：**先把题目本身查透、自然数据路径做实，再投入模型预算。**

## 最重要的入口

### 1. 找题规则

[`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md)

回答：什么题自然、什么算主会尺度、N0/N1 怎么做、什么时候必须砍。

### 2. 当前选题

[`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)

2026-08-29 data-first re-audit 后，当前 phenomenon discovery queue 只保留 **7 个**问题：4 个近期开 D0 数据审计，3 个先做 20-unit source-yield audit。旧 Batch/Tier/Promoted/162-card 标签不再有当前状态含义。

详细的数据裁决见 [`phenomenon_miner/DATA_REVIEW_2026-08-29.md`](phenomenon_miner/DATA_REVIEW_2026-08-29.md)。

### 3. 数据 scope 规则

[`phenomenon_miner/DATASET_SCOPE_AUDIT.md`](phenomenon_miner/DATASET_SCOPE_AUDIT.md)

回答一个独立于 novelty 的问题：**最后造出来的数据，还是不是原来那个科学问题的数据？**

核心纪律：scientific population 先冻结；raw / validity / matched / analysis strata 分层；理论 moderator 默认 factor-not-filter；不能靠筛窄数据来制造“干净现象”。

### 4. 失败选题与原因

[`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)

记录 KILL / ROUTE / HOLD-DATA / capability floor / artifact / collision，以及防止 rename revival 的可复用教训。

### 5. 模型调用授权

[`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md)

**唯一模型调用授权源。当前 authorized model calls = 0。**

- `007_weak_evidence_backfire` 已有 merged smoke verdict：**HARD KILL**；
- `014_alias_entrainment_transfer` 历史 phase 1–3 已完成，但下一次 D1/phase-4 call 被 corrected r4 data/scope audit 阻塞；
- `013_publicness_coordination_dissociation` 继续 `PARKED / HOLD-DATA`。

---

## 当前 discovery 优先级

近期开 D0 数据审计：

1. **Mixed-Status Event Attraction**
2. **Subgroup-Significance → Interaction Promotion**
3. **Stock–Flow Correlation Intrusion**
4. **Harmless-Error → Remedy Collapse**

先做 20-unit manual source-yield audit：

5. **Noninferiority → Equivalence Collapse**
6. **Surrogate → Clinical-Outcome Promotion**
7. **Dissent → Holding Role Swap**

Task-Switch TR/TL、Resolved-Ambiguity Neuron Persistence、Action-Boundary State Routing 等 hidden-state-defined questions 已从 phenomenon queue 路由为 `MECH-FOLLOWUP`；有趣不等于新的自然 phenotype。

---

## 新题流程

```text
mother question / natural phenomenon
→ N0 breadth
→ N1 depth
→ D0 source-feasibility
  → scope-integrity audit
→ DISCOVERY-PASS
→ formal registration
→ freeze locked D0
→ behavioral smoke
→ generality
→ mechanism
```

N0、N1、数据搜索都在**找题阶段**做完。`active/` 不再用来继续找文献、换数据或修 scientific contract。

## 目录角色

```text
phenomenon_miner/   找题规则 + 当前题 + 数据审查 + 失败知识 + dispatch
active/             历史/当前尚保留的具体项目；目录存在不代表授权
archive/            已停止项目及完整实验/裁决证据
rejected_candidates/更早 brainstorming / rejected 历史
preflight/          共享环境/工具历史
```

公开数据集参考见 [`DATASET_CATALOG.md`](DATASET_CATALOG.md)；较早期、实际消耗过算力的详细失败复盘见 [`FAILURE_POSTMORTEMS.md`](FAILURE_POSTMORTEMS.md)。

## 不变纪律

- **Behavior first**：现象没过行为与一般性，不靠 hidden-state evidence 救题。
- **Data is part of topic selection**：自然 source / hard gold / independent unit / license / scope 做不实，题就没选完。
- 自构造数据可以做机制控制，但不能替代自然行为锚点。
- terminal failure 不靠换弱模型、subset、readout、阈值或名字续命。
- mother 已有 headline behavior，只剩 `representation → causal? / route? / where?` 时，标成 `MECH-FOLLOWUP`，不占 phenomenon slot。
- claim/source 实质改变就退回 discovery。
- 模型调用权限永远只看 `phenomenon_miner/AUDIT_REGISTRY.md`。
