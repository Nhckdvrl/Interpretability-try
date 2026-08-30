# 018 — Stock–Flow Correlation Intrusion

**中文一句话：** 模型明明算对了“流入减流出”，为什么最后判断库存涨跌时还是会被最显眼的 inflow 走势带跑？

**Status:** `D0-v2 COMPLETE / NO-PROMOTE / NO-MI / TERMINAL (2026-08-31)`
**Created:** 2026-08-30
**Top-10 rank:** #5
**Primary builder:** `src/stock_flow_intrusion/build_bank.py`

---

## 1. 研究问题

库存、人口、水库水量、账户余额都属于 stock；生产/销售、出生/死亡、流入/流出属于 flow。

最基本关系是：

```text
stock(t+1) = stock(t) + inflow - outflow
```

经典认知科学发现，人即使知道这个公式，也常犯 **stock-flow failure**：看到 inflow 上升，就直觉认为 stock 也上升，忽略了 outflow 或 net flow。

我们想问 LLM 是否有更尖锐的版本：

> **模型在前一问已经正确算出 net flow 为负，说明局部算术能力存在；但下一问判断 stock trajectory / peak 时，是否仍然错误地跟随 inflow 的表面趋势？**

如果成立，它不是“不会减法”，而是一个 **local computation correct -> downstream integration ignores it** 的 cognition–behavior dissociation。

---

## 2. 人类 mother phenomenon

Cronin, Gonzalez & Sterman (2009), *Why Don't Well-Educated Adults Understand Accumulation?* 系列工作系统展示 stock-flow failure，并提出 **correlation heuristic**：人倾向让 stock pattern 跟 inflow / flow pattern 相似。

Overview / author page: https://mitmgmtfaculty.mit.edu/jsterman/whydontwelleducatedadultsunderstand/
DOI: 10.1016/j.obhdp.2008.03.003

后续研究反复发现这个 bias 很稳健，并讨论 global-vs-local processing 等解释。

这给本题一个非常自然的 mother phenomenon：我们不是发明一个 LLM-only puzzle。

---

## 3. Novelty boundary

### 已知

- 人类存在 stock-flow failure；
- LLM 在算术、时序、图表理解上会犯错；
- cognitive-bias benchmark 已经测试许多人类 bias 在 LLM 中是否重现。

### 我们真正要找的对象

不是“LLM 会不会答错 stock-flow 题”。

我们只关心 recognition-gated / computation-gated dissociation：

```text
Q1: net flow direction? -> correct
Q2: stock direction / peak? -> wrong in inflow-following direction
```

更强一点：在同一 real-world window 中，模型明确说 `outflow > inflow`，却仍然说 storage 会涨，因为 inflow 在涨。

这对应一个非常具体的 mechanistic question：**正确 net-flow representation 为什么没有被 downstream stock readout 使用？**

**Novelty boundary:** 现有 stock-flow 人类文献与通用 LLM bias work 没有直接建立这种“局部 net-flow 计算已正确但 downstream stock readout 仍受 correlation heuristic 入侵”的 mechanistic phenotype。该 registered phenotype 已由 D0-v2 直接检验并失败，不再追加 N1 或把题目缩成 polarity/prompt/model-specific 子题。

---

## 4. 数据：ResOpsUS

Steyaert et al., *ResOpsUS, a dataset of historical reservoir operations in the contiguous United States*。

Scientific Data: https://doi.org/10.1038/s41597-022-01134-7
Zenodo: https://zenodo.org/records/6612040

数据包含：

- 679 个 major reservoirs；
- daily inflow；
- daily outflow；
- storage；
- elevation；
- evaporation（部分）；
- 时间大体覆盖 1930–2020，不同 reservoir 覆盖不同。

这是天然数据，不是我们编的“浴缸故事”。

现有 builder：

`preflight/d0_stock_flow_correlation_intrusion/build_from_resopsus.py`

---

## 5. 程序自动找什么窗口

