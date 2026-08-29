# Final verdict — Source-Discount Recovery

Date: 2026-08-29  
Status: **`TERMINAL-KILLED / HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`**

## Decision

012 is terminated at the behavioral capability denominator. It does **not** proceed to recovery interpretation, N1, cross-family generality expansion, scaling, or mechanism work. No fourth instrumentation pass is authorized.

D0 remains `PASS`: the 108-scenario NetEaseCrowd bank and its frozen statistical contract were not implicated in the failure.

## Evidence chain

### r2 — instrumentation hold

The first two-family smoke ran Qwen3-8B and Gemma-3-12B-IT over the full 108-scenario bank. Its summarizer returned `HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR`, but the binding `source_credibility` capability probe was a yes/no item whose gold was always Yes and showed a decisive, opposite answer-position artifact in the two families. The other source-identity and message-direction memory probes were at ceiling. r2 is therefore retained as **`HOLD-INSTRUMENTATION-ARTIFACT`**, not used as the terminal scientific kill.

### r3 — one-item repair and full rerun

r3 changed exactly one capability item: `source_credibility` became a counterbalanced `more reliable / less reliable` content-choice probe. The D0 bank, primary/secondary membership, support probes, belief/action readouts, `p_target` aggregation, thresholds and panel rules were unchanged, and both models were fully rerun with no r2 rows spliced in.

The repaired probe removed the always-Yes degeneracy but still left a source-conditioned response bias, so the ordinary summarizer again stopped at the memory floor: Qwen memory-gated 3/108 pairs and Gemma 11/108.

That gate ordering is not the terminal reason for killing 012.

## Decisive terminal test

The untouched immediate readouts reproduced r2 exactly to four decimals:

| model | belief initial gap | action initial gap |
|---|---:|---:|
| Qwen3-8B | +0.0112 | +0.0795 |
| Gemma-3-12B-IT | +0.0316 | +0.2309 |

Frozen thresholds were belief `0.05` and action `0.04`.

A counterfactual capability audit then **granted the memory gate outright** and applied only the frozen support gate, immediate-influence floors, and initial high-vs-low source discount gap. This removes the disputed credibility probe from the decision entirely:

| model | passing direction entries | weighting-capable pairs | frozen minimum |
|---|---:|---:|---:|
| Qwen3-8B | 9 / 216 | **0 / 108** | 20 |
| Gemma-3-12B-IT | 8 / 216 | **0 / 108** | 20 |

A pair requires both evidence directions. The dominant blocker is `belief_initial_gap`. Thus **even perfect source-memory instrumentation cannot create a denominator in either family**.

## Why no further rescue is allowed

Any subsequent change capable of making this project pass would alter the already-observed phenotype rather than repair the demonstrated r2 instrumentation defect: replacing the belief probability readout with log-odds, lowering the belief gap threshold, dropping belief as a co-primary interface, relaxing bidirectionality, or choosing a different/weaker model family would all be post-result rescue.

The action interface does show larger high-vs-low source gaps than the belief interface. This is preserved as a failure-bank observation only; it was not independently preregistered as a new phenomenon and cannot be used to rename or continue 012.

## Final state

```yaml
formal_n0_verdict: PASS
d0_verdict: PASS
r2_disposition: HOLD-INSTRUMENTATION-ARTIFACT
r3_disposition: TERMINAL-KILLED
behavioral_verdict: HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR
qwen_counterfactual_weighting_capable_pairs: 0/108
gemma_counterfactual_weighting_capable_pairs: 0/108
validation_authorized: false
```
