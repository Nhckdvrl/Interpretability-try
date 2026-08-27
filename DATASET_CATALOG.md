# Phenomenon Miner Dataset Catalog

> 与 [`PHENOMENON_MINING_GUIDE.md`](PHENOMENON_MINING_GUIDE.md) 配套。这里回答“每个领域具体可以从哪些公开数据开始，以及适合扫什么轴”。

版本：2026-08-27

---

# 0. 状态图例与使用规则

## 本地状态

| 标记 | 含义 |
|---|---|
| `● LOCAL` | 已在 `/home/xiang/.cache/huggingface/datasets` 发现 processed dataset 目录；仍需检查目标 split 与 Arrow 完整性 |
| `◐ HUB` | 已在 Hugging Face hub cache 发现 dataset repository / snapshot；可能只有 metadata、部分文件或未完成下载 |
| `○ REMOTE` | 当前扫描未发现本地副本，需要下载 |
| `△ SPECIAL` | 需要执行环境、图像、人工 evaluator、受控访问或高成本，不适合第一轮小模型 smoke |

“本地存在”不等于“完整”。runner 使用前必须检查：

```text
revision / snapshot
available configs
available splits
row count
schema
license / access conditions
是否只有缓存 metadata
```

## Gold 类型

| 标记 | 含义 | Discovery 优先级 |
|---|---|---|
| `DET` | exact answer、程序执行、AST、逻辑标签等 deterministic gold | 最优 |
| `MAP` | transformation 后 gold 可程序映射 | 最优 |
| `ALI` | answer aliases / normalization 后确定 | 高，但必须审 scorer |
| `RULE` | 可执行 constraint verifier | 高 |
| `HUM` | 人工判断或开放式参考答案 | 低 |
| `JUDGE` | 依赖 LLM-as-a-judge | 不用于第一轮晋级 |

## 数据集选择规则

优先选择：

1. 本地已有；
2. 原任务 control accuracy 足够；
3. gold 为 `DET/MAP/RULE`；
4. transformation 可以最小化；
5. 有天然强度、位置、路径或 factorial 轴；
6. 官方 evaluation 可复用。

---

# 1. 数学与数值推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| GSM8K | 小学数学文字题 | `DET` | 人物重命名、独立句重排、单位等价、整体数值缩放、正确中间量单调加入 | `● LOCAL` `openai/gsm8k` | A |
| GSM-Hard | 大数值 GSM8K 变体 | `DET` | 与 GSM8K 配对做 magnitude / token-length scaling | `● LOCAL` `reasoning-machines/gsm-hard` | A |
| MATH-500 | 竞赛数学，多类别 | `DET/ALI` | 变量 alpha-renaming、等价表达、正确 lemma、解题提示距离 | `● LOCAL` `HuggingFaceH4/math-500` | A |
| Hendrycks MATH | 竞赛数学完整集 | `DET/ALI` | 与 MATH-500 相同，适合扩大确认 | `● LOCAL` `EleutherAI/hendrycks_math` | A |
| Minerva Math | 数学自由回答 | `DET/ALI` | 表达式 serialization、单位、公式顺序 | `● LOCAL` `math-ai/minervamath` | B |
| AIME 1983–2025 | 整数答案竞赛题 | `DET` | 正确 hint 强度、变量名、格式、reasoning mode × hint | `● LOCAL` 多版本 | B |
| AMC 2023 | 多项选择竞赛数学 | `DET` | option permutation、verified elimination、数值表示 | `● LOCAL` 多版本 | B |
| OlympiadBench | 奥数、多语言/多模态版本 | `DET/ALI` | 语言等价、公式 serialization、text/image factor | `● LOCAL` / `◐ HUB` | B |
| Omni-MATH | 高难数学 | `DET/ALI` | difficulty × hint、scale anomaly | `● LOCAL` `KbsdJames/Omni-MATH` | B |
| NuminaMath / NuminaMath-CoT | 问题与解答轨迹 | `ALI` | solution-step permutation、prefix truncation、correct-step insertion | `● LOCAL` | B |
| Synthetic Unanswerable Math | 信息不足数学题 | `DET` abstain | 补充缺失信息、answerability monotonicity、abstention inertia | `● LOCAL` | A |
| SVAMP | 小学数学变体 | `DET` | 数字 / 实体 swap、问题反转、等价改写 | `○ REMOTE` | B |
| ASDiv | 多样化数学文字题 | `DET` | relation-preserving paraphrase、单位、背景句 | `○ REMOTE` | B |
| MAWPS | 多来源文字题 | `DET` | 跨 source distribution 复现 GSM 轴 | `○ REMOTE` | B |
| AQUA-RAT | 带 rationale 的数学 MCQA | `DET` | option / rationale order、正确中间提示 | `○ REMOTE` | B |
| MathQA | 程序化数学推理 | `DET/MAP` | operator rename、program permutation、equivalent execution | `○ REMOTE` | A |
| DeepScaleR Preview | 推理轨迹数据 | `ALI` | trace length、prefix path、reasoning-mode signatures | `● LOCAL` | C |

首选 discovery：`GSM8K × GSM-Hard`、`MATH-500`、`Synthetic Unanswerable Math`。它们的 gold 最容易程序验证。

