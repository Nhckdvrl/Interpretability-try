# Finding Rules — 唯一权威选题协议

版本：2026-09-01 v2.1  
状态：`AUTHORITATIVE DISCOVERY PROTOCOL`

本文件是**唯一选题协议**。旧 gate / funnel / addendum 只保留历史证据，不再并列定义规则。

目标：寻找 ACL / EMNLP / NAACL 风格、自然、清楚、真正有正常论文幅度的 LLM mechanistic interpretability 题目。允许最后为 0；绝不因为已经投入时间或算力而保题。

---

## 0. 2026-09-01 v2.1 修正：不要把“严格”误写成“复杂”

031 之后我们正确提高了 paper-scale / novelty / substrate 门槛，但后续搜索暴露了另一个问题：**过度要求候选在 GPU 前就拥有完整的三机制理论、精确 interaction statistic、复杂 cross-task architecture，会系统性把题目推向越来越难解释的抽象问题。**

这与强 ACL/EMNLP 论文和高质量 model-biology / top-down interpretability 的实际形状并不一致。

强题可以来自三种形状：

1. 一个成熟 scientific debate，MI 用来裁决；
2. 一个强 mother 留下的真实、独立 scientific axis；
3. **一个极自然、稳定、令人意外的模型现象/内部 object，本身就值得命名，然后用 MI 去理解它。**

第三种形状同样合法。ACL 2025 Outstanding `Llama See, Llama Do` 就是典型：先有一个简单、广泛、可复现的 contextual entrainment phenomenon，后面才长出 heads / causal mechanism / mitigation。

因此 v2.1 的原则是：

> **保持 novelty 严格，保持数据真实，保持问题自然；降低对“预先理论复杂度”的强迫。**

新的默认顺序：

```text
一句普通人能懂的 natural question / phenomenon
→ benchmark-removal + natural-object + normal-scope
→ strongest-neighbor N0/N1/N2
→ exact accessible substrate / established behavior
→ 选择合适路线 A / B / C
→ 写最小但可证伪的 causal contract
→ PASS-REGISTER
→ GPU
```

仍然禁止：

```text
看到 benchmark failure
→ 找一个 layer/head/SAE
→ 跑一点
→ 根据结果重新定义 paper question
```

---

## 1. PAPER-SCALE GATE：题目本身必须像一篇正常顶会论文

任何 serious candidate 先回答下面 8 个问题。

### P1 — Benchmark-removal test

删掉 dataset / benchmark / mother 名字后，scientific question 是否仍完整、自然、有意义？

- `某 benchmark broken-list failure 在哪层发生？` → **FAIL**。
- `工具参数结构匹配但语义无关时，为什么模型仍调用工具？` → **PASS**。
- `模型被要求随便选择时，为什么输出存在稳定偏好？` → **PASS**；这是 dataset 之前就成立的行为问题。

如果删除 benchmark 后只剩“这个 failure 内部是什么”“哪层坏了”“行为相似是否机制相似”，默认 KILL。

### P2 — Natural-object test

核心 object 必须在 benchmark 之外有独立意义：实体、颜色、数量、记忆、歧义、参考、相关性、社会信号、事件、工具相关性、上下文使用、语言结构、推理过程等。

**synthetic dataset 可以用，但 synthetic label 不能创造 scientific object。**

一个强的 sanity test：

> 能否不用 `LLM / benchmark / mechanistic interpretability / activation / SAE` 这些词，把问题讲给另一个研究方向的人听懂？

如果不能，优先怀疑题目本身过度技术化。

### P3 — Normal-scope test

一句话问题应能支撑完整论文，而不是单个 ablation。

但 **不再要求每个题在注册前都天然产生 2–4 个成熟 competing mechanisms。**

正常论文幅度可以来自：

- 一个广泛、稳定、值得命名的新 phenomenon；
- 一个干净的新 semantic/cognitive axis；
- 一个经典理论争论；
- 一个跨实例/模型稳定的内部 object，且有因果作用与有意义的 controls。

仍然 FAIL 的贡献形状：

- “我们找到 layer 17 的一个 head”；
- “我们解释 mother 的一张 table”；
- “我们验证 mother future work 的一句 mechanism 猜想”；
- “我们证明 benchmark proxy 不完全等于 construct”。

### P4 — Novelty-step test

与 strongest neighbor 的差别必须是**概念级 scientific delta**，不能只是：

- 换 dataset / model / language / prompt；
- behavior → mechanism，除此之外没有新 object；
- token → sentence；
- probe → SAE / patching；
- future-work completion；
- mother 已经提出 A-vs-B，我们只定位 A/B 的 head。

