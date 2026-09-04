# 004 — Unringing the Bell：模型知道证据必须排除，却仍被它改变裁决

**Status:** `KILLED BEFORE G0 / PROMPT-AUTHORITY CONFOUND / 006-ISOMORPHIC`  
**Created:** 2026-08-27  
**One-line phenomenon:** **Knowing that evidence must not be used is not the same as not using it.**

> 这不是“模型不懂证据规则”，也不是一般的 irrelevant-context robustness。目标现象是严格分离：模型明确、正确地判断某条证据不得用于裁决，但它的最终裁决仍系统性地向该证据移动。

## 0. Kill decision（2026-08-27）

本候选在模型测试前即终止。核心 contrast 依赖 system/user prompt 如何定义“只使用可采纳证据”，效应可能主要测量 prompt hierarchy、规范措辞和 instruction following。它与 006 的形式同构：显式读出一个 control variable，再测试下游是否按该 variable 门控。换掉 `posterior/reliability` 为 `admissibility` 没有解决 006 的母题人造性。

因此不再运行本目录的 G0，也不得通过调整 system prompt 寻找显著结果。后续候选必须满足：不含 `use/ignore/obey/disregard` 等授权词；gold 由世界结构本身决定；去掉 system prompt 后 relation 仍成立。

## 1. 为什么这像 Hamdi 式问题

Hamdi 的关键不是模型是否见过某个实体，而是拆开两个通常被混写的变量：

```text
familiarity / knowledge of an entity
≠
ontological commitment that the entity is real
```

这里拆开的也是两个变量：

```text
admissibility reader：这条证据能不能用？
≠
verdict writer：这条证据实际上有没有进入裁决？
```

如果 reader 接近满分而 writer 仍被排除证据推动，模型不是简单“没读懂指令”；它读懂了规范状态，却没有用这个状态门控内容整合。

## 2. Mother question

> **语言模型表示的是“当前合法证据集”，还是所有已经进入上下文、因而无法被真正撤销的信息？**

它对应法律与认知心理学中的老问题 *unring the bell*：陪审员听见一条信息后，法官即使要求忽略，也未必能把认知状态恢复到听见之前。

最自然的演示只有三行：

```text
同一宗证据均衡的案件
+ 一条强烈不利证词                         → guilty 上升
+ 同一条证词，但法官裁定 inadmissible 并要求不得考虑 → 理论上应回到 baseline
```

再单独问：

```text
“陪审员可否使用这条证词？” → 模型答 No
```

真正的 phenotype 是：

```text
rule answer = correct (“No, it must be disregarded”)
AND
verdict(inadmissible) remains much closer to verdict(admissible) than baseline
```

## 3. 为什么它可能跨规模存活

这项预测不依赖小模型不会法律术语：

1. **规模增加首先会把 reader 推到 ceiling，但不保证产生 causal gate。** 这反而使 dissociation 更干净。
2. **更强模型通常更会从上下文吸收具体、诊断性内容。** 因此 instruction-following 变强与 evidence uptake 变强是竞争趋势，效应不必随规模单调消失。
3. **所有 decoder-only 家族共享同一个结构压力：** 已读到的证据内容已经改变 residual stream；后出现的“不得使用”需要主动逆转或门控，而不是简单缺省忽略。
4. **已有相邻结果显示更强 reasoning 不必修复 use failure。** 2026 年 temporal applicable-law 工作报告：模型知道法律有时间适用范围、也知道旧法内容，却仍偏向使用当前法；更强 reasoning 甚至可能更差。它支持“显式规则知识不等于规则控制计算”，但不是本现象。

必须诚实保留的风险：frontier instruction tuning 也可能显著减少该效应。因此 G0 的目标不是找任何会错的模型，而是检查 effect 是否在不同家族与尺寸中保持，并把 `reader-correct` 样本作为唯一分析集合。

## 4. 最小自然 G0（不靠奇怪构造）

### 4.1 材料

优先级：

1. 直接复用公开/可取得的 mock-jury 实验材料与经典 inadmissible-evidence paradigms；
2. 使用公开案件摘要，人工只做最小的 evidence insertion 和 judge ruling；
3. discovery 阶段允许 24–40 个简短案件，但必须由法律背景人员盲审自然性与证据强度。

每宗案件同时做 incriminating 与 exculpatory 两个方向，避免模型只是服从“更谨慎/更无罪”的安全先验。

### 4.2 Frozen conditions

```text
B0  baseline：案件中没有目标证据
A   admitted：目标证据出现且可采纳
I   inadmissible：与 A byte-identical 的证据出现，随后法官裁定排除并要求不得考虑
P   placebo ruling：同长度程序性文字，但不排除目标证据
```

核心不是把很多 transformation 凑在一起；只有一个自然事件：**证据被法官排除**。P 只是排除新增文字、长度或“法官语气”的解释。

### 4.3 两个分离 readout

在不同 prompt/copy 中测，避免一个答案显式牵引另一个答案：

- `reader`: 该证据依法是否可用于裁决？只答 Yes/No。
- `writer`: guilty probability 0–100；另给 forced verdict。

