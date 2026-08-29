# LLM 反直觉现象发现指南

版本：2026-08-29  
定位：**短版 discovery 手册**。旧的长版指南保留在 Git history，不再在当前树重复保存大量与 `PROCESS.md` / `REQUIREMENTS.md` 重叠的流程文字。

正式流程看 [`phenomenon_miner/PROCESS.md`](phenomenon_miner/PROCESS.md)；硬门槛看 [`phenomenon_miner/REQUIREMENTS.md`](phenomenon_miner/REQUIREMENTS.md)。

## 1. 从什么开始找

不是从一个解释工具开始，也不是先决定一个心理学 bias 名字。

优先从下面几类 scientific object 出发：

- 人人能理解的自然 failure；
- 强 mother paper 已经建立但留下明确下一问的对象；
- 两个理论上应分离的心智步骤：`A 会，但 B 不会`；
- 一个规范上应保持 invariance / monotonicity / reversibility / composition 的自然关系；
- 现实任务中长期存在的冲突：prior vs evidence、history vs current state、knowledge vs use、public vs private information 等。

一个候选至少要能写成：

```text
mother question
+ 一句话反直觉矛盾
+ decisive contrast
+ 两个 competing mechanisms
+ hard kill
```

## 2. 找题时文献就要做透

每个候选在 candidate pool 中完成两层 novelty audit：

### N0 breadth

快速搜 exact/near-exact phenotype、mother phenomenon、wrong destination、同义词、repo death family。

### N1 depth

只对 N0 survivor 做：全文、appendix、supplement/code、citation chain、successor、mother inclusion、mechanism occupancy、scale survival。

**N1 不是 smoke 后的步骤。** 如果一个题连 strongest neighbor 的 appendix 都还没看完，它还不是一个确定题目。

## 3. 找题时数据也要做透

每个 promising candidate 必须同时回答：

```text
数据具体在哪里？
版本是什么？
license/adaptation 可以吗？
gold 是什么？
独立单位是什么？
大约有多少 eligible cases？
怎么程序化抽取/配对？
随机看 20 个，真的自然吗？
```

### 最优数据路径

```text
公开自然 benchmark / corpus
+ 原生 gold
+ 足够独立 cases
+ 最小 deterministic transformation
```

### 没有现成 pairs

允许：

```text
公开自然 source
→ 可复现程序变换
→ 可独立证明 gold
→ dry-run 先估 yield
→ 20 例人工 audit
```

不允许先注册题目，再开始发明 generator 或到处找能凑够数量的数据。

## 4. DISCOVERY-PASS 才算“题目定了”

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
```

这之后才 formal registration。注册以后只 materialize/freeze 已锁定数据，不再普通地搜文献或找新数据源。

若 source/recipe 必须实质变化，退回 candidate pool；若 claim 改变，重开受影响 novelty audit。

## 5. Behavior first

题目定了也不等于现象成立。

```text
freeze D0
→ 2-family smoke
→ raw-case/artifact/capability audit
→ 3/5 family + size curve
→ strong-model kill test
→ mechanism
```

现象没过 behavior/generality，不做大规模 probe/patch/SAE 来救。

## 6. 推荐的 candidate card

```yaml
title:
mother_question:
plain_language_contradiction:
decisive_contrast:
competing_mechanisms: []
hard_kill:

n0:
  strongest_obvious_neighbors: []
  verdict:

n1:
  full_text_neighbors: []
  mother_inclusion_test:
  why_not_a_rename:
  mechanism_occupancy:
  scale_survival_risk:
  verdict:

d0_feasibility:
  source:
  version:
  license:
  statistical_unit:
  gold_source:
  extraction_or_construction_recipe:
  estimated_eligible_count:
  feasibility_audit_ids: []
  external_validation_anchor:
  verdict:
```

如果这张 card 填不完整，继续 discovery；不要创建一个 active project 等以后补洞。
