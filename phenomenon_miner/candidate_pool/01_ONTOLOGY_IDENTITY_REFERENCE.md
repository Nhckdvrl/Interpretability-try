# 领域 01：本体、同一性与指称

状态：`12 candidate cards — UNTESTED / literature triage incomplete`
母问题：模型如何区分“同一类东西”“同名的东西”“属性相同的东西”和“数值上同一个东西”？

## 领域边界

这个领域和 Hamdi 的现实/虚构题共享“ontology”高度，但概念轴不同：Hamdi 问一个实体是否现实存在；这里问**话语中有几个个体、不同提及是否共指、关系中的哪个个体占据答案槽**。

最近占位较强的工作包括：

- [Meaning Beyond Truth Conditions](https://aclanthology.org/2025.acl-long.432/) 已系统研究 anaphora accessibility；
- [From Ambiguity to Accuracy](https://aclanthology.org/2025.acl-srw.27/) 研究 coreference resolution 对 RAG 的影响；
- ICLR 2026 [Is the Reversal Curse a Binding Problem?](https://iclr.cc/virtual/2026/poster/10007939) 把 reversal curse 与 binding 联系；
- ICLR 2026 [Language Models Use Lookbacks to Track Beliefs](https://openreview.net/forum?id=6gO6KTRMpG) 已给出简化 ToM 中角色—物体—状态绑定的端到端机制；
- 本仓库 [EIRD](../promoted/002_evidence_induced_referent_displacement.md) 已覆盖“新证据把答案槽重绑到关系邻居”。

所以本领域不能只做普通 coreference accuracy 或“模型有 binding error”。值得晋级的必须是**一种自然、选择性、跨规模的 individuation failure**，最好表现为 `identity readout 正确，但 downstream use 错误`。

## 优先数据架

| 数据 | 自然单元 | gold | 适合问题 | 可得性 |
|---|---|---|---|---|
| [FraCaS](https://huggingface.co/datasets/maximoss/fracas) | 人工语言学推理小故事 | entail/unknown/contradict | one-anaphora、复数、广义量词、同一性 | 公开；本轮已下载 TSV |
| [AmbER](https://aclanthology.org/2021.acl-long.345/) | 同名实体的检索与 QA | aliases/answer | namesake separation | 公开 |
| [EntityQuestions](https://aclanthology.org/2021.emnlp-main.496/) | relation-balanced entity QA | aliases | type/instance、别名 | 公开 |
| [BookCoref](https://aclanthology.org/2025.acl-long.1197/) | 书籍尺度指代 | coreference spans | 长距离对象边界 | 公开 |
| [OntoNotes](https://catalog.ldc.upenn.edu/LDC2013T19) / GAP | 自然文本指代 | clusters | mention identity | OntoNotes 受许可；GAP 公开 |
| [LongMemEval](https://arxiv.org/abs/2410.10813) | 多会话更新 | answer aliases | 人物/物品更新与重建 | 公开 |
| [MEBench](https://aclanthology.org/2025.emnlp-main.77/) | 跨文档多实体 QA | answer | 同名/多实体组合 | 公开 |
| [NOPE](https://github.com/nyu-mll/NOPE) | 自然 presupposition NLI | human labels | 提及、存在与预设 | 已在本地 |

---

## OIR-01 — “也买了一台”被当成“买了同一台”

**一句话矛盾。** 模型知道句子只重复了物品类型，却把两个新的不定个体合并成同一个对象。

**日常例子。** “Alice 买了一台笔记本电脑，Bob 也买了一台。”这不推出“两人共同拥有同一台电脑”；“Bob 买了同一台”才推出。

**自然数据与轴。** FraCaS ellipsis/one-anaphora 原题提供原生锚点；再从公开商品、住房、宠物和交通文本中抽取 `a X ... one too`。最小四格是 `one too / the same one / another one / a X`，同时询问类型事实与 token identity。外部确认可用 OntoNotes/GAP 中 one-anaphora 片段或公开英语语料人工抽样。

**晋级 signature。** 至少三家族能正确回答“Bob 也有一个 X”，却选择性地把共享 token 判为真；`same one` 和 `another one` controls 正确；错误不依赖 entailment 标签。若只有 FraCaS 一条旧题或 CoT 后完全消失，KILL。

**规模与机制。** 更强语言建模会强化 one-anaphora 的类型继承，但并不自动要求为两个 existential introductions 分配不同 discourse referent，故可能随规模保留。机制 A：existential slot 被复用；B：slot 分开，但 final NLI transitivity/overlap heuristic 合并。可用 mention-level referent probe 与 `one too ↔ same one` activation interchange 裁决。

**碰撞边界。** 普通 anaphora/coreference 已很拥挤；独特空位只能是 **type inheritance intact + token identity collapsed** 的行为—机制解离。

**最便宜证伪。** 24 个自然场景、四条件、自由解释 + direct judgment；若 Qwen/Gemma/Phi 中少于 2 家同方向，立即 KILL。

## OIR-02 — 两次不定引入被默认合成一个人

**一句话矛盾。** “一位医生打来电话；一位医生随后到场”被模型默认理解为同一个人，即使文本没有任何共指依据。

**日常例子。** 两个句子都说“a doctor”，类型相同并不保证个体相同；若作者要共指，通常会说“the doctor”或“she”。

**自然数据与轴。** 从 OntoNotes/BookCoref 的不定 NP 引入、FraCaS discourse items 与新闻事件链中采样。原生对照：`a doctor ... a doctor`、`a doctor ... the doctor`、不同职业、显式 `another doctor`。gold 是“必然同一/必然不同/未确定”，不是猜作者最可能意图。

**晋级 signature。** 模型能在显式 definite/another 条件正确 individuate，却在重复 indefinite 上稳定产生 false necessity；随着两次提及距离或中间相似属性增加出现 cliff。若错误只是 pragmatic preference 而非把“不确定”判成“必然”，KILL。

**规模与机制。** next-token 训练奖励连贯的实体延续，可能系统性偏向最小实体数，即便强模型懂冠词。A：discourse model 在早层直接复用 entity index；B：两个 index 保留，晚层 coherence prior 压过 modal/necessity readout。

**碰撞边界。** 与普通 coreference resolution 不同，本卡测的是**没有足够证据时是否非法断言 numerical identity**。

## OIR-03 — 同名跨文档实体融合

**一句话矛盾。** 模型能分别读懂两篇文章，却把两个同名人物的属性拼成一个不存在的人。

**日常例子。** 一篇报道中的 Alex Lee 是医生，另一篇中的 Alex Lee 是乐手；“Alex Lee 是会拉琴的医生”没有被任何文档支持。

**自然数据与轴。** AmbER 为主，MEBench 与 Wikidata 同名实体页面为外部确认。使用真实同名人物及各自原文，不改事实；轴为单文档→双文档、同名→不同名 matched pairs、加入明确职业/地点 disambiguator、相同属性但不同名 nuisance control。

**晋级 signature。** 单篇问答与显式“有两位同名者”计数均正确，但跨文档 conjunction 产生 hybrid entity；错误答案必须组合两人的真实属性，而非随机。若只是检索选错一篇文档，降为普通 entity disambiguation 并 KILL。

**规模与机制。** 更强模型包含更多同名实体知识，也面临更强 parametric association，融合风险未必下降。A：文档级 entity keys 过度按表面名聚合；B：keys 分开但 query readout 用 name-only routing。可 patch 标题/mention/answer token 区分。

**碰撞边界。** AmbER 已研究歧义检索；可辩护空位是**局部识别完整但生成出跨实体混合体**及其 binding mechanism。

## OIR-04 — 角色继任被表示成“同一个人改名”

**一句话矛盾。** 模型知道职位保持不变、任职者已经更换，却在后续推理中把前任的属性转移给继任者。

**日常例子。** “Maya 原是项目负责人，周二 Omar 接任。”项目负责人仍是一个角色，但 Maya 与 Omar 不是一个持续对象。

**自然数据与轴。** LongMemEval knowledge-update items、MultiWOZ/Schema-Guided Dialogue 的负责人/预订人变更、真实公司职位时间线。比较 role query、person query、role-property inheritance 与显式 unchanged-property controls。

**晋级 signature。** 当前任职者和更新时间都答对，却把前任个人属性（专业、许可、承诺）归给继任者；role-level 属性仍正确。若只是忘记谁是当前负责人，属于普通 update failure。

**规模与机制。** 角色是稳定检索 key，人物是随时间替换的 value；强检索可能反而加深以 role 为 key 的属性缓存。A：role slot 未把 person-specific attributes 卸载；B：表示已分开，query 对“负责人”走旧聚合路径。

**碰撞边界。** 动态知识/职位更新已多；必须是 **role persistence 与 person identity 选择性混合**，不是 stale fact。

## OIR-05 — 属性相等被误当对象同一

**一句话矛盾。** 两个对象在任务相关属性上完全相同，模型便开始把“相等”当作“同一个”。

**日常例子。** 两把钥匙型号、颜色、齿形都一样，也仍可能是两把不同钥匙；丢掉一把不意味着另一把也丢失。

**自然数据与轴。** 从 TextWorld/ALFWorld 的重复物体、CLUTRR/SpartQA 的同属性对象、商品/库存数据中抽取真实对象状态；公开环境提供 object IDs 和 deterministic gold。轴为共享属性数与 identity marker，另用显式 alias（真正同一对象）对照。

**晋级 signature。** 属性读取与对象计数正确，但一次状态更新选择性传播到相似对象；传播随属性重合出现非线性，而对真实 alias 应传播。若模型连 object count 都错，KILL。

**规模与机制。** 语义压缩鼓励相似对象共享表示，而 identity tracking 需额外 address。A：早层 object embeddings collapse；B：独立 embeddings 在 update routing 时因相似 key 同时被写入。

**碰撞边界。** 不能只做“entity names matter”。独特对象是 **equality–identity dissociation + mutation spillover**。

## OIR-06 — 整体与部分交换答案槽

**一句话矛盾。** 模型已经识别问题问的是整体，新出现的真实部分信息却让它回答那个部分；反方向也可能发生。

**日常例子。** 已知道谜底是 Mozilla，再告诉它“其浏览器 Firefox 很流行”，答案变成 Firefox。

**自然数据与轴。** 这是已获得跨模型证据的 [EIRD](../promoted/002_evidence_induced_referent_displacement.md) 子结构，不作为新卡重复验证。后续可在 Protobowl、Chicago Open、增量 biography 和 RAG 中按 whole↔part / organization↔product 单独确认。

**晋级 signature。** 只作为 EIRD 机制分层：gold 仍可解码、答案槽重绑到关系邻居、后续线索恢复。不得另起“part-whole confusion”论文与 EIRD 内耗。

**状态。** `ANCHOR / ROUTE TO EXISTING PHENOMENON`。

## OIR-07 — 集体行动被投射给每个成员

**一句话矛盾。** “委员会批准了提案”被模型当成“委员会每个成员都投了赞成票”。

**日常例子。** 一个委员会可以按多数票通过，而某个成员投反对；集体谓词不等于成员逐一满足。

**自然数据与轴。** FraCaS plurals/generalized quantifiers、plural NLI datasets、真实议会投票记录与新闻句。比较 collective predicate、distributive predicate、显式 unanimous/majority、成员级查询；gold 由逻辑与公开投票决定。

**晋级 signature。** 模型能区分 unanimous/majority 词义并读出真实票数，却只在从 group action 推 member action 时产生 false entailment；反向 `all members → group` 正确。若所有 plural reasoning 都差，KILL。

**规模与机制。** 群体名常作为单一 entity token 与动作关联，强事实记忆不要求展开成员量词。A：group predicate 被错误 distributivize；B：量词表示正确但 entity-to-member expansion 在晚层过宽。

**碰撞边界。** 复数语义是老语言学题；必须有跨模型 dissociation、自然投票数据和因果 group/member routing，不能只报 FraCaS accuracy。

## OIR-08 — 同一个对象的两个合法描述被当成两个对象

**一句话矛盾。** 模型能判断两个描述共指，却在计数、更新或行动时仍保留两个对象槽。

**日常例子。** “Clark Kent 就是 Superman”之后，问有几个人应答一；知道别名关系却安排两张不同的票，就是 identity recognition–use gap。

**自然数据与轴。** Wikidata alias/redirect pairs、AmbER、LongMemEval 中显式 alias introduction；使用现实别名与上下文临时别名。四格：identity probe、cardinality、属性更新传播、行动资源分配；对照为真正不同但相似名字。

**晋级 signature。** identity probe 高、属性事实高，但 cardinality/更新/资源分配稳定双计；至少一条错误随规模不减。此前本仓库简单角色计数因接口 artifact 被否，本卡只有在**自然 alias 来源 + 自由生成 + downstream use**下才可复活。

**规模与机制。** 知识规模改善 alias recognition，却可能不触发 context object store 的 canonicalization。A：两个 entity slots 未 merge；B：merge 表示存在，但 count/action reader 仍读 surface mentions。

**碰撞边界。** identity knowledge 与 reversal/binding 工作接近，风险高；独特性必须是识别—对象库 canonicalization 解离。

## OIR-09 — 被删除的对象以“幽灵实体”继续参与关系

**一句话矛盾。** 模型能报告对象已不存在，却仍让它占用位置、权限、库存或因果链中的一个槽。

**日常例子。** 会议已经取消，模型却说那个时间段仍“冲突”；文件已经删除，却继续把它算进文件数。

**自然数据与轴。** ToolSandbox/τ-bench、MultiWOZ reservation state、LongMemEval 更新、真实日程/库存日志。比较 existence probe、count、constraint solving 和 action；control 是对象仍存在但 inactive，以及新建同名对象。

**晋级 signature。** deletion/existence 问题正确，只有关系/资源计算仍把幽灵对象算入；create→delete 与 never-create 同终态却行为不同。若只忘记 delete 信息，归入普通 state tracking。

**规模与机制。** 删除需要从多种索引反注册，而语言模型可能只追加 tombstone。A：旧 object slot 保留且 relational edges 未清；B：current state 正确，但 planner 检索未过滤 tombstone。

**碰撞边界。** 与 retraction/hysteresis 相邻，需把“对象存在性正确、关系使用错误”作为 decisive contrast。

## OIR-10 — 类别答案吞掉实例答案，或实例答案吞掉类别答案

**一句话矛盾。** 模型知道“这是什么种类”和“具体是哪一个”，但新证据会使输出在 type 与 token 之间跳槽。

**日常例子。** 问“哪一种疾病”应答 influenza；问“哪位患者”应答 Alice。相关证据里同时出现两者时，答案类型不该互换。

**自然数据与轴。** EntityQuestions/WebQSP 的 class–instance 关系、QASC 科学分类、Protobowl incremental clues；选择同一 evidence set，只用原数据中不同合法 query target，另测 answer type probe。

**晋级 signature。** answer type 能被正确陈述，但自由生成错误稳定落到相邻层级；提示答案类型可 rescue，而删除相关实体名不会完全 rescue。若只是 alias scorer，KILL。

**规模与机制。** 强知识模型形成更密集的 type-instance 图，竞争节点更多。A：query type feature衰减；B：feature 保留，但 relation participant salience 改写 answer pointer。

**碰撞边界。** 与 EIRD 高度相邻；只有跨非增量任务、呈现独立 type/token gate 才单独保留，否则并入 EIRD。

## OIR-11 — 关系方向正确，关系承担者却被交换

**一句话矛盾。** 模型知道发生了“挑战/治疗/收购”，却把施事者、受事者或拥有者写进错误实体槽。

**日常例子。** “David 挑战 Goliath”不等于“Goliath 挑战 David”；模型可能正确识别 challenge，却把问题所问的人换成另一个 participant。

**自然数据与轴。** TACRED/Re-TACRED、DocRED、WebQSP inverse relations、Protobowl relational clues。使用原生 subject/object 与 inverse queries；实体交换后 gold 可程序映射。

**晋级 signature。** relation classification 与两个实体识别都正确，joint role binding 错；错误系统性落到 converse triple，而非随机实体。若只是 reversal curse 的已知方向失败，KILL。

**规模与机制。** relation 与 participant 可能由不同路径编码，强模型改善两个局部成分但不保证 late binding。A：subject/object address 未 canonicalize；B：query-created answer pointer 受最近 participant 劫持。

**碰撞边界。** reversal curse、relation extraction 和 EIRD 均相邻；必须是 components-intact / binding-broken 的自然联合解离。

## OIR-12 — 提及一个对象被当成承诺它存在

**一句话矛盾。** 模型能读出句子是在否认、怀疑或询问某对象，却在后续回答中把“被谈到”升级成“世界中存在”。

**日常例子。** “调查没有发现第二名嫌疑人”提到了第二名嫌疑人，但并未证明有这样一个人。

**自然数据与轴。** NOPE presupposition corpus、SQuAD2/FalseQA 的 false-premise questions、FEVER 中否定存在 claims、新闻中的 `no evidence of X`。依次测 mention detection、existence status、后续 count/causal query；quote/negation/uncertainty 是原生 operator。

**晋级 signature。** 模型正确分类 operator 与否定，却在延迟的对象计数或因果解释中让该对象“进入世界”；直接 existence probe 正确、downstream use 错时最强。若只是在否定句上错误，属于已知 negation failure。

**规模与机制。** 语言建模需要为任何名词短语激活实体内容，但 existence/commitment 是额外 source tag；内容表示越强不保证 tag 被路由。A：mention 自动实例化 persistent object slot；B：slot带 nonexistence tag，后续生成路径丢弃 tag。

**碰撞边界。** 与 Hamdi 的 reality ontology 不同：这里所有对象都可能是现实类型，轴是 **mention/denial 是否引入 discourse referent 与 world existence**。仍需 exact 审计 false-presupposition 与 negation 文献。

## 本领域首轮排序

| 顺位 | 卡 | 理由 | 主要风险 |
|---:|---|---|---|
| 1 | OIR-01 one-anaphora type/token | 一句例子、FraCaS 原生锚点、matched identity controls | anaphora 文献拥挤；可能被强推理消除 |
| 2 | OIR-03 namesake hybrid | 真实跨文档应用、错误落点可结构化 | 可能退化成普通 entity disambiguation |
| 3 | OIR-09 ghost entity | 真实事务语义、存在 probe/use 解离、可做路径机制 | 与 state/retraction 工作重叠 |
| 4 | OIR-04 role/person inheritance | 天然 ontology 分解，强规模生存理由 | 动态知识文献多 |
| 5 | OIR-12 mention→existence | 基本哲学问题、NOPE/false-premise 自然数据 | gold/pragmatics 易争议 |
| 6 | OIR-07 collective→distributive | 普通人易懂、公开投票可校验 | 可能只是量词能力不足 |

OIR-06 已归入 EIRD；OIR-08 只有在自然数据上摆脱此前接口 artifact 才允许重开。
