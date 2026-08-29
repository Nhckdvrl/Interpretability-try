# 007 Result Lineage

这个目录保存不同时间点 / 不同 frozen contract 的结果。**不要跨 D0 SHA 或 contract 直接合并结论。**

## `smoke_r5/` — historical 25-case contract

- execution commit: `0ef5ee612ccb251f5ded2fe301487c925455405a`
- D0 SHA256: `b1f6f88983b68e2764ff99964debd71a307dc0209c2cb9d2bb8f6d7484fd9792`
- D0 size: 25 scenarios / 50 directions
- models: Qwen3-8B, Gemma3-12B-IT
- verdict under that contract: `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`
- raw outputs and [`SMOKE_VERDICT.md`](smoke_r5/SMOKE_VERDICT.md) remain valid provenance for that exact snapshot

## Current project contract — no result stored here yet

After the historical smoke, commit `3cbe5e2` materially changed D0 provenance / held-out LR verification / builder behavior. The current project README and authoritative registry point to:

- D0 size: 30 natural scenarios
- current D0 SHA256: `d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a`
- status: `READY-TO-SMOKE`

Therefore the 25-case hard kill must **not** be copied into summaries of the current 30-case contract, and the current READY status must **not** be retroactively attached to the old raw outputs.

When a current-contract smoke is run, create a new result directory with the frozen D0 SHA, execution commit, model revisions, raw completeness audit and verdict in its header.