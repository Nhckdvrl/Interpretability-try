# Batch 3 Mother-Paper Extension Ledger — 大规模母论文扫读、延展与死亡库

日期：2026-08-29
状态：`DISCOVERY LEDGER / NOT A DISPATCH QUEUE`

本批采用新的找题纪律：**先选已经把 scientific object 做扎实的强母论文，再问它真正留下的下一问。** 母论文不是装饰性 related work；如果去掉它以后新问题几乎不变，这个 extension 就不够“mother-paper grounded”。

## Hamdi-style extension test

每条 extension 必须至少属于以下一种：

```text
A. scope boundary: X 在母论文的空间/任务/条件之外还成立吗？
B. missing axis: 母论文研究 X，但邻接且正交的 Y 是否独立存在？
C. behavior → mechanism: 母论文已证明自然行为，下一问解释内部计算。
D. representation → causal use: feature 可读，不代表模型真的使用它。
E. correlation → causal plan: predictive state 是否真正控制未来 computation。
F. mechanism semantics: 已定位的 feature/circuit 到底编码什么变量？
G. implementation switch: 母论文发现多种算法，模型如何切换/更新/失效？
H. mechanism-derived failure: 母机制预测一个原 benchmark 没覆盖的新失败。
```

禁止的“extension”：换模型、换语言、换 benchmark、换专业领域、只增加一个 readout、仅做更大规模复现。

---

## 母论文 sweep（>25 条）

下面记录本轮真实扫过/攻击过的母线。`KEEP` 表示至少长出一个进入最终十强的问题；`RESERVE` 表示仍有科学空间但不如十强；`KILL/NO-EXTENSION` 表示相邻轴已被母论文/后续文献做掉，或只能长出 incremental 题。

