# 研究方案：正确的值，错误的槽位——结构化生成中的角色—值绑定失败

**状态：** `PRE-CANDIDATE / NOT YET ACTIVE`  
**冻结日期：** 2026-08-26  
**第一目标：** 在投入可解释性分析之前，先用公开数据和公开模型输出判断“自然角色—值绑定错误”是否真实、稳定、足够一般。  
**目标尺度：** ACL / EMNLP / NAACL Main 常规宽度，而不是某个 API 的 bug report。

---

## 1. 母问题

很多结构化 NLP 任务都要求把文本中的值绑定到语义角色。例如：

```text
Tokyo -> origin
Osaka -> destination
```

模型可能同时满足：

1. 工具选对；
2. Tokyo 和 Osaka 都看到了；
3. JSON 语法合法；
4. 但输出：

```json
{"origin": "Osaka", "destination": "Tokyo"}
```

本项目不泛泛研究“为什么工具参数会错”，而问一个更具体、可以被因果实验裁决的问题：

> **当正确值已经可用时，结构化生成中的错误究竟发生在值提取、角色语义、角色—值绑定，还是最终序列化阶段？**

这四个故障阶段对应完全不同的修复方法。因此，可解释性在这里不是附加分析，而是用来决定“应该修哪里”。

---

# 2. 研究对象为什么自然

“角色—填充值绑定”不是 LLM 特有现象。经典语义表示、信息抽取和认知中的 role-filler binding 都要求区分：

```text
Alice ordered tea from Bob.
customer=Alice, seller=Bob

Bob ordered tea from Alice.
customer=Bob, seller=Alice
```

同一组实体因为关系结构不同，应绑定到不同角色。

结构化生成给这个老问题带来一个新的实验优势：

- schema 中角色明确；
- ground truth 精确；
- 输出可以自动解析；
- 自然错误可以从真实 benchmark 中直接筛出；
- 不需要 LLM-as-a-judge；
- 后续可以对同一错误做内部表示和因果干预。

因此我们研究的不是“某模型某层有一个方向”，而是一个模型外部先存在的问题：

> **正确内容如何被绑定到正确结构角色。**

---

# 3. Novelty package 与 collision audit

目标不是证明“从来没人碰过 binding”，而是确认我们的核心叙事没有被完整做掉。

## 3.1 已经不能 claim：generic parameter failure

EMNLP Findings 2025：

- *Butterfly Effects in Toolchains: A Comprehensive Analysis of Failed Parameter Filling in LLM Tool-Agent Systems*  
  https://aclanthology.org/2025.findings-emnlp.907/

该工作已经：

- 建立 parameter failure taxonomy；
- 分析多类输入扰动；
- 研究 tool-agent parameter filling 的行为失败；
- 提出可靠性建议。

因此我们不能讲：

> “首次研究 LLM 工具参数为什么会填错。”

我们的 decisive contrast 必须更具体：

> **在正确值已经可用、工具和 schema 都正确的条件下，错误发生在 role semantics、role–value association，还是 serialization。**

## 3.2 已经不能 claim：tool identity 的内部表示

2026：

- *Tool Calling is Linearly Readable and Steerable in Language Models*  
  https://arxiv.org/abs/2605.07990

已有结果表明：

- tool identity 可以从内部表示中线性读出；
- 可以 steering 工具选择；
- 工具名被改变后，后续 argument schema 会自回归适配；
- 但在同一工具下把参数值从 Tokyo steering 到 Paris 的实验为 `0/30`；
- 作者明确指出 argument content 与 tool identity 的内部组织不同，参数值更多是根据 query 动态取得；
- 论文评测主要保证目标 tool/schema，并没有把 argument value correctness 作为机制对象。

因此它不是我们的论文，但它给出了一个很重要的局部前提：

> **tool identity 的机制不能直接外推到 argument binding。**

## 3.3 已经不能 claim：LLM 中首次存在低维 binding 表示

ACL 2026 Main：

