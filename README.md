# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然、反直觉、可机制化的问题**。

> **2026-08-31 最新权威状态：当前 continuation search 的 `PASS_REGISTER = 0`。**
> 继续工作必须先读 [`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) 和最新 [`rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md`](rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md)。本 README 下方保留的历史 `survivor / registered / HOLD` 叙述是研究轨迹记录，**若与最新 handoff / terminal addendum 冲突，一律视为 stale，不可计入当前五题目标。**

Top-6 实跑后，选题流程已经从“能不能构造漂亮 factorial experiment”改成：

```text
natural question
→ strong mother / external concept anchor
→ classify failure vs factorization
→ S0: open-model effect OR objective row-level gold + counted cross-cells
→ Hamdi-style mother-inclusion N0
→ strongest-neighbor / successor N1
→ if novelty gets narrower and narrower, KILL
→ data as measurement instrument
→ cheap behavioral/capability contract
→ controls
→ mechanistic interpretability
```

核心规则：[`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)。
注册前一票否决：[`phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`](phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md)。

> **最新跨对话接力入口：[`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md)。** 继续搜题前先读该文件与 `rejected_candidates/` 最新 terminal addenda；旧 chat 中的 `lead/HOLD` 不具有更高权威性。

## 当前 established / adjudicated 主线

### 014 Alias Entrainment Transfer

Broad cross-surface learned-relation spillover 已成立；reference-specific/entity-salience interpretation 不成立。论文固定为 cross-surface transfer 的 structural gradient + lexical/reference boundary。

### 018 Stock–Flow Correlation Intrusion

Natural stock-flow question 经 bounded D0-v2 semantic-recognition repair 后仍为
0/4 family PROMOTE；可估计家族的正确-net-history effect 为小幅 null 或反向。
状态固定为 `NO-PROMOTE / NO-MI / TERMINAL`，禁止继续 gate repair 或缩成
polarity/prompt/model-specific 子题。

## 第一轮 Hamdi-style N0 survivors

> **历史记录提示：本节中的 survivor 标签不是当前 continuation 的 PASS 状态。以最新 handoff 为准。**

### 024 Alignment: Descriptive Social Model vs Normative Readout

> Alignment 让模型更 normative 时，是 descriptive human model 被改坏，还是 descriptive knowledge 仍在而 normative signal / late readout 赢了？

### 025 World-Indexed Truth

> 同一 proposition 在 actual world 与 stipulated local world 下有不同 truth value 时，模型是否表示 `Truth(P, world)`？

完整审计：[`phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md)。

## 第二轮：N0 + N1 三个新注册题

> **历史记录提示：这些旧 registration 后续已被 retrospective S0 adjudication；不可从这里直接恢复为当前 PASS。**

完整审计：[`phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md`](phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md)。

### 026 Plausibility Is Not Testability

> **“这个科学假设可能是真的”和“它能被一个有区分力的实验检验”不是同一判断。LLM 是否把 plausibility 与 testability 分成两个内部 scientific variables？**

Mother：ACL 2026 scientific feasibility + NAACL scientific-hypothesis evaluation。N1 未找到 causal internal factorization 的直接工作。

详细合同：[`active/026_scientific_plausibility_testability_factorization/`](active/026_scientific_plausibility_testability_factorization/)

Retrospective S0：`KILL`。当前公开 artifact 没有 broad、independent、
expert-grounded P/T 双 gold；不使用 o1-preview ratings 替代专家标注。

### 027 Questions That Assert

> **识别“这是 rhetorical question”和理解“speaker 借它实际上断言了什么 proposition/stance”是否是两个 computation？**

Mother：EMNLP 2025 SRAQ + ACL 2026 RQ representation。不能退化成 RQ detection 或 yes/no polarity trick。

详细合同：[`active/027_rhetorical_force_implied_assertion/`](active/027_rhetorical_force_implied_assertion/)

Retrospective S0：`KILL`。SRAQ/QT30 提供自然、多功能 force gold，
但没有发布与 question 对齐的 implied assertion / speaker commitment gold；
不以 polarity inversion、任意 following turn 或 LLM label 代替中央 target。

### 028 Cause Is Not Blame

> **不同 narrative 改变 blame/credit 时，模型是否保留一个相对稳定的 event-causal core，还是 responsibility framing 会重写 causality itself？**

Mother：ACL 2026 FrECI。不能退化成 source identity / political bias probe。

详细合同：[`active/028_causality_responsibility_factorization/`](active/028_causality_responsibility_factorization/)

Retrospective S0：`KILL`。论文 schema/human annotation 通过，但
官方 row-level repository 当前 404；论文的 shared-effect fragmentation
统计不能回答 same cause-effect pair / different responsibility frame 的数量。

## Strict novelty kills

- **Superseded Truth ≠ Never-True Falsehood**：2026 temporal-drift mechanism work 已覆盖独立 axis + stale/confabulation + dynamics + steering；KILL。
- **Falsehood ≠ Deceptive Intent**：N1 发现近期 deception-specific / intent-targeted probe 与 non-lying-deception work 已逼近标题级结论；继续只能缩成 subtype，因此未注册。
- 007 / 020 / 021 / 022 已从 active 清理进 archive，禁止换数据复活。

## HOLD

> **历史记录提示：本节是旧状态；当前 continuation 允许继续执行的 frontier 只以 authoritative handoff 的四条列表为准。**

- 003 Diagnostic Counterevidence Revision — natural mother provenance；no call。
- 013 Publicness–Coordination — natural question, HOLD-DATA。
- 023 Description–Experience Gap — natural external phenomenon，HOLD-N0-REAUDIT。

## 关键入口

- **[`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`](phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md) — 最新跨对话 authoritative handoff；当前新题 0 PASS-REGISTER。**
- **[`rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md`](rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md) — 最新 terminal negative memory / 本轮失败题总表。**
- [`phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md`](phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md) — 下一轮对话可直接使用的完整执行提示词。
- [`phenomenon_miner/NTSB_LOCAL_AGENT_PROMPT_2026-08-31.md`](phenomenon_miner/NTSB_LOCAL_AGENT_PROMPT_2026-08-31.md) — NTSB 验证交给本地 agent 的可复制提示词。
- [`phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`](phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md) — NTSB 本地数据审计→G0 的完整执行合同。
- [`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)
- [`phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`](phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md)
- [`phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md`](phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md)
- [`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)
- [`active/README.md`](active/README.md)
- [`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md)
- [`phenomenon_miner/S0_FUNNEL_2026-08-31.md`](phenomenon_miner/S0_FUNNEL_2026-08-31.md) — 48-way S0-first discovery funnel；本轮 0 survivors。
- [`archive/README.md`](archive/README.md)
- [`rejected_candidates/README.md`](rejected_candidates/README.md)

## One-line discipline

> **像 Hamdi 一样：mother 先给出一个无需 dataset 也值得追问的 scientific object；我们再问它内部到底是什么。若 novelty 审计迫使标题不断加限定词，题就已经死了。**