# Interpretability Topic Search

这个仓库用于寻找、证伪和解释 **LLM / agent 的自然反直觉现象**。原则是：**先把题目本身查透、数据路径做实，再投入模型预算。**

## 最重要的入口

### 1. 找题规则

[`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md)

回答：什么题自然、什么算主会尺度、N0/N1 怎么做、数据怎么前置、什么时候必须砍。

### 2. 当前选题

[`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)

当前 19 个 discovery survivors + 2 个 legacy continuing projects。旧 Batch/Tier/Promoted 标签不再有当前状态含义。

### 3. 失败选题与原因

[`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)

记录 KILL / ROUTE / capability floor / artifact / collision / D0 failure，以及防止 rename revival 的可复用教训。

### 4. 模型调用授权

[`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md)

**唯一模型调用授权源。** 当前只有 `active/007_weak_evidence_backfire` 的冻结 30-case contract 为 authorized。

---

## 新题流程

```text
mother question / natural phenomenon
→ N0 breadth
→ N1 depth
→ D0 source-feasibility
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
phenomenon_miner/   找题规则 + 当前题 + 失败知识 + dispatch
active/             已正式注册且尚未 terminal 的项目
archive/            已停止项目及完整实验/裁决证据
rejected_candidates/更早 brainstorming / rejected 历史
preflight/          共享环境/工具历史
```

公开数据集参考仍见 [`DATASET_CATALOG.md`](DATASET_CATALOG.md)；较早期、实际消耗过算力的详细失败复盘见 [`FAILURE_POSTMORTEMS.md`](FAILURE_POSTMORTEMS.md)。

## 不变纪律

- Behavior first；现象没过行为与一般性，不靠 hidden-state evidence 救题。
- 自构造数据可以做机制控制，但不能替代自然行为锚点。
- terminal failure 不靠换弱模型、subset、readout、阈值或名字续命。
- claim/source 实质改变就退回 discovery。
- 模型调用权限永远只看 `phenomenon_miner/AUDIT_REGISTRY.md`。
