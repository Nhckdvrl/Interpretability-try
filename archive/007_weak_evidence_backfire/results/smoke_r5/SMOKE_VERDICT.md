# 007 Weak-Evidence Backfire — frozen two-family smoke

Date: 2026-08-29  
Smoke execution commit: `0ef5ee612ccb251f5ded2fe301487c925455405a`; result is now preserved on merged `main` commit `230e176ab4bd969bf28291c753990055b753c6e8`.  
Frozen D0 SHA256: `b1f6f88983b68e2764ff99964debd71a307dc0209c2cb9d2bb8f6d7484fd9792`  
Environment: local `.venv-vllm`, Python 3.12.13, torch 2.13.0+cu130, transformers 5.16.1, dtype `bfloat16`, exact continuation log-probability scorer.  
Model revisions resolved from the local Hugging Face cache: Qwen3-8B `b968826d9c46dd6066d109eabc6255188de91218`; Gemma3-12B-IT `96b6f1eccf38110c56df3a15bffe176da04bfd80`. The runner summaries record `revision=null` because the revision flag was omitted; the loaded local cache `refs/main` are the frozen revisions above.

## Execution and completeness

At the smoke commit, `pytest -q` was **17 passed**. Frozen D0 materialized 25 scenarios and `validate-data` returned 25 validated scenarios. Both model raw outputs contain exactly **3800 lines** (`50 directions × 76 requests`), so the harness completed without result truncation.

After the smoke, a concurrent remote main commit (`3cbe5e2`) was merged and pushed. Its stricter validator makes six existing synthetic unit fixtures lack held-out LR metadata, and the current environment lacks the new builder's `sklearn` dependency; a post-merge `pytest -q` therefore reports **12 passed, 6 failed**. This is recorded as an engineering follow-up and does not change or invalidate the already completed raw smoke outputs or their frozen-D0 checksum.

Raw audit: [raw_case_audit.md](raw_case_audit.md)

## Model aggregates

| metric | Qwen3-8B | Gemma3-12B-IT |
|---|---:|---:|
| total scenarios / directions | 25 / 50 | 25 / 50 |
| recognition-gated directions | 0 | 6 capability-gated (8 support-gated) |
| gated scenario pairs | 0 | 1 |
| mean pair belief backfire | null | -0.495647 |
| belief 95% CI | [null, null] | [-0.495647, -0.495647] |
| mean pair action backfire | null | -0.250170 |
| action 95% CI | [null, null] | [-0.250170, -0.250170] |
| strong pair fraction | 0.000 | 0.000 |
| support-gate fraction | 0.000 | 0.160 |
| pragmatic pair survival | 0.000 | 0.000 |
| matched-length pair survival | 0.000 | 0.000 |
| bidirectional backfire fraction | 0.000 | 0.000 |
| neutral artifact fraction | 0.000 | 1.000 |
| mean direction asymmetry (belief) | null | 0.416736 |
| positive domains | 0 | 0 |
| verdict | `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR` | `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR` |
| model pass | false | false |

Gemma's only gated pair was `wine:10:proline`; its pair-level belief and action movements were negative, not the required positive sign reversal. It also failed completeness, matched-length, neutral, and bidirectional controls. The negative pair values therefore do not establish an alternative phenotype under this contract.

## Decision

**007: HARD KILL for this frozen operationalization — no backfire phenotype.**

The two-family first shot does not establish the prerequisite evidence-direction capability. Qwen has no eligible denominator. Gemma has one eligible pair, but it fails every decisive survival requirement and shows the opposite aggregate sign. The appropriate result is a scientific null/capability-floor failure, not prompt selection, threshold changes, subset selection, or a second model panel.

Do not run N1, mechanism work, or an expanded panel for 007 from this result. Preserve the raw outputs and this audit as the reproducible failure record.

## 012 and 013 scope

No model calls were made for 012 or 013 in this round. 012 remains `D0-AUDITING` pending a frozen, task-disjoint natural source set and manual audit; 013 remains `HOLD-D0`.
