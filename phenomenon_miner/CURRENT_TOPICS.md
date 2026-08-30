# Current Topics

日期：2026-08-30  
状态：`AUTHORITATIVE TOP-10 / ACTIVE D0 SCREENING QUEUE`

当前 owner 决策：**不再只保留 2 个 off-the-shelf D0。现在 Top-10 全部注册进 `active/`，依次实际跑 cheap behavioral D0。**

这里的目标不是一上来就证明 paper，而是尽快用低成本、尽量程序化的数据把现象跑死或跑活。

---

## 1. 新的筛选原则

优先级现在同时看四件事：

```text
1. scientific question 一听就懂，不靠 hidden-state jargon 才成立
2. D0 尽量不需要我们人工打新标签
3. gold 来自 source dataset / deterministic rule / executable oracle
4. 行为一旦成立，后面有清楚的 mechanistic fork
```

**数据构造可以程序化，但不能为了容易构造就把题变成纯 synthetic puzzle。**

人工允许做的是随机 source audit，检查 builder 没写歪；不允许人工逐条决定主 gold。

---

## 2. Current Top-10

### #1 — Clarification Resolution Lag

目录：[`../active/015_clarification_resolution_lag/`](../active/015_clarification_resolution_lag/)

> 用户已经把歧义解释清楚了，模型会不会还停留在旧的 ambiguous state？

Primary data: CondAmbigQA-2K；secondary: PRACTIQ。

真正 novelty 不是“condition helps”，而是：**最终 condition/evidence 相同，只因为之前经历过 ambiguity history，最终 answer 仍更差或被旧 interpretation 吸引。**

数据难度：**低**。

---

### #2 — Mixed-Status Event Attraction

目录：[`../active/016_mixed_status_event_attraction/`](../active/016_mixed_status_event_attraction/)

> 两个 event 单独 factuality 都能判断，放进同一真实 discourse 后会不会互相带偏？

Primary data: MAVEN-FACT，112k+ source-annotated event factuality mentions。

现有 builder：`../preflight/d0_mixed_status_event_attraction/build_from_maven_fact.py`。

必须看到 toward-neighbor-status 的 directional error，而不是普通 context-length accuracy drop。

数据难度：**低**。

---

### #3 — Alias Entrainment Transfer

目录：[`../active/014_alias_entrainment_transfer/`](../active/014_alias_entrainment_transfer/)

> 看见一个实体名字，会不会连没出现过的另一个 alias 也被 entrain？

Broad cross-surface phenotype 已经成立；当前问题是它究竟是 entity/reference identity，还是 learned pair association。

下一步不是重新 D0，而是 r4 RedirectQA + `ASSOC_ANY` construct validation。

数据难度：**中**；下一次 D1 仍受 registry gate 限制。

---

### #4 — Cross-Modal Resolution Inertia

目录：[`../active/017_cross_modal_resolution_inertia/`](../active/017_cross_modal_resolution_inertia/)

> 文字先形成了一个旧解释；晚到的图片已经把意思定死，模型还能不能真正改过来？

Primary data: MUCAR dual-ambiguity。

MUCAR 已经做了 static cross-modal disambiguation；我们的 money cell 必须是：

```text
text-only initially wrong
simultaneous image+text correct
text-first then same image -> still sticks to old interpretation
```

数据难度：**低到中**，取决于 MUCAR release 形式与 open MLLM harness。

---

### #5 — Stock–Flow Correlation Intrusion

目录：[`../active/018_stock_flow_correlation_intrusion/`](../active/018_stock_flow_correlation_intrusion/)

> net flow 已经算对了，stock 判断为什么还会跟着 inflow 走？

Primary data: ResOpsUS real reservoir time series。

现有 builder：`../preflight/d0_stock_flow_correlation_intrusion/build_from_resopsus.py`。

核心是 computation-gated dissociation：`net flow correct -> stock wrong specifically toward inflow`。

数据难度：**低**。

---

### #6 — Abstention Hysteresis

目录：[`../active/019_abstention_hysteresis/`](../active/019_abstention_hysteresis/)

> 模型先说过一次“信息不足”，后来证据补齐了，它会不会还更容易继续拒答？

Primary data shape: source supporting-fact QA，自动 full -> ablate -> restore；可参考 AbstentionBench。

只分析：

```text
initial incomplete -> model abstains
DIRECT full -> model correct
POST-ABSTENTION full -> ?
```

数据难度：**低**，但 2026 abstention 文献更新快。

---

