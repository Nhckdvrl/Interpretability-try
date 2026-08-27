# MTR / DPC 第二轮对抗审计

审计日期：2026-08-28
对象：首轮晋级的 MTR-07、MTR-13、MTR-14、DPC-11，以及从时间、事件与语用文献缺口中新长出的候选。
纪律：本轮故意忽略首轮结论，以最强近邻和最坏构念解释重新判定；**未运行模型、未请求或关闭任何推理服务**。

## 结论先行

| 候选 | 第二轮结论 | 一句话理由 |
|---|---|---|
| MTR-07 event-token identity collapse | **HOLD** | 自然事件的 identity gold 有连续性；一旦改成无歧义显式事件，强模型可能直接解决。更致命的是，2026 的 repeated-token counting 已把“正确表示存在、计数输出被晚层覆盖”的通用机制做到很深。 |
| MTR-13 expiry gate bypass | **KILL — exact collision** | ContractBench 已直接测试“artifact 过期后仍被使用”，覆盖确定性虚拟时钟、38 个模型、尺度 cliff、非单调 scaling 与干预；TicToc 又覆盖 stale context 到 tool action。 |
| MTR-14 document-time→event-time routing | **KILL** | DCT/event-time 是 TimeML 时代的基本区分；TimeSET、ETRQA、EventRelBench/UERLens 已占行为与表示。自然新闻中的更新时间往往并非语义无关，干净 oracle 只能靠重筛或人工造窄例。 |
| DPC-11 local agreement→global stance | **FINALIST-CONDITIONAL（本轮唯一）** | 仍有一个可守边界：局部 target 与全局 stance 都独立判断正确，但下游 summary/state/action 发生 scope broadcast。风险是自然 concession gold 模糊，且 P3Sum/PSV/ambivalence 已非常接近。 |

因此第二轮没有为了凑数保留两个旧 finalist。旧候选只保留 **一个条件式 FINALIST**；它在行为验证前仍不是“已发现现象”。

## 判定合同

第二轮只问四件事：

1. **强模型会不会自然消失？** 不是要求先跑 frontier，而是判断效应是否只依赖小模型不会解析句子、不会计数或不会按格式输出。
2. **自然 gold 是否客观？** 如果只有研究者读完后“感觉应该如此”，或要把自然文本改成玩具句才无歧义，不能晋级。
3. **是否超出母现象？** 不能把 event factuality、stance drift、counting failure 或 temporal QA 加一句 representation-use dissociation 就称为新现象。
4. **是否有直接机制口？** 至少两套在层位、方向或 intervention 预测上不同的机制；“模型不够重视 X”不算机制。

---

## 旧四项逐项反证

### MTR-13 — 淘汰：expiry 已被 exact work 占领

