# 026 — Plausibility Is Not Testability

**Working title:** *Plausibility Is Not Testability: How Language Models Factorize Scientific Feasibility*
**Status:** `NATURAL-QUESTION PASS / N0 PASS / N1 PASS / ACTIVE-PREFLIGHT / NO MODEL CALL YET`
**Created:** 2026-08-31

## 1. 一句话问题

> **一个科学假设“听起来可能是真的”和“真的能设计实验检验它”不是一回事。LLM 内部会不会把这两个判断当成两个不同的科学变量？**

例子不用提任何模型就能成立：

- 一个假设可能很符合现有理论，但变量无法观测、没有可区分实验，因此 **plausible but hard/un-testable**；
- 一个假设可能非常离谱，但只要给出清楚可反驳预测，就可以 **implausible but testable**；
- 真正好的科学判断需要同时知道“值不值得相信”和“怎么把它证伪/支持”。

这不是为了造 2×2 benchmark 才发明的区别，而是科学方法里本来就存在的区别。

## 2. 为什么这是 ACL/EMNLP 级问题

LLM 已经大量进入 scientific discovery：生成 hypothesis、读论文、设计实验、评估研究方向。如果模型把 plausibility 和 testability 压成一个模糊的 `feasible / not feasible` 感觉，它可能：

- 把听起来合理但不可检验的 speculation 当好研究；
- 把不符合先验但很容易检验的高价值 hypothesis 直接拒掉；
- 在看到 positive outcome 后事后觉得 experiment 本来就是好的；
- 无法解释到底是“不相信假设”还是“不相信实验能裁决假设”。

一个主会级故事可以是：

```text
scientific feasibility looks one-dimensional behaviorally
→ internally it may decompose into plausibility and testability
→ errors occur at a specific merge/readout stage
→ causal interventions selectively move one judgment
→ mechanism predicts when scientific agents confuse "unlikely" with "untestable"
```

## 3. Mother paper

Mohammadi, Gaur & Ferraro, **Experiments or Outcomes? Probing Scientific Feasibility in Large Language Models**, ACL 2026 Short.

https://aclanthology.org/2026.acl-short.50/

它已经回答：

- LLM 能否判断 scientific feasibility；
- hypothesis-only / experiment / outcome / experiment+outcome 哪种信息最有用；
- outcome evidence 通常比 experiment descriptions 更可靠；
- incomplete experiment information 可能让判断变差。

它对 feasibility 的定义本身包含两个概念：

1. claim 是否符合 established scientific knowledge；
2. experimental evidence 是否能够 support/refute claim。

**它没有问这两个概念在模型内部是不是同一个 computation。**

## 4. Strong adjacent work

Kumbhar et al., **Hypothesis Generation for Materials Discovery and Design Using Goal-Driven and Constraint-Guided LLM Agents**, Findings NAACL 2025:

https://aclanthology.org/2025.findings-naacl.420/

其 expert-developed hypothesis-quality rubric 已经分别评价：

- Scientific Plausibility
- Testability
- Feasibility & Scalability
- Innovation / impact 等

所以我们的两个轴不是自己为了 MI 方便硬拆出来的。已有 scientific evaluation 就认为它们应该分开。

其它相邻线包括 HARPA、SFBench、FirstResearch 等 scientific-discovery / feasibility / falsifiability 工作；它们研究如何生成或评估更可测试的科学问题，不研究 LLM 内部如何把 plausibility 与 testability 表示和组合。

完整 N0/N1：[`../../phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md`](../../phenomenon_miner/HAMDI_MOTHER_N0_N1_3_2026-08-31.md)。

## 5. Novelty boundary

### 已经不能 claim

- “我们发现 LLM 会判断 scientific feasibility”；
- “experiments 和 outcomes 对模型影响不同”；
- “scientific hypothesis 应该同时 plausible、testable”；
- “我们提出一个科学假设评分 rubric”；
- “LLM scientific agents 需要 falsifiability”。

### 我们真正的新问题

> **Is scientific feasibility internally factorized into plausibility and testability, and where are the two judgments combined into a final decision?**

至少需要区分三种内部结构：

### H1 — Generic feasibility scalar

模型很早就把两种信息压成一个：

```text
hypothesis + experiment
→ generic "good/bad science" state
→ feasibility answer
```

### H2 — Separate axes, late merge

```text
hypothesis semantics → plausibility state
experimental design  → testability state
                         ↓
                    late arbitration
                         ↓
                    feasibility answer
```

### H3 — One axis exists, one is reconstructed late

例如模型真正稳定表示 plausibility，但 testability 只靠 surface experiment cues 临时推断；这可以解释 mother paper 中 experiment descriptions 的脆弱性。

## 6. 为什么 MI 是必要的

只做 output benchmark 无法区分：

