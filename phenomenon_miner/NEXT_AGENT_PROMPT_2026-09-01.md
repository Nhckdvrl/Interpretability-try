# Next Agent Prompt — 2026-09-01

继续 GitHub 仓库 `Nhckdvrl/Interpretability-try` 的 ACL / EMNLP / NAACL 风格 **LLM mechanistic interpretability 找题工作**。

这是上一轮 fresh topic search 的直接 continuation。**不要从零 brainstorm，不要让我重新解释背景，也不要重审已经冻结的 034 / 035，除非你发现新的致命 novelty collision。**

## 第一步：先完整读取当前 authority

必须先读：

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` —— 完整读，尤其 PAPER-SCALE / Benchmark-removal / Natural-object / Normal-scope / Novelty-step / Story-invariance / Dataset-is-a-window / Branch-concreteness / Venue-scale comparator / N2 delta-width / F8
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` —— 当前 authoritative handoff，日期内容已更新到 2026-09-01
4. `active/034_prospective_memory_retrieval_architecture/README.md`
5. `active/035_shared_dynamic_context_update/README.md`
6. 本文件 `phenomenon_miner/NEXT_AGENT_PROMPT_2026-09-01.md`

只在新候选与旧题语义重合时，定向查 `rejected_candidates/` 和 `archive/`。不要重新通读所有历史 addendum。

## 当前 authoritative 状态

```yaml
CURRENT_FRESH_PASS_REGISTER: 2
CURRENT_FRESH_ACTIVE_TOPICS: 2
target: 5
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
remaining_needed: 3
```

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

Scientific question：

> 当 LLM agent 一边继续做当前任务、一边要记住未来意图时，它靠持续 strategic monitoring、cue-triggered spontaneous retrieval，还是根据 cue/context 动态切换？

为什么已注册：

- 是经典 prospective-memory retrieval theory，不依赖 benchmark；
- PM-Bench 公布 deterministic scenario、scorer/runtime、64 trajectories；
- Llama-3.3、Mistral、Qwen3 等 open families 有 substantial non-ceiling phenotype；
- strongest-neighbor search 没发现 native open-weight LLM 上已经 causal adjudicate monitoring vs spontaneous retrieval；
- frozen S0、cue focality/context microscope、H1/H2/H3、fatal controls、first causal interaction statistic 都已写完。

**不要把它重新改成“PM-Bench failure mechanism”。不要改变 headline。**

### 035 — Shared Dynamic Context Update Across Discourse Phenomena

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

Scientific question：

> LLM 是否维护一个可复用的、动态更新的 local discourse context，同时支持 anaphora accessibility 与 presupposition projection；还是两个现象各自依赖独立/static/lexical computation？

为什么已注册：

- object 来自 dynamic semantics / DRT，而不是 dataset；
- ACL 2025 anaphora accessibility + CoNLL 2026 Outstanding presupposition 提供两个独立 behavioral windows；
- 两边都有公开逐 item artifact，且共享 `Llama-3.1-8B-Instruct`；
- strongest-neighbor search 没发现跨 phenomena 的 shared dynamic-context causal machinery 已被做掉；
- 冻结 common structural window 是 conditional local context；
- H1 shared update / H2 phenomenon-specific / H3 lexical-static；
- primary statistic 是 cross-task causal transfer 相对于 within-task causal effect，而不是 best layer。

**不要把 035 缩回“presupposition mechanism”或“anaphora mechanism”。**

## 这一轮最重要的成果：最初五个候选 5/5 全死

上一轮一开始找到五个 PAPER-SCALE-looking candidates，但用户明确要求最终 authoritative register 5 个，而不是 5 个“有潜力”。于是做 hard gate，结果 5/5 被正确挡在 GPU 外：

1. **explicit vs implicit memory systems — KILL-NOVELTY**  
   ACL 2026 ImplicitMemBench 已经把 implicit behavior 解释为不能还原为 explicit storage/retrieval，并暗示 distinct mechanisms。再做 causal double dissociation 太像 mother mechanization。

2. **prototype vs exemplar categorization — KILL-NOVELTY**  
   EACL 2026 Best Paper 已经占据 LM category learning 的 abstraction-vs-exemplar 概念轴。

3. **source independence / false corroboration — KILL-NOVELTY**  
   2026 `Beyond Memory Majority` 已明确提出 shared upstream source 被重复算成 independent evidence 的 Memory Correlation Bias，并做 provenance-aware correction。