---

# 2. 形式逻辑、演绎与约束推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| FOLIO | 自然语言一阶逻辑推理 | `DET` | premise permutation、alpha-renaming、redundant lemma、negation × quantifier | `○ REMOTE` | A |
| ProofWriter | 规则与多步证明 | `DET/MAP` | graph relabel、proof order、shortcut lemma、独立子图、depth | `○ REMOTE` | A |
| RuleTaker | 规则推理与 entailment | `DET` | rule/fact grouping、order、redundant facts、entity rename | `○ REMOTE` | A |
| AbductionAndNegationCorpus | 否定与溯因 | `DET` | polarity equivariance、negation scope、fact addition | `○ REMOTE` | B |
| PrOntoQA | 程序化 ontology 推理 | `DET/MAP` | ontology relabel、rule order、known/novel entity | `○ REMOTE` | B |
| LogicNLI | 逻辑一致性 / NLI | `DET` | premise order、label mapping、quantifier transforms | `○ REMOTE` | B |
| ReClor | 阅读理解逻辑 MCQA | `DET` | option permutation、premise order、verified elimination | `○ REMOTE` | B |
| LogiQA / LogiQA 2.0 | 自然语言逻辑 MCQA | `DET` | 与 ReClor 相同，适合跨分布验证 | `○ REMOTE` | B |
| AR-LSAT | 分析推理与约束 | `DET` | constraint order、equivalent serialization、added derived constraint | `○ REMOTE` | A |
| ZebraLogic | Zebra puzzle / CSP | `DET` | entity permutation、clue order、redundant clue、path | `○ REMOTE` | A |
| BigBench Logical Deduction | 排序约束 | `DET/MAP` | entity swap、clue permutation、answer equivariance | `○ REMOTE` | A |
| BigBench Tracking Shuffled Objects | 状态追踪 | `DET/MAP` | object rename、swap sequence inverse、path length | `○ REMOTE` | A |
| BigBench Dyck Languages | 括号语言 | `DET` | symbol bijection、reversal、depth | `○ REMOTE` | C |

最适合 mechanism 的通常是 ProofWriter / RuleTaker：内部变量、proof edge 与 clean/corrupt pair 最清楚；但必须先在自然语言数据 FOLIO / ReClor 上确认外部有效性。

---

# 3. 多跳 QA 与组合推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| MuSiQue | 2–4 hop 可组合 QA，含 decomposition | `ALI` | support order、bridge alias、局部 subquestions vs full composition、document grouping | `● LOCAL` | A |
| HotpotQA Distractor | 双跳 QA + distractors | `ALI` | support separation、distractor placement、title/content、support order | `● LOCAL` | A |
| 2WikiMultiHopQA | Wikipedia 多跳 QA | `ALI` | entity chain、alias、support order、path reversal | `● LOCAL` | A |
| Bamboogle | 搜索困难多跳 QA | `ALI` | retrieval path、support addition、known/rare entity | `● LOCAL` | B |
| FRAMES | 多约束、多跳事实 QA | `ALI` | constraint order、source composition、correct clue monotonicity | `● LOCAL` `google/frames-benchmark` | A |
| MultiHopRAG | RAG corpus + multi-hop queries | `ALI` | retrieved-doc set、order、boundary、corroboration | `● LOCAL` | A |
| HoVer | 多跳 fact verification | `DET/ALI` | evidence number、document path、claim polarity | `◐ HUB` | A |
| QASC | 两事实 science composition | `DET/ALI` | fact order、bridge insertion、local vs joint | `● LOCAL` | A |
| ComplexWebQuestions | 复杂 WebQuestions | `ALI` | decomposition、relation order、entity alias | `◐ HUB` 多版本 | B |
| WebQSP / RoG-WebQSP | KG QA 与 reasoning paths | `ALI/MAP` | graph relabel、path order、shortcut edge | `● LOCAL` | A |
| StrategyQA | 隐式多步常识 QA | `DET` | evidence addition、question paraphrase、real/fiction world | `● LOCAL` 多版本 | B |
| MuSR | 长故事多步推理 | `DET` | evidence order、character rename、local/full dissociation | `● LOCAL` | A |

注意：本轮已在 MuSiQue supporting-only 上否掉简单的 one-document vs many-documents 主效应。若再使用 MuSiQue，必须换成新的 decisive contrast，不能原样重跑。

---

