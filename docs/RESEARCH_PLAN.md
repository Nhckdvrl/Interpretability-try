# 研究方案：正确的值，错误的槽位——结构化生成中的角色—值绑定失败

**状态：** `PRE-CANDIDATE / NOT YET ACTIVE`  
**方案冻结日期：** 2026-08-26  
**第一目标：** 在投入机制分析前，用公开数据和官方公开输出判断自然 binding failure 是否足够稳定、足够一般。  
**目标会议尺度：** ACL / EMNLP / NAACL Main 的常规宽度，而不是一个 API-specific bug report。

---

## 1. 母问题

很多结构化 NLP 任务都要求把从文本中获得的值绑定到语义角色：

```text
Tokyo  -> origin
Osaka  -> destination
```

模型可能：

1. 选对工具；
2. 看到/提取出 Tokyo 与 Osaka；
3. 生成合法 JSON；
4. 却输出：

```json
{"origin": "Osaka", "destination": "Tokyo"}
```

本项目不问泛泛的“为什么工具参数会错”，而问一个更具体、可因果区分的问题：

> **当正确值已经可用时，结构化生成中的错误发生在值提取、角色语义、角色—值绑定，还是自回归序列化阶段？**

如果能区分这些阶段，方法设计就不再是统一地“多训一点 function calling”，而可以针对实际失败步骤修复。

---

# 2. 为什么这个问题值得研究，但现在还不能宣布成立

## 2.1 外部 construct 是自然的

“role-filler binding” 本身是经典认知/NLP 问题：同一组 filler 可以因为关系结构不同而绑定到不同角色。例如：

```text
Alice ordered tea from Bob.
customer=Alice, barista=Bob

Bob ordered tea from Alice.
customer=Bob, barista=Alice
```

结构化生成恰好把这个抽象问题变成了一个**具有精确 gold、可以自动检测真实失败**的应用场景。

但我们绝不能声称“首次发现 role-filler binding”或“首次发现 LLM 内部存在 binding”。已有工作已经覆盖这些更宽的主张。

## 2.2 真正可能的新叙事

我们希望验证的 novelty package 是：

```text
自然结构化生成 failure
-> 严格排除 extraction / schema / tool-selection 混淆
-> 区分 binding 前、binding 本身、binding 后序列化三类计算失败
-> 用 on-manifold 因果干预裁决
-> 由故障阶段导出不同修复方法
-> 在第二个结构化任务上检验是否可推广
```

只要其中第一步“自然 failure 稳定存在”不成立，后面全部停止。

---

# 3. 近期文献与 collision audit

本节的目标不是“证明没人做过”，而是明确：哪些贡献已经不能 claim，哪些关键对照仍然可能开放。

## 3.1 BFCL：数据与真实输出基础

- Berkeley Function Calling Leaderboard (BFCL) 当前公开榜单：<https://gorilla.cs.berkeley.edu/leaderboard>
- 官方代码：<https://github.com/ShishirPatil/gorilla>
- 官方结果归档：<https://github.com/HuanzhiMao/BFCL-Result>

当前榜单声明模型使用 `f7cf735` 评测，并公开原始模型 response。因此**第一枪可以零 GPU 完成**。

我们 pin：

```text
BFCL data/eval commit:
f7cf7359b7ac615a0b294831c5ba2bc95ee4a000

BFCL result archive commit:
6830ed13035c0cfee9aa7a9a0ffed70f10b3dd50
(snapshot 2025-12-16)
```

`simple_python` 有 400 条样本，并且每条只提供一个函数。这个性质很重要：它让 G0 可以先消除“工具选错”这一大类混淆。

## 3.2 《Butterfly Effects in Toolchains》：generic parameter failure 已经有人做

EMNLP Findings 2025：
<https://aclanthology.org/2025.findings-emnlp.907/>

它已经：

