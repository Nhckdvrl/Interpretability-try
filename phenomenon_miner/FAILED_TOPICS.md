# Failed-Topic Lessons — 通用负知识

日期：2026-08-31  
状态：`AUTHORITATIVE GENERAL FAILURE MEMORY`

本文件不再逐题复述几十个 rejection。逐题证据留在 `archive/` 与 `rejected_candidates/`；这里只维护**能改变下一轮选题行为的一般规律**。

---

## 1. 最重要的结论

过去的大多数失败并不是“实验运气差”，而是候选生成阶段就犯了同一种错误：

> **先想一个听起来有趣的 distinction / mechanism，再赌模型上存在对应 behavior。**

`S0_FUNNEL_2026-08-31.md` 的 48 个 idea 给了很清楚的统计：

| first fatal blocker | count |
|---|---:|
| behavior absent / unstable / synthetic-only / scorer artifact | 24 |
| independent gold / artifact / natural cross-cell absent | 8 |
| mother / direct successor already owns title | 14 |
| later N0/N1 collision | 2 |
| survivor | **0** |

所以真正该优化的是**idea source**，不是继续增加更多 downstream gate。

---

## 2. 七类一般性失败

### F1. Behavior lottery

症状：

- “人类有这个 bias，所以 LLM 也许有”；
- “这个 mechanism 很漂亮，如果 effect 出现就很好”；
- 需要先跑三四个模型才能知道题是否存在；
- 只有 synthetic template 能表达现象。

为什么危险：GPU 被拿来做选题；null 之后除了“没有现象”什么都没得到。

新规则：failure 题必须先有 prior/open-output/everyday evidence；否则不进入 expensive G0。

---

### F2. Mother ownership / rename novelty

症状：

- mother 已经报告 headline behavior，我们只剩 “where / why / causal?”；
- strongest neighbor 已经直接命名同一 distinction；
- novelty 只能靠换 dataset、语言、模型、subtype、prompt 或 MI tool。

关键修正：`mother → mechanism` 不是绝对非法；**generic localization** 才非法。像 Hamdi random-choice 那样，如果新问题是 prior work 没问过的内部 computation，存在 competing causal hypotheses，并能推出新 intervention，则仍可成立。

新规则：问“旧论文一句话能否已经回答我们的 title question？”如果能，直接 KILL。

---

### F3. Substrate mirage

症状：

- schema 里有两个字段，就以为有两个 scientific axes；
- 第二轴其实是 proxy；
- paper 给 aggregate statistics，却没有 row-level matched population；
- gold 需要我们自己标或用 LLM judge 补；
- natural cross-cell 数量没真正数过。

典型教训：数据“存在”与 scientific object “可测”完全不同。

新规则：row-level artifact、gold provenance、cross-cell count、random audit 必须在注册前完成。

---

### F4. Measurement / denominator artifact

症状：

- exact-string scorer 把语义正确答案判错；
- option position / answer format / prompt wording 主导结果；
- metadata、长度、编号等 stupid baseline 比模型更强；
- capability floor 不成立，却硬谈 recognition→use dissociation。

NTSB 是一个很好的终局例子：数据门通过，但 relevance task 本身只有 0.54–0.64 BA，且 bookkeeping/length 特征能达到更高分。此时继续解释 role selection 没有意义。

新规则：先做 stupid baseline、scorer sanity、capability denominator，再看模型故事。

---

### F5. “大家都错”但不是同一种错

症状：

- 平均指标都低，却不同家族 wrong destination 不同；
- 一家有 target effect，另一家是 generic failure，第三家方向反了；
- 只有弱模型出现，强模型干净。

新规则：要的是跨家族**同一 structural signature**，不是“都没做对”。

---

### F6. Post-hoc rescue / scope drift

症状：

- 看结果后换 subset、threshold、prompt、readout；
- extreme cell 有 effect 就把标题缩成 extreme cell；
- 为了 clean matching 把理论 factor 当 exclusion；
- 换一个 dataset 继续寻找同一个 dead object。

新规则：原 estimand 一旦失败就结束。真正换 scientific object 必须重新从 mother card 开始，不能继承 survivor 身份。

---

### F7. Mechanistically weak / method-closed

症状：

- 最终贡献只是 probe accuracy、layer localization、一个 SAE latent；
- competing hypotheses 实际没有不同预测；
- 机制无论是什么，一个简单 external verifier/wrapper 都同样解决问题；
- 结论高度符合默认直觉，没有 Hamdi-style surprise。

新规则：MI 必须能**区分因果计算**，最好推翻一个自然直觉并推出新的 intervention。

---

## 3. 我们以前过度使用的坏模板

以下不是“永远不能做”，但已经证明是高风险默认模板：

```text
knows X but does not use X
reader vs writer
switch vs dial
representation exists → is it causal?
X != Y because dataset has both labels
human cognitive bias → test LLM replication
same behavior, different domain/model/language
```

这些词本身不是问题；问题是它们太容易让我们**从机制形状反推 scientific question**。

今后必须先有 concrete mother 和 omitted question，再允许出现这些机制词。

---

## 4. 真正成功/接近成功的共同结构

### 014 Alias Entrainment Transfer

先有真实 broad entrainment effect；复杂 controls 是为了区分**已经存在的 effect 的解释**，不是制造 effect。即使 reference-specific story 被杀，cross-surface transfer 仍然成立。

### Hamdi entity real/fictional

先有 mother 对 entity knowledge/familiarity 的 validated recipe；新轴是同一个 entity 的 ontological status，天然与 familiarity 可分，known-fictional cross-cell 在现实中大量存在。

### Hamdi random-choice

随机偏置先存在；新问题是内部是否有 arbitrary-choice mode，以及它是否直接控制 entropy。直觉被 causal result 修正为 reader/switch + separate writer，并自然推出 gated edit。

共同点不是某个 MI 方法，而是：

```text
base object 已经可靠
→ 新问题不是靠实验赌出来
→ decisive alternative 很清楚
→ mechanism 结果能改变解释
```

---

## 5. 下一轮看到一个 idea 时只问五件事

1. **它从哪篇具体 mother 来？**
2. **mother 已经测清的同一个 object 是什么？**
3. **我们问的到底是哪一个 mother 没问的现实轴 / internal computation？**
4. **不跑昂贵新 G0，我为什么已经知道这个问题值得存在？**
5. **两种可能机制会做出什么不同预测？**

有一项答不清，就不要进入候选池。

---

## 6. 详细负知识怎么用

`rejected_candidates/` 和 `archive/` 继续保存逐题证据，但它们不再是每轮必读长清单。

正确用法：

```text
新 mother-extension card
→ 写 5–10 个 semantic aliases
→ 在 rejected/archive 中定向搜索
→ 命中同义 dead family 才读对应详细文件
```

不要每轮从头通读九个 addendum；也不要因为没记住某个具体旧题就重新发明它。

---

## One-line lesson

> **我们失败得最多的不是“机制没找到”，而是“把一个还没有 scientific object 的猜测送进了实验”。**
