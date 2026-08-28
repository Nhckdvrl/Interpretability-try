# 领域 05：话语、语用与沟通

状态：`14 candidate cards — UNTESTED / BRUTALLY AUDITED (1 PROMOTE / 5 HOLD / 8 KILL)`
本文件只建立候选池；**未运行任何模型，也未触碰常驻服务**。
逐卡证据与裁决见 [AUDIT_MTR_DPC.md](audits/AUDIT_MTR_DPC.md)。`PROMOTE` 仅表示行为若跨家族成立便值得进入机制阶段，不表示已经验证。
母问题：模型是否能识别说话者做了什么言语行为，却在建立共同知识、总结立场或采取行动时退回字面句法与被提及命题？

## 领域边界与红线

“LLM 不懂语用”已经被 [PUB](https://aclanthology.org/2024.findings-acl.719/)、[PragmatiCQA](https://aclanthology.org/2023.findings-acl.385/) 等宽评测占据；间接回答有 [CIRCA](https://aclanthology.org/2020.emnlp-main.601/)，假预设有 [CREPE](https://aclanthology.org/2023.acl-long.583/) 与 FalseQA，修辞问句已有 EMNLP 2025 [SRAQ](https://aclanthology.org/2025.emnlp-main.1553/) 和 ACL 2026 [representation study](https://aclanthology.org/2026.acl-long.5/)，讽刺甚至已有 ACL 2026 Findings 的 [intent–irony decoupling](https://aclanthology.org/2026.findings-acl.962/)。

因此不能以 detection accuracy 作为现象。候选必须包含一个**被正确识别的 pragmatic act 与错误下游用途之间的决定性分离**：

```text
recognize rejection → nevertheless write rejected proposition into common ground
recognize indirect answer → nevertheless act on its literal excuse
recognize sarcasm → nevertheless treat literal praise as speaker belief
recognize rhetorical question → nevertheless wait for missing information
recognize canceled implicature → nevertheless use the canceled inference
recognize acknowledgment → nevertheless summarize it as agreement
```

## 优先公共数据架

| 数据/来源 | 原生对象 | 适合候选 | 可得性 |
|---|---|---|---|
| [PUB](https://aclanthology.org/2024.findings-acl.719/) | implicature、presupposition、deixis、reference 共 14 任务 | 宽 collision control | Anthology data/code |
| [PragmatiCQA](https://aclanthology.org/2023.findings-acl.385/) | 开放域对话的隐含意图与心理状态 | DPC-03/04/13 | 官方数据公开 |
| [CIRCA](https://aclanthology.org/2020.emnlp-main.601/) / [FRIENDS-QIA](https://aclanthology.org/2021.codi-main.1/) | 间接 yes/no、条件式与不确定回答 | DPC-03/13 | 公开 |
| [SRAQ](https://aclanthology.org/2025.emnlp-main.1553/) / [Rhetorical Questions in LLM Representations](https://aclanthology.org/2026.acl-long.5/) | 语境决定的修辞/信息问句 | DPC-06 | 数据/附件公开 |
| [SocKET](https://aclanthology.org/2023.emnlp-main.699/) / [FLUTE](https://aclanthology.org/2022.emnlp-main.481/) | sarcasm、讽刺与 figurative NLI | DPC-05 | 公开 |
| [SIGA](https://aclanthology.org/2024.lrec-main.1288/) | C4 自然文本中的 scalar implicature | DPC-07 | 官方 GitHub 公开 |
| [NOPE](https://aclanthology.org/2021.conll-1.28/) / IMPPRES | 自然预设与投射/取消 | DPC-09/12 | 公开 |
| [CREPE](https://aclanthology.org/2023.acl-long.583/) / [FalseQA](https://aclanthology.org/2023.acl-long.309/) | 自然假预设及其纠正/解释 | DPC-09 | 官方数据公开 |
| [REPAIR-QA](https://aclanthology.org/2023.sigdial-1.52/) / [GrounDialog](https://aclanthology.org/2023.bea-1.26/) | misunderstandings、repair、grounding | DPC-01/08/12 | 公开 |
| [Frame of Reference](https://aclanthology.org/2026.findings-acl.1645/) | 对话共同知识与关系指称 | DPC-01/02/08 | 论文 benchmark 公开 |
| [PDTB](https://catalog.ldc.upenn.edu/LDC2019T05) / [ChangeMyView concessions](https://aclanthology.org/2018.dnd-9.4/) | concession、contrast 与论证立场 | DPC-10/11 | PDTB 需 LDC；CMV 派生数据公开 |
| [SAD](https://aclanthology.org/2026.acl-long.1673/) | 大规模 CMV 策略与立场标注 | DPC-08/11/14 | 官方论文/数据 |
| [TEACh dialog acts](https://aclanthology.org/2022.sigdial-1.13/) | situated task dialogue acts 与非语言行动 | DPC-04/08 | 公开 |

---

## DPC-01 — 被明确否定的说法仍进入共同知识

`stage: IDEA | audit: HOLD | priority: A | naturalness: N3 | source: GrounDialog/Frame-of-Reference | collision: HIGH`

**一句话矛盾。** 模型会解释“不是红门，是蓝门”否定了红门，稍后协作时却仍把红门当双方都接受的候选。

**日常例子与数据。** 对话中 A 提议或猜测 P，B 明确拒绝并给出 Q；GrounDialog 的 repair/grounding 与 Frame of Reference 的 situated dialogues 提供自然拒绝、确认和后续指称。

**发现轴与晋级 signature。** 先问 `A proposed what / B accepted what / common ground now contains what`，再做后续 referential choice。只有 rejection 与 Q 都识别正确，P 却在共同知识查询或行动中复活；`proposal / rejection / correction / acknowledgment` 形成不同 update signature。

**规模与机制。** 大模型更完整保存 utterance content，但 common-ground writer 必须对 discourse act 做有符号更新。A：提及即写入；B：rejection tag形成但后续 reference retriever忽略 polarity/source。

**最近工作与空位。** Frame of Reference 已直接研究 established common ground，Belief-R/negation工作也近。只有 **rejection act intact / rejected content selectively remains shared** 且超出 reference retrieval accuracy 才保留。

**最便宜的证伪。** 抽 20 个明确 `No, Q` 的原生对话；若 common-ground问答本身也错，或任何被提及对象都同样干扰，KILL。

## DPC-02 — 私下分别告诉每个人，不等于公开宣布

`stage: ROUTE | audit: KILL-ROUTE | priority: A | naturalness: N3 | source: multi-party dialogue/ToM | collision: OCCUPIED`

**一句话矛盾。** 每个人都知道消息，并不自动意味着每个人都知道其他人也知道。

**日常例子与数据。** 老师分别私信每位学生“考试取消”，与在全班群公开宣布具有同样的一阶知识，却不同于共同知识。可从 multi-party dialogue、FANToM/OpenToM 信息接触轨迹筛选，并只做自然 `public channel vs separate private messages` 配对。

**发现轴与晋级 signature。** 一阶 knowledge 对两条件相同；二阶/共同知识、协调行动不同。模型必须正确回答每个人都知道，只有 private condition 错当 common knowledge；不能退化成“某人没看见消息”。

**规模与机制。** 规模改善 agent-specific knowledge，common-knowledge closure 是独立递归 computation。A：channel visibility 未编码；B：可见性正确，但 group-state writer 把 unanimous first-order knowledge 压成 public fact。

**最近工作与空位。** ToM 与 common-ground benchmark 很拥挤；本卡更适合路由至 social/collective 文档。若已有工作覆盖 public-vs-private decisive contrast 与机制，则 OCCUPIED。

**最便宜的证伪。** 先查 FANToM/OpenToM 是否有原生 multi-recipient channels，再做 12 个极短自然场景。若二阶题地板太低或只有单一 wording 生效，KILL。

## DPC-03 — 间接回答已经听懂，行动仍按字面理由走

`stage: IDEA | audit: HOLD | priority: A | naturalness: N3 | source: CIRCA/FRIENDS-QIA | collision: HIGH`

**一句话矛盾。** 模型知道“我明早六点要起床”是在婉拒晚间邀约，安排日程时却仍把对方列为参加。

**日常例子与数据。** CIRCA/FRIENDS-QIA 有自然 indirect yes/no、conditional 与 uncertainty labels；给 indirect answer 后分别问 pragmatic answer、literal fact、RSVP/action state。

**发现轴与晋级 signature。** `direct no / indirect no / literal-only same sentence / uncertain answer`；pragmatic label正确而 action与 direct-no 不同，且错误不是对不确定回答合理保守处理。

**规模与机制。** 强模型能读懂 implicature，但 task-state writer常依赖显式 yes/no token。A：implicit answer未形成稳定 state；B：形成了，但 action compiler只读 surface polarity/slot。

**最近工作与空位。** CIRCA、PUB、PragmatiCQA 已覆盖理解；空位是 **indirect-answer classification intact / deterministic dialogue-state action wrong**，不是再做分类 benchmark。

**最便宜的证伪。** 每类抽 20 个高一致度 CIRCA 样本，先问 label 再输出 RSVP JSON。若 label与 action 同步，或 effect只来自 ambiguous items，KILL。

## DPC-04 — 间接请求已经识别，回复仍只回答字面问题

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: PragmatiCQA/TEACh | collision: OCCUPIED`

**一句话矛盾。** 模型会说“你能把窗关上吗？”是在请求关窗，作为助手却只回答“能”。

**日常例子与数据。** PragmatiCQA 的 indirect intent、TEACh 的 situated dialogue acts 与后续非语言动作；匹配 direct request、conventional indirect request、真正 capability question。

**发现轴与晋级 signature。** intent classification 和可执行性均正确，但 response/action 落到 literal answer；交换动词和礼貌程度后错误跟随 interrogative form 而非 intent。

**规模与机制。** instruction tuning提升意图识别，也可能强化问句—答案模板；二者竞争。A：speech-act representation不足；B：representation存在，response router被 question-answer path晚层覆盖。

**最近工作与空位。** PragmatiCQA 已以“Do you have a minute?”为典型，TEACh 已用 dialogue acts指导行为。只有跨数据的 **intent correct/action literal** 与因果路由才有空位；否则高碰撞。

**最便宜的证伪。** 20 个自然、无安全/能力障碍的 indirect requests；若模型默认都会执行或主动澄清，KILL。

## DPC-05 — 讽刺已经识别，字面赞美仍被当成说话者信念

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: SocKET/FLUTE | collision: EXACT-NEAR-OCCUPIED`

**一句话矛盾。** 模型正确说“真是天才操作”是在讽刺，稍后总结立场却写成说话者赞扬该操作。

**日常例子与数据。** SocKET/FLUTE/Reactive Supervision 的 natural sarcasm，加后续 stance、belief 与 recommendation readout；direct praise、direct criticism 与 sarcastic praise为三格。

**发现轴与晋级 signature。** sarcasm label、intended sentiment正确，只有 speaker-belief或行动沿 literal polarity；换说话者和被评价对象后错误等变。

**规模与机制。** 字面 proposition 与 pragmatic inversion可能同时保留，规模增强两者但不保证下游选路。A：inversion只停在分类 token；B：belief state正确，summary writer受正向词汇吸引。

**最近工作与空位。** ACL 2026 Findings [Decision Biases and Intent-Irony Decoupling](https://aclanthology.org/2026.findings-acl.962/) 已非常接近，且发现 subsidiary inference与holistic irony judgment分离。本卡只有在**正确 holistic irony judgment之后，字面命题进入独立 belief/action state**才可能不被覆盖；正式审计前不优先。

**最便宜的证伪。** 抽 20 个标注明确样本，要求 detection→stance JSON→downstream choice。若 stance已正确且下游也正常，KILL；若 detection就错，撞车。

## DPC-06 — 修辞问句已经识别，系统仍把它当待回答的信息缺口

`stage: IDEA | audit: KILL | priority: B | naturalness: N3 | source: SRAQ/RQ corpora | collision: OCCUPIED`

**一句话矛盾。** 模型知道“难道这还不明显吗？”是在强调立场，却在对话状态中标记成用户等待一个事实答案。

**日常例子与数据。** SRAQ 的 context-conditioned ambiguous questions、Twitter/debate forum rhetorical-question corpora；测 rhetorical label、entailed stance、dialogue next act和open-question ledger。

**发现轴与晋级 signature。** 同一 question surface 在 rhetorical/informational contexts下切换；label与stance正确，但 only rhetorical condition错误地创建 unresolved QUD 或请求澄清。

**规模与机制。** ACL 2026 已显示 RQ representation 多方向、跨数据不统一；这反而允许测试哪种方向被 QUD updater使用。A：rhetorical representation弱；B：存在，但 question syntax触发 open-slot writer。

**最近工作与空位。** SRAQ做识别，ACL 2026主会已做representation。空位只剩 **representation/label intact → QUD state/action wrong** 的因果机制；仅做 probe 完全撞车。

**最便宜的证伪。** 20 对 SRAQ matched contexts，输出 `needs_answer` 与下一动作。若label正确时 ledger也总正确，KILL。

## DPC-07 — “有些——事实上全部”之后，已取消的“并非全部”仍在

`stage: IDEA | audit: KILL | priority: A | naturalness: N3 | source: SIGA/natural corpora | collision: EXACT-OCCUPIED`

**一句话矛盾。** 模型知道说话者后来明确了“全部”，却在后续推理中继续使用“不是全部”这一已取消的会话含义。

**日常例子与数据。** “Some of the files—indeed, all of them—were corrupted.” 字面上 `some` 与 `all`兼容，`not all`只是可取消 implicature。SIGA提供自然 scalar items；从 C4/新闻中再筛选 self-strengthening/cancellation句。

**发现轴与晋级 signature。** 先测 literal entailment、scalar implicature、cancellation recognition，再问是否存在未损坏文件或做 count bounds。晋级要求前三项正确，但下游仍导出 `not all`；`some only / some, perhaps all / some, in fact all / all` 是自然梯度。

**规模与机制。** 大模型更会生成默认 implicature，也更会理解 correction；默认推断可能早写入而 cancellation只在表面解释层生效。A：implicature不可逆写入；B：已取消但 NLI/decision reader偏好初始 scalar state。

**最近工作与空位。** SIGA、PUB 与 scalar-implicature研究已占理解/生成。独特性是**cancellation recognized / canceled inference reused**，不是“模型是否产生 some→not all”。

**最便宜的证伪。** 先从自然语料找至少 30 条非模板 cancellation，并人工双人核验。若只能靠重复构造句或模型对 cancellation直接判断错误，KILL。

## DPC-08 — “听到了”被总结成“同意了”

`stage: IDEA | audit: HOLD-MERGE-DPC11 | priority: A | naturalness: N3 | source: CMV/SAD/dialogue acts | collision: MEDIUM-HIGH`

**一句话矛盾。** 模型会解释“I see your point”只是 acknowledgment，最后却总结为双方已经达成一致。

**日常例子与数据。** 辩论、客服和协商中，理解/确认收到并不等于接受。SAD 与 ChangeMyView 含立场和 concession，GrounDialog/通用 dialogue-act corpora含 acknowledgment、agreement、disagreement。

**发现轴与晋级 signature。** `bare acknowledgment / acknowledgment+but disagreement / explicit agreement / no response`；先问 dialogue act与speaker stance，再问 common ground/consensus。只有 act与stance正确、consensus错误才晋级。

**规模与机制。** helpful dialogue training偏好和谐收束，可能把 grounding success映射为 social agreement。A：acknowledgment与agreement共用低维方向；B：方向可分，但 conversation summarizer有consensus prior。

**最近工作与空位。** stance、dialogue-act与CMV persuasion工作多，但当前检索未见主会工作完整覆盖 **acknowledgment recognized / agreement state falsely written / causal route**。截至 2026-08-28 只能标 LOW-MEDIUM，不能声称新颖。

**最便宜的证伪。** 从 CMV/SAD 抽 30 个带后续明确立场的 acknowledgment turns。若 act分类本身不稳定，或总结错误只是遗漏 later disagreement，KILL。

## DPC-09 — 假前提已经驳回，后续解释仍沿用它的因果框架

`stage: IDEA | audit: HOLD | priority: A | naturalness=N3 | source: CREPE/FalseQA | collision: HIGH`

**一句话矛盾。** 模型正确回答“Lee并没有偷车”，继续解释事件时却仍推断他有逃跑动机或赃物。

**日常例子与数据。** CREPE含自然 information-seeking false presuppositions及corrections；FalseQA含人工 FPQ、解释和修正版问题。把 rebuttal 与一个需要该前提才成立的下游因果/人物状态问题配对。

**发现轴与晋级 signature。** `true premise / false premise unrebutted / false premise explicitly rebutted / corrected question`；模型必须检测并纠正假前提，只有 downstream consequences 保留原 frame。

**规模与机制。** rebuttal模块可调用参数知识，问题frame在后续生成中仍提供事件schema。A：presupposed event已实例化；B：事件标false，但因果completion忽略factuality gate。

**最近工作与空位。** CREPE与FalseQA已做 detect/rebuttal，BWA-08做 denial-as-evidence。空位是 **successful rebuttal followed by structured causal residue**；若只是第一问被误导，完全占领。

**最便宜的证伪。** 20个CREPE高一致度样本，每例只加一个人类可判的必需后果问句。若rebuttal后后果均归零，KILL；若rebuttal本身失败，不推进。

## DPC-10 — “虽然 P，但是 Q”中，被让步的 P 压过了主结论 Q

`stage: IDEA | audit: KILL | priority: B | naturalness=N3 | source: PDTB/CMV | collision: FATAL-CONSTRUCT`

**一句话矛盾。** 模型知道作者最终主张 Q，却在摘要或决策里按被让步的 P 行动。

**日常例子与数据。** “虽然方案便宜，但安全风险不可接受。”最终决策应受风险否决，而非因“便宜”批准。PDTB concession/contrast、CMV argumentative concessions与政策文本可提供自然样本。

**发现轴与晋级 signature。** 先问 relation、作者主结论与 P/Q truth commitment，再做 recommendation；交换 clause order、`although/but/despite` 和同内容 plain conjunction。只有 nucleus识别正确但 action稳定跟 satellite 才晋级。

**规模与机制。** 两命题都真实且可用，问题是 discourse salience与decision gate。A：nucleus/satellite未形成；B：形成，但 lexical utility或first-clause path控制 action。

**最近工作与空位。** discourse relation classification与concession persuasion成熟；若只是 relation识别错误，撞车。空位是 **relation+nucleus correct / action follows concession**。

**最便宜的证伪。** 从PDTB/CMV人工筛20个后果明确样本；若建议本来允许trade-off、gold不唯一，直接KILL该例，不用LLM judge硬判。

## DPC-11 — “我同意这一点”被扩张成同意整套观点

`stage: IDEA | audit: PROMOTE-UNTESTED | priority: A | naturalness=N3 | source: CMV/SAD | collision: MEDIUM-HIGH`

**一句话矛盾。** 模型能指出说话者只承认一个局部事实，却总结成他接受了对方的总体结论。

**日常例子与数据。** “我同意成本会上升，但仍支持这项政策。”局部 concession不等于 stance flip。CMV/SAD有多轮立场与argument strategy，CMV concession annotations可定位局部承认。

**发现轴与晋级 signature。** `local premise agreement × global conclusion agree/disagree` 四格；先抽取agreement target与global stance，再总结是否改观。必须出现 target binding正确、global stance仍被局部“agree”词覆盖。

**规模与机制。** 强模型会更好提取论元，却可能因RLHF的共识偏好过度扩大agreement scope。A：scope binding错误；B：binding正确，summary writer把positive dialogue act广播到speaker-level stance。

**最近工作与空位。** CMV stance/persuasion与SAD已广，但主要研究策略与预测；当前可辩护空位是 **agreement target intact / speaker-level commitment overgeneralized** 的绑定机制。

**最便宜的证伪。** 抽30个后文明确重申总体立场的natural cases。若局部target extraction也错，或只有含“agree”单词才触发且paraphrase消失，KILL。

## DPC-12 — 预设已经明确取消，人物档案仍保留它

`stage: ROUTE | audit: KILL-DUPLICATE | priority: B | naturalness=N3 | source: NOPE/IMPPRES | collision: OCCUPIED`

**一句话矛盾。** 模型知道“如果她有孩子，她会接孩子；事实上她没有孩子”取消了有孩子的预设，随后人物摘要仍写她有孩子。

**日常例子与数据。** NOPE自然预设、IMPPRES controls，分别测试 trigger、projection、cancellation、persona summary。

**晋级 signature。** cancellation判断正确但presupposed entity/event进入summary或后续reference；不能只是自然语句本身scope含混。

**规模与机制。** presupposition常以默认common-ground write实现，取消可能只加negative tag。A：accommodation不可逆；B：已标canceled，下游persona writer不过滤。

**最近工作与空位。** 这是 [BWA-09](02_BELIEF_WORLDS_ATTITUDES.md#bwa-09--被取消的预设仍留在人物档案里) 的路由；NOPE/IMPPRES已覆盖projection判断，generic unring-bell也近，不另立重复题。

**最便宜的证伪。** 先复用NOPE cancellation items做判断→summary；若判断错，不是目标现象。

## DPC-13 — 条件式答应被压成无条件答应

`stage: IDEA | audit: HOLD | priority: B | naturalness=N3 | source: CIRCA/FRIENDS-QIA | collision: HIGH`

**一句话矛盾。** 模型知道“如果能提前下班，我就来”只是有条件的 yes，名单里却把此人标成确定参加。

**日常例子与数据。** CIRCA标注 `yes, subject to some conditions`、probably yes/no 与 middle；后续生成 RSVP state、capacity count或是否需要follow-up。

**发现轴与晋级 signature。** pragmatic label正确，但 structured state从conditional/uncertain坍缩到yes；direct yes/no与conditional content controls齐全。最好 action不确定性也消失，而模型自身confidence仍高。

**规模与机制。** task systems偏好闭合slot，writer可能拒绝保留三值/条件状态。A：semantic state已binary化；B：多值state存在，schema/decoder强制映射到yes。

**最近工作与空位。** CIRCA本身已定义并预测细粒度标签，UQ/abstention也拥挤。只有**label correct → downstream binary state collapse**和schema-independent机制才保留。

**最便宜的证伪。** 用CIRCA高agreement conditional items输出自由文本与三值JSON。若仅binary schema下出错，属于interface artifact，KILL。

## DPC-14 — 引用对方的话被总结成自己承诺了该命题

`stage: ROUTE | audit: KILL-DUPLICATE | priority: B | naturalness=N3 | source: QuoteBank/news/dialogue | collision: OCCUPIED`

**一句话矛盾。** 模型正确知道“安全无虞”是公司发言人的说法，却把记者或回应者写成认可该说法。

**日常例子与数据。** QuoteBank、新闻fact-check与SAD/CMV中的quote-reply结构；测 attribution、speaker commitment、document commitment和summary。

**晋级 signature。** attribution正确、report verb force正确，只有 narrator/responder commitment错；`said/claimed/confirmed/denied`应有结构梯度。

**规模与机制。** quote payload比source tag更易进入summary；A：source binding丢失；B：binding正确但truth-oriented writer只取payload。

**最近工作与空位。** 这是 [BWA-01](02_BELIEF_WORLDS_ATTITUDES.md#bwa-01--会归因引语却把引语当作者自己的话) 的路由，不另建题。quotation/source工作已多，必须做commitment-specific因果路径。

**最便宜的证伪。** 20条真实引语，先attribution再document stance；若 attribution一错全错，KILL。

## 审计后验证队列与停止清单

| 顺位 | 卡 | 裁决 | 只有什么结果才晋级 | 最大风险 |
|---:|---|---|---|---|
| 1 | DPC-11 local agreement→global stance | PROMOTE-UNTESTED | agreement target 与 global stance 都对，summary/action 仍产生 stance flip；自然 paraphrase 后保留 | 不能只是 stance extraction 错或词面 `agree` priming |
| 2 | DPC-08 acknowledgment→agreement | HOLD / merge into DPC-11 | 只用后文明确 disagreement 的 acknowledgment；作为 commitment-scope control | 裸 acknowledgment 的 gold 有语用歧义 |
| 3 | DPC-01 rejection→common-ground write | HOLD / control | rejection/Q/common-ground components 均正确，只复活被拒命题 | common-ground benchmark 已很近 |
| 4 | DPC-03 indirect answer→wrong action | HOLD | free text、三值 state 与真实行动都同错，且 label 正确 | indirect-speech representation 已占；schema artifact |
| 5 | DPC-09 rebuttal→causal residue | HOLD | 真实数据原生带确定 downstream consequence | false-premise QA 拥挤；问题常需人为构造 |
| 6 | DPC-13 conditional yes→unconditional | HOLD | 自由文本也删除条件，不依赖 binary schema | CIRCA 已定义条件标签 |

**停止投入：** DPC-02/04/05/06/07/10/12/14。特别是 DPC-07 已被 2026-07 的 implicature recognition-and-cancellation 数据与评测直接占据；DPC-04/05/06 已各有表征/机制近邻；DPC-10 缺少唯一的行动 gold。

---

## Batch-2 脑暴死亡回填（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Imperfective completion / imperfective paradox** | `KILL-EXACT` | ACL 2026 已有 *The Imperfective Paradox in Large Language Models*，且进入 Outstanding Paper 名单；不能再以“进行中事件被当成已完成”作为新的 behavior discovery。 |
| **Presupposition projection / existential presupposition（宽版本）** | `KILL/OCCUPIED` | ACL Findings 2025、LREC 2026、CoNLL 2026 已从 presupposition judgments、existential presupposition、conditionals/reasoning 多侧直接研究；本文件 DPC-09/12 也已有历史路由。 |
| **Scalar implicature cancellation** | `KILL-EXACT/NEAR-EXACT` | 2026 已有 implicature recognition/cancellation 直接工作；本文件 DPC-07 已明确停止投入，不能再换 `some→all`、cancelled inference 等名字重开。 |

**禁止复活。** imperfective、presupposition、scalar-cancellation 若要回来，只能是用户明确授权的机制 follow-up，并必须承认行为母题已占；不得再以“下游 summary/action 不同”单靠 readout replacement 重新宣称行为 novelty。
