# 016 — Mixed-Status Event Attraction

**中文一句话：** 模型单独知道“这件事真的发生了、那件事只是可能发生”，放到同一个真实 discourse 里以后，会不会把两件事的 factuality 状态互相带偏？

**Status:** `REGISTERED / OFF-THE-SHELF-D0 / BEHAVIOR-FIRST`
**Created:** 2026-08-30
**Top-10 rank:** #2
**Primary builder:** `../../preflight/d0_mixed_status_event_attraction/build_from_maven_fact.py`

---

## 1. 研究问题

语言里经常把不同现实状态的事件放在一起：

```text
The company completed the sale of its old division.
It is also considering acquiring a smaller rival next year.
```

第一件已经发生，第二件只是可能发生。

一个模型可能分别看两句时都判断正确，但在同一段 discourse 中处理多个事件后，把一个事件的 status 错误地“传染”给另一个事件。

我们问：

> **事件 factuality 是否是稳定地绑定在每个 event 上，还是会在多事件 discourse 中发生系统性的 status attraction / pooling？**

关键不是普通 EFD accuracy，而是一个 paired behavioral phenotype：

```text
目标事件单独/最小充分上下文时判断正确
+ 加入同文档另一种 factuality 的事件
-> 目标事件的判断有方向地向另一个事件的 label 移动
```

---

## 2. Mother / adjacent work

### MAVEN-FACT

Li et al., Findings of EMNLP 2024, *MAVEN-FACT: A Large-scale Event Factuality Detection Dataset*。

它提供：

- 112,276 个 event factuality annotations；
- factual / possible / impossible 等细粒度状态；
- event mentions、sentence positions、event types；
- 非事实事件的 supporting evidence；
- MAVEN 原有 event arguments / temporal / causal / subevent relations。

Paper: https://aclanthology.org/2024.findings-emnlp.651/
Code/data description: https://github.com/THU-KEG/MAVEN-FACT

Mother paper 的问题是 **event factuality detection**：给文本后能否正确识别某个 event 的 factuality，以及 arguments/relations 是否帮助模型。

### Event factuality / modality literature

更早的 EFD 工作大量研究 lexical cues、negation、modality、factuality propagation 等，但通常目标是预测 source-defined factuality label。这里我们不重新做 EFD benchmark，而是研究**两个已能分别识别的 event state 在同一 discourse 中是否互相污染**。

---

## 3. Novelty boundary

### 已知，不可写成贡献

- LLM 做 event factuality 并不完美；
- modality / negation / event relations 会影响 factuality；
- 同一文档中的其他事件可以提供有用信息；
- MAVEN-FACT 已经是大规模 EFD dataset。

### 我们真正要新增的对象

不是“更多 context 会不会改变预测”，而是：

> **当 target event 的 factuality 已经被模型正确识别时，加入 source-authored、同文档、不同 factuality 的另一个 event，是否造成朝该 event 状态方向移动的错误？**

这个定义要求错误有明确 wrong destination，例如：

```text
CT+ target + PS+ neighbor
target prediction: CT+ -> PS+
```

比单纯 accuracy decrease 更强。

**Working novelty hypothesis:** 截至当前检索，我们没有看到 MAVEN-FACT 或相邻 EFD 工作把“cross-event factuality attraction under recognition gating”作为独立现象并追踪其机制。正式写论文前仍需做更深 N1 collision search。

---

## 4. 数据为什么简单

这题最大的优点是**不需要我们标 factuality**。

MAVEN-FACT 每个 mention 自带：

```text
document id
sentence id
event id
trigger
event type
factuality label
evidence offsets (for non-factual mentions)
```

程序自动枚举同文档不同状态的 ordered pairs。

现有 builder：

`preflight/d0_mixed_status_event_attraction/build_from_maven_fact.py`

输出：

- `raw_mentions.jsonl`
- `eligible_pairs.jsonl`
- `audit_sample.jsonl`
- `scope_summary.json`
- `AUDIT_SAMPLE.md`

人工只随机抽查 source mapping，不产生 gold。

---

## 5. 不要犯的设计错误

### 5.1 不随机拼两篇文章

随机 concatenation 虽然更“干净”，但会把科学问题变成 synthetic distractor test。

主分析只允许：

```text
same original MAVEN-FACT document
```

### 5.2 不把某种 event type / distance 筛掉

sentence distance、event type、temporal/causal relation 都应该是 factor / stratum，而不是为了 money cell 越筛越窄。

### 5.3 不把 annotation 名字直接塞进 prompt

不能给模型看到 `CT+`、`PS+` 这些 source annotation。Prompt 用自然语言定义固定四类输出，label mapping 在 scorer 内完成。

