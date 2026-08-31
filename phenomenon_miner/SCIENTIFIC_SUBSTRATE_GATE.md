# S0 Scientific-Substrate Gate

版本：2026-08-31

状态：`AUTHORITATIVE PRE-N0/N1 REGISTRATION BLOCKER`

本 gate 解决的问题不是“题目自然不自然”，而是：

> **标题里的 scientific object 在我们注册之前，是否已经有独立、可观测、可规模化、可用于目标 open models 的现实承载物？**

一个自然问题可以没有可做的 scientific substrate。Novelty 不能补数据，漂亮
的机制假设也不能补行为 existence。S0 必须在 N0/N1 之前完成；失败即删除，
不进入 `active/`，不以 `PARK-DATA` 占注册位。

---

## 1. 先分类，再使用不同合同

每个 idea 必须且只能先归入以下一种主类型。

### A. Failure-mechanism

研究对象是模型已经表现出的结构性 failure，例如 arbitrary-choice bias、
stock-flow error、错误更新或错误 routing。

注册前必须证明：

1. failure 在**我们实际能做 causal interpretability 的 open checkpoints** 上存在；
2. 不靠闭源模型、纯人类经典现象或更大不可解释模型外推；
3. signature 在普通、忠实输入上直接可见，不靠事后筛选 synthetic contrast；
4. 至少三个目标家族做 cheap existence sanity，默认要求 2/3 同方向；
5. 行为测量、错误落点和 hard kill 在看结果前定义；
6. effect 足以值得解释，而不是统计显著但实质接近零。

人类 mother 只能说明问题有历史意义，不能代替 open-LLM existence。

### B. Factorization/object

研究对象是两个独立 scientific variables 是否在模型中被分离、绑定或组合，
例如 knowledge 与 existence。注册前必须证明：

1. 两个轴都有独立于模型输出的 objective definition；
2. 两个轴都有可靠 gold，且核心 gold 不由我们或另一个 LLM 临时创造；
3. row-level artifact 已实际取得并可解析；
4. natural population 中所有 decisive cross-cells 都有足够 independent units；
5. 至少随机审 20 条 source rows，并审主要 drop reasons；
6. 不需要 synthetic protocol 才让两个轴“看起来”分离；
7. 分离与不分离都能回答标题级 scientific question。

哲学上清楚的 distinction 不等于可测的 model object。若 aligned controls、
natural cross-cells 或独立 gold 不存在，S0 失败。

---

## 2. 什么算 objective substrate

允许：

- 原始数据的正式人工/专家标注；
- 现实世界中可独立查询且版本锁定的事实；
- 数学、程序、数据库约束直接给出的确定性 oracle；
- 已公开并通过其原任务质量协议的标签；
- 对已经成立的 failure，天然可生成且标签无歧义的 request class，例如
  arbitrary-choice vs deterministic-choice。

不允许：

- 为当前题临时发明核心 annotation ontology；
- 用被测模型或另一个 LLM 产生中央 gold；
- 把 paper-level aggregate 当作需要的 row-level matched population；
- 看到 schema 中有两个字段就假定存在需要的 cross-cells；
- 用 following turn、polarity inversion、proxy rubric 替代标题变量；
- 先造 synthetic 2×2，再把 protocol-induced shortcut 当 scientific object。

人工审核只能验证 source mapping / naturalness / parsing，不能替代缺失的中央
target。需要我们自己标关键变量时，默认 KILL；若未来出现外部 artifact，可作为
全新的候选重新经过 S0，而不是保留 active slot。

---

## 3. Artifact-before-claim 证据要求

S0 PASS 必须留下可复核的本地产物，而不是“某论文看起来应该有”。

### Failure-mechanism S0 card

```yaml
type: failure_mechanism
plain_failure:
target_open_checkpoints: []
faithful_prompt_population:
predeclared_error_signature:
sanity_items_per_family:
family_effects: {}
families_same_direction:
minimum_effect:
artifact_paths: []
synthetic_contrast_required: false
verdict: PASS | KILL
```

必须保存逐条 prompt/output/score、精确 checkpoint revision 和最小汇总。

### Factorization/object S0 card

```yaml
type: factorization_object
axis_a:
axis_b:
source:
version:
license:
downloaded_artifact_path:
artifact_hash:
row_level_loaded: true|false
gold_a_source:
gold_b_source:
gold_independent_of_tested_models: true|false
statistical_unit:
cross_cell_counts: {}
independent_unit_counts: {}
random_audit_ids: []  # >=20
major_attrition_counts: {}
core_gold_requires_new_annotation: false
synthetic_contrast_required: false
verdict: PASS | KILL
```

只有真实运行过 counter 和 audit script 才能填写 counts。论文正文中的样本总数
或字段列表不算。

---

## 4. 成本顺序

新漏斗固定为：

```text
30–50 mother extensions（内部 idea pool，不注册）
→ Natural Question Gate
→ classify: failure-mechanism | factorization/object
→ S0 artifact / open-model existence audit
→ five-minute behavior sanity or objective-label/cross-cell audit
→ N0 mother-inclusion
→ N1 successor collision
→ register only complete survivors
→ freeze D0
→ MI only after D0 promotion
```

S0 的目标是便宜地杀题。不要在一个尚未取得 artifact 或尚未显示 open-model
effect 的 idea 上先花半天写漂亮 novelty narrative。

---

## 5. 注册规则

以下全部满足才允许创建新的 `active/NNN_*`：

```text
Natural Question PASS
+ type-specific S0 PASS
+ row-level artifacts and audit files committed
+ N0 PASS
+ N1 PASS
+ title-level population/estimand unchanged through the audits
= REGISTER
```

注册数允许为 0。不得以“本轮需要三个题”为隐含 objective。30–50 个 ideas
全部失败时，正确输出是一个有证据的 0-survivor funnel。

`PARK-DATA` 只用于**已经注册后外部 artifact 意外消失**等真正状态变化；S0
阶段已知缺 gold、缺 row-level rows 或缺 cross-cells 的 idea 直接记入 rejection
funnel，不进入 active。

---

## 6. 从本轮失败反推的硬规则

- 018：人类经典 failure 不能替代目标 open LLM 上的 effect existence。
- 024：闭源/强 mother effect 不能替代实际 analyzable open pairs 的稳定性。
- 025：形式 distinction 不能替代 natural observable substrate；conflict-only
  synthetic success 必须被 aligned controls 否决。
- 026：没有独立 expert-grounded plausibility/testability 双 gold，S0 KILL。
- 027：没有 implied-assertion / commitment gold，S0 KILL。
- 028：没有可取得的 row-level matched population，S0 KILL。
- 014：先有稳定 open-family transfer effect，变量可外部定义，复杂 controls
  只解释已存在 effect；这是 failure-mechanism S0 的正例。

---

## 7. 一票否决

任一项成立即停止：

1. 核心变量需要我们自己创造 gold；
2. failure 只在 synthetic contrast 或筛选后的特殊子集出现；
3. mother effect 在可解释 open models 上不稳定或实质太小；
4. row-level artifact 未取得；
5. decisive cross-cell 只是从 paper/schema 猜测，未实际计数；
6. random-20 audit 暴露字段语义与标题变量不一致；
7. 为解决 substrate failure 必须缩窄标题或更换 scientific object。

S0 failure 不进入 N0/N1，不允许写代码“先跑看看”，也不允许用机制结果反向
证明 behavior/object 存在。