- *Cell-Based Representation of Relational Binding in Language Models*  
  https://aclanthology.org/2026.acl-long.2194/

该工作在受控关系任务中：

- 研究 entity–relation–attribute binding；
- 用 Partial Least Squares 找到低维 binding subspace；
- 做跨 domain、跨模型验证；
- activation patching 可以因果改变 relational prediction。

因此我们不能说：

> “首次证明 LLM 内部有 role/relation binding。”

它提供的是**技术可行性先例**。

## 3.4 structured-output 行为 benchmark 已经很多

近邻包括：

- JSONSchemaBench: https://arxiv.org/abs/2501.10868
- CONSTRUCT: https://arxiv.org/abs/2603.18014
- ExtractBench: https://arxiv.org/abs/2602.12247
- LlamaIndex ExtractBench: https://arxiv.org/abs/2607.29677

它们说明 schema compliance、field correctness、完整性和 wrong-field/wrong-record 都是真实现象。

截至本轮检索，没有发现一篇已经完整完成下面这条链：

```text
自然 role-value swap failure
-> 排除 extraction / schema / tool-selection
-> value vs role vs binding vs serialization 阶段诊断
-> 内部因果定位
-> 由故障阶段导出不同修复方法
-> 第二个结构化任务验证
```

因此当前 collision 判定：

`YELLOW-GREEN / 可以做低成本 G0 / 不能提前宣布 novelty 成立`

如果后续再发现母问题级论文，立即停止，不靠换模型或换数据续命。

---

# 4. 为什么 G0 选 BFCL V4 `simple_python`

BFCL：

- Leaderboard: https://gorilla.cs.berkeley.edu/leaderboard
- Official code: https://github.com/ShishirPatil/gorilla
- Official result archive: https://github.com/HuanzhiMao/BFCL-Result

冻结版本：

```text
BFCL data/eval:
f7cf7359b7ac615a0b294831c5ba2bc95ee4a000

BFCL result archive:
6830ed13035c0cfee9aa7a9a0ffed70f10b3dd50
snapshot = 2025-12-16
```

选择 `simple_python` 不是因为它最流行，而是因为它对我们的科学问题有三个关键优势。

## 4.1 每个样本只提供一个函数

第一阶段天然消掉：

```text
wrong tool selection
```

如果从多工具任务开始，参数错误可能只是模型先选错工具，后面的 binding 解释会被污染。

## 4.2 ground truth 是字段级、结构化、带 acceptable values

答案类似：

```json
{
  "origin": ["New York City"],
  "destination": ["Washington D.C."]
}
```

因此可以严格自动判断：

- key 是否正确；
- value 是否属于接受集合；
- 两个值是否只是被交换；
- 是否存在 missing / hallucinated key。

## 4.3 官方原始模型输出已经公开

第一枪不需要自己跑模型：

```text
公开数据
+ 公开 raw responses
-> CPU 自动分类
-> 如果自然错误不存在，0 GPU kill
```

只有这个阶段通过，才允许本地跑开源 checkpoint 获得 hidden states。

---

# 5. G0-A：先冻结哪些样本有资格讨论 binding

**必须在看模型错误之前完成 eligibility。**

第一阶段只研究 direct-copy binding。

一对 required slots `(r1, r2)` 只有同时满足以下条件才 eligible：

1. 两个 slot 都是 required；
2. schema type 相同；
3. 两个正确值不同；
4. 每个 slot 至少有一个 BFCL accepted scalar value 作为独立 literal 明确出现在用户问题中；
5. 不依赖计算、常识推断、单位转换或默认值。

例如：

```text
origin:string = Tokyo
destination:string = Osaka
```

是好的 binding 对。

而：

```text
destination:string = Tokyo
days:int = 7
```

不适合第一阶段，因为类型本身就是强约束。

同样：

```text
area = 50
```

如果需要根据 base 和 height 算出来，也不进入第一阶段，因为这会混入 computation/extraction failure。

实现：`binding_probe.classify.binding_eligible_pairs`。