- 建立参数失败 taxonomy；
- 研究不同输入来源和 15 类输入扰动与 parameter failure 的关系；
- 给出工具链可靠性改进建议。

因此我们**不能**把论文讲成：

> “LLM tool-agent 的 parameter filling 为什么会失败？”

这已经太接近已有工作。

我们的窄而完整的 decisive contrast 必须是：

> **正确值可用且 schema 正确时，错误是 role semantics / role–value association / serialization 中哪一步？**

## 3.3 《Tool Calling is Linearly Readable and Steerable》：tool identity 已经做，argument 恰好留下问题

2026：<https://arxiv.org/abs/2605.07990>

已有结果：

- tool identity 在多模型中线性可读、可 steering；
- tool name 一旦改变，后续 argument schema 会通过 autoregression 跟着适配；
- 但同一 tool 下把 argument value 从 Tokyo steering 到 Paris 的实验是 `0/30`；
- 作者明确指出 argument values 是根据 query 动态获得的；
- 他们的评测主要验证 tool identity / JSON schema，而不是 argument value 是否实际正确。

因此我们不能重复：

> “内部能不能读出模型要用哪个 tool？”

反而应该把它作为局部机制前提：**tool identity 与 argument content 的内部组织并不相同。**

## 3.4 《Cell-Based Representation of Relational Binding》：binding 可因果研究，但不是自然结构化错误

ACL 2026 Main：
<https://aclanthology.org/2026.acl-long.2194/>

它已经：

- 在受控多句关系任务中研究 entity–relation–attribute binding；
- 用 Partial Least Squares 找低维 binding subspace；
- 跨 domain、跨两个 model family；
- activation patching 能系统性改变 relational prediction。

因此我们不能 claim：

> “首次证明 LLM 中存在低维 role/relation binding representation。”

但它提供了重要的**技术可行性先例**：binding 不是只能靠 probe 猜，可以有选择性的 causal intervention。

我们的新对象是：

> **公开真实结构化生成 benchmark 上的自然错误，以及错误在计算流水线的哪一步产生。**

## 3.5 Structured-output benchmarks：行为问题存在，但内部阶段诊断仍开放

相关近邻：

- JSONSchemaBench: <https://arxiv.org/abs/2501.10868>
- CONSTRUCT: <https://arxiv.org/abs/2603.18014>
- ExtractBench (ContextualAI): <https://arxiv.org/abs/2602.12247>
- ExtractBench (LlamaIndex, 2026-07): <https://arxiv.org/abs/2607.29677>

这些工作说明结构化输出的 schema compliance、field correctness、完整性和错误检测是现实问题；其中 ExtractBench 也明确包含 values attached to wrong record 一类错误。

但截至本次检索，没有发现一篇已经完成下面整条链：

```text
natural role-value swap failure
-> extraction vs role semantics vs binding vs serialization
-> internal causal localization
-> mechanism-specific repair
```

因此当前判定是：`COLLISION_YELLOW-GREEN`，可以做零成本 G0，但**尚未进入 ACTIVE**。

---

# 4. 为什么第一阶段选 BFCL simple_python

不是因为 BFCL 最流行，而是因为它对我们的因果问题有三个特殊优势。

## 4.1 一个样本只有一个工具

因此在第一阶段：

```text
wrong tool selection
```

这个 competing explanation 被设计上移除。

如果从多工具 BFCL 开始，一条 parameter error 可能只是模型先选错 tool；后面所有 binding 解释都会污染。

## 4.2 Ground truth 是结构化、字段级、带 acceptable values 的

BFCL 的答案形式类似：

```json
{
  "origin": ["New York City"],
  "destination": ["Washington D.C."]
}
```

因此我们不需要 LLM-as-a-judge，也不需要人工给“这个值是否正确”打标签。

## 4.3 官方模型输出已经公开

当前 BFCL 榜单公开了原始 response。第一阶段直接读取官方轨迹，比自己先跑模型更合理：

