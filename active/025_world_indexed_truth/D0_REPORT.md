# 025 D0 report — world-indexed truth capability

## Verdict

```yaml
v1_verdict: HOLD_PREREQUISITE_CAPABILITY
v2_verdict: HOLD_PREREQUISITE_CAPABILITY
mechanism_authorized: false
topic_killed: false
```

The same-proposition behavioral prerequisite did not pass. No probe,
representation comparison, attribution, or intervention is authorized.

## Frozen experiment

The bank contains 64 audited propositions from solar-system, chemistry, and
arithmetic domains. Every proposition appears in an aligned and a conflicting
local world. Each fixed context is queried once for actual truth and once for
local truth, giving 128 paired contexts and 256 scored queries. Three world
frames and three query-paraphrase families are deterministically rotated.

The primary metric is context-level joint accuracy: both actual and local
queries must be correct. Candidate `TRUE` and `FALSE` strings are compared by
length-normalized conditional sequence log likelihood, with no free-form parser.

## V1: sub-2B capability screen

| Family | Query accuracy | Overall joint | Conflict joint | Aligned joint | Pass |
|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B | 0.777 | 0.555 | 0.406 | 0.703 | no |
| Gemma3-1B | 0.723 | 0.469 | 0.094 | 0.844 | no |
| Llama3.2-1B | 0.527 | 0.281 | 0.125 | 0.438 | no |
| SmolLM2-360M | 0.504 | 0.250 | 0.000 | 0.500 | no |

No family passed. Median conflict joint accuracy was 0.109. Qwen and Gemma were
already highly accurate on local queries (0.992 and 0.930) but actual-world
accuracy was only 0.563 and 0.516. This is consistent with local-context
overwrite, but the frozen capability gate does not identify a mechanism.

## V2: models-only strong-checkpoint replication

V2 inherited the exact bank, prompt, scoring, thresholds, and adjudication and
changed only checkpoint scale/family.

| Family | Query accuracy | Overall joint | Conflict joint | Aligned joint | Pass |
|---|---:|---:|---:|---:|---:|
| Qwen3-8B | 0.855 | 0.734 | 0.891 | 0.578 | no |
| Gemma3-12B | 0.887 | 0.773 | 0.922 | 0.625 | no |
| Llama3.1-8B | 0.758 | 0.523 | 0.828 | 0.219 | no |
| Mistral-Small-24B | 0.852 | 0.711 | 0.828 | 0.594 | no |

All four strong checkpoints cleared the frozen conflict-joint threshold, and
the median conflict joint accuracy was 0.859. Nevertheless, none passed the
full family gate because every model failed aligned controls and overall joint
accuracy. Gemma came closest at 0.773 overall joint versus the frozen 0.80
floor, but its 0.625 aligned joint was far below the 0.85 floor.

## Scientific interpretation

Testing only counterfactual conflict cases would have produced a strong but
invalid positive result across four families. The aligned controls show that
models often exploit a contrast heuristic: when the prompt emphasizes separate
worlds, the actual answer is treated as the alternative to the local
stipulation. That shortcut succeeds when actual and local truth values conflict
and fails when they align. This is source/task routing, not evidence that two
world-bound valuations coexist.

This diagnostic is an inference from the condition asymmetry, not a causal
mechanism claim. The bank rotates frame and paraphrase rather than holding their
surface strings identical across aligned/conflict contexts, so future work must
also rule out residual wording interactions.

## Topic judgment

The topic retains potential: the conflict-only false positive is substantive,
cross-family, and directly motivates the title-level distinction between
world-bound truth and late contrast routing. It is held—not narrowed into a
prompt-compliance paper and not killed. A future contract would need a
behavioral design in which aligned and conflicting valuations are both solved
without contrast inference before MI can distinguish dual binding from routing.
Lowering the aligned gate, dropping controls, or studying only the successful
conflict subset is forbidden.
