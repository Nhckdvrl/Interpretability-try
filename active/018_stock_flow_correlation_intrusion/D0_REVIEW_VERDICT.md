# 018 post-run review verdict

**Date:** 2026-08-30  
**Independent status:** `INCONCLUSIVE / HOLD-D0-MEASUREMENT-FAILURE / REDESIGN-REQUIRED`

This file supersedes any interpretation of `D0_V1_REPORT.md`'s `NO-PROMOTE` as a scientific null.

The ResOpsUS source bank and balanced 2×2 design are valid. The failure occurs at the **net-recognition measurement instrument**: strict gating requires correctness across four A/B presentations, but negative-net items show extreme answer-position dependence. In the clearest case, Llama recognizes negative net at ~99–100% with the canonical option position and 0% after option reversal. Qwen and Gemma also show severe presentation dependence.

Therefore all strictly gated items are positive-net items and the preregistered direction-controlled stock-flow intrusion estimand is non-estimable. This does **not** justify the claim that Stock–Flow Correlation Intrusion is absent.

A future D0 v2 may be run only after a new contract is frozen. It must:

1. preserve all four `net direction × inflow trend` semantic cells;
2. replace letter-position-dependent recognition with semantic continuation scoring (`positive` vs `negative`) or deterministic numeric cumulative-net output;
3. keep wording/order changes as diagnostics rather than defining competence by one A/B mapping;
4. retain `explicit_correct_net` downstream controls;
5. forbid positive-net-only rescue.

Until then, no new model call is authorized. Full reasoning is in `../../phenomenon_miner/TOP6_RESULT_REVIEW_2026-08-30.md`.
