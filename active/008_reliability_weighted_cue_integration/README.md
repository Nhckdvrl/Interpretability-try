# 008 — Reliability-weighted cue integration

**Status:** `PRE-CANDIDATE / PAPER-AUDIT-PASSED / G0-SCAFFOLD`  
**Created:** 2026-08-27

> 行为 G0 通过前，不进入 VLM hidden-state mechanism。

## Mother question

经典 psychophysics / multisensory integration 问题：

> **当两个 noisy cues 指向同一个连续量时，系统是否会按各自可靠性进行近似 Bayes-optimal 加权？**

本项目不研究“VLM 总体视觉能力差”，而研究 uncertainty/reliability 是否被表示并真正用于 cue fusion。

## Behavioral prerequisite

本轮筛选与已报道 open-model 差异见：

`rejected_candidates/search_round_2026-08-27_natural_phenomena_final.md`

已有行为工作显示不同 open multimodal family 的 cue-integration efficiency 差异很大，但本地必须先确认 Gemma/Qwen 上目标 effect 足够强。

## Competing mechanisms

- **H1 uncertainty representation failure**：模型根本没有形成随 noise 改变的可靠性表征。
- **H2 fusion/routing failure**：可靠性可读，但融合时仍错误使用 noisy cue。
- **H3 late magnitude readout failure**：内部融合接近 normative，最终数值/readout 才失真。

## Minimal G0 scaffold

`g0.py` 目前只做 deterministic stimulus generation + scorer：

1. 生成一个 latent target value；
2. text cue 与 visual cue 分别是带已知 Gaussian noise 的 measurement；
3. 把 visual cue 渲染成简单 SVG marker/ruler；
4. 根据 inverse-variance weighting 计算 normative fused estimate 与 image weight；
5. 读取后续模型 runner 产出的 numeric prediction，反推出 observed image weight 并与 normative weight 比较。

当前 deliberately 不把某个 VLM serving API 写死；后续只需生成 `predictions.jsonl`（`id`, `prediction`）即可评分。

### Provisional STOP gate

正式冻结前可进一步细化，但不得结果出来后放宽：

- 至少 Gemma-3 与 Qwen2.5-VL 两个 family；
- unimodal cue reading 不能接近随机，否则不是 integration failure；
- observed cue weight 必须随 reliability ratio 有可测响应；
- 若某模型已近似 normative，不把它当 failure model 强行做机制；
- 至少一个 family 存在稳定 `mean |w_observed - w_optimal| >= 0.15`，且不是纯 numeric parsing/readout error。

若模型完全读不懂 SVG/marker：`HOLD_STIMULUS_INTERFACE_BAD`，不是机制 failure。

## Method opening

H1 → uncertainty/reliability representation training；  
H2 → reliability-aware fusion/gating；  
H3 → late continuous-value readout correction。

## Files

- `g0.py` — SVG stimulus + JSONL manifest generator；可对 numeric predictions 做 deterministic scorer。

## Current verdict

`PRE-CANDIDATE`. 先确认本地 cue-integration behavior，再决定是否值得白盒。