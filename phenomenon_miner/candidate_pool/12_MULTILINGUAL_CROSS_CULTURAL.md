# 领域 12：多语言、跨语言状态与跨文化适应

状态：`14 candidate cards — NOVELTY-AUDITED: 3 PROMOTE / 4 HOLD / 7 KILL；均未做行为验证`
审计详情：[AUDIT_UDH_MCC.md](audits/AUDIT_UDH_MCC.md)
母问题：模型是否能翻译并分别理解多种语言中的内容，却没有把“同一命题、同一来源、同一实体、同一次更新”归并到同一个世界状态？

## 顶会边界

普通“同一事实换语言答案不同”已经被系统研究：[EMNLP 2023 cross-lingual factual consistency](https://aclanthology.org/2023.emnlp-main.658/)、NAACL 2024 [CLiKA](https://aclanthology.org/2024.naacl-long.339/)、ACL 2025 [Lost in Multilinguality](https://aclanthology.org/2025.acl-long.253/) 和 Findings EMNLP 2025 [cross-lingual knowledge and reference](https://aclanthology.org/2025.findings-emnlp.267/) 已覆盖行为一致性、表示共享、late-layer language transition 与 code-mixed coreference；EMNLP 2025 的 [multilingual knowledge editing survey](https://aclanthology.org/2025.emnlp-main.803/) 说明参数知识编辑的跨语传播也已形成独立成熟母线。ACL 2026 [All Languages Matter](https://aclanthology.org/2026.acl-long.338/) 还已占据 mRAG 对 English/query-language 的 reranking bias。文化知识/价值表现差也有 [CulturalBench](https://aclanthology.org/2025.acl-long.1247/)、[NormAd](https://aclanthology.org/2025.naacl-long.120/) 和 EMNLP 2024 [文化评测综述](https://aclanthology.org/2024.emnlp-main.882/)。

因此这里不保留“翻译后掉点”“低资源语言更差”“英文更可信”“模型不懂某文化”这些宽结论。高价值 signature 必须是：

```text
翻译 / alias / source / update / rule status 均能单独识别
                          ↓
跨语言组合时，内容被重复计数、拆成两个对象、不能撤销或接错行动
                          ↓
错误随 semantic identity 或 language boundary 以可预测方式移动
```

语言配对优先使用人译或原生平行数据；自动翻译只能做 discovery，不得把 MT 错误当模型现象。文化候选必须把“明确写出的当地规则”与“模型的语言/文化先验”做冲突，不能把多数群体答案当普遍真理。

## 优先数据架

| 数据 | 自然单元 | 适合轴 | 可得性 |
|---|---|---|---|
| [MKQA](https://aclanthology.org/2021.tacl-1.82/) | 10k 问题、26 种语言、人译且答案语言独立 | same proposition、answerability | 公开 |
| [MIRACL](https://aclanthology.org/2023.tacl-1.63/) | 18 语言的真实查询与 Wikipedia passage | cross-language evidence/source | 公开 |
| XOR-TyDi QA / TyDi QA | 跨语言检索与原生问题 | query/evidence language split | 公开；逐库核 license |
| [MEMERAG](https://aclanthology.org/2025.acl-long.1101/) | 基于 MIRACL 的专家标注 mRAG 回答 | faithfulness、relevance、summary | 公开性按论文仓库核验 |
| [mLAMA/RankC](https://aclanthology.org/2023.emnlp-main.658/) | 跨语言事实 probe 与编辑 | fact identity、update propagation | 公开代码数据 |
| [X-FACT](https://arxiv.org/abs/2106.09248) | 多语言真实 fact-check claims | claim/source/verdict | 公开 |
| [Multi3WOZ](https://aclanthology.org/2023.tacl-1.79/) | 四语言、多平行、文化适配任务对话 | slot update、日期、action | 公开仓库 |
| [MTOP](https://aclanthology.org/2021.eacl-main.257/) | 六语言 task-oriented utterance 与语义树 | intent/slot/action binding | 公开 |
| [CorefUD shared task](https://aclanthology.org/2022.crac-mcr.1/) | 多语言 identity coreference | mention→entity | 公开集合，license 随语言树库 |
| [MERLIN](https://aclanthology.org/2026.tacl-1.19/) | 5 语言 BBC 标题、7k mention、Wikidata ID | alias/entity identity | 公开论文资源 |
| [WikiANN](https://aclanthology.org/P17-1178/) / Wikidata aliases | 282 语言实体 mention/链接 | transliteration、same QID | 公开；自动标注需抽检 |
| [NormAd-Eti](https://aclanthology.org/2025.naacl-long.120/) | 75 国、2.6k 社交礼仪情境 | explicit norm specificity | 公开论文资源 |
| [CulturalBench](https://aclanthology.org/2025.acl-long.1247/) | 45 地区、人工验证文化问题 | local rule/knowledge controls | 公开论文资源 |
| [CAMT](https://aclanthology.org/2024.findings-emnlp.765/) | 6 语言对、文化特有项人类标注 | translation vs pragmatic status | 公开论文资源 |

## 候选登记

| ID | 简题 | stage | audit | priority | naturalness | source | collision |
|---|---|---|---|---|---|---|---|
| MCC-01 | 同一来源的两种语言被当成两名证人 | LITERATURE-CHECKED | **PROMOTE** | A | N3 | HUB | MEDIUM |
| MCC-02 | 同一事实的双语复述被计成两条事实 | LITERATURE-CHECKED | **KILL→probe MCC-01** | A | N3 | HUB | HIGH |
| MCC-03 | 一种语言里的修正没有更新另一语言的状态 | LITERATURE-CHECKED | **HOLD→setting MCC-10** | A | N3 | HUB | HIGH |
| MCC-04 | 跨语言撤回失败：否定已懂，旧主张仍有效 | LITERATURE-CHECKED | **HOLD→setting MCC-10** | A | N3 | HUB | HIGH |
| MCC-05 | 明知是同一名字，计数时仍成两个人 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | OCCUPIED |
| MCC-06 | 同一人的跨语言属性被拆成两份记录 | LITERATURE-CHECKED | **HOLD** | A | N3 | HUB | HIGH |
| MCC-07 | 跨语言转述把被引观点变成作者立场 | LITERATURE-CHECKED | **KILL** | B | N3 | HUB | OCCUPIED |
| MCC-08 | 权威排序答对，结论仍跟随查询语言来源 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | OCCUPIED |
| MCC-09 | 另一语言中的政策例外被理解却未执行 | LITERATURE-CHECKED | **HOLD** | A | N3 | HUB | HIGH |
| MCC-10 | 相同最终状态因更新语言路径不同而不同 | LITERATURE-CHECKED | **PROMOTE** | A | N3 | HUB | MEDIUM |
| MCC-11 | “传闻/已确认”跨语言摘要后状态脱落 | LITERATURE-CHECKED | **PROMOTE** | B | N3 | HUB | MEDIUM |
| MCC-12 | 条件两边跨语言时，条件门被绕过 | LITERATURE-CHECKED | **KILL** | B | N2 | HUB | OCCUPIED |
| MCC-13 | 明知当地明文规则，行动仍回到语言刻板默认 | LITERATURE-CHECKED | **KILL** | A | N3 | HUB | OCCUPIED |
| MCC-14 | 日期理解正确，跨语言工具参数却按错 locale | LITERATURE-CHECKED | **KILL** | B | N3 | HUB | OCCUPIED |

---

## MCC-01 — 同一来源的两种语言被当成两名证人

**一句话矛盾。** 模型能看出两段材料是一篇报道的原文与翻译，汇总证据时却像有两个独立来源一样增加信心。

**日常例子。** 一则通讯社稿被英文站和西班牙文站转载，不应算两家媒体独立证实。

**自然数据锚点与发现轴。** MIRACL/Wikipedia 跨语言页面、X-FACT 的真实 claim、新闻站点明确标注的翻译/转载；`one source`、`source+translation`、`two independent sources`，内容支持方向和总 token 匹配。source identity 必须由 canonical URL、Wikidata item 或转载声明确定。

**晋级 signature。** 模型准确回答“前两段同源”且能区分独立来源，但 confidence/verdict 只在 source+translation 条件像证据数从 1 变 2；加入同语言副本的效应显著较小或具有不同机制。若所有重复文本都同样加权，退化为重复证据母现象。

**规模生存与竞争机制。** 多语能力随规模增强会使内容合并更好，但 evidence accumulator 可能按语言通道或 document slot 计数。A：同一命题进入两个 language-specific evidence nodes；B：命题已共享，但 source-independence mask 未传给累加器。A 预测跨语 activation 两簇，B 预测共享 proposition、独立性 gate 因果失效。

**最近工作与空位。** GroupQA/Whose Facts Win 覆盖重复与来源偏好，ACL 2026 mRAG 覆盖 language bias；当前可辩护空位是 **source identity 被显式识别、翻译副本仍获得独立证据权重**。截至 2026-08-28，以检索式 `[LLM multilingual translated duplicate evidence source independence]` 未找到完整覆盖该 signature 的主论文。

**最便宜的证伪。** 取 30 个短、canonical source 明确的平行段落，先测 source identity，再做一条冲突 claim。若翻译副本效应不高于同源同语复述，或 identity 判断不正确，KILL。

## MCC-02 — 同一事实的双语复述被计成两条事实

**一句话矛盾。** 模型知道双语句子语义完全相同，回答“有几件事/几项理由”时却计成两项。

**日常例子。** 会议纪要先写 “The office closed”，下一行给出中文翻译“办公室已关闭”；世界里只发生一次关闭。

**自然数据锚点与发现轴。** MKQA 人译问题、FLORES/CAMT 平行句、MAVEN-FACT 的 event IDs；从有 stable event/entity ID 的自然文本选句，比较单语重复、双语翻译、两个真正不同事件。输出 event count、timeline 与 summary。

**晋级 signature。** translation equivalence 与 event coreference 都能回答正确，但 count/timeline 产生两个 event token；最好在摘要中出现两次不同措辞，而单语副本不会。若只是计数指令脆弱，KILL。

**规模生存与竞争机制。** 强模型更会翻译，却可能在 episodic writer 中按 mention/language 建节点。A：language-specific event instantiation；B：共享 event node，但 count head 对 mention nodes 求和。可用 event identity activation patch 与 count readout区分。

**最近工作与空位。** 跨语言 factual consistency 与 coreference 已覆盖同义识别；独特性是 **semantic equivalence intact / event cardinality wrong**，不是答同一事实是否一致。

**最便宜的证伪。** 从 25 个短平行句做 1-vs-2 event 对照。若单语重复也同幅双计或翻译判断不稳，KILL。

## MCC-03 — 一种语言里的修正没有更新另一语言的状态

**一句话矛盾。** 模型准确翻译并复述西班牙语中的新值，随后用英语回答当前状态时仍给旧值。

**日常例子。** “会议周二。Perdón, será el jueves（抱歉，改为周四）。”最终英文日程只能是 Thursday。

**自然数据锚点与发现轴。** Multi3WOZ 的平行 dialogue state、PRESTO 多语言修正、MTOP slot values；`same-language repair`、`cross-language repair`、`cross-language add`，并控制脚本、距离和最后提问语言。gold 来自原 dialogue-state replacement。

**晋级 signature。** repair type、new value 与 translation 均正确，current-state/action 只在语言跨界时复活 old value；改变 query language 后错误跟随 state channel 而非最后文本位置。

**规模生存与竞争机制。** 多语 reader 能解码 new value，但 dialogue state cache 可能按语言分区。A：每种语言有独立 slot state，新 update 未覆盖旧语言槽；B：canonical state 已更新，English answer decoder 又检索旧 English mention。

**最近工作与空位。** PRESTO 覆盖多语不流畅/修正，EMNLP 2025 [multilingual knowledge editing survey](https://aclanthology.org/2025.emnlp-main.803/) 汇总了参数知识编辑的跨语言传播；空位必须是 **单次自然对话内部的 transactional slot replacement 已被正确理解，却没有跨语言 commit 到当前状态**，不能写成一般“更新没有传播”。

**最便宜的证伪。** 直接取 40 个 Multi3WOZ/PRESTO 原生 repair，人工确认自然 code-switch 点。若 current slot 同语言也差或 translation probe 不高，KILL。

## MCC-04 — 跨语言撤回失败：否定已懂，旧主张仍有效

**一句话矛盾。** 模型知道后一语言说的是“前述消息不实/请撤回”，最终摘要或判断仍保留旧主张。

**日常例子。** 英文消息称活动取消，中文更正说“刚才消息有误，活动照常”；模型翻译正确却仍回答“活动取消”。

**自然数据锚点与发现轴。** X-FACT 中真实 claim/correction、新闻更正、Multi3WOZ cancel/rebook turns；只采用有原生 correction/retraction label 的材料。比较 same-language 与 cross-language retraction，问 status、current fact、next action。

**晋级 signature。** retraction scope 与 corrected proposition 正确，summary/action 才保留旧 assertion；与 MCC-03 的值 replacement 区分，本卡要求 **assertion status 从 valid→withdrawn**。

**规模生存与竞争机制。** 否定/翻译能力提高不保证跨语 truth-maintenance。A：retraction edge 只作用于本语言 proposition copy；B：proposition 共享，但 status tag 不进入 summarizer。

**最近工作与空位。** cross-lingual factual consistency、否定污染和 correction 文献邻近；完整 signature 需要 language-bound invalidation 以及同语正常 control。

**最便宜的证伪。** 20 个真实更正 + 20 个任务对话 cancel；若同语/跨语差异不存在，或旧主张在 status report 里也未撤销，KILL。

## MCC-05 — 明知是同一名字，计数时仍成两个人

**一句话矛盾。** 模型正确说 “محمد صلاح” 与 “Mohamed Salah” 指同一人，统计参与者或合并记录时仍当作两个人。

**日常例子。** 双语新闻名单出现同一人的阿拉伯文和拉丁文名字，人数不应加一。

**自然数据锚点与发现轴。** MERLIN 的 Wikidata ID、WikiANN/Wikidata aliases、跨语言 person-entity linking 集合；同 QID 的不同 script alias 对照不同 QID namesake。先问 linking/alias，再做 count、attribute join、group membership。

**晋级 signature。** explicit entity linking 正确，only downstream cardinality/join 双计；namesake control 能分开，交换 script 后错误跟随 alias boundary。若 linking 本身错，属于 multilingual entity linking。

**规模生存与竞争机制。** 实体知识增长会改善 QID mapping，但 working-memory entity writer 仍可能按 surface mention 创建 token。A：先建两个 entity token、后加 sameAs edge；B：一个 entity node，count head 对 mention representations 求和。

**最近工作与空位。** Findings EMNLP 2025 已直接研究 code-mixed factual knowledge/reference，MERLIN 研究 linking，碰撞风险高。只有 **reference answer correct + cardinality/attribute merge failure** 才保留。

**最便宜的证伪。** 30 对 high-confidence Wikidata aliases，先筛 linking 稳定项。若计数无差或同语 alias 同样双计，KILL/转 OIR-08。

## MCC-06 — 同一人的跨语言属性被拆成两份记录

**一句话矛盾。** 模型知道两种语言里的名字是同一人，却不能把一种语言给出的职位与另一语言给出的所在地合并回答。

**日常例子。** 英文段落说 A 是工程师，日文段落说同一个 A 住在大阪；问“住在大阪的工程师是谁”应直接合并。

**自然数据锚点与发现轴。** MERLIN/Wikidata aliases、MIRACL 跨语言 passages、XOR-TyDi 多跳 QA；使用同 QID 且两个属性均有 provenance 的自然段落。四格 `same entity/different entity × same language/cross language`。

**晋级 signature。** entity identity、两个单属性问题均正确，只有 cross-language conjunction/join 失败；错误落点最好是“没有此人”或只返回一侧实体，而不是自由 hallucination。

**规模生存与竞争机制。** 强模型可以独立读两段，但属性绑定可能留在 language-local entity copy。A：sameAs edge 不做 feature union；B：feature 已合并，multi-hop retriever在 query language 只访问一侧。

**最近工作与空位。** multilingual multi-hop/RAG 与 cross-language reference 已覆盖宽能力；本卡需 **identity known + single-hop intact + cross-language attribute union selectively fails**。

**最便宜的证伪。** 从 Wikidata/MIRACL 组 30 个自然两属性 join，人工读 10 个。若 same-language join 同样差或 entity identity 不稳，KILL。

## MCC-07 — 跨语言转述把被引观点变成作者立场

**一句话矛盾。** 模型正确识别外语引文的说话者和内容，换一种语言总结时却把引文写成报道者自己的断言。

**日常例子。** 法文新闻写“某官员声称 X”，英文摘要变成“报道确认 X”。

**自然数据锚点与发现轴。** QuoteBank/多语新闻平行语料、X-FACT claims、公开带 direct/indirect quote 标记的报道；对照 same-language summary 与 cross-language summary，保持 claim byte-equivalent via human translation。分别问 speaker、commitment、summary factuality。

**晋级 signature。** speaker attribution 和 “source merely claimed” 判断正确，只有 cross-language summary 的 narrator commitment 升级；同语摘要与无引文 factual statement 正常。

**规模生存与竞争机制。** 翻译会加强 proposition salience，同时弱化 speech-act carrier。A：translation bottleneck只传 content不传 commitment；B：commitment保留，target-language summarizer偏好无来源的陈述句。

**最近工作与空位。** 引文 attribution、事件 factuality 和跨语言一致性都邻近；需要 **attribution intact / commitment lost specifically at cross-language generation**，否则路由到 BWA-01。

**最便宜的证伪。** 20 条短 direct quotes、20 条 indirect reports；若 target summary 不出现结构化 commitment 升级或同语同样错，KILL。

## MCC-08 — 权威排序答对，结论仍跟随查询语言来源

**一句话矛盾。** 模型正确说来源 A 更权威、来源 B 只是转载，最终答案却跟随与提问语言相同的 B。

**日常例子。** 用户用日语提问；英文官方公告与日语论坛帖子冲突，模型会把官方公告排第一，却采用论坛内容。

**自然数据锚点与发现轴。** MIRACL/MEMERAG、X-FACT、官方多语公告；四格 `authority × language match`，来源权威由数据 provenance 或人工明确标签给定。分别测 source ranking、claim extraction、verdict。

**晋级 signature。** authority ranking 与两边 claim 都正确，verdict 仅在低权威来源匹配 query language 时翻转；交换 query language 可等变搬动错误，且 output language 固定。

**规模生存与竞争机制。** 大模型的 authority knowledge提高，但 language-congruent retrieval/generation path 也可更强。A：verdict accumulator按 language alignment加权，忽略显式 authority；B：authority加权正确，late decoder重取 query-language proposition。

**最近工作与空位。** ACL 2026 All Languages Matter 已发现 mRAG reranker 偏好英文/查询语言，碰撞高。只有 **oracle evidence已给出、模型显式 authority ranking正确、generator仍反向选择** 才超出 reranking bias。

**最便宜的证伪。** 不跑 retrieval，只给 30 对短材料，交换 query language。若 source ranking随 verdict一起错，或语言效应消失，KILL。

## MCC-09 — 另一语言中的政策例外被理解却未执行

**一句话矛盾。** 模型能翻译并确认外语条款中的例外适用于当前个案，执行任务时仍按主语言中的默认规则行动。

**日常例子。** 英文总则说需手续费，西班牙语补充条款明确当地退款免手续费；模型复述例外，却仍收取费用。

**自然数据锚点与发现轴。** Multi3WOZ 文化适配政策、跨语言公共服务/航空规则、ContractNLI 的明确 exception 文句配人工高质量翻译；`default language × exception language × query language` 三因子。gold 来自原规则逻辑。

**晋级 signature。** translation、exception truth、applicable rule report 均正确，tool argument/action 才恢复默认；same-language exception 正常，跨语言无例外 control 正常。

**规模生存与竞争机制。** rule reader 与 action compiler可能有语言偏好。A：exception gate 只修改同语言 policy state；B：统一 state 正确，tool decoder读取主语言/default span。

**最近工作与空位。** 普通 multilingual instruction following 与 guideline exception 均邻近；独特性是 **cross-language exception recognition/action split**，不是 target-language accuracy。

**最便宜的证伪。** 先用 30 个非高风险任务政策和固定 tool choices。若 report/action 都正常，再不扩展；若 translation/report 不稳，KILL。

## MCC-10 — 相同最终状态因更新语言路径不同而不同

**一句话矛盾。** 两段对话最终给出完全相同的当前状态，只因更新先后使用了不同语言，模型给出不同答案。

**日常例子。** 路径一：英文 A→中文 B；路径二：中文 A→英文 B；两者最终都是 B，却一个回答 A、一个回答 B。

**自然数据锚点与发现轴。** Multi3WOZ 平行 slot updates、PRESTO repair、MKQA entities；做严格 path pair：`L1:A→L2:B`、`L2:A→L1:B`、`L1:B`、`L2:B`。内容用人工平行版本，gold 为最后值。

**晋级 signature。** 语言和每次 update 都可正确复述，final state 却呈 language-conditioned recency/primacy 或 hysteresis；必须有非平滑或稳定方向，不能只是平均小掉点。

**规模生存与竞争机制。** 语言特定缓存即使翻译强也存在。A：每语 slot 各自 last-write-wins，query选同语槽；B：统一槽，但 update strength 随语言资源量不同。query-language swap只应搬动A，B则由update language质量主导。

**最近工作与空位。** cross-lingual consistency 通常比较静态翻译；本卡研究 **动态 state machine 的 language-conditioned path dependence**。

**最便宜的证伪。** 20 个两值 slot × 4 条路径。若单步 B 都不稳定或差异只与最后一句理解有关，KILL。

## MCC-11 — “传闻/已确认”跨语言摘要后状态脱落

**一句话矛盾。** 模型正确翻译“据称/未经证实/已确认”等证据状态，跨语言摘要只保留命题内容，丢掉其可靠性。

**日常例子。** 西班牙语原文是“据称工厂关闭”，英文摘要却写成“工厂关闭了”。

**自然数据锚点与发现轴。** MAVEN-FACT factuality、X-FACT、带 hedging/attribution 的多语新闻；由专业/人类翻译保持 evidential markers。比较 same-language vs cross-language summary，问 marker meaning、event factuality、summary commitment。

**晋级 signature。** marker translation 与 factuality classification 正确，只有 summary commitment 在 language transition 后系统升级；actual events 不受影响，否定/rumor/forecast 错误 destination 可分。

**规模生存与竞争机制。** proposition 传输比 evidential metadata 更受训练强化。A：跨语 concept bottleneck压缩掉 status；B：status保留，目标语言摘要风格覆盖 hedging。对隐藏状态的 status intervention应只在B后段生效。

**最近工作与空位。** event factuality和 translation consistency已覆盖宽能力；需要 **status recognition intact + target-language writer selectively strips it**。

**最便宜的证伪。** 30 条简短、人工核实的 factual/rumor/forecast 三元组。若同语摘要同样升级或 marker 直接翻错，KILL。

## MCC-12 — 条件两边跨语言时，条件门被绕过

**一句话矛盾。** 模型分别能翻译条件和结果，也能在单语中正确推理；条件写成一种语言、结果写成另一种语言时却把结果当无条件事实。

**日常例子。** “Si llueve（如果下雨），the event moves indoors”；已知没下雨，不应推出 indoors。

**自然数据锚点与发现轴。** XNLI/XCOPA 的人译/平行条件关系、Multi3WOZ 条件政策、ContractNLI 短条件条款；只在自然 code-switch boundary（引用、双语政策、跨团队消息）使用，不随机逐词混合。四格 `condition true/false × same/cross language`。

**晋级 signature。** clause translation、condition truth 和单语 implication 都正确，只有跨语言 boundary 让 consequent 无条件激活；交换哪一侧语言后效应跟随 scope boundary，而非某语言能力。

**规模生存与竞争机制。** 强模型可懂两句但 composition gate可能依赖局部语言 segment。A：semantic parser生成两个 discourse graphs，conditional edge未跨图；B：统一图正确，consequent salience晚层绕过 gate。

**最近工作与空位。** multilingual NLI 与 code-switch reasoning很邻近；本卡自然性风险较高，只有真实双语条款/对话中复现并有 **condition recognition/composition split** 才晋级。

**最便宜的证伪。** 先用 20 个自然 bilingual policy/对话，不做随机混词。若只在人造 code-switch 上出现，KILL。

## MCC-13 — 明知当地明文规则，行动仍回到语言刻板默认

**一句话矛盾。** 模型能复述情境中明确写出的当地规范，给建议或判断时仍按提示语言所关联的另一套文化默认。

**日常例子。** 场景明确说“在这里拒绝第二次劝食是礼貌的最终拒绝”，模型复述无误，却仍因英语礼貌脚本建议继续劝。

**自然数据锚点与发现轴。** NormAd-Eti 的不同 specificity 层级、CulturalBench 人工验证问题、CAMT 文化特有项；只选有地区标注与多名本地 annotator 支持的项。比较 `no explicit norm`、`explicit local norm agrees/disagrees with model prior`，并交换提示语言但固定地区。

**晋级 signature。** explicit norm extraction 与 applicability 正确；行为/acceptability judgment 仍跟随 prompt language 而非明文 norm，且在 prior-conflict 条件选择性出现。没有明确 norm 的文化差异不算。

**规模生存与竞争机制。** 更大模型拥有更强文化先验，也更能读规则，冲突未必随规模消失。A：语言触发的 norm prior 与 explicit rule竞争，policy gate权重失衡；B：规则已主导判断，response style/rationalizer又恢复默认。

**最近工作与空位。** NormAd 已研究从 abstract value 到 explicit norm 的文化适应，碰撞不低。只有 **explicit norm answer correct + downstream action reverts under language switch** 才是新机制口子。

**最便宜的证伪。** 从 NormAd 取 30 个 specificity 高且标注一致样本；提示语言只在人译版本间切换。若 norm extraction随判断一起错或翻译不等价，KILL。

## MCC-14 — 日期理解正确，跨语言工具参数却按错 locale

**一句话矛盾。** 模型能用自然语言正确解释 “03/04” 在当前 locale 是 3 April，写入工具参数时却提交 March 4。

**日常例子。** 用户法语对话明确采用日/月格式；agent复述“3 avril”，日历 API 中却写 `2026-03-04`。

**自然数据锚点与发现轴。** Multi3WOZ 的本地化 slot values、MTOP 日期/时间 intents、公开日历 function-call schema；只用 locale 元数据明确且可确定解析的原生日期。比较 unambiguous textual date、ambiguous numeric date、same/cross-language tool schema。

**晋级 signature。** natural-language date interpretation、locale 和目标格式都分别正确，tool argument 才落到另一 locale 的合法日期；错误随 tool-schema language 或预训练高频格式呈选择性切换。若只是不会格式化，KILL。

**规模生存与竞争机制。** 参数化 API patterns 可能持续压过已理解的 locale。A：semantic date object 正确，serializer使用错误 locale default；B：两个 date parse 并存，tool decoder选择英文高频分支。可对中间 ISO representation 做 patch/intervention。

**最近工作与空位。** multilingual semantic parsing 与 function-calling 已有大量工作；独特性必须是 **date semantics report intact / serializer chooses a competing valid locale interpretation**，且跨至少两个应用数据。

**最便宜的证伪。** 30 个 Multi3WOZ/MTOP 原生日程项，先筛复述正确样本。若只有弱模型出现或错误无固定 alternative date，KILL。

## 审计后短名单与 agent 路由

| 顺位 | 卡 | audit | 为什么仍值得 | 一票否决 |
|---:|---|---|---|---|
| 1 | MCC-10 language-conditioned state path | **PROMOTE** | strict same-final-state、原生 slot gold、dynamic state 不是静态多语一致性 | 只是最后一句读不懂；只改变回复语言 |
| 2 | MCC-01 translation counted as independent source | **PROMOTE** | provenance independence 是独立 gate，区别于 query-language bias 和 generic repetition | 同语副本同幅生效；source identity 不正确 |
| 3 | MCC-11 evidential status stripped | **PROMOTE** | proposition 保留 / status 丢失有多个离散 destination 与机制切口 | marker 翻错；同语摘要同样丢失 |

`HOLD`：MCC-03、MCC-04 并入 MCC-10 作两个 update subtype；MCC-06、MCC-09 先满足审计文档中的解锁条件。其余七张不再作为独立现象验证：MCC-07 已被 CS-Sum 的 speaker misattribution 压住，MCC-14 已被 ACL 2026 multilingual tool-calling 的更一般执行错位覆盖。首轮优先人译或原生资源，并保存每条 stimulus 的 translation/source provenance。