**最强近邻不是“相似”，而是任务同构。** [ContractBench](https://arxiv.org/abs/2605.17281) 把 API 中间产物的时效约束称为 observation contract，33 个双轴任务中的 validity failure 正是“artifact 已过期仍被 agent 使用”。它用虚拟时钟给确定性 oracle，测试 38 个模型；frontier 仍低于 80%，Qwen 3.5 出现 4B→9B cliff，GPT-5 家族还出现非单调 scaling，并做了可操作的奖励干预。MTR-13 原先想保留的 `expiry understood → action still uses it`、尺度行为和 agent action 都已在其主张内。

[Your LLM Agents are Temporally Blind](https://aclanthology.org/2026.findings-acl.1848/) 的 TicToc 又用 76 种、多于 1,800 条多轮 tool-use trajectory 测量 stale context 如何改变 function-calling decision，并做 prompting/post-training 缓解。再加 [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) 与 [STALE](https://arxiv.org/abs/2605.06527)，已没有足够独立空间。

**为什么不能改名求生。** 从 token、票券、政策或推荐换领域，只是在 ContractBench/TicToc 的 validity failure 上换 payload。若限定“模型口头说过期但仍使用”，又退化为现有 judge–action gap 的一个筛选切片。**结论：KILL，不进验证。**

### MTR-07 — 降级：自然性—难度陷阱，加上通用 counting dissociation 已占

**最强反证一：自然 event identity 没有想象中硬。** [EventRelBench](https://aclanthology.org/2025.findings-emnlp.482/) 已有 35K 个事件 coreference、temporal、causal、super/sub relation 问题；[UERLens](https://aclanthology.org/2026.acl-short.38/) 已定位事件关系的层级特征并做 manipulation。更早的 [On Event Individuation](https://aclanthology.org/2023.findings-emnlp.862/) 说明事件个体化本身依赖参与者、时间、地点和语篇粒度。真实新闻里的“两次还是一次”经常是连续体，不是干净 binary oracle。

**最强反证二：representation→counting 的漂亮机制已经有人做完。** [Repeated-Token Counting Reveals a Dissociation Between Representations and Outputs](https://arxiv.org/abs/2605.09239) 发现正确 count 在所有 post-embedding 层几乎完美可解码，错误却由约 85–93% 深度的 MLP 覆盖，并跨 Llama 1B/3B、Qwen 1.5B/3B/7B 成立。若 MTR-07 最终只有“事件属性/身份知道，count 错”，论文会被直接视为语义版 counting routing failure。

**构念两难。**

- 保持真实事件：non-coreference gold 常有争议，错误可以解释为合理 event granularity。
- 为硬 gold 加上不同日期、地点、参与者并明确“这是另一次”：大模型极可能解决，剩下小模型 counting/format failure。
- 再要求 token-specific consequence 也合并：可以排除纯 counting，但若模型没有直接把两事件判成共指，错误又容易落入普通 binding/retrieval。

**结论：HOLD。** 只有未来自然数据筛出 `pairwise non-coreference + 两组 token-specific consequence 均正确 + 非计数后果仍按 type 合并`，且大模型不消失，才可复审。它不占当前 FINALIST 名额。

### MTR-14 — 淘汰：时间槽不是无关 metadata，干净例又会变窄

**母区分过于经典。** TimeML/TempEval 长期区分 Document Creation Time 与 event time；[TimeSET](https://arxiv.org/abs/2403.00990) 已以真实新闻研究 timeline construction、partial ordering 与任务 formulation，[ETRQA](https://aclanthology.org/2025.findings-acl.1198/)、EventRelBench 和 UERLens 又覆盖 event-time QA、关系行为与内部特征。

**原 invariant 不总成立。** publication/update time 在真实新闻里常会：

- 锚定 today/yesterday/currently 等相对时间；
- 表示后续修订加入了新的结果、确认或第二事件；
- 与转载时间、原始发布时间、最后更新时间混合。

因此“只改 metadata，事件世界严格不变”需要人工确认文章版本没有新增事件，还要剔除所有相对时间。做到这一步后，剩下的是异常干净、显式列出三个日期的单事件样本，强模型很可能不再生成 phantom recurrence。

**机制也不够专属。** 若三个时间槽全对而自由时间线多出一次事件，最朴素解释是 generic summarization hallucination 或输出格式诱导；若要求 phantom 精确落在 revision date，样本量和自然性又急剧下降。**结论：KILL。** 可作为未来 temporal benchmark 的 error tag，不应单独消耗现象验证预算。

### DPC-11 — 唯一条件式 FINALIST，但必须缩窄 headline

**最近邻比首轮想象得强。**

- [Perspectivized Stance Vectors](https://aclanthology.org/2025.findings-naacl.83/) 已显式表示一个 argument 对不同 perspective 的局部 stance，并从局部维度聚合 agreement/disagreement。
- [P3Sum](https://aclanthology.org/2024.naacl-long.119/) 发现超过 50% 新闻摘要改变作者政治 stance，并做 perspective-preserving intervention。
- [Arbiters of Ambivalence](https://aclanthology.org/2025.findings-acl.243/) 显示模型在开放回答中能保持 nuance，却在 judge/debater role 被迫选边。
- [ChangeMyView Through Concessions](https://aclanthology.org/2018.dnd-9.4/) 已标 concession，但也明确指出 marker 多义、argumentative concession 难判，自动方法 test F1 仅 46.0%。

所以“LLM 把局部同意总结成全局同意”本身不足以称新。唯一可守的决定性解离是：

```text
independent probe: agreement target correct
independent probe: local proposition stance correct
independent probe: speaker's global stance correct

yet an unprompted downstream receiver
(summary / stable speaker state / consequential choice)
systematically broadcasts local +1 to global stance
```

**自然 gold 风险。** 裸 `yes, but ...`、`I see your point` 与 concession 并不总承诺前半命题；必须优先使用后文明确重申总立场、或原作者 delta/stance 有原生证据的 CMV/SAD 回合。若只留下模板式 “I agree P but reject C”，强模型可能全解，届时应诚实淘汰。

**两套机制。**

- H1（scope binding failure）：agreement act 的 positive feature 在中层即绑定到 speaker/global topic，而不是 local target。
- H2（receiver reduction failure）：local target 与 global stance 都在中层分开存在，只有 summary/state writer 使用 `any(local agreement) → global +1` 的错误 reducer。

target-span patch 若同时改变 component judgments 与 downstream 支持 H1；只在晚层/输出 receiver 发生翻转支持 H2。去掉词面 `agree` 的自然 paraphrase、local agree × global stance 四格、acknowledgment 与 explicit full agreement 是不可少的 controls。

**保留条件。** 现阶段标为 `FINALIST-CONDITIONAL / UNTESTED`。若自然样本 gold 达不到双人高一致，或错误只在 forced summary label、不在自由 summary/状态/选择中出现，立即降级。

---

## NEW-GAP-GROWN：从未做对比中新长出的三个候选

下面三项不是旧卡改名。每项先经过 exact-collision 检索，并且在**尚未运行模型**的前提下，达到了“值得交给便宜验证代理”的 paper-level bar。状态统一为 `FINALIST-UNTESTED`，不是声称现象已存在。

### NG-01 — 习惯被写成经历：event kind 被实例化成 event token

**一句话现象。** 模型能正确解释“Lina 通常骑车上班”描述的是习惯、并不说某一天真的骑了车；但随后整理人物时间线或回答“那天发生了什么”时，却凭空写入一次确定的骑车经历。

这不是 “possible event 被当真”。一个 habitual/generalization 可以完全为真，但它谈的是一种规律或 event kind，不蕴含任意指定的 event token。核心本体区分是：

```text
knows: kind / habitual, not a particular episode
uses: creates a dated or countable episode anyway
```

**天然公开数据。**

- [UDS-Genericity](https://aclanthology.org/Q19-1035/) 基于 English Web Treebank，公开约 27K/3K/3K predicate train/dev/test 标注，直接问 predicate 是 particular event 还是 general pattern。
- [Situation Entities](https://www.coli.uni-saarland.de/projects/sitent/page.php?id=resources) 公开 MASC + Wikipedia 的 genericity、habituality、episodic type 标注。
- [Richer Event Description](https://aclanthology.org/W16-5706/) 的公开仓库含新闻/论坛 95 文档、8,731 events，并在 annotation ontology 中明确 generic event 不进入文档 actual timeline；其 SET–MEMBER 还提供 generic pattern 与 actual member 的自然正对照。

发现阶段直接筛自然 habitual/generic clause，不把人名日期硬塞进模板。正例是语料中原生的 actual episode；负例是原生 generic/habitual。抽样必须由人核验 particular-occurrence entailment。

**exact-collision 审计。** UDS-G/SitEnt 研究 generic–habitual–episodic 的标注与分类；RED/THYME 把 generic 从 actual timeline 中区分；[MAVEN-Fact](https://aclanthology.org/2024.findings-emnlp.651/) 研究 fact/possibility/impossibility；CogNarr 研究 perception/imagination 与 factual events。本轮以 `LLM habitual generic timeline`, `generic event actualization`, `genericity downstream timeline`, `habitual event factuality LLM` 等组合检索，**截至审计日未找到**同时要求 `genericity judgment correct → downstream episodic write wrong → internal causal mechanism` 的工作。它不由 MAVEN-Fact 包含，因为 generic truth 与 token actuality 是不同轴。

**为什么可能不随规模消失。** 英语 habitual 常无显式 `usually`（如 “I walk to work”），依赖语篇与 aspect；更大模型会提高 semantic label，却未必让 event-memory writer 拥有 kind/token 类型系统。摘要、memory 与 event extraction 的训练又奖励保留显著 predicate。由于晋级只统计 genericity probe 已正确的 item，scale 提高 reader 反而会扩大可审计子集，而不自动修复 writer。

**两个竞争机制。**

- H1（early tokenization of event ontology）：event trigger 先创建 token node，generic/habitual classifier 只是旁路标签；时间线读取的是已实例化 node。
- H2（late writer type erasure）：kind/token 在中层可分，timeline/memory writer 的 event schema 没有 generic type，或忽略 type bit，把所有 salient predicates写成 episode。

跨层 probe 若在早层已经出现 phantom token 支持 H1；若 kind/token 一直可解码、仅 writer 层 patch 能消除实际化支持 H2。

**最便宜证伪。** 先取 30–50 条人工确认的自然 habitual/generic 与 actual SET-member controls。若强一些的同家族尺寸在无特殊提示的 timeline/episode/count 三种 readout 都不实际化，直接 KILL，不进入大样本。

### NG-02 — 事实性传染：同一句里的事件被压成一个 reality status

**一句话现象。** “球队已经出场，之后也许会庆祝。”模型分别问时知道 `出场=事实`、`庆祝=可能`；可一旦生成时间线、因果链或事件清单，确定事件把可能事件“带真”，或可能事件把确定事件“带虚”。

这不是平均 event factuality accuracy，而是 mixed-status composition 的结构性错误：

```text
event A status correct       event B status correct
             \               /
              same clause/document
                       ↓
downstream assigns A and B one shared status
```

应重点找具有方向、局部性和非线性的 `status attraction`：同一 coordinate/causal edge 最大，拉开句距衰减；CT+ 邻居让 PS+ actualize，或非事实邻居使 CT+ 被漏掉。只有能预测错误 destination 的形状才晋级，普通“多事件更难”不算。

**天然公开数据。** [MAVEN-Fact](https://aclanthology.org/2024.findings-emnlp.651/) 含 112,276 个自然新闻事件的五类 factuality、supporting words、arguments 与 event relations；可直接筛同句/相邻句、不同 factuality 的自然 event pairs。RED 也有 ACTUAL/HYPOTHETICAL/GENERIC/UNCERTAIN contextual modality 和 event relations，可做第二语料。所有主结果先用原文共现，不拼接两个不相关句子；程序筛选后人工抽样检查 scope。

**exact-collision 审计。** MAVEN-Fact 做个体 EFD、supporting evidence，并测试“加入 arguments/relations 是否帮助分类”；其结果反而显示额外 relation/argument 对 LLM 常无益或有害。传统 document-level EFP 与 scope-composition 工作预测每个 event 的 factuality。检索 `event factuality interference`, `mixed factuality events LLM`, `modality contagion coordination`, `adjacent event factuality` 未找到以 **两个 component label 均正确、下游被压为共享 status** 为 phenotype 并做机制的论文。它比一般 hallucination 多出邻居 status、关系局部性和双向/单向 attraction 三个可证伪结构。

**为什么可能不随规模消失。** MAVEN-Fact 中 GPT-4 的 non-factual 宏观表现仍低，且给 LLM 添加 event relation/argument 没带来稳定收益；更重要的是，本候选只看两个 label 已正确的 item。一个句子通常共享 residual context 与 summary salience，事件级 addressability 不是靠参数量必然获得的。强模型更擅长压缩多事件叙述，反而可能更稳定地采用 clause-level status reducer。

**两个竞争机制。**

- H1（scope spillover）：modal/negation/evidential cue 在中层错误广播到 coordinate/causal neighbor；单独 label 可由局部词面旁路答对。
- H2（receiver pooling）：每个 event 的 status 在中层保持分离，但 timeline/summary writer 先把句子或 event cluster 池化，再用多数、最高确定性或最显著事件的 status 写全部节点。

对 A/B event token 的 status probe、关系边消融和 matched activation interchange 可区分：中层 neighbor status 已变支持 H1；仅 late writer patch 改变 downstream 而 component status 不动支持 H2。

**最便宜证伪。** 先筛 40–60 个原生 mixed-status pairs，要求两个单项 status probe 都正确。若完整上下文中的事件清单/时间线没有朝邻居 status 的定向错误，只是随机 omission，立即 KILL。

### NG-03 — 部分回答让问题过早“结案”

**一句话现象。** 记者问“项目花了多少钱、何时完成？”回答只谈了时间。模型能准确说这是 partial answer，甚至指出“成本没有回答”；可让它接管访谈、维护未决事项或填写案件状态时，它却把整道问题标成 resolved，不再追问成本。

这里坏掉的不是 answer classification，而是 QUD（Question Under Discussion）状态更新：

```text
recognizes: response answers only subquestion q1
correct state: q1 closed, parent QUD still open because q2
observed state: whole parent QUD popped/closed
```

**天然公开数据。**

- [“I Never Said That”](https://aclanthology.org/2024.findings-emnlp.300/) 公开 3,445 个真实政治访谈 QA，包含 Clear/Ambivalent/Non-reply 三级标签和 `Partial/half-answer`、General、Dodging 等细类；其代码与数据随 Anthology/GitHub 发布。
- [Covering Uncommon Ground](https://aclanthology.org/2023.acl-short.20/) 公开 200 个 SNLI 信息缺口实例及人写 gap-focused follow-up，可作为缺口已知、下一问 gold 明确的辅助集。
- [QUDeval](https://aclanthology.org/2023.emnlp-main.325/) 提供 2,190 个细粒度 QUD 评价，可用于构建/QUD parser control，但不作为主要行为集。

主结果优先用真实访谈中的 multi-part question、原回答与后续采访语境。只有回答缺了哪个 slot 能由原问题分解和人标清晰确定的 item 才入池；不把“我不喜欢这个回答”误作 partiality。

**exact-collision 审计。** “I Never Said That” 做 response clarity/evasion classification；Covering Uncommon Ground 在已知 source–student gap 时生成 follow-up；QUDeval 评估 QUD parsing；AskBench/MediQ 测初始信息不足时是否主动澄清。本轮以 `partial answer QUD closure LLM`, `evasive answer unresolved question follow-up`, `answer completeness dialogue state`, `question remains open LLM` 检索，未找到 **模型先正确识别 partiality/缺失部分，却在后续 QUD state 或行动中把父问题关闭** 的跨模型机制研究。母工作拥有 reader 或 generator，未测两者之间的 state updater。

**为什么可能不随规模消失。** 对话预训练和 instruction tuning 中，`question turn → answer turn → next topic` 是极强结构先验；模型可以学会精细地解释 evasiveness，同时 state updater 仍在 turn/role 边界执行粗粒度 pop。更大模型提高 partiality reader，未必改变“收到一个 answer-shaped turn 就前进”的策略。现象还可能在 judge/agent 模式增强，类似已知的 open-answer nuance 在 forced role 中坍缩，但这里 gold 是未回答 slot，不是主观中立。

**两个竞争机制。**

- H1（early turn-boundary pop）：看到 answer role/相关回复后，QUD stack 在内容整合前就关闭；partiality label 来自另一条语义路径。
- H2（policy/readout failure）：parent QUD 与 missing slot 在中层仍可解码，只有 follow-up/state writer 因 conversational-progress 或 completion prior 选择 `resolved`。

若在 answer 末尾层 parent-QUD representation 已消失、换角色边界即可改变，支持 H1；若 missing slot 保留到晚层、对 state/follow-up head patch 才恢复，支持 H2。

**最便宜证伪。** 从真实 multi-part political QA 取 30–50 条双人确认样本；先独立筛 partiality 与 missing-slot 判断均正确的 item，再看自由 follow-up、unresolved checklist 和 consequential handoff 三个 readout。若只在强制二值 JSON 出错，或强模型自然都会追问，KILL。

---

## 三个新候选的相互边界

| 候选 | 它不是哪一个母现象 | 必须出现的独特 signature |
|---|---|---|
| NG-01 habit→episode | 不是普通 factuality/imagined-event hallucination | generic/habitual 与 truth 都判断正确；错误是创造一个可计数、可定时的 event token |
| NG-02 status attraction | 不是整体 EFD accuracy drop | A/B 各自 status 正确；只有 mixed-status composition 的下游状态朝邻居定向收缩 |
| NG-03 partial-answer closure | 不是 clarification/response clarity 低 | partiality 与 missing slot 正确；父 QUD/工作流仍被关闭 |

NG-01 研究 **kind→token type erasure**，NG-02 研究 **token A/B 之间 status pooling**；不能因为都用 event 数据就合并。NG-03 是 dialogue-state updater，和 DPC-11 的 stance reducer也不同：一个错误地做 `some answered → all resolved`，另一个错误地做 `some agreed → global agree`。若后续机制发现二者共享同一 `existential-to-universal reducer`，那是额外统一结果，不是预设命名。

## 建议交给验证代理的顺序

1. **NG-01**：自然、可一句话解释、gold 与 ontology 最硬，且 kind/token 是比一般 factuality 更独立的机制问题。
2. **NG-03**：真实应用场景最强，现成政治访谈数据可直接筛；先警惕 partial gold 与后续问题的多解性。
3. **NG-02**：数据规模最大、机制最直接，但必须先证明是定向 contagion，不是多事件上下文的一般难度。
4. **DPC-11**：最近邻最拥挤，作为旧候选对照验证；若 effect 很强仍可回到第一梯队。
5. **MTR-07**：只做低优先级 opportunistic scan，不单独启动大规模实验。

## Novelty 表述纪律

上述 exact-collision 审计只能支持：“截至 2026-08-28，本轮检索未找到完整覆盖指定决定性解离的工作。”不能写 `first`，也不能在行为未跑前写“模型普遍表现出”。任何新候选若 component judgment 同时失败、只能靠模板/系统提示诱发、只在一个小模型成立、或错误没有指定 destination，立即淘汰，不用 representation probing 给弱现象续命。
