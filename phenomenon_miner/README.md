# Phenomenon Miner

这里是仓库的 **LLM 可解释性选题工作台**。只保留四类当前有决策价值的信息：

1. **怎么找题** → [`FINDING_RULES.md`](FINDING_RULES.md)
2. **现在做哪些题** → [`CURRENT_TOPICS.md`](CURRENT_TOPICS.md)
3. **哪些题死了、为什么死** → [`FAILED_TOPICS.md`](FAILED_TOPICS.md)
4. **哪些正式项目可以调用模型** → [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)

模型家族与 scaling 验证约定单独见 [`MODEL_PANEL.md`](MODEL_PANEL.md)。

## 核心哲学

```text
先找到自然、重要、能一句话讲清的 scientific object
→ 找题阶段把 novelty 和数据路径一次做透
→ DISCOVERY-PASS 后才正式注册
→ 行为先过关
→ 再做机制
```

这里不再保存多代 Batch shortlist、working N0 audit、旧 `promoted/phenomena/candidates` 状态树或 162-card 大库存。它们对当前决策已经失去权威性，完整历史仍可从 Git history 追溯。

## 当前状态

- **19 个**新题继续 discovery；其中 7 个 Tier S 优先完成最后的 N1/data feasibility closure。
- `active/007_weak_evidence_backfire` 是当前唯一 authorized smoke。
- `active/013_publicness_coordination_dissociation` 继续 legacy HOLD。
- 新题没有任何一个因为“看起来 promising”就自动获得 `DISCOVERY-PASS` 或模型授权。

## 目录边界

- `phenomenon_miner/`：找题规则、当前题、失败知识、dispatch。
- `active/`：已正式注册且仍可能继续的项目。
- `archive/`：terminal 项目及完整实验/裁决证据。
- `rejected_candidates/`：更早期 brainstorming/rejection 历史；不参与当前调度。

**不要从旧 commit 里的 Batch/Tier/Promoted 标签推断当前状态。当前选题只看 `CURRENT_TOPICS.md`，模型调用只看 `AUDIT_REGISTRY.md`。**