但注意：**一个简单的新 object / axis 可以是足够的 concept-level delta。** 不需要为了显得新而强行把问题改写成复杂 architecture。

### P5 — Story-invariance test

实验前至少写 2–3 个可能结果。无论结果如何，headline scientific object 必须保持不变。

合法：

```text
问题：模型是否有独立的 X 表示？
A：有且因果使用
B：可读但不因果使用
C：连稳定表示都没有
```

三种结果仍然回答同一个问题。

非法：

```text
原题：spontaneous deception
失败后：cross-query construct validity
再失败：within-run graph-state corruption
```

### P6 — Dataset-is-a-window test

数据可以 synthetic/control，但必须满足：

1. 问题在 dataset 之前独立成立；
2. manipulation 隔离的是自然变量；
3. central label 不是为论文临时发明；
4. 最好能走向 naturalistic validation；
5. paper story 不依赖 toy-world 特殊规则。

### P7 — Branch-concreteness test

研究中允许探索，但分支必须围绕同一 object。

不允许：看到 null 后不断换 token position / subset / prompt / probe，直到找到可讲的故事。

允许：对一个已冻结 object 先用简单 probe/steering 找 foothold，再根据结果选择更精确的 causal tool，前提是 headline question 不变。

### P8 — Venue-scale comparator

注册前仍需与至少 **3 篇强 ACL/EMNLP/NAACL Main / Outstanding/Best 邻近论文**比较题目幅度。

比较的是：

- question 是否同样自然清楚；
- contribution 是否有一个可一句话复述的 central object；
- novelty 是新 object/axis，还是已有 story 的机制细节；
- dataset 是否只是 measurement window；
- 是否有足够 evidence package 支撑 Main-paper 规模。

**不要误解为候选必须比这些论文理论更复杂。** 很多强论文的问题反而非常简单。

---

## 2. 顶会尺度校准：真正要模仿的是问题形状

### ACL 2025 Outstanding — `Llama See, Llama Do`

广泛新现象：context 中出现过的 token 会被系统性增权，即使 token 是随机的。随后才命名 contextual entrainment、找 causal heads、做 mitigation。

标尺：**simple surprising phenomenon → broad evidence → mechanism → consequence.**

https://aclanthology.org/2025.acl-long.791/

### EMNLP 2025 Outstanding — shared filler-gap structure

成熟理论问题：不同 filler-gap constructions 是否共享抽象机制；causal intervention 裁决。

标尺：**external theory → causal LM evidence.**

https://aclanthology.org/2025.emnlp-main.1271/

### NAACL 2025 — property inference taxonomy vs similarity

经典认知争论，dataset 只是窗口，A/B/C 都保持标题不变。

标尺：**一个简单理论轴足以撑 paper，不需要三层 architecture。**

https://aclanthology.org/2025.naacl-long.574/

### NAACL 2025 — `Racing Thoughts`

先提出一个能解释一类 contextualization errors 的统一 hypothesis，再做 correlational + causal validation。

标尺：**一个强 hypothesis 可以胜过复杂 taxonomy。**

https://aclanthology.org/2025.naacl-long.155/

### ACL 2026 Main — `Do LLMs Know Tool Irrelevance?`

核心问题极简单：tool 的语义相关性与参数结构匹配冲突时，模型到底听谁的？controlled dataset 只是隔离两者。

标尺：**现实变量先存在，controlled data 用来解耦。**

https://aclanthology.org/2026.acl-long.1473/

---

## 3. 三种合法找题路线

### Route A — Mother omitted-axis extension

适合“已有 object O，但存在一个 mother 没问的自然轴 B”。

必须满足：

1. strong mother；
2. B 在现实/科学文献中独立存在，或是明显自然 semantic axis；
3. natural cross-cells / counterexamples 存在；
4. mother 没回答 B；
5. B 不是 limitation/future-work 同义改写；
6. B 删掉 mother 名仍足够自然；
7. measurement recipe 大部分可继承。

最理想形状不是“补一格 2×2”，而是：

> mother 研究 X；我们发现 X 与一个被混淆但不同的自然属性 Y 可以被干净分离，且 Y 有自己的 representation/causal role。

### Route B — Established anomaly + independent mechanism debate

适合成熟理论争论。

要求：

1. exact behavior 已在现代 open models / prior work 中存在；
2. 至少两个真正 competing computations；
3. competing mechanisms 来自科学理论，而不是 early/middle/late layer；
4. 不提 benchmark 仍值得研究；
5. 不同机制给出不同 intervention/generalization prediction。

