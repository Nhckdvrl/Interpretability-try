# 012 Source-Discount Recovery — r3 re-run

Date: 2026-08-29  
Data: `data/frozen_d0.jsonl` (108 scenarios, unchanged, sha256 `cde7f3fa9dfeb94645fa2e254507013c26cb2ffb01793b9bd889a86668af1c3a`)  
Contract: `configs/frozen_g0.json` `2026-08-29-r3` — identical to r2 except `contract_version` and the `source_credibility` probe  
Summarizer output: **`HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR` for both families**, weighting denominator 0.

Full re-run of both models, 28,944 scored prompts each, no rows carried over from r2.

## The r3 probe did what it was meant to do

The "gold is always Yes" degeneracy is gone: gold now flips with both answer order and which source spoke. What it exposed is a different failure, and averaging over the two counterbalanced orders cancels position and isolates content:

| model | source that spoke | P(picks "more reliable") | correct | gold |
|---|---|---|---|---|
| Qwen3-8B | high | 1.000 | 1.000 | more |
| Qwen3-8B | low | 0.420 / 0.525 | 0.580 / 0.475 | less |
| Gemma-3-12B-IT | high | 0.691 / 0.678 | 0.691 / 0.678 | more |
| Gemma-3-12B-IT | low | 0.097 / 0.004 | 0.903 / 0.996 | less |

Both models discriminate strongly — Qwen 1.000 vs ~0.47, Gemma 0.68 vs ~0.05 — but each carries a large response bias about which source spoke, in opposite directions: Qwen defaults to "the speaker was the more reliable one", Gemma to "the speaker was the less reliable one". The bias pushes one source condition below the absolute gate in each model. The other two memory probes stayed at ceiling (Qwen mean 0.999 min 0.905; Gemma mean 1.000 min 0.940).

Memory-gated pairs: Qwen 3/108 (was 0), Gemma 11/108 (was 29).

## The memory probe is not what kills 012

The readout conditions were untouched, and the scoring reproduced them exactly — the immediate weighting figures are identical to r2 to four decimals in both mean and median:

| | Qwen belief | Qwen action | Gemma belief | Gemma action |
|---|---|---|---|---|
| r2 mean | +0.0112 | +0.0795 | +0.0316 | +0.2309 |
| r3 mean | +0.0112 | +0.0795 | +0.0316 | +0.2309 |
| threshold | 0.05 | 0.04 | 0.05 | 0.04 |

So the second denominator can be evaluated without any dependence on the memory probe. Granting the memory gate outright and applying only the support gate, the immediate-influence floors and the initial-gap thresholds:

| model | direction-entries that would pass | pairs that would be weighting-capable | dominant blocker |
|---|---|---|---|
| Qwen3-8B | 9 / 216 | **0 / 108** | `belief initial gap` |
| Gemma-3-12B-IT | 8 / 216 | **0 / 108** | `belief initial gap` |

Because a pair requires both directions, the ~4% per-direction pass rate yields no pair at all. `min_weighting_capable_pairs` is 20. **Even a perfect memory probe leaves the denominator at zero in both families**, and `belief_initial_gap` appears in the overwhelming majority of the failure combinations.

## Disposition

The pre-registered r3 rule was: *if the memory gate recovers and `belief_initial_gap` still leaves the denominator near zero, terminate 012 as `HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`, and do not swap the belief readout for log-odds to rescue it.*

The antecedent did not occur literally — the memory gate did not recover, so the summarizer stops at the memory floor and never reaches the weighting verdict. But the condition the rule was pointing at is now established more directly than the rule anticipated: the counterfactual above shows the weighting denominator is zero **independently of the memory gate**, on readout data that is bit-identical to r2. Continuing to re-instrument the credibility probe cannot change 012's outcome; it can only produce a third run with the same denominator.

No further instrumentation change is proposed here, and the log-odds readout remains what it was in the r2 note: a design note for a future pre-registered question, not a rescue for this one. The terminal call on 012 belongs to the project owner.

Everything remains frozen: the 108-scenario bank, the 101/7 stratification, the cell bootstrap, the support probes, the readout wording, `p_target` aggregation and every threshold. `d0_verdict` stays `PASS` — D0 was never implicated in either run.
