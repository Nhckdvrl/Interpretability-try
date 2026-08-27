# 领域 11：不确定性、决策与高风险文本

状态：`14 candidate cards — NOVELTY-AUDITED: 3 PROMOTE / 4 HOLD / 7 KILL；均未做行为验证`
审计详情：[AUDIT_UDH_MCC.md](audits/AUDIT_UDH_MCC.md)
用途：**仅用于研究评测与模型机理分析，不构成医疗、法律或其他专业建议。**
母问题：模型是否已经表示了“证据有多强、规则是否适用、行动是否被禁止”，却没有让这些状态进入最终决策的 gate？

## 顶会边界与研究安全

“模型不校准/不 abstain”已经非常拥挤。[TACL 2025 abstention survey](https://aclanthology.org/2025.tacl-1.26/)、ACL 2025 [ConfuseBench](https://aclanthology.org/2025.acl-long.840/) 和 ACL 2026 [MedQAbstain](https://aclanthology.org/2026.acl-long.1365/) 已分别覆盖 abstention 全景、识别不确定性来源以及医疗过度作答。医疗诊断中的典型病先验压过反事实证据也已被 ACL 2026 [MedEinst](https://aclanthology.org/2026.acl-long.1847/) 明确占位。法律侧，[LegalBench](https://arxiv.org/abs/2308.11462) 已包含 162 个法律推理任务，[LexGLUE](https://aclanthology.org/2022.acl-long.297/) 覆盖判例、条款与判决分类。

所以这里不把“答错”“置信不准”“不愿拒答”“医疗 anchoring”列为现象。候选只有满足下列结构才有资格晋级：

```text
证据强度 / 禁忌 / 法律地位 / 适用规则报告正确
                    ↓
最终 decision 仍稳定落到一个可命名的错误状态
                    ↓
错误对更新路径、authority slot 或 action threshold 有选择性
```

任何医学事实变换都必须由原数据标签、公开规范文本或有资格的领域专家确认；不得让生成模型自行发明“正确诊疗规则”。法律候选同理，只能使用数据原标签、原裁判文书或明确写出的规则。首轮只做离线文本评测，不输出给真实患者、当事人或决策者。

## 优先数据架

| 数据 | 自然单元 | 可用轴 | 可得性/限制 |
|---|---|---|---|
| [MedQAbstain](https://aclanthology.org/2026.acl-long.1365/) | 从标准医疗 MCQA 派生的不确定题 | answerable→insufficient、abstain | 论文与待核公开资源；宽 abstention 已占位 |
| [MedEinst](https://aclanthology.org/2026.acl-long.1847/) | 5,383 对典型/反事实病例 | 先验→判别证据翻转 | 论文称将开源；不能重复 diagnosis anchoring |
| [ClinicBench](https://aclanthology.org/2024.emnlp-main.759/) | 11 个临床生成、理解、推理数据集 | diagnosis→decision、开放回答 | 组合资源；逐子集核 license |
| [ClinBench](https://aclanthology.org/2026.findings-acl.767/) | 医学期刊真实病例 | 逐步证据、鉴别诊断 | 公开性与正文授权需逐项核验 |
| [CliMedBench](https://aclanthology.org/2024.emnlp-main.480/) | 中文临床场景 | 跨语言外部确认、开放决策 | 公开论文/代码；仅作研究 |
| [PubMedQA](https://arxiv.org/abs/1909.06146) | 研究摘要与 yes/no/maybe | 证据充分性、结论强度 | 公开 |
| [MedNLI](https://github.com/jgc128/mednli) | 临床前提—假设关系 | contradiction、evidence removal | 需完成数据使用申请/条款 |
| [LegalBench](https://github.com/HazyResearch/legalbench) | 专家设计的 162 个任务 | 规则、例外、证明标准、证据法 | 公开仓库；逐任务 license |
| [CaseHOLD](https://github.com/reglab/casehold) | 判决段落与 holding 选择 | majority/dissent、holding/背景 | 公开；注意训练污染 |
| [ContractNLI](https://aclanthology.org/2021.findings-emnlp.164/) | 合同全文、假设与证据 span | amendment、exception、scope | 可下载但须接受使用条款 |
| [LexGLUE](https://aclanthology.org/2022.acl-long.297/) | ECtHR、SCOTUS、EUR-LEX、条款、CaseHOLD | authority、holding、条款状态 | 公开聚合；逐子集 license |
| [MAVEN-FACT](https://aclanthology.org/2024.findings-emnlp.651/) | 112,276 个事件 factuality 标注 | alleged/possible/actual | 公开仓库；用于非专业外部确认 |

## 候选登记

| ID | 简题 | stage | audit | priority | naturalness | source | collision |
|---|---|---|---|---|---|---|---|
| UDH-01 | 结论已更新，行动仍沿旧结论 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | OCCUPIED |
| UDH-02 | 关键证据已撤回，决定仍不撤回 | LITERATURE-CHECKED | **KILL→merge UDH-11** | A | N3 | HUB | HIGH |
| UDH-03 | 最终证据相同，先不确定过就更爱拒答 | LITERATURE-CHECKED | **PROMOTE** | A | N3 | HUB | MEDIUM |
| UDH-04 | 会指出缺什么，却追问无关信息 | LITERATURE-CHECKED | **KILL** | C | N3 | HUB | OCCUPIED |
| UDH-05 | 禁忌识别正确，推荐仍越过禁忌 | LITERATURE-CHECKED | **HOLD** | A | N3 | REMOTE | HIGH |
| UDH-06 | 风险判断上升，处置紧迫度反而下降 | LITERATURE-CHECKED | **KILL→control UDH-05** | B | N3 | REMOTE | HIGH |
| UDH-07 | 排除性结果被承认，旧诊断仍驱动下一步 | LITERATURE-CHECKED | **HOLD** | B | N3 | HUB | HIGH |
| UDH-08 | 明知病例满足例外，仍套默认指南 | LITERATURE-CHECKED | **KILL→setting UDH-05** | A | N3 | REMOTE | HIGH |
| UDH-09 | 正确区分多数意见与异议，却引用异议作规则 | LITERATURE-CHECKED | **PROMOTE** | A | N3 | HUB | MEDIUM |
| UDH-10 | 会复述法定定义，适用时却回到日常词义 | LITERATURE-CHECKED | **HOLD** | A | N3 | HUB | HIGH |
| UDH-11 | 明知证据不可采，裁决时仍让它起作用 | LITERATURE-CHECKED | **PROMOTE** | A | N3 | HUB | MEDIUM |
| UDH-12 | 明知“更可能”未达到证明标准，仍作肯定裁决 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | HIGH |
| UDH-13 | 修订条款已被识别，旧条款仍决定结果 | LITERATURE-CHECKED | **HOLD** | A | N3 | HUB | HIGH |
| UDH-14 | 明知判例已被推翻，仍把它当现行依据 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | OCCUPIED |

---

## UDH-01 — 结论已经更新，行动仍沿旧结论

**一句话矛盾。** 模型明确说新证据使原结论不再成立，下一步建议或选择却仍精确对应原结论。

**日常例子。** 新检测结果排除了最初猜测；模型在“现在最可能是什么”上已经改口，却继续选择只服务旧猜测的下一步。

**自然数据锚点与发现轴。** MedEinst 成对病例、ClinBench/ClinicBench 中原生逐项检查结果，以及 LegalBench 中事实更新任务；不改医学或法律事实，只把原案例按真实出现顺序显示。比较 `all-at-once`、`old→decisive update` 与内容完全相同的 final state，并分别问 current conclusion、evidence relevance、next decision。

**晋级 signature。** 更新后的结论与关键证据判断都正确，错误决策稳定落到旧结论对应动作；同一最终证据集的直接路径正常、增量路径异常。若结论本身没更新，KILL。

**规模生存与竞争机制。** 规模会强化证据抽取和结论 reader，却可能强化缓存计划。A：belief state 已更新但 decision policy 读旧 plan carrier；预测 activation interchange 只交换 decision 前的旧状态即可搬动动作。B：新旧结论并存，回答 query 和 action query 使用不同检索键；预测错误随 action wording 而非证据距离变化。

**最近工作与空位。** MedEinst 已覆盖 counterfactual evidence 下的诊断 anchoring；ACL 2026 representation-use gap 覆盖宽泛“知道但不用”。只有出现 **diagnosis/current rule 已翻转 + action 独有的旧状态 destination + path dependence**，本卡才不是它们的子实验。

**最便宜的证伪。** 从 30 个已有 paired cases 只取模型两种结论都答对的样本，再比较一步决策。若错误不指向旧结论或 all-at-once 同样差，立即 KILL。

## UDH-02 — 关键证据已经撤回，决定仍不撤回

**一句话矛盾。** 模型能准确指出某证据已被撤回、作废或证实错误，最终决定仍像该证据有效一样。

**日常例子。** 报告后来注明“样本标签错了，请忽略上一结果”；模型复述这一点，却继续以旧结果为理由。

**自然数据锚点与发现轴。** PubMedQA 的证据—结论、ContractNLI 的 evidence span、真实勘误/更正文档，以及不含专业建议的 MAVEN-FACT 外部确认。四格 `evidence valid/invalidated × mentioned/not mentioned`；无效化语句必须来自文档原文或确定性标记。

**晋级 signature。** validity report 和可用证据集合均正确；只有 verdict/action 保留被撤回证据的方向，且内容换边后错误等变。若所有被否定信息都会泛化污染，转交 BWA-08，不在本领域晋级。

**规模生存与竞争机制。** 强模型更能保留原证据 payload，也更可能产生“内容仍在、status gate 未生效”。A：证据节点被 append，retraction 只加标签不减权；B：权重已归零，生成器被早期 verdict attractor 锁定。

**最近工作与空位。** 普通信念修正、否定处理和 context conflict 很拥挤；空位只可能是 **evidence admissibility/validity recognition intact，但 decision accumulator 不减账**，并能以因果干预改变 accumulator。

**最便宜的证伪。** 用 20 个非专业事实题和 20 个合同原生 span 先测。若显式问“可用证据”也保留旧证据，说明只是语言理解失败，KILL。

## UDH-03 — 最终证据相同，先经历不确定就更爱拒答

**一句话矛盾。** 两条路径最终提供完全相同且充分的证据，模型若先被迫承认“不确定”，后来仍更可能拒答。

**日常例子。** 一次性给齐材料时能决定；先给缺一页的材料、再补上那一页，最后却仍说信息不足。

**自然数据锚点与发现轴。** MKQA/PubMedQA 有确定答案与 no/maybe 状态的样本、MedQAbstain 的 answerable/insufficient 配对、LegalBench 的规则与事实；将原信息按字段边界分两轮，不改文本。比较 `full at once` 与 `partial→full`，并控制 token 距离和最后一轮重复总结。

**晋级 signature。** 模型能列出当前完整证据并回答“现在是否充分”为是，但只在 partial→full 路径 abstain；形成随首次 uncertainty commitment 出现的迟滞，而不是长上下文遗忘。

**规模生存与竞争机制。** instruction tuning 可能强化自我一致与 refusal 状态，所以规模未必消除。A：abstain 作为持久 dialogue state；B：第一轮生成的语言形成 self-conditioning anchor。前者应在隐藏第一轮文本但保留内部历史时持续，后者应随改写/删除 assistant turn 消失。

**最近工作与空位。** MedQAbstain 和 abstention survey 已占普通 under/over-abstention；本卡唯一空位是 **相同充分 final state 的 uncertainty hysteresis**。

**最便宜的证伪。** 取 40 个 full-context 稳定答对样本，做两种路径。若 partial→full 的 sufficiency report 也低，或差异只由 context length 解释，KILL。

## UDH-04 — 会指出缺什么，却追问无关信息

**一句话矛盾。** 模型准确说出决策缺少的唯一信息，获准追问一次时却问另一个无关问题。

**日常例子。** 它说“关键是不知道日期”，下一句却问用户喜欢哪种颜色。

**自然数据锚点与发现轴。** [ConfuseBench](https://aclanthology.org/2025.acl-long.840/) 的 document scarcity/query ambiguity、MultiWOZ/Multi3WOZ 缺 slot 对话、LegalBench 缺事实任务。先让模型标 missing variable，再自由生成或从候选选 clarification。

**晋级 signature。** 缺失变量识别高、候选问题语义也都能判断，最终 query 稳定落到显著但无决策价值的 slot；需要一个可交换的 wrong destination。若只是 clarification 质量差，本卡已被 ConfuseBench 完整覆盖。

**规模生存与竞争机制。** 强 reader 与 conversational policy 可接受不同训练信号。A：uncertainty representation 不送入 question planner；B：送入但对话礼貌/常见 slot prior 覆盖信息增益。

**最近工作与空位。** ConfuseBench 明确研究“识别并解决不确定性”，碰撞风险高。只有 **正确 missing-variable representation + 结构化错误 query route + 可因果搬动** 才留，否则立即标 `OCCUPIED`。

**最便宜的证伪。** 直接复用 ConfuseBench/Multi3WOZ 50 项，不构造新任务。若现象不能在强模型或不同领域出现，KILL。

## UDH-05 — 禁忌识别正确，推荐仍越过禁忌

**一句话矛盾。** 模型正确指出候选行动与当前个案存在明确禁忌或硬冲突，最终仍选择该行动。

**日常例子。** 系统在比较表里把某选项标为“本例不可用”，最后的选择却正是它。

**自然数据锚点与发现轴。** 仅使用有原生禁忌/排除标注的数据，如临床试验资格数据、公开药品标签中的明确 contraindication 字段，或更安全的 LegalBench/合同中“明确禁止”类比外部确认；专业标签必须人工抽查。三因子 `benefit prior × explicit prohibition × alternative available`。

**晋级 signature。** prohibition、适用主体和替代项均报告正确，选择错误只在高先验候选被明确禁止时发生；移除禁忌后同一候选正常，交换候选后错误跟随被禁止 action payload。

**规模生存与竞争机制。** 更大模型可能同时增强熟悉方案先验与规则 reader。A：contraindication 表示未进入 action veto；B：veto 存在但晚层 high-prior action feature 覆盖。可比较决策前后的 logit/activation intervention。

**最近工作与空位。** ClinicBench 测宽临床决策，普通 guideline adherence 与 safety benchmark 众多；只有 **contraindication report/action veto 解离** 及跨非医疗硬约束复现才有独特性。

**最便宜的证伪。** 先用 30 个公开、单一明确 exclusion criterion 的资格判断，避免生成治疗建议。若资格判断本身不对或错误不跟随被禁选项，KILL。

## UDH-06 — 风险判断上升，处置紧迫度反而下降

**一句话矛盾。** 加入一条按原数据标签严格增加风险的证据后，模型也承认风险更高，行动紧迫度却降低。

**日常例子。** 模型把“现在风险比之前更高”说对，却从“立即升级处理”改成“以后再看”。

**自然数据锚点与发现轴。** 只使用已有 ordinal risk/triage 标签的公开基准或规则明确的非医疗类比（网络安全告警、LegalBench sanctions/penalty thresholds）；医疗素材须来自 ClinicBench/CliMedBench 原标签并经专家复核。比较原生相邻风险级，不自行杜撰病征。

**晋级 signature。** risk classification 与依据方向正确，action urgency 才发生反单调；至少两个相邻层级和一个非医疗外部设置同方向。若只是生成措辞波动，KILL。

**规模生存与竞争机制。** ordinal risk reader 可随规模改善，但 policy 可能由案例相似度/默认模板控制。A：risk scalar 未送入 threshold gate；B：送入后发生类别标签与行动模板的错接。前者干预 risk feature 应单调搬动 action，后者只修 label binding 有效。

**最近工作与空位。** calibration 与 medical QA 不包含“模型自己也判得更危险、行为却更缓”的反单调 gate。若 risk report 也错，则完全退化为普通领域能力。

**最便宜的证伪。** 首先只做确定性非医疗风险等级的 50 对；若不存在，再不值得支付专家医疗审核成本，KILL。

## UDH-07 — 排除性结果被承认，旧诊断仍驱动下一步

**一句话矛盾。** 模型正确说新结果反驳最初诊断，后续检查选择仍以确认那个诊断为目标。

**日常例子。** “这个结果使 A 不太可能”之后，唯一选择的下一步仍是一个只用于继续确认 A 的动作。

**自然数据锚点与发现轴。** MedEinst/ClinBench 中有明确 discriminative evidence 的 paired cases；下一步候选必须来自原数据或专家标注，不让模型生成医学方案。先测 evidence→diagnosis，再测 diagnosis→information-gain target。

**晋级 signature。** 排除性证据解释和 current differential 均正确；next-information target 却稳定指向已降级诊断，且 all-at-once control 正常。若诊断仍错，已被 MedEinst 覆盖，KILL。

**规模生存与竞争机制。** 强模型可形成正确 posterior 但保留原 problem representation。A：question planner 寻址 initial diagnosis node；B：信息增益计算正确，生成器被常见 workup sequence 牵引。

**最近工作与空位。** MedEinst 的核心就是 atypical evidence 下误诊，碰撞很高；只有 **diagnosis 已修正 / information-acquisition policy 未修正** 的双重分离才保留。

**最便宜的证伪。** 只在 current diagnosis 稳定答对的 20–30 对上提供固定 next-test choices。若选择无系统旧目标，KILL。

## UDH-08 — 明知个案满足例外，仍套默认指南

**一句话矛盾。** 模型能逐条证明个案满足规则的例外条款，最终决定仍应用默认规则。

**日常例子。** 政策说“一般必须 X，但条件 E 下无需 X”；模型确认 E 成立，却仍要求 X。

**自然数据锚点与发现轴。** LegalBench 的 rule/exception 任务、ContractNLI 的 exclusion/exception hypotheses，以及公开规范文本；医疗仅作经专家确认的第二设置。四格 `default present × exception satisfied`，分别问 rule、exception membership、applicable consequence。

**晋级 signature。** exception text 检索正确、E truth 正确、适用性报告正确，final decision 却回到 default；错误只在 default action 有强先验时出现，并随 action payload 交换。

**规模生存与竞争机制。** 规模增强规则复述但也增强默认模板。A：exception gate 停在语言表示层；B：default 和 exception 都进入 policy，但 exception 是减性信号，晚层被正性 action feature 覆盖。

**最近工作与空位。** 法律 rule application、generics exception 和 guideline adherence 都邻近；必须是 **exception membership intact + default-action restoration**，而非条件推理错误。

**最便宜的证伪。** 先从 LegalBench/ContractNLI 自动找含明确 except/unless 的 50 项，经人工抽 20 项。若 exception membership 不高，KILL。

## UDH-09 — 正确区分多数意见与异议，却引用异议作规则

**一句话矛盾。** 模型知道某段是 dissent、另一段才是 controlling holding，回答“本案规则是什么”时却采用 dissent 的命题。

**日常例子。** 它能说“这句话是反对意见，不是法院结论”，最终法律摘要仍把那句话写成法院确立的规则。

**自然数据锚点与发现轴。** CaseHOLD/LexGLUE 的判决文本、CourtListener 等公开带 opinion type 的判例；仅保留 majority 与 dissent 在同一法律点明确相反、且有原文标签的样本。问 section role、speaker stance、holding 与下游 case application。

**晋级 signature。** section/author/stance 全部正确，holding 错误精确落到 dissent proposition；交换呈现顺序、长度、引文密度后仍由 authority binding 而非位置解释。

**规模生存与竞争机制。** 大模型更能理解异议论证，其说服力反而可能强化 competing proposition。A：proposition 与 authority status 在摘要压缩时脱绑定；B：绑定完整，writer 偏好论证更丰富/最近的 proposition。

**最近工作与空位。** CaseHOLD 已测 holding 识别，最新工作还研究 scale 与 memorization；本卡只有在 **dissent correctly tagged yet deterministically promoted**，并有 authority-binding 机制时超出普通 holding accuracy。

**最便宜的证伪。** 人工审 25 个短、标签明确、双方命题相反的公开判例。若错误随长度/末尾位置而非 dissent 身份移动，转为通用 position effect，KILL。

## UDH-10 — 会复述法定定义，适用时却回到日常词义

**一句话矛盾。** 模型准确复述法律文本对术语的专门定义，判断个案时却按普通语言含义使用该词。

**日常例子。** 法规明确说“本条中的 vehicle 包括自行车”；模型复述无误，却因“自行车通常不叫机动车”判定不适用。

**自然数据锚点与发现轴。** LegalBench statutory interpretation/definition tasks、公开法条与配套事实模式；对照同一术语无专门定义、定义扩大、定义缩小三种原生条款。不得让模型生成法定义义。

**晋级 signature。** definition extraction、scope 和事实归类均分别正确，只有 legal consequence 回到 ordinary meaning；定义反向时错误应跟随普通义而非固定标签。

**规模生存与竞争机制。** 参数规模增强词义先验，也增强条文 reader，竞争可能持续。A：statutory definition 未改写 lexical feature；B：改写完成，但 consequence head 检索 parametric ordinary sense。

**最近工作与空位。** LegalBench 已包含 rule application 与 interpretation；只有 **legal definition recognized / ordinary-sense restoration in downstream application** 的解离和机制，才不是单一 LegalBench 子任务掉点。

**最便宜的证伪。** 使用 LegalBench 已标注定义任务中 40 个短例，不加 prompt 花样。若模型不能复述 definition 或事实 category，KILL。

## UDH-11 — 明知证据不可采，裁决时仍让它起作用

**一句话矛盾。** 模型正确判断某信息在给定规则下不可作为证据，最终 verdict 仍随这条信息的内容翻转。

**日常例子。** 它说“这段传闻不可用于裁决”，把传闻从支持改成反对时，结论却跟着变。

**自然数据锚点与发现轴。** LegalBench 的 hearsay/evidence 任务与专家给出的规则—事实对；构造只做**内容符号交换**：同一不可采 span 分别支持 A/B，另有 matched admissible control。gold 由原 evidence-rule 标签确定。

**晋级 signature。** admissibility 与 rule rationale 正确；inadmissible 内容仍对 verdict 有大且方向可预测的因果效应，而 matched irrelevant text 没效应。若模型连 admissibility 都错，属于普通法律推理。

**规模生存与竞争机制。** 更强模型更能抽取证据内容，即便 status gate 仍弱。A：evidence accumulator 不乘 admissibility mask；B：mask 生效于显式理由，却未传到 verdict writer。

**最近工作与空位。** hearsay classification 和 irrelevant-context 工作是母现象；独特性是 **模型明确判为不可采、但 proposition 仍进入 verdict accumulator**，且不同于一般 distractor。

**最便宜的证伪。** 20 个 LegalBench hearsay 样本做支持/反对交换。若 verdict 不随不可采内容移动，或 relevant/admissible control 也异常，KILL。

## UDH-12 — 明知“更可能”未达到证明标准，仍作肯定裁决

**一句话矛盾。** 模型正确区分“最可能是真的”与“已达到所需证明标准”，最终裁决却只按最大概率候选作答。

**日常例子。** 它说现有材料让 A 略占优势，但规则要求远高于“略占优势”，仍判 A 成立。

**自然数据锚点与发现轴。** LegalBench 中 burden-of-proof/probability threshold 类任务、规则明确的合成概率事实（仅作机制 sandbox）和自然判例；主数据必须是专家创建任务，不能靠模型编法律。分别问 most likely、threshold met、verdict。

**晋级 signature。** relative likelihood 与 threshold comparison 都正确，verdict 才坍缩到 argmax；改变 threshold 而保持证据不变时，threshold report 变、verdict 不变。

**规模生存与竞争机制。** 分类式后训练强化“选最可能标签”，而 calibrated threshold 是独立 gate。A：verdict head 直接读 ranking；B：threshold feature存在但强 forced-choice writer 绕过 abstain/not-proven 状态。

**最近工作与空位。** calibration 与 legal reasoning 都很广；空位是 **ranking/threshold/verdict 三段中的特定 threshold bypass**，需要跨普通决策任务确认，不是法律准确率表。

**最便宜的证伪。** 先用 LegalBench 自带 burden tasks 和 30 个确定性概率 sandbox。若 threshold report 也随 verdict 错，KILL。

## UDH-13 — 修订条款已被识别，旧条款仍决定结果

**一句话矛盾。** 模型能说后来的 amendment 替换了原条款，回答当前权利义务时仍使用原条款。

**日常例子。** 合同先写“30 天”，修订为“60 天”；模型说“现行条款是 60 天”，却据 30 天判断违约。

**自然数据锚点与发现轴。** ContractNLI、公开 SEC 合同及 amendment 文档；只使用能由日期和明确 replace/amend 文句确定 current clause 的实例。比较 `amended path` 与只呈现最终条款的 `canonical path`，最终文本状态等价。

**晋级 signature。** current clause、effective date 与替代关系报告正确；只有 obligation/deadline verdict 在 amended path 复活旧值，形成 transaction-like hysteresis。若只是 long-context retrieval，KILL。

**规模生存与竞争机制。** 长上下文模型更能同时记住两个值，未必会 canonicalize。A：append-only clause memory；B：current clause 正确，但 downstream NLI 检索 lexical match 更强的旧 span。

**最近工作与空位。** ContractNLI 覆盖 document-level entailment，2025 [CLAUSE](https://arxiv.org/abs/2511.00340) 已用 CUAD/ContractNLI 派生扰动合同测试细粒度 discrepancy，目标切换/修正也有母现象；本卡的专属性质必须是**真实 amendment chain、相同最终合同状态、temporal precedence 已识别、旧 obligation 仍复活**，不能只是另一种扰动合同错误。

**最便宜的证伪。** 从公开合同中人工确认 20 个一句式 amendment；若 current clause report 不稳或 canonical path 同样错，KILL。

## UDH-14 — 明知判例已被推翻，仍把它当现行依据

**一句话矛盾。** 模型准确指出一项旧判例已被 overrule，给出现行规则或类案结论时仍引用旧判例的 holding。

**日常例子。** 它说“这条旧规则已不再有效”，紧接着以这条规则作为决定性依据。

**自然数据锚点与发现轴。** CaseHOLD 仓库中的 Overruling 子任务、LegalBench、带 Shepardized/明确后续历史标签的公开判例；只用有机器可核 authority status 的样本。对照 `never valid / valid / valid→overruled / overruled→reinstated` 中可得的自然路径。

**晋级 signature。** authority status、时间顺序和新规则均正确，应用题错误却落到旧 holding；移除旧文本即恢复，加入等长非权威历史文本无影响。

**规模生存与竞争机制。** 更大模型可能记得更多旧判例文本，也更会识别 overruling；二者可产生更强解离。A：authority node 未对 proposition 做 invalidation；B：invalidation 正确，citation/answer writer 受参数化著名判例先验控制。

**最近工作与空位。** CaseHOLD 与 citation/memorization 研究覆盖 holding recall；只有 **overruling knowledge intact + causal old-rule reuse** 才有独特解释空间。

**最便宜的证伪。** 先用 CaseHOLD Overruling 任务中可公开核验的 25 项。若模型 status knowledge 本身差，或错误不落旧 holding，KILL。

## 审计后短名单与 agent 路由

| 顺位 | 卡 | audit | 为什么仍值得 | 一票否决 |
|---:|---|---|---|---|
| 1 | UDH-03 uncertainty hysteresis | **PROMOTE** | 同 final state、定向 abstain 迟滞、公共 answerability gold、专业依赖最低 | sufficiency report 也错；只是长度/follow-up 波动 |
| 2 | UDH-09 dissent→holding | **PROMOTE** | proposition–authority binding 有独立错误落点，真实判决天然存在 | 只由位置、长度或更强论证导致 |
| 3 | UDH-11 inadmissible evidence still votes | **PROMOTE** | 法定 mask 与 verdict accumulator 可给出确定性因果预测 | 只能靠拼接虚构案件；admissibility 本身失败 |

`HOLD`：UDH-05、UDH-07、UDH-10、UDH-13；先满足审计文档中的解锁条件，不进入默认 smoke queue。其余七张不再作为独立现象验证。尤其 UDH-13 已被 ACL 2026 evolving legal standards 明显压缩，不能再排首位。高风险测试 agent 必须先做数据/标签审计，再请求模型预算。