4. **model-based vs model-free decision control — KILL-NOVELTY / KILL-BEHAVIOR**  
   LLM-specific work 已直接研究该轴；two-step behavior 又不够唯一诊断，必须重新发明 behavior battery 才能继续。

5. **event-boundary memory organization — KILL-BEHAVIOR**  
   LLM 能做 event segmentation，但 ordinary comprehension 中 boundary-driven memory restructuring 没有足够强的现代 open-model phenotype。

这一步是本轮筛选哲学的核心：**PAPER-SCALE 只是第一门，不等于 register。**

## 其他已经认真审过并 KILL 的路线

这些都已经或应当在 `rejected_candidates/` 有短记录。禁止通过换标题/数据/模型/probe/subset/语言复活：

- revision vs world update
- source memory / reality monitoring
- common-ground shared state vs private-belief reconstruction
- proactive vs reactive executive control
- premise-diversity induction
- garden-path serial commitment vs parallel interpretation competition
- structural priming lexical boost / abstract vs lexical priming mechanism
- scalar implicature default vs contextual mechanism
- reasoning stopping / progress monitoring / when-to-quit
- quantifier-scope heuristic-first vs structure-sensitive computation
- confirmation bias acquisition vs assimilation locus

主要死亡模式：

- mother 已经拥有 headline interpretation，继续只是 behavior→mechanism；
- strongest neighbor 已占 concept-level axis；
- exact modern open-model phenotype 不存在；
- artifact 不完整 / code-data 只写 coming soon；
- 必须先自己造 contrast 跑模型看看 effect 是否存在，违反“不能用 GPU 发现论文问题”。

## 当前最强但尚未注册的 lead

### Good-enough syntax–semantic arbitration

当前只处于 **HARD AUDIT / NOT REGISTERED**。

Behavioral window：EACL 2026 Main `The Dog the Cat Chased Stumped the Model` / CenterBench。

已知：

- 9,720 comprehension questions；
- 交叉操纵 syntactic complexity × semantic plausibility；
- 多模型有 strong plausibility × complexity interaction；
- 某些结构要求高的题里，semantic plausibility 反而会伤害正确理解；
- 这与 psycholinguistic `good-enough processing` 有自然 lineage。

可能的一句话问题：

> 当结构分析与 semantic plausibility 冲突时，LLM 是持续 arbitration 两种 evidence，还是随着 processing difficulty 增大，从 structure-sensitive computation 切换到 semantic shortcut？

但是 **千万不要直接注册**。下一轮第一件候选工作就是把它按 hardest N2 攻击：

1. 完整读 EACL 2026 mother 的 discussion / limitations；
2. 判断 mother 是否已经拥有 `complexity rises -> model abandons structure for semantic shortcut` 这个 headline interpretation；
3. 搜 2025–2026 good-enough comprehension、syntax/plausibility conflict、thematic-role reversal、semantic plausibility、processing-regime switching 的 mechanistic work；
4. 如果最自然描述变成 `mother found X; we explain X internally`，立即 `KILL-NOVELTY`；
5. 只有保留下来的问题是独立 theory-level arbitration / regime-selection question，而且 Result A/B/C 都不换标题，才继续；
6. 再审 exact artifact、row-level data、modern open checkpoints、scoring、>=2 open-family phenotype；
7. 冻结 S0 + first causal interaction，再注册。

## 下一轮目标

不是再给我 3 个“不错的想法”。

目标是：

> **继续广搜和屠杀，直到再得到 036、037、038 三个与 034/035 同等级的 `PASS-REGISTER / GPU AUTHORIZED` 项目，把 authoritative register 从 2/5 真正推进到 5/5。**

预计死亡率很高。为了得到最后三个，应该准备认真审查至少 10–20 个 serious candidates，而不是只找三个。

## 正确找题顺序

严格保持：

```text
独立自然 scientific question
→ benchmark 名删掉仍值得问
→ scientific/cognitive/formal-theory lineage
→ strong mother / established object
→ strongest-neighbor N0/N1/N2
→ exact accessible substrate
→ modern open-model behavior / legitimate Route-A omitted axis
→ theory-level competing mechanisms
→ Result A/B/C story invariance
→ frozen S0 / first causal statistic / fatal controls
→ PASS-REGISTER
→ GPU
```

