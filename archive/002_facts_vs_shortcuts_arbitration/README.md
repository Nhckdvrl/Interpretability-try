# 002 — Facts vs Shortcuts Arbitration in Entity Comparison

**Status:** `PRE-CANDIDATE / BEHAVIOR G0 ONLY`  
**Created:** 2026-08-26  
**Do not start hidden-state analysis before:** `PASS_BEHAVIOR_G0`

## 1. Mother question

自然现象已经由 EACL 2026 Main 明确报告：在“哪条河更长 / 哪个国家人口更多”等实体数值比较中，LLM 即使单独询问时给出的两个数值已经足以导出正确比较，最终 pairwise answer 仍可能与自己的数值知识矛盾，并受实体知名度、出现顺序、语义共现等表面捷径影响。

本项目**不**再研究：

- 模型是否编码实体数值属性；
- 数值比较是否存在低维表示；
- popularity / order / co-occurrence bias 是否存在。

这些已有工作已经覆盖。

如果行为 G0 通过，后续真正要回答的是：

> **当可用的数值事实与表面捷径冲突时，训练完成的 LLM 在推理过程中如何仲裁两类信号？错误发生在事实进入比较之前、比较计算本身，还是后期决策阶段被捷径信号压过？模型规模增长改善的是事实知识，还是仲裁机制？**

这是当前保留的 novelty package；如果后续发现已有工作已经用基本相同的 decisive contrast + causal intervention 回答完，直接 KILL。

## 2. Why this project is allowed to enter G0

与归档的 `001_role_value_binding` 不同，这里不是从 benchmark 总分猜一个细分 failure。

EACL 2026 已经明确报告：

- pairwise comparison 与模型自己的 pointwise numerical extraction 存在系统不一致；
- 小模型的选择常被 popularity / mention order / semantic co-occurrence 预测；
- 大模型更能在自己的数值知识可靠时使用它；
- 原作者代码完整公开。

因此 G0 只需要验证：**在我们当前能跑的开源模型 / 当前 upstream code 上，这种自然 failure 是否仍有足够数量与跨设置复现性。**

## 3. Frozen G0 definition

### 3.1 Public source only

使用原作者公开仓库：

- paper: `Knowing the Facts but Choosing the Shortcut: Understanding How Large Language Models Compare Entities`, EACL 2026 Main
- code: `https://github.com/HeLehm/facts-vs-shortcuts`
- pinned upstream commit: `91d320541f44518266ffa34f6138bd16eb775d83`

**G0 禁止自己合成专门诱导 shortcut 的样本。**

### 3.2 Strict natural failure

一条样本只有同时满足以下条件，才计为目标 failure：

1. pairwise 输出明确选择两个实体之一；
2. ground-truth 两个数值非空、非平局；
3. pointwise numerical extraction 对两个实体都成功、非平局；
4. 由模型自己 pointwise 数值导出的比较方向与 ground truth 一致；
5. 但模型最终 pairwise choice 错误。

即：

```text
模型自己的数值知识 -> 足够导出正确答案
pairwise final choice  -> 错误
```

这比“模型单独能说出大概数字”更严格，也避免把知识缺失误计为 shortcut/arbitration failure。

### 3.3 Margin sensitivity

不人为挑一个 margin 阈值。代码同时报告：

- 0%
- 5%
- 10%
- 20%

最小 relative gap 下的 failure 数量和 Wilson 95% CI。

如果现象只存在于两个数字几乎一样的边界案例，后续机制叙事降级或停止。

### 3.4 Shortcut columns are descriptive at G0

若结果 CSV 已包含：

- QRank popularity；
- cosine co-occurrence；

G0 会额外报告 strict failures 中模型是否选择：

- 第一个实体；
- 更高 popularity 实体；
- 更高 co-occurrence 实体。

**这些只是分层统计，不作为“机制已证明”的证据。**

G0 不训练 probe，不做 activation analysis，也不因为某个 shortcut cue 与错误相关就声称找到了 causal mechanism。

## 4. Frozen STOP gate

默认 gate 是为了保证后续机制实验有足够自然 failure，而不是统计显著性阈值：

```text
总 facts-available cases >= 500
总 strict natural failures >= 50
至少 2 个 model-dataset group 同时满足：
    strict failures >= 10
    failure rate >= 2%
```

可能 verdict：

- `PASS_BEHAVIOR_G0`
- `HOLD_INSUFFICIENT_FACT_AVAILABLE_CASES`
- `STOP_TOO_FEW_NATURAL_FAILURES`
- `STOP_NOT_REPLICATED_ACROSS_GROUPS`

如果 STOP：

- 不改成更弱模型；
- 不主动制造 popularity/order conflict；
- 不只挑少数 dataset / prompt template；
- 不继续 hidden-state probing；
- 不用 SAE / patching 把题救回来。

## 5. If G0 passes: pre-registered competing explanations

机制阶段至少区分三种解释：

### A. 事实进入失败

pointwise 能抽出数值，不代表 comparison prompt 中这些实体数值真正被激活并送入比较过程。

预测：错误样本在事实/数值属性相关内部变量上，早期就与正确样本分离；修复事实进入可恢复答案。