对第 i 个案件定义：

```text
uptake_i = verdict(A_i) - verdict(B0_i)
leak_i   = verdict(I_i) - verdict(B0_i)
retention_i = leak_i / uptake_i
```

exculpatory 案件按方向翻转后再合并。只在 `reader(I)=No` 且 baseline/admitted 方向有效的案件上计算主效应。

### 4.4 预注册门槛

Promote 必须同时满足：

```text
reader accuracy >= 90%
admitted evidence 有稳定 uptake
inadmissible retention >= 0.30，或 I-B0 >= 10 probability points
至少 3 个模型家族方向一致
至少一个家族内两个尺寸仍成立
incriminating 与 exculpatory 两方向都成立
placebo ruling 不能解释效应
```

如果只在小模型上成立，或 reader 错误样本驱动全部效应：立即 KILL。

## 5. 最重要的形状扫描

不先堆 benchmark；只沿一个有理论意义的轴扫描“排除强度”：

```text
证据从未出现
→ 出现后被明确排除
→ 出现后被说明为何不可靠而排除
→ 出现后被证明是伪造的
```

理想异常不是平滑改善，而是：模型口头上的 admissibility/reliability 判断已在第二级到顶，但 verdict 要到“证明伪造”才突然回到 baseline。那会提示内部使用的是 `content validity`，而不是规范性的 `admissibility` gate。

## 6. Collision audit（截至 2026-08-27）

### 已经相邻，但不等同

- **人类 mock-jury 文献：** 数十年研究表明，人类陪审员常无法忽略 inadmissible evidence；这是老母题与自然材料来源，不是 LLM 机制答案。
- **Wrong-law / temporal legal reasoning (2026)：** 发现模型懂 temporal scope 却使用当前法，且强 reasoning 模型可能更差。其 phenotype 是 *current-law bias*，没有研究“同一证据被裁定排除后仍保留多少 causal influence”。
- **Reasoning models do not always say what they think：** 隐蔽 hints 可影响答案且 CoT 不忠实；没有显式 `inadmissible reader correct / verdict writer contaminated` 分离。
- **Irrelevant context / distractor robustness：** 目标证据在语义上高度相关、甚至很有诊断性；它被排除是因为规范/来源状态，而非无关。
- **Sycophancy / belief drift：** 没有固定的证据可用性规则，也没有同一内容 admitted/inadmissible 的 paired causal contrast。
- **Role-play / fiction：** 测的是 persona 或 truth representation；这里测的是模型能否用已识别出的 source status 控制 downstream decision。

### 禁止的 novelty claim

不能声称首次发现“LLM 会受无关信息影响”或“knowledge-use dissociation”。可辩护的精确 claim 只能是：

> **LLMs can explicitly recognize that evidence is excluded while retaining its directional causal influence on judgment; the admissibility representation fails to gate evidence-to-verdict integration.**

正式投稿前必须再查法律 NLP、LLM juror 与 context editing 文献，并联系最接近作者确认边界。

## 7. 可解释性入口

### H1 — ruling 没被内部表示

不太有趣；若 reader 已经正确，此解释应很弱。

### H2 — 表示存在，但没有门控 evidence content

主假设。训练线性 probe 定位：

- evidence direction / polarity；
- admissible vs inadmissible status；
- verdict direction。

然后在 matched A/I pairs 上做 activation patching：把 I 的 admissibility-state patch 到 A，是否能在不改变 evidence content representation 的情况下把 verdict 拉回 baseline？

### H3 — 中间层成功排除，晚层重新吸收

逐层读出 `I-B0`。如果中层短暂回到 baseline、后层又靠近 A，就是非常漂亮的 late recontamination。

### H4 — status 只局部绑定在 ruling tokens，未绑定到 evidence tokens

检查 ruling → evidence span → verdict token 的 attention/path mediation。这里有直接方法口：把 source/status tag 因果绑定到证据表征，而不是泛化地“多提醒模型”。

## 8. Mechanism 导出的 method

如果 H2/H4 成立，方法不是 generic SFT，而是 **causal evidence gating**：

1. 为每个 evidence span 维护可用性/来源状态；
2. 在定位到的 integration layers 对 invalidated span 做选择性抑制或低秩门控；
3. 训练目标直接最小化 `I-B0`，同时保持 `A-B0`；
4. 评价副作用：不能让模型普遍忽略负面证据，也不能损害 admitted evidence 的使用。

这是机制必要性的判据：只有知道 failure 是 H2、H3 还是 H4，修复位置才不同。

## 9. 决策

这是当前最值得立即跑的候选，因为它同时满足：

- 一句话能讲清；
- 来源是古老、自然的人类认知/法律问题；
- 不是小 benchmark 的格式噪声；
- 规模增大不保证消失，并存在相邻的 inverse-scaling 先例；
- reader/writer dissociation 给出清晰的 mechanistic decomposition；
- 精确 LLM phenotype 暂未在检索中发现直接占位。

但在三家族 G0 之前，它仍是高优先级**假设**，不能写成已证实现象。