禁止：

```text
mother limitation
→ 想内部 mechanism
→ 找 dataset
→ 先跑小实验
→ 根据结果决定 paper story
```

## 优先搜索形状

### Route A — real omitted scientific axis

mother 建立 object O；新轴 B 必须：

- 在真实 scientific literature 中本来就存在；
- 有自然 cross-cells；
- mother 没问；
- 不是 limitation/future work 的同义改写；
- 本身足够撑一篇论文；
- 不只是补一个 2×2 表格。

### Route B — established anomaly + independent mechanism debate

- behavior 已经在现代 open models 上稳定存在；
- row-level/executable artifact 真实可得；
- 新机制问题本身有独立 scientific meaning；
- 至少两个 theory-motivated competing mechanisms；
- 不能是 early/middle/late localization；
- 不提 benchmark 仍然是一篇正常论文的问题。

## 对每个 serious candidate 必须输出/记录

### A. Natural question
一句普通研究者能懂的话。

### B. Why paper-scale
不提 benchmark 说明为什么值得研究。

### C. Scientific lineage
来自哪个真实 theory/debate/phenomenon。

### D. Strong mother(s)
mother 提供 established object，不是 future-work 缝。

### E. Exact novelty delta
与 strongest 3–5 neighbors 比，新增哪个 concept-level question。

### F. Venue-scale comparison
至少和 3 篇 ACL/EMNLP/NAACL Main/Outstanding 比题目幅度。

### G. Data
natural/synthetic、central gold、为什么 dataset 只是 window、open checkpoint、artifact 是否真实可执行。

### H. Competing mechanisms
必须是理论上不同的 computation，而不是 layer 位置。

### I. Story invariance
Result A/B/C 三种结果下，标题问题完全不变。

### J. Fatal risks
最可能死在哪里。

### K. Verdict
只能：

- `CONTINUE-PAPER-SCALE`
- `PASS-REGISTER`
- `KILL-SCALE`
- `KILL-NOVELTY`
- `KILL-DATA`
- `KILL-BEHAVIOR`

## PASS-REGISTER 的硬条件

只有下面全部明确写出后，才允许创建 `active/036_*` / `037_*` / `038_*`：

```text
PAPER-SCALE
+ benchmark-removal PASS
+ independent scientific object
+ >=3 venue-scale comparators
+ N0 clear
+ N1 unoccupied
+ N2 concept-level delta wide enough
+ exact accessible row-level substrate / central gold
+ established modern open-model behavior OR legitimate Route-A omitted axis
+ >=2 relevant open families where required
+ 2–3 theory-level competing mechanisms
+ Result A/B/C invariant headline
+ frozen S0 / controlled microscope
+ frozen first causal statistic / intervention predictions
+ fatal controls / hard kill conditions
= PASS-REGISTER / GPU AUTHORIZED
```

**如果还需要“先跑一个小实验看看现象有没有”，就不允许注册。**

## 失败记录纪律

任何 serious candidate 一旦认真查过 mother / strongest neighbor / data / behavior 并 KILL：

- 立即写 `rejected_candidates/<canonical_name>_2026-09-01.md`；
- 写 semantic aliases；
- 写决定性 kill evidence；
- 写 nearest-neighbor warning；
- 写 resurrection condition；
- 不要写几十页 addendum。

## Venue-scale calibration anchors

继续用这些做题目幅度标尺：

- ACL 2025 Outstanding — `Llama See, Llama Do`
- EMNLP 2025 Outstanding — `Causal Interventions Reveal Shared Structure Across English Filler–Gap Constructions`
- NAACL 2025 — `Characterizing the Role of Similarity in the Property Inferences of Language Models`
- NAACL 2025 — `Racing Thoughts`
- ACL 2026 Main — `Do LLMs Know Tool Irrelevance?`

## 最终一句执行指令

> **保持 034 / 035 冻结。先 hard-audit good-enough syntax–semantic arbitration，但不要被它锚定；继续广泛 fresh search，宁可再杀十几个题，也不要为了凑数降低标准。只有当 036–038 每个都已经有独立 paper-scale question、N0/N1/N2、真实可执行 substrate、现代 open-model premise、冻结 S0 与 causal contract 时，才把 authoritative register 从 2 改到 5。**
