# Finding Rules — 唯一权威选题协议

版本：2026-08-31 v2  
状态：`AUTHORITATIVE DISCOVERY PROTOCOL`

本文件是**唯一选题协议**。旧 gate / funnel / addendum 只保留历史证据，不再并列定义规则。

目标：寻找 ACL / EMNLP / NAACL 风格、真正有正常论文幅度的 LLM mechanistic interpretability 题目。允许最后为 0；绝不因为已经投入时间或算力而保题。

---

## 0. 2026-08-31 最重要的新修正：先过 PAPER-SCALE，再谈 mother / dataset / MI

031 的失败证明旧协议仍然不够严格：它能防止“现象根本不存在”，却没有充分防止**问题本身只是某个 benchmark / mother paper 内部的一条解释缝**。

031 从 `spontaneous deception` 一路缩成 `cross-query latent belief`，再缩成 `within-run graph-state corruption`。每一步单独看都能设计实验，但 headline scientific question 已经改变。这不是健康的实验分岔，而是原题死亡后的叙事救援。

以后候选生成顺序改为：

```text
PAPER-SCALE natural question
→ strong mother / established object
→ exact novelty delta
→ natural/legitimate substrate
→ existing behavior or omitted axis
→ strongest-neighbor attack
→ S0 / measurement
→ registration
→ causal MI
```

**没有先过 PAPER-SCALE，不允许因为 mother 很强、数据公开、现象很大就注册。**

---

## 1. PAPER-SCALE GATE：题目本身必须像一篇正常顶会论文

任何 candidate 在查数据和写机制实验前，先回答下面 8 个问题。

### P1 — Benchmark-removal test

把 dataset / benchmark / mother paper 名字从标题和一句话问题里删掉，scientific question 是否仍然完整、自然、有意义？

- `LLM 在 CSQ broken-list 上的 deceptive event 内部是什么？` → **FAIL**，问题靠 benchmark construct 才成立。
- `模型在工具参数结构匹配但语义无关时，为什么仍调用工具？` → **PASS**，dataset 只是隔离真实因素的测量工具。
- `property inheritance 依赖 taxonomy 还是 similarity？` → **PASS**，这是数据集之外已有的认知科学问题。

如果删除 benchmark 名后只剩：

- “行为相似是否机制相似？”
- “某 failure 到底在哪层？”
- “某 mother metric 内部是什么？”

通常说明题目过泛或过窄，默认 KILL。

### P2 — Natural-object test

核心 object 必须在 benchmark 之外就有独立意义：认知现象、推理过程、语言结构、训练动态、agent decision、context use、memory、uncertainty、social/world representation 等。

**synthetic dataset 可以用，但 synthetic label 不能创造 scientific object。**

### P3 — Normal-scope test

一句话问题应当能支撑一篇完整论文，而不是一个 ablation：

- 能自然产生 2–4 个理论上不同、都值得解释的机制；
- 能跨多个实例/设置/模型验证；
- 结果会改变我们对一个广泛能力/失败/表示的理解。

如果贡献最终最自然地表述成：

- “我们找到某 layer/head/subspace”；
- “我们解释了 mother 的一个 table”；
- “我们验证了 mother future work 的一个猜想”；
- “我们发现 benchmark label/proxy 不严谨”；

则默认不是当前目标幅度。

### P4 — Novelty-step test

与 strongest neighbor 的差别必须是**概念级 scientific question 的差别**，不是：

- 换 dataset / model / language / prompt；
- 从 behavior 改成 mechanism；
- 从 token 改 sentence；
- 从 generic head 改 semantic head；
- 从一个 mother 现象追问“具体怎么实现”；
- 把 mother limitation/future-work 原句直接变成题目。

`mother behavior -> mechanism` 不是自动非法，但要证明新 mechanism question 本身有独立理论对象，而非 generic localization。

### P5 — Story-invariance test

