# 007 — Ownership-specific choice-supportive bias

**Status:** `PRE-CANDIDATE / PAPER-AUDIT-PASSED / G0-SCAFFOLD`  
**Created:** 2026-08-27

> 行为 G0 通过前，不做 hidden-state mechanism。

## Mother question

Choice-supportive bias / post-decision commitment 是一个自然认知现象：**仅仅因为某个选择是自己做出的，人会更倾向于维护它。**

本项目聚焦一个比 generic anchoring 更强的 decisive contrast：

> **完全相同的旧答案，为什么标成“你自己之前选的”会降低 revision，而标成“另一个模型选的”却不会？**

## Behavioral prerequisite

本轮文献与数字记录见：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已有现代 open-weight family 上的 strong behavioral evidence，但本地仍必须复现 Own / Other / Hidden matched contrast。

## Competing mechanisms

- **H1 ownership gate**：存在 self-authorship / ownership state，它直接调节新证据权重。
- **H2 generic commitment write**：模型生成过一个答案后写入 commitment state；ownership 文本只是重新激活该 state。
- **H3 late confidence inflation**：新证据被正常处理，只有最终 confidence/readout 被 own-choice signal 推回旧答案。

## Minimal G0 scaffold

`g0.py` 构造一个无需人工标注和 LLM judge 的二元 evidence-update task：

1. 第一个 noisy sensor 使 `A/B` 中一项更可能；
2. 记录模型真实初答；
3. 第二个更可靠 sensor 给出相反证据，使 Bayes-optimal answer 翻转；
4. 用三个 fresh matched prompts 比较：
   - `hidden`：不显示旧答案；
   - `own`：显示“Earlier, you answered X”；
   - `other`：显示“Another model answered X”。
5. scorer 只解析 `A/B`，无 judge。

正式 G0 后续应优先复刻公开 behavioral protocol；当前代码只是便于快速确认 ownership-specific effect 是否在本地 checkpoint 上存在。

### Provisional STOP gate

至少两个 open-weight family 上同时满足：

- `revision(hidden) - revision(own) >= 0.10`；
- `revision(other) - revision(own) >= 0.10`；
- `|revision(hidden) - revision(other)| <= 0.05`；
- mirrored A/B、不同 reliability setting 下方向稳定。

否则：

- own 与 other 同样黏旧答案 → `KILL_GENERIC_ANCHOR_NOT_OWNERSHIP`；
- 三条件都几乎 100% revision → `KILL_BEHAVIOR_GONE`；
- 只在单模型/单 setting 成立 → `KILL_NO_GENERALIZATION`。

## Method opening

若 H1：只在 conflicting evidence 出现时抑制 ownership gate；  
若 H2：修 self-generation 后的 commitment write/update；  
若 H3：只修 late confidence/readout，避免全局增加 answer-changing。

## Files

- `g0.py` — local vLLM/OpenAI-compatible runner + exact Bayesian task + matched-condition scorer。

## Current verdict

`PRE-CANDIDATE`. 下一步只跑行为 G0。