---

## 6. D0 条件

对 ordered pair `(target, neighbor)`：

### TARGET_LOCAL

给 target 所在自然句子和 source-defined 最小必要邻域，问 target factuality。

### TARGET_PLUS_SAME_STATUS

加入同文档另一个与 target **同 factuality** 的 event sentence，作为“多一个 event / 多 context”的控制。

### TARGET_PLUS_MIXED_STATUS

加入同文档另一个**不同 factuality** event sentence。

### FULL_LOCAL_DISCOURSE

保留包含二者的原始连续 discourse window，用于检验 effect 是否在自然上下文中存在，而不是 sentence stitching artifact。

如果两个事件本来就在同一句，则保留原句，不人为拆句。

---

## 7. Primary metric

先把每个 source label 映射到固定 natural-language options，例如：

```text
A definitely happened / is happening
B is presented as possible or planned
C is presented as impossible / counterfactual / did not happen
D cannot be determined from the passage
```

具体 mapping 必须在 materialization 前按 MAVEN-FACT annotation manual 冻结。

主指标不是 overall accuracy，而是：

```text
attraction(target <- neighbor) =
Δ logit/probability of neighbor's factuality label
when moving SAME/LOCAL -> MIXED
```

以及 recognition-gated transition rate：

```text
LOCAL correct
MIXED wrong exactly toward neighbor label
```

要分别报告：

- factual -> possible
- possible -> factual
- factual -> impossible
- impossible -> factual

禁止把所有方向混成一个平均数。

---

## 8. Gates / controls

一个 target 进入 decisive analysis 前至少要求：

1. `TARGET_LOCAL` 正确；
2. source factuality label 非 `unknown/uncertain` 边界项，或该边界单独报告；
3. `TARGET_PLUS_SAME_STATUS` 不出现同量级退化；
4. order counterbalance 后方向仍在；
5. event trigger / evidence sentence 没因 builder 截断；
6. document cluster 作为统计单位，不能把同一篇文章 100 个 pair 当 100 个独立样本。

---

## 9. 最危险的替代解释

### “另一个事件其实提供了合法的新证据”

这是本题最大风险。

处理方式不是硬筛所有 related pairs，而是：

- 标记 temporal / causal / subevent relation；
- separately report explicit-related vs no-explicit-relation；
- same-status neighbor 做控制；
- 用 target evidence span 是否变化做 source audit；
- 如果 effect 只在有明确语义关系的 pair 中出现，则它更可能是正常 discourse inference，不叫 contamination。

### “只是更长 context 导致性能下降”

same-status / matched-length conditions 必须排除。

---

## 10. PROMOTE / KILL

### PROMOTE

至少两个模型家族：

- local recognition denominator 足够；
- mixed-status condition 出现稳定 directional attraction；
- same-status matched control 显著更弱；
- effect 在 document-cluster bootstrap 下 CI 不含 0；
- 至少两个 factuality direction 同号，或一个方向极强且有清晰理论解释；
- 不依赖一个 event type / 一个文档主题。

### KILL

- 只有总体 accuracy 下降，没有 toward-neighbor 的 wrong destination；
- same-status context 一样坏；
- effect 只来自 builder 截断、label leakage 或单一 relation type；
- recognition gate 后 denominator 太小；
- full natural discourse 中 effect 消失，只在人工拼 sentence 的版本出现。

---

## 11. Mechanistic follow-up

如果行为成立，最自然的问题是：

> **模型到底是没有为每个 event 建立独立 factuality slot，还是已经表示对了但在输出时把 status readout 绑定错了 event？**

可区分：

```text
A. status representation pooling：多个 event 的 factuality 表征本身混合
B. binding failure：status 都存在，但 target-event ↔ status 绑定错
C. discourse summary overwrite：后出现/更显眼 event 重写了共享 discourse state
```

实验：

- event-position-specific factuality probes；
- target vs neighbor token activation patching；
- swap neighbor factuality while holding target text fixed；
- layer-wise target-label vs neighbor-label trajectories；
- attention heads from modality/evidence cue -> target trigger；
- causal erase/restore neighbor status component。

这会是一个很标准的 **behavioral phenomenon -> binding mechanism** 故事。

---

## 12. 最小执行顺序

```text
1. 下载 MAVEN-FACT train/valid
2. 跑现有 builder，先只 materialize source pairs
3. 看 scope_summary + 20 random audit rows
4. 冻结 label verbalization / local-window rule
5. Qwen3-8B + Gemma-3-12B-IT D0 smoke
6. 若出现 directional attraction，再扩第三家族
7. N1 exact collision search
8. 才进入 MI
```
