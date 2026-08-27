# LLM 反直觉现象发现指南

> 内部选题机器；不是论文贡献，不对外宣称“提出一个 metamorphic testing framework”。

版本：2026-08-27

这份文档统一仓库已有的 interpretability 选题原则与本轮新的转向：

> **不要先决定一个已有 bias 的名字，再去模型里寻找它。先找到一个人类直觉上基本、模型内部却可能被错误分解的心智问题，再用自然对照制造发现机会，让具体 phenotype 从实验中长出来。**

最终论文可以只讲那个被发现的自然 phenotype、它的机制和由机制推出的方法；`phenomenon_miner` 只是私人矿镐。

---

# 0. 一页版执行摘要

## 0.1 搜索对象：先有母问题，再有 relation

2026-08-27 对 `#r_hamdi` 的完整回溯说明，单纯把搜索对象写成
`benchmark × relation` 会系统性地产生细碎题。正确层级是：

```text
人类早已有词的基本心智动作 / 世界结构
× 一个人人能懂的日常矛盾
× 两个可能不同的内部计算
× 用来区分它们的自然 relation / intervention
```

例如：

```text
知道某实体很多事实 ≠ 认为它真实存在
识别“请任意选择” ≠ 真正塑造一个公平输出分布
理解一个假设 ≠ 相信这个假设
记住一个目标 ≠ 仍承诺执行这个目标
拥有相同属性 ≠ 是同一个对象
```

只有母问题成立后，才进入原来的自动扫描层：

搜索的基本单位不是“一个认知偏差”，而是：

```text
公开 source distribution
× 一个有理论约束的 relation
× 一个强度 / 位置 / 路径轴
× 两个便宜但有基础能力的独立模型家族
```

relation 优先来自五类：

1. strict invariance；
2. equivariance；
3. monotonicity；
4. reversibility / path independence；
5. factor composition。

硬规则：如果删掉数据集名称和 transformation 以后，研究问题便不存在，说明它还只是测试用例，不是候选题。

## 0.2 最终想捞出的东西

理想候选能用一句普通话说清，例如：

```text
同一条证据放在中间，模型反而看不见。
同一组逻辑前提只换顺序，准确率掉三十个百分点。
同一句错误只因被标成“自己的想法”，模型就不愿纠正。
模型记得最早状态，却忘记当前状态。
```

不是：

```text
在模板 T7、参数 α=.4、三种扰动同时存在时，某指标下降 4.2 分。
```

## 0.3 不可降低的晋级门槛

一个候选只有同时满足以下条件，才可以从矿机输出升级为研究题：

- **自然**：普通人一听就知道模型哪里奇怪；
- **母问题够大**：指向现实使用或基本认知结构，而非某 benchmark 的局部答题技巧；
- **规模上有生存理由**：现象来自目标冲突、训练目标或计算分解，而不只是能力不足；优先寻找随能力增强保持或增强的 dissociation；
- **关系有效**：变换前后的 gold 关系可以独立证明；
- **效应够大**：优先 `>15 pp`，或有明显 cliff / U-shape / sign reversal / 巨大 odds change；
- **跨家族**：至少两个独立模型家族同方向，正式确认最好三个；
- **有能力基线**：模型在 control 上确实会做任务；
- **有选择性**：目标 manipulation 大，长度、措辞、格式等 nuisance controls 小；
- **有结构**：不是所有扰动都平均掉一点；
- **可解释**：存在至少两个有不同因果预测的机制解释；
- **有方法口**：机制 A 与机制 B 会导向不同修复；
- **叙事未撞车**：母现象可以已有，但我们的 decisive contrast / structural signature 没被做完。

## 0.4 搜索顺序

```text
一句话母问题 + 一个日常例子
→ 写出至少两个竞争性内部机制
→ 解释为什么更强模型也未必自动解决
→ N0 exact phenotype + mother-inclusion 全文审计
→ 独立对抗复核
→ relation/data/license/20例 D0 audit
→ 冻结合同并获得 READY-TO-SMOKE
→ 30–50 对 × 两个小模型 smoke
→ 看 paired raw cases，不只看均值
→ N1 按真实错误目的地与形状二次审计
→ 200–500 对跨家族确认
→ nuisance / scorer / prompt controls
→ 画强度与尺度曲线
→ 才给现象命名
→ 冻结机制问题
→ 白盒解释
→ 机制预测方法
```

任何一步失败，记录后停止。不得靠换弱模型、挑模板、挑 subset 或放宽指标续命。

尤其不得把“在小模型上稳定犯错”误当作一般性。正式候选必须尽早经过一个当前强模型的杀伤测试；强模型若几乎消除现象，除非出现清楚的反常 scaling，否则不再投入机制分析。

---

# 1. 为什么要从“搜现象论文”转向“制造发现机会”

旧路线是：

```text
论文已报告 behavioral phenomenon
→ 查有没有 mechanism
→ 没有就补 mechanism
```

它适合找到“能做”的题，但存在系统性天花板：一个现象一旦大到足以被广泛注意，2025–2026 的作者通常已经顺带做 representation、attention、intervention 或 mitigation。后来者只能不断压窄。

新路线是：

```text
寻找理论上受约束的自由度
→ 在公开自然任务上成对扫描
→ 从违反关系的形状中发现 phenotype
→ 跨模型、跨尺寸确认
→ 最后才问它叫什么、是否已有工作
```

四个代表性工作都遵循这个结构：