---

# 6. G0-B：strict natural binding error 的冻结定义

一个输出只有同时满足以下条件，才记为 `strict_natural_binding`：

1. function name 正确；
2. required keys 全部存在；
3. 没有未知 schema key；
4. optional field 若被输出，也必须正确；
5. required predicted values 都来自本样本 required ground-truth value 集合；
6. 至少两个 required roles 错误；
7. 错误恰好构成 ground-truth values 在 roles 间的一一置换；
8. 每条错配边都必须属于 G0-A 在看输出前冻结的 eligible same-type/direct-copy role pair。

通过：

```text
GT:   origin=Tokyo, destination=Osaka
Pred: origin=Osaka, destination=Tokyo
```

不通过：

```text
origin=Nagoya, destination=Osaka     # value error
origin=Tokyo                         # missing key
origin=Tokyo, foo=Osaka              # schema error
```

这样可以防止我们为了得到“binding 现象”而事后放宽定义。

代码会额外区分：

- `parse_failure`
- `wrong_tool`
- `schema_key_error`
- `value_error`
- `mixed_value_error`
- `pure_binding_permutation`
- `correct`

只有 `pure_binding_permutation` 中满足预注册 eligible edge 的子集才算 strict natural binding。

---

# 7. G0-C：零 GPU 公共轨迹审计

## 7.1 Discovery model

先用官方公开：

```text
Qwen_Qwen3-4B-Instruct-2507-FC
```

理由：

- 4B，后续机制实验成本低；
- BFCL 已公开结果；
- Qwen tool-call template 明确；
- 最近 tool-selection mechanism 工作研究过类似 Qwen 规模，便于衔接。

## 7.2 Cross-family behavior sanity

同时检查官方：

```text
google_gemma-3-4b-it
```

此处只看行为，不要求两个家族的具体 layer/head 一致。

分类器已经支持：

- Qwen `<tool_call>{...}</tool_call>`；
- BFCL prompt-mode `[func(key=value)]`。

## 7.3 feasibility gate：在看结果前冻结

这些阈值不是统计显著性标准，而是“值不值得投入机制实验”的工程门槛。

### GREEN：进入本地复现和机制阶段

Discovery model 同时满足：

- `>=20` 个 strict natural binding errors；
- 覆盖 `>=8` 个不同 function schemas；
- 单一 function 不贡献超过 25% 错误；
- 第二模型至少 `>=5` strict errors，覆盖 `>=3` schemas。

为什么需要这种规模？

因为后续必须按 function schema 分组做 held-out validation。如果错误只有 3–5 个，或者都来自同一 API，那么任何 probe/patch 结果都可能只是模板特例，撑不起 ACL Main 尺度。

### YELLOW：只允许扩到现成公开数据

如果 `simple_python` 的 eligible denominator 本身 `<80`，可以扩到 BFCL **已有**的其他单工具/simple 类别，继续使用完全相同的冻结 detector。

不允许：

- 自己先造几千条 origin/destination；
- 看错误后再修改 eligibility；
- 为提高错误数放宽到 derived/default values。

### RED：杀题

满足任一：

- eligible denominator 足够，但 discovery model `<5` strict errors；
- pooled public outputs 仍无法形成跨 schema cohort；
- 错误主要是 value extraction / missing key，而不是 binding permutation；
- strict errors 基本只出现在某一个 function/schema。

RED 的科学结论就是：

> **自然 role-value swap 不是足够大的现实 failure surface。**

停止，不转成合成 benchmark 续命。

---

# 8. G0-D：只有 GREEN 后才做本地 deterministic reproduction

Discovery checkpoint：

```text
Qwen/Qwen3-4B-Instruct-2507
```

冻结解码：

```text
do_sample = False
max_new_tokens = 192
thinking = off（模板支持时）
bfloat16 on GPU
```

只跑已经冻结的 eligible IDs。

如果本地输出与 BFCL 官方结果明显不一致，先排查：

