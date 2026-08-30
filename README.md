# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然反直觉现象**。

当前工作方式已经从“先把所有题审到完美再允许模型调用”调整为两层：

```text
cheap D0 screening：尽快跑，尽快 kill
full validation / mechanism：现象和 novelty 都站住后再做
```

## 最重要的入口

### 当前 Top-10

[`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)

2026-08-30 owner decision：当前 Top-10 已全部注册进 [`active/`](active/README.md)，用于实际 D0 screening。

Top-10：

1. Clarification Resolution Lag
2. Mixed-Status Event Attraction
3. Alias Entrainment Transfer
4. Cross-Modal Resolution Inertia
5. Stock–Flow Correlation Intrusion
6. Abstention Hysteresis
7. Incremental Clue Backfire
8. Task-Switch Carryover
9. Local Success, Global Composition Failure
10. Description–Experience Gap

每个项目自己的 README 都详细写了：**研究问题、最接近工作、novelty 边界、数据集、自动构造方案、hard scoring、fatal controls、PROMOTE/KILL、mechanistic fork。**

### Active projects

[`active/README.md`](active/README.md)

这里是实际跑题入口。`active` 的含义现在是“值得真正动手跑 cheap D0”，不是“已经证明是 paper”。

### 模型调用授权

[`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md)

registry 现在区分：

- **D0 screening authorization**：Top-10 新项目允许在各自 README 的 pre-run gate 满足后跑便宜 behavioral smoke；
- **full validation / mechanism authorization**：当前仍为 0，必须等 behavioral phenotype、N1 collision、scope、fatal controls、frozen contract 都闭合。

014 是特殊项目：历史 phase 1–3 已完成，但下一次 D1 仍需先 materialize corrected r4 RedirectQA + `ASSOC_ANY` bank 并完成 source/scope/attrition audit。

### 找题规则

[`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md)

核心仍然是：**phenomenon before mechanism**。Mother paper 已经有 headline behavior、我们只剩 representation/route/causal fork 时，不能把机制问题冒充新现象。

### 数据 scope

[`phenomenon_miner/DATASET_SCOPE_AUDIT.md`](phenomenon_miner/DATASET_SCOPE_AUDIT.md)

不能为了制造干净 money cell，把 scientific population 越筛越窄。理论 moderator 默认 factor-not-filter。

### 失败库

[`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)

内部失败证据是 hard pre-filter。换名字、换 dataset 不能复活同一个已经失败的 scientific object。

---

## 当前数据原则

我们现在优先找：

```text
公开 dataset / structured source
+ source labels / executable oracle / deterministic rule
-> Python 自动构造 paired D0
-> 人工只随机抽查 builder 是否写歪
```

而不是：

```text
研究者人工写 100 条 scenario
研究者逐条判断 gold
为了显著不断删 domain/type/direction
```

当前尤其偏好三类 data shape：

1. **source labels already exist**：CondAmbigQA、MAVEN-FACT、MUCAR、MuSiQue；
2. **source structure can be ablated/restored**：supporting-fact QA、Quiz Bowl prefixes；
3. **deterministic natural/process oracle**：ResOpsUS、exact-frequency gamble generator。

---

## 新的运行流程

```text
natural question / mother phenomenon
-> register screening project
-> materialize source data
-> deterministic builder + source sanity
-> cheap two-family D0 smoke
-> KILL or phenotype PASS
-> N1 exact collision closure
-> scope/fatal controls/generality
-> freeze behavioral contract + data SHA
-> full validation
-> mechanism
```

这意味着：**D0 可以早点跑，但 MI 不能早点跑。**

---

## 旧状态

- `007_weak_evidence_backfire` — **TERMINAL HARD KILL**；
- `013_publicness_coordination_dissociation` — PARKED/HOLD-DATA；
- 法律/医学那批需要逐篇手工抽 gold 的题继续 park；
- 旧 Task-Switch TR/TL / Resolved-Ambiguity Neuron Persistence 等 hidden-state-defined 版本不直接复活；新的 015/021 必须先建立独立 output-level phenotype。

---

## 一句纪律

> **先把自然、可硬评分的行为跑出来；没现象就杀，撞 mother 就 route。只有一个现象同时过了 behavioral evidence 和 novelty boundary，hidden state 才值得看。**
