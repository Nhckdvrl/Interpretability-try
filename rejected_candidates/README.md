# Rejected Interpretability Candidates

这里记录**一开始确实值得认真考虑，但后来被硬证据砍掉或明确降级**的候选题。

它和 `archive/` 不同：

- `archive/`：已经正式建项目、写过 G0/代码/计划，后来终止；
- `rejected_candidates/`：多数还停留在搜题 / paper audit 阶段，就因为行为、artifact、novelty、naturalness、surprise 或 exact mechanism collision 被提前杀掉。

## Search organization: one domain at a time

后续搜题**不再横向混扫若干互不相关的题**，而是一次锁定一个现象领域，尽量把该领域的候选空间扫透：

1. 先定义当前 domain 及其自然现象边界；
2. 广搜该领域已有 behavior / benchmark / mechanism / method 工作；
3. 对每个最初看起来值得认真考虑的题做 collision audit；
4. 被 kill 的题全部写入该 domain 的 rejection log；
5. 只有仍然存活的题才进入跨领域最终候选池；
6. 以后重新进入该领域时，必须先读对应 rejection log，避免重新发明旧题。

这套目录的目标是逐渐形成一个**按领域组织的负知识库**：不仅记录“哪些题不行”，还记录“为什么不行、以后看到什么相似题应该立即警觉”。

## Mandatory rejection fields

每个值得记录的 rejected candidate 至少写：

- **Natural question**：不提解释工具也能成立的一句话问题；
- **Why it initially looked good**；
- **Kill evidence**：行为证据 / 论文 collision / artifact failure 等；
- **Death code**；
- **Nearest-neighbor warning**：以后哪些换名、换 benchmark、换模型的版本也不应复活；
- **Resurrection condition**：只有出现什么新的自然行为证据 / artifact / decisive contrast 才值得重开。

## Surprise test

在 README 的硬门槛之外，再做一个高阶筛选：

> **如果最终结果成立，它是否可能让读者产生“原来模型是这样坏掉的 / 原来直觉错了”的感觉？**

如果无论结果如何都高度符合默认直觉，例如“语义不同所以表示不同”“更灵活的方法比线性方法拟合更准”，即使 technically novel，也应显著降级。

这个标准来自实际选题反馈：研究问题本身必须有趣，结果最好能打破一个自然默认直觉，而不是做完后让人觉得理所当然。

## Death codes

- `NO_NATURAL_BEHAVIOR`
- `DIRECT_MECHANISM_COLLISION`
- `NARRATIVE_COLLISION`
- `ARTIFACT_FAILURE`
- `NATURALNESS_FAILURE`
- `METHOD_COLLISION`
- `LOW_SURPRISE`

## Domain logs

- [`agent_tool_use.md`](./agent_tool_use.md) — Agent / tool-use / execution failures
- [`cognitive_logical_reasoning.md`](./cognitive_logical_reasoning.md) — formal / conditional / logical reasoning phenomena
- [`cognitive_decision_making.md`](./cognitive_decision_making.md) — economic choice, legal judgment, anchoring, authority, risk, sunk cost
- [`factuality_information_conflict.md`](./factuality_information_conflict.md) — false premises, answerability, misinformation, source credibility, repetition
- [`multimodal_grounding.md`](./multimodal_grounding.md) — VLM perception–knowledge conflict and counterfactual visual grounding
- [`001.md`](./001.md) — **legacy mixed-domain batch**，保留历史记录，不再继续追加。包含 role-value binding、facts-vs-shortcuts、fan effect、VLM conflict、self-correction、tool irrelevance、irrelevant context、negation、social compliance、overthinking。

后续新增 rejection **只进入对应 domain log**；如果出现新的领域，就新建 `<domain>.md`。旧 `001.md` 不删除，作为第一轮搜题历史快照。