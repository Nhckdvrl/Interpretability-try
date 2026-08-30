# 018 post-run review verdict

**Date:** 2026-08-31
**Independent status:** `D0-v2 COMPLETE / NO-PROMOTE / NO-MI / TERMINAL`

The bounded repair authorized below was frozen and completed. Full results are
in `D0_V2_REPORT.md` and `results/d0_v2/analysis.json`.

The ResOpsUS source bank and balanced 2×2 design are valid. The failure occurs at the **net-recognition measurement instrument**: strict gating requires correctness across four A/B presentations, but negative-net items show extreme answer-position dependence. In the clearest case, Llama recognizes negative net at ~99–100% with the canonical option position and 0% after option reversal. Qwen and Gemma also show severe presentation dependence.

Therefore D0-v1 did not justify a scientific null by itself.

D0-v2 implemented exactly one measurement repair:

1. preserve all four `net direction × inflow trend` semantic cells;
2. replace letter-position-dependent recognition with semantic continuation scoring (`positive` vs `negative`) or deterministic numeric cumulative-net output;
3. keep wording/order changes as diagnostics rather than defining competence by one A/B mapping;
4. retain `explicit_correct_net` downstream controls;
5. forbid positive-net-only rescue.

The same 600-window bank was run on Qwen, Gemma, Llama, and Phi. Every family
missed at least one 50-item semantic cell. Among estimable families, the primary
actual-history attraction was +1.23pp, −3.88pp, and +0.75pp respectively for
Qwen, Gemma, and Phi, below the frozen +5pp threshold or opposite in direction.
Llama lacked positive-net coverage, so its negative-only diagnostic cannot be
promoted.

The registered phenotype is therefore `NO-PROMOTE`. No D0-v3, selected-polarity
rescue, second natural source, additional N1 search, or mechanistic call is
authorized.