- 模型根本不知道假设是否 plausible；
- 模型知道 plausible，但误把“不可测”当“不可能”；
- 两个判断都对，final feasibility reader 合并错；
- outcome evidence 直接覆盖了 experimental testability judgment。

这些机制预测完全不同的 interventions，所以内部分析不是装饰。

## 7. 数据原则：data is instrument

**严禁先搜一个有两个 rating 列的数据集再把题变成评分预测。**

需要的 population 是自然 scientific hypotheses + experiment descriptions，最好包含 source/expert provenance。

候选 source：

1. ACL 2026 mother 使用的 scientific-feasibility datasets；
2. Findings NAACL 2025 materials-discovery released artifacts / expert-curated goals, constraints, methods；
3. SFBench expert-created feasibility claims；
4. 其它公开 scientific hypothesis corpora，只作为 cross-domain confirmation。

### Preflight 必须确认

```yaml
natural_hypotheses: true
source_provenance: explicit
plausibility_target: independently_definable
testability_target: independently_definable
no_llm_judge_as_primary_gold: preferred
cross_axis_support: sufficient
restriction_budget: small
```

如果最后只能靠“我们人工/LLM judge 给每条 hypothesis 打 plausibility 和 testability 分数”，本题 **PARK-DATA**，不能为了跑而降低标准。

## 8. 最小 behavioral prerequisite

我们不要求先发现一个巨大的 failure 才能做，因为 factorization 本身值得研究；但至少要证明模型能够分别执行两个 judgment。

建议四类 natural cells：

```text
P+ T+ : plausible and testable
P+ T- : plausible but currently non-discriminating / untestable
P- T+ : implausible but sharply testable/falsifiable
P- T- : implausible and untestable
```

这里的 2×2 必须从 source/expert judgments 或明确 scientific constraints 得到，而不是 prompt engineering 造笑话。

第一阶段测：

- explicit plausibility query；
- explicit testability query；
- composite feasibility query；
- experiment/outcome conditions。

## 9. Mechanistic plan

行为/capability 过 gate 后才允许：

1. layer-wise probes / representation geometry：P 与 T 是否独立可读；
2. cross-domain transfer：不是材料学词汇 detector；
3. residualization：控制 scientific field、length、experiment vocabulary、positive/negative wording；
4. activation patching：只改 P donor 或只改 T donor；
5. steering / causal mediation：改变 plausibility 是否保持 testability，反之亦然；
6. locate merge/readout：composite feasibility 在哪层开始依赖两者；
7. mother-result explanation：为什么 outcome evidence 更稳定、experiment text 更 brittle。

### Money result

最强结果不是两个 probe 都高，而是 causal double dissociation：

```text
intervene plausibility state
→ plausibility/composite judgment changes
→ testability judgment stays stable

intervene testability state
→ testability/composite judgment changes
→ plausibility stays stable
```

再定位 final feasibility reader 如何组合两者。

## 10. Fatal controls

- domain/topic leakage；
- hypothesis lexical absurdity；
- experimental-detail length；
- “testable” 被模型偷换成“cheap/easy to execute”；
- plausibility 被模型偷换成“already supported by evidence”；
- outcome evidence 改变 posterior plausibility 是合法的，不应误叫 testability contamination；
- train/test 必须按 topic/source cluster split。

## 11. PROMOTE / ROUTE / KILL

### PROMOTE

- natural multi-domain source 支持两个独立 target；
- ≥2 open model families 明确能做 P/T judgments；
- internal evidence 显示可复现 factorization 或可解释的 merge structure；
- causal intervention 区分 competing mechanisms；
- mechanism 能解释 mother 的 experiment-vs-outcome asymmetry 或预测新的 scientific-agent failure。

### ROUTE

如果只剩：

> experiment text 比 outcome text 更难

直接 route 回 ACL 2026 mother。

### KILL / PARK

- 只有 materials-specific tiny rubric 才有 gold；
- axes 只有 lexical/template signal；
- 独立评分根本没有可靠 source；
- 最后只能写成“better feasibility classifier”；
- novelty 被迫缩成一个 benchmark-specific science domain。

## 12. Anti-narrowing contract

允许收窄的是**测量**，不能收窄的是 scientific title。

如果 N1/D0 后只能安全声称：

> “在某个材料数据集里，某一类合成假设的 testability direction 与 plausibility direction 不同”

则本项目停止，不把它包装成 ACL/EMNLP 论文。

## 13. 下一步

```text
1. source/provenance audit
2. 检查 mother datasets + materials artifacts 是否能自然得到独立 P/T targets
3. 统计 2×2 support / attrition
4. 冻结 capability-only D0
5. 过 behavioral/source gate 后才允许 hidden-state work
```

**Current model-call authorization: FALSE.**
