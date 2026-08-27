# SEC / KRE 候选的残酷论文可用性审计

审计日期：`2026-08-28`
审计对象：[领域 06：社会证据、共同知识与集体状态](../06_SOCIAL_EVIDENCE_COLLECTIVE.md) 的 SEC-01–12，以及 [领域 07：知识、检索、证据与引用](../07_KNOWLEDGE_RAG_EVIDENCE.md) 的 KRE-01–14。
结论：`4 PROMOTE-TO-PILOT / 7 HOLD / 15 KILL-or-ROUTE`。本轮**没有运行任何模型**；PROMOTE 只表示“若跨家族行为成立，论文空间仍足以立即进入机制研究”，不表示现象已经被证实，也不表示完成了正式 novelty claim。

## 判定标准

- **PROMOTE-TO-PILOT**：自然问题能一句话说清；有公开自然数据或可审计原生记录；预注册的 signature 不是普通 accuracy drop；最近工作没有报告同一个 `recognition intact → selective downstream use failure` 及同一错误目的地；一旦在 3/5 家族和多个尺寸成立，内部机制问题立即明确。
- **HOLD**：exact signature 尚未找到，但母现象拥挤、gold 含混或最可能机制已被占；只有先出现非常特定的错误结构，才允许继续。
- **KILL**：最近工作已经覆盖现象或关键 dissociation，或者候选只是更宽现象的普通子例。
- **KILL (ROUTE)**：不应单独成题，但可作为仓库中已有主候选的自然应用复现。

检索优先覆盖 ACL/EMNLP/NAACL 2023–2026、相关 Findings、ICLR/ICML/NeurIPS 与 arXiv 2024–2026；按候选的一句话矛盾、内部解离、数据名、常见同义词和错误目的地做 targeted search，并回看论文摘要/正文而非只看标题。**未检出 exact work 不是不存在证明**；正式立项前仍需作者级 citation chaining 和新一轮时间戳检索。

## 总表

