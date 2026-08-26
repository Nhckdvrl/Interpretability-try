# 006 — Bayesian latent inference → downstream-use gap

**Status:** `PRE-CANDIDATE / PAPER-AUDIT-PASSED / G0-SCAFFOLD`  
**Created:** 2026-08-27

> 行为 G0 通过前，禁止进入 probe / SAE / attention sweep / activation patching。

## Mother question

人在连续观察证据时，应先形成对隐藏状态的 posterior belief，再把该 belief 一致地用于后续预测或决策。

本项目问：

> **模型已经能正确推断隐藏状态时，为什么仍不能把这个 belief 正确用于下一步决策？**

这是 Bayesian evidence accumulation / latent-state inference 的自然问题，不以 LLM benchmark 为起点。

## Behavioral prerequisite

本轮 paper audit 记录在：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已有 BayesBench 行为结果支持 open-weight Llama/Qwen 中存在 inference→use dissociation。本地仍必须先复现；不能因为论文报告成立就跳过 G0。

## Competing mechanisms

- **H1 representation failure**：模型输出看似能报告 posterior，但内部没有稳定/calibrated latent belief。
- **H2 routing failure**：latent belief 已形成，但 downstream decision computation 没有使用它。
- **H3 late readout distortion**：belief 已进入 downstream computation，最终 categorical/readout 阶段才发生失真。

机制不同必须导向 representation correction / belief routing / late readout calibration 三种不同修复。

## Minimal G0 scaffold

`g0.py` 目前只做一个极小、闭式可算的 smoke test：

1. 二元 hidden state `A/B`；
2. 给出若干 noisy observations；
3. 闭式计算 `P(A|evidence)`；
4. 分开询问模型 posterior 与一个依赖 posterior threshold 的 downstream action；
5. 统计“posterior 已经答得接近 gold，但 action 仍错”的 know-use failures。

这不是正式 BayesBench 复现，也不能作为最终论文证据；后续应优先替换/扩展为官方公开任务。

### Provisional STOP gate

冻结 full G0 前可再收紧，但不得事后放宽救题：

- 至少两个 open-weight family 复现；
- 在 Bayes-margin >= 0.10 的非边界 cases 上，posterior MAE <= 0.15 的 cases 足够多；
- 在这些“latent inference 已基本正确”的 cases 中，downstream error 仍 >= 15%；
- 若 use failure 只来自 posterior 本身答错，则 `KILL_NO_INFERENCE_USE_DISSOCIATION`。

## Files

- `g0.py` — closed-form case generator + optional local OpenAI-compatible/vLLM runner + exact scorer。

## Current verdict

`PRE-CANDIDATE`. 现在只允许补全/运行行为 G0。