在跑实验前写出至少 2–3 个可能结果。**无论哪一个结果发生，论文标题里的 scientific question 必须保持不变。**

合法分岔：

```text
同一问题：property inheritance 由 taxonomy 还是 similarity 驱动？
结果 A：taxonomy
结果 B：similarity
结果 C：两者交互
```

非法分岔：

```text
原题：spontaneous deception
失败后：cross-query construct validity
再失败：within-run graph-state corruption
```

如果 negative result 迫使更换 headline object，原题已死，必须重新从 PAPER-SCALE 开始，不能叫“强 null 仍是同一论文”。

### P6 — Dataset-is-a-window test

优先自然/真实数据。若使用 synthetic/control dataset，必须满足：

1. scientific question 在 dataset 之前已独立成立；
2. synthetic design 只是为了 causal identification；
3. 中央变量不是我们为了题目临时发明；
4. 最好存在 naturalistic / external validation 路线；
5. 论文叙事不能靠 toy world 的特殊规则才成立。

**数据可以不自然，但问题必须自然；越 synthetic，越需要更强的外部 scientific grounding。**

### P7 — Branch concreteness test

研究过程中允许出现很多分岔，但每个分岔必须：

- 回答同一个 headline question；
- 有预先可写出的 causal prediction；
- 不是看到 null 后换 token position / probe / subset / prompt 继续搜；
- 不是把 scope 从 behavior → construct → representation 一路缩窄。

### P8 — Venue-scale comparator

注册前必须拿 candidate 和至少 **3 篇强 ACL/EMNLP/NAACL Main / Outstanding/Best 邻近论文**比较叙事幅度，而不仅仅做“有没有同标题”的 novelty search。

重点比较：

- scientific object 是否同样自然；
- dataset 是 object 还是 measurement window；
- prior-work delta 是概念差还是机制细节；
- contribution 是否包含 broad behavior + causal explanation + cross-setting evidence；
- 是否能在不提具体 benchmark 的情况下解释“为什么这值得知道”。

---

## 2. 顶会尺度校准：我们真正要模仿什么

以下不是固定 mother 列表，而是**题目幅度标尺**。

### ACL 2025 Outstanding — `Llama See, Llama Do`

它不是先挑一个 benchmark failure 再找 head，而是先发现一个跨模型、跨 prompt setting 的广泛现象：**context 中出现过的 token 会被系统性增权，即使是随机 token**。随后才提出 contextual entrainment、找 causal entrainment heads、做 ablation/mitigation。

标尺：**广泛新现象本身就值得命名；机制解释服务于现象。**

https://aclanthology.org/2025.acl-long.791/

### EMNLP 2025 Outstanding — `Causal Interventions Reveal Shared Structure Across English Filler–Gap Constructions`

问题来自成熟语言学理论：不同 filler-gap construction 是否共享抽象机制。dataset/句子只是测量窗口，causal intervention 用来裁决一个本来就存在的理论问题。

标尺：**强外部科学理论 → LMs 提供新的因果证据。**

https://aclanthology.org/2025.emnlp-main.1271/

### NAACL 2025 — `Characterizing the Role of Similarity in the Property Inferences of Language Models`

核心是经典认知争论：property inheritance 到底由 taxonomic structure 还是 similarity 驱动。behavior + causal representation analysis 都围绕同一问题；不管结果偏哪一边，题目不变。

标尺：**竞争机制在实验前就由科学理论给出，而不是由层位置/patch 结果事后生成。**

https://aclanthology.org/2025.naacl-long.574/

### NAACL 2025 — `Racing Thoughts`

它提出对 contextualization errors 的统一 race-condition hypothesis，再用多种 MI 方法给 correlational + causal evidence，并给 intervention。

标尺：**先有能解释一类 failure 的统一 hypothesis，再做机制验证；不是逐 benchmark 修补。**

https://aclanthology.org/2025.naacl-long.155/

