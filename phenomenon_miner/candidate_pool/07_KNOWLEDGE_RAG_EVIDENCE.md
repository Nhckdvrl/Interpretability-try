# 领域 07：知识、检索、证据与引用

状态：`14 candidate cards — AUDITED 2026-08-28 · 0 PROMOTE / 5 HOLD / 9 KILL-or-ROUTE · UNTESTED`
文献审计：[SEC / KRE 候选的残酷论文可用性审计](audits/AUDIT_SEC_KRE.md)
母问题：检索系统把文档放进上下文后，模型是否区分“搜到了什么、文档是否相关、文档支持什么、证据是否充分、该引用支持哪一条 claim、最后该回答什么”？

## 领域边界

RAG 是最拥挤的候选区之一。下列宽结论已经不能单独成题：

- 无关文档让准确率下降；
- 长上下文位置、文档顺序或 top-k 改变答案；
- context 与参数知识冲突；
- 多数、重复或高信誉来源赢得冲突；
- multi-hop 最后一步失败；
- citation 不完整或不准确；
- 模型能检测冲突但仍答错。

相邻占位至少包括 [GroupQA](https://aclanthology.org/2026.findings-acl.2003/)、[Whose Facts Win?](https://aclanthology.org/2026.acl-long.1357/)、[Authority Bias in RAG](https://aclanthology.org/2025.acl-long.1400/)、[Query–Knowledge Relevance](https://aclanthology.org/2024.emnlp-main.353/)、[ALCE](https://aclanthology.org/2023.emnlp-main.398/)、[Attribute or Abstain](https://aclanthology.org/2024.emnlp-main.463/)、[Ragability](https://aclanthology.org/2026.lrec-1.182/) 以及大量 positional/noise/conflict 工作。

本领域只保留能指出一个**特定信息状态或接口边界**的异常：

```text
no retrieval result ≠ negative evidence
query overlap ≠ relevance
headline / snippet ≠ document commitment
newer document ≠ automatically applicable current state
answering ≠ answering with citations
correct claim ≠ correctly bound citation
quoted false claim ≠ fact-checker's verdict
bridge fact available ≠ bridge used at composition
faithful compression ≠ faithful downstream use
evidence sufficiency judgment ≠ answer/abstain gate
```

ACL 2026 的 [representation-use gap](https://aclanthology.org/2026.acl-long.676/) 已占据“知道但不用”的宽母现象。每张卡都必须再给出一个自然的 gate、错误目的地或阶段转移，否则不进入验证。

## 优先数据架

| 数据 | 自然单元与 gold | 适合轴 | 可得性 |
|---|---|---|---|
| [NoMIRACL](https://aclanthology.org/2024.findings-emnlp.730/) / SQuAD v2 | relevant / non-relevant 或 answerable / unanswerable | 空检索、缺证、abstain | 公开；SQuAD v2 已在本地 |
| Natural Questions / TriviaQA / PopQA | 真实信息查询、短答案与证据 | closed-book、query echo、检索状态 | 公开 |
| [HotpotQA](https://aclanthology.org/D18-1259/) / [MuSiQue](https://aclanthology.org/2022.tacl-1.31/) / [2Wiki](https://aclanthology.org/2020.coling-main.580/) | 支持文档、bridge、decomposition | 局部/组合、边界、路径 | 已在本地或公开 |
| FEVER / HoVer / FEVEROUS | claim、support/refute/NEI、evidence chain | polarity、充分性、修正 | 本地或 Hub |
| [PrimeFacts](https://aclanthology.org/2026.lrec-1.613/) / PolitiFact | 真实 fact-check 文章、verdict、外链证据 | 引述反驳、source graph | 公开或按网站条款 |
| [ALCE](https://aclanthology.org/2023.emnlp-main.398/) | ASQA/ELI5/QAMPARI 的答案与 citation | citation obligation / binding | 公开 |
| [LAB](https://aclanthology.org/2024.emnlp-main.463/) / Qasper | 长文档 QA 与 evidence spans | attribute/abstain、claim-level support | 公开 |
| [SituatedQA](https://aclanthology.org/2021.emnlp-main.586/) | 同一问题在不同时间/地点的答案 | freshness、applicability | 公开 |
| AmbigQA / ASQA / EntityQuestions | 歧义问题、多答案/消歧证据 | specificity、answer target | 公开 |
| MultiHopRAG / KILT / FRAMES | 检索语料、provenance、多约束 QA | source grouping、证据角色 | 本地或公开 |

---

## KRE-01 — “没有搜到”被当成“答案不存在”

`priority=C · stage=KILL · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL；ACL 2026 已把检索长期未命中后推断目标“不存在”写成 canonical evidence-deprivation case，核心故事抢题风险过高。

**一句话矛盾。** 模型知道一次搜索只返回“没有相关结果”，后续却把它当成否定事实，甚至推翻自己原本正确的答案。

**日常例子。** 公司知识库搜不到“东京是否是日本首都”，只说明该库没收录，不说明东京不是首都。

**自然数据与轴。** SQuAD v2/NoMIRACL 提供 answerability/relevance，Natural Questions/TriviaQA/PopQA 提供可独立校验的 closed-book 问题；同一 query 比较 `未调用检索 / 明确 0 hits / 返回不相关 hits / 返回一条真正反证`。先问 search status和是否出现否定证据，再问世界事实与下一搜索动作。

**晋级 signature。** closed-book 正确、0-hit status正确、模型也说“absence of evidence is not evidence of absence”，最终事实或行动仍从正确变否定/放弃；真正反证 control 能正常改变答案。若 prompt 规定“只能用文档回答”，或只是规范性 abstain，KILL。

**规模与机制。** 强模型更会把检索当工具和可靠过程，`NO_RESULT` control token 可能获得更强 stopping 权重。机制 A：empty result被编码为 negative evidence；B：open-world表征正确，但 answer gate把 retrieval failure解释成 unanswerable world state。

**最近工作与空位。** NoMIRACL 测 irrelevant retrieval，answerability/abstention工作测不知，search-agent工作测空库恢复；本卡只在 **search-state recognition intact + world-state polarity flips** 时独立。

**最便宜证伪。** 20 个高熟悉、20 个低熟悉问题，四条件，完全中性任务说明；若 0-hit 只提高合理的不确定性而不产生否定/知识擦除，KILL。

## KRE-02 — 问题回声压过模型已经识别出的相关证据

`priority=C · stage=KILL · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL；query echo 是 hard distracting passage / lexical-relevance failure 的直接子类，另加 relevance probe 不足以独立。

**一句话矛盾。** 模型准确判断哪篇文档真正回答问题，却在作答时跟随那篇只重复问题关键词的无关文档。

**日常例子。** 问“谁负责 Project Titan 的预算”，一篇反复说“Project Titan 预算”但只谈历史的页面，不应压过一篇用“该项目财务负责人”表述答案的页面。

**自然数据与轴。** NoMIRACL、Natural Questions、MultiHopRAG；从真实检索结果中选 `high lexical overlap / low semantic relevance` 与 `low overlap / answer-bearing` 对，gold 由人工/原 benchmark支持句。先做逐文档 relevance和answer-span定位，再联合回答；控制排名、长度、实体数和标题。

**晋级 signature。** relevance classification与支持句定位均正确，联合答案仍跟 echo 文档或其显著实体；移除 overlap tokens 可选择性 rescue。若 relevance 判断也错，已被 lexical-bias/relevance工作覆盖。

**规模与机制。** 更强模型能恢复更多 query paraphrase，也可能形成更强 query-to-token copy path。机制 A：relevance reader与answer pointer共享不足；B：semantic relevance已进入中层，late lexical matching head覆盖。

**最近工作与空位。** [Query–Knowledge Relevance](https://aclanthology.org/2024.emnlp-main.353/) 与 lexical-semantic conflict reranking 已很近；只有 **relevance correct / answer routing wrong** 和可因果 overlap path 才保留。

**最便宜证伪。** 先人工审 30 个原生检索对；若 lexical control后效果消失但 relevance probe本来不高，标 `OCCUPIED` 而非继续。

## KRE-03 — 标题或摘要支持，正文反驳；模型跟标题走

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；只有 body commitment 判对且错误严格跟 metadata slot、而非位置和 lexical overlap 移动时复活。

**一句话矛盾。** 模型能复述正文明确否定标题中的说法，最终 verdict 却仍跟随标题或搜索摘要。

**日常例子。** 标题问“咖啡会导致癌症吗？”，正文结论是“没有证据”；标题中的命题不是作者承诺的事实。

**自然数据与轴。** PrimeFacts/PolitiFact、PHEME 外链、真实 question-headline 与 clickbait/debunk文章；保留原始 title/snippet/body，不生成伪网页。分别问各字段内容、document-level commitment、支持句和最终 claim verdict；控制标题只是主题描述、标题与正文同向。

**晋级 signature。** body entailment与document commitment正确，只有 joint answer被 title/snippet polarity带走；字段交换后错误跟 metadata slot 而非词序移动。若模型读不懂正文或只是 title 更靠前的位置效应，KILL。

**规模与机制。** 网页训练把标题作为高权重 summary key，可能存在独立 title→answer shortcut。机制 A：title先写入文档 stance，正文未覆写；B：最终 stance正确可解码，answer decoder重新寻址 title token。

**最近工作与空位。** [RAG webpage metadata/appearance](https://aclanthology.org/2024.blackboxnlp-1.24/) 已直接研究时间、来源、外观，presentation bias 也多；只有 **body commitment recognition intact / headline polarity late override** 才可能独立。

**最便宜证伪。** exact literature audit先行；若该论文已含 title–body polarity factorial与同样 dissociation，直接标 `OCCUPIED`。

## KRE-04 — 知道哪份资料更新，答案仍停在旧状态

`priority=C · stage=KILL · naturalness=N3 · source_status=REMOTE · collision_risk=OCCUPIED`

**审计结论。** KILL；*When Facts Change* 已报告大型模型识别 temporal conflict/mutability、却不传播到 final prediction 的同构解离。

**一句话矛盾。** 模型正确指出新文档发布时间更晚、旧值已被替代，却回答“现在是多少”时仍给旧值。

**日常例子。** 旧页面说票价 20 元，新公告说从本月起 25 元；问当前票价应答 25，而问去年票价仍应答 20。

**自然数据与轴。** SituatedQA、TempLAMA/时间知识资源、真实政策/价格/职位更新；每例有旧文档、新文档、生效日期和 timestamped question。四格为 `current / at old date × old-only / old+new`，先问日期、替代关系和适用区间。

**晋级 signature。** 时间与 supersession relation 全部答对，但 current-answer reader选择旧值；past query仍正确，表明不是统一 recency confusion。最好规模越大，日期识别越好而旧值吸引不减。

**规模与机制。** 参数知识与旧高频网页随规模增强，新文档在 context中作为更新 gate。机制 A：新值未改写 canonical state；B：两个时态状态均存在，current query错误路由到 prior/高频 slot。

**最近工作与空位。** SituatedQA 已显示更新语料不能自动解决更新答案，temporal RAG与 metadata-time论文很多；独特空位必须是 **freshness/applicability recognition complete + current-state readout stale**，并做内部因果裁决。

**最便宜证伪。** 先用 SituatedQA 40 个可核验 update pair；若模型日期/生效条件本身错误或只在知名旧答案上失败，降为普通 parametric conflict。

## KRE-05 — 一要求引用，正确答案反而改成更容易照抄的错误答案

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；citation integration/order 的总体 trade-off 已出现，只剩 within-item 正确答案定向翻到可引用错误 span 的 signature。

**一句话矛盾。** 同一组证据下模型本来答对；只增加“请给出处”，答案内容却转向一段容易逐字引用但不真正回答问题的文字。

**日常例子。** 文档需两步推出结论，旁边有一句表面很像答案；要求脚注不应改变事实答案。

**自然数据与轴。** ALCE 的 ASQA/QAMPARI、LAB/Qasper；同一 question和documents比较 `answer only / answer then cite / interleaved citation / evidence spans first`，答案 gold与citation support均由 benchmark给出。控制输出长度和格式 token。

**晋级 signature。** 无引用时答案正确、相关文档定位正确；引用义务使 content系统性转到 verbatim-citable distractor，而不是随机变差。先生成答案后补引用若恢复，可定位 phase boundary。

**规模与机制。** 大模型更会遵守 citation format，也可能更强地优化局部 claim–span alignment，故不保证随规模消失。机制 A：citation planning提前约束 answer content；B：答案表示正确，citation token路径反向牵引 answer pointer。

**最近工作与空位。** ALCE、LAB 与 citation-training 明确评估 answer/citation quality，有工作甚至把“不损害答案”写成要求；本卡必须审计它们是否已经报告 **within-item answer flip destination**。若只重复总体 trade-off，KILL。

**最便宜证伪。** 先对 40 个无引用时稳定正确的 items做 matched decoding；若内容 EM 不变，仅 citation差，KILL。

## KRE-06 — 事实答对了，引用却稳定绑到关系邻居

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；只有 answer/support judgment 均正确、wrong citation 跨数据显著富集于关系邻居时才复活。

**一句话矛盾。** 模型给出正确事实，却把脚注挂到提到相邻人物/事件、但不支持该事实的文档。

**日常例子。** 答“药物 A 由公司 X 生产”是对的，脚注却指向只讨论同公司药物 B 的页面。

**自然数据与轴。** ALCE、LAB/Qasper、CiteME/CiteGuard；选择每个答案同时出现 `support document / relation-neighbor document / merely mentions answer entity` 的自然 retrieval set。测 answer、claim decomposition、support judgment与citation id；交换实体名和文档序。

**晋级 signature。** support judgment逐文档正确、answer正确，citation却选择结构化邻居；错误类型集中在 whole/part、same entity/different relation或same relation/different participant。若 citation只是随机或格式错，已被现有 attribution工作覆盖。

**规模与机制。** citation生成是单独的 document-pointer readout，知识答案变强不保证 pointer binding。机制 A：claim representation缺 participant role；B：角色完整，citation decoder按 entity overlap取最近文档。

**最近工作与空位。** [MIRAGE](https://aclanthology.org/2024.emnlp-main.347/)、ALCE、CiteGuard 已高度占位；只有一个跨数据的**关系绑定错误族**及 causal pointer mechanism 才值得留。

**最便宜证伪。** 先对现有 ALCE outputs做 post-hoc wrong-citation taxonomy，不生成新数据；若错误没有关系邻居富集，KILL。

## KRE-07 — 读懂了“这是反驳文章”，提取时却复活被反驳的说法

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；contextual entrainment 已有 causal-head 解释，必须证明 document-role/polarity effect 超出 token repetition controls。

**一句话矛盾。** 模型正确说文章结论为“该说法是假的”，回答细节问题时却抄出文章开头引用的假说法。

**日常例子。** fact-check 先写“网上流传疫苗含芯片”，随后完整反驳；引用谣言不是证实谣言。

**自然数据与轴。** PrimeFacts 的 13,106 篇 PolitiFact文章及 verdict/外链、LIAR-PLUS/PubHealth、PHEME debunk links；保留原文的 `quoted claim → verdict → evidence` 结构。分别问文章 verdict、被检验 claim、事实答案、支持 span与下游 summary。

**晋级 signature。** verdict和negation都正确，事实/summary仍稳定输出 quoted false claim；错误受 quote位置或重复数调制，却不出现在同样位置的 true quotation。若 verdict也错，属于普通 fact-checking。

**规模与机制。** 反驳文章必须充分激活假说法才能否定它，内容与polarity天然可能分路。机制 A：quoted claim成为高显著 fact node、verdict tag未绑定；B：绑定可解码，answer retrieval只按 question overlap取被引 span。

**最近工作与空位。** misinformation propagation、negation/contextual entrainment及 [Missing Counter-Evidence](https://aclanthology.org/2022.emnlp-main.397/) 相邻；独特 signature 是 **document verdict intact / claim extraction polarity inverted**，不是一般否定错误。

**最便宜证伪。** 人工审 40 篇原始 fact-check，每篇标 quote/verdict/evidence spans；若 false quote错误不高于同长度 irrelevant quote，KILL。

## KRE-08 — 每一跳都答对，组合时却换了桥接实体

`priority=C · stage=KILL · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL；子题全对/full question 错已是 multi-hop 常规分析，没有稳定 alternative-bridge destination 前不另立现象。

**一句话矛盾。** 模型单独回答两个子问题都正确，联合问题却把第二跳接到另一个关系相邻实体。

**日常例子。** 它知道《Superstition》的歌手是 Stevie Wonder，也知道 Stevie Wonder 的母亲是谁，合起来却跳到另一位歌手的母亲。

**自然数据与轴。** MuSiQue 的 gold decomposition/intermediate answers、HotpotQA/2Wiki 的 bridge/support；先原样测子问题，再测 full question，并保存错误桥实体 taxonomy。只使用 benchmark原生 decomposition，不临时拼题。

**晋级 signature。** 每个 local answer稳定正确，full answer错误且中间 trace/activation出现一个可命名的 alternative bridge；support order/format controls排除接口。若只是 final relation不会，KILL。

**规模与机制。** local retrieval和late binding接受不同训练信号；但该故事已有大量工作。机制 A：bridge未被构造；B：bridge可读却在第二跳被错误 query重绑定。

**最近工作与空位。** [Latent Multi-Hop Reasoning](https://aclanthology.org/2024.acl-long.550/)、Back Attention、BRIEF及多跳解释工作已很近；在 exact audit 前保持 HOLD，只有新的结构化错误落点或反常 scaling才晋级。

**最便宜证伪。** 先离线统计原生 MuSiQue 子题全对/full错的数量；仓库已否掉简单 one-vs-many-document主效应，不得重跑那个轴。

## KRE-09 — 自己写出的充分摘要，下一步却不会按摘要回答

`priority=C · stage=KILL · naturalness=N2 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL；summary 的 downstream utility 已有直接母工作，当前无清晰、低争议的独特错误目的地。

**一句话矛盾。** 模型从长文档生成了包含全部必要事实的正确摘要，把同一摘要作为后续知识使用时却答错原问题。

**日常例子。** 助手笔记准确写下“退款仅适用于未拆封商品”，下一轮仍建议给已拆封商品退款。

**自然数据与轴。** Qasper/LAB、HotpotQA/MuSiQue、真实政策 QA；`full docs→answer`、`full docs→summary`、`gold evidence summary→answer`、`self-summary→answer`。摘要充分性由原 gold spans + 人工抽样确认，不以模型自评充当 oracle。

**晋级 signature。** self-summary在独立 entailment审计下完整充分，直接全文与gold-summary能答对，只有 self-summary downstream use错；若摘要漏了否定/条件，就是普通 compression loss。

**规模与机制。** 摘要生成和读取可能使用不同的表面线索；更流畅的强模型摘要甚至更抽象。机制 A：self-generated text带内部低可信/source tag；B：摘要语义表示正确，但原 plan/answer prior在后续层压过它。

**最近工作与空位。** [BRIEF](https://aclanthology.org/2025.findings-naacl.301/) 与 RAG compression 已研究摘要质量/QA；ACL 2026 representation-use gap很宽。必须出现 **human-audited sufficient self-summary + path-specific failure** 才保留。

**最便宜证伪。** 先只取 30 条人审为充分的 self-summaries；若 self/gold summary 在长度风格匹配后无差，KILL。

## KRE-10 — 能判断证据已经充分，却仍继续搜或拒答

`priority=C · stage=KILL · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL；over-search 与显式 sufficiency controller 已成为系统研究对象，report/action gap 单独不足以立项。

**一句话矛盾。** 模型正确说现有文档已足以回答，决策时却继续检索；或者正确说证据不足，却直接给出确定答案。

**日常例子。** 官方政策已明确给出截止日期，再搜索只会增加噪声；只有一半合同条款时则不应自信下结论。

**自然数据与轴。** MuSiQue-Full 的 answerable/unanswerable contrast、FEVER/HoVer 的 gold evidence sets、NoMIRACL、Qasper；逐步展示 `0 / partial / sufficient / sufficient+noise` 原生证据，先问 sufficiency，再给 `answer / abstain / retrieve more` 三项行动。

**晋级 signature。** sufficiency report与缺失事实描述正确，action却在 partial→sufficient 边界不切换，或出现同一可命名的 search inertia；普通 risk/abstention control正确。若只是不懂证据，KILL。

**规模与机制。** reasoning/search训练可能强化“继续查证”，与可读的充分性状态分属 controller。机制 A：sufficiency scalar未送入 retrieval policy；B：已送入，但 search/answer默认动作有迟滞阈值。

**最近工作与空位。** adaptive RAG、over-search、abstention和 representation-use文献都相邻；独特空位必须是 **item-level sufficiency correct + action gate wrong + natural phase boundary**。

**最便宜证伪。** 不跑完整 agent，先只给三选一 next-action；若 report/action高度一致或不随证据阶段形成结构，KILL。

## KRE-11 — 赞成旧答案时很快停止，反对旧答案时反复继续搜

`priority=B · stage=HOLD · naturalness=N3 · source_status=REMOTE · collision_risk=HIGH`

**审计结论。** HOLD；confirmation bias 已跨模型占位，只允许 matched evidence 下随 initial prior 交换而移动的 stop-threshold hysteresis 复活。

**一句话矛盾。** 同样强、同样排名的证据若支持模型初始答案就足以停止搜索，若推翻初始答案却被要求更多确认。

**日常例子。** 助手先猜航班正常；第一份官方公告若说正常便停止，若说取消却继续找理由怀疑。

**自然数据与轴。** FEVER/HoVer、SituatedQA updates、可重放的检索 corpus；先记录无检索 answer，再以内容/强度/来源/排名匹配的支持或反驳文档逐步揭示，测 evidence judgment、stop/continue和最终 answer。使用原 benchmark true/refute pairs，不由模型编事实。

**晋级 signature。** 文档相关性、来源和支持/反驳方向都识别正确；停止阈值只随是否匹配 initial belief变化，内容交换后跟 prior-alignment移动。若只是反证通常更弱，KILL。

**规模与机制。** 更强参数知识产生更稳定 prior，也可能使 asymmetric stopping更强。机制 A：initial answer形成 attractor并改变 sufficiency阈值；B：证据整合对称，但 controller对answer change施加额外成本。

**最近工作与空位。** context-parametric conflict、confirmation bias、adaptive retrieval与 GroupQA 都可能覆盖部分现象；只有 **matched evidence + correct polarity judgment + stop-policy asymmetry** 才有独立方法口。

**最便宜证伪。** 先在 30 对 item上做一次性 stop/continue，不启动真实搜索；若方向不稳定或被文档顺序完全解释，KILL。

## KRE-12 — 同一来源切成多块后被当成多份佐证

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；只作为 Lineage–Weight 的真实 RAG/chunking 外部复现。

**一句话矛盾。** 一篇报道切成四个 chunk，模型把它当成四家来源共同证实。

**状态与路由。** 该问题属于 [Lineage–Weight Dissociation](../candidates/lineage_weight_dissociation.md) 的 RAG 实例，不另开论文。Whose Facts Win、GroupQA 与 CAMA 已占 false majority 母现象。

**唯一可新增价值。** 如果 chunk/source metadata在模型内部可准确读出，late evidence aggregator仍按 chunk count加权，且真实 RAG pipeline 的 retriever chunking触发规模反常，作为现有候选的应用复现。

**最便宜证伪。** 不再做人工重复段落；只在真实 MultiHopRAG/KILT retrieval logs 中审计同 source chunk duplication。

## KRE-13 — 新的真实证据把答案从目标实体推到关系邻居

`priority=C · stage=KILL-ROUTE · naturalness=N3 · source_status=LOCAL · collision_risk=OCCUPIED`

**审计结论。** KILL as standalone；只作为 promoted EIRD 的 held-out RAG 外部复现。

**一句话矛盾。** 问题目标未变，新增真实相关证据后，模型从正确目标跳到证据中新出现的 part、creator、member或product。

**状态与路由。** 直接路由到已推广的 [Evidence-Induced Referent Displacement](../promoted/002_evidence_induced_referent_displacement.md)。RAG 外部复现应使用 Natural Questions/AmbigQA/ASQA/MultiHopRAG 的原始支持文档，并预注册关系类别。

**唯一可新增价值。** held-out RAG 中错误仍落到 relation-neighbor、gold在内部仍可读、证据继续增加后可恢复；不能把普通 distractor drop写成 EIRD。

**最便宜证伪。** 只抽真实 progressive evidence cases并做 blind error taxonomy；若 wrong answers不富集关系邻居，停止该复现线。

## KRE-14 — 相同证据跨文档边界后行为改变

`priority=C · stage=KILL · naturalness=N2 · source_status=LOCAL · collision_risk=HIGH`

**审计结论。** KILL；简单 document-boundary 主效应已有本地 null，且当前没有预注册的新自然交互。

**一句话矛盾。** 两条支持事实文字完全相同，只因属于同一文档还是两篇文档，答案不同。

**状态与路由。** 仓库已在 MuSiQue supporting-only 上否掉简单 one-document vs many-documents 主效应；普通 boundary/serialization又容易被 long-context 与 positional工作包含，因此禁止原样重跑。

**只有以下情况可复活。** 文档边界与一个独立自然变量形成选择性交互，例如 boundary只阻断 recognised bridge、只放大同源误计数，或产生跨尺寸 cliff；且要在 MultiHopRAG/HotpotQA 原始文档结构中成立。

**最便宜证伪。** 不做模型测试；文献与现有日志中若没有新交互假设，就保持 HOLD。

## 审计后 shortlist

本领域经 exact-neighbor 审计后**没有候选直接进入验证队列**。RAG/citation/search controller 在 2025–2026 已极度拥挤；为避免把已有现象换名字，以下五张卡只保留为有条件 HOLD：

| 卡 | 审计判定 | 唯一允许复活的 signature |
|---|---|---|
| KRE-03 headline/body | **HOLD** | body commitment 判对；错误严格跟 metadata slot 而非位置/overlap 移动 |
| KRE-05 citation obligation | **HOLD** | 同一 item 从正确答案定向翻到“可逐字引用但错误”的 span；Answer First 选择性救回 |
| KRE-06 citation relation-neighbor | **HOLD** | answer/support judgment 均正确；wrong citations 跨数据富集在关系邻居 |
| KRE-07 refutation quote | **HOLD** | 排除 token repetition 后，只有 refutation/document-role 导致 false-quote 复活 |
| KRE-11 prior-aligned stopping | **HOLD** | polarity/strength 均判对；交换 initial prior 后 stop threshold 跟 prior alignment 移动 |

**KILL：** KRE-01 已在 ACL 2026 evidence-deprivation case 中出现核心故事；KRE-02 被 hard distraction/lexical relevance 覆盖；KRE-04 的完整 freshness-recognition/final-use 解离已由 *When Facts Change* 报告；KRE-08、09、10 分别被 multi-hop composition、summary utility、over-search/sufficiency-controller 母工作吞掉；KRE-14 有本地 null 且无新交互。
**ROUTE：** KRE-12 仅作为 Lineage–Weight 的 RAG setting，KRE-13 仅作为 EIRD 的 RAG 外部复现。完整依据见[残酷审计](audits/AUDIT_SEC_KRE.md)。
