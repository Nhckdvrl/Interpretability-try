# Interpretability Topic Search

这个仓库用于寻找、快速证伪、再解释 **LLM / MLLM 的自然、反直觉、可机制化的问题**。

Top-6 实跑后，选题流程已经从“能不能构造漂亮 factorial experiment”改成：

```text
natural question
→ strong mother / external concept anchor
→ Hamdi-style mother-inclusion N0
→ strongest-neighbor / successor N1
→ if novelty gets narrower and narrower, KILL
→ data as measurement instrument
→ cheap behavioral/capability contract
→ controls
→ mechanistic interpretability
```

核心规则：[`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)。

## 当前 established / redesign 主线

### 014 Alias Entrainment Transfer

Broad cross-surface learned-relation spillover 已成立；reference-specific/entity-salience interpretation 不成立。论文固定为 cross-surface transfer 的 structural gradient + lexical/reference boundary。

### 018 Stock–Flow Correlation Intrusion

Natural stock-flow question 保留；D0-v1 是 A/B recognition measurement failure，不是 scientific null。下一轮只允许 bounded net-recognition repair。

## 第一轮 Hamdi-style N0 survivors

### 024 Alignment: Descriptive Social Model vs Normative Readout

> Alignment 让模型更 normative 时，是 descriptive human model 被改坏，还是 descriptive knowledge 仍在而 normative signal / late readout 赢了？

### 025 World-Indexed Truth

> 同一 proposition 在 actual world 与 stipulated local world 下有不同 truth value 时，模型是否表示 `Truth(P, world)`？

完整审计：[`phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md)。

## 第二轮：N0 + N1 三个新注册题

完整审计：[`phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md`](phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md)。

### 026 Plausibility Is Not Testability

> **“这个科学假设可能是真的”和“它能被一个有区分力的实验检验”不是同一判断。LLM 是否把 plausibility 与 testability 分成两个内部 scientific variables？**

Mother：ACL 2026 scientific feasibility + NAACL scientific-hypothesis evaluation。N1 未找到 causal internal factorization 的直接工作。

详细合同：[`active/026_scientific_plausibility_testability_factorization/`](active/026_scientific_plausibility_testability_factorization/)

Source preflight: `PARK-DATA`。当前公开 artifact 没有 broad、independent、
expert-grounded P/T 双 gold；不使用 o1-preview ratings 替代专家标注。

### 027 Questions That Assert

> **识别“这是 rhetorical question”和理解“speaker 借它实际上断言了什么 proposition/stance”是否是两个 computation？**

Mother：EMNLP 2025 SRAQ + ACL 2026 RQ representation。不能退化成 RQ detection 或 yes/no polarity trick。

详细合同：[`active/027_rhetorical_force_implied_assertion/`](active/027_rhetorical_force_implied_assertion/)

Source preflight: `PARK-DATA`。SRAQ/QT30 提供自然、多功能 force gold，
但没有发布与 question 对齐的 implied assertion / speaker commitment gold；
不以 polarity inversion、任意 following turn 或 LLM label 代替中央 target。

### 028 Cause Is Not Blame

> **不同 narrative 改变 blame/credit 时，模型是否保留一个相对稳定的 event-causal core，还是 responsibility framing 会重写 causality itself？**

Mother：ACL 2026 FrECI。不能退化成 source identity / political bias probe。

详细合同：[`active/028_causality_responsibility_factorization/`](active/028_causality_responsibility_factorization/)

Source preflight: `PARK-ARTIFACT`。论文 schema/human annotation 通过，但
官方 row-level repository 当前 404；论文的 shared-effect fragmentation
统计不能回答 same cause-effect pair / different responsibility frame 的数量。

## Strict novelty kills

- **Superseded Truth ≠ Never-True Falsehood**：2026 temporal-drift mechanism work 已覆盖独立 axis + stale/confabulation + dynamics + steering；KILL。
- **Falsehood ≠ Deceptive Intent**：N1 发现近期 deception-specific / intent-targeted probe 与 non-lying-deception work 已逼近标题级结论；继续只能缩成 subtype，因此未注册。
- 007 / 020 / 021 / 022 已从 active 清理进 archive，禁止换数据复活。

## HOLD

- 003 Diagnostic Counterevidence Revision — natural mother provenance；no call。
- 013 Publicness–Coordination — natural question, HOLD-DATA。
- 023 Description–Experience Gap — natural external phenomenon，HOLD-N0-REAUDIT。

## 关键入口

- [`phenomenon_miner/NATURAL_QUESTION_GATE.md`](phenomenon_miner/NATURAL_QUESTION_GATE.md)
- [`phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md`](phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md)
- [`phenomenon_miner/CURRENT_TOPICS.md`](phenomenon_miner/CURRENT_TOPICS.md)
- [`active/README.md`](active/README.md)
- [`phenomenon_miner/AUDIT_REGISTRY.md`](phenomenon_miner/AUDIT_REGISTRY.md)
- [`archive/README.md`](archive/README.md)
- [`rejected_candidates/README.md`](rejected_candidates/README.md)

## One-line discipline

> **像 Hamdi 一样：mother 先给出一个无需 dataset 也值得追问的 scientific object；我们再问它内部到底是什么。若 novelty 审计迫使标题不断加限定词，题就已经死了。**