我们不随机取 window，而是自动找**诊断性冲突窗口**：

```text
inflow trend: up
net flow / observed storage delta: down
```

或：

```text
inflow reaches peak at t1
storage reaches peak at t2 != t1
```

优先第一类，因为 wrong destination 最清楚。

程序对每个 reservoir/time window 计算：

- Δstorage；
- inflow - outflow；
- cumulative net flow；
- inflow slope；
- storage slope；
- closure error；
- missingness；
- source/agency/schema metadata。

只有 accounting 基本闭合的窗口才进入主 bank。

---

## 6. 为什么要用真实数据，而不是 synthetic tank

Synthetic tank 很容易做无限数据，但会让 paper 退化成“LLM 数学题 benchmark”。

真实 reservoir 的好处：

1. 科学对象仍然是普遍的 stock-flow cognition；
2. 数值不是为了诱导模型而设计；
3. 可以检查 phenomenon 是否跨 reservoir / time / scale；
4. 后续可以加 official population accounting 做第二 source family。

D0 第一轮只用 ResOpsUS，不需要一开始凑三 domain。

---

## 7. D0 prompt 结构

对一个真实 window，用表格形式给 daily data。

### Step 1 — LOCAL NET FLOW

问：

```text
On the final day / over this interval, is net flow positive or negative?
```

或者要求算 `inflow - outflow`。

### Step 2 — STOCK

在同一上下文继续问：

```text
Over the same interval, is reservoir storage increasing or decreasing?
```

### Step 3 — PEAK（secondary）

问 storage peak 出现在哪天，与 inflow peak 区分。

同时做 independent prompt 版本，避免 Q1 本身教学式提示改变 Q2。

---

## 8. Money cell

最关键的 item：

```text
net_flow_answer = correct
stock_answer = wrong
wrong_stock_direction == inflow_direction
```

定义：

```text
intrusion_rate =
P(stock follows inflow incorrectly | net flow recognized correctly)
```

对比 baseline wrong directions。如果模型只是随机错，不应特别偏向 inflow。

还可以计算 logit attraction：

```text
P(stock-up | inflow-up, net-down)
vs
P(stock-up | inflow-down, net-down)
```

---

## 9. Fatal controls

### Accounting closure

真实水库可能有 evaporation、单位转换、测量误差。若 `Δstorage` 与已知 flows 不能基本对应，不能把该 window 当 deterministic oracle。

### Unit sanity

不同 agency 的 unit 必须 source-grounded，不得猜。

### Presentation

第一轮用 table/text。Chart 只能是后续 modality factor，不能让“读图能力”成为主 confound。

### Arithmetic capability

如果模型连 Q1 net flow 都算错，item 不进入 main phenotype denominator。

### Inflow vs net-flow distinction

wrong answer 必须是**朝 inflow 方向**，不是任意错误。

---

## 10. PROMOTE / KILL

### PROMOTE

- 两个模型家族都有充足 net-flow-correct denominator；
- 在 `inflow direction != storage/net direction` 窗口中，stock 错误显著偏向 inflow；
- effect 在 reservoir-cluster bootstrap 下稳定；
- 改数值尺度 / 表格顺序后方向不变；
- 至少第二个自然 stock-flow source family（例如 official population accounting）可复现。

### KILL

- net-flow gate 后错误变成随机；
- 所有效应来自 arithmetic failure；
- source accounting 不闭合；
- 只有图表形式出现；
- 换表格顺序/单位后完全消失；
- 真实数据没有足够 diagnostic windows。

---

## 11. Mechanistic story

如果行为成立，核心不是“哪层会减法”，而是：

```text
模型已经形成正确 net-flow state
为什么最终 stock judgment 没有使用它？
```

候选 fork：

1. **correct but transient**：net-flow representation 在中层存在，后层消失；
2. **parallel heuristic**：inflow trend 与 net flow 同时存在，最终 readout 权重偏 inflow；
3. **object-attention bias**：更显眼的单变量 inflow 得到更强 attention；
4. **binding/integration failure**：模型不能把 rate-of-change state 积分到 stock state；
5. **verbal shortcut**：自然语言里的“increasing inflow”激活“increasing level” lexical association。

