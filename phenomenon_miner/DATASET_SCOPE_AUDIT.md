# Dataset Scope Audit — 防止造数据时把科学问题越筛越窄

版本：2026-08-29  
状态：`MANDATORY D0 SCOPE-INTEGRITY RULES`

本文件是 [`FINDING_RULES.md`](FINDING_RULES.md) 中 D0 source-feasibility 的强制组成部分。它解决一个和“数据有没有”“gold 对不对”不同的问题：

> **最后造出来的数据，还是不是原来那个科学问题的数据？**

014 Alias Entrainment Transfer 暴露了一个典型失败：原问题是“同一 referent 的不同 surface forms 之间，contextual salience 是否传播以及如何随 surface relation 改变”，但数据构建逐步加入 `person-only + 四类 alias + non-compositional + opaque_strict + one alias/entity + one direction`，最后把 estimand 偷偷改成了“opaque person alias → canonical name”。每一步单独看都像在“清理 confound”，合在一起却已经换题。

以后所有 D0 / confirmatory D1 都必须通过下面的 scope audit。

---

## 1. 在任何过滤前先冻结 scientific population

先写清楚，不允许从已经过滤后的 dataframe 反推：

```yaml
scientific_population:
  natural_object:
  observational_unit:
  ordered_or_unordered:
  treatment_or_exposure:
  scored_outcome:
  valid_directions:
  domains_or_entity_types_in_scope: ALL | [...]
  theoretically_meaningful_factors: []
  nuisance_variables: []
  measurement_validity_exclusions: []
```

其中 `theoretically_meaningful_factors` 尤其重要。只要某个变量本身可能解释 mechanism / boundary / structural signature，它默认就是 **factor-not-filter**。

典型例子：

- surface overlap / compositionality；
- entity type / domain；
- direction；
- difficulty / popularity；
- model capability gate；
- ambiguity；
- evidence strength；
- relation type；
- prompt/frame family。

这些变量可以成为主效应、interaction、stratum、sensitivity analysis；不能因为“最干净的子集更容易解释”就在 construction 阶段删掉。

---

## 2. 强制分成四层数据对象

### A. `SOURCE / RAW BANK`

尽可能忠实保留 natural source 中属于 scientific population 的全部单位，只做 source-level dedup 和显然无效的解析修复。

允许：

- 去掉空值、损坏记录、重复模板实例；
- 保留 provenance / source category / raw IDs；
- 给结构变量打标签。

默认不允许：

- 只留一个 domain/entity type；
- 只留“最干净”的结构层；
- 为了统计独立每实体只留一条；
- 为了 effect 更可能显著设置 popularity / length / confidence floor；
- 因为某个 control 不好找就从 raw bank 删除 treatment item。

### B. `VALIDITY-ELIGIBLE BANK`

这里只允许做**测量定义本身所需**的 exclusion。

例如：

- scored target 已经字面出现在 treatment context，导致所谓 cross-surface readout 变成 EXACT；
- gold 无法独立验证；
- treatment/control 实际同指，破坏 contrast；
- prompt leakage 让答案直接出现；
- source record 根本不属于预先定义的 natural object。

判断问题：

> **如果不删这条，测到的还是同一个量吗？**

若答案是“还是，只是更难/更杂/效应可能更小”，那它不是 validity exclusion。

### C. `MATCHED / CONTROL-AVAILABLE BANK`

需要 SEMREL、ASSOC、counterfactual、matched distractor 等 control 时，在这一层构造。

关键纪律：

> **control availability 决定某条能不能进入 matched causal contrast，不决定它是否属于 scientific population。**

找不到合格 control 的 item 必须：

- 留在 RAW / VALIDITY bank；
- 在 matched bank 记录明确 `drop_reason`；
- 报告 attrition；
- 不允许无痕消失。

### D. `ANALYSIS STRATA`

所有理论 moderator / nuisance sensitivity / model-specific gate 在这里切：

```text
all valid matched data
→ factor interactions
→ clean / hard / opaque / high-confidence strata
→ capability-gated strata
→ same-type / stricter-control sensitivity
```

**小而干净的 money cell 可以决定某个强解释是否成立，但不能冒充整个 phenomenon 的数据集。**

---

## 3. Factor-not-filter 原则

以下问题必须在每个过滤条件前回答：

```yaml
filter_name:
reason:
class: VALIDITY | MATCHING | ANALYSIS_STRATUM | CONVENIENCE
changes_scientific_population: true|false
removes_a_theoretical_factor_level: true|false
why_not_keep_and_label:
```

规则：

- `VALIDITY`：可以进入 builder 的 hard exclusion；
- `MATCHING`：只能影响 matched-control bank；
- `ANALYSIS_STRATUM`：不得删除 raw/eligible 数据；
- `CONVENIENCE`：禁止作为 scientific filter。

