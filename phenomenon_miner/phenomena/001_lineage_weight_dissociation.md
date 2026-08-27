# 001 — 来源谱系识别—证据加权解离

英文工作名：**Lineage–Weight Dissociation**
登记日期：2026-08-27

| 维度 | 当前状态 |
|---|---|
| 行为证据 | `VERIFIED` |
| 一般性 | `CROSS_FAMILY + CROSS_SIZE` |
| 新颖性 | `NARROWED` |
| 可解释性 | `HYPOTHESES` |
| 总体决策 | `HOLD` |

## 一句话现象

> 模型能说出十篇报道都来自同一项民调，做判断时却仍像听到了十份独立证据。

更严格的潜在主张是：

> **规模增长改善了来源谱系识别，却没有相应改善来源谱系的使用。**

## 为什么自然

新闻转载、联合发布、共同引用一项民调、多个医生依赖同一次化验、多个 agent memory 继承同一 tool result，都要求区分“报告数量”和“独立观察数量”。复制或转述报告不应自动增加它的证据权重。

## 已有行为依据

当前实验覆盖 Qwen3 4B/8B/32B、Gemma3 4B/12B 与 Phi-4-mini。多个 matched 条件显示：模型可在显式 probe 中恢复共同来源关系，但在决策中仍偏向被多个二手报道支持的一侧。Qwen 与 Gemma 均包含跨尺寸结果；Phi 提供第三家族验证。

自然 election-poll 范式和模板化来源独立性范式均已运行。Mistral-Small-24B 是边界模型：它能处理依赖证据，却对真正独立多数过度保守，因此不能被隐藏，也不用于否定 Qwen/Gemma/Phi 上的主要行为。

### 复现入口

- 详细历史备忘：[`../candidates/lineage_weight_dissociation.md`](../candidates/lineage_weight_dissociation.md)
- 模板化实验：[`../run_source_independence.py`](../run_source_independence.py)
- 自然人类范式：[`../run_human_consensus.py`](../run_human_consensus.py)
- 原始结果：[`../results/`](../results/)

## 新颖性审计后的修正

不得声称“首次发现模型会把重复或相关证据当作多数”。截至 2026-08-27，宽母现象已被以下工作显著覆盖：

1. **Whose Facts Win? LLM Source Preferences under Knowledge Conflicts**（ACL 2026）：直接比较不同来源、同一来源重复及可信度提示，并在 13 个跨家族/尺寸模型上发现重复偏好。
2. **Rational Synthesizers or Heuristic Followers? / GroupQA**（Findings ACL 2026）：显示重复改写可以比独立、多样证据更有说服力。
3. **Beyond Memory Majority / CAMA**（arXiv:2608.19701）：将共享上游来源形成的错误多数称为 *Memory Correlation Bias*。

因此：

- **已被覆盖：** 重复证据偏差、共同上游造成错误多数、跨模型存在性；
- **尚未检索到被系统做完：** 同一 base model 的谱系关系识别与决策使用之间的 matched dissociation；该差距随规模呈现的反常变化；其白盒因果机制。

“尚未检索到”不是绝对优先权证明。

## 当前可辩护的独特性质

```text
来源关系 probe：正确，并可能随规模改善
证据加权 decision：错误，且没有同步改善
独立多数 control：模型又能正常使用真正多数
```

这比一般 repetition bias 更窄、更有解释性，但审稿人仍可能将其视为已有工作的机制型扩展。因此当前只标记为 `HOLD`，不是“全新现象已确认”。

## 下一裁决条件

只有以下结果同时成立，才升级为 `ADVANCE`：

1. 使用自然、多跳的二手报道谱系，而非相同文本复制；
2. 在完全 matched 的 SAME/DIFFERENT probe 与 decision 中量化识别—使用差距；
3. 按 Qwen、Gemma、Phi、Llama、Mistral 五家族面板验证，至少 `3/5` 成立，并确认失败家族不是任务能力地板；
4. 证明差距随规模保持或扩大，而不只是小模型错误；
5. 排除频次、位置、长度、可信度和 prompt 服从解释；
6. 与 *Whose Facts Win?*、GroupQA、CAMA 的条件做直接对照；
7. 新颖性审计仍找不到已完成上述完整 signature 的工作。

若这些条件失败，该现象保留为真实行为记录，但不作为主要新题推进。
