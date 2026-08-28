# 领域 06：社会证据、共同知识与集体状态

状态：`12 candidate cards — AUDITED 2026-08-28 · 4 PROMOTE-TO-PILOT / 2 HOLD / 6 KILL-or-ROUTE · UNTESTED`
文献审计：[SEC / KRE 候选的残酷论文可用性审计](audits/AUDIT_SEC_KRE.md)
母问题：模型是否把“某人知道”“大家各自知道”“大家知道彼此知道”“某人公开表态”“群体作出决定”压成同一个模糊的 social state？

## 领域边界

这个领域不能再写成“多数说几次，模型就信了”。[Whose Facts Win?](https://aclanthology.org/2026.acl-long.1357/) 已跨 13 个开源模型研究来源类型、可信度和重复；[GroupQA](https://aclanthology.org/2026.findings-acl.2003/) 已显示释义重复可比独立支持更有说服力；本仓库也已有 [Lineage–Weight Dissociation](../candidates/lineage_weight_dissociation.md)。普通 ToM 又已被 [FANToM](https://aclanthology.org/2023.emnlp-main.890/) 和 ACL 2026 的 [Social World Models](https://aclanthology.org/2026.acl-long.1735/) 大量覆盖。

因此只保留以下更细、但概念上更基础的裂缝：

```text
individual knowledge ≠ common knowledge
message delivery ≠ uptake
public stance ≠ private belief
institutional commitment ≠ every member's belief
mention / question / silence ≠ endorsement
first-hand observation ≠ hearsay
group decision ≠ unanimity
descriptive regularity ≠ normative permission
```

最强 signature 不是 social QA 准确率低，而是：模型正确报告了人物、传播路径或社会状态，协调、证据加权或行动却稳定读取了另一个可命名的状态。

## 优先数据架

| 数据 | 自然单元与 gold | 适合轴 | 可得性 |
|---|---|---|---|
| [FANToM](https://aclanthology.org/2023.emnlp-main.890/) | 多人对话、加入/离开、角色可见信息 | 一阶/高阶信念、公开/私下传播 | 公开 |
| [Reflect](https://aclanthology.org/2022.emnlp-main.714/) | 带共同语境标注的对话与人写回复 | shared ground / private inference | 公开 |
| [RumourEval](https://aclanthology.org/S19-2147/) / PHEME | 真实谣言线程、support/deny/query/comment、veracity | 立场、传闻链、修正 | 公开；平台文本依许可 |
| [QuoteBank](https://figshare.com/articles/dataset/Quotebank_A_Repository_of_Attributed_Quotations_from_News/14184808) | 新闻引语、speaker attribution | 公开言论、机构/成员、转述 | 公开 |
| [NormBank](https://aclanthology.org/2023.acl-long.429/) | 155k 情境化社会规范 | 描述/规范、角色、例外 | 公开，CC BY-SA 4.0 |
| AMI / ICSI / MeetingBank / Molweni | 多人会议或聊天、speaker/turn/discourse | 沉默、确认、共同承诺 | 公开或研究许可 |
| Convote / 公开议会 roll-call + 新闻 | 发言、群体表决、成员票 | collective / distributive | 公开 |
| ExpertQA / PubMedQA / Qasper | 问题、领域来源、作者/文档 | prestige / topical expertise | 公开 |
| PolitiFact / LIAR-PLUS / PrimeFacts | claim、speaker、证据与 verdict | 利益冲突、撤回、来源关系 | 公开或按网站条款 |

---

## SEC-01 — 所有人分别知道，不等于成为共同知识

`priority=A · stage=PROMOTE-TO-PILOT · naturalness=N3 · source_status=HUB · collision_risk=HIGH`

**审计结论。** PROMOTE-TO-PILOT；只验证 matched first-order knowledge 下 public-event 对自然协调行动的选择性影响，禁止退回普通高阶 ToM 谜题。

**一句话矛盾。** 模型知道每个人都收到了同一消息，却预测私下逐一告知和当众宣布会产生同样的协调行为。

**日常例子。** 活动取消若在全员会上宣布，人人不只知道取消，还知道别人也知道；分别私信每个人并不自动产生这种共同知识。

**自然数据与轴。** 以 FANToM 的多人加入/离开对话、Reflect 的 shared-ground 对话和会议通知为母文本；只保留原生公开 utterance、私聊/缺席片段，必要的原则性补充是 `public channel / identical private messages / private messages with delivery receipts`。先问每人的一阶知识，再问二阶知识和必须依赖协调的下一行动。

**晋级 signature。** 两条件下一阶知识均正确，传播方式也报告正确；只有 public/private 对协调或高阶 belief 的影响消失、倒置或在人数增加时出现 cliff。若只是普通二阶 ToM 不会，KILL。

**规模与机制。** 一阶事实提取会随规模提高，而共同知识要求把传播事件绑定到“所有人看见所有人看见”的公共事件节点。机制 A：为每人写入独立 belief slot，却不创建 public-event operator；B：operator 存在，但 coordination reader只聚合一阶 beliefs。

**最近工作与空位。** FANToM 测信息不对称，Reflect 测 common-ground response，Social World Models 测 ToM/语用共享机制；尚不能据此声称它们已覆盖 **matched first-order knowledge + publicness-specific coordination gap**。只有该解离成立，本卡才摆脱普通 ToM。

**最便宜证伪。** 先人工审核 24 个自然多人片段，每片 public/private matched pair；若强模型连传播条件都不稳定识别，或协调差异完全由“公开/私下”关键词提示驱动，KILL。

## SEC-02 — 送达、打开、阅读和理解被压成“知道”

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；只有原生通信日志上出现稳定 `delivered→known` 行动边界、且显式状态表不能修复时复活。

**一句话矛盾。** 模型能复述消息只“已送达、未读”，推断人物行为时却当作对方已经知道内容。

**日常例子。** 邮件进了收件箱，不等于收件人已经看见；已打开也不保证理解或相信。

**自然数据与轴。** 从公开客服/协作对话、ToolSandbox/AppWorld 通讯日志、邮件状态机和多人聊天中抽取真实 `sent / delivered / opened / read / acknowledged / acted` 轨迹；gold 来自事件日志而不是语言模型。先问传输状态，再问人物知识、预期回应和是否应升级提醒。

**晋级 signature。** transport-state classification 正确，只有 mental-state/action readout 在 delivered→known 处跳变；`read but misunderstood` 和 `read and acknowledged` controls 正常。若一句“对方没看”即可完全修复，且自由文本状态本来含混，KILL。

**规模与机制。** 更强模型更会解析状态日志，但训练语料常把“发给了 X”作为 X 后续反应的前兆。机制 A：message payload 在 mention 时直接写入 recipient belief；B：delivery tag保留，人物模拟器忽略 access gate。

**最近工作与空位。** ToM access tasks 多操纵人物是否在场，agent 状态论文多操纵工具成功与否；本卡只在 **通信层状态读对 / epistemic access 用错** 时有独立性。

**最便宜证伪。** 先用 20 条公开状态日志和 4 个原生阶段，不写劝导式 system prompt；若错误只出现在不自然的“delivered”模板或随显式状态表消失，KILL。

## SEC-03 — 私下意见一致，被误当成大家都知道已达成共识

`priority=C · stage=KILL · naturalness=N3 · source_status=HUB · collision_risk=OCCUPIED`

**审计结论。** KILL；2026 的 *Everyone Conforms, No One Believes* 已跨模型直接研究 pluralistic ignorance、公私分离与 cascade。

**一句话矛盾。** 模型正确知道每个人私下都支持方案，却认为每个人也知道其他人支持，从而抹掉 pluralistic ignorance。

**日常例子与数据。** 五名员工都私下反对加班，却各自以为别人赞成；真实私好已一致，感知到的群体规范仍可能相反。

**自然数据与轴。** FANToM/Reflect 的 private disclosures、匿名调查与公开会议材料；从公开 survey + discussion 数据构造“private response / public response / belief about group”三列，禁止凭空写人格。分别问真实意见分布、人物对分布的看法、公开行为和协调预测。

**晋级 signature。** 私人 beliefs 与公开 statements 均逐人答对，却把真实分布直接复制成每个人的 higher-order belief；增加一条公开但非代表性发言出现结构化 sign reversal。若只是把某个人立场记错，KILL。

**规模与机制。** 人物状态可逐个正确，却可能在回答“大家怎么看大家”时调用全局 summary。机制 A：group-summary token覆盖 individual meta-beliefs；B：meta-beliefs可解码，但 query router误选 omniscient narrator state。

**最近工作与空位。** FANToM 已强占普通高阶信念；本卡必须展示 **private-belief matrix intact / perceived-norm matrix collapsed**，并以自然群体决策为外部 setting。

**最便宜证伪。** 先在 FANToM 片段上人工派生 24 个不需新事实的问题；若 direct belief 与 meta-belief 同时失败或无跨片段一致错误落点，KILL。

## SEC-04 — 提问或围观被算成支持

`priority=A · stage=PROMOTE-TO-PILOT · naturalness=N3 · source_status=REMOTE · collision_risk=MEDIUM`

**审计结论。** PROMOTE-TO-PILOT；必须是逐条 stance 判对、聚合时 query/comment 因 claim payload 被正计数的双解离。

**一句话矛盾。** 模型能把回复标成“提问”或“无立场评论”，汇总群体证据时却把它们算成对原帖的赞同。

**日常例子。** “真的吗？有来源吗？”重复了传闻内容，但不是支持传闻。

**自然数据与轴。** RumourEval/PHEME 直接提供 `support / deny / query / comment` 人工标签和线程 veracity；保持原帖和回复原文，比较逐条 stance 分类、support count、群体立场 summary 与最终 veracity。控制回复长度、词汇重叠和线程位置。

**晋级 signature。** stance probe 对 query/comment 正确，但 aggregate support 或 verdict 随 query/comment 数量单调偏向原帖；错误强度更跟“重复 claim token”而非 stance 标签。若 stance 本身错，降为普通 rumor classification。

**规模与机制。** 强模型更会识别疑问语用，却也更能从回复中恢复完整 claim payload。机制 A：evidence aggregator只取 proposition、不取 stance sign；B：stance sign存在，但高词汇重叠激活重复/熟悉度路径。

**最近工作与空位。** RumourEval 工作联合预测 stance/veracity，GroupQA 已占重复说服；可辩护空位是 **同一模型 stance recognition 完整，但 query/comment 在群体聚合中被正计数** 的因果 dissociation。

**最便宜证伪。** 从原 dev/test 各抽 30 个 query/comment 丰富线程；若加入回复并不系统改变 support count/verdict，或效果等同任意长 distractor，KILL。

## SEC-05 — 听说和亲眼看见被赋予同样证据身份

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=REMOTE · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；作为 Lineage–Weight Dissociation 的 firsthand/hearsay 自然复现路由保留。

**一句话矛盾。** 模型能指出某人只是转述别人，却在证据加权时把转述者当作第二名独立目击者。

**日常例子。** Bob 说“我听 Alice 说车是红的”并没有在 Alice 的观察之外新增一次独立观察。

**自然数据与轴。** PHEME/RumourEval 的回复树、QuoteBank 的嵌套归因、PrimeFacts/PolitiFact 的引用链接；抽取原生 `I saw / X told me / according to X / outlet cites source`。分别测 event content、speaker、information source、独立观察数与 belief/action。

**晋级 signature。** hearsay relation与源头都回答正确，但证据数或最终 belief 把 relay 节点当新观察；firsthand↔hearsay 内容交换后错误跟传播角色移动。若只是不懂 reportive language，KILL。

**规模与机制。** 规模改善嵌套 attribution，却不保证 evidence graph 做 ancestor deduplication。机制 A：每个 speaker mention新建 evidence node；B：provenance edge在中层可解码，late aggregator按 speaker数加权。

**最近工作与空位。** Whose Facts Win、GroupQA 和 CAMA 占据来源/重复母现象；本卡只有 **firsthand–hearsay role recognition / independent-observation use** 的 matched 解离才独立，否则路由到 SEC-11。

**最便宜证伪。** 先抽 20 条一跳、20 条两跳自然引语链；若 source-of-information 问题低于可用水平，或决策不随 relay 数变化，KILL。

## SEC-06 — 源头撤回了，传播链仍像原证词有效

`priority=A · stage=PROMOTE-TO-PILOT · naturalness=N3 · source_status=REMOTE · collision_risk=MEDIUM`

**审计结论。** PROMOTE-TO-PILOT；本轮最强卡，目标是 recognized provenance graph 上只漏掉 descendant invalidation 的结构化错误。

**一句话矛盾。** 模型知道原始消息已被当事人撤回，却仍把引用该消息的下游帖子当成独立有效支持。

**日常例子。** 记者撤回错误数字后，转载旧数字的三篇文章不应继续构成三份证据。

**自然数据与轴。** PHEME/RumourEval 的时间线程、PolitiFact/PrimeFacts 的更新与引用链接、新闻 corrections；选择可验证的 `original claim → copies → source recantation/correction`。问 recantation status、哪些节点受影响、有效支持数和最终 verdict。

**晋级 signature。** 源头撤回与传播边都识别正确，模型却只删除源节点，不使后代证据失效；直接转载受影响、真正独立来源不受影响。若所有 correction 都不理解，属于普通 revision failure。

**规模与机制。** append-only 文本天然保留所有旧 payload，强长上下文甚至更能取回它们。机制 A：撤回只给源节点加负标签，不沿 provenance edge传播；B：图更新正确，但 evidence reader不读取 invalidation mask。

**最近工作与空位。** misinformation correction、knowledge update和 CAMA 邻近；独特对象是 **retraction propagation over a recognized social provenance graph**，不是“旧事实仍被记住”。

**最便宜证伪。** 先人工核验 15 条真实修正链并做 independent-source control；若 gold 链路含混或错误只因日期排序，KILL。

## SEC-07 — 机构的正式立场被投射成每个成员的私人信念

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=REMOTE · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；institution→member 属于 OIR collective→distributive projection，roll-call 只作外部复现。

**一句话矛盾。** 模型知道声明代表机构，询问成员观点时却把它复制给所有成员，包括公开投反对票的人。

**日常例子。** 董事会通过声明，不意味着每位董事私下同意；党团立场也不等于每名议员的投票。

**自然数据与轴。** QuoteBank 的组织发言、公开议会 roll-call、Convote/议会辩论与官方声明；同一事件连接 `official stance / vote outcome / named member vote or quote`。分别问机构 commitment、程序结果和个人 belief/stance。

**晋级 signature。** 机构立场与成员明示反对都可正确检索，联合查询仍把官方立场写进该成员；错误只从 institution→member，不从明示 unanimous 场景出现。若只是同名或检索错，KILL。

**规模与机制。** 机构名是高频单一实体，成员关系检索可能把其 stance 当可继承属性。机制 A：organization belief slot 被默认 distributivize；B：成员 stance保留，但 institution-conditioned query走共享 group summary。

**最近工作与空位。** 复数量词和 OIR-07 已覆盖一般 collective→distributive；本卡只有 **official public commitment vs named member private/public stance** 形成自然双解离时保留，否则并入 OIR-07。

**最便宜证伪。** 用 30 条有明确 dissenting vote/quote 的真实事件；若模型直接检索个人票已足以消除错误或跨领域无一致性，KILL。

## SEC-08 — 公开表态被当成私人相信

`priority=C · stage=KILL · naturalness=N3 · source_status=HUB · collision_risk=OCCUPIED`

**审计结论。** KILL；TactfulToM 与 2026 pluralistic-ignorance 工作已直接占据公开表态、动机和私人信念的主要叙事。

**一句话矛盾。** 模型理解人物是在礼貌、战略或代表组织发言，却仍把这句话当作其私人信念。

**日常例子与数据。** 发言人说“公司对前景充满信心”，并不逻辑蕴含发言人私下也乐观。

**自然数据与轴。** TactfulToM 的 white-lie conversations、FANToM、QuoteBank、公开听证/谈判对话；对照 `sincere assertion / white lie / role-required statement / explicit private aside`。问 utterance content、communicative goal、public commitment、private belief与预测行动。

**晋级 signature。** communicative motive和公私冲突都回答正确，private-belief query仍跟公开话语；加入 private aside 后行动预测与 belief report产生选择性分裂。若只是白谎识别差，已被 TactfulToM覆盖。

**规模与机制。** instruction/role modeling可能强化公共言语行为，而 belief tracker仍把 assertion当默认证据。机制 A：speech-act写入speaker belief slot；B：公私槽分开，belief query偏向最近/公开 utterance。

**最近工作与空位。** TactfulToM 直接造成高碰撞；只有它未研究的 **motive recognized + public commitment correct + private-belief/action routing wrong** 及其机制，才值得保留。

**最便宜证伪。** 先在 TactfulToM 原文上新增不超过两类 deterministic follow-up；若行为等同论文已报白谎 accuracy，标 `OCCUPIED`。

## SEC-09 — 名气压过与问题真正相关的专长

`priority=B · stage=HOLD · naturalness=N2 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；Whose Facts Win 已覆盖来源声望母区，只允许客观 jurisdiction gold 下的 prestige×topical-expertise crossover 复活。

**一句话矛盾。** 模型能指出小众来源才是该问题的领域专家，冲突答案仍跟随更有名但不相关的机构。

**日常例子。** 对地方火山的当前活动，当地地质台应比著名但讨论宏观经济的报纸更相关。

**自然数据与轴。** ExpertQA、PubMedQA/Qasper、官方技术报告和真实作者 affiliation；必须用可审计的 topic–expertise 匹配与 source date，不凭名字臆造权威。先问 topical expertise、document entailment和source fame，再问冲突答案/是否继续查证。

**晋级 signature。** expertise 和文本支持都识别正确，选择却随 generic prestige 而非 topic match；内容交换后偏好跟来源而不是 proposition，且无冲突时普通 QA 正常。若“哪个来源该信”本身没有客观 gold，KILL。

**规模与机制。** 规模增强机构先验，也增强专长识别，两路径可能反而竞争更明显。机制 A：source embedding带全局 authority scalar；B：topic-conditioned reliability可表示但未送入 evidence gate。

**最近工作与空位。** Whose Facts Win 已研究机构/个人和来源流行度，因此风险高；只有 **global prestige 与 query-conditioned expertise 的交叉双解离** 才不是重复。

**最便宜证伪。** 文献与数据审计先行：若 Whose Facts Win 已有 topic-expertise factorial，直接 KILL；否则只选 20 个有明确法定/学术管辖权的实例试水。

## SEC-10 — “大家都这样做”被改写成“这样做是允许的”

`priority=A · stage=PROMOTE-TO-PILOT · naturalness=N3 · source_status=HUB · collision_risk=HIGH`

**审计结论。** PROMOTE-TO-PILOT；必须同时保留 descriptive/deontic 语义与 policy 识别，只让频率双向改写行动合法集。

**一句话矛盾。** 模型明白一句话只描述行为频率，给建议时却把高频行为当成许可甚至义务。

**日常例子。** “多数乘客逃票”不推出逃票被允许；“很少人申请休假”也不推出休假不被允许。

**自然数据与轴。** NormBank 的情境规范、Social Chemistry、真实政策文本配公开统计；保持 action/setting相同，分开 `many do / socially expected / legally permitted / required`。先问各句语义与规则，再问是否合法、是否推荐和应否惩罚。

**晋级 signature。** descriptive/prescriptive分类正确，policy text也正确，但 action reader随频率改变合法集合；反方向“很少做但明确允许”出现镜像错误。若只有道德态度变化而无可判定规则，KILL。

**规模与机制。** 语言预训练中频率和规范常相关，强世界知识不会自动学会 Hume 式 is/ought gate。机制 A：descriptive norm与injunctive norm共享scalar；B：modal type可解码，action recommender以社会原型覆盖规则。

**最近工作与空位。** [McCannon (2024)](https://doi.org/10.1016/j.econlet.2024.111828) 已发现 ChatGPT-3.5 的独裁者博弈行为同样受 descriptive 与 injunctive norm 影响；因此“描述性规范影响行为”本身已被占。仅保留 **明文冲突 policy + 两种语义区分完整 + 行动合法集双向发生 descriptive→normative laundering + 跨家族机制**。

**最便宜证伪。** 先抽 30 个 NormBank setting并配真实 policy，不让模型判断主观道德；若 policy-following不受描述频率影响，KILL。

## SEC-11 — 知道多份报告同源，仍把它们算成多份证据

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；继续完全路由到仓库 Lineage–Weight 主候选。

**一句话矛盾。** 模型正确识别三篇报道都来自同一调查，最终仍按“三票对一票”决策。

**状态与路由。** 这不是新卡；直接路由到本仓库已经有行为证据的 [Lineage–Weight Dissociation](../candidates/lineage_weight_dissociation.md)。自然来源包括 GroupQA、新闻 syndication、PHEME 传播树和公开引用图。

**可保留的唯一 signature。** 来源依赖识别随规模变强、加权反而不改善，并可因果定位 dependency representation 未进入 evidence aggregator。普通重复偏差、majority bias 或 source preference 均已被 Whose Facts Win、GroupQA 与 CAMA 占位。

**最便宜证伪。** 不重跑仓库已有模板；下一步只做真实 provenance 图的外部复现与 exact literature audit。

## SEC-12 — 群体决定被当成全员赞成

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=REMOTE · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；group decision→unanimity 继续路由到 OIR，保留真实表决 setting 即可。

**一句话矛盾。** 模型知道委员会以多数票通过提案，询问某位反对者时仍说其赞成。

**状态与路由。** 该母结构已在 [OIR-07 collective→distributive](01_ONTOLOGY_IDENTITY_REFERENCE.md#oir-07--集体行动被投射给每个成员) 登记。这里补充社会数据路线：公开 roll-call + 同事件新闻摘要，可把“组织决定、投票规则、成员票、官方声明”四层同时校验。

**可保留的唯一 signature。** 票数与个人票均能正确读出，只有从 group action 到 named member stance 的 late readout错误；并能与 SEC-07 的“机构正式承诺/成员私人信念”分开。普通复数量词错误不另起题。

**最便宜证伪。** 先审 30 条有明确反对票的报道；若错误只在新闻省略票数时发生，属于信息不足，KILL。

## 审计后 shortlist

| 顺位 | 卡 | 审计判定 | 只有什么结果才算命中 |
|---:|---|---|---|
| 1 | SEC-06 recantation propagation | **PROMOTE-TO-PILOT** | 撤回与 provenance 均识别正确；只漏掉 descendant invalidation，独立来源正常 |
| 2 | SEC-04 query/comment counted as support | **PROMOTE-TO-PILOT** | stance 判对；query/comment 因 claim-token 重复在聚合中被正计数 |
| 3 | SEC-01 public vs private common knowledge | **PROMOTE-TO-PILOT** | 一阶知识严格匹配；只有自然协调行动没有读取 public-event 差异 |
| 4 | SEC-10 descriptive → normative laundering | **PROMOTE-TO-PILOT** | 描述/规范与明文 policy 均判对；频率仍双向改写行动合法集 |

**HOLD：** SEC-02 仅在自然通信日志上出现稳定 `delivered→known` gate 时复活；SEC-09 仅在有客观 jurisdiction gold 的 prestige×expertise crossover 时复活。
**KILL / ROUTE：** SEC-03 被 2026 pluralistic-ignorance 工作直接占位；SEC-08 被 TactfulToM 与公私顺从工作夹住；SEC-05、SEC-11 路由 Lineage–Weight；SEC-07、SEC-12 路由 OIR。完整依据见[残酷审计](audits/AUDIT_SEC_KRE.md)。

---

## Batch-2 脑暴死亡回填（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Pluralistic ignorance** | `KILL-EXACT` | 2026 *Everyone Conforms, No One Believes: Pluralistic Ignorance in LLM Agent Populations* 已直接研究 private beliefs、public conformity 与群体 cascade；本文件 SEC-03 的旧卡也已经因此 KILL。 |
| **Generic bystander effect / responsibility diffusion in LLM populations** | `KILL / NEAR-EXACT` | multi-agent social-bias / responsibility-diffusion 工作已经直接逼近经典 bystander 搬运；仅把场景换成 agent population 不构成新 operator。 |
| **Hidden-profile bias（宽版本）** | `NOT-ADDED / ROUTE SEC-F4-F9` | hidden-profile 是成熟群体信息共享范式；若只是 shared information 被过度加权、private information 未汇合，会被 SEC 来源/分区母族和既有范式吸收。 |
| **Collective/group→member projection（宽版本）** | `ROUTE SEC-07/12 + OIR-07` | 群体决定、机构立场向成员广播已经在本文件与 OIR 注册；本轮不重复建立“collective predicate”新卡。 |

**禁止复活。** pluralistic ignorance、bystander、hidden-profile 等经典社会心理名称不能因为“我们做 mechanistic interpretability”就重新作为 behavior novelty；必须先指出最近工作和本仓库 SEC/F4/F9 无法预测的独立 operator。