- [Lost in the Middle](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long)：同一证据、同一问题、同一 distractors，只改变证据位置，扫出 U-shape。
- [Premise Order Matters](https://proceedings.mlr.press/v235/chen24i.html)：逻辑等价的前提排列，扫出 `30%+` 差异与 proof-order 结构。
- [The Self-Correction Illusion](https://arxiv.org/abs/2606.05976)：byte-identical claim 只换 role metadata，扫出 `23–93 pp` 差异。
- [Transformers Remember First, Forget Last](https://arxiv.org/abs/2603.00270)：同一状态历史只换“最初 / 当前”查询，所有 39 个模型出现 PI > RI，且 scaling law 不同。

这些工作不是先搜到一个心理学标签。它们先问：

> **哪个自由度在规范上不应影响答案，却可能暴露模型内部不同的计算路径？**

Metamorphic testing 已经是成熟测试思想，[大规模 LLM metamorphic testing](https://arxiv.org/abs/2511.02108) 与 [LGMT](https://www.sciencedirect.com/science/article/pii/S0950705126010506) 也已经把框架本身做成研究。因此本项目不写：

> We propose an invariance testing framework.

本项目要写的是：

> We discovered that models do **X**, isolated **Y** as its decisive structural property, identified **Z** as its causal mechanism, and derived **M** from that mechanism.

## 1.1 与仓库旧原则的统一

这次转向不是推翻 `Behavior first`，而是修正“behavior 从哪里来”。

| 看似冲突的原则 | 统一后的解释 |
|---|---|
| 从自然现象出发 vs 现象应是搜索输出 | discovery 从自然公开任务与自然关系出发；具体 phenotype 是输出，不要求预先命名 |
| 先查文献 vs 不要让文献锁死 hypothesis | 先冻结自然主张，再做 N0 exact/母现象全文审计；smoke 后用真实 signature 做 N1，不用文献预先规定现象名称 |
| 不许乱造数据 vs 主动制造发现机会 | 机会来自对公开样本做 gold-preserving 程序变换，不来自发明整套 task / rule / label |
| novelty 必须强 vs 母现象可以已有 | 不要求脱离所有母现象；要求新结构性质、关键交互或机制问题未被完整覆盖 |
| 参考老问题 vs 不先找认知偏差 | 老问题只贡献关系、对照和可能轴；是否呈现对应“偏差”由数据决定 |

因此完整链条是：

```text
人类直觉中的 mother question
→ 一句话日常矛盾
→ 两个可分离的心智步骤 / 概念轴
→ 自然 source distribution 与决定性 relation
→ 未命名 behavioral anomaly
→ 稳定 phenotype
→ mechanism
→ method
```

## 1.2 从 `#r_hamdi` 复原出的真实选题法

这不是根据成稿倒推的故事，而是按 Slack 时间线还原的发现过程。

### 题一：随机选择不是“数字 7 偏差”

起点是任何用户都见过的行为：

> 让模型随便选一个数字、颜色或硬币面，它并不像公平随机源，而会强烈偏爱 `7`、`blue` 等答案，也难以遵守指定分布。

关键提升不是收集更多偏爱项，而是把一个表面行为拆成两个原则上不同的计算：

```text
reader：识别“现在要求任意 / 随机选择”
writer：把答案概率塑造成目标分布
```

实验随后才发现两者真的分离：choice-state direction 像 switch，增强它只会进入模型原有的“随机作答模式”，不会持续提高熵；另一个晚层方向才像 distribution writer。这一 dissociation 自然导向 gated reader×writer intervention。

这里的搜索模板是：

```text
一个人人见过的失败
→ 不研究它偏爱哪个答案
→ 追问完成该行为至少需要哪两个心智步骤
→ 寻找“步骤 A 完好、步骤 B 异常”的分离
→ 用分离推出干预结构
```

### 题二：熟悉一个实体不等于认为它存在

起点不是扫 benchmark，而是把已有问题 `Do I know this entity?` 的概念轴旋转：

```text
epistemic：我是否知道 x？
ontological：x 是否真实存在？
```

Harry Potter、Hogwarts、龙和 kryptonite 都高度熟悉，但并不真实存在。因此 familiarity-matched 的现实 / 虚构实体可以把两条轴拆开。一个例子就能讲清问题：

> 问模型“怎样带我的宠物龙去看兽医”，它可以指出龙不存在，也可以顺着设定回答；它内部是否仍保留“龙是虚构的”这一判断？

后续实验才发现 reality direction、行为上的 play-along 和内部 ontology 可以分离；“answer as if dragons were real” 能翻转输出，却几乎不移动内部 imaginary representation。

这里的搜索模板是：

```text
借用一篇工作的测量方法
→ 找到与原概念相关但逻辑独立的老问题
→ 用天然反例证明两轴不是一回事
→ 先找跨域表征，再找行为—表征 dissociation
```

### 两题共有的六条原则

1. **问题先于数据集。** 数据集只是把“随机、公平、现实、虚构”等大问题操作化。
2. **概念分解先于 perturbation。** 最值钱的 relation 是 `A ≠ B`：知道≠存在、识别任务≠执行策略、输出配合≠内部相信。
3. **天然极端反例优于人工模板。** “熟悉但不存在的 Harry Potter”本身就把 familiarity 与 reality 拆开。
4. **行为失败不是终点。** `总选 7` 只是入口；真正题目是模型把随机选择实现成了什么计算。
5. **好题自带 scaling 生存理由。** 更强的知识会强化 reality representation；更强的指令理解会强化 choice reader，但 next-token sampling 本身并不会自动变成公平 RNG。因此现象不依赖模型笨。
6. **机制必须产生方法。** reader/writer 分解预测 gated edit；ontology/play-along 分解预测可以改变行为而不改内部判断，并可分别干预。

因此，后续禁止从“小模型在哪个 benchmark 上掉分”直接晋级。优先搜索下面这种句式：

> 模型已经会 / 知道 **A**，但这并不意味着它会 / 知道 **B**；人类通常把 A 与 B 紧密联系，而实验显示模型内部把它们以一种反直觉方式分开或混合。

---

# 2. 搜索中的基本概念

## 2.1 Source distribution

现成公开 benchmark 提供自然问题、原始文本、任务分布与 gold。它回答：

> “这些输入为什么不是我们为了得到现象而临时编的？”

优先级：

```text
官方 benchmark 原样输入
> 官方输入的程序化最小变换
> 独立真实数据的最小变换
> 公开知识图谱导出的自然语言实例
> 大规模自构造模板
```

最后一档只能做机制 sandbox，不能独自承担自然性与一般性。

## 2.2 Relation

relation 不是字符串扰动，而是变换前后输出之间的理论约束：

```text
R(x, T(x), y, T_y(y)) = true
```

例如：

- 答案严格不变；
- 答案随实体交换而交换；
- 加入真实且有帮助的信息后，表现不应下降；
- 走一条变换再走逆变换，应回到原状态；
- 两个单独无害因素组合后，不应无缘无故触发灾难性开关。

## 2.3 Axis

axis 是 relation 内可扫描的连续或离散自由度，例如：

- 证据位置 `0% → 100%`；
- 支持证据数 `1 → 2 → 4 → 8`；
- 更新步数 `0 → 2 → 4 → 8 → 16`；
- 同实体事实数；
- 文档边界数；
- identity chain 长度；
- 可靠性从低到高；
- 两因素的四个 factorial cell。

只做两个点能发现平均差异；扫轴才能发现 U-shape、cliff、bimodality、phase transition 和 sign reversal。

## 2.4 Phenotype

phenotype 是扫描输出的**可复现结构签名**，而不只是一个 accuracy drop。它至少应包含：

```text
effect direction
effect magnitude
cross-model direction
shape over axis
paired flip pattern
selectivity controls
capability dissociation
scale trend
representative natural cases
```

## 2.5 Decisive contrast

决定论文是否新、机制是否清楚的不是宽标签，而是关键对照。例如：

```text
宽母现象：多文档会使 RAG 变难。
decisive contrast：局部证据检索完好，但只有跨文档组合崩溃；同文档组合不崩。
```

母现象可以已有；若该结构性质、交互和因果问题未被已有工作覆盖，仍可能是好题。

---

# 3. 自然性：什么叫“不是一堆变换凑出来”

## 3.1 自然性四级

### N3 — 最优

- 原 benchmark 输入；
- 只移动、删除、重复、重命名或重新分组已有内容；
- gold 由原数据直接继承；
- 一句话能解释 manipulation。

### N2 — 可接受

- 原 benchmark 输入；
- 增加一条可程序验证的提示、约束、来源标签或逆操作；
- 不引入新的 task ontology；
- gold 由 relation 确定。

### N1 — 仅作预检

- 从公开知识图谱或公开问题自动生成短场景；
- 有完整 provenance；
- 需要外部 benchmark 再验证。

### N0 — 不得晋级

- task、规则、label、interface、bridge 全由项目定义；
- 只有一个人工模板族；
- scorer 依赖另一个 LLM；
- 现象只在作者挑选的例子上存在。

## 3.2 “一句话测试”

候选必须能填完：

> **即使 ______ 完全相同，模型只因为 ______，就从 ______ 变成 ______。**

或：

> **给模型更多 / 更可靠 / 更直接的 ______，它反而 ______。**

如果一句话必须包含三个模板名、两个超参数和一串缩写，先降级。

## 3.3 最小操纵原则

Discovery 阶段一次只改变一个可命名自由度。组合因素只用于预先定义的 factorial：

```text
A=0, B=0
A=1, B=0
A=0, B=1
A=1, B=1
```

不能同时更换措辞、长度、答案位置、角色和任务格式，然后把差异归因给最喜欢的变量。

---

# 4. 五类 relation 的统一定义

## 4.1 Strict invariance

定义：

```math
f(T(x)) = f(x)
```

变换不能改变任务世界、问题含义和 gold。

优先轴：

- 独立前提排列；
- set / map / JSON 无序字段排列；
- entity、变量、图节点的双射重命名；
- 同义 alias 的全局一致替换；
- 加法乘法中的交换操作；
- 坐标整体平移；
- 不跨日历边界的时间整体平移；
- 等值单位表示；
- 等价 serialization；
- proof-irrelevant 事实的位置；
- 同一证据在 document / section 容器中的分组；
- 无语义的 document ID、filename、tool-call ID；
- 冗余真事实的重复与去重；
- 代码 alpha-renaming；
- 不改变控制流的格式化与注释。

高价值输出不是“每种扰动掉一点”，而是某个轴出现稳定、尖锐、选择性的结构。

## 4.2 Equivariance

定义：

```math
f(T_x(x)) = T_y(f(x))
```

输入变化后，答案应以已知方式变化。

优先轴：

- 全局交换 Alice / Bob，答案实体同步交换；
- 反转 `left/right`、`before/after`、`greater/less`，答案关系同步反转；
- graph node permutation；
- 选项 label permutation；
- category label bijection；
- 代码变量 / API 名称重命名；
- 摄氏 / 华氏、米 / 厘米的输入输出共同转换；
- 坐标旋转 / 镜像与方向答案同步变换；
- 图像水平镜像与左右答案交换；
- 正负极性翻转与 entail / contradict 标签交换；
- 主客体交换与逆关系答案映射；
- 时间线反转与 first / last 映射。

它尤其适合 activation interchange：clean 与 transformed pair 的内部内容变量也应可预测地交换。

## 4.3 Monotonicity

定义：当信息、约束或工具严格更有帮助时，目标成功概率不应系统下降：

```math
E_1 \subseteq E_2 \Rightarrow P(\text{success}\mid E_2) \ge P(\text{success}\mid E_1)
```

优先轴：

- 增加一致的充分证据；
- 增加独立来源的同向证据；
- 删除一个已知错误选项；
- 增加经过验证的错误选项排除信息；
- 补充缺失条件，使问题从不可答变为可答；
- 把模糊约束变得更具体；
- 提高信息源可靠性；
- 增加正确中间 lemma / proof hint；
- 把提示逐步移近答案；
- 增加 tool schema 中真正需要的参数说明；
- 增加正确单元测试；
- 提高图像 / 表格分辨率；
- 增加与问题相关、但不直接泄漏答案的解释；
- 增加支持事实而保持总长度或 distractor 数匹配。

重点看：

```text
1 → 2 → 3 正常，4 突然 collapse
弱提示有效，强提示反而无效
可靠性提高到某阈值后符号反转
```

## 4.4 Reversibility / path independence

逆变换：

```math
x \xrightarrow{T} x' \xrightarrow{T^{-1}} x
```

路径独立：

```math
Path_1(s_0)=s_f,\quad Path_2(s_0)=s_f
\Rightarrow f(Path_1)=f(Path_2)
```

优先轴：

- 状态 `A → B → A` 与直接 `A`；
- create → delete 与从未 create；
- grant → revoke 与从未 grant；
- rename → rename back；
- 单位转换后再转回；
- 代码 refactor 后 inverse refactor；
- 事实 correction 后 retraction；
- alias merge 后明确 unmerge；
- 进入 fictional frame 后明确退出；
- quote / unquote 或 nested scope 的进入退出；
- 多步更新与一步更新得到相同 current state；
- 两个独立更新 `T1,T2` 与 `T2,T1`；
- tool / database transaction commit 后 rollback；
- navigation 绕路返回同一地点与原地未动。

最有价值的问题是：

> **模型表示的是当前世界，还是到达当前世界的历史？**

## 4.5 Factor composition

定义交互残差：

```math
I_{AB}=\Delta_{AB}-\Delta_A-\Delta_B
```

重点找：

```text
A 单独无害
B 单独无害
A+B 突然 collapse
```

高价值组合：

- 证据位置 × source role；
- 知识冲突 × factual / fictional frame；
- identity alias × belief / knowledge scope；
- 文档边界 × multi-hop composition；
- 重复项 × 重复间距；
- negation × quantifier；
- 同实体负载 × 更新深度；
- 模糊实体 × 相似 distractor；
- tool 名称相似度 × schema 长度；
- answer rarity × context conflict；
- reasoning mode × misleading but irrelevant cue；
- 约束数量 × 约束嵌套深度；
- image mirror × textual spatial frame；
- scale × role metadata；
- parametric familiarity × local renaming。

组合实验必须保留四个 cell，不能只比较 control 与 `A+B`。

---

# 5. 如何选“高价值轴”

不是所有 invariant 都同样值得扫。优先选择满足以下至少三项的轴。

## 5.1 轴可能切换计算路径

例如：

- user / tool / memory role；
- real / fictional / quoted world；
- direct retrieval / multi-hop composition；
- current state / historical state；
- known entity / novel entity；
- natural language / structured serialization；
- answer / abstain；
- report / use；
- one document / multiple documents。

这些轴不只是表面字符串变化，可能对应 reader、router、gate 或不同 information pathway。

## 5.2 轴有明确的规范关系

优先：

- 数学、逻辑或程序语义可证明；
- gold 由原 benchmark 继承；
- 变换由 deterministic program 生成；
- 人类标注者无需重新判断答案。

谨慎：

- “应该更可信”；
- “应该更自然”；
- “两个故事语义差不多”；
- 哲学上本来就有争议的身份判断。

## 5.3 轴能形成强度曲线

两个点只告诉我们有差。优先可以扫：

- 位置；
- 数量；
- 距离；
- 更新次数；
- 边界数；
- chain depth；
- reliability；
- similarity；
- conflict strength；
- scale。

## 5.4 轴天然有 negative controls

例如研究 role：

```text
rename       no effect
paraphrase   no effect
length       no effect
role         huge effect
```

若找不到至少两个合理 nuisance controls，因果解释风险很高。

## 5.5 轴能映射到内部变量

理想 matched pair 能指出：

- 哪个 token / span 承载 content；
- 哪个位置承载 role / world / source；
- 哪个 receiver 应读取它；
- 哪个 late path 写入输出。

这使后续 activation interchange、path patching 和 gated intervention 不需要盲扫全网。

---

# 6. 现象矿区地图：领域、公开数据与高价值轴

下表不是“要研究这些已命名现象”，而是 source distribution 与 relation 的路由表。

| 矿区 | 优先公开数据 | 自然任务单元 | 高价值关系轴 | 最值得观察的结构 | 主要伪解释 |
|---|---|---|---|---|---|
| 数学文字题 | GSM8K, GSM-Hard, MATH-500, MATH, AMC/AIME | 原题与数值答案 | 单位等价、变量重命名、无关句排列、正确中间量单调加入、整体数值平移/缩放 | cliff、hint 越近反而越差、换单位符号翻转 | scorer、数值格式、真实难度改变 |
| 形式逻辑 | FOLIO, ProofWriter, AbductionAndNegation, RuleTaker | 前提集、结论、标签 | 前提 permutation、alpha-renaming、冗余 lemma、逆规则、独立子图、proof order | proof-order peak、冗余真前提 collapse、局部推理好但组合坏 | 变换不保持逻辑、标签偏置 |
| 多跳 QA | MuSiQue, HotpotQA, 2WikiMultiHopQA, Bamboogle, FRAMES | 问题、support paragraphs、decomposition | support 顺序、document grouping、bridge alias、局部 vs 完整问题、shortcut lemma | subquestions 全对而 composition 崩、边界交互 | 答案 alias、段落截断、support 不充分 |
| RAG / 知识冲突 | Faithfulness-QA, FEVER, FEVEROUS, QASC, ConflictBank, PopQA | context、claim/question、答案 | parametric familiarity、fiction/fact frame、source label、证据数与独立性、conflict strength | conflict 条件巨大而 aligned 条件为零；frame gate | context 本身不蕴含 gold、来源语义真的不同 |
| 长上下文检索 | LongBench, LongMemEval, NarrativeQA, Qasper, MoreDocsSameLen | 长文档、needle、问答 | 位置、重复距离、文档数、边界位置、query 前后位置、同实体 fan | U-shape、repetition-distance dip、局部/全局 dissociation | token 长度、截断、模板差异 |
| 状态与时间 | LongMemEval, TempReason, TimeQA, TGQA, state-tracking tasks | 更新历史、当前/过去查询 | `A→B→A`、直接/多步同终态、独立更新交换、全局时间平移、first/current query | history hysteresis、current/path 解耦、scale 变坏 | 时间语义改变、更新不是真正可逆 |
| 实体与指称 | PopQA, WebQSP, EntityQuestions, AmbER, Wikidata-derived QA | 实体、alias、关系 | alias swap、entity rename、known/novel、merge/unmerge、同名异实体、belief scope | identity binding 只在某 scope 泄漏；known/novel sign reversal | 问题歧义、错误 alias、parametric gold 不唯一 |
| 信念 / 知识 / ToM | ToMi, FANToM, Hi-ToM, OpenToM, BigToM | 故事、agent world、belief query | narrator/agent knowledge、alias identity、嵌套深度、事实揭示顺序、现实/信念查询 | 外部真相追溯写入旧信念、深度 cliff、report/use dissociation | Yes/No 默认策略、题目语义有争议 |
| 现实 / 虚构 / 引用 | Faithfulness-QA, narrative QA, public fiction corpora | 同一内容置于不同 world/source scope | factual/fictional、quote/assert、frame enter/exit、嵌套 fiction、真实/虚构实体 | fiction selectively releases parametric conflict；退出后仍残留 | frame 改变了正确答案、jailbreak/安全混杂 |
| 常识与策略推理 | StrategyQA, CommonsenseQA, SocialIQA, MuSR | 自然问题、证据、选择 | entity replacement、world-consistent counterfactual、解释提示、答案选项排列 | realistic/novel world interaction、reasoning mode 反而更差 | 常识变换不自然、选项偏置 |
| 多项选择 | GPQA, MMLU, SciQ, CommonsenseQA | question、options、gold | label permutation、wrong-option removal、verified elimination、distractor similarity、only-correct | eliminated option attraction、set-size cliff、scale anomaly | exact scorer、选项内容本身构成语境 |
| 指令遵循 | IFEval, FollowBench, Multi-IF, ComplexBench | prompt 与可验证 constraints | 冗余约束、约束顺序、等价 serialization、scope、嵌套、grant/revoke | 加一条一致约束触发 mode switch；可逆指令留痕 | constraint evaluator 错、任务真的更难 |
| Tool use / agents | BFCL, APIBank, ToolBench, τ-bench | user request、schema、calls、state | schema order、tool rename、无关工具增删、参数说明、create/delete、rollback | irrelevant tool 引发 tool switch；rollback 不回原态 | tool 名语义、parser、environment side effect |
| 代码生成与修复 | HumanEval+, MBPP+, LiveCodeBench, CRUXEval, SAFIM, SWE-bench Verified | specification、code、tests | alpha-renaming、等价 refactor、注释、正确测试单调加入、inverse patch | 多一个正确测试反而破坏已过测试；refactor hysteresis | 测试非等价、随机执行、语言版本 |
| 事实核查 / NLI | FEVER, FEVEROUS, FOLIO, ANLI, HANS | claim、evidence、label | 证据 permutation、同义改写、negation/quantifier factorial、冗余 entailment | negation×quantifier switch、证据更多反而错 | NLI label token bias、改写改变蕴含关系 |
| 因果 / 反事实 | COPA, CLadder, CRASS, Counterfactual Story | causal graph、question、world intervention | variable rename、graph-isomorphic relabel、irrelevant intervention、reversal、minimal change | irrelevant variable spillover、graph symmetry break | counterfactual gold 不唯一、世界知识冲突 |
| 空间推理 | StepGame, SpartQA, SpatialSense, ReSQ | objects、relations、query | 坐标平移/旋转/镜像、entity swap、path reversal、reference frame | 某旋转角 cliff、left/right only collapse | 语言模板方位偏置、镜像映射错误 |
| 表格 / 图表 / 文档 | TabFact, WikiTableQuestions, ChartQA, DocVQA | table/chart/document、question | row/column permutation、单位、sort/unsort、equivalent layout、resolution | 排序方向 switch、视觉布局而非值决定答案 | OCR、裁剪、layout 真改变读取难度 |
| 多模态 | MMMU, MathVista, VQAv2, BLINK | image+text、answer | image mirror、color/entity swap、text/image reliability、resolution、modality duplication | 单模态都对、组合反而错；可靠 cue 加入后 collapse | 图像编辑 artifact、视觉 gold 改变 |
| 安全 / 拒答 | XSTest, StrongReject, HarmBench 的安全子集 | intent、content、response class | 内容不变的 role/source、quote/use、fiction/fact、benign transformation | metadata 触发巨大拒答开关且内容能力完好 | policy 本就要求 role-sensitive、不能把规范差异叫 invariant |

## 6.1 本地已确认缓存的数据集

截至 2026-08-27，本机 Hugging Face cache 已确认包括：

- `openai/gsm8k`；
- `reasoning-machines/gsm-hard`；
- `HuggingFaceH4/math-500`；
- `EleutherAI/hendrycks_math`；
- 多个 AMC / AIME 集；
- `lime-nlp/synthetic_unanswerable_math`；
- `allenai/sciq`；
- `Idavidrein/gpqa`；
- `cais/mmlu`；
- `hotpotqa/hotpot_qa`；
- `dgslibisey/mu_si_que`；
- `voidful/2_wiki_multihop_qa`；
- `chiayewken/bamboogle`；
- `google/frames-benchmark`；
- `yixuantt/multi_hop_rag`；
- `TAUR-Lab/mu_sr`；
- `rajpurkar/squad_v2`；
- `pminervini/hl-fever`；
- `Dzeniks/feverous_3way`；
- `allenai/qasc`；
- `ml1996/webqsp` 与 `rmanluo/ro_g-webqsp`；
- `tau/commonsense_qa`；
- `akariasai/pop_qa`；
- `zhui711/med_einst`；
- `Shahar6000/more_docs_same_len`；
- `gonglinyuan/safim`；
- `mgor/protobowl-11-13-agent-responses`。

小模型应先用这些本地数据，不要一开始下载大数据集。

## 6.2 完整 dataset catalog

按领域整理的扩展数据集目录、任务结构、可扫描 relation、gold 类型、本地缓存状态与优先级，见：

[`DATASET_CATALOG.md`](DATASET_CATALOG.md)

该目录目前覆盖数学、逻辑、多跳 QA、RAG、长上下文、长期记忆、状态更新、实体指称、ToM、现实/虚构、指令遵循、工具调用、代码、因果、空间、表格图表、多模态、安全、语言学、翻译与不确定性等矿区。下一模型选轴前应先从 catalog 确认：

```text
dataset 属于什么领域
gold 是否 deterministic / inherited
本地数据是否完整
哪些 transformations 合法
哪些轴已被 benchmark 本身研究过
```

---

# 7. 高价值轴库

下面是用于组合实验的轴库。它们不是待证明的“现象名”，而是可枚举的自由度。

## 7.1 内容保持、容器改变

- document vs section；
- user vs tool vs memory；
- plain text vs JSON / XML / Markdown table；
- paragraph vs footnote；
- body vs title；
- quoted vs unquoted；
- factual article vs fictional story；
- current message vs conversation history；
- answer option vs supporting statement；
- source with opaque ID vs semantic name。

适合发现 role reader、source gate、serialization pathway 与 metadata dominance。

## 7.2 世界与本体

- real entity vs fictional entity；
- famous entity vs novel entity；
- actual world vs hypothetical world；
- narrator world vs character belief world；
- quoted claim vs asserted claim；
- nested fiction depth `0/1/2/3`；
- enter frame / exit frame / re-enter；
- entity exists / is merely mentioned；
- one entity with two aliases / two entities with similar names；
- merge identity / retract identity。

这些轴必须特别审查 gold：世界切换有时真的会改变真值，不能把语义差异误称 invariance。

## 7.3 位置与距离

- normalized evidence position；
- evidence–query distance；
- bridge-fact distance；
- two repeated items 的间距；
- correction 与原 claim 的距离；
- identity statement 与 belief statement 的顺序；
- support facts 是否相邻；
- distractor 是否插在 proof edge 之间；
- query 在 context 前或后。

扫描至少五个位置；只测头尾不能发现 U-shape。

## 7.4 数量与负载

- document count，保持总长度；
- supporting evidence count；
- distractor count；
- facts per entity；
- updates per variable；
- entities per relation；
- constraints per instruction；
- tools per schema；
- aliases per entity；
- proof depth；
- nested scope depth；
- repeated occurrence count。

数量轴应同时有固定总长度或固定相关信息量的 control，以区分 generic context load。

## 7.5 可靠性与冲突

- source reliability；
- evidence agreement；
- evidence independence / common provenance；
- parametric familiarity；
- conflict strength；
- number of consistent repetitions；
- recency of correction；
- authority label；
- direct observation vs hearsay；
- exact quote vs summary。

这里的 gold 往往不是 strict accuracy relation；优先用已有标注或显式概率规则，不自行发明“合理权重”。

## 7.6 表示与命名

- natural names vs arbitrary names；
- single-token vs multi-token labels；
- alphabetic vs numeric symbols；
- frequent vs rare aliases；
- semantically meaningful vs opaque IDs；
- code variable rename；
- unit notation；
- date format；
- option labels `A/B/C` vs `1/2/3`；
- Unicode / ASCII 等价表示。

必须匹配 token length，或至少把 tokenization 作为显式解释而非机制结论。

## 7.7 查询与输出

- first vs current vs previous；
- fact recall vs use in action；
- answer vs verify；
- open generation vs multiple choice；
- entity answer vs relation answer；
- positive query vs logically equivalent negative query；
- direct question vs inverse question；
- answer text vs label；
- abstain allowed vs forced choice；
- prediction vs explanation。

查询轴非常容易混入接口难度，必须用 matched semantic-output controls。

---

# 8. 从老问题借“关系”，不要借“答案标签”

导师提示的老问题很有价值，但正确用法是把它们转换为 relation generators，而不是先决定“研究某偏差”。

| 老问题 / 思想 | 可借出的结构 | 可扫描轴 | 不应预设的结论 |
|---|---|---|---|
| type–token distinction | 同一类型的多个 occurrence 是否被合并 | repetition count / distance | “模型有 repetition blindness” |
| use–mention distinction | 被谈论的句子是否被当成断言或指令 | quote depth / role | “模型不懂 quotation” |
| Frege / intensional opacity | 共指替换在事实世界成立、在信念世界未必成立 | known alias × belief scope | “模型一定泄漏身份” |
| possible worlds | 世界内真值与现实知识的分离 | real/fiction/counterfactual | “fiction 一定改善服从” |
| belief revision | 相同最终信念集是否受更新路径影响 | update/retract order | “模型有 anchoring” |
| source monitoring | 内容与来源角色能否分开 | content × source | “模型有 source amnesia” |
| fan effect | 总长度相同时，单实体关联数是否影响检索 | facts/entity | “LLM 复制人类 fan effect” |
| part-list cuing | 部分提醒是否选择性妨碍未提醒项 | cue size / relatedness | “提醒必然导致遗忘” |
| Ranschburg / repetition | 相同项是否比不同项更难 individuate | identity × spacing | “重复就是坏” |
| proactive / retroactive interference | 新旧状态的干扰方向 | update depth / query time | “PI 或 RI 必然更强” |
| object permanence | 暂时不可见是否等于不存在 | occlusion duration | “模型有人类发展阶段” |
| conservation | 等价表示改变是否误改数量判断 | shape / unit / layout | “模型缺少物理直觉” |
| Einstellung | 已走路径是否阻止更直接解 | solution history | “示例总会害模型” |
| hysteresis | 同一当前输入是否因历史不同而处于不同模式 | enter/exit strength | “有 latent state” |
| causal modularity | 无关干预不应改变目标机制 | intervention locality | “模型因果推理差” |
| compositionality | 部件会做不等于能组合 | local vs joint | “模型没有 composition” |
| symmetry / group action | 变换输入应可预测变换输出 | swap/rotate/invert | “模型有方向偏置” |
| monotone logic | 添加真前提不应撤销蕴含 | lemma/evidence count | “更多信息一定更好” |
| path independence | 同终态不同路径应等价 | direct vs detour | “模型记住历史” |
| common-cause dependence | 重复来源不等于独立证据 | provenance structure | “模型只数票” |
| sorites / category boundary | 连续强度是否出现内部开关 | fine-grained strength | “模型阈值不合理” |

正确流程：

```text
老问题提供一个可证明 / 可对照的自由度
→ 在公开任务上扫
→ 看模型实际产生什么结构
→ 最后再决定是否借用老名字
```

---

# 9. 第一轮可直接交给小模型枚举的 search cards

每张 card 都只定义关系，不预设会发现什么。

## 9.1 数学与逻辑

1. GSM8K：全局一致重命名人物，保持数字与关系；比较 natural names / opaque IDs。
2. GSM8K：把所有同量纲数字与答案共同乘 `10/100`，筛掉会改变整除结构的题。
3. GSM8K：等值单位转换，答案同步转换；扫单位粒度。
4. GSM8K：将独立背景句移到开头 / 中间 / 末尾。
5. MATH：变量 alpha-renaming，答案表达式同步重命名。
6. MATH：加入一个官方解答中正确但非最终的中间等式；扫 hint 距最终答案的步数。
7. FOLIO：独立前提 permutation；按是否接近 proof execution order 分析。
8. FOLIO / ProofWriter：加入一条可由现有前提推出的 redundant lemma。
9. ProofWriter：图同构 node relabeling；比较语义名与随机名。
10. ProofWriter：两个互不相连子图交换顺序；查询不变。
11. Logic：把 rule 与事实分别 block / interleave，保持内容与顺序映射。
12. Logic：在 `A→B→C` 中加入正确 shortcut `A→C`；local 与 full proof 分开计分。

## 9.2 QA、RAG 与长上下文

13. MuSiQue：support paragraphs 同文档 vs 多文档；必须同时测各 subquestion 与完整问题。
14. MuSiQue：只移动 proof-irrelevant paragraph，不动 support 的绝对位置。
15. MuSiQue：bridge entity 用官方 alias 全局替换，答案同步映射。
16. HotpotQA：support facts 相邻 vs 被 distractors 隔开，保持各自 normalized position。
17. MoreDocsSameLen：固定总长度与 support 位置，只改变 document 数。
18. RAG：相同支持句由一个来源重复 vs 多个独立来源出现；答案不变，置信度另测。
19. Faithfulness-QA：aligned / conflict × factual / fictional frame 的四格。
20. Faithfulness-QA：fiction frame enter → exit 后，再问现实问题；比较直接现实路径。
21. PopQA：同总事实数下，其他事实集中在目标实体 vs 分散到不同实体。
22. SQuAD2：从缺少关键句到补回关键句，扫关键句出现位置；答题与 abstain 分开。
23. Long context：相同 needle 出现一次 / 两次一致 / 两次矛盾；扫两次间距。
24. Qasper / NarrativeQA：query 放在 context 前 / 后；用等长 reminder 控制。

## 9.3 状态、时间、身份与世界

25. 状态历史：`A=v1 → A=v2 → A=v1` 与直接 `A=v1`，问 current state。
26. 状态历史：两个独立对象的更新交换顺序，问各自 current state。
27. 状态历史：多步更新与一步更新到同终态；扫 detour 长度。
28. 时间 QA：所有日期整体平移固定天数，避开周末、闰日和月份边界。
29. 时间 QA：事件与 query 同时反转，before/after 答案同步反转。
30. Entity QA：官方 alias 全局交换；事实世界与 agent-belief world 做四格。
31. Entity QA：known alias pair vs novel stipulated alias pair，其他 token 结构匹配。
32. Identity：声明 merge 后再明确撤销 merge；比较从未 merge 的同终态。
33. Fiction：同一反事实文章的 factual / fictional / quoted 三种 scope。
34. Fiction：嵌套 story 中退出一层或两层，分别询问各 world 的事实。
35. Belief QA：叙述者后来获知身份，agent 未知；比较事实查询与 agent belief 查询。
36. Belief QA：局部人物信念都能报告，再测试这些信念是否被用于预测行动。

## 9.4 选择、约束、工具与代码

37. GPQA：option label permutation；按模型 uncertainty 分层，而非只看总均值。
38. GPQA：逐步删除 wrong options 与逐步加入 verified elimination，比较逻辑等价曲线。
39. IFEval：加入与已有约束逻辑重复的约束；保持输出目标不变。
40. IFEval：独立约束顺序 permutation；按执行顺序距离分析。
41. IFEval：grant → revoke 与从未 grant；测最终允许集合。
42. BFCL：tool schema 顺序；保持正确 tool 的绝对位置与相对位置分别控制。
43. BFCL：无关 tool 添加 / 删除；按名称相似度与 schema 相似度扫轴。
44. BFCL：tool 与参数 alpha-renaming；调用同步映射。
45. Agent state：create → delete / write → rollback 与直接终态。
46. HumanEval+：变量 alpha-renaming 与注释格式变换。
47. HumanEval+：逐步加入正确 tests；记录已通过 tests 是否被新代码破坏。
48. Code repair：patch → inverse patch 与原程序；比较生成行为和内部 state。
49. SAFIM：等价代码 serialization、函数顺序和局部命名。
50. LiveCodeBench：正确类型提示从弱到强；看是否单调。

## 9.5 空间、因果与多模态

51. StepGame：坐标整体平移；答案不变。
52. StepGame：旋转 `90/180/270°`，方向答案同步映射。
53. StepGame：实体全局 swap 与答案实体同步 swap。
54. Causal graph：graph-isomorphic variable rename。
55. Causal graph：对 d-separated 无关变量干预，目标答案不变。
56. Causal graph：同一最终 assignment 的直接 intervention 与多步 intervention。
57. ChartQA：row / column permutation，保持 label 与 value 对应。
58. ChartQA：单位缩放，问题与答案同步缩放。
59. VQA / spatial image：水平镜像，left/right 答案交换。
60. Multimodal cue：单模态文本正确、单模态图像正确、双模态一致；检查组合是否劣于两者。

这些 cards 只进入 30–50 对 smoke。没有明显结构，不扩大运行。

---

# 10. Anomaly signature 与自动评分

## 10.1 先硬门槛，后排序

不能用一个高综合分掩盖致命问题。以下任一为假，候选不进入排行榜：

```text
relation_valid
gold_deterministic_or_inherited
baseline_capability_above_floor
paired_sample_size_sufficient
scorer_audited
at_least_two_families_same_direction
```

## 10.2 Effect size

二元准确率用 paired difference：

```math
\Delta_T = \frac{1}{N}\sum_i [c_i(T(x))-c_i(x)]
```

同时保存 discordant pairs：

```text
help: baseline wrong → transformed correct
hurt: baseline correct → transformed wrong
```

只报均值会掩盖“同样多 help 与 hurt”的不稳定性。至少报告 paired bootstrap CI 或 McNemar test；统计显著不能替代 effect size。

推荐等级：

- `|Δ| < 5 pp`：通常是噪声 / 普通 robustness；
- `5–15 pp`：只有强结构、强 dissociation 才保留；
- `15–25 pp`：值得确认；
- `>25 pp`：高优先级；
- `>40 pp` 或 control 接近完好：立即做 artifact audit。

## 10.3 Cross-family consistency

保存：

```text
direction_consistency = same-sign capable models / capable models
median_effect
minimum_family_effect
between-family variance
```

不能让一个大效应模型平均掉另一个反向模型。

## 10.4 Shape

自动标记：

- monotone；
- U-shape / inverted U；
- cliff；
- sign reversal；
- bimodal item effects；
- saturation；
- growing-with-scale；
- reasoning-mode-only。

cliff 可用最大相邻跳变占总范围变化的比例作初筛，但必须看 confidence interval 与原始样本。

## 10.5 Non-additive interaction

四格实验报告：

```math
I_{AB} = (Y_{11}-Y_{10})-(Y_{01}-Y_{00})
```

高价值模式：

```text
|ΔA| < 5 pp
|ΔB| < 5 pp
|IAB| > 15 pp
```

## 10.6 Dissociation

定义目标能力与 matched control：

```text
local retrieval       vs cross-boundary composition
fact report           vs use in action
original value        vs current value
content understanding vs role-conditioned use
single modality       vs combined modalities
known identity        vs agent-specific identity belief
```

简单分数：

```math
D = |\Delta_{target}| - |\Delta_{control}|
```

但论文应报告完整四格，不只报告 D。

## 10.7 Selectivity

至少比较：

```text
target manipulation
length-matched nuisance
paraphrase nuisance
format/tokenization nuisance
generic difficulty control
```

若所有 perturbation 都掉 8 pp，结论是 generic brittleness，不是目标机制。

## 10.8 Surprise 与 naturalness

这两项不能完全自动化，使用冻结 rubric：

### Surprise `0–3`

- 0：普通难度增加；
- 1：方向略意外但可由长度解释；
- 2：违反清楚关系，且出现结构；
- 3：能力完好 / 目标崩溃、sign reversal、规模越大越强或只在组合条件打开。

### Naturalness `0–3`

- 0：自定义 ontology 与复杂模板；
- 1：公开事实自动造题；
- 2：公开 benchmark 的简单程序变换；
- 3：原任务中自然存在的自由度，仅移动 / 标记 / 重排。

## 10.9 机制与方法潜力 `0–3`

- 0：只能说“模型不鲁棒”；
- 1：能 probe，但无 competing mechanisms；
- 2：有 clean/corrupt pairs 与两个因果预测；
- 3：content 与 gate/role/path 可正交交换，且不同机制导向不同修复。

## 10.10 推荐综合分

硬门槛通过后，将各项缩放到 `[0,1]`：

```math
S = E^{1.5} \times X \times U \times H \times D \times N \times M \times (1-A)
```

其中：

- `E` effect；
- `X` cross-family；
- `U` surprise；
- `H` shape / nonlinearity；
- `D` dissociation / selectivity；
- `N` naturalness；
- `M` mechanism + method opening；
- `A` artifact risk。

乘法只用于排序，不能把 rubric 当成科学结果。

---

# 11. 分阶段实验协议

## Stage −1 — Relation validity

在调用模型前完成：

- 写出 relation 的形式定义；
- 证明 gold 如何继承或映射；
- 自动检查 transformation 没改答案；
- 抽查至少 20 对原始样本；
- 记录会使 relation 失效的 edge cases；
- 冻结 scorer。

失败即停止。

## Stage 0 — N0 novelty 与 D0 data 授权

在任何模型调用前，按 [`phenomenon_miner/NOVELTY_GATE.md`](phenomenon_miner/NOVELTY_GATE.md) 完成全文级 collision、母现象包含、独立复核、license/gold 和 20 例抽样。只有注册表 `validation_authorized: true` 才进入 smoke。

## Stage 1 — 两家族小模型 smoke

建议：

```text
30–50 paired items
2 independent families
temperature = 0
1 frozen prompt
deterministic scorer
保存所有 raw outputs
```

晋级条件满足其一：

- 两家族同方向且都 `>15 pp`；
- 一家族 `>25 pp`、另一家族 `>8 pp`，且已有非线性 / dissociation；
- effect 尚小，但出现极清楚的 cliff、sign reversal 或 factorial interaction。

否则归档，不扩样本。

## Stage 2 — N1 actual-signature audit

读取 raw cases 后，按真实错误目的地、形状、reader/use 解离与 scale 迹象二次检索。撞车立即 KILL；未完成 N1 不扩模型。

## Stage 3 — 200–500 paired confirmation

- 随机种子冻结；
- 不根据 smoke 错例挑 subset；
- 报 paired CI 与 flips；
- 按原 benchmark 难度、类别、长度分层；
- 查看效应是否由少数模板驱动；
- scorer 人工审计至少 50 个 discordant pairs。

## Stage 4 — Artifact audit

最少包含：

- exact-answer / label parser 对照；
- 输出格式控制；
- prompt paraphrase；
- token-length matched control；
- option / label permutation；
- baseline capability；
- task comprehension；
- relation validity re-audit；
- contamination / memorization 风险；
- refusal / default-label 率。

## Stage 5 — 第三家族与尺寸曲线

正式 phenotype 最好覆盖：

```text
Qwen: small + medium/large
Gemma: small + medium
Mistral / Llama / Phi: 至少一家
```

不是所有尺寸都必须失败，但必须预先定义：

- persistent failure；
- decreasing-with-scale；
- increasing-with-scale；
- emergent-at-capability；
- reasoning-model-specific。

不能事后把不一致都改写成 scaling story。

## 历史 Stage 4 — Exact collision audit（已废止：由 N0/N1 取代）

不得等现象出现后才第一次搜索。以下检索在 N0 先做，smoke 后以真实 signature 在 N1 更新：

```text
task + exact manipulation
task + effect shape
mother phenomenon + decisive contrast
mechanism vocabulary + manipulation
最新 arXiv / ACL / OpenReview / PMLR
```

逐项比较：

| 项目 | 最近工作 | 我们 |
|---|---|---|
| mother question |  |  |
| source distribution |  |  |
| manipulation |  |  |
| decisive contrast |  |  |
| cross-family law |  |  |
| mechanism claim |  |  |
| causal evidence |  |  |
| method |  |  |

若已有工作只覆盖母现象，但没有我们的结构性质，可以继续；若 decisive contrast 与机制问题都已覆盖，KILL。

## Stage 6 — Mechanism prerequisite

进入白盒前必须能写出：

```text
Mechanism A predicts observable/intervention A1.
Mechanism B predicts observable/intervention B1.
Mechanism C predicts observable/intervention C1.
```

以及：

- clean/corrupt matched pairs；
- content variable；
- role / gate / path variable；
- target semantic logit 或 deterministic output；
- unrelated-output controls；
- confirmation model。

## Stage 6 — Mechanism and method

推荐顺序：

```text
behavioral decomposition
→ representation readout（仅作为定位）
→ natural activation interchange
→ causal tracing / path patching
→ component/subspace intervention
→ selective rescue
→ mechanism-predicted training or routing method
```

SAE、probe、head ablation 都不是默认答案。

---

# 12. 从 anomaly signature 路由到机制问题

| 行为结构 | 优先 competing explanations | 优先白盒实验 | 可能方法口 |
|---|---|---|---|
| U-shape over position | attention allocation vs positional encoding vs retrieval policy | position-matched patching、attention output path patch | position-invariant routing / retrieval curriculum |
| cliff / phase switch | saturation vs learned gate vs decoder policy | boundary-layer causal tracing、gate subspace intervention | calibrated gate、soft routing、threshold regularization |
| content 相同、role 巨变 | role reader vs source trust vs alignment policy | role-token patch、Q/K selector 与 V/content 分离 | role-invariant verifier、source-calibrated router |
| local abilities 完好、composition 崩 | missing representation vs transport bottleneck vs commit failure | subanswer carrier patch、bridge path tracing | explicit composition interface、bridge-state transport |
| 同终态不同路径 | persistent history state vs update failure vs prompt recency | endpoint-state interchange、history carrier ablation | state canonicalization、rollback-aware memory |
| known entity 与 novel entity 反向 | parametric-context arbitration vs alias binding | factual memory heads/path 与 contextual carrier patch | conflict-aware router、entity unbinding |
| 更多正确信息反而更差 | evidence competition vs dedup/spam gate vs aggregation saturation | evidence-count sweep、source-attention patch | evidence de-correlation、aggregation normalization |
| reasoning model 才出现 | deliberation policy vs longer trace interference | base/reasoning matched path comparison | adaptive reasoning trigger、trace pruning |
| scale 越大 effect 越大 | newly learned circuit vs stronger priors vs alignment gate | cross-size representation alignment、component emergence | training objective targeted at emerging path |
| 事实会报告但行动不用 | content absent vs route closed vs late writer error | report/use four-cell interchange、semantic action logit | reader-gated writer、transport supervision |

机制命名必须由干预支持。不能先叫 reader/writer，再找一个可 probe 的方向来配名。

---

# 13. 方法口必须在发现后自然分叉

发现阶段只需写条件式方法预测：

```text
若信息没有形成：改 representation learning / data curriculum。
若信息形成但没跨边界运输：改 routing / bridge state / attention path。
若 source role 错误开关：做 source-calibrated gate。
若 current state 未 canonicalize：做 state compaction / rollback normalization。
若多个证据在聚合时饱和：做 correlation-aware aggregation。
若 late readout 绑定错 label/entity：做 binding-aware decoder / constrained decoding。
```

好方法应满足：

- 只在预测 failure condition 下介入；
- 保持 matched controls；
- 不依赖 gold answer；
- 优于无条件 steering / generic CoT；
- 修复强度随机制变量变化；
- 在至少一个 held-out task 或模板族迁移。

---

# 14. 小模型运行策略

## 14.1 小模型不是越弱越好

discovery model 必须先过 capability floor：

```text
control accuracy ≥ 60%（普通任务）
或显著高于 chance，且至少有 50 个 baseline-correct paired items
```

若模型根本不会原任务，任何 transformation effect 都没有解释价值。

## 14.2 本地模型面板

本机缓存已确认包括：

### Qwen

- Qwen2.5 `0.5B / 7B / 14B / 32B Instruct`；
- Qwen3 `0.6B / 1.7B / 4B / 8B / 14B / 32B`；
- Qwen3.5 `4B / 9B / 27B / 35B-A3B`。

### Gemma

- Gemma-3 `4B-IT / 12B-IT`。

### 其他家族

- Mistral-Small-24B-Instruct-2501；
- Phi-4-mini-instruct；
- LLaDA-8B-Instruct；
- Dream-v0-Instruct-7B；
- Pythia 小尺寸（更适合机制 sandbox，不适合承担 instruction phenotype）。

## 14.3 推荐面板

### Smoke

```text
Qwen3-4B or 8B
Gemma-3-4B or 12B
```

### Confirmation

```text
Qwen3-8B + Qwen3-32B
Gemma-3-4B + Gemma-3-12B
Mistral-Small-24B or Phi-4-mini
```

不要在 smoke 阶段同时启动所有大模型。

## 14.4 解码与复现

- `temperature=0` 作为主结果；
- 若研究随机选择 / confidence，另行预注册 sampling protocol；
- 保存 model revision、chat template、thinking mode；
- 输出 label 与答案文本都保存；
- scorer 同时检查 label 与 text，防止本轮 GPQA 式假低分；
- 不同模型必须用语义等价、但符合各自官方 chat template 的 prompt。

---

# 15. Harness 最小规格

## 15.1 组件接口

```text
dataset_adapter:
  load() -> examples
  render(example) -> canonical_input
  gold(example) -> canonical_gold

transform:
  applicable(example) -> bool
  apply(example, strength, seed) -> transformed_example
  map_gold(gold) -> transformed_gold
  validate(original, transformed) -> checks

runner:
  model + prompt + decoding config -> raw output

scorer:
  raw output + canonical gold -> score + parse diagnostics

analyzer:
  paired records -> anomaly signature
```

## 15.2 每条记录必须保存

```json
{
  "dataset": "...",
  "split": "...",
  "item_id": "...",
  "relation_family": "monotonicity",
  "transform_id": "...",
  "strength": 3,
  "seed": 27,
  "original_input": "...",
  "transformed_input": "...",
  "original_gold": "...",
  "transformed_gold": "...",
  "relation_checks": {},
  "model_family": "...",
  "model_revision": "...",
  "chat_template_hash": "...",
  "raw_output": "...",
  "parsed_output": "...",
  "correct": true,
  "parse_ok": true,
  "latency": 0.0,
  "token_counts": {}
}
```

## 15.3 每个 anomaly 输出

```text
rank
one_sentence_description
dataset × transform × model panel
effect by family and size
paired help/hurt counts
shape label and curve
interaction / dissociation
capability floor
nuisance controls
top representative pairs
failure clusters
artifact risks
nearest-work search queries
mechanism hypotheses
method branches
verdict: PROMOTE / HOLD / KILL
```

## 15.4 推荐目录

```text
phenomenon_miner/
  adapters/
  transforms/
    invariance/
    equivariance/
    monotonicity/
    reversibility/
    composition/
  scorers/
  configs/
  runs/
  reports/
  killed/
  promoted/
```

矿机代码强调可审计和快速杀题，不需要先做成通用软件产品。

---

# 16. 最常见的假阳性

## 16.1 Scorer 假象

模型输出：

```text
B. 10^-4 eV
```

gold：

```text
10^-4 eV
```

若 exact string scorer 判错，会制造 90% 的假 collapse。所有 MCQA 同时解析 label 与 answer text，并人工审计。

## 16.2 Default-label / default-No

主条件答对不等于会推理。必须有：

```text
same-query positive control
label-balanced examples
answer swap
Yes/No reversal
```

本轮 identity-opacity 初看有 12–48 pp 差异，但 Qwen 连“人物明确相信原句”也大量答 No；缺少 control 会误称身份泄漏。

## 16.3 Capability floor 不足

弱模型在 control 与 treatment 都接近 chance 时，方向可以随 seed 漂移。不能为了找到 failure 换越来越弱的模型。

## 16.4 Relation 实际失效

- 日期平移跨越闰日；
- 单位转换改变舍入；
- premise permutation 改变指代；
- quote / fiction 改变了真值；
- 删除 option 改变了 pragmatic context；
- identity alias 不是严格共指；
- 多一条证据来自同一来源，不等于独立证据。

先验证关系，再解释模型。

## 16.5 长度与位置混杂

增加 evidence 也增加 token 数；分成多文档也增加 header；加入提示也移动原证据。至少做 token-matched filler 与 position-matched control。

## 16.6 Prompt hunting

发现一个模板有大效应后不断换措辞，只保留最大值，不是 discovery。主模板、两个 paraphrase 与停止门槛必须冻结。

## 16.7 平均数掩盖交换错误

baseline 与 transform 准确率都 60%，可能有 40% items 互相翻转。保存 paired consistency；稳定答案本身也是现象维度。

## 16.8 “跨模型”只是共同 artifact

两个模型都使用相似 chat template、相同 scorer 或同一训练数据，并不自动排除 artifact。第三家族与语义控制仍必要。

## 16.9 先命名后筛样本

先叫“fan effect”，再只保留随 entity fan 下降的关系类型，会把现象造出来。分层只能用于解释已经冻结的 overall effect。

---

# 17. 本轮已经运行、不要原样重跑的负结果

这些结果用于校准矿机，不应包装为论文，也不应由下一模型无理由重复。

## 17.1 SciQ：正确 support 与重复

200 个公开 SciQ items：

- Qwen3-8B：closed `94.5%`，support ×1/2/4 为 `97.0/96.5/97.0%`；
- Gemma3-12B：closed `93.0%`，support ×1/2/4 均约 `98.0%`；
- 删除错误选项与只留正确项没有反直觉大跌。

结论：没有 monotonicity violation。

## 17.2 GPQA：删除错误选项

198 个 GPQA Diamond items：删除不同错误选项会产生 paired flips，但总体不形成跨模型同构大异常；而且 ACL 2025 已明确研究 adding/removing incorrect options 的波动。结论：宽叙事撞车。

## 17.3 PopQA：part-list cueing

100–300 条事实负载下，Qwen/Gemma 只有 `0–4 pp` 零散波动；target cue 自身也会偶尔伤害。结论：长度 / generation noise，非稳定选择性效应。

## 17.4 MuSiQue / MoreDocs：文档边界组合

240 个公开多跳问题，同一 supporting paragraphs 标成一个或多个文档：

- Qwen3-8B 总差约 `1.7 pp`；
- Gemma3-12B 总差约 `2.1 pp`；
- hop 分层方向不稳定，Gemma 4-hop 无差。

结论：没有“局部完好、跨边界组合崩溃”的强 dissociation。

## 17.5 Intensional identity opacity

显式写明 agent 不知道两个 alias 共指，模型仍做共指替换：

- Qwen3-8B 约 `12%` 选择性错误；
- Gemma3-12B 约 `17%`。

效应不足；更宽的 prompt 还暴露 Qwen default-No / premise-comprehension confound。只能保留为低优先级 anchor，不能宣布现象。

## 17.6 GPQA：verified negative evidence

修正 label scorer 后：

- Qwen3-8B：baseline `38.9%`，排除 1/2/3 个错误项 `46.0/59.6/96.0%`；
- Gemma3-12B：`41.9% → 43.4/57.6/95.5%`。

基本严格单调，没有 negative-evidence attraction。

这些 KILL 结果说明：一句话很好听不够；必须让结构签名自己说话。

---

# 18. 新颖性审计：母现象可以已有，但新性质必须真实

## 18.1 三层 novelty

### 层 1：component overlap

别人研究过 attention、knowledge conflict、ToM、RAG、option order。允许。

### 层 2：mother phenomenon overlap

别人知道“多文档变难”“模型有知识冲突”“模型对 premise order 敏感”。仍可能允许。

### 层 3：decisive contrast overlap

别人已经报告：

- 同一个 factorial；
- 同一种非线性 shape；
- 同一个 local-vs-composition dissociation；
- 同一个跨尺寸规律；
- 同一个 causal gate；
- 同一个 selective repair。

若层 3 被覆盖，基本 KILL。

## 18.2 可以成立的新增性质

例如母现象是“知识冲突”，我们的新性质可以是：

- 只在 fictional frame 下符号反转；
- 退出 fictional frame 后存在 hysteresis；
- local report 正确但 action use 错；
- scale 越大冲突越强；
- 一个低维 ontology gate 因果控制 context / memory routing。

但这些性质必须先在数据中出现，不能为了避撞车事后发明。

## 18.3 文献搜索时机

- 写 transformation 后、调用模型前：完成 N0 exact phenotype、母现象包含与全文/appendix 审计；
- N0 后完成 D0 数据/license/gold/20例审计并取得明确授权；
- smoke 有异常后、扩模型前：完成 N1 actual-signature audit；
- 机制前：查 representation / circuit 邻近工作。

既不能先读 100 篇把 hypothesis space 限死，也不能跑完昂贵实验才发现 exact paper。

---

# 19. 每日工作流

## 上午：生成候选并先做 N0/D0

先完成 exact/母现象全文审计、独立复核与数据抽样；未授权候选当天不得进入模型队列。

## 通过授权后：生成与验证 relations

1. 从一个公开 dataset 采样 50 items；
2. 为 3–5 个 axes 写 deterministic transforms；
3. 自动 relation checks；
4. 人工读每轴 10 对；
5. 删除不自然或 gold 可疑的轴。

## 下午：两模型 smoke

1. 每轴 30–50 paired items；
2. 两家族并行；
3. 自动输出 effect、flips、shape、parse failures；
4. 人工查看最强 20 个 discordant pairs；
5. 大多数 axes 当天 KILL。

## 晚上：只审最强异常

对前 1–3 名问：

- 一句话能否说明？
- control 能力是否完好？
- 两家族方向是否一致？
- 是否只是 scorer / length / label？
- 原始例子是否真的怪？
- exact phenotype 是否已有？
- 若成立，内部至少有什么两种解释？

没有异常的日子是正常结果，不要为了“今天必须有题”降低门槛。

---

# 20. 候选报告模板

```markdown
# Candidate: 暂不命名

## One-sentence observation
即使 ______ 相同，只改变 ______，模型也从 ______ 变成 ______。

## Source distribution
- dataset / split / license:
- original task:
- why natural:

## Relation
- family:
- formal constraint:
- gold mapping:
- invalid edge cases:

## Frozen manipulation
- control:
- treatment:
- strength axis:
- nuisance controls:

## Behavior
| model | control | treatment | Δ | help | hurt |
|---|---:|---:|---:|---:|---:|

## Shape / dissociation
- curve:
- interaction:
- target vs control capability:
- scaling trend:

## Artifact audit
- parser:
- token length:
- label/order:
- prompt paraphrase:
- baseline competence:

## Representative paired cases
1. ...
2. ...
3. ...

## Nearest-work audit
- mother phenomenon:
- closest decisive contrast:
- what remains genuinely new:

## Competing mechanisms
- A:
- B:
- C:
- discriminating interventions:

## Method branches
- if A:
- if B:
- if C:

## Verdict
PROMOTE / HOLD / KILL
```

---

# 21. 可直接交给下一小模型的总提示词

```text
你正在操作一个内部 phenomenon miner。你的目标不是提出 testing framework，
也不是先选择一个已命名认知偏差。phenomenon 必须是扫描输出。

每轮只做以下工作：

1. 先读 DATASET_CATALOG.md，从对应领域选择一个本地已缓存或明确注册的公开 benchmark。
2. 选择 3–5 个理论上有效的 invariance / equivariance / monotonicity /
   reversibility / composition relations。
3. 在调用模型前证明 gold mapping，写自动 validator，人工抽查 20 对。
4. 先运行 30–50 paired items，模型使用两个有基础能力的独立家族。
5. 保存 raw outputs；同时解析 answer label 与 answer text。
6. 报告 paired effect、help/hurt flips、capability floor、曲线形状和 parse failures。
7. 任何模型 control 不会任务，或两家族不同方向，或 effect <5 pp 且无结构，立即 KILL。
8. 只有 >15 pp、或出现 cliff/U-shape/sign reversal/强 interaction/dissociation 的候选才扩到 200–500 对。
9. 扩样本后做 token length、paraphrase、label、order、scorer 与 default-answer controls。
10. 调用模型前完成 N0 exact/母现象全文审计；smoke 后按真实错误 signature 完成 N1，二者都比较 decisive contrast，不只比关键词。
11. 在提出机制前写至少两个互斥解释与各自的因果预测；在提出方法前说明不同机制为何导向不同修复。
12. 不得换更弱模型、挑 subset、挑 prompt 或放宽 scorer 来续命。

自然性要求：一句话能说明；优先原 benchmark 的移动、重排、重命名、增删、分组与可逆更新。
禁止用 task、rule、label、interface 全自定义的数据独自把项目晋级。

先读“本轮已经运行、不要原样重跑的负结果”，不要重复浪费预算。
每轮最终只输出：运行了什么、完整数字、代表 case、artifact 判断、PROMOTE/HOLD/KILL，以及下一轮唯一最有信息量的实验。
```

---

# 22. 最终原则

1. **Phenomenon is an output, not an input.**
2. **公开自然任务提供分布，relation 提供 oracle。**
3. **优先寻找 broken invariants，不优先列认知偏差。**
4. **大的平均 drop 不如选择性 dissociation；平滑下降不如结构性非线性。**
5. **跨家族同方向先于白盒解释。**
6. **能力不够、scorer 错、default answer 和 prompt artifact 都能伪造现象。**
7. **母现象可以已有；真正的新颖性看 decisive contrast 与整套叙事。**
8. **机制必须裁决 competing explanations，不能停在 probe/readout。**
9. **方法必须由机制推出，不能最后补一个 LoRA 或 steering。**
10. **快速杀死 99 个轴，是找到第 100 个真正异常的正常成本。**

我们每天真正要问的不是：

> 今天又找到哪个已知 bias 可以解释？

而是：

> **今天，在一个答案本应不变或只能按已知方式变化的地方，模型到底做了什么离谱而稳定的事情？**