- tokenizer/template revision；
- transformers version；
- function-calling handler；
- model revision。

在 reproduction 没对齐之前，不做 hidden-state claim。

---

# 9. 机制阶段：四个竞争解释

只有自然错误 G0 通过后才进入。

## H1：值提取失败

模型并没有在内部稳定获得正确 fillers。

预测：

- 在输出前，正确 filler identity 已经不可恢复或被错误值替代；
- 即使给定正确 role，也偏向错误 filler；
- 修复较早的 filler representation 才能恢复答案。

如果 H1 成立，论文不应强行叫 binding mechanism，而应转向 grounded value extraction。

## H2：角色语义失败

fillers 正确，但 schema roles 没被正确区分。

例如：

```text
origin vs destination
start vs end
sender vs receiver
```

预测：

- filler identity 正确；
- role-conditioned compatibility 已经错误；
- schema description 的匹配改写会显著影响错误。

## H3：真正的 role–value binding 失败

模型分别知道 fillers，也理解 roles，但 association 错了。

预测：

- value identity 与 role identity 分别正确；
- role–filler compatibility 偏向错误 permutation；
- 选择性 causal patch 可以交换 assignment，而不改变 tool、schema key set 和 filler set。

## H4：binding 正确，但序列化阶段失败

在真正输出 tool call 前，内部 assignment 是正确的；错误在自回归生成字段值时才产生。

预测：

- pre-output role–filler matching 仍偏好正确 pairing；
- teacher-forced 到具体 field/value token 时 margin 才翻转；
- 前期 representation 修复无效，两阶段 structured decoding 更有效。

---

# 10. 表示实验：probe 只能当诊断工具

不能做：

```text
全层训练 origin/destination classifier
-> 找最高 AUROC
-> 宣布模型有 binding representation
```

这无法区分词汇、schema 和真正 association。

## 10.1 matched counterfactual

只从已经存在的 eligible example 派生最小 filler swap：

```text
A: from Tokyo to Osaka
B: from Osaka to Tokyo
```

两条文本的 filler set 完全相同：

```text
{Tokyo, Osaka}
```

只有角色 assignment 改变。

代码中的 `counterfactual.py` 只在两个 literal 各出现一次时才允许交换；出现歧义就返回 `None`。

这些 counterfactual **只能在自然 failure G0 通过以后使用**，目的是做 matched causal pairs，不是用来人为制造行为现象。

## 10.2 role–filler compatibility，而不是单独 role classifier

更合适的对象是一个低容量 compatibility score：

```text
s(role_i, filler_j) = filler_j^T W role_i
```

训练正例：正确 pairing。  
训练负例：**同一个样本内部**的 filler permutation。

关键要求：

- function schema 整体分组切分 train/dev/test；
- 同一 function 的不同样本绝不能跨 split；
- layer 选择只能在 dev 上完成；
- 最终结果在 held-out schemas 报告；
- 必须有 shuffled-label control；
- 不允许用 test error examples 调 probe 超参数。

如果一个 representation 只在同 schema 内有效，不能称为一般 binding representation。

## 10.3 自然错误上的关键判别

在自然错误样本中比较：

```text
正确 pairing score
vs
错误 permutation score
```

如果很早就偏向错误值，支持 H1/H2/H3 中的前期失败。

如果在生成前一直偏好正确 pairing，到具体字段生成时才翻转，更支持 H4。

---

# 11. 序列化阶段定位

要区分 H3 与 H4，仅看 hidden state 不够。

对同一 prompt 做 teacher forcing：

```text
... "origin":
```

比较：

```text
log P(Tokyo | prefix)
log P(Osaka | prefix)
```

再到：

```text
... "destination":
```

比较相反的 filler margin。

同时跟踪：

- tool name 前；
- argument key 前；
- key 后、value 前；
- 第一个 value 生成后；
- 第二个 value 生成前。

如果内部 assignment 本来正确，但第一个 value token 一生成就污染后面的 binding，这会形成非常明确的 serialization failure 证据。