**Route B 仍然需要较强预注册。** 因为它最容易退化成 mother behavior → mechanism。

### Route C — Simple phenomenon / simple latent object first（v2.1 新增）

适合 model biology / top-down interpretability，也是今后 fresh search 的高优先级路线。

形状：

> 一个人人能懂、稳定而意外的行为或语义属性  
> → 做干净 matched controls，证明不是最明显 confound  
> → 问模型内部是否存在可泛化、可干预、行为相关的 representation/pathway  
> → 再决定最合适的 MI 工具。

Route C **不要求注册前已经有 2–3 个成熟 cognitive mechanisms**。

但必须满足：

1. phenomenon/object 本身简单自然，一句话可懂；
2. broad enough：跨多个实例/域/setting，而不是一个 prompt trick；
3. strongest neighbor 没有已经拥有这个 object；
4. central confound 能在设计上解耦；
5. 至少一个 modern analyzable open model 有公开或强 prior evidence；最好 ≥2 families，但不再机械要求所有题在注册前都有两家完全同型 published artifact；
6. 有一个明确的 causal-use question，例如：`这个 representation 只是可读，还是模型实际用它决定行为？`；
7. 至少一个 nontrivial control / falsifier 能区分“真 object”与 superficial correlate；
8. 不能只有“找 SAE feature”这一项贡献。

Route C 的 paper 可以在实验中发现 mechanism structure，**只要 object/question 不随结果变化。**

---

## 4. 注册前 PAPER CARD

```yaml
paper_scale:
  one_sentence_question:
  question_without_llm_or_method_jargon:
  independent_scientific_or_model_object:
  why_a_non_benchmark_reader_should_care:
  three_strong_venue_comparators: []

route: A | B | C

mother_or_behavioral_anchor:
  paper_or_source:
  established_result:
  statistical_unit:
  measurement_recipe:

novelty:
  exact_conceptual_delta:
  strongest_neighbors: []
  why_not_just_mechanizing_mother:
  main_confounds_to_separate: []

substrate:
  natural_or_synthetic:
  central_gold_source:
  row_level_artifact:
  analyzable_open_checkpoint:
  modern_open_family_evidence:
  why_dataset_is_only_a_measurement_window:

causal_contract:
  central_causal_question:
  simplest_discriminating_test:
  negative_control_or_falsifier:
  route_B_hypotheses_optional_for_A_C: []

story_invariance:
  result_A_story:
  result_B_story:
  result_C_story:
  same_headline_object_under_all_results: true|false

existence:
  phenomenon_or_axis_already_established: true|false
  requires_gpu_to_discover_whether_question_exists: true|false

verdict: CONTINUE-PAPER-SCALE | PASS-REGISTER | KILL-SCALE | KILL-NOVELTY | KILL-DATA | KILL-BEHAVIOR
```

硬规则：

- headline object 不能随结果变化；
- GPU 不能用来发现“这个现象到底存不存在”然后再决定论文问题；
- strongest-neighbor collision 仍然致命；
- central measurement/gold 必须可审计；
- **不再因为候选暂时只有一个强 causal question、而没有三套 mechanism theory，就自动拒绝。**

---

## 5. 数据与 S0

### Route A S0

- 两轴定义独立于模型；
- central gold 不由我们/LLM judge 临时创造；
- row-level artifact 可得；
- natural cross-cells 可计数；
- mother recipe 可合法延伸。

### Route B S0

- exact theory-diagnostic behavior 已存在；
- open checkpoint 可分析；
- raw outputs / scorer 可审计；
- effect 非 floor/ceiling；
- family/generalization evidence 足够支撑理论裁决。

### Route C S0

Route C 允许更接近实际 model-biology workflow，但仍不允许 behavior lottery。

注册前至少需要：

- phenomenon 已由 prior work / released outputs /多设置公开证据建立；或是一个 deterministic semantic axis，不依赖先跑 GPU 才知道有没有；
- analyzable open checkpoint；
- matched controls 能去掉最明显 confound；
- object 有跨 item/domain 的 generality path；
- cheap reproduction 可以在注册后作为 execution gate，但不能据此重写 question。

**“≥2 modern families”从 universal hard law 改为 strong preference。**

以下情况仍必须 ≥2 families：

- claim 本身是“LLMs generally do X”；
- behavior 很容易是 model-specific artifact；
- family difference 会直接改变 scientific interpretation。

如果 paper 明确是“we discover and characterize X in model family M, then test transfer/generalization”，单 family 可以进入 register，但必须把 scope 写清楚并预设第二-family replication 为 paper-strengthening step，而不是用它决定题目是否存在。

