# D0 v2 gate-failure forensic decomposition

Status: `EXPLORATORY-LOCAL / INVALIDATED-HARNESS-DIAGNOSTIC`

The v2 polarity probe maps pro-TARGET to semantic Yes and pro-OTHER to semantic No. The counts below separate that probe from the paired admitted operator.

| Model | Polarity | Inadmissible mean-gate | Scope mean-gate | Polarity mean-gate | Polarity both-orders | Admitted directional |
|---|---:|---:|---:|---:|---:|---:|
| Qwen/Qwen3-8B | supports_target | 19/20 | 13/20 | 12/20 | 11/20 | 20/20 |
| Qwen/Qwen3-8B | supports_other | 17/20 | 15/20 | 5/20 | 1/20 | 7/20 |
| google/gemma-3-12b-it | supports_target | 20/20 | 10/20 | 10/20 | 9/20 | 17/20 |
| google/gemma-3-12b-it | supports_other | 20/20 | 18/20 | 17/20 | 17/20 | 2/20 |

## Pair-level diagnosis

- **Qwen/Qwen3-8B**: 11/20 pairs pass rule/scope plus admitted pair delta; 8 of those are killed only by the explicit polarity probe. Current fully gated pairs: 1.
  - Probe-induced pair IDs: legalbench-hearsay-37, legalbench-hearsay-38, legalbench-hearsay-41, legalbench-hearsay-42, legalbench-hearsay-44, legalbench-hearsay-45, legalbench-hearsay-49, legalbench-hearsay-51
- **google/gemma-3-12b-it**: 8/20 pairs pass rule/scope plus admitted pair delta; 3 of those are killed only by the explicit polarity probe. Current fully gated pairs: 1.
  - Probe-induced pair IDs: legalbench-hearsay-33, legalbench-hearsay-35, legalbench-hearsay-44

## Verdict

`POLARITY-PROBE-INDUCED-FALSE-FAILURE` is confirmed as a harness failure mode. This does not rescue D0 v2: the dangling never-seen baseline, generic neutral salience, and exclusion-reason confound remain independent blockers.