### ACL 2026 Main — `Do LLMs Know Tool Irrelevance?`

现实 object 是 tool semantic relevance 与 parameter structural match 的冲突。作者设计 SABEval 是为了**解耦两个现实中本就独立的因素**，然后找到 semantic checking 与 structural matching 两条 competing pathways，并做 rebalancing mitigation。

标尺：**controlled dataset 可以很人工，但它解耦的是天然变量；paper question 不依赖 SABEval 这个名字。**

https://aclanthology.org/2026.acl-long.1473/

---

## 3. 两种合法找题路线仍保留，但必须在 PAPER-SCALE 之后

### Route A — Mother omitted-axis extension

必须满足：

1. strong concrete mother；
2. mother 已稳定测量 object `O`；
3. 新轴 `B` 是现实中 `O` 的独立属性；
4. natural counterexamples / cross-cells 已存在；
5. mother 没回答 B；
6. 大部分 measurement recipe 可继承；
7. **B 本身达到 PAPER-SCALE，而不是一个方便补齐的矩阵格子。**

### Route B — Established anomaly → unasked causal computation

必须满足：

1. headline behavior 已在 open models / prior work 中稳定存在；
2. ordinary faithful setting，不靠特殊 prompt 才有；
3. 至少两个真正 competing causal mechanisms；
4. mechanisms 来自对现象的理论解释，不只是 early/middle/late layer 分类；
5. 不同机制预测不同 intervention / generalization；
6. **即使完全不提 mother benchmark，新 causal question 仍是一个值得研究的问题。**

Route B 最危险。以后若只是：

> `Mother discovered X; we ask which internal circuit causes X.`

默认 **KILL-SCALE**，除非能证明这个 mechanism question 本身具有独立科学对象与广泛意义。

---

## 4. 注册前必须写的 PAPER CARD

```yaml
paper_scale:
  one_sentence_question:
  question_without_dataset_names:
  independent_scientific_object:
  why_a_non_benchmark_reader_should_care:
  three_strong_venue_comparators: []
  scope_difference_from_each:

mother:
  paper:
  scientific_object:
  established_result:
  statistical_unit:
  measurement_recipe:

novelty:
  exact_conceptual_delta:
  strongest_neighbor:
  why_not_just_mechanizing_mother:
  why_not_future_work_completion:

substrate:
  natural_or_synthetic:
  why_dataset_is_only_a_measurement_window:
  central_gold_source:
  external_validity_path:

mechanism:
  hypothesis_1:
  hypothesis_2:
  hypothesis_3_optional:
  discriminating_predictions:

story_invariance:
  result_A_story:
  result_B_story:
  result_C_story:
  same_headline_question_under_all_results: true|false

existence:
  behavior_already_exists: true|false|not_applicable
  requires_expensive_G0_to_discover_question: true|false

verdict: CONTINUE | KILL_SCALE | KILL_NOVELTY | KILL_DATA | KILL_BEHAVIOR
```

硬规则：

- `same_headline_question_under_all_results = false` → KILL；
- `requires_expensive_G0_to_discover_question = true` → 默认 KILL；
- 无法写出 `why_not_just_mechanizing_mother` → KILL-SCALE；
- 无法写出 3 篇强 venue comparator → 不注册。

---

## 5. 数据与 S0：PAPER-SCALE 过了以后再做

### Route A S0

- 两轴定义独立于模型；
- central gold 不由我们/LLM 临时创造；
- row-level artifact 真正拿到；
- natural cross-cells 可程序计数；
- mother recipe 可合法延伸；
- no synthetic 2×2 manufacturing。

### Route B S0

- exact behavior 在 analyzable open checkpoints 上存在；
- 至少 2/3 genuinely different families 同一 qualitative signature，或 prior work 已给足强证据；
- raw outputs 可审计；
- capability denominator 合法；
- effect substantial；
- hard kill 预先冻结。

S0 是确认**能否测量既定问题**，不是让 experiment 帮我们决定论文究竟要讲什么。

