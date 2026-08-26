# Rejected Interpretability Candidates

这里记录**一开始确实值得认真考虑，但后来被硬证据砍掉或明确降级**的候选题。

它和 `archive/` 不同：

- `archive/`：已经正式建项目、写过 G0/代码/计划，后来终止；
- `rejected_candidates/`：多数还停留在搜题 / paper audit 阶段，就因为行为、artifact、novelty 或 exact mechanism collision 被提前杀掉。

目的：

1. 防止后续搜题重新发明已经判死的问题；
2. 记录每类题真正的死亡原因，而不只记“感觉不行”；
3. 在新候选出现时，强制与历史失败做 nearest-neighbor 对照；
4. 保留对未来 search strategy 有用的负结果。

## Rules

- 每个 numbered document 最多 **10 个候选**；
- 满 10 个后冻结，下一批写入下一个文档；
- 只有“最初确实有希望、后来被证据砍掉”的题进入；
- 随手 brainstorm 后立刻觉得无聊/不自然的题不记录；
- 如果一个 rejected candidate 未来因为**新的自然行为证据、公开 artifact 或新的 decisive contrast**重新变得可行，必须明确写 resurrection reason，不能直接删掉旧记录。

## Death codes

- `NO_NATURAL_BEHAVIOR`
- `DIRECT_MECHANISM_COLLISION`
- `NARRATIVE_COLLISION`
- `ARTIFACT_FAILURE`
- `NATURALNESS_FAILURE`
- `METHOD_COLLISION`

## Documents

- [`001.md`](./001.md) — 第一批 10 个：role-value binding、facts-vs-shortcuts、fan effect、VLM conflict、self-correction、tool irrelevance、irrelevant context、negation、social compliance、overthinking。

后续新增候选从 `002.md` 开始。
