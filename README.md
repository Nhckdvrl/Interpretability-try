# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / VLM 的自然、反直觉、可机制化 scientific questions**。

当前 continuation search：

```yaml
PASS_REGISTER: 0
counts_toward_target_five: 0
new_topic_MI_authorized: false
latest_terminal_execution: NTSB causal-role frontier KILL-S0
```

**No candidate passes the current bar.**

---

## 当前只认三份权威文件

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — **唯一选题协议**
2. [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 当前状态 / 下一步
3. 本 README — 仓库入口

一般失败经验：[`phenomenon_miner/FAILED_TOPICS.md`](phenomenon_miner/FAILED_TOPICS.md)。

其它 gate、funnel、N0/N1、terminal addendum、domain log、old candidate 文件都是**历史证据**。除非一个新题语义上接近它们，否则下一轮不需要完整通读。

旧文件里的 `lead / HOLD / PRE-S0 / registered / survivor / under audit / active` 不自动代表当前有效状态；以 handoff 为准。

---

## 现在怎样找题

今天的核心修正是停止：

```text
想一个听起来合理的 phenomenon
→ 设计数据和机制故事
→ 花算力赌模型会不会出现
```

改为真正的 Hamdi-style mother extension：

```text
strong concrete mother
→ mother 已经测清 object O
→ 找 O 上 mother 没问的现实轴 / internal computation
→ 尽量复用 mother 的 unit / readout / recipe
→ semantic negative-memory + strongest-neighbor attack
→ cheap artifact/output falsifier
→ S0
→ registration
→ MI
```

只允许两类主要来源：

- **omitted-axis extension**：同一个 object 上有现实中独立的新属性，例如 entity knowledge → ontological status；
- **established anomaly → unasked causal computation**：行为已经成立，再问 prior work 没问的内部 state/computation，并要求 competing causal hypotheses 与不同 intervention prediction，例如 arbitrary-choice bias → choice-state vs entropy writer。

详细合同全部集中在 `FINDING_RULES.md`。

---

## 最重要的失败教训

48-way S0 funnel 的结果是：24 个先死于 behavior/measurement，8 个死于 substrate，14 个在 pre-S0 就被 mother/successor 占据，只有 2 个走到更后的 novelty gate，最终 **0 survivor**。

因此问题不是 gate 不够多，而是过去 candidate generation 太宽、太依赖猜测。

当前统一把死亡归为七类：

```text
F1 behavior lottery / synthetic-first
F2 mother or strongest-neighbor ownership
F3 substrate / gold / cross-cell mirage
F4 measurement / metadata / capability artifact
F5 no common phenotype across families
F6 post-hoc rescue / scope drift
F7 mechanistically weak / method-closed
```

详见 `FAILED_TOPICS.md`。逐题死因只作为证据留在 `rejected_candidates/` 和 `archive/`，不再反复复制到新协议里。

---

## 当前执行状态

### 014 Alias Entrainment Transfer

已有正式研究结果，继续 paper development。Broad cross-surface learned-relation spillover 成立；reference-specific/entity-salience interpretation 不成立。项目证据在 [`active/014_alias_entrainment_transfer/`](active/014_alias_entrainment_transfer/)。

### NTSB causal relevance vs causal-role selection

**TERMINAL `KILL-S0 / RELEVANCE-ALSO-FAILS`**。四个 open families 的 relevance BA 仅 0.537–0.635，没有预设的 `relevance strong / role weak` dissociation；metadata/length audit 也暴露 construct 问题。详见 [`rejected_candidates/ntsb_causal_relevance_vs_causal_role_selection_2026-08-31.md`](rejected_candidates/ntsb_causal_relevance_vs_causal_role_selection_2026-08-31.md)。

其它旧 frontier / HOLD 的最新处理见 handoff；它们都**不计入五题**。

---

## 目录怎么用

- `active/`：曾进入正式实验身份的项目；目录名不保证当前仍 active。
- `archive/`：正式项目的停止/终止证据。
- `rejected_candidates/`：逐题 negative evidence，供**定向 semantic search**，不是每轮必读清单。
- `phenomenon_miner/`：当前协议、handoff 与历史 discovery artifacts。

新 rejection 文件保持短：记录 question、mother、F1–F7 kill class、decisive evidence、nearest-neighbor warning、resurrection condition 即可。不要再复制整套协议。

---

## One-line discipline

> **不要问“模型还可能有什么有趣的错？”；问“这篇强 mother 已经测清的 object，还有哪个重要属性或 computation 它没有问？”**