---

# 12. 因果实验：必须是选择性的 on-manifold intervention

只有表示实验发现稳定、跨 schema 的候选 component 后才进入。

## 12.1 干预对象

优先使用 matched A/B filler-swap pair 的真实 activation interchange。

不优先使用：

- 大倍数 steering vector；
- 随机放大某个 SAE feature；
- 全层全 head brute-force sweep。

原因是这些操作容易把隐藏状态推到 off-manifold 区域，出现“输出变了但不是我们声称的机制”。

## 12.2 选择性成功标准

一次 causal repair 只有满足以下条件才算支持 binding claim：

应该改变：

- target role 绑定到哪个 filler；
- 或修复 strict natural binding error。

必须保持：

- tool/function name；
- schema key set；
- filler value set；
- 与目标 role pair 无关的其他参数；
- structured-output validity。

也就是说，不能只是让模型“更偏向 Tokyo”；必须改变：

> **Tokyo 属于哪个 role。**

## 12.3 Negative controls

至少包括：

- 同维数随机/正交子空间 patch；
- unrelated-example activation patch；
- sham patch；
- filler identity control；
- tool identity control。

如果所有 slot 都被推向同一个值，只说明找到了 value steering，不是 binding。

---

# 13. 结果如何决定方法

方法必须由机制结论推出，不允许最后硬塞一个 LoRA。

## 如果 H1：value extraction

方法方向：

- input-span-grounded argument extraction；
- copy-aware value objective；
- 先定位 source span，再形成 structured value。

## 如果 H2：role semantics

方法方向：

- schema-role contrastive objective；
- 对容易混淆的 role pair 做 description-level hard negatives；
- schema role disambiguation training。

## 如果 H3：binding

方法方向：**binding-consistency objective**。

原始 supervision 已经有：

```text
(origin, Tokyo)
(destination, Osaka)
```

不需要新人工标签，可以直接把同一个调用内部的 swapped pairing 当 hard negatives：

```text
(origin, Osaka)
(destination, Tokyo)
```

训练目标显式要求：

```text
score(correct pairing) > score(permuted pairing)
```

## 如果 H4：serialization

方法方向：**two-stage binding-preserving decoding**。

阶段一先形成语义 assignment：

```text
origin -> Tokyo
destination -> Osaka
```

阶段二只负责把冻结 assignment 序列化成 JSON/tool protocol。

这样可以避免某个字段的自回归 token 对下一个字段 association 造成污染。

---

# 14. 方法评测不能只看总 BFCL 分数

至少同时报告：

1. strict natural binding error rate；
2. non-binding parameter error rate；
3. overall BFCL simple accuracy；
4. structured validity；
5. wrong-tool rate；
6. 对非目标错误类型是否有副作用。

如果方法只是让模型更保守、少输出参数，从而 binding error 看起来下降，不算成功。

---

# 15. 什么时候才能把题目从 tool calling 提升到 structured generation

只做 BFCL 时，论文主张必须写成：

> role–value binding failures in function/tool calling

不能直接声称“structured generation 的统一机制”。

只有在第二个**非 tool-calling**任务复现同一阶段性机制，才允许提升叙事。

优先候选：

- ExtractBench：schema-guided document extraction；
- CONSTRUCT：structured-output fields。

外部验证重点不是再刷一个总分，而是检查：

> value identity 正确、field identity 正确，但 field–value association 错误时，是否出现与 BFCL 相同的故障阶段。

这一步只在 BFCL 机制已经明确后做。

---

# 16. 模型策略

## Discovery

优先：

```text
Qwen/Qwen3-4B-Instruct-2507
```

理由：开源、便宜、原生工具模板清楚、官方 BFCL 轨迹存在。

## Confirmation

至少一个不同 family，例如 Gemma。

要求复现的是**计算阶段结论**：

```text
extraction / role / binding / serialization
```

不要求具体 layer/head 编号相同。

如果只有 Qwen 成立，必须降级为 model-family-specific mechanism，不能硬写一般结论。