### B. 比较计算失败

两个事实都进入了，但 greater-than / smaller-than 比较过程本身给出错误关系。

预测：实体数值表征仍正确，但 comparison mediator 已经错误；只修复比较中介即可恢复答案。

### C. 仲裁失败

事实和比较关系内部都正确，但后期 popularity/order/co-occurrence 等捷径信号压过 factual path。

预测：错误样本在较晚阶段仍可恢复正确 numerical preference；选择性削弱 shortcut 或增强 factual mediator 可以翻转最终答案，同时不改变实体事实表征。

当前 paper-scale 故事更偏向 C / arbitration；A、B 是必须排除的竞争解释。

## 6. Mechanism prerequisites after PASS only

在进入因果分析前仍需再过：

1. strict failures 在至少两个模型 / 多个 numerical attributes 中成立；
2. 能构造自然 clean/error matched subsets，不主动诱导错误；
3. 能复用已有数值表示 / comparison mechanism 作为技术基础；
4. intervention 可以选择性改变最终比较，而不是全局推动某个 entity/token；
5. 至少一个不同模型家族做 confirmation。

## 7. Method runway

如果支持 A：

- 加强 entity numerical fact 在 comparison context 中的 retrieval / routing；
- 训练 comparison-context factual activation consistency。

如果支持 B：

- 针对 comparison mediator 做 targeted training / representation objective；
- 避免泛化为“再做一个 numerical reasoning SFT”。

如果支持 C：

- 设计 factual-evidence / shortcut arbitration gate；
- 训练“当 factual evidence 可靠时抑制 shortcut”的选择性目标；
- 研究大模型为何比小模型更能根据信息可靠性切换策略，并把这一机制迁移到小模型。

如果 A/B/C 最后导出的方法完全相同，说明机制分析没有真正改变方法设计，需要重新审题。

## 8. Collision audit snapshot (2026-08-26)

### Direct behavioral seed

**Lehmann et al., EACL 2026 Main — Knowing the Facts but Choosing the Shortcut**

已做：自然实体数值比较、pointwise knowledge vs pairwise decision、popularity/order/co-occurrence shortcut、规模效应、CoT。

我们不能重复其行为贡献。

### Strong mechanism neighbor

**El-Shangiti et al., NAACL 2025 — The Geometry of Numerical Reasoning**

已做：实体数值属性的低维线性子空间；对这些子空间做因果干预会改变数值比较结果。

因此不能 claim “首次发现实体数值知识的内部表示 / 因果作用”。它是我们的技术基础，也是 collision 约束。

### Output-gap neighbor

**Yuchi et al., EACL 2026 — LLMs Know More About Numbers than They Can Say**

已做：混合数字表示中，hidden states 可高精度编码 magnitude/ranking，但最终 verbalized comparison 仍错；通过辅助 probe loss fine-tuning 改善输出。

因此不能把本项目写成泛泛的“内部知道但输出错”。我们的独有对象必须是：**实体 factual path 与自然 shortcut path 的竞争与仲裁。**

### Learning-dynamics neighbor

**Pretraining Data Statistics Shape the Phases of Learning Entity Comparison in Language Models (2026 under review)**

已做：训练过程中 frequency heuristic -> position heuristic -> correct comparison 的阶段，以及数据统计如何控制这些阶段。

因此不能 claim “首次发现 entity comparison 在 shortcut 与真实比较之间切换”。我们的对象是**训练完成模型推理时的内部仲裁及 failure localization**。

### Current collision verdict

`YELLOW-GREEN / G0 ALLOWED`

允许行为 G0；不允许在 G0 通过前进入机制。若后续检索发现 inference-time factual-vs-shortcut arbitration 已被基本相同的 causal contrast 完整做掉，直接归档。

## 9. Run

### Install local G0 package

```bash
cd active/002_facts_vs_shortcuts_arbitration
pip install -e '.[dev]'
pytest -q
```

### Fetch pinned upstream

```bash
bash scripts/bootstrap_upstream.sh
```

注意：upstream 自身依赖较重。建议在单独环境里按照原作者 README 安装依赖。

### Run upstream natural tasks

例如：

```bash
bash scripts/run_upstream_model.sh qwen3-8b 64
bash scripts/run_upstream_model.sh olmo-2-7b 64
```

不要先加 synthetic perturbation。

### Run strict G0

```bash
bash scripts/run_g0.sh upstream_results artifacts/g0
```

输出：

- `summary.csv` — 每个 model-dataset 的主统计；
- `sensitivity.csv` — 不同 relative-gap 阈值下的稳健性；
- `strict_natural_cases.csv` — 后续人工 spot-check / mechanism planning 的自然错误样本；
- `verdict.json` — 冻结 STOP/PASS 结论。

## 10. Current local code validation

项目代码写入前已在独立环境运行：

```text
pytest: 7 passed
```

测试覆盖：

- strict failure 定义；
- larger/smaller prompt polarity；
- unknown/tie 排除；
- popularity 只做描述、不进入 failure definition；
- pointwise lowest-perplexity merge 与 upstream 规则一致；
- STOP / PASS gate。