实验：

- layer-wise probes for inflow / net-flow / stock direction；
- activation patch correct net-flow state into stock-answer run；
- counterfactual swap inflow/outflow labels while preserving net；
- numeric vs verbal representation；
- causal ablation of inflow-trend features；
- compare table vs equation vs prose。

---

## 12. 最小执行顺序

```text
1. 下载并解压 ResOpsUS
2. 跑现有 builder
3. 看 closure / schema / qualifying-window counts
4. random 20 windows 只核 source mapping
5. 冻结 window length 与 prompt
6. Qwen3-8B + Gemma-3-12B-IT smoke
7. 如果有 directional intrusion，再加第二自然 source family
8. N1 closure 后做 MI
```

---

## 13. D0 v1 implementation（2026-08-30）

### Source and window audit

D0 使用官方 ResOpsUS v2（Zenodo record `6612040`，archive MD5 `d0684cbacf6196c246c73b858ab5b752`，CC-BY-4.0）。官方 schema 明确规定 storage=MCM、inflow/outflow=m³/s，因此最终 builder 不做任何 unit inference。

对全部 678 个 `time_series_all` files 扫描连续 7-row window。初始 storage 使用第 1 行，prompt 展示随后 6 天 flow；这是因为 release 中 `S[end]-S[start]` 与日期 `start+1...end` 的 daily-average flows 对齐。进入 bank 的窗口必须：

- source 未被官方 `INCONSISTENCIES_NOTED` 标记；
- inflow / outflow 非负、无缺失，日期逐日连续；
- rounded prompt 数字与原始数值的 net sign 一致；
- observed storage delta 与 converted cumulative net sign 一致，closure error ≤10%；
- net margin ≥5%；
- inflow 与时间的绝对 correlation ≥.60，range / mean ≥.15。

过滤后仍有 719,074 个 eligible natural windows、274 个 reservoirs。最终 deterministic bank 冻结为 `net/storage direction × inflow trend direction` 四 cell 各 150，共 600 windows / 200 reservoirs；每个 reservoir-cell 最多 2 条，同库任意入选 window 起点至少间隔 30 天。40/40 source audit sample 已逐值回查官方 CSV。

### Why the full 2×2 is necessary

只保留 conflict window 时，binary stock 题的任何错误都必然朝 inflow direction，无法证明 directional attraction。D0 因而在控制 net direction 后估计：

```text
0.5 * [P(stock-up | net-up, inflow-up) - P(stock-up | net-up, inflow-down)]
+ 0.5 * [P(stock-up | net-down, inflow-up) - P(stock-up | net-down, inflow-down)]
```

正值才表示 inflow trend 对 stock readout 有条件性侵入。

### Recognition gate and controls

每个 item 的 net direction 必须在 2 个 column orders × 2 个 net-option orders 下全部正确，才进入 stock analysis。stock-up probability 再跨 2 个 column orders × 2 个 stock-option orders平均。五个条件为：

1. `direct`；
2. `actual_net_history`（写入模型自己识别出的 semantic net direction，不复用 A/B token）；
3. `explicit_correct_net`；
4. `masked_net_history`；
5. `formula_reminder`。

主推断按 `dam_id` 做 10,000 次 cluster bootstrap。冻结 PROMOTE 门槛见 `configs/d0_contract.json`；至少两个家族在 actual 与 explicit-correct-net 条件均显示 ≥5pp、CI 下界过零的 inflow attraction，且两个 net directions、两个 column orders 方向一致，才进入第二自然 source family。

### N1 boundary