| # | mother / line | venue/year | 我们尝试的下一问 | 裁决 |
|---:|---|---|---|---|
| 1 | *Llama See, Llama Do* | ACL 2025 Main | reappearance 的 causal unit 是 token 还是 entity/concept？ | **KEEP → Alias Entrainment** |
| 2 | *Sentence-Level Contextual Entrainment* | arXiv 2026 | sentence→semantic identity transfer | `NEIGHBOR`; 已占 sentence reappearance，但未占 unseen alias |
| 3 | *LLM Task Interference* | EMNLP 2024 Main | task switch 的内部哪个子系统没切换？ | **KEEP** |
| 4 | *Localizing Task Recognition and Task Learning...* | ICLR 2026 | TR/TL 是否在 task switch 时异步？ | **KEEP** |
| 5 | *Internal Planning: Horizon and Branch Awareness* | ICLR 2026 | valid branch 变 invalid 后如何 retire？ | **KEEP** |
| 6 | *Fresh in memory: Training-order recency...* | ICLR 2026 | training-time metadata 是否成为 conflict priority？ | **KEEP** |
| 7 | *LLMs Process Lists With General Filter Heads* | ICLR 2026 | predicate 修订时 eager flags 如何失效并切 lazy path？ | **KEEP** |
| 8 | *Around the World in 24 Hours* | ACL 2025 Main | geography 与 temporal arithmetic 到底在哪里 join 失败？ | **KEEP** |
| 9 | *Action Boundary Blindness* | ACL 2026 Main | EBP 所谓 latent boundary perception 是已有 state 还是被 prompt 新建？ | **KEEP** |
| 10 | *Sparse Neurons Carry Strong Signals of Question Ambiguity* | EMNLP 2025 Main | AEN 编码 surface ambiguity 还是 unresolved posterior ambiguity？ | **KEEP** |
| 11 | *Knowing but Not Showing* | arXiv 2026 | contextual resolution × ambiguity behavior | `NEIGHBOR`; 行为 gap 已占，AEN dynamic semantics 未占 |
| 12 | *Pathway to Relevance: Semantic BM25* | EMNLP 2025 Main | semantic matching 后 saturation 是否也按 concept 聚合？ | **KEEP** |
| 13 | *Retrieval Heads are Dynamic* | ACL 2026 Main | hidden-state future-head predictor 是否 causal plan？ | **KEEP** |
| 14 | *Stochastic Chameleons* | ACL 2025 Main | direct-query vs context-cue arbitration | `KILL`: mother 已经给出 competing circuits/mechanistic explanation |
| 15 | *Do Language Models Track Entities Across State Changes?* | ICML 2026 | REMOVE-tag 的更多 state-update failure | `KILL AS NEW PAPER`: mother 已从机制反推 reintroduction/no-op/shared-label failure |
| 16 | *Latent Agents: Internalized Multi-Agent Debate* | ACL 2026 Main | agent subspaces 如何形成 consensus/arbitration | `RESERVE`: 科学问题好，但依赖特制 post-training model，普适性弱于十强 |
| 17 | *Narrow Finetuning Leaves Clearly Readable Traces...* | ICLR 2026 | trace 是 readout 还是 causal prior？ | `DOWNGRADE`: mother 已 steering 并做因果/overfitting 分析，简单 causal-use extension 不新 |
| 18 | *How Language Models Conflate Logical Validity with Plausibility* | ACL 2026 | validity/plausibility decoupling 的边界 | `NO-EXTENSION`: mother 已 representational conflation + steering，邻接空间偏 incremental |
| 19 | *Mechanistic Interpretability of Large-Scale Counting...* | ACL 2026 | segment boundary / aggregation circuit 泛化 | `NO-EXTENSION`: mother 已定位多阶段 System-2 circuit，下一步多为 scaling/transfer |
| 20 | *Rhetorical Questions in LLM Representations* | ACL 2026 | 多个 dataset-specific directions 是否汇聚到共同 pragmatic reader | `RESERVE`: 有趣但自然 failure / causal prediction 不如十强强 |
| 21 | *Tracing Relational Knowledge Recall in Large Language Models* | ACL 2026 | relation direction 与 entity connectivity 的可迁移机制 | `DOWNGRADE`: relation recall / binding 周边过密 |
| 22 | *Aligning What LLMs Do and Say* | ACL 2026 Findings | explanation/decision attribution gap 的内部 readout | `DOWNGRADE`: explanation faithfulness 已是成熟母区，难长出独立新问题 |
| 23 | filler-gap shared-mechanism line | EMNLP 2025 / ACL 2026 | island condition 是否 gate shared filler-gap circuit | `KILL`: 2026 *Causal Drawbridges* 已直接做 syntactic-island causal blocking |
| 24 | *Causal Drawbridges: Characterizing Gradient Blocking of Syntactic Islands...* | 2026 | island gate 的进一步 construction transfer | `NO-EXTENSION`: exact 邻接已高度占位 |
| 25 | structured-knowledge hallucination / serialization line | ACL 2026 + prior | 同一 graph 换 linearization/order 时内部 representation 是否 invariant | `KILL`: graph linearization/order sensitivity 2024–2026 已形成独立成熟线，且已有结构失真机制 |
| 26 | cell-based relational-binding line | ACL 2026 | coreference/update 后 cell merge/split | `DOWNGRADE`: mother 已做多关系、多结构与 cue conflict；新题易落 repo F2/F3 |
| 27 | cross-lingual language-agnostic concept line | ACL/ICLR 2026 | language-neutral concept 在 mixed-language composition 中是否统一 | `ROUTE`: repo MCC/F9 已系统覆盖跨语言 partition/join/update |
| 28 | instruction-vector / nonlinear circuit-selection line | ACL/ICLR 2026 | supersession/composition of simultaneous instructions | `DOWNGRADE`: task-vector composition、多轮 instruction shard 与 repo F3 邻域过密 |
| 29 | memory–context conflict / parametric-vs-context line | 2025–2026 | 冲突时哪个 memory wins | `KILL AS BROAD TOPIC`: CoRect/DUD/knowledge-conflict 机制线已拥挤 |
| 30 | *Latent Planning Emerges with Scale* | arXiv 2026 | planned concept 是否被后续环境变化撤销 | `RESERVE`: 与 Internal Planning/branch lifecycle 重叠，保留一条即可 |
| 31 | *Do I Know This Entity?* | 2024/2025 | epistemic knowledge → ontology | `REFERENCE ONLY`: 这是方法范式示例，相关 ontology extension 已被其他项目采用，不重复 |
| 32 | contextual truth / truth-falsity geometry line | ACL 2026 | conflict context 是否覆盖/共存 parametric truth state | `DOWNGRADE`: truth/conflict/knowledge-editing 邻域太拥挤 |