| 卡 | 判定 | 最近的占位工作 | 残酷判断 |
|---|---|---|---|
| SEC-01 | **PROMOTE** | [Grounding Gaps](https://aclanthology.org/2024.naacl-long.348/)、[Frame of Reference](https://aclanthology.org/2026.findings-acl.1645/)、[Mirage of the Shared Mind](https://doi.org/10.21203/rs.3.rs-9230289/v1) | common-ground 与公私 epistemic decoupling 已拥挤，但未见“每个人一阶知识严格匹配，仅 public announcement 产生协调优势”的自然行为解离。须避开 formal DEL puzzle 和 multi-agent consensus，落在同一模型的 matched coordination action。 |
| SEC-02 | **HOLD** | FANToM、OpenToM、对话 grounding 与 agent state tracking | `delivered/open/read/understood` 很自然，但状态日志容易变成模板化 access-control QA；强模型若只在含混日志上失败，没有 ACL 级现象。 |
| SEC-03 | **KILL** | [Everyone Conforms, No One Believes](https://arxiv.org/abs/2608.02758) | 100 场景、10 领域、8 模型/6 机构已经直接研究 pluralistic ignorance、private rejection/public conformity、cascade 和 ablation。当前卡的主要叙事已被占。 |
| SEC-04 | **PROMOTE** | [RumourEval](https://aclanthology.org/S19-2147/)、[joint stance/veracity](https://aclanthology.org/W19-6122/)、[stance + debunking](https://aclanthology.org/2024.findings-acl.796/) | 旧工作把 query/comment 当独立 stance 并用于 veracity pipeline；未见对同一 LLM 证明“逐条 stance 判对，但聚合时因 claim-token 重复把 query/comment 正计数”的选择性解离。 |
| SEC-05 | **KILL (ROUTE)** | 来源可信/重复证据、GroupQA、仓库 Lineage–Weight | firsthand/hearsay 是 lineage dedup 的自然实例，不足以单独成题；只能作为 Lineage–Weight 的社会传播外部复现。 |
| SEC-06 | **PROMOTE** | [Unraveling Misinformation Propagation](https://aclanthology.org/2025.findings-emnlp.627/)、[When Do LLMs Admit Their Mistakes?](https://arxiv.org/abs/2505.16170) | correction/continued influence 已知，但未见“撤回状态和 provenance 边均识别正确，只撤销源节点、不沿复制链失效；独立来源保持有效”的 descendant-selective signature。 |
| SEC-07 | **KILL (ROUTE)** | collective/distributive errors、仓库 OIR | institution→member 是 OIR 的直接自然实例；个人私人 belief 又缺可靠 gold。真实 roll-call 可作为 OIR 外部复现，不能另立主现象。 |
| SEC-08 | **KILL** | [TactfulToM](https://aclanthology.org/2025.emnlp-main.1272/)、[pluralistic ignorance](https://arxiv.org/abs/2608.02758) | public statement/private belief、white lie、动机和公开顺从都已成为直接研究对象；只补一个 belief/action readout 不足以抵抗“普通 ToM 子集”质疑。 |
| SEC-09 | **HOLD** | [Whose Facts Win?](https://aclanthology.org/2026.acl-long.1357/) | 来源类型、声望、流行度、地域接近、学术头衔已被跨 13 个开源模型系统扫过。仅“global prestige × query-specific jurisdiction”严格 crossover、且 gold 客观时才可能脱离母现象。 |
| SEC-10 | **PROMOTE** | [AI is a Pro-Social Norm Complier](https://doi.org/10.1016/j.econlet.2024.111828)、[Normative Reasoning in LLMs](https://aclanthology.org/2025.blackboxnlp-1.17/)、[NormBank](https://aclanthology.org/2023.acl-long.429/) | 2024 经济学工作已发现单一 ChatGPT 对 descriptive/injunctive norm 都改变独裁者博弈行为；但它没有明文冲突 policy、语义识别解离、跨家族或机制。只在这些新增 signature 全部成立时才不被母现象吞掉。 |
| SEC-11 | **KILL (ROUTE)** | GroupQA、Whose Facts Win、仓库 Lineage–Weight | 与既有 Lineage–Weight 主候选同一 signature，不重复立项。 |
| SEC-12 | **KILL (ROUTE)** | collective/distributive quantifier work、仓库 OIR | group decision→unanimity 正是 collective-to-distributive projection；作为 OIR 的 roll-call setting 保留。 |
| KRE-01 | **KILL** | [Rethinking Reasoning-Intensive Retrieval](https://aclanthology.org/2026.acl-long.1705/) | ACL 2026 已把“13 轮未取回 gold 后，agent 推断插件不存在”作为 canonical evidence-deprivation case；即使未系统命名 0-hit ontology flip，核心故事已被明确写出，抢题风险过高。 |
| KRE-02 | **KILL** | [The Distracting Effect](https://aclanthology.org/2025.acl-long.892/)、[Query–Knowledge Relevance](https://aclanthology.org/2024.emnlp-main.353/) | query echo/lexical overlap distractor 是 hard distraction 的典型子类；“另问一次 relevance 能答对”不足以构成独立 phenotype。 |
| KRE-03 | **HOLD** | [webpage metadata/appearance](https://aclanthology.org/2024.blackboxnlp-1.24/)、headline–body incongruity 文献 | 未见 exact `body commitment correct → metadata-slot polarity late override`，但 title/clickbait/presentation bias 母区过密。只有错误跟 metadata slot 而非位置、词汇重叠移动时才复活。 |
| KRE-04 | **KILL** | [When Facts Change](https://aclanthology.org/2026.findings-acl.103/)、[HoH](https://aclanthology.org/2025.acl-long.301/) | 2026 工作已报告大型模型能检测 temporal conflict/识别 mutability，却不把判断传播到最终预测，连 scale-dependent failure point 都已给出；与本卡 signature 基本同构。 |
| KRE-05 | **HOLD** | [ALCE](https://aclanthology.org/2023.emnlp-main.398/)、[Attribute or Abstain](https://aclanthology.org/2024.emnlp-main.463/)、[ArchEHR-QA](https://www.nature.com/articles/s41597-026-06639-z) | ArchEHR-QA 已跨 Llama/Mixtral 比较 Together、Answer First、Evidence First，并显示 citation integration/order 改变 factuality/relevance。只剩“within-item 正确答案定向翻到可逐字引用的错误 span”可能独立。 |
| KRE-06 | **HOLD** | MIRAGE、CiteFix、[table data referencing errors](https://aclanthology.org/2026.acl-long.762/) | attribution/citation error 已高度拥挤。只有 answer/support judgment 都对、错误 citation 显著富集在 same-entity/different-relation 等关系邻居，才形成可解释 pointer-binding phenotype。 |
| KRE-07 | **HOLD** | [Llama See, Llama Do](https://aclanthology.org/2025.acl-long.791/)、fact-check/negation work | “上下文出现过的 token 获得更高 logits”已有机制论文和 causal heads；假引文复活很可能被 contextual entrainment 包含。只有 document-role/polarity binding 超出 token repetition controls 才保留。 |
| KRE-08 | **KILL** | [Latent Multi-Hop Reasoning](https://aclanthology.org/2024.acl-long.550/) 及大量 decomposition/composition work | 子题全对/full question 错已是多跳推理常规分析。没有先观察到稳定 alternative-bridge destination 前，不应把普通 composition failure 包装成新现象。 |
| KRE-09 | **KILL** | [Is Summary Useful or Not?](https://aclanthology.org/2024.lrec-main.821/)、[generated explanations may not help](https://aclanthology.org/2022.blackboxnlp-1.14/) | self-summary 的 downstream utility 已有直接母问题；“人工审计充分”成本高且边界争议大，当前没有独特错误目的地。 |
| KRE-10 | **KILL** | [Over-Searching](https://aclanthology.org/2026.eacl-long.361/)、[S2G-RAG](https://aclanthology.org/2026.acl-long.1185/)、Adaptive-RAG | over-search 与 sufficiency controller 均已成为系统研究对象；再做“报告充分但动作错误”很容易只是 representation-use 重新命名。 |
| KRE-11 | **HOLD** | [Failing to Falsify](https://arxiv.org/abs/2604.02485)、Over-Searching | confirmation bias 已跨 11 模型、多家族/尺寸，并做干预和迁移；只剩交换初始 prior 后、证据强度和 polarity judgment 均匹配的 **stop-threshold hysteresis** 可能独立。 |
| KRE-12 | **KILL (ROUTE)** | GroupQA、Whose Facts Win、仓库 Lineage–Weight | chunk fake corroboration 是 lineage-weight 的 RAG 实例；只做应用复现。 |
| KRE-13 | **KILL (ROUTE)** | 仓库 Evidence-Induced Referent Displacement | 已有 promoted 主候选；本卡只是 RAG 外部复现入口。 |
| KRE-14 | **KILL** | long-context serialization/boundary literature；仓库本地 MuSiQue null | 简单 one-document vs many-documents 主效应已有本地负证据，也缺新的自然交互假设；停止消耗。 |

## 四个真正进入验证队列的候选

### 1. SEC-06：撤回没有沿传播链生效

这是本轮最强候选。它不是“模型不听 correction”，而是一个图更新错误：

```text
source recants
model correctly identifies recantation
model correctly identifies copies and independent reports

expected: invalidate source + descendants, preserve independent reports
observed candidate: invalidate source only
```

它同时具备自然性、deterministic gold、路径/图机制和明确的错误目的地。现有 misinformation propagation 主要研究错误如何进入后续 reasoning，self-retraction 研究模型是否承认自身错误；它们没有给出 recognized provenance graph 上的 descendant-selective invalidation。若跨家族成立，机制问题立即是：失效 mask 没传播，还是传播了但 evidence reader 没读。

**硬 KILL 条件：** 模型不认识撤回、分不清转载与独立来源、真实链路 gold 争议大，或任何 correction 都同样失败。

### 2. SEC-04：疑问句被当成支持票

这个候选的价值不在“谣言判断会错”，而在 **speech-act sign 与 proposition payload 分离**：模型逐条知道“真的吗？有来源吗？”是 query，却在汇总时把其中重复出现的 claim 当作 positive evidence。RumourEval 天然提供 query/comment/stance 与线程结构，数据不是为现象临时编造。

**必须观察到的错误形状：** query/comment 数量增加时 support count 或 veracity 单调向原帖移动；强度跟 claim-token repetition 走；deny 和真正 support controls 正常。若只是 stance classifier 本身错，立即 KILL。

### 3. SEC-01：人人知道仍不等于共同知识

common ground、二阶 ToM 和 public-announcement logic 都已有工作，因此论文不能写“LLM 不懂 common knowledge”。可保留的 exact phenotype 是：

```text
public announcement             identical private messages
everyone's first-order fact = correct in both
delivery/publicness report = correct in both

only coordination behavior should differ
```

如果模型把两者预测为相同行动，问题不是一般事实记忆，也不是普通二阶 QA，而是 public-event operator 是否建立、以及 coordination reader 是否读取它。数据必须来自会议通知、多人对话或协作场景；若退回 muddy-children 式谜题，论文空间显著缩水。

人类实验已经表明公共知识与 mere shared/private knowledge 会系统性改变协调行为（[PNAS 2019](https://doi.org/10.1073/pnas.1905518116)）；2026 的 *Mirage of the Shared Mind* 又研究了 LLM societies 的公开协调/私人状态脱钩。因此本卡的 novelty 只剩 **matched public-vs-identical-private event**，不能扩写成笼统 common knowledge 或 collective coordination。

**硬 KILL 条件：** 一阶知识未匹配、效果由 public/private 单词提示驱动、或只有显式高阶 belief QA 失败而自然行动没有差异。

### 4. SEC-10：描述性频率被洗成规范许可

这张卡只有在 policy gold 客观时才成立：模型既正确区分 `many do` 与 `permitted`，也正确复述明文规则，却在 advice/action readout 中让频率改变合法集合。它比“LLM normative reasoning 不好”窄得多，错误方向是可命名的 **descriptive-to-normative laundering**。

[McCannon (2024)](https://doi.org/10.1016/j.econlet.2024.111828) 已发现 ChatGPT-3.5 在独裁者博弈中同样响应 descriptive 与 injunctive norm，所以“描述性规范会影响 LLM 行为”本身绝不新。可发表空间只来自：明确冲突的客观 policy、两种语义均识别正确、双向合法集翻转、跨家族与内部 gate 机制。

**需要镜像双向：** `many do but forbidden` 被宽免，以及 `few do but explicitly permitted` 被误禁；只出现道德态度变化、社会建议变化或含混规范，不算。

## HOLD 队列：不是下一轮默认验证对象

| 卡 | 唯一允许复活的观察 |
|---|---|
| SEC-02 | 原生日志状态逐项正确，`delivered→known` 在自然行动上形成稳定边界；显式状态表仍不能修复。 |
| SEC-09 | 有客观 jurisdiction gold；global prestige 与 topical expertise 交换后形成 crossover，而不是一般 authority bias。 |
| KRE-03 | 正文 commitment 判对；错误严格跟 title/snippet metadata slot 移动，并排除首因、位置和 lexical overlap。 |
| KRE-05 | citation obligation 在同一 item 上把正确内容定向拉到“可逐字引用但错误”的 span；Answer First 选择性救回。 |
| KRE-06 | answer 与逐文档 support judgment 都正确；wrong citation 在关系邻居类别显著富集并跨数据复现。 |
| KRE-07 | false-quote 复活在 token repetition、位置、长度相配后仍只由 refutation/document-role 触发。 |
| KRE-11 | evidence polarity/strength/source 全部判对；交换 initial prior 后 stop threshold 跟 prior alignment 移动，并非一般 search bias。 |

没有上述观察，不应因为“一句话听起来不错”继续补机制故事。

## 建议的便宜验证顺序（本审计未执行）

1. **SEC-06**：15–30 条真实 correction/provenance chains，先人工审 gold；最可能给出 ACL 级结构。
2. **SEC-04**：直接复用 RumourEval/PHEME，数据和 stance gold 最现成，最容易快速证伪。
3. **SEC-01**：24–40 个自然协调 matched pairs；价值高，但 pair 审计比 SEC-04 更费力。
4. **SEC-10**：只用有明确 policy 的客观样本，并做双向镜像；不要先碰主观 social norm。

只有行为在至少 3/5 家族、多个尺寸上呈同方向，且 recognition probes 保持完整，才从 `PROMOTE-TO-PILOT` 升成仓库正式 promoted phenomenon。反之按硬 KILL 条件停止，而不是靠 prompt engineering 挽救。

## 主要近邻文献索引

- 社会状态/共同知识：[Common knowledge, coordination, and strategic mentalizing](https://doi.org/10.1073/pnas.1905518116)、[Grounding Gaps in Language Model Generations](https://aclanthology.org/2024.naacl-long.348/)、[MindDial](https://aclanthology.org/2024.sigdial-1.63/)、[Frame of Reference](https://aclanthology.org/2026.findings-acl.1645/)、[Mirage of the Shared Mind](https://doi.org/10.21203/rs.3.rs-9230289/v1)、[TactfulToM](https://aclanthology.org/2025.emnlp-main.1272/)、[Everyone Conforms, No One Believes](https://arxiv.org/abs/2608.02758)。
- 社会证据/规范：[RumourEval](https://aclanthology.org/S19-2147/)、[Reinforcement Tuning for Detecting Stances and Debunking Rumors](https://aclanthology.org/2024.findings-acl.796/)、[Whose Facts Win?](https://aclanthology.org/2026.acl-long.1357/)、[AI is a Pro-Social Norm Complier](https://doi.org/10.1016/j.econlet.2024.111828)、[NormBank](https://aclanthology.org/2023.acl-long.429/)、[Normative Reasoning in Large Language Models](https://aclanthology.org/2025.blackboxnlp-1.17/)。
- correction/temporal：[Unraveling Misinformation Propagation](https://aclanthology.org/2025.findings-emnlp.627/)、[When Facts Change](https://aclanthology.org/2026.findings-acl.103/)、[HoH: A Dynamic Benchmark for Outdated Information in RAG](https://aclanthology.org/2025.acl-long.301/)。
- RAG distraction/citation：[The Distracting Effect](https://aclanthology.org/2025.acl-long.892/)、[Llama See, Llama Do](https://aclanthology.org/2025.acl-long.791/)、[ALCE](https://aclanthology.org/2023.emnlp-main.398/)、[Attribute or Abstain](https://aclanthology.org/2024.emnlp-main.463/)、[ArchEHR-QA](https://www.nature.com/articles/s41597-026-06639-z)、[When LLMs Read Tables Carelessly](https://aclanthology.org/2026.acl-long.762/)。
- search/controller：[Rethinking Reasoning-Intensive Retrieval](https://aclanthology.org/2026.acl-long.1705/)、[Over-Searching](https://aclanthology.org/2026.eacl-long.361/)、[S2G-RAG](https://aclanthology.org/2026.acl-long.1185/)、[Failing to Falsify](https://arxiv.org/abs/2604.02485)。
