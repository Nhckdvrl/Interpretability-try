# UDH / MCC 候选的 novelty 与 occupancy 残酷审计

审计日期：`2026-08-28`
审计范围：领域 11（UDH）与领域 12（MCC），共 28 张候选卡。
行为状态：**未运行模型、未做现象成立性验证；本文只审计“如果成立，是否值得继续”。**
结论：`6 PROMOTE / 8 HOLD / 14 KILL`。

## 标签不是温和排序

- `PROMOTE`：若严格 signature 在多家族、多个尺寸上成立，即可把资源转向行为边界与机制；仍不等于已证明新颖或已证明现象存在。
- `HOLD`：有思想，但现在成立也不足以直接写机制论文；必须先解决母现象碰撞、数据自然性或错误落点不唯一中的至少一项。
- `KILL`：不再作为独立候选验证。可以充当 control、数据源或另一个 PROMOTE 的子条件，但不要给它单独预算。

审计故意不设 effect-size 硬阈值。真正的门槛是结构：同一 final state、正确中间判断、稳定错误 destination、选择性 control，以及模型规模增大后仍可能保留的 computation split。

## 六条红线

1. **“模型说对但做错”不是 novelty。** ACL 2026 已直接研究模型编码了 in-context representation 却不会使用；只有一个具体 gate、binding 或 writer 丢失了具体属性，才可能超出 [Language Models Struggle to Use Representations Learned In-Context](https://aclanthology.org/2026.acl-long.676/)。
2. **自报告正确不等于内部表示正确。** 所有 `PROMOTE` 都必须用 forced choice、counterbalanced destination、logit/activation 或行为等变性证明，不把自然语言解释当机制证据。
3. **普通 belief revision、abstention、code-switch robustness、multilingual RAG language bias 已占位。** 换数据集或换领域不能制造新现象。
4. **系统提示依赖即降级。** 目标 signature 必须在中性、任务必要的说明下出现；只有写出“请忽略/请坚持/请服从”才出现的效应不能晋级。
5. **只有人造拼接才成立即 KILL。** 可做原则性 matched relation，但原始情境、规则、更新或来源关系必须是现实任务中自然存在的。
6. **规模理由不是规模证据。** `PROMOTE` 中写的只是为什么值得跨尺寸测；实际若只在最小模型出现，仍要 KILL。

## 决定性占位文献

下表不是穷举综述，而是本轮改变判决的主要工作。检索覆盖 ACL/EMNLP/NAACL 及其 Findings、ICLR/ICML/NeurIPS/OpenReview 和 arXiv 2024–2026；关键词围绕每张卡的 exact signature，而非只搜 broad topic。

| 文献 | 已占的母现象或精确现象 | 对本池的后果 |
|---|---|---|
| [Belief Revision / Belief-R, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.586/) | 新证据到来后无法恰当修正 belief | 普通“旧信息没更新”不再新 |
| [Seeing Isn't Believing, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1884/) | agent 忽略与先验冲突的显式 observation；已命名 belief inertia 并做 intervention | UDH-01 被直接挤占 |
| [Ask Again, Then Fail, ACL 2024](https://aclanthology.org/2024.acl-long.577/) | follow-up question 使原本正确 judgment 摇摆 | UDH-03 必须是同终态的定向 abstention hysteresis，不能只是多轮不一致 |
| [Know Your Limits, TACL 2025](https://aclanthology.org/2025.tacl-1.26/)；[MedQAbstain, ACL 2026](https://aclanthology.org/2026.acl-long.1365/) | abstention 全景与医疗过度作答 | 一般拒答/校准不保留 |
| [ConfuseBench, ACL 2025](https://aclanthology.org/2025.acl-long.840/) | 识别并解决 query / document uncertainty | UDH-04 基本完整占位 |
| [MedEinst, ACL 2026](https://aclanthology.org/2026.acl-long.1847/) | 反事实判别证据下的医疗 anchoring | UDH-07 只能保留“诊断已改、下一检查仍追旧诊断”窄口 |
| [LegalBench](https://arxiv.org/abs/2308.11462)；[CourtReasoner, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1787/) | 法律规则、定义、hearsay、holding 与综合 judicial reasoning | 普通法律答错没有空位 |
| [Sycophants in the Courtroom, ACL 2026](https://aclanthology.org/2026.acl-long.497/) | temporal validity、normative relations、权威冲突；规模增大可放大脆弱性 | UDH-13/14 的“旧法仍用”母现象已占位 |
| [CaseFacts, ACL 2026](https://aclanthology.org/2026.acl-long.785/)；[Validate Your Authority, NLLP 2025](https://aclanthology.org/2025.nllp-1.13/) | Overruled 标签与 precedent treatment | UDH-14 直接 KILL |
| [CLAUSE, Findings EACL 2026](https://aclanthology.org/2026.findings-eacl.305/)；[contract comparison, NLLP 2024](https://aclanthology.org/2024.nllp-1.11/) | 合同 discrepancy 与 amendment comparison | UDH-13 只能 HOLD，不能直接宣称发现 amendment failure |
| [Cross-lingual Knowledge and Reference, Findings EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.267/) | code-mixed coreference、跨语知识一致性，并已做 layer analysis / activation patching | MCC-05 直接占位；MCC-06 需严格 attribute-union 解离 |
| [mRAG Context Utilization, MRL 2025](https://aclanthology.org/2025.mrl-main.15/)；[All Languages Matter, ACL 2026](https://aclanthology.org/2026.acl-long.338/) | query-language distractor 与 reranking language bias | MCC-08 直接占位；MCC-01 必须是 source independence 而非 language preference |
| [CS-Sum](https://arxiv.org/abs/2505.13559)；[Lost in the Mix, ACL 2026](https://aclanthology.org/2026.acl-long.2080/) | code-switched summarization 的 speaker misattribution、meaning shift 与一般 reasoning degradation | MCC-07/12 不宜独立验证 |
| [Cross-turn Language Switching, MME 2026](https://aclanthology.org/2026.mme-main.13/) | query-following 与 context-anchoring；task accuracy 基本稳定 | MCC-10 必须研究 state value，而非回复语言 |
| [Lost in Execution, ACL 2026](https://aclanthology.org/2026.acl-long.2039/) | 意图/工具选择正确但 multilingual parameter realization 错误 | MCC-14 已被更一般且更强的现象覆盖 |
| [NormAd, NAACL 2025](https://aclanthology.org/2025.naacl-long.120/) | 从抽象价值到明文当地规范的 cultural adaptability；明文规范下仍有错误 | MCC-13 的核心条件已占位 |

“截至日期未检出”只说明本轮 exact-query 未找到，不是优先权证明。若 smoke test 成立，提交前仍需作者级 citation chasing、Google Scholar forward citations 与最近 arXiv 再审一次。

## 28 张卡总判决

| ID | 判决 | 核心理由 | 唯一可继续的结构 |
|---|---|---|---|
| UDH-01 | **KILL** | Belief-R、belief inertia、MedEinst 与 representation-use 已把“更新没进入行动”包围；当前卡没有比它们更独立的 gate | 仅可作为其他 action-gate 卡的 control |
| UDH-02 | **KILL** | 普通 retraction / invalidation 是 belief revision；其“无效证据仍投票”部分与 UDH-11 重复 | 合并进 UDH-11 的 admissibility/validity mask，不单跑 |
| UDH-03 | **PROMOTE** | 同一充分 final evidence 下，由先前 uncertainty commitment 造成定向 abstention 迟滞；不同于一般 over-abstention 与 follow-up vacillation | `full-at-once 正常；partial→full 仍拒答；当前充分性判断正确` |
| UDH-04 | **KILL** | ConfuseBench、AskBench/SAGE 类 clarification 工作直接覆盖识别缺口与提问质量 | 无独立预算 |
| UDH-05 | **HOLD** | contraindication benchmark 与 guideline adherence 很拥挤；医学标签成本高，且容易只是 generic rule-use gap | 必须跨医疗与非医疗硬禁令复现“禁忌识别正确 / action veto 失效” |
| UDH-06 | **KILL** | triage/clinical safety audits 已观察风险识别与处置不足；单调 urgency 只是其窄实例且需专家 | 可当 UDH-05 的 ordinal control |
| UDH-07 | **HOLD** | MedEinst 已占诊断 anchoring；公开数据通常没有可靠 next-test gold | 只有 `current diagnosis 正确 + information-acquisition target 精确追旧诊断 + all-at-once 正常` 才重审 |
| UDH-08 | **KILL** | 与 UDH-05、普通 exception reasoning、representation-use 重复，没有独有 destination | exception 可作为 UDH-05 非医疗 setting |
| UDH-09 | **PROMOTE** | 不是 holding accuracy，而是 proposition 与 authority-role 脱绑定：模型知道谁是 dissent，却把其命题提升成 controlling rule | `role/stance 正确；holding 精确等于 dissent proposition；位置长度控制无效` |
| UDH-10 | **HOLD** | statutory definition 与 ordinary meaning 已有任务和专门研究；数据常把“找定义”和“适用定义”分开 | 只有明确法定定义已正确绑定、case application 却回到 parametric ordinary sense，并随词义竞争强度出现结构曲线 |
| UDH-11 | **PROMOTE** | hearsay 分类不等于裁决中的证据权重；精确的 admissibility-mask / verdict-accumulator 解离尚未检出完整覆盖 | `可采性、scope、其支持方向均正确；判决仍随不可采内容等变翻转` |
| UDH-12 | **KILL** | burden-of-proof、threshold calibration、forced-choice overcommit 都是拥挤母现象；自报“未达标准”也易受模板诱导 | 只可作为 UDH-11 的 decision-threshold control |
| UDH-13 | **HOLD** | ACL 2026 已系统研究 evolving legal standards，另有 amendment comparison / contract discrepancy | 只有自然 amendment chain 的同终态 path dependence，加上 current clause report 正确、旧 obligation ghost 可因果定位，才重审 |
| UDH-14 | **KILL** | CaseFacts 已有 6,294 个 Supported/Refuted/Overruled claims；precedent treatment 与 evolving authority 都已直接做 | 不再单独验证 |
| MCC-01 | **PROMOTE** | language bias 与 repetition 都不是目标；目标是已识别 translation provenance 后仍违反 source independence | `同一 source 的译本只在跨语时获得第二票；同语复述、独立来源、query language 均有反事实控制` |
| MCC-02 | **KILL** | 是 MCC-01 的更窄计数版，也容易退化为 mention counting / coreference | event-count 可作为 MCC-01 downstream probe，不单跑 |
| MCC-03 | **HOLD** | PRESTO/Multi3WOZ repair 很自然，但只是 MCC-10 的一个实例；参数知识编辑的“跨语言传播”叙事也已拥挤 | 并入 MCC-10，作为 slot-replacement setting |
| MCC-04 | **HOLD** | cross-lingual correction、negation 与 belief revision 均邻近；单独写“旧主张未撤回”太宽 | 并入 MCC-10；若 valid→withdrawn 与 value replacement 呈不同 scale law 再拆分 |
| MCC-05 | **KILL** | Findings EMNLP 2025 已直接做 code-mixed reference consistency、layer bottleneck 与 patching | entity count 可作 MCC-01 控制，不单跑 |
| MCC-06 | **HOLD** | multilingual multi-hop/RAG 与 cross-lingual reference 已覆盖宽能力；很可能只是跨语 join 变难 | 只保留 `same QID known + 两个 single-hop 正确 + 仅 attribute union 失败` |
| MCC-07 | **KILL** | CS-Sum 已把 speaker misattribution 列为三大错误并跨多模型量化 | commitment status 转给 MCC-11；speaker attribution 不单跑 |
| MCC-08 | **KILL** | query-language distractor/reranker bias 已被 MRL 2025 与 ACL 2026 直接占位 | authority control可用于 MCC-01，不单跑 |
| MCC-09 | **HOLD** | 与 multilingual instruction following、exception reasoning、UDH-05/08 均重叠；易受条款翻译与工具提示驱动 | 必须同语 exception 正常、跨语 report 正确、action 才恢复 default，并跨两个自然应用 |
| MCC-10 | **PROMOTE** | 静态翻译一致性与 output-language alignment 都不等于动态 state machine 的 path dependence | `两条语言路径 final state 完全相同；每次 update 可复述；current value 随 path/query channel 稳定改变` |
| MCC-11 | **PROMOTE** | 一般 hallucination、meaning shift、speaker error 不包含“命题保留而 evidential status 选择性脱落” | `marker 翻译与 factuality 分类正确；跨语 writer 才把 alleged/forecast/confirmed 压到错误 commitment state` |
| MCC-12 | **KILL** | ACL 2026 已系统做 linguistically grounded code-switch reasoning，早期工作也做 code-switched RuleTaker；自然双语条件样本又稀少 | 可作 MCC-10 的 compositional negative control |
| MCC-13 | **KILL** | NormAd 明确包含“相关当地规范已经给出”仍判断错误；语言切换只是其自然 follow-up 轴 | 不作为独立现象 |
| MCC-14 | **KILL** | ACL 2026 Lost in Execution 已直接得到“语义/工具正确、跨语参数错误”，覆盖范围比 locale 日期更广 | 日期 locale 可作其 benchmark 子类，但不是本项目题目 |

## PROMOTE：成立即可转机制的六个 exact contracts

### P1 — UDH-03：uncertainty-state hysteresis

**自然命题。** 材料最终已经齐全，但模型一旦先说过“不确定”，就难以退出拒答状态。

**最小行为合同。** 对同一原生题形成 `full-at-once`、`partial→missing evidence supplied`、`partial→full restated` 三条路径；最终事实集合逐字或字段级相同。只分析 full-at-once 稳定答对且最终 sufficiency probe 正确的项目。目标差异必须落在 abstain/answer gate，不能只是答案内容错、上下文更长或 assistant 先前文本更近。

**为什么不是母现象。** 一般 abstention 研究改变最终信息充分性；Ask Again 改变 follow-up interaction。这里 final state 相同，且变化方向被“曾经进入 uncertainty state”决定，是 hysteresis 而非平均不一致。

**公共/自然数据。** PubMedQA、MKQA、MedQAbstain 的 answerable/insufficient relation；优先按原文段落或原字段分轮，不生成新事实。专业医疗仅作外部确认，不作为首个 setting。

**两个竞争机制。** A：持久的 dialogue-level abstain state，后续证据已写入但 gate 未 reset；预测删除/替换 assistant 自述仍保持。B：第一轮生成的“不确定”文本产生 self-conditioning；预测隐藏或语义中性的 assistant turn 会消失。可再与 content-length/recency 机制用 final recap control 分开。

**跨规模理由。** instruction tuning 和 safety tuning 会强化稳定拒答/自洽状态，而 evidence reader 随规模改善；因此 reader 正确与 gate 迟滞可能反而更清楚。实际只在小模型有则 KILL。

### P2 — UDH-09：authority–proposition unbinding

**自然命题。** 模型知道一句话来自异议意见，却把这句话写成法院确立的规则。

**最小行为合同。** 只取 majority 与 dissent 在同一争点上有可引用、方向相反命题的真实判决。模型须正确回答 section role、author、stance；最终 holding 错误必须可文本匹配到 dissent proposition。交换顺序、篇幅、引文数量和结尾位置后，错误仍由 dissent/authority 身份而非 salience 决定。

**为什么不是母现象。** CaseHOLD 测 holding 选择；一般 legal hallucination 测错误内容；evolving-authority 工作测法源关系。这里 proposition content 被正确理解，失败发生在 `proposition ↔ institutional authority` binding 的压缩或读取。

**公共/自然数据。** CourtListener/CAP 等公开判决文本与原生 opinion type；CaseHOLD 可筛候选，但 headline set 必须人工核对原判决，不依赖生成模型造相反命题。

**两个竞争机制。** A：摘要压缩时 proposition 与 authority tag 脱绑定；预测 authority-tag activation interchange 可把 holding 搬到另一命题。B：绑定仍在，writer 偏好论证更完整/更可预测的 dissent；预测只在晚层或生成开头干预 proposition salience 有效。

**跨规模理由。** 更大模型可能更能理解 dissent 的论证，因而其内容竞争力变强；authority binding 未必随内容能力同步改善。若错误随模型变大单调消失且无 reader/writer dissociation，降为普通法律能力。

### P3 — UDH-11：inadmissibility mask failure

**自然命题。** 模型知道某项证据法律上不能使用，裁决时却仍被它说服。

**最小行为合同。** 只用真实裁判或专家可核规则中 scope 清楚的 inadmissibility。模型须正确判断 admissibility、适用主体、证据支持哪一方；翻转不可采 evidence 的内容方向应等变翻转 verdict，而等长 irrelevant text 不应。删除不可采 payload 应恢复；仅说“不可采”但不知道它支持谁不算。

**为什么不是母现象。** LegalBench hearsay 只测 evidence category；generic knowledge-use gap 没有法定的“该信息必须被 mask 为零”的可检验 accumulator。这里错误 destination 是被禁止 evidence 的符号方向。

**公共/自然数据。** LegalBench hearsay 用作 reader 筛选；headline set 应来自 CourtListener/CAP 中原判决明确讨论被排除证据及其内容的案件。若只能把一个 hearsay 小题硬拼到虚构 verdict，立即降为 HOLD。

**两个竞争机制。** A：admissibility tag 被表示但没有乘到 evidence accumulator 的 mask；预测中层 evidence-value feature 仍随 payload 改变。B：accumulator 已屏蔽，late answer writer 重新读取鲜明 payload；预测 decision state 正确而最后若干层/answer token 重新偏转。

**跨规模理由。** 内容抽取与法律标签识别都会随规模增强，但硬 mask 需要不同的 learned computation；更强 payload representation 甚至可增大泄漏。若强模型完全归零或只在提示诱导下出现，KILL。

### P4 — MCC-01：translation violates source independence

**自然命题。** 同一篇报道的译文不是第二名证人，但模型可能把它当作第二票。

**最小行为合同。** 三源冲突：一个 canonical source 的 L1 原文与 L2 官方译本支持 A，一个真正独立且同级来源支持 B。模型须正确回答两段是同源译本；把译本加入后，A 的 evidence weight 不应像增加独立来源那样跃迁。必须比较同语复述、同源译文、独立同语来源、独立跨语来源，并交换 query/output language。

**为什么不是母现象。** repetition bias 不要求 provenance 已知；mRAG language bias 研究偏好哪种语言；这里严格测试 `source independence`：语言变化是否使同一 provenance 被拆成两个证据节点。

**公共/自然数据。** 有 document/source ID 的官方多语公告、欧盟/联合国平行发布、Wikinews 或人译 parallel news；claim conflict 来自原始来源或公开 fact-check，不允许生成模型凭空制造“独立证人”。

**两个竞争机制。** A：每种语言建立独立 evidence node，translation_of edge 没参与 vote count；预测跨语 node patch 可改变票数。B：source node 已共享，但 answer accumulator 对 mention-level support 求和；预测 source-identity 表示正确而 aggregation 层仍出现两份 support。

**跨规模理由。** 翻译和 source-identity reader 随规模变好，并不保证 evidence aggregation 学会 provenance independence；更强模型可能把两份流畅证据都抽取得更强。若同语复述同幅生效，则退化为 generic repetition，KILL。

### P5 — MCC-10：language-conditioned state-path dependence

**自然命题。** 当前日程明明一样，只因“怎么用两种语言改到这里”不同，模型记住了不同的现在。

**最小行为合同。** 对同一原生 dialogue slot 建立四条短路径：`L1:A→L2:B`、`L2:A→L1:B`、`L1:B`、`L2:B`。每个 update 与最后值均能被模型正确翻译/复述；最终 state 仍随 path 或 query language 稳定改变。最后一句、token 数、脚本、value familiarity 和 output language 全部平衡。

**为什么不是母现象。** 静态 cross-lingual consistency 比较翻译版本；output-language alignment 看模型用哪种语言回答；一般 code-switch robustness 看平均准确率。这里是同一 final world state 的动态 path independence 被破坏。

**公共/自然数据。** Multi3WOZ 平行 slot、PRESTO repair、公开 task dialogue；只在预约、改期、取消/重订等自然 code-switch 边界做，不逐词随机混语。MCC-03 是 replacement setting，MCC-04 是 validity setting。

**两个竞争机制。** A：语言分区的 slot cache，各语言各自 last-write-wins，query 选择同语 cache。B：统一 state，但不同语言 update 写入强度不同。query-language swap 应只系统搬动 A；B 应主要跟 update language/resource level。

**跨规模理由。** 多语言解码可随规模变强，而 dialogue cache 的组织方式是架构/训练形成的 computation；强 reader 会让“每步都懂、final state 却错”的解离更干净。若只是低资源语言最后一句读不懂，KILL。

### P6 — MCC-11：evidential-status stripping

**自然命题。** “据称工厂关闭”翻译总结后变成“工厂关闭了”：事情被保留，证据状态消失。

**最小行为合同。** factual / alleged / forecast / negated 至少三类，自然文本中的 proposition 尽量 matched。模型必须正确翻译 marker、正确分类 event factuality；只有跨语言 summary/answer commitment 被系统压到更肯定的状态。同语摘要、单纯 factual 事件与只做翻译不做摘要是必要 control。

**为什么不是母现象。** CS-Sum 的 meaning shift/SMA 不区分 proposition 与 evidential metadata；multilingual hallucination看事实错；本卡要求 content identity preserved、status attribute selectively lost，并有多个可命名错误 destination。

**公共/自然数据。** MAVEN-FACT 的 event factuality、带 attribution/hedging 的多语新闻与 X-FACT；目标语版本必须有人译或双人审核。不要把机器翻译漏词当模型机制。

**两个竞争机制。** A：跨语言 conceptual bottleneck 只传 proposition，status feature 在语言桥上消失。B：status 跨语仍可读，目标语言 summarization writer 因风格/压缩把 hedge 去掉。若 target-language factuality probe 在生成前已失败支持 A；若 probe 正常但生成晚层偏转支持 B。

**跨规模理由。** 预训练强烈奖励 proposition alignment，evidential morphology/markers 跨语言不均衡；规模可强化内容保持，却不保证 metadata binding。若错误只是小模型翻译失败，KILL。

## HOLD 的解锁条件

| ID | 现在不跑的原因 | 何时重新进入 smoke queue |
|---|---|---|
| UDH-05 | 医疗安全 benchmark 拥挤、标签/专家成本、generic rule-use 风险 | 先找到两个公开原生 hard-exclusion 数据源，其中一个非医疗；明确被禁 action 是唯一 wrong destination |
| UDH-07 | MedEinst 母现象强、next-test gold 稀缺 | 得到原生或专家标注的 next-information target，且 current diagnosis 已正确 |
| UDH-10 | ordinary meaning / definition 工作多，数据桥不足 | 找到真实 statute-definition-application triples，不自行造 vehicle 类小谜题 |
| UDH-13 | evolving authority 已被 ACL 2026 占位 | 找到自然多次 amendment chain，并把 novelty 收窄为 same-final-state transactional ghost + internal causal localization |
| MCC-03 | 与 MCC-10 重复 | MCC-10 先成立后，将它作为 replacement subtype 扩展 |
| MCC-04 | 与 MCC-10、belief revision 重叠 | MCC-10 成立且 validity update 呈不同 shape/scale law |
| MCC-06 | 很可能只是 multi-hop 难度 | 先在现成 QID/provenance 数据上证明 identity 与 two single-hop 接近 ceiling |
| MCC-09 | instruction/rule-use 重叠且翻译混淆大 | 找到两个自然 bilingual policy/application 数据源；不靠系统 prompt，same-language exception 正常 |

## 合并与验证路由

```text
MCC-03 slot replacement ─┐
                         ├─> MCC-10 dynamic state-path dependence
MCC-04 validity update ──┘

UDH-02 invalidated evidence ──> UDH-11 admissibility/validity mask control
UDH-06 ordinal urgency ───────> UDH-05 veto/decision monotonicity control
UDH-08 explicit exception ────> UDH-05 non-medical hard-rule setting

MCC-02 event count ───────────> MCC-01 downstream count probe
MCC-05 alias count ───────────> MCC-01 identity/provenance negative control
MCC-07 commitment component ──> MCC-11，speaker attribution 本身不再研究
```

建议便宜验证顺序不是按领域，而是按 oracle 成本：

1. `MCC-10`：原生 slot gold、四条短路径、deterministic scorer。
2. `UDH-03`：现有 answerability gold，先筛 full-context 正确项。
3. `MCC-01`：source/translation provenance 确定，需人工核 20–30 条。
4. `MCC-11`：需人译/双人核 evidential marker，先做小而干净的三状态集合。
5. `UDH-09`：真实判例阅读成本高，但无需创造法律规则。
6. `UDH-11`：最后做；必须先找到真实可核的 inadmissibility→decision 材料，否则不要用合成捷径。

每张 PROMOTE 的第一轮都只回答四件事：现象是否存在、是否跨家族、是否跨至少两个尺寸、signature 是否真是指定 wrong destination。第一轮不做大规模曲线、不做 probe、不做 mitigation。只有这四项同时通过，才进入正式 novelty refresh 与机制实验设计。