# 4. 开放域 QA、实体知识与指称

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| PopQA | 长尾实体事实 QA | `ALI` | entity popularity、alias、facts/entity、known/novel | `● LOCAL` | A |
| WebQuestions | 开放域实体 QA | `ALI` | alias、relation inverse、entity swap | `◐ HUB` | B |
| WebQSP | KG grounded QA | `ALI/MAP` | graph node relabel、path transforms | `● LOCAL` | A |
| ComplexWebQuestions | 复杂实体关系 | `ALI` | decomposition、alias、path depth | `◐ HUB` | B |
| SQuAD v2 | extractive QA + unanswerable | `ALI/DET` | answerability completion、evidence position、abstention | `● LOCAL` | A |
| Natural Questions | Wikipedia QA | `ALI` | title/body、evidence position、answer alias | `○ REMOTE` | B |
| TriviaQA | trivia + evidence | `ALI` | parametric familiarity、context conflict、alias | `○ REMOTE` | A |
| EntityQuestions | relation-balanced entity QA | `ALI` | relation type、entity frequency、alias | `○ REMOTE` | A |
| AmbER | ambiguous entity retrieval / QA | `ALI` | same-name entities、disambiguation evidence、title | `○ REMOTE` | A |
| KILT | knowledge-intensive tasks with provenance | `ALI/HUM` | provenance grouping、retrieval set、source role | `○ REMOTE` | B |
| Protobowl 11–13 | incremental quiz-bowl clues | `ALI` | clue count monotonicity、clue order、early/late evidence | `● LOCAL` | A |
| Protobowl Agent Responses | 多模型历史响应 | existing outputs | 低成本离线 anomaly mining、clue-position curves | `● LOCAL` | A |

Protobowl 特别适合 monotonicity：随着正确 clues 增加，答题本应越来越容易；可以直接寻找非单调 cliff，并利用本地已有多模型输出先离线筛轴。

---

# 5. RAG、知识冲突、证据与事实核查

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| Faithfulness-QA | SQuAD/TriviaQA 反事实实体替换 | `ALI` | aligned/conflict × factual/fictional frame、conflict strength、entity familiarity | `○ REMOTE` | A |
| FEVER | claim verification + evidence | `DET/ALI` | evidence order、support count、claim polarity、source grouping | `◐ HUB` | A |
| FEVEROUS | text + table fact verification | `DET/ALI` | modality grouping、evidence order、table serialization | `● LOCAL` / `◐ HUB` | A |
| HoVer | 多跳 fact verification | `DET/ALI` | evidence chain、document count、support locality | `◐ HUB` | A |
| HL-FEVER | hard long-tail FEVER | `DET` | popularity × evidence、parametric conflict | `● LOCAL` | A |
| QASC | science evidence composition | `DET/ALI` | corroboration、bridge fact、source order | `● LOCAL` | A |
| CounterFact | factual association / editing | `DET/ALI` | parametric familiarity、context overwrite、alias | `○ REMOTE` | B |
| MQuAKE | multi-hop questions after knowledge edits | `ALI` | edit propagation、path、reversibility | `○ REMOTE` | A |
| ConflictBank | context-memory / inter-context conflicts | `DET/ALI` | source role、conflict count、reliability | `○ REMOTE` | A |
| RECALL | external counterfactual knowledge robustness | `DET/ALI` | conflict strength、repetition、source format | `○ REMOTE` | A |
| WhoQA | knowledge conflict QA | `ALI` | context vs parametric answer、entity type | `○ REMOTE` | B |
| LLM Source Preference | source-attributed conflicting facts | dataset-dependent | source identity、order、authority、content swap | `◐ HUB` `JaSchuste/llm-source-preference` | A |
| HaluEval | hallucination / groundedness | `DET/HUM` | evidence presence、answerability、source role | `○ REMOTE` | C |

