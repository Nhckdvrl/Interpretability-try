# 领域 10：代码语义、对象身份与结构化状态

状态：`15 candidate cards — UNTESTED`
母问题：当自然语言表面、测试信号和程序真正执行语义冲突时，模型表示并使用的是“程序做什么”，还是“程序看起来像什么”？

## 顶会边界

代码生成准确率、执行 trace 有用性、代码评审和 repository completion 都很拥挤：[CodeScope](https://aclanthology.org/2024.acl-long.301/)、[Do Code Semantics Help?](https://aclanthology.org/2025.findings-emnlp.548/)、[CodeJudge](https://aclanthology.org/2024.emnlp-main.1118/) 与 [RepoCoder/RepoBench](https://aclanthology.org/2023.emnlp-main.151/) 已覆盖宽问题。这里不研究“模型不懂代码”，而寻找**两种状态本体或两种 authority 冲突时的定向错路由**；首选真实仓库片段和执行 oracle，不用为了现象手写一批玩具程序。

## 优先数据架

| 数据 | 自然单元 | 适合轴 | 可得性 |
|---|---|---|---|
| [SWE-bench](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html) | 真实 GitHub issue/patch/tests | spec、patch、test、repo state | 公开 |
| [RepoBench/RepoCoder](https://aclanthology.org/2023.emnlp-main.151/) | 真实仓库 completion | stale duplicate、cross-file state | 公开 |
| [CRUXEval](https://github.com/facebookresearch/cruxeval) | 800 个短 Python 函数/I-O | alias、scope、execution | 公开 |
| [CodeScope](https://aclanthology.org/2024.acl-long.301/) | 多语言、多任务、执行评测 | semantics、generation | 公开 |
| [DS-1000](https://proceedings.mlr.press/v202/lai23b.html) | StackOverflow 数据科学题 | copy/view、mutation、API semantics | 公开 |
| HumanEval+ / MBPP+ / LiveCodeBench | 代码与严格 tests | no-op、exception、spec coverage | 公开 |
| Defects4J / BugsInPy / ManySStuBs4J | 真实 bug-fix commits | stale comment、exception、patch effect | 公开 |
| CodeSearchNet / CodeXGLUE | code-doc pairs | docstring/code conflict | 公开 |

---

## CSS-01 — 过期注释压过当前代码

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=LITERATURE-CHECKED`

**一句话矛盾。** 模型能逐行算出代码现在做 B，回答功能或改 bug 时却仍按过期注释里的 A。

**日常例子。** 注释说“按升序排列”，实现后来改成降序；运行结果而非注释决定事实。

**数据与轴。** 从 SWE-bench、Defects4J/BugsInPy、真实 git 历史中找 comment与后续代码不一致的自然 commits；同一 executable code 配当前注释、旧注释、无注释，先做 execution prediction，再做 summary/patch choice。

**晋级 signature。** execution trace/I-O预测正确，功能说明或补丁精确回到 stale comment；移除注释恢复，换无关注释不掉。若连执行也错，属于代码理解不足。

**规模与机制。** 更强模型的自然语言指令先验可能更强，不必被 execution能力压过。A：注释重写语义表示；B：runtime表示正确，task-specific readout选择doc channel。可做 comment/code activation swap。

**碰撞边界。** 文档生成研究不等于“stale documentation recognized yet controls action”；需 exact audit 软件工程中 comment-code inconsistency 工作。

**最便宜证伪。** 先人工审计 30 个真实 commit，不允许自动反转注释造数据；若强模型report/action都跟代码，KILL。

## CSS-02 — 测试全绿被当成需求已经满足

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型正确指出现有测试没覆盖用户要求，却因测试全绿仍宣布补丁正确。

**日常例子。** 测试只检查正数，issue要求也支持空输入；旧测试通过不能证明新需求实现。

**数据与轴。** SWE-bench issue/patch/test，HumanEval+/MBPP+ base-vs-plus tests；分别问 requirement coverage、预测 hidden test、accept/reject patch。比较绿测试+覆盖、绿测试+缺口、红测试。

**晋级 signature。** coverage缺口和反例输入均能正确给出，acceptance仍随 green token走；加入它自己给出的反例后才翻转更强。若只是没理解 issue，KILL。

**规模与机制。** RL/agent训练强奖励“tests passed”，可能形成独立完成 gate。A：green status覆盖spec model；B：spec/bug model存在但 judge readout只读test channel。机制可导出 coverage-aware stopping。

**碰撞边界。** CodeJudge/validation gap相邻；独特性是 **known test incompleteness + green-build semantic override**。

**最便宜证伪。** 用公开 base/plus test差异的 20 题离线评审；若acceptance由自己给出的counterexample正确控制，KILL。

## CSS-03 — 有补丁不等于有行为变化

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型能解释一个 diff 是 no-op，工作流里却只因“patch applied”就把问题标成已修复。

**日常例子。** 改格式、改死代码或把表达式换成等价表达式，不会修复运行时 bug。

**数据与轴。** SWE-bench patches、program-repair datasets；从真实代码做语义保持 edits（格式、rename、unreachable branch）并使用执行 oracle，比较 no-op/partial/fixing patch。先问行为等价，再做 completion judgement。

**晋级 signature。** equivalence判断正确，任务状态仍 `diff exists→fixed`；错误随 patch framing/size出现而非内容难度。

**规模与机制。** agent轨迹把 edit action当进度信号，强模型同样可能过早终止。A：patch-event触发completion；B：semantic verifier正确但 planner未调用/未使用。

**碰撞边界。** 不是普通 patch correctness；核心是 no-op recognition/action gap和 edit-event gate。

**最便宜证伪。** 20 个真实函数的已验证等价 patches；若模型一贯拒绝 no-op，KILL。

## CSS-04 — happy path 正确，已知异常路径仍被当成成功

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道给定输入会触发异常、没有 catch，最终仍预测函数返回 happy-path 的值。

**数据与轴。** CRUXEval、BugsInPy、HumanEval+；自然函数中 `normal / boundary / exception-triggering` inputs，先定位触发语句，再问 observable outcome（return/raise/side effect）。

**晋级 signature。** exception condition和控制流报告正确，output prediction稳定越过 exception继续执行；错误落到异常后的 nominal return。

**规模与机制。** 代码补全训练偏正常返回，exception control token可能未送达 output simulator。A：execution state未终止；B：终止正确，answer decoder偏return槽。

**碰撞边界。** execution reasoning宽问题已做；需 exception-termination特异路径及跨语言/尺寸结构。

**最便宜证伪。** 在 CRUXEval 自动筛现成 raise/exception代码；若错误与总体execution准确率无分离，HOLD。

## CSS-05 — 同名变量跨作用域串值

**元数据。** `priority=B; naturalness=N2; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型能指出内外层 `x` 是不同绑定，执行预测时却把内层值带到外层。

**数据与轴。** CRUXEval、CodeScope、真实短函数；从原生 shadowing examples配对 unique-name alpha-renaming（程序语义不变），测 binding explanation、逐步值与输出。

**晋级 signature。** binding report正确，只有执行中产生 inner→outer或outer→inner的定向串槽；alpha rename选择性修复。若rename普遍改善可读性而无错误落点，降为复杂度效应。

**规模与机制。** 变量名诱导复制/检索路径是token binding问题，可跨尺寸保留。A：同token共享value carrier；B：scope表示存在，late value read按name检索。

**碰撞边界。** synthetic variable binding研究很多；必须从自然代码出发并显示 report/use解离，而非再做rename robustness。

**最便宜证伪。** 从 CRUXEval 抽 30 个真实shadowing片段；若样本太少或仅玩具，HOLD。

## CSS-06 — 相等的值被误当成同一个对象

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 两个对象当前内容相同但彼此独立，模型看到修改一个后却把另一个也改了。

**日常例子。** 两份内容相同的购物车不是同一购物车；改其中一份不会改另一份。

**数据与轴。** DS-1000、CRUXEval、real Python/JS code；正交 `equal distinct objects / aliased same object` × mutation，先问 identity/equality，再预测两个值。使用实际执行oracle。

**晋级 signature。** identity判断正确，mutation output仍出现 equal→alias spillover；反向 alias→independent也单列。错误随 equality而非名称/位置。

**规模与机制。** identity与value equality是基础但训练中表面高度共现；更强模型可能更会解释概念而 simulator仍压缩状态。A：heap nodes合并；B：nodes分开，mutation propagation按value similarity。

**碰撞边界。** 传统code reasoning会测alias，但未必研究“knows identity / simulates equality”解离与机制；先审计 ICLR/ICML code MI。

**最便宜证伪。** 30 个自然库操作片段，避免 `a=[]; b=[]` 玩具；若concept和execution同步，KILL。

## CSS-07 — 真正的别名关系没有传播修改

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 两个名字明确指向同一对象，模型说它们是 aliases，却只更新被直接写到的名字。

**数据与轴。** 与 CSS-06 共用 DS-1000/CRUXEval；包含 dataframe views、mutable defaults、dictionary/list aliases。比较 alias、shallow copy、deep copy。

**晋级 signature。** alias/copy类型报告正确，post-state仍按变量名分裂；浅拷贝只传播嵌套层可形成层级曲线。

**规模与机制。** 语言模型自然以变量token为state slots，heap identity需额外绑定。A：引用图未形成；B：图可解码但mutation updater局部写name slot。

**碰撞边界。** 可与 CSS-06 合并成 equality–identity 双重分离论文；单边小错误不够。

**最便宜证伪。** 先测 pandas/numpy view/copy真实问答；若模型对API知识不足，不能归因identity，KILL。

## CSS-08 — 删除后的定义仍像在仓库中存在

**元数据。** `priority=A; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道函数已在当前版本删除，补全或调用时仍复活旧 API。

**日常例子。** 当前分支删除了 `legacy_send()` 并迁移到 `send()`；旧文档/邻近文件仍提到前者。

**数据与轴。** SWE-bench、RepoBench、真实 git commits；使用删除/rename API 的 pre/post snapshots，当前代码相同但是否提供历史/旧文档不同。问current API set、completion与patch。

**晋级 signature。** current absence与迁移说明正确，生成仍稳定调用deleted symbol；编译错误终点明确。若纯训练记忆导致旧API且上下文未说明删除，不能算本卡。

**规模与机制。** 规模增加参数知识和旧API熟悉度，可能加强冲突。A：repository retriever把历史mention当current definition；B：current symbol table正确但 decoder走高频parametric API。

**碰撞边界。** context-parametric conflict/RAG code completion相邻；独特性是 current symbol-table report与deleted-symbol resurrection。

**最便宜证伪。** 20 个真实API迁移commit；若加current imports后错误完全消失，可能仍只是retrieval不足，HOLD。

## CSS-09 — 回滚/异常后，内存或数据库状态没有回到原点

**元数据。** `priority=A; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型正确说事务已回滚，预测变量或数据库时仍保留中途写入。

**数据与轴。** BugsInPy/Defects4J中 transaction/context-manager cases，AppWorld execution code；`commit / exception+rollback / caught exception without rollback`，用真实运行oracle。

**晋级 signature。** rollback scope与触发条件正确，post-state精确等于中途state而非initial；同终态 direct路径正常。

**规模与机制。** current-state canonicalization与event-log memory冲突，和ATW-09可跨自然语言agent/代码形成外部确认。A：state simulator只append writes；B：rollback state存在但answer readout取最近write。

**碰撞边界。** 若与ATW-09同一机制，可形成跨界验证而非另立论文；若代码端不成立不影响agent卡。

**最便宜证伪。** 自动筛选含transaction的真实测试；没有足够自然样本则HOLD，不手造简单bank模板。

## CSS-10 — 不可达代码仍影响输出预测

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型知道一段代码永远不会执行，预测输出时仍被其中的值吸引。

**数据与轴。** CRUXEval/CodeScope/real bug corpora；原生 `after return / false branch / impossible guard` 代码，保留/删除/改变 dead-code payload，execution semantics严格不变。

**晋级 signature。** reachability report正确，output错误随dead payload等变；不是长度或最后数字bias，需活分支位置/数字controls。

**规模与机制。** token序列模型可能并行表征所有assignments，control-flow gate晚到。A：dead assignment进入state；B：state正确但 output decoder被last-write表面吸引。

**碰撞边界。** metamorphic code testing可能已覆盖 dead-code insertion；只有 recognition-use、错误等变与电路机制才有空位。

**最便宜证伪。** CRUXEval现成函数中筛 dead branches；若必须大量人工插入才有样本，降低naturalness。

## CSS-11 — 测试名/注释说成功，断言明明失败

**元数据。** `priority=B; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 测试函数叫 `test_success`、注释写“应该通过”，模型也看懂 assertion，仍预测测试会通过。

**数据与轴。** SWE-bench/Defects4J tests；真实 misnamed/stale tests或自然 commit前后，分开 identifier/comment 与 assertion semantics，实际执行oracle。

**晋级 signature。** assertion evaluation正确，test outcome受名称/注释方向吸引；name rename不改程序却翻转预测。若仅弱模型不会执行assert，KILL。

**规模与机制。** identifier携带强意图先验，code execution携带事实。A：name prior提前设outcome；B：execution正确、classification head读semantic label token。

**碰撞边界。** 与CSS-01同族；若只有同一language-vs-code gate应合并，不拆小论文。

**最便宜证伪。** 真实misnamed tests很少时不构造海量假样本；20例不足则HOLD。

## CSS-12 — 后定义覆盖前定义，模型仍执行旧版本

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 同名函数在当前作用域被重新定义，模型能指出“后者生效”，输出仍来自前一个版本。

**数据与轴。** notebooks、DS-1000 stateful cases、真实Python repo/tests；`old→new definition` 与仅new、new→old，问active definition、output、patch。使用 notebook cell execution order而非打乱文本。

**晋级 signature。** active version report正确，execution取old body；错误随初始定义的熟悉度/长度出现，形成 definition inertia。

**规模与机制。** 参数/早期上下文先验与current symbol binding竞争。A：symbol table未overwrite；B：overwrite可读，function simulator检索首次body。

**碰撞边界。** 与 premise order/recency不同；本体是语言规定的动态binding和 notebook真实状态。

**最便宜证伪。** 从公开notebook数据抽现成redefinition；若只在人工短函数出现，KILL。

## CSS-13 — shallow copy 被压成全别名或全独立

**元数据。** `priority=B; naturalness=N3; collision_risk=LOW; stage=IDEA`

**一句话矛盾。** 模型知道浅拷贝“外层独立、内层共享”，执行时却只能把它当完全共享或完全独立。

**数据与轴。** DS-1000、StackOverflow-derived code、CRUXEval扩展；同一 nested object执行 outer mutation与inner mutation，对照alias/deep copy。

**晋级 signature。** copy定义报告正确，两个mutation层级却同向回答；出现离散二模式或随问法切换尤其有解释价值。

**规模与机制。** shallow copy要求层级reference graph，不是规模单调的事实记忆。A：表示只有单bit shared/not-shared；B：层级图存在但mutation router不选择depth。

**碰撞边界。** 比CSS-06/07更具体；若三个卡共享同一现象，应合为“identity graph compression”主候选。

**最便宜证伪。** 真实SO问题30条；若API知识地板导致，换纯语言自带list.copy仍不稳则HOLD。

## CSS-14 — 修复一个调用点，被误当成所有调用点都修复

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型正确找到多个受影响调用点，只改其中一个后却宣布迁移完成。

**数据与轴。** SWE-bench/RepoBench API migrations；真实patch中多call sites，先列affected set，再评partial/full patch。控制重复文本与不同文件。

**晋级 signature。** affected-set report完整，completion judgement却在任何一个salient site被修后触发；漏项精确对应未编辑文件/低显著site。

**规模与机制。** repository理解提升能找到sites，agent stopping仍可能是any-progress gate。A：edit event触发完成；B：set representation存在但 reducer错用existential而非universal。

**碰撞边界。** 普通repo repair失败不够；需 set-known/coverage-judgement错算子的清晰解离。

**最便宜证伪。** 利用SWE-bench gold patch多文件任务的partial patches离线判断；若affected set本身不稳，KILL。

## CSS-15 — 新 API 返回结构已读懂，写代码时仍按旧结构取字段

**元数据。** `priority=B; naturalness=N3; collision_risk=MEDIUM; stage=IDEA`

**一句话矛盾。** 模型正确复述新版返回 `user.profile.name`，生成代码仍访问旧版 `user.name`。

**数据与轴。** SWE-bench真实API migration、RepoBench、library-learning benchmark；新旧schema、current-only、新说明+旧示例，分别测schema QA与code generation。

**晋级 signature。** schema回答正确，代码稳定落到旧field；错误随旧API参数熟悉度或旧example出现，current-only control恢复。

**规模与机制。** 规模越大旧库记忆越强，可能非单调恶化。A：parametric code prior覆盖context schema；B：schema表示正确，code decoder走memorized syntax pathway。

**碰撞边界。** context-parametric conflict和library ICL已有；只有 report/generation解离、版本scale law与可因果路由空位才保留。

**最便宜证伪。** 20个真实breaking API changes；若新schema明确时所有模型都服从，KILL。

## 本领域首轮排序

| 顺位 | 卡 | 主要价值 | 最大风险 |
|---:|---|---|---|
| 1 | CSS-02 green tests override known spec gap | 软件工程极自然、训练信号解释强 | validation文献相邻 |
| 2 | CSS-06/07/13 identity graph compression | 基础本体、双向/层级结构、机制很干净 | 玩具化风险 |
| 3 | CSS-01 stale comment over current code | 普通人易懂、真实git数据可挖 | comment-code工作可能撞车 |
| 4 | CSS-09 rollback ghost | 跨agent/代码外部确认、路径独立 | 自然样本筛选成本 |
| 5 | CSS-08 deleted API resurrection | 规模可能增强、真实仓库 | context-parametric冲突母现象 |
| 6 | CSS-14 known affected set / any-edit completion | set reducer机制、SWE-bench自然 | agent stopping母现象 |

优先把 CSS-06/07/13 视为一个候选族，而不是三篇小题；只有出现 equality、alias、shallow-copy 的结构曲线后再决定名称。

---

## Batch-2 脑暴死亡回填与新 survivor 路由（2026-08-28）

完整账本：[`BATCH2_BRAINSTORM_LEDGER_2026-08-28.md`](BATCH2_BRAINSTORM_LEDGER_2026-08-28.md)。

| 本批主题 | 裁决 | 领域内理由 |
|---|---|---|
| **Dead/unreachable-code influence（作为新的 Batch-2 题）** | `DUPLICATE / ROUTE CSS-10` | 本文件 CSS-10 已完整登记 `reachability report correct → dead payload still affects output`；本轮再想到 dead code 不能另起卡或换名。 |
| **Generic exception happy-path continuation** | `DUPLICATE / ROUTE CSS-04` | 已有 CSS-04 `exception known → nominal return`，不重复。 |
| **Generic concurrency/race confusion** | `NOT-ADDED / F3-RISK` | 若只有 interleaving/race 导致执行预测错误，是普通 execution/state reasoning；若强调历史路径残留又与 CSS-09/ATW-09/F3 重合。 |

### 本领域仍活的 Batch-2 新方向

- **Short-Circuit Side-Effect Leakage**：见 [`audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md`](audits/BATCH2_N0_WORKING_REVIEW_2026-08-28.md)。它不是 CSS-10 的普通 dead-code 版本，只有在 `RHS not executed` 与 expression value 都判断正确、但 post-state 仍加入 RHS side effect 时才独立；目标 operator 是同一 expression 中的 value/effect short-circuit gate。
- **SQL UNKNOWN Interface Collapse**：同上。它不是 F8 generic unknown→false，而是正式第三 truth value `UNKNOWN` 已正确表示后，被 `WHERE`、`CHECK` 等 interface 错误使用同一个 Boolean policy；必须用固定 SQL dialect 的执行 oracle。

**禁止复活。** dead code、exception continuation、race/concurrency 以后先查 CSS-04/CSS-09/CSS-10 和 Batch-2 ledger；若只是换语言、换库或换 readout，不进入新 N0。
