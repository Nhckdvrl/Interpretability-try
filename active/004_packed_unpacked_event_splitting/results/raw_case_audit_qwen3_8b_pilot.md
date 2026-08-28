# Raw-case audit — Qwen3-8B pilot

This is an exploratory local pilot on 5 Football-Data scenarios, each with k=2/3/4.
The scorer used the local qwen3-8b vLLM endpoint and exact echo token logprobs.

Summary: HOLD-ARTIFACT-CONTROLS.

- 10/15 partitions passed the relation gate.
- Mean core unpacked bias: 0.04499.
- 5/5 scenario groups failed artifact controls.
- Mean reorder gap: visibly above the 0.06 contract tolerance in the raw cases.
- Mean repacking recovery: -0.05082, i.e. repacking often increased rather than
  recovered the absolute bias.
- Mean within-family branch-count slope: -0.19849.
- Natural-template positive fraction: 0.60.

The largest apparent positive effects were concentrated in k=2/k=3. The same
source scenarios often reversed sign at k=4, and the reordered condition moved
substantially. These are direct reasons not to call the pooled positive movement
Packed–Unpacked Event Splitting. No N1, panel expansion, or mechanism work is
authorized from this pilot.