```text
已有公开轨迹
-> 自动筛错误
-> 如果题不存在，0 GPU kill
```

只有现象通���="24�

应改变：

- target role 接收到哪个 filler；
- 或修复 strict natural binding error。

必须保持：

- tool/function name；
- schema key set；
- filler value set `{Tokyo, Osaka}`；
- 与目标 pair 无关的其他参数；
- 输出合法性。

也就是说，不能只是让模型“更倾向 Tokyo”，而必须改变：

> **Tokyo 属于谁。**

## 12.3 Negative controls

至少包括：

- 同范数 orthogonal subspace patch；
- unrelated example activation；
- 相同 filler identity、相同 role 的 sham patch；
- patch 后 value identity / tool identity 的独立检查。

如果干预总是把所有 slot 往某个值推，只说明找到 value steering，不是 binding。

---

# 13. 机制结论的判定表

| 结果 | 结论 | 论文方向 |
|---|---|---|
| filler 在早期就错误/丢失 | H1 extraction | 不强称 binding；转 grounded value extraction 或直接降级 |
| filler 正确，role representation 错 | H2 role semantics | schema-role representation / schema design |
| filler、role 单独正确，但 association 错且可选择性 patch | H3 binding | 核心机制论文最强情况 |
| pre-output association 正确，生成时才错 | H4 serialization | structured decoding / two-stage assignment |
| probe 有信号但 patch 不选择性 | 相关性，不足机制 | STOP causal claim，不用 SAE 续命 |
| 不同 function 完全不同、无共享规律 | API-specific | 不够 Main-scale，STOP/general claim |

---

# 14. 方法口：由机制结果决定，不提前硬塞

## 若 H1：value extraction

方法候选：

- input-span grounded argument extraction；
- copy-aware value objective；
- 先定位 source span，再生成结构化 value。

## 若 H2：role semantics

方法候选：

- schema-role contrastive objective；
- 对易混 role pairs 做 description-level hard negatives；
- schema description rewriting / role-disambiguation training。

## 若 H3：binding

方法候选：

### Binding-consistency objective

训练数据原本就有：

```text
(role, correct filler)
```

无需新人工标注，直接把同一调用内的 swapped pairing 当 hard negative：

```text
(origin, Tokyo)      positive
(origin, Osaka)      negative
(destination, Osaka) positive
(destination, Tokyo) negative
```

训练目标不是增加 generic tool-call tokens，而是显式拉开：

```text
score(correct binding) > score(permuted binding)
```

## 若 H4：serialization

方法候选：

### Two-stage binding-preserving decoding

第一阶段形成语义 assignment table：

```text
origin -> Tokyo
destination -> Osaka
```

第二阶段只负责把已冻结 assignment 序列化成 JSON/tool-call protocol。

这样可以避免前一个字段的自回归 token 对后一个字段的 association 造成污染。

---

# 15. 方法评测设计

方法不能只看总体 BFCL accuracy。

必须分别报告：

1. strict natural binding error rate；
2. non-binding parameter error rate；
3. overall BFCL simple accuracy；
4. schema validity；
5. wrong-tool rate；
6. 对非目标错误类型是否有副作用。

一个方法若只是通过变得保守、少调用工具来降低 binding error，不算成功。

---

# 16. Generalization：什么时候才能把题目叫“structured generation binding”

如果只在 BFCL tool calling 成立，论文只能保守叫：

> role–value binding failures in function calling

要升级成：

> structured generation binding

至少需要一个非 tool-calling 外部任务。

优先考虑现成：

- ExtractBench: schema-guided document extraction；
- CONSTRUCT benchmark 中的 structured-output fields。

理由：它们同样有 schema + ground-truth values，并存在 wrong-field / wrong-record errors；但任务输入从短 user query 变成文档抽取，可以检验机制是否真跨任务。

**这一阶段绝不在 G0 前做。**

---