### #7 — Incremental Clue Backfire

目录：[`../active/020_incremental_clue_backfire/`](../active/020_incremental_clue_backfire/)

> 已经答对后，再增加一条真实、同 gold 的 clue，模型反而会不会改错？

Primary data: Quiz Bowl ordered clue prefixes。

数据可完全程序化 prefix sweep，不需要新 label。

**前置：必须先查内部 failed-topic collision。** 若旧 Evidence-Induced Referent Displacement 已覆盖同一 scientific object，直接 kill/route，不能换数据复活。

数据难度：**低**。

---

### #8 — Task-Switch Carryover

目录：[`../active/021_task_switch_carryover/`](../active/021_task_switch_carryover/)

> 换任务后犯的错，是随机变多，还是还在执行上一个任务的规则？

Mother: Gupta et al., EMNLP 2024 已证明 aggregate task-switch interference。

所以本题只有找到**old-rule-specific wrong destination**才有独立 phenotype；单纯复现 accuracy drop 不算。

数据难度：**中**，因为还需要 natural hard old-rule oracle。

---

### #9 — Local Success, Global Composition Failure

目录：[`../active/022_local_success_global_composition_failure/`](../active/022_local_success_global_composition_failure/)

> 中间答案已经全部正确、甚至显式摆在同一上下文里，最后还会不会组合错？

Mother collision: Press et al. 2023 已定义 compositionality gap。

本题只有更强条件才可能新：

```text
all required intermediate facts explicitly present in current context
-> final composition still wrong
```

Primary data: MuSiQue；secondary: 2WikiMultiHopQA。

数据难度：**低**，novelty 风险：**高**。

---

### #10 — Description–Experience Gap

目录：[`../active/023_description_experience_gap/`](../active/023_description_experience_gap/)

> 同一个 gamble，直接写概率和展开成完全等价的历史结果，模型最后选择会不会不同？

不需要人工数据集：deterministic exact-frequency generator 即可。

主设计用 exact frequencies，避免 sampling noise；另做 empirical-frequency / expected-value capability gate。

数据难度：**极低**，但需要严格查最新 2026 LLM risk-choice 文献。

---

## 3. 实际运行顺序

按“最快得到有意义的 yes/no”排序，而不是论文最终价值：

```text
1. 015 Clarification Resolution Lag
2. 016 Mixed-Status Event Attraction
3. 019 Abstention Hysteresis
4. 020 Incremental Clue Backfire（collision-first）
5. 018 Stock-Flow Correlation Intrusion
6. 017 Cross-Modal Resolution Inertia
7. 023 Description-Experience Gap
8. 021 Task-Switch Carryover
9. 022 Local/Global Composition（Press exact-collision-first）
10. 014 Alias r4 construct validation
```

如果你想按“paper 潜力”而不是“跑起来快”排序，继续参考 active README 的 Top-10 rank；两种排序不是同一件事。

---

## 4. Screening 与正式晋级

当前 Top-10 已 owner-approved 进入便宜 D0 screening。授权细节看 [`AUDIT_REGISTRY.md`](AUDIT_REGISTRY.md)。

D0 出现现象以后，还不能直接做 mechanism。必须再过：

```text
N1 exact collision closure
source-population/scope integrity
fatal controls
second-family/generalization where required
frozen behavioral contract + data/generator SHA
```

尤其：

- 021 不得把 mother task-switch interference 当新贡献；
- 022 不得把 compositionality gap 当新贡献；
- 017 不得把 static MUCAR failure 当新贡献；
- 019 不得把一般 abstention failure 当新贡献。

---

## 5. PARKED / TERMINAL 仍保持

下面旧题没有因为 Top-10 注册而复活：

- `007 Weak-Evidence Backfire` — **TERMINAL HARD KILL**；
- `013 Publicness–Coordination Dissociation` — PARKED/HOLD-DATA；
- Training-Recency Conflict Arbitration — HOLD-DATA；
- Correlation -> Agreement / Interchangeability — HOLD-DATA；
- Habitual -> Episode Actualization — HOLD-DATA；
- Competing-Event -> Censoring Collapse — HOLD-DATA；
- 法律/医学那批需要逐篇人工抽 gold 的题 — 继续 park，不抢当前跑题资源。

---

## 一句纪律

> **现在 active 的意义是“值得真的跑一下”，不是“我已经相信这个故事”。先让程序化 D0 把坏题杀掉；只有 output-level 现象和 novelty boundary 都站住，hidden states 才进场。**