---

# 17. 成本阶梯

整个项目严格按从便宜到昂贵排序。

## Stage 0：文献 + eligibility

- CPU；
- 400 条 simple_python；
- 秒到分钟级。

## Stage 1：官方公开结果审计

- 0 GPU；
- 下载 JSONL；
- CPU 分类。

## Stage 2：本地 deterministic reproduction

- 只跑 eligible IDs；
- Qwen 4B；
- 单卡足够。

## Stage 3：hidden-state readout

- 只有 GREEN 后进入；
- 只保存预先选定 token positions；
- 不默认保存所有层 × 所有 token 的全部激活。

## Stage 4：causal patching

- 只在已选 layer/site 和 matched pairs 上；
- 不做无目的 layer × head × SAE 大网格搜索。

## Stage 5：method training

- 只有 causal mechanism 确认后进入。

这样保证最可能失败的门槛发生在最便宜的阶段。

---

# 18. 禁止续命规则

以下情况直接停止当前 mother route：

1. public natural binding errors 太少；
2. 错误只来自单一 API/schema；
3. 主要错误其实是 value extraction；
4. 只能同 schema probe，跨 schema 完全失效；
5. activation intervention 无法选择性改变 binding；
6. 所谓 binding component 实际是 generic value/compliance/tool direction；
7. 必须大规模生成新合成数据才能得到行为现象；
8. 必须靠 SAE 才能“找到”一个 construct，而行为/paired causal analysis 不支持。

不得把失败题改写成：

> “某个 origin/destination circuit”

来续命。

---

# 19. 代码与阶段对应

| 文件 | 当前职责 |
|---|---|
| `src/binding_probe/bfcl.py` | pinned BFCL 数据、schema 转换、JSONL I/O |
| `src/binding_probe/fetch.py` | 下载 pinned BFCL category + answers |
| `src/binding_probe/scan.py` | 在看模型输出前冻结 eligible examples |
| `src/binding_probe/official.py` | 下载 pinned BFCL 官方模型 raw responses |
| `src/binding_probe/classify.py` | 解析输出、错误 taxonomy、strict detector、Wilson CI |
| `src/binding_probe/infer_hf.py` | 本地 deterministic HF tool-calling reproduction |
| `src/binding_probe/counterfactual.py` | G0 通过后构造 matched filler-swap pair |
| `tests/test_classifier.py` | strict definition 单元测试 |

当前**故意没有**预先写大规模 hidden-state / activation-patching harness。

原因不是做不了，而是 executable-first 原则要求：

> 在自然 failure 通过之前，不应先投入大量 model-specific mechanism code。

一旦 G0 GREEN，下一次提交才实现冻结模型对应的最小机制 harness。

---

# 20. 第一轮执行顺序

```text
0. pytest
1. binding-fetch --category simple_python
2. binding-scan -> eligible set
3. binding-official(Qwen3-4B)
4. binding-classify(Qwen3-4B)
5. binding-official(Gemma3-4B)
6. binding-classify(Gemma3-4B)
7. 按预注册 gate 判 GREEN / YELLOW / RED
8. 只有 GREEN -> 本地 Qwen 重跑 eligible IDs
9. reproduction 对齐 -> 冻结机制实验设计
```

仓库提供：

```bash
bash scripts/run_public_g0.sh
```

完成第 1–6 步，且第一阶段不需要 GPU。

---

# 21. 这轮真正要回答的问题

第一轮不是为了证明一个漂亮机制，也不是为了尽快写论文。

第一轮只回答：

> **公开真实结构化生成数据中，是否存在足够多、足够分散、定义足够严格的“正确值被绑定到错误槽位”的自然错误，使得后续机制研究值得投入？**

如果答案是否定的，本题应在最便宜的阶段被杀掉。

如果答案是肯定的，我们才有资格继续问：

> **这些错误在模型内部究竟发生在哪一步，以及这个机制是否能指导一个针对性的修复方法。**