---

## 6. Novelty 审计升级：不只看 collision，还看 DELTA WIDTH

### N0 — title/object ownership

mother / neighbor 是否一句话已回答新问题？是 → KILL。

### N1 — causal occupancy

是否已有工作做了关键 factorization / causal test？是 → KILL。

### N2 — delta-width audit（新增，注册必做）

即使 N0/N1 没撞，也要问：

> 与最强 prior work 相比，我们新增的是**一个新的 scientific question**，还是只是把已有 phenomenon 再解释得更细？

以下通常不够：

- behavior paper → mechanism paper，除此之外无新理论对象；
- mother 已提出两个功能因素，我们只定位它们的 heads；
- mother future work 明确写了我们要做的 decomposition；
- 某 benchmark proxy → 我们证明 proxy 不完全等于 construct；
- 结果仅是更精确地分类已有 failure。

---

## 7. 八类死亡模式

F1 — Behavior lottery / synthetic-first  
F2 — Mother / neighbor ownership  
F3 — Substrate mirage  
F4 — Measurement / denominator invalid  
F5 — No common phenotype across families  
F6 — Post-hoc rescue / scope drift  
F7 — Mechanistically weak  

### F8 — Topic-scale / benchmark-dependence failure（新增）

问题只有放在某 benchmark / mother construct 内才显得成立；或者 prior-work delta 只是“再做机制”“再细分一种 failure”“完成 future work”。

典型症状：

- dataset 名一删，问题变成空泛常识；
- dataset 名保留，问题又只对该 benchmark 有意义；
- negative result 后 headline 连续换 object；
- mechanism hypotheses 只是 early/middle/late localization；
- 需要把一个 Findings/mother 的讨论段扩成整篇论文才能显得新。

处理：**KILL-SCALE，禁止通过更窄叙事救活。**

031 是当前 canonical negative example。

---

## 8. 031 postmortem：以后绝不能重复

031 的执行本身遵守了停止规则，V3 在 held-out、polarity-invariant reachability measurement 上失败并及时终止；真正错误发生在**选题阶段**。

错误链：

```text
mother: hard wrong + easy correct 被解释为 spontaneous deception
→ 我们问 knowledge-action vs reasoning corruption
→ V2 whole-state patch 被 shuffled donor 解释
→ 叙事改成 cross-query construct validity
→ 用户指出该 claim 过度依赖 benchmark 且接近 elicitation 常识
→ 再改成 within-run graph-state corruption
→ V3 measurement gate AUROC ≈ 0.53，终止
```

教训不是“probe 选错了”，而是：

1. 原题没有通过 benchmark-removal test；
2. mother 的 `deception` construct 本身定义了问题；
3. negative result 迫使 headline scientific object 连续变化；
4. graph dataset 是 toy substrate，无法自动提供 broad narrative；
5. 我们把“可以设计一个 causal experiment”误当成“这是正常论文幅度的问题”。

以后看到类似路径，**在 GPU 前 KILL-SCALE。**

---

## 9. Active / registration discipline

`PASS-REGISTER` 现在意味着同时通过：

```text
PAPER-SCALE
+ strong scientific object
+ concept-level novelty delta
+ legitimate substrate
+ existing behavior / natural omitted axis
+ strongest-neighbor N0/N1
+ delta-width N2
+ story invariance
+ >=2 theoretically meaningful causal hypotheses
+ frozen fatal controls
```

**注册不是“这个实验值得试”；注册是“这个问题本身已经值得一篇论文，只差用实验回答”。**

如果只能说“先跑跑看，跑出来再决定怎么讲”，禁止注册。

---

## 10. 当前 one-line discipline

> **先找一个不依赖 benchmark 名字也值得 ACL/EMNLP/NAACL 研究的问题；再找数据和 MI 去回答它。不要从一个强 mother 留下的机制缝里反推整篇论文。**
