# Finding Rules — 唯一权威选题协议

版本：2026-08-31  
状态：`AUTHORITATIVE DISCOVERY PROTOCOL`

本文件是**唯一需要维护的选题规则**。旧的 `NATURAL_QUESTION_GATE.md`、`SCIENTIFIC_SUBSTRATE_GATE.md`、各轮 funnel / addendum 只保留历史证据，不再各自定义流程。

目标：为 ACL / EMNLP / NAACL 风格 mechanistic interpretability 找到真正值得做的问题。允许最后为 0；不为数量降低标准。

---

## 1. 今天最大的修正：不再“猜一个现象，然后赌 G0”

过去最主要的失败不是模型实验做得不够，而是**候选生成方式错了**：

```text
听起来很自然的 distinction
→ 找一个能拼出 contrast 的 dataset
→ 猜模型也许会有某种 failure
→ 跑 3–4 家族昂贵 G0
→ 发现 effect 不存在 / scorer 有问题 / gold 不对 / metadata 泄漏
```

这条路线现在禁止作为默认找题方法。

真正要模仿 Hamdi 的是：

```text
一个强 mother 已经建立了 object O
→ 看 mother 到底测了 O 的哪些属性
→ 找同一个 O 上一个现实中独立、但 mother 没问的轴 B
→ 尽量继承 mother 的 unit / readout / recipe
→ 先证明“B 是未被问过的问题”，而不是先赌“模型会不会出错”
```

实体题的结构是：

```text
mother: known / unknown entity
new axis: real / fictional entity
```

两轴本来就在世界里不同；著名虚构实体提供 `known + fictional` 的自然 cross-cell。新题不是猜一个新 failure，而是在**同一个 entity representation** 上问 mother 没问过的 ontology 属性。

随机选择题是第二种合法路线：随机偏置本身早已肉眼可见并被 prior work 建立；新问题不是“会不会偏”，而是**模型是否有 random/arbitrary-choice state，以及这个 state 是否就是控制 entropy 的变量**。因果分析最后推翻了单一 dial 直觉，得到 switch/reader 与 downstream writer，并预测出 gated intervention。

---

## 2. 只允许两种候选生成路线

### Route A — Mother omitted-axis extension

适合 factorization / representation object。

必须满足：

1. 有一个**具体 strong mother**，而不是宽泛领域；
2. mother 已经稳定测量 object `O`；
3. 新轴 `B` 是 `O` 在现实世界中的独立属性，不是我们为论文发明的 label；
4. 有天然 counterexample / cross-cell 证明 `A != B`；
5. mother 没有已经回答 `B`；
6. 能继承 mother 的大部分 measurement recipe；
7. 不需要先跑昂贵多家族实验才能知道“这个问题是否存在”。

标准句式：

> Paper M established A about object O. But A does not answer B, because B is an independently meaningful property of the same O. Natural A/B counterexamples already exist, and M's validated recipe can be extended to ask B.

### Route B — Established anomaly → unasked causal computation

适合 failure-mechanism。

必须满足：

1. headline behavior **已经存在**：prior work、公开 raw outputs，或普通 prompt 下极易观察；
2. 最好已经在当前/相近 open families 上出现，不从纯人类 bias 外推；
3. 新问题不是“哪个 layer/head”，而是一个 prior work 没问过的内部 computation/state；
4. 至少有两个真正 competing causal mechanisms；
5. 不同机制会预测不同干预或泛化结果；
6. 即使最终机制很简单，答案也会改变我们对该 behavior 的解释。

因此，`mother behavior → mechanism` **不再一刀切禁止**。禁止的是 generic localization；允许的是像 random-choice 一样，提出一个未被问过、可被因果实验证伪的内部 scientific object。

---

## 3. Mother-extension card：任何新题先填这个

没有这张卡，不进入文献深搜、数据构建或 GPU。

```yaml
mother:
  paper:
  scientific_object:
  established_result:
  statistical_unit:
  measurement_recipe:

extension:
  new_question:
  omitted_axis_or_internal_object:
  why_mother_does_not_answer_it:
  natural_counterexample_or_cross_cell:
  what_can_be_inherited_from_mother:

existence:
  route: omitted_axis | established_anomaly
  behavior_already_exists: true|false|not_applicable
  evidence:
  requires_expensive_G0_to_discover_the_question: true|false

novelty:
  semantic_aliases: []
  strongest_neighbor:
  title_level_collision: true|false

mechanism:
  hypothesis_1:
  hypothesis_2:
  different_prediction:
  possible_surprising_intervention:

verdict: CONTINUE | KILL
```

硬规则：`requires_expensive_G0_to_discover_the_question = true` 时默认 KILL。

---

## 4. 正确的成本顺序

```text
1. concrete mother
2. omitted-axis / unasked-computation card
3. semantic negative-memory search
4. strongest-neighbor/title collision
5. cheap substrate / artifact / existing-output audit
6. only if necessary: small faithful behavior sanity
7. formal S0
8. N0/N1 closure
9. registration
10. mechanistic experiments
```

注意：S0 的职责是**确认 measurement 可执行**，不是替我们发现一个可能不存在的 behavior。

Fresh 3–4-family G0 是后期验证工具，不再是候选生成工具。

---

## 5. Cheap falsifier：先用最便宜的东西杀

优先级从高到低：

- mother paper 已有 per-model table / appendix；
- released raw predictions / logits / outputs；
- row-level artifact + cross-cell count；
- deterministic majority / length / position / metadata baseline；
- scorer sanity；
- 5–20 个普通 faithful examples；
- 最后才是 fresh multi-family inference。

