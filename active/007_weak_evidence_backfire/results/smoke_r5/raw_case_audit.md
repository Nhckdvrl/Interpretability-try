# 007 frozen two-family smoke: raw-case audit

Date: 2026-08-29  
Frozen D0: `b1f6f88983b68e2764ff99964debd71a307dc0209c2cb9d2bb8f6d7484fd9792`  
Audit rule: inspect all 25 scenario pairs and 50 directional summaries; no positive subset was selected for inference.

## Completeness

| model | raw lines | directions | scenario pairs | support-gated directions | capability-gated directions | gated pairs |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-8B | 3800 | 50 | 25 | 0 | 0 | 0 |
| Gemma3-12B-IT | 3800 | 50 | 25 | 8 | 6 | 1 |

## Recognition and controls

- Qwen: 50/50 directions failed the support recognition gate; consequently there are no eligible downstream cases. The apparent movements in raw summaries are not phenotype evidence.
- Gemma: 42/50 directions failed the support recognition gate. Of 8 support-gated directions, 2 failed the downstream capability gate; all 6 capability-gated directions failed the strong-evidence/primary control requirements (`strong=false`).
- No model produced a strong scenario pair. The Qwen pair denominator is empty. Gemma's only pair in the denominator is `wine:10:proline`.
- The Gemma gated pair failed pragmatic completeness, matched-length, neutral, bidirectional, and strong-evidence requirements. Its neutral artifact flag is false (`neutral_artifact_fraction=1.0` at aggregate level).

## Representative raw cases

The following are deterministic representatives from the frozen summaries, included to make the failure auditable. They are not used to rescue or redefine the result.

| model/case | gate status | belief backfire | action backfire | relevant observation |
|---|---|---:|---:|---|
| Qwen `breast:01:mean_radius` | capability fail | -0.492 | -0.486 | apparent movement is in the opposite sign and recognition is not established |
| Qwen `wine:06:nonflavanoid_phenols` | capability fail | +0.001 | +0.001 | closest-looking ungated movement is effectively zero |
| Gemma `wine:10:proline`, supports_target | capability pass, pair gated | -0.431 | -0.501 | direction is opposite to the required target-support backfire signature; neutral/control failure remains |
| Gemma `wine:10:proline`, supports_other | capability pass, pair gated | -0.704 | -0.007 | matched direction does not yield the required positive target movement |
| Gemma `breast:11:worst_radius`, supports_target | support pass, capability fail | -0.098 | -0.002 | downstream gate failure; not eligible evidence |

## Domain concentration

| model | domain | gated pairs | mean belief backfire | strong pairs |
|---|---|---:|---:|---:|
| Qwen3-8B | breast-cytology | 0 | null | 0 |
| Qwen3-8B | wine-origin | 0 | null | 0 |
| Gemma3-12B-IT | breast-cytology | 0 | null | 0 |
| Gemma3-12B-IT | wine-origin | 1 | -0.495647 | 0 |

The only Gemma gated pair is concentrated in `wine-origin` and is a single failed pair, not a positive domain effect. No domain was removed from analysis.

