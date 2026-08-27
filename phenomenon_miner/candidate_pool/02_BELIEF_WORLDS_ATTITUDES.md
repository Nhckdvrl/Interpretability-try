# 领域 02：信念、世界与命题态度

状态：`12 candidate cards — UNTESTED / high collision risk`
母问题：模型能否把一个命题的内容，与“谁相信它、在哪个世界假设它、说话者是否承诺它、它是否真正发生”分开？

## 领域边界与红线

这是机制潜力最高、也最容易与 Hamdi 或已有 ToM 工作相撞的领域。以下宽主张不得单独推进：

- “模型内部区分现实与虚构”；
- “模型能/不能做 false-belief QA”；
- “fact / fiction / forecast 有不同表示”；
- “一句话在 quote、user、tool role 下表现不同”；
- “模型可线性解码 belief/truth，但输出不总服从”。

邻近占位包括 [Representations of Fact, Fiction and Forecast](https://aclanthology.org/2025.acl-long.1345/)、[Language Models Use Lookbacks to Track Beliefs](https://openreview.net/forum?id=6gO6KTRMpG)、[How Context Shapes Truth](https://arxiv.org/abs/2601.06599)、ACL 2026 [Language Models Struggle to Use Representations Learned In-Context](https://aclanthology.org/2026.acl-long.676/)，以及 Hamdi 的 reality/imaginary 主线。

本领域只有在**特定 operator 或 scope 的内容/状态解离**上才能保留：例如能正确归因引语却当作叙述者承诺、能识别反事实却在退出 scope 后把它并入历史、能报告 agent belief 却不用它预测 agent action。

## 优先数据架

| 数据 | 标注对象 | 适合轴 | 可得性 |
|---|---|---|---|
| [CommitmentBank](https://aclanthology.org/D19-1630/) | 说话者对补语真值的承诺 | factive/non-factive、否定、问题、speaker | 公开 |
| [MegaVeridicality](https://aclanthology.org/D18-1501/) | embedding verb 的事实性推断 | know/claim/hope/deny | 公开 |
| [NOPE](https://github.com/nyu-mll/NOPE) | 自然预设与投射 | quote/negation/question/embedding | 已在本地 |
| [MAVEN-Fact](https://github.com/THU-KEG/MAVEN-Fact) | 事件 factuality | actual/possible/negative | 已在本地 |
| FactBank / MEANTIME / UW factuality | 新闻事件 factuality | source、modal、time | 公开/按许可 |
| [FANToM](https://aclanthology.org/2023.emnlp-main.890/) / BigToM / ToMi | 多角色信念与信息接触 | narrator/agent、belief/action | 公开 |
| [MuSR](https://arxiv.org/abs/2310.16049) | 长故事中的人物、动机与行动 | belief/desire/action | 已在本地 |
| [QuoteBank](https://figshare.com/articles/dataset/Quotebank_A_Repository_of_Attributed_Quotations_from_News/14184808) | 真实新闻引语与 speaker | attribution/endorsement | 公开 |
| Counterfactual Story / TimeTravel | 反事实故事 | scope、minimal change | 公开；开放 gold 慎用 |

---

## BWA-01 — 会归因引语，却把引语当作者自己的话

**一句话矛盾。** 模型正确说出“这句话是 Alice 说的”，随后总结时却把内容写成叙述者或文档已经确认的事实。

**日常例子。** 新闻写“公司 CEO 声称产品绝对安全”，不等于新闻机构确认产品安全。

**自然数据与轴。** QuoteBank 的真实引语—speaker 对、新闻 fact-checking corpora、CommitmentBank 的 report verbs。原生四格：直接断言、引语、间接引语、作者明确背书；先问 speaker attribution，再问 document commitment 和下游 factual summary。

**晋级 signature。** attribution probe 与 quote span extraction 正确，只有文档承诺/后续推理把 quoted proposition 当真；`said/claimed/confirmed` 呈有结构的梯度。若模型连谁说的都不知道，属于普通 attribution failure。

**规模与机制。** 强模型更会保留引语 payload，但 truth-oriented generation 可能把可用内容与 source commitment 分路。A：source tag 形成但 summary router 丢弃；B：tag 与内容在同一 entity/event slot 内被后续 attention 覆写。

**碰撞边界。** source preference 与 quotation 工作很多；独特空位是 **speaker attribution intact / narrator commitment wrong**，并做因果 source-tag routing。

## BWA-02 — “假设一下”在退出假设后仍污染现实

**一句话矛盾。** 模型能在假设内部正确推理，明确结束假设后却继续把假设事实当作现实前提。

**日常例子。** “假设东京在法国，回答下面一道题。现在结束假设：东京在哪个国家？”最终应回到日本。

**自然数据与轴。** Faithfulness-QA / SQuAD context-conflict items、counterfactual QA、真实规划中的 what-if 分析。关键不是单句 frame prompt，而是自然 `enter → reason → exit → unrelated real-world use` 进程；对照为直接现实路径、quote scope、同长度真实事实。

**晋级 signature。** scope 内服从正确、exit 标记理解正确、现实知识 control 正确，但退出后的答案沿 counterfactual；随 scope 深度或内部推理步数出现 hysteresis。若一句“回到现实”即可在所有模型完全恢复且无内部残留，只是 prompt following，不推进。

**规模与机制。** 更强模型会更好地构造 coherent hypothetical world，因此其上下文状态也可能更强，未必自动 canonicalize。A：world gate 未关闭；B：gate 已关闭但假设期间写入了无 source tag 的事实缓存。

**碰撞边界。** 与 Hamdi reality representation 不同，本卡研究 **scope exit 与状态恢复**；与本仓库 unring-bell 项目可能相撞，正式验证前必须对照其 exact claim。

## BWA-03 — 反事实内容“倒灌”成真实历史

**一句话矛盾。** 模型能判断一个句子是反事实，稍后重述故事时却把反事实分支里最鲜明的事件列入实际发生事件。

**日常例子。** “如果救援队晚到，桥就会坍塌；事实上他们及时赶到。”总结不能写“桥坍塌后……”。

**自然数据与轴。** TimeTravel/Counterfactual Story、MAVEN-Fact、新闻中的 counterfactual conditionals。先做 operator classification，再做 delayed event list、causal query 和 summary；matched factual event content 与 lexical salience。

**晋级 signature。** counterfactual status 初始读取正确，actual event recall 正确，但延迟总结出现 branch intrusion；错误落点优先是 vivid consequence 而非任意词。若直接 factuality probe 也错，归入普通 factuality。

**规模与机制。** 更强模型生成/理解更丰富的模拟内容，content trace 可能强于 world tag。A：branch content 写入共享 event memory；B：分支存储分开，但 summary query 无 world-address selector。

**碰撞边界。** CogNarr 与 event factuality已覆盖宽行为；只有 **status initially intact → downstream reuse loses it** 才保留。

## BWA-04 — 心理事件的内容变成外部事件

**一句话矛盾。** 模型记得某人计划、害怕或想象了什么，却后来把所想内容当成真正发生的事情。

**日常例子。** “Lena 担心航班会取消，但航班正常起飞。”不能在旅行历史中记录一次取消。

**自然数据与轴。** 本仓库已有 [event actuality gate](../candidates/event_actuality_gate.md)：MAVEN-Fact、FactBank、MEANTIME、认知过程叙事。分别测 content、holder、operator、actuality 与 delayed use。

**晋级 signature。** ordinary event memory 高，mental-content memory 高，operator probe 高，只有外部时间线/因果推理选择性失去 non-actual tag。

**状态。** `HOLD / EXISTING CANDIDATE`。CogNarr 2026 已占领宽行为；不可另起普通 event-factuality 卡。

## BWA-05 — 会报告人物信念，却不用信念预测其行动

**一句话矛盾。** 模型正确回答“人物相信钥匙在抽屉”，预测人物下一步时却让他走向现实中的桌子。

**日常例子。** Sally 不知道球被移走；她的行动应由自己的信念而非叙述者真相决定。

**自然数据与轴。** FANToM/BigToM/ToMi 的 belief questions 与 action questions、MuSR 中 motive/action。对每个故事构造原数据支持的 matched `belief report / action prediction / world truth`，避免自造世界规则。

**晋级 signature。** belief report 和 action affordance controls 正确，只有 action prediction受 reality leakage；反方向 `correct belief → action` 完好。若仅高阶 ToM 难度随 depth 下降，KILL。

**规模与机制。** belief retrieval 与 action policy可能是不同 downstream receivers；Lookback 机制解决“取出 belief”，不保证 planner消费它。A：belief payload未送入 action token；B：已送入但现实-state path在晚层竞争获胜。

**碰撞边界。** ToM 行为极拥挤；独特空位是 **同一 item 内 belief retrieval 完好、action receiver 错误**，以及相对于已知 lookback 的 downstream routing。

## BWA-06 — 愿望被当成预测，预测被当成事实

**一句话矛盾。** 模型知道某人“希望/预计/保证”某事，却在概率判断或事实总结中不给这些态度留下区别。

**日常例子。** “市长希望明天下雨”不提高下雨概率；“气象员预计下雨”可能提供证据；“市长保证会下雨”也不等于已发生。

**自然数据与轴。** CommitmentBank、MegaVeridicality、QuoteBank 与天气/金融预测新闻。保持 proposition 相同，仅使用语料原生 attitude holder/verb；对照 speaker expertise 与 later observed outcome。

**晋级 signature。** verb meaning/paraphrase probe 正确，但 downstream probability 或 event history按词的表面确定性排序而非 attitude type；最好出现 desire→prediction 的选择性混淆而 factive verbs 正确。

**规模与机制。** 语言模型擅长补全 attitude complement，payload 激活可能独立于 evidence-status gate。A：态度类型未绑定到 proposition；B：绑定存在但 evidence aggregator只读 lexical certainty。

**碰撞边界。** factivity/veridicality 是成熟语义任务；需从 classification 提升到 **attitude recognition–evidential use dissociation**。

## BWA-07 — “可能、很可能、确定”在行动中被压成同一个开关

**一句话矛盾。** 模型能给三个 epistemic modal 正确排序，制定行动时却把它们全部当成已经发生或全部忽略。

**日常例子。** “药物可能有严重副作用”和“确定有严重副作用”不应触发完全相同的风险权衡；二者也都不等于副作用已发生。

**自然数据与轴。** CommitmentBank/MegaVeridicality、MAVEN-Fact 的 certainty labels、医疗/天气风险决策 benchmark。先测 verbal/numeric strength ordering，再用同一 payoff 下的 deterministic threshold decisions。

**晋级 signature。** 概率/语言强度报告单调，行动却在某个 modal category出现 cliff、反序或全-or-none；改变 payoff threshold 能区分 belief与policy。若只是概率校准差，归入 UQ 文献。

**规模与机制。** 表征 epistemic strength 和把它写入 discrete action policy接受不同训练信号。A：writer只读取 categorical possible/actual gate；B：连续 strength存在但阈值固定或被风险风格覆盖。

**碰撞边界。** UQ/abstention很拥挤；这里需 natural modal-to-action transfer 与机制化 writer gap。

## BWA-08 — 否认的命题仍被当作支持证据

**一句话矛盾。** 模型能指出一条 claim 被明确否认，整合证据时却仍让 claim 的内容推高相关结论。

**日常例子。** “警方否认有第二名嫌疑人”不应成为“存在第二名嫌疑人”的正证据。

**自然数据与轴。** FEVER/HoVer 的 refute evidence、QuoteBank 中 denial、MAVEN-Fact negative events。比较 assert/deny/question/quote，先做 polarity与source probe，再做 multi-hop conclusion；使用同一 content span。

**晋级 signature。** deny识别高，直接真假题正确，但把 denial sentence加入证据集反而提升被否命题或其后果；删除 payload noun不再触发。若所有 negation都错，KILL。

**规模与机制。** content token 的 contextual entrainment可能强于否定/operator tag；强模型知识图更易由 payload扩散。A：negation在早层未作用于实体/事件激活；B：truth status正确但下游 retriever/aggregator忽略 polarity。

**碰撞边界。** contextual entrainment与 negation处理已有机制工作；必须是 **denial recognition intact + downstream evidence sign wrong**。

## BWA-09 — 预设在被明确取消后仍留在共同世界

**一句话矛盾。** 模型知道说话者撤销了一个预设，后续对话却继续把它当双方已经接受的事实。

**日常例子。** “我并没有孩子，所以‘我的孩子几点放学’这个问题不成立。”后面不能继续推断说话者有孩子。

**自然数据与轴。** NOPE 的 projection/accommodation 标注、false-presupposition QA、真实问答纠错对话。进程为 trigger→challenge/cancel→后续 inference；直接无 trigger、未取消、显式确认是 controls。

**晋级 signature。** 模型能解释 presupposition与 cancellation，却在后续 count/profile/action中保留它；`cancelled` 与 `never introduced` 同终态不同。若 gold 依赖有争议的 projection reading，剔除。

**规模与机制。** 对话模型被训练维护 common ground，但大多以追加方式更新，撤销可能只加 correction 不清除旧 presupposition slot。A：accommodation不可逆写入；B：已标 invalid，但下游 persona memory不过滤。

**碰撞边界。** 与 unring-bell/retraction强相邻；独特性必须来自 **presupposition-specific common-ground write**，而非任意纠错迟滞。

## BWA-10 — 局部假设泄漏到相邻、独立的问题

**一句话矛盾。** 模型在解决一个“假设 P”的子问题后，把 P 带入同一文档里的另一个明确独立子问题。

**日常例子。** 法律备忘录分别分析“若合同有效”和“若合同无效”两种情形；第一部分的假设不能污染第二部分。

**自然数据与轴。** ReClor/AR-LSAT 多情形题、法律 hypotheticals、MMLU case questions；使用原生并列 scenarios，交换情形顺序，逐一与合并呈现，gold来自原题/规则。

**晋级 signature。** 两个 scenario单独都对，合并后第二个选择性继承第一个假设；交换顺序后污染方向随先后而变，且 section headers/长度 controls无效。若只因总长度增加，KILL。

**规模与机制。** 更强模型更会建立局部 world model，但是否为每个 subproblem分配独立 world address并不由规模保证。A：shared scratch state未reset；B：worlds分开但query router取最近高激活分支。

**碰撞边界。** 不能包装成普通 multi-question interference；必须是可证明的 **scope-bound assumption leakage**。

## BWA-11 — 认识到自己不知道，却在复述时生成确定“记忆”

**一句话矛盾。** 模型先正确说某人物没有看到某事，稍后总结人物经历时却补出该人物不可能拥有的确定记忆。

**日常例子。** Tom 离开房间后花瓶被移动；模型知道 Tom 没看到，却写“Tom 记得花瓶被移到柜子”。

**自然数据与轴。** BigToM/FANToM 的 perceptual access、LoCoMo/SHARE 长对话 memory。匹配 knowledge probe、experience summary与行动预测；对照真正目击者、听说者和未知者。

**晋级 signature。** access/knowledge query正确，生成的 episodic summary却采用全知叙述者事实；错误不是笼统 action prediction而是具体“个人记忆”内容。

**规模与机制。** summarization训练偏向完整、coherent叙事，可能压过 agent-specific memory boundaries。A：memory generator读取global state；B：agent state已路由但 completeness objective晚层补全缺失事件。

**碰撞边界。** ToM与hallucination母现象均近；独特对象是 **knowledge boundary intact / episodic memory fabrication**。

## BWA-12 — 承认一个命题“只是传闻”，行动时仍把它当事实

**一句话矛盾。** 模型能准确标注信息是传闻、猜测或未经证实，建议行动时却不给这一 source status任何折扣。

**日常例子。** 一条匿名传闻称航班取消；模型先说“尚未证实”，随后仍建议立刻放弃行程，和航空公司正式通知无差别。

**自然数据与轴。** PHEME/RumourEval、新闻 verification corpora、CommitmentBank、真实风险决策场景。保持 content和后果相同，使用原生 source/veracity labels；测 status report、belief、action与信息搜寻。

**晋级 signature。** source/veracity识别正确，但 action与正式确认条件重合；最好信息搜索/澄清也不随 status变化，而独立风险偏好control正常。

**规模与机制。** 识别 epistemic status来自语言理解，行动建议来自 helpfulness/precaution policy，两者可能目标冲突。A：status未送入planner；B：送入但保守policy饱和。通过 payoff与可逆性轴区分。

**碰撞边界。** source preference、misinformation与UQ已广；需 **status recognition–action weighting** 的 matched dissociation，不是“模型受谣言骗”。

## 本领域首轮排序

| 顺位 | 卡 | 最强点 | 首要撞车/风险 |
|---:|---|---|---|
| 1 | BWA-01 quote attribution→endorsement | 新闻自然、source/content正交、机制清楚 | quotation/source文献 |
| 2 | BWA-05 belief report→action | 基本主体问题、现有lookback之后仍有receiver空位 | ToM高度拥挤 |
| 3 | BWA-03 counterfactual backwash | 一句话惊喜、自然进程轴 | event factuality/CogNarr |
| 4 | BWA-08 denial as evidence | operator识别与evidence sign可解离 | negation/entrainment机制已有 |
| 5 | BWA-11 impossible personal memory | 比普通ToM更自然、生成错误落点清楚 | gold与生成scorer成本 |
| 6 | BWA-02 hypothetical scope exit | scale生存理由强、可做state gate | Hamdi与unring-bell边界 |

BWA-04 只作为已有 actuality 候选的路由；BWA-09 在与 unring-bell exact 对照前不得验证。