如果一个 metadata/length baseline 已经比语义模型更强，先解释 substrate，不要继续 MI。

---

## 6. 七类通用死亡模式

以后不要为每个死题发明一套新哲学。绝大多数失败都落在下面七类。

### F1 — Behavior lottery / synthetic-first

我们只是觉得某 failure “应该会有”，却没有既有 open-model evidence；或者必须靠 synthetic 2×2 / 特殊 prompt 才出现。

**处理：** 不跑大 G0；回到 mother。

### F2 — Mother / neighbor ownership

mother 已经拥有 headline object，或 strongest neighbor 已经问了同一个轴。剩余 novelty 只是在换 dataset、model、language、subtype 或 MI tool。

**处理：** KILL；semantic rename 不算新题。

### F3 — Substrate mirage

哲学 distinction 很漂亮，但没有独立 gold、row-level artifact、自然 cross-cell；第二轴其实是 proxy；schema 中有字段不代表它就是标题变量。

**处理：** KILL-DATA。不要自己补 central labels，也不要用 LLM judge 替代。

### F4 — Measurement / denominator invalid

scorer、option position、format、长度、metadata、prompt interface 或 capability floor 制造了 apparent effect。

**处理：** 先修 measurement；修完 effect 消失就终止。

### F5 — No common phenotype across families

不同模型“都错了”不等于它们在犯同一种错；强模型消失也不能靠弱模型续命。

**处理：** 没有同方向、同结构 signature 就 KILL。

### F6 — Post-hoc rescue / scope drift

看完结果后改 subset、threshold、prompt、label、模型、标题；或者为了 clean data 把理论 factor 全过滤掉。

**处理：** 原题死亡；新 estimand 必须从头重新过协议。

### F7 — Mechanistically weak

结果最多是“某信息可 probe”“某 layer 更强”“某 head 相关”；没有 competing causal hypotheses，或一个简单外部 wrapper 无论机制如何都解决问题。

**处理：** 不作为当前高标准候选。

---

## 7. 过往失败告诉我们的统计事实

`S0_FUNNEL_2026-08-31.md` 的 48 个 idea 中：

- 24 个首先死于 behavior 不存在、不稳定、synthetic-only 或 scorer artifact；
- 8 个死于独立 gold / artifact / natural cross-cell 不成立；
- 14 个在进入 S0 前就被 mother / direct successor 占据；
- 只有 2 个走到更后面的 N0/N1，仍然死亡；
- **0 survivor**。

这说明主要瓶颈不是“MI 做不出来”，而是**candidate generation 太宽、太猜、太晚做 ownership audit**。

因此未来优化方向不是再增加 gate，而是让进入 gate 的 idea 本来就来自更窄、更可靠的 mother extension。

---

## 8. S0：只保留最必要的合同

### Route A / omitted-axis

注册前确认：

- 两轴定义独立于模型；
- central gold 不由我们/LLM 临时创造；
- row-level artifact 真正拿到；
- natural cross-cells 程序计数；
- 随机审至少 20 rows；
- mother recipe 可合法延伸；
- no synthetic 2×2 manufacturing。

### Route B / established anomaly

注册前确认：

- exact behavior 在 analyzable open checkpoints 上存在；
- 至少 2/3 genuinely different families 同一 qualitative signature；
- ordinary faithful prompt；
- raw item outputs 保存；
- capability denominator 合法；
- effect substantial，不是几个百分点噪声；
- hard kill 预先冻结。

如果 prior work 已经给出足够 current-open-family evidence，S0 可以复核现有 artifact，而不要求重新烧一遍大 G0。

---

## 9. Novelty：两次攻击就够，不再堆文档

### N0 — title ownership

只问：

> mother 或最强 neighbor 是否已经可以用一句话回答我们的新 question？

如果可以，KILL。

### N1 — causal/mechanistic occupancy

只问：

> 即使 title 还没撞，是否已有工作已经做了我们关键的 factorization / causal test / intervention？

如果答案是 yes，而且我们只能靠 subtype/domain/method 差异续命，KILL。

不再为每个候选写长篇 novelty essay。保存 strongest 3–5 neighbors 和一段 decisive difference 即可。

---

## 10. PASS-REGISTER 的真正含义

只有同时满足：

```text
strong mother provenance
+ no behavior lottery
+ new omitted axis / unasked causal computation
+ semantic negative-memory clean
+ strongest-neighbor clean
+ valid substrate / existing behavior
+ no artifact/capability problem
+ broad enough narrative
+ >=2 competing causal mechanisms
+ plausible surprising prediction/intervention
```

才叫 `PASS-REGISTER`。

`HOLD`、`PRE-S0`、`frontier`、`under audit` 都不计入目标五题。

---

## 11. 仓库文档纪律

当前权威层只保留三份：

1. `README.md` — 入口与目录；
2. `phenomenon_miner/FINDING_RULES.md` — **唯一选题协议**；
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — 当前状态。

失败的一般规律只维护在 `phenomenon_miner/FAILED_TOPICS.md`。

`rejected_candidates/` 内逐题文件是**证据库**：只有当新题语义接近时搜索，不要求下一轮完整通读所有 addendum/domain logs。

旧 gate / funnel / N0 文件保留历史 provenance，但不再成为并列 authority。

---

## One-line discipline

> **不要问“模型还可能有什么有趣的错？”；先问“这篇强 mother 已经测清的 object，还有哪个现实属性或内部 computation 是它明确没有问的？”**