检索到最接近的公开先例是 2023 MetaSD 个人博客的一次 ChatGPT department-store 演示，并非系统实验。人类 stock-flow / correlation-heuristic 文献很成熟；2026 FinIndices 研究长财报中的 accounting stock-flow caliber mismatch，但不测 recognition-gated correlation intrusion。当前未发现同行评审工作使用真实自然 flow series、2×2 directional estimand、三模型家族和 local-correct/downstream-use dissociation 的组合。

---

## 14. D0 v1 result

三家族均完成冻结 bank 的完整运行（每家 14,400 raw rows），联合决策为 `NO-PROMOTE`。严格 recognition gate 要求同一 item 在 2 column orders × 2 option orders 下全部答对；通过情况为：

| Family | Gated / 600 | Gated reservoirs | net-down cells | net-up cells |
|---|---:|---:|---:|---:|
| Qwen3-8B | 292 (48.7%) | 154 | 0 / 300 | 292 / 300 |
| Gemma-3-12B-IT | 300 (50.0%) | 156 | 0 / 300 | 300 / 300 |
| Llama-3.1-8B-Instruct | 127 (21.2%) | 94 | 0 / 300 | 127 / 300 |

因此控制 net direction 的主 inflow-attraction estimand 在所有家族均不可估计，四 cell 最低样本量门槛也均失败。失败不是自然数据不足：冻结 bank 的四 cell 各 150；而是模型的 net-flow recognition 对极性和答案顺序不稳健。

Qwen 与 Gemma 对 net-up 近乎满分，但 net-down presentation-level accuracy 分别只有 9.8–29.8% 和 11.5–20.7%。Llama 的 net-down canonical-option accuracy 为 82.0–100%，reversed-option accuracy 为 0%，显示强答案位置依赖。不能据此选取 canonical-only 或 net-up-only 子集，因为那会改变冻结 gate 并把宽题收窄。

在仅作诊断、不能支持主 claim 的 net-up gated 子集中，写入正确 semantic net direction 后：Qwen stock accuracy 为 99.3–99.5%，其 inflow-direction difference 为 −0.23pp（95% CI [−1.43, 0.81]）；Gemma 为 93.0–97.8%，difference 为 −4.91pp（95% CI [−8.29, −1.72]）；Llama difference 为 +1.67pp（95% CI [0.32, 2.97]），低于冻结的 5pp 门槛。三者没有形成所需的跨家族正向 intrusion。

完整方法、失败审计与后续判断见 `D0_V1_REPORT.md`；机器可读联合结果见 `results/d0_analysis.json`。本题不进入第二自然 source 或 mechanistic intervention 阶段。

---

## 15. D0-v2 bounded repair and terminal result（2026-08-31）

D0-v2 保持同一 600-window natural bank、四个 semantic cells、五个 stock
conditions、stock readout、dam-cluster bootstrap 与 PROMOTE 门槛，只把 A/B
net-recognition gate 改为 exact one-token `positive` / `negative` semantic
scoring。column order 只做 diagnostic，不再要求每个 presentation 都正确。

Qwen、Gemma、Llama 三个必需家族和第四个 Phi 家族均完成 13,200-row full
run。四家 gated cell counts 分别为：

- Qwen: `102 / 45 / 148 / 149`；
- Gemma: `39 / 14 / 150 / 150`；
- Llama: `150 / 150 / 0 / 3`；
- Phi: `79 / 10 / 149 / 150`。

没有家族通过每 cell ≥50 的冻结 gate。更关键的是，可估计三家的
`actual_net_history` inflow attraction 为 Qwen +1.23pp（95% CI −0.16 至
+2.77）、Gemma −3.88pp（−6.36 至 −1.63）、Phi +0.75pp（−0.57 至
+2.01）；均未达到 +5pp，Gemma 还是显著反向。Llama 只有 negative-net
stratum 可估计，不能做 positive-only/negative-only rescue。

最终判定为 0/4 family `NO-PROMOTE / NO-MI`。不再做 numeric D0-v3、第二
source、机制实验或追加 N1；完整裁决和可复现信息见 `D0_V2_REPORT.md`，机器
结果见 `results/d0_v2/analysis.json`。