[Faithfulness-QA](https://arxiv.org/abs/2604.25313) 提供 99,094 个 counterfactual entity substitution 样本，适合把 ontology/world framing 当作 factorial axis；但必须先核查 Hamdi 的 real-versus-imagined 工作是否已覆盖 exact contrast。

---

# 6. 长上下文与文档结构

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| LongBench | 多任务长上下文 | `DET/ALI` | evidence position、query placement、document order、length | `◐ HUB` `THUDM/LongBench` | A |
| LongBench v2 | 更难长上下文 reasoning | `DET/ALI` | position × composition、length scaling | `○ REMOTE` | B |
| MoreDocsSameLen | 固定总长度、改变文档数 | `ALI` | document count、support distribution、order | `● LOCAL` | A |
| RULER | synthetic configurable long-context | `DET/MAP` | position、frequency、aggregation、needle count | `○ REMOTE` | A sandbox |
| InfiniteBench | 超长上下文任务 | `DET/ALI` | context length、position、retrieval vs reasoning | `○ REMOTE` | C |
| LooGLE | 长文档理解 | `ALI/HUM` | evidence distance、global/local questions | `○ REMOTE` | B |
| NarrativeQA | 长故事 QA | `ALI/HUM` | event distance、character fan、summary/full text | `○ REMOTE` | B |
| Qasper | 学术论文 QA | `ALI/HUM` | section location、title/abstract/body、evidence grouping | `○ REMOTE` | B |
| MultiFieldQA | 多领域长文 QA | `ALI` | domain × length、document structure | included in LongBench | B |
| PassageCount / PassageRetrieval | 长上下文合成任务 | `DET` | repetition、position、document IDs | included in LongBench | A sandbox |

RULER 等合成数据适合定位 shape 和 mechanism，但不能单独承担自然性。至少需要 LongBench / Qasper / NarrativeQA 中一个外部确认。

---

# 7. 长期记忆、会话历史与状态更新

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| LongMemEval | 多 session memory、更新、时间、abstain | `ALI/DET` | first/current、update path、session order、A→B→A | `○ REMOTE` | A |
| LoCoMo | 长对话记忆与推理 | `ALI/HUM` | session order、speaker/source、temporal distance | `○ REMOTE` | A |
| EgoMemReason | 第一视角记忆推理 | dataset-dependent | event order、identity、temporal path | `◐ HUB` `Ted412/EgoMemReason` | B |
| EgoLife | 长时第一视角多模态记忆 | `HUM/ALI` | modality、event distance、source | `◐ HUB` `lmms-lab/EgoLife` | C |
| MemoryBank | 长期对话 memory | `HUM` | update/retraction、speaker identity | `○ REMOTE` | C |
| PersonaChat / Persona-MME | persona facts 与一致性 | `HUM/DET` | fact update、persona source、contradiction、reversibility | `◐ HUB` Persona-MME | B |
| StreamingBench | 流式长期交互 | dataset-dependent | arrival order、current state、history length | `○ REMOTE` | B |
| Narrative state tracking subsets | 事件与 object state | `ALI` | direct/detour same endpoint、independent updates | 多来源 | A |

[LongMemEval](https://arxiv.org/abs/2410.10813) 明确覆盖 information extraction、multi-session reasoning、temporal reasoning、knowledge updates 与 abstention，最适合 path independence 主线。

---

# 8. 时间推理与动态知识

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| TempReason | 时间知识 QA | `ALI` | timestamp translation、before/after equivariance、update recency | `○ REMOTE` | A |
| TimeQA | 时间约束 QA | `ALI` | event order、date format、time shift | `○ REMOTE` | A |
| SituatedQA | 时间/地点变化事实 | `ALI` | reference date、current vs historical query | `○ REMOTE` | B |
| TGQA | 时间图 QA | `DET/MAP` | graph time shift、path reversal、interval scaling | `○ REMOTE` | A |
| TORQUE | event temporal ordering | `DET` | sentence order、event swap、before/after mapping | `○ REMOTE` | B |
| MATRES | event temporal relations | `DET` | clause permutation、relation inversion | `○ REMOTE` | B |
| TimeDial | 对话时间常识 | `DET` | time expression equivalence、speaker turn | `○ REMOTE` | B |
| Dynamic knowledge QA / TempLAMA | 随时间变化的事实 | `ALI` | cutoff、update/retraction、current/past | `○ REMOTE` | B |

日期平移 transformation 必须自动排除闰日、月份长度、星期与时区等会改变语义的样本。

---

# 9. 信念、知识、Theory of Mind 与社会推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| ToMi | 一阶/二阶 false belief | `DET` | agent/narrator query、story order、entity swap | `○ REMOTE` | A |
| FANToM | 复杂对话 ToM | `DET/ALI` | information access、speaker order、belief depth | `○ REMOTE` | A |
| Hi-ToM | 高阶 ToM | `DET` | nesting depth、identity × scope、scale | `○ REMOTE` | A |
| OpenToM | 开放场景 ToM | `ALI/HUM` | event order、agent knowledge boundary | `○ REMOTE` | B |
| BigToM | 大规模可控 ToM | `DET/MAP` | world state、perceptual access、agent swap | `○ REMOTE` | A |
| SocialIQA | 社会常识 MCQA | `DET` | entity/role swap、perspective query | `○ REMOTE` | B |
| MuSR | murder/motive/object placement reasoning | `DET` | local/full、character rename、belief/action | `● LOCAL` | A |
| CommonsenseQA | 常识 MCQA | `DET` | option order、entity replacement、world frame | `● LOCAL` | B |
| Moral Stories / ETHICS subsets | 规范判断 | `DET/HUM` | role reversal、entity swap、order | `○ REMOTE` | C |

ToM 数据特别容易出现 Yes/No 默认偏置。必须同时做 agent swap、truth-value balance 与 same-surface positive controls。

---

# 10. 现实、虚构、引用、指令与信息世界

该领域没有一个现成 benchmark 能覆盖所有 ontology relations，优先从已有 QA / narrative 数据做最小 framing，而不是自造大规模哲学题。

| Dataset / source | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| Faithfulness-QA | 现实知识冲突阅读 | `ALI` | factual/fictional/quoted frame、frame enter/exit | `○ REMOTE` | A |
| SQuAD / TriviaQA conflict pairs | 文章内答案 | `ALI` | claim scope、narrator attribution、reality query | SQuAD `● LOCAL` | A |
| NarrativeQA | fiction 内事件与人物 | `ALI/HUM` | in-world/out-of-world query、nested narration | `○ REMOTE` | B |
| ToMi / BigToM | narrator 与 agent worlds | `DET/MAP` | world boundary、identity substitution | `○ REMOTE` | A |
| FEVER | claim vs quoted claim | `DET` | use/mention、quote/assert，但必须重新验证 gold | `◐ HUB` | B |
| Public-domain fiction corpora | story world | `HUM` | real entity embedded in fiction、frame depth | `○ REMOTE` | C |
| GOLEM narrative ontology resources | fictional entity ontology | structured | entity type、story-world membership | `○ REMOTE` | C |

该矿区机制潜力高，但 collision 风险也最高。Hamdi 的 real-versus-imagined 工作必须在任何 GPU 扩展前完成 exact-scope audit。

---

# 11. 指令遵循与可验证约束

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| IFEval | 可验证自然语言约束 | `RULE` | independent constraint order、redundancy、serialization | `○ REMOTE` | A |
| IFBench | 58 类 OOD verifiable constraints | `RULE` | seen/unseen constraint、composition、order | `○ REMOTE` | A |
| FollowBench | 多级指令复杂度 | `RULE/HUM` | constraint count、nesting、position | `○ REMOTE` | B |
| Multi-IF | 多语言 instruction following | `RULE` | language equivariance、constraint order | `○ REMOTE` | A |
| ComplexBench | 复杂指令遵循 | `RULE/HUM` | scope、constraint composition、redundancy | `○ REMOTE` | B |
| InfoBench | instruction following 综合评估 | `HUM/JUDGE` | order、paraphrase、constraint categories | `○ REMOTE` | C |
| COLLIE | compositional language instructions | `RULE` | composition、label mapping、depth | `○ REMOTE` | B |
| CELLO / constraint benchmarks | 长形式约束 | `RULE` | count、interaction、reversibility | `○ REMOTE` | B |

[IFBench](https://arxiv.org/abs/2507.02833) 强调对未见过的可验证约束进行泛化，可避免只在 IFEval 已被训练过的 constraint types 上发现“现象”。

---

# 12. Tool use、function calling 与 agent state

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| BFCL V4 | single/multi-turn tool calling、memory、format | `DET/RULE` | tool/schema order、rename、irrelevant tools、rollback、format | `○ REMOTE` | A |
| ToolBench | 大规模 API tool use | `DET/HUM` | tool set、schema similarity、path | `○ REMOTE` | B |
| APIBank | API planning / calls | `DET` | API rename、parameter order、irrelevant API | `○ REMOTE` | A |
| τ-bench | 真实领域 agent interaction | environment | state path、tool order、rollback、policy | `○ REMOTE` `△ SPECIAL` | B |
| ToolSandbox | stateful tool use | environment | create/delete、permission、side effects | `○ REMOTE` `△ SPECIAL` | A |
| GTA | general tool agents | `DET/HUM` | tool composition、schema order | `○ REMOTE` | B |
| NexusRaven function calling | function selection | `DET` | function rename、similar distractors | `○ REMOTE` | B |
| AgentBench | 多环境 agents | environment | path independence、history、tool availability | `○ REMOTE` `△ SPECIAL` | C |

[BFCL V4](https://gorilla.cs.berkeley.edu/leaderboard) 已经包含 memory 与 format sensitivity categories，因此使用 BFCL 时不能把“测试 tool schema 格式敏感”本身当 novelty；要寻找更具体的 interaction、reversibility 或 dissociation。

---

# 13. 代码生成、程序理解与软件修复

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| HumanEval / HumanEval+ | 函数生成 | execution | alpha-renaming、docstring paraphrase、correct-test monotonicity | `○ REMOTE` | A |
| MBPP / MBPP+ | 简短程序生成 | execution | 与 HumanEval 相同，跨分布验证 | `○ REMOTE` | A |
| LiveCodeBench | 时间切分竞赛代码生成 | execution | type hints、examples、constraint order、reasoning mode | `◐ HUB` | A |
| CRUXEval | input/output 程序推理 | `DET` | variable rename、statement order、inverse query | `○ REMOTE` | A |
| BigCodeBench | 实用 API code generation | execution | import order、API alias、tests、tool docs | `○ REMOTE` | B |
| EvalPlus | HumanEval+/MBPP+ evaluator | execution | 用作严格 scorer，不是 source distribution | `○ REMOTE` | A infrastructure |
| SAFIM | fill-in-the-middle code | execution / exact | equivalent serialization、function order、identifier rename | `● LOCAL` | A |
| DS-1000 | data-science code | execution | API alias、input schema、correct examples | `○ REMOTE` | B |
| RepoBench | repository-level completion | execution/exact | file order、dependency distance、path | `○ REMOTE` | B |
| SWE-bench Verified | 真实 issue repair | tests | file/order、additional tests、patch reversibility | `○ REMOTE` `△ SPECIAL` | C |
| CodeContests | 竞赛编程 | execution | constraints、examples、hint monotonicity | `○ REMOTE` | B |

代码任务必须用执行结果作主 scorer；字符串相似度不能承担现象晋级。

---

# 14. 因果、反事实与干预推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| CLadder | 因果层级推理 | `DET/MAP` | variable relabel、irrelevant interventions、graph isomorphism | `○ REMOTE` | A |
| CRASS | 反事实常识 reasoning | `DET` | entity swap、minimal-change、world frame | `○ REMOTE` | B |
| COPA | 因果选择 | `DET` | cause/effect inversion、option permutation | `○ REMOTE` | B |
| CausalBench | 多类 causal reasoning | `DET/HUM` | graph symmetries、intervention locality | `○ REMOTE` | B |
| Counterfactual Story / TimeTravel | 故事反事实改写 | `HUM/JUDGE` | path、minimal change、world consistency | `○ REMOTE` | C |
| MQuAKE | knowledge edit propagation | `ALI` | intervention propagation、rollback、multi-hop | `○ REMOTE` | A |
| CausalQA / causal graph synthetic sets | graph QA | `DET/MAP` | node permutation、edge reversal、do-intervention | `○ REMOTE` | A sandbox |

优先选择 graph-grounded 且 `MAP` gold 的数据；开放式 counterfactual story 不适合第一轮 deterministic anomaly ranking。

---

# 15. 空间、导航与关系推理

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| StepGame | 多步二维空间关系 | `DET/MAP` | rotation、mirror、translation、entity swap、path length | `○ REMOTE` | A |
| SpartQA | 文本空间 QA | `DET` | object rename、relation inverse、sentence order | `○ REMOTE` | A |
| SpaRTUN | spatial reasoning | `DET` | reference frame、relation composition | `○ REMOTE` | B |
| SpatialSense | 空间 relation classification | `DET` | subject/object swap、inverse relation | `○ REMOTE` | B |
| ReSQ | realistic spatial questions | `DET/ALI` | viewpoint、entity swap、language variation | `○ REMOTE` | B |
| bAbI positional reasoning | 合成位置推理 | `DET/MAP` | graph transformations、path | `○ REMOTE` | A sandbox |
| Navigation / BBH | 网格导航 | `DET/MAP` | rotation、inverse actions、detour same endpoint | `○ REMOTE` | A |
| MA-EgoQA | 第一视角空间 / 行为 QA | dataset-dependent | viewpoint、temporal order、identity | `◐ HUB` | C |

空间任务天然适合 equivariance，尤其 `90°/180°/270°` rotation curves；这比只比较 left/right 更容易暴露非线性方向 gate。

---

# 16. 表格、图表、文档与结构化输入

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| WikiTableQuestions | 表格 QA | `ALI` | row/column permutation、sort、serialization | `○ REMOTE` | A |
| TabFact | 表格 fact verification | `DET` | row order、column order、header alias | `○ REMOTE` | A |
| HiTab | hierarchical table QA | `ALI` | hierarchy serialization、row grouping、depth | `○ REMOTE` | B |
| FeTaQA | free-form table QA | `HUM/ALI` | row order、evidence grouping | `○ REMOTE` | C |
| OTT-QA | open-domain table+text QA | `ALI` | modality boundary、retrieval source order | `○ REMOTE` | B |
| FinQA | financial table + numerical reasoning | `DET` | unit scaling、row order、program serialization | `○ REMOTE` | A |
| TAT-QA | table-and-text financial QA | `DET/ALI` | text/table source role、unit、order | `○ REMOTE` | A |
| ChartQA | chart visual QA | `DET/ALI` | axis order、unit, color mapping、resolution | `○ REMOTE` | A multimodal |
| DocVQA | 文档视觉 QA | `ALI` | layout、resolution、page order | `○ REMOTE` | B multimodal |

表格 row permutation 只有在没有依赖顺序、排名或相邻关系时才是 strict invariant；validator 必须识别这些题型。

---

# 17. 多模态与视觉—文本组合

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| MMMU | 多学科视觉推理 | `DET` | modality ablation、question/option order、resolution | `○ REMOTE` | B |
| MathVista | 视觉数学推理 | `DET/ALI` | image/text clue、unit、diagram transform | `○ REMOTE` | A |
| MathVision | 高难视觉数学 | `DET/ALI` | resolution、diagram/text composition | `● LOCAL` | A |
| ChartQA | 图表 QA | `DET/ALI` | color / legend permutation、axis swap、resolution | `○ REMOTE` | A |
| DocVQA | 文档图像 QA | `ALI` | layout、OCR、page order | `○ REMOTE` | B |
| TextVQA | 图中文字 QA | `ALI` | OCR text placement、question order | `○ REMOTE` | B |
| VQAv2 | 通用视觉 QA | `ALI` | image mirror、entity/color swap | `○ REMOTE` | B |
| BLINK | core visual perception | `DET` | mirror、rotation、viewpoint | `○ REMOTE` | A |
| Winoground | compositional image-text matching | `DET` | caption swap、entity/relation equivariance | `○ REMOTE` | A |
| SugarCrepe | compositionality negatives | `DET` | relation swap、attribute swap | `○ REMOTE` | B |
| MMBench | 多维视觉能力 | `DET` | option order、language、image/text role | `○ REMOTE` | B |
| Persona-MME | 多模态 persona / identity | dataset-dependent | identity、world/source、memory | `◐ HUB` | C |
| EgoLife / EgoMemReason | 第一视角长期多模态 memory | `ALI/HUM` | time、source、modality | `◐ HUB` | C |

所有图像变换必须保存 edit provenance，并自动验证目标 object、文字和答案没有被裁剪或镜像成不同语义。

---

# 18. 语言学、语义、NLI 与指代

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| BLiMP | 最小对句法可接受性 | `DET` | lexical swap、construction depth、polarity | `○ REMOTE` | B |
| SyntaxGym | targeted syntactic expectations | surprisal | dependency distance、island / scope | `○ REMOTE` | C |
| HANS | NLI heuristic tests | `DET` | subject/object swap、word order、label mapping | `○ REMOTE` | A |
| ANLI | adversarial NLI | `DET` | premise/hypothesis transformations、negation | `○ REMOTE` | B |
| SNLI / MNLI | NLI | `DET` | label permutation、premise order、paraphrase | `○ REMOTE` | B |
| WinoGrande | commonsense coreference | `DET` | entity/gender swap、option order | `○ REMOTE` | A |
| Winograd Schema | coreference | `DET/MAP` | entity swap、clause order | `○ REMOTE` | A |
| GAP | gender-balanced coreference | `DET` | name/gender swap、position | `○ REMOTE` | B |
| OntoNotes coreference | 文档级 coreference | spans | entity rename、mention order、distance | `○ REMOTE` | B |
| SuperGLUE diagnostic tasks | 多类语言推理 | `DET` | 按 phenomenon axis 分层 | `○ REMOTE` | B |

语言学数据可以提供非常严格的 minimal pairs，但必须避免“从已有 construction 名直接找 bias”的旧路线；应横跨多个 constructions 扫共同 relation。

---

# 19. 多语言、翻译与跨语言 equivariance

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| OPUS-100 | 多语言平行语料 | parallel text | language swap、round trip、entity/number invariance | `● LOCAL` de-en config | A |
| FLORES-200 | 多语言翻译评估 | references | language path、script、entity/number preservation | `○ REMOTE` | A |
| XNLI | 跨语言 NLI | `DET` | language equivariance、label mapping | `○ REMOTE` | A |
| XCOPA | 跨语言因果推理 | `DET` | language、cause/effect mapping | `○ REMOTE` | B |
| MGSM | 多语言 GSM8K | `DET` | language × numerical representation | `○ REMOTE` | A |
| Belebele | 多语言阅读理解 | `DET` | language、option permutation | `○ REMOTE` | B |
| TyDi QA | 多语言 QA | `ALI` | language、script、evidence position | `○ REMOTE` | B |
| PAWS-X | 跨语言 paraphrase | `DET` | word order、translation path | `○ REMOTE` | B |
| Multi-IF | 多语言 instruction following | `RULE` | language × constraint type | `○ REMOTE` | A |

翻译 round-trip 不是严格 invariance，除非只评价数字、实体、代码或结构化 slot 等可证明保持的字段。

---

# 20. 不确定性、拒答与答案存在性

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| SQuAD v2 | answerable/unanswerable QA | `DET/ALI` | missing evidence completion、position、abstain option | `● LOCAL` | A |
| Synthetic Unanswerable Math | 不充分数学题 | `DET` | sufficient fact addition、history/path | `● LOCAL` | A |
| SelfAware | answerability / unknown detection | `DET` | evidence addition、domain、familiarity | `○ REMOTE` | B |
| UnknownBench | unknown / unanswerable | `DET/HUM` | parametric familiarity、source context | `○ REMOTE` | B |
| AbstentionBench | abstention calibration | `DET` | abstain option、evidence strength、role | `○ REMOTE` | B |
| GPQA / MMLU with abstain | hard QA | `DET` | forced choice vs abstain、elimination | GPQA/MMLU `● LOCAL` | A |
| OneRuler absence variants | long-context answer absence | `DET` | needle presence、position、language | `○ REMOTE` | B |

answerable 与 unanswerable 两类必须平衡；否则模型的 default abstain / default answer 足以伪造大效应。

---

# 21. 安全、拒绝与 benign over-refusal

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| XSTest | exaggerated safety / over-refusal | `DET/HUM` | quote/use、fiction/fact、role、benign paraphrase | `○ REMOTE` | B |
| OR-Bench | over-refusal | `DET/HUM` | harmless content × surface risk cues | `○ REMOTE` | B |
| StrongReject | jailbreak / refusal evaluation | rubric | role/source、encoding、fiction | `○ REMOTE` | C |
| HarmBench | harmful behavior benchmark | classifier/rubric | metadata、role、format | `○ REMOTE` | C |
| WildGuardMix | safety classification | `DET` | role/source、language、quote | `○ REMOTE` | B |
| BeaverTails | safety preference / classification | `DET/HUM` | category、paraphrase、role | `○ REMOTE` | C |
| Do-Not-Answer | refusal QA | labels | content-preserving format / source | `○ REMOTE` | B |
| AdvBench | adversarial harmful prompts | rubric | 不用于首轮自然 anomaly mining | `○ REMOTE` | C |

安全策略本来就可能规范性地依赖 role、source 与 intent。只有 gold policy 明确要求 invariant 时，才能称 broken invariant。

---

# 22. 医疗、科学与高风险领域

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| MedEinst | 医疗诊断、evidence revision | `ALI` | counterevidence strength、order、diagnosis revision | `● LOCAL` | A |
| MedQA | 医学 MCQA | `DET` | option order、verified elimination、evidence hints | `○ REMOTE` | B |
| PubMedQA | 生物医学 yes/no/maybe | `DET` | abstract sentence order、evidence addition | `○ REMOTE` | B |
| MedMCQA | 医学 MCQA | `DET` | option / hint axes | `○ REMOTE` | B |
| SciQ | science QA + support | `DET` | support addition/duplication、wrong option removal | `● LOCAL` | C, 已跑 null |
| ARC Challenge | 科学 MCQA | `DET` | option、evidence、question representation | `○ REMOTE` | B |
| QASC | science two-fact reasoning | `DET/ALI` | composition、evidence order | `● LOCAL` | A |
| GPQA | 研究生科学 QA | `DET` | difficult MCQA axes | `● LOCAL` | A |

医疗任务只做行为研究，不把实验结果当临床建议。counterevidence transformation 必须来自病例 gold 或专业标注，不能由模型自行编造。

---

# 23. 情感、偏好与自然文本分类

| Dataset | 子领域 / 任务 | Gold | 适合的 relation / axis | 状态 | 优先级 |
|---|---|---:|---|---|---:|
| Yelp Review Full | 五级情感 | `DET` | sentence order、irrelevant clause、rating-equivariant lexical swap | `● LOCAL` | B |
| SST-2 / SST-5 | 情感分类 | `DET` | negation、clause order、entity rename | `○ REMOTE` | B |
| IMDB | 长评论情感 | `DET` | evidence position、length、paragraph order | `○ REMOTE` | B |
| AG News | topic classification | `DET` | sentence order、entity replacement | `○ REMOTE` | C |
| DBpedia | ontology classification | `DET` | entity rename、description order | `○ REMOTE` | C |
| Amazon Reviews | rating / sentiment | `DET` | length、position、duplication | `○ REMOTE` | C |

该领域容易只发现普通 robustness；只有出现强非线性、选择性交互或跨尺寸异常才值得晋级。

---

# 24. 本地优先队列

## Tier A0 — 不下载即可立即开始

| 领域 | Dataset | 推荐第一轴 | 原因 |
|---|---|---|---|
| 增量证据 | Protobowl + existing model responses | clue count / clue position monotonicity | 可先离线筛，多模型历史输出已缓存 |
| 状态 / abstain | Synthetic Unanswerable Math | 补足信息、single-turn vs update path | deterministic “I don't know” gold |
| 多跳组合 | MuSiQue | bridge alias / support separation，需避开已跑 boundary 主效应 | 有 decomposition |
| 多跳事实 | FRAMES | constraint order / correct clue monotonicity | 自然多约束问题 |
| KG / 指称 | WebQSP / RoG-WebQSP | graph path、alias、entity relabel | 可程序化 relation |
| 长上下文 | LongBench hub snapshot | position × task type | 先检查 snapshot 完整性 |
| RAG 证据 | HL-FEVER / FEVEROUS / HoVer | popularity × evidence、text/table source | 有事实核查 gold |
| 数学 | GSM8K × GSM-Hard | unit / magnitude / hint | 两个现成对照分布 |
| 代码 | LiveCodeBench / SAFIM | identifier rename、correct tests、serialization | execution scorer |
| 医疗 revision | MedEinst | evidence strength / order | 自然病例，但需专业 gold 审计 |
| 多语言 | OPUS-100 de-en | entity/number preservation | 本地 processed config |
| 视觉数学 | MathVision | text/image relation | 已缓存，但需要 VLM server |

## Tier A1 — 小下载、高回报

```text
FOLIO
ProofWriter
IFEval / IFBench
LongMemEval
StepGame
Faithfulness-QA
BFCL V4
HumanEval+ / MBPP+
ToMi / BigToM
TabFact / WikiTableQuestions
```

## Tier C — 暂缓

```text
SWE-bench Verified：执行成本高
大型多模态集合：图像与 VLM 基础设施成本高
开放式 counterfactual stories：gold 不稳定
安全 jailbreak 数据：规范关系与 evaluator 复杂
需要 LLM judge 的 generation benchmark：容易把 judge artifact 当现象
```

---

# 25. 下载与注册前检查模板

```markdown
## Dataset registration

- canonical name:
- official paper / repository:
- license:
- task domain:
- subdomain:
- official configs / splits:
- expected row counts:
- local cache status:
- schema:
- gold type: DET / MAP / ALI / RULE / HUM / JUDGE
- official evaluator:
- contamination risks:
- natural unit of pairing:
- valid transformations:
- transformations that change semantics:
- capability-floor model:
- maximum smoke budget:
```

每个新下载数据集注册后，才允许写 transform。不要先批量下载几十个大型 corpus，再决定是否可用。

---

# 26. 给小模型的 dataset 选择指令

```text
先读 DATASET_CATALOG.md。

选择数据集时：
1. 优先 ● LOCAL，其次 ◐ HUB，最后 ○ REMOTE。
2. 优先 DET / MAP / RULE gold。
3. 先检查本地 row count、schema、split 与 snapshot 完整性。
4. 从该数据集所在领域表中选择 3–5 个合法 relation axes。
5. 不得在同一轮混合多个领域、多个 scorer 或多个 task interface。
6. 先用 30–50 paired items；不满足晋级门槛就换轴，不换更弱模型。
7. 若数据集已有工作直接研究该轴，只允许测试未覆盖的 interaction / shape / dissociation。
8. 将新数据集的注册信息写入本 catalog，再开始大规模运行。
```