---

## 6. Novelty 审计：N0 / N1 / N2 仍然保留

### N0 — object ownership

strongest neighbor 是否一句话已经研究同一个 object / axis？是 → KILL。

### N1 — causal occupancy

是否已有工作做了决定性的同一 factorization / intervention？是 → KILL 或必须证明新的 object-level delta。

### N2 — delta-width audit

问：

> 我们新增的是一个新 scientific/model object，还是只是把已有 phenomenon 解释得更细？

通常不够：

- behavior paper → mechanism paper，且无新 object；
- mother 已提出 A/B，我们只找 heads；
- future-work completion；
- benchmark proxy audit；
- 只换更强 MI method。

但以下可以足够：

- 一个此前未被分离的、自然且 orthogonal 的 semantic axis；
- 一个 broad new behavioral phenomenon；
- 一个跨域稳定、可因果操控的新 latent object；
- 一个简单但重要的新 factorization，且 strongest prior 没问。

**不要为了 N2 而故意把题目写复杂。Novelty 的单位是“新 object / 新 axis / 新 phenomenon”，不是标题里的抽象名词数量。**

---

## 7. 死亡模式

F1 — Behavior lottery / synthetic-first  
F2 — Mother / neighbor ownership  
F3 — Substrate mirage  
F4 — Measurement / denominator invalid  
F5 — Claim scope 超过 family evidence  
F6 — Post-hoc rescue / scope drift  
F7 — Mechanistically empty: only probe/SAE without causal/use story  
F8 — Topic-scale / benchmark-dependence failure  
F9 — **Over-engineered question**: 为满足形式 gate 强行把一个简单现象包装成多阶段、多模块、多理论 architecture，导致问题不再自然

F9 不是“题太难所以不做”，而是提醒：

> 如果一句简单问题可以撑 paper，就不要为了显得学术而把它改造成三个 latent states + 两个 arbitration stages + 一个 cross-task architecture。

---

## 8. 031 postmortem：仍然是 F8 / scope-drift canonical negative example

031 从 `spontaneous deception` → `cross-query latent belief` → `within-run graph-state corruption`。

问题不是 causal tool 选错，而是：

1. 原题依赖 benchmark construct；
2. negative result 后 headline object 连续变化；
3. 可以设计实验被误当成有正常 paper question；
4. toy substrate 不能自动制造 broad narrative。

v2.1 **不会**撤销这条教训。放松的是理论复杂度，不是允许 post-hoc rescue。

---

## 9. Active / registration discipline（v2.1）

`PASS-REGISTER` 的 universal core：

```text
PAPER-SCALE natural question / phenomenon
+ benchmark-removal PASS
+ independent object / axis / broad phenomenon
+ >=3 venue-scale comparators
+ N0 clear
+ N1 not fatally occupied
+ N2 concept-level delta
+ exact accessible substrate / central gold
+ analyzable open checkpoint
+ established behavior OR legitimate omitted axis/object
+ story-invariant headline
+ minimal causal-use contract
+ explicit confound controls / kill conditions
= PASS-REGISTER / GPU AUTHORIZED
```

Route B 额外要求：

```text
>=2 theory-level competing mechanisms
+ theory-diagnostic S0
+ discriminating intervention predictions
```

Route C **不额外要求**三机制理论，也不要求在注册前冻结一个复杂的数学 interaction statistic。

注册时只需冻结：

1. central object/question；
2. decisive behavioral/representation measurement；
3. simplest causal-use test；
4. strongest confound controls；
5. hard kill / scope limit。

之后可以让 experiment 揭示机制结构，但不能让 experiment 重新发明 headline。

---

## 10. 搜题偏好：simplicity prior

Fresh search 默认优先顺序：

1. **简单 semantic distinction**：两个普通人自然会区分、但 prior 可能混在一起的属性；
2. **简单 everyday anomaly**：模型一个稳定、意外、跨 prompt/domain 的偏好或失误；
3. **简单 generalization question**：模型学到的是表面相关，还是一个更一般的概念；
4. **成熟 scientific debate**：已有清楚 competing theories；
5. 最后才考虑需要很长理论铺垫的 architecture question。

生成 candidate 时先强制写：

> `用和 AI/可解释性完全无关的语言，这个问题是什么？`

如果一句话不顺，先简化或砍掉，不要继续加术语。

---

## 11. 当前 one-line discipline

> **先找一个简单、自然、值得知道的新 object / axis / phenomenon；再用最简单的实验把它隔离干净，最后才决定需要哪种 MI。严格不等于复杂。**