# 17. 模型策略

## Discovery

优先：Qwen3-4B-Instruct-2507。

原因不是“Qwen 好”，而是：

- 公开；
- 4B 足够便宜；
- tool-call template 清楚；
- 官方 BFCL response 可比；
- 已有 tool-identity mechanism 文献提供近邻基础。

## Confirmation

至少一个不同 family，例如 Gemma 3。

要求复制的是**计算层结论**：

> failure 出现在 extraction / role / binding / serialization 哪个阶段。

不要求具体 layer/head 编号相同。

如果只有 Qwen 成立，则结论必须降级成 model-family-specific，不能硬写通用机制。

---

# 18. 计算成本控制

按最坏情况从便宜到贵：

### Stage 0：文献 + corpus eligibility

- CPU；
- 400 条 `simple_python`；
- 几秒到几分钟。

### Stage 1：官方结果自然错误审计

- 0 GPU；
- 下载公开 JSONL；
- CPU 分类。

### Stage 2：本地 deterministic replication

- 只跑 eligible IDs；
- Qwen 4B；
- 单卡即可。

### Stage 3：hidden-state readout

- 只有 GREEN 后进行；
- 保存必要 token positions，不默认把全层×全 token 激活全部落盘。

### Stage 4：patching

- 只在已选 layer/site 与 matched pairs 上进行；
- 不做无目的的 layer×head×SAE grid search。

### Stage 5：method training

- 只有机制被因果确认后才进行。

这保证最可能失败的门槛发生在最便宜阶段。

---

# 19. 预注册的禁止续命规则

以下情况直接停止当前 mother route：

1. public natural binding errors 太少；
2. 只有单一 API/schema 有错误；
3. error 主要是 value extraction，而不是 association；
4. probe 只能同 schema 有效；
5. activation intervention 无法选择性改变 binding；
6. 所谓 binding vector 实际是 generic value / compliance / tool direction；
7. 必须大量生成新合成数据才能得到行为现象；
8. 必须靠 SAE 才“找到”一个 construct，而 behavior/paired causal analysis 不支持。

不得把失败题改写成：

> “某个 origin/destination circuit”

来续命。

---

# 20. 当前仓库代码与阶段对应

| 文件 | 用途 |
|---|---|
| `bfcl.py` | pinned BFCL 数据、schema 转换、JSONL IO |
| `fetch.py` | 下载 pinned BFCL category + answers |
| `scan.py` | 输出预先冻结的 binding-eligible examples |
| `official.py` | 下载 pinned BFCL 官方模型输出，转成统一格式 |
| `infer_hf.py` | 本地 deterministic HF tool-call 推理 |
| `classify.py` | 解析输出、错误 taxonomy、strict natural binding detector、Wilson CI |
| `counterfactual.py` | 通过已存在 literal swap 构造后续 matched causal pair |
| `tests/test_classifier.py` | 关键定义单元测试 |

机制阶段的 hidden-state/patching 代码**刻意没有现在假装完成**。原因：在 G0 未通过前写大量 model-specific hook 代码，会违反本项目最重要的 executable-first 原则。G0 一旦 GREEN，再针对实际发生错误的 checkpoint 与 output protocol 实现最小机制 harness。

---

# 21. 第一轮执行顺序

```text
0. pytest
1. binding-fetch(simple_python)
2. binding-scan -> eligible set
3. binding-official(Qwen3-4B)
4. binding-classify(Qwen3-4B)
5. binding-official(Gemma3-4B)
6. binding-classify(Gemma3-4B)
7. 按预注册 gate 判 GREEN / YELLOW / RED
8. 只有 GREEN -> 本地 Qwen 重跑 eligible IDs
9. reproduction 对齐 -> 实现 mechanism harness
```

第一轮的成功标准不是“得到一个好看的论文结果”，而是：

> **用最低成本知道这条题有没有资格进入真正的可解释性研究。**
