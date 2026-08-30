# 021 — Task-Switch Carryover

**中文一句话：** 对话已经明确换任务了，模型犯错时，会不会不是随机错，而是还在按上一个任务的规则做？

**Status:** `REGISTERED / STRONG-MOTHER / NOVELTY-MUST-BE-WRONG-DESTINATION`
**Created:** 2026-08-30
**Top-10 rank:** #8

---

## 1. 先把边界说清楚

“Task switch 会让 LLM performance 下降”已经被做过，而且是很直接的 mother paper。

Gupta et al., EMNLP 2024 Main, *LLM Task Interference: An Initial Study on the Impact of Task-Switch in Conversational History*：

- 5 datasets；
- 15 task switches；
- 多个 LLM；
- 发现 conversational history 中的 previous task 会显著伤害 switched target task。

Paper: https://aclanthology.org/2024.emnlp-main.811/
Code: https://github.com/ivaxi0s/llm-task-switch

所以本项目**绝对不能**把“task switch hurts”当 novelty。

---

## 2. 真正的问题

Mother paper 的核心量主要是 target performance / sensitivity 变化。

我们想把错误拆得更有方向：

> **模型切到新任务后犯的错，是否系统性地符合“旧任务仍然在控制输出”的预测？**

换句话说，不只是：

```text
accuracy 90% -> 70%
```

而是：

```text
新任务正确规则 = B
旧任务如果继续执行 = A
模型实际输出 = A
```

这才叫 **carryover**。

如果错误只是随机增加，或者格式更乱，那只能复现 mother interference，不能形成新 paper。

---

## 3. Novelty boundary

### Mother 已经解决

- conversational history 会产生 task interference；
- history length / task combination 会影响程度；
- 不同 task switch 的 sensitivity 不同。

### 本项目要新增

三个层级：

1. **wrong-destination specificity**：错误是否特别落到 previous-task rule 的预测上；
2. **decay trajectory**：switch 后第 1、2、3… 个 target turn，旧 task influence 怎么消退；
3. **mechanistic state transition**：模型什么时候内部已经切 task，但 output policy 还没切，或反过来。

只有 1 成立，才值得做 2/3。

**Working novelty hypothesis:** 当前 mother work 强烈覆盖 aggregate task-switch interference；我们尚未确认它是否已系统研究“previous-rule-predicted wrong answers + post-switch decay + causal mechanism”。因此本项目的 novelty 风险高，D0 必须先建立比 accuracy drop 更具体的 behavioral signature。

---

## 4. 数据来源

优先复用 mother repo，而不是自己重新发明 10 个 task：

https://github.com/ivaxi0s/llm-task-switch

其公开实现支持：

- Rotten Tomatoes sentiment；
- TweetQA；
- MMLU variants；
- GSM8K；
- Gigaword；
- DailyMail；
- moral / law / math 等。

但这些异质任务不一定能给出“旧 task 对当前 item 会预测什么”的 hard oracle。

因此 D0 分两层。

---

## 5. D0-A：先复现 mother，不算 novelty

直接用 mother repo 做：

```text
no-history target
same-task history target
switched-task history target
```

目的只有两个：

1. 验证当前模型族仍有 interference；
2. 找哪些 task pair 有足够 effect，值得进入 wrong-destination D0-B。

如果 mother effect 在现代模型上基本没了，本题直接降级。

---

## 6. D0-B：构造可判定的旧规则 wrong destination

要研究 carryover，必须选择**同一 target input 可以同时被 old rule 与 new rule 明确定义**的 task pair。

最简单的做法是使用已有 labeled dataset 的属性，程序化定义两个不同 question operators，而不是人工写题。

理想 source 形状：

```text
item x has label_a and label_b
Task A asks attribute a
Task B asks attribute b
```

例如未来可寻找 multi-attribute classification dataset：同一 text/image 有 sentiment + topic、entity + relation、truth + modality 等 source labels。

若找不到天然 multi-label source，允许一个**secondary diagnostic control**使用 counterbalanced label mappings：

```text
Task A: positive -> A, negative -> B
Task B: positive -> B, negative -> A
```

但这种 mapping-switch 只能证明 rule carryover 的机制，不应成为 paper 的唯一 natural anchor。

---

## 7. 关键设计

对 target item `x`，必须能算：

```text
new_gold(x)
old_rule_prediction(x)
```

并且两者不同。

然后比较：

```text
DIRECT_B:
Task B instruction + x

SWITCH_A_TO_B:
several Task A turns
explicit switch to Task B
x
```

主指标：

```text
carryover_error =
P(output = old_rule_prediction | switch)
-
P(output = old_rule_prediction | direct B)
```

这比 `accuracy_B(switch) - accuracy_B(direct)` 更有诊断性。

---

## 8. Decay trajectory

如果 D0-B 有 carryover，再连续给多个 Task B items：

```text
B1, B2, B3, B4, ...
```

测：

```text
old-rule attraction at B1
old-rule attraction at B2
...
```

可能出现：

- exponential decay；
- one-shot reset；
- persistent plateau；
- error-triggered reset；
- correct-answer-triggered reset。

这是比 mother aggregate interference 更自然的“state persistence”问题。

---

## 9. Fatal controls

### Explicit switch instruction

必须清楚告诉模型“previous task ended; now do Task B”。否则不是 failure，而是 instruction ambiguity。

### Output alphabet

old/new task 的选项位置、label string 要 counterbalance，避免位置 priming。

### History length

same-task B history / neutral history 做控制。

### Capability

DIRECT_B 必须正确，old Task A capability 也要足够。

### Wrong destination

如果 switched condition 只是更多 malformed outputs、格式错误、随机 labels，而不是 old-rule prediction，不能叫 carryover。

---

## 10. PROMOTE / KILL

### PROMOTE

- mother aggregate interference 在当前模型仍存在；
- 至少一个 natural/multi-attribute source 能给 hard old-rule destination；
- switch 后 old-rule-specific error 显著高于 direct / matched-history；
- effect 有可重复 decay trajectory；
- 至少两家族同方向。

### KILL / ROUTE

- 只能复现 mother accuracy drop；
- 找不到 natural old-rule oracle，只剩 synthetic label flip；
- errors 不朝 old rule；
- explicit switch 后 effect 消失；
- 现代模型 mother interference 已很弱；
- novelty search 发现 mother/后续工作已经做了同样 wrong-destination analysis。

如果只剩内部 TR/TL representation question，则 ROUTE 回 `MECH-FOLLOWUP`，不能硬当新 phenotype。

---

## 11. Mechanistic fork

如果 behavior 是 old-rule-specific，可以问：

```text
A. task representation 没切换
B. task representation 已切换，但 label/readout mapping 还旧
C. instruction representation 对了，但 old conversation examples 通过 induction heads 继续控制输出
D. post-switch 前几层是 old task，后几层才完成切换
```

可做：

- decode task identity across layers / turns；
- decode label mapping separately；
- patch DIRECT_B task state into SWITCH_B；
- ablate history-attending heads；
- trace switch instruction token pathways；
- fit state-space decay across post-switch turns。

这时我们之前的 `TR/TL desynchronization` 才有资格作为机制解释，而不是论文 headline。

---

## 12. 最小执行顺序

```text
1. 跑 mother repo 的现代 open-model reproduction
2. 找 strongest task pairs
3. 同时搜 natural multi-attribute source，要求 old/new rule 都有 source label
4. 先做 output-level old-destination D0
5. 没有 wrong destination -> KILL/MECH-FOLLOWUP
6. 有 -> 跑 post-switch decay
7. N1 collision search
8. 再做 task-vs-label state MI
```