这一 sweep 不是穷尽 bibliography；其作用是防止只围绕一个小圈子爱上十个相似题。

---

## 原始 extension 脑暴（保留失败过程）

在上述 mother lines 上，本轮至少尝试过以下 extension family：

- contextual entrainment：alias transfer、synonym transfer、sentence→concept transfer、cross-language alias（后者 ROUTE MCC）；
- task interference：TR stale、TL stale、label-map stale、task-subspace carryover；
- internal planning：branch retirement、branch confidence decay、alternative-branch capacity、branch invalidation；
- training recency：conflict arbitration、unlearning priority、source reliability interaction、retrieval latency；
- filter heads：predicate composition（KILL，mother 已做加法/析取）、predicate correction、eager→lazy migration、flag invalidation；
- GeoTemp：timezone retrieval、offset arithmetic、retrieval→arithmetic binding、CoT route selection；
- action boundary：latent boundary probe、EBP donor patch、granularity/scope/completeness geometry、boundary state vs generic success state；
- ambiguity neurons：same-surface contextual resolution、misleading context、clarification answer injection、surface-vs-posterior ambiguity；
- semantic BM25：exact repetition saturation、synonym stuffing、alias stuffing、concept-level saturation、distinct-evidence control；
- dynamic retrieval heads：future schedule causality、donor-schedule patching、second-hop retargeting、schedule-vs-content separation；
- latent agents：consensus arbitration, perspective suppression, agent-subspace weighting（Reserve）；
- structured knowledge：serialization invariance / graph order（KILL by occupied line）；
- filler-gap：island gate（KILL by Causal Drawbridges）；
- entity state tracking：REMOVE tag generalization/reintroduction（mother 已经做得过深，KILL）；
- narrow finetuning：trace causal role（mother 已 steering/causal, DOWNGRADE）。

---

## 本轮 independent-style N0 纪律

最终十强不是“每篇母论文挑一个”。先做 extension，再以 reviewer 视角重新攻击：

1. **Exact collision**：检索 exact phenotype + mechanism terms，而不是只搜新标题。
2. **Mother appendix inclusion**：母论文若已经顺手做过下一问，extension 直接死。
3. **Successor collision**：例如 token entrainment 的 sentence-level follow-up、ambiguity AEN 的 2026 behavioral follow-up必须一起算。
4. **Repo mother-inclusion**：用 F1–F9 压缩；若只是旧 family 换 setting，ROUTE。
5. **D0 identifiability**：变量必须能独立操纵；Batch2 RIF 已证明“理论现象漂亮但 runtime state 不可识别”也必须杀。
6. **Mechanism fork**：至少两个机制必须给出不同 intervention prediction。
7. **Hard kill before smoke**：没有便宜 fatal control 的题不进十强。

### 特别高风险但仍保留

- **Dead-Branch Residue**：最接近 repo F3；只有绑定 mother paper 的 branch representation/lifecycle 才独立。
- **Action-Boundary State Routing**：不能退化成 generic `knows-but-doesn't-use`；必须找到 subtype-specific causal state。
- **Synonym-Saturation Escape**：不能退化成“keyword stuffing 攻击”；必须解释 mother circuit 里 semantic matching 与 saturation granularity 的不一致。

正式十题及每题 hard kill 见 [`BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md`](BATCH3_HAMDI_MOTHER_PAPER_N0_SURVIVORS_10_2026-08-29.md)。