如果一个 filter `removes_a_theoretical_factor_level=true`，默认 **BLOCK**。要真的改变 scope，必须显式改 mother question / estimand，并留下 amendment，不能把它叫“feasibility adaptation”。

---

## 4. 不要用“统计独立”当删数据理由

一个 entity 有多个 surface forms、一个 patient 有多个 visit、一个 document 有多个 evidence span，这些是依赖结构，不等于只能留一个 observation。

优先：

- cluster bootstrap；
- mixed effects；
- entity-equal weighting；
- within-unit aggregation；
- hierarchical model。

只有当多个记录真的是同一 measurement 的重复实现时才 dedup。不能为了让 iid 假设看起来简单就随机/确定性只取一条，从而改变自然分布和 structural coverage。

---

## 5. Direction 必须当成科学变量检查

若自然对象有方向性，先构建**所有测量上合法的方向**。

例如 `A -> B` 因为 B 已经包含在 A 中而发生 target leakage，只能删除 `A -> B` 这个方向；若 `B -> A` 合法，必须保留。

禁止因为某一个方向“更保守”“更容易找到 control”“更接近常见文本模式”，就默认把另一方向从 scientific population 删除。可以预注册某个方向为 decisive test，但数据构造仍应保留方向因子。

---

## 6. Scope attrition table 是 D0 必需品

每个关键阶段都必须输出：

```text
stage
n_rows
n_independent_units
n_entities/domains
factor-level distribution
removed_n
removal_reason
```

至少覆盖：

```text
source
→ raw bank
→ validity-eligible
→ control-available/matched
→ each decisive analysis stratum
```

并同时报告：

- 每个 domain / entity type；
- 每个结构层；
- 每个方向；
- source category；
- 若有 capability gate，则 gate 前后。

如果某一步让一个 factor level 从大量样本变成 0 或接近 0，必须触发 **SCOPE-DRIFT REVIEW**，不能继续默默 freeze。

---

## 7. 两轮人工审计，不只看最终“干净样本”

### Audit A — source-population audit

在任何强过滤前随机看 >=20 个 natural source units，回答：

- scientific object 真存在吗？
- source metadata 的语义和我们以为的一样吗？
- population 里有哪些自然 variation？
- 哪些 variation 是理论 factor，而不是垃圾？

### Audit B — attrition audit

在 matched/final bank freeze 前，再随机看：

- >=20 survivors；
- 每个主要 drop reason 各至少若干例；
- 被大量删除的 factor level；
- 每个 decisive stratum 的代表例。

目的是检查：builder 是在去 artifact，还是在去掉“不够漂亮的科学现象”。

---

## 8. “最干净子集”只能回答更强的解释，不能定义现象

允许这样的证据链：

```text
Broad phenotype on natural population
→ structured gradient across factors
→ decisive matched control
→ clean/hard subset rules out strongest confound
→ mechanism
```

不允许：

```text
先把 natural population 过滤到最可能排除 confound 的小格子
→ 在这个格子上看到 effect
→ 把它写成原始 broad phenomenon
```

前者是科学收敛；后者是 estimand substitution。

---

## 9. Builder 的工程要求

每个正式 dataset builder 必须：

1. raw bank 与 final matched bank 使用不同文件名；
2. 输出 schema 中保留 source IDs、factor labels、drop provenance；
3. 不把 analysis-only 标签硬编码成输出常量；
4. 对 stale/intermediate artefact 使用版本号或 hash，防止旧 shard 被新 pipeline 误读；
5. 有 scope regression tests，至少防止关键 factor 被再次 hard-filter；
6. final freeze 前运行 `scope summary`，打印各层数量和 factor 分布；
7. 旧错误数据不要“就地覆盖后假装一直如此”：保留 git provenance，并明确 superseded。

---

## 10. D0 source-feasibility 的新增 PASS 条件

以后 `d0_source_feasibility_verdict: PASS` 必须同时满足：

```yaml
scope_integrity:
  scientific_population_frozen_before_filtering: true
  raw_bank_preserved: true
  validity_vs_matching_vs_stratum_separated: true
  theoretical_factors_kept_as_labels: true
  all_valid_directions_constructed: true
  dependence_handled_statistically_not_by_scope_collapse: true
  attrition_table_complete: true
  source_population_audit_n: >=20
  attrition_audit_complete: true
  scope_regression_tests_present: true
  verdict: PASS
```

任何一项做不到：

```text
D0 source-feasibility = HOLD-SCOPE
```

不是先注册/先跑模型以后再补。

---

## 一句原则

> **控制 confound 的正确方式是设计 contrast、分层和统计控制；不是把母问题里不够“干净”的部分提前删掉。先保存 population，再收敛解释。**
