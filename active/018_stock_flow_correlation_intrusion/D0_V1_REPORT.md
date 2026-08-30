# 018 D0 v1 Report — Stock–Flow Correlation Intrusion

**Decision:** `NO-PROMOTE`

**Date:** 2026-08-30

**Contract:** `018-d0-v1`

## Bottom line

The preregistered broad claim is not supported. None of Qwen, Gemma, or Llama supplied a recognition-gated denominator in all four natural `net direction × inflow trend` cells. Every strictly gated item in every family had positive net flow. The controlled inflow-attraction estimand is therefore non-estimable, and no family passes promotion.

This result must not be converted into a canonical-option-only or positive-net-only claim. Those variants would remove the fatal controls that distinguish downstream stock-flow intrusion from polarity, arithmetic, and answer-order failure.

## Frozen design

- Natural 2×2: net/storage up or down × inflow trend up or down.
- 600 ResOpsUS v2 windows, exactly 150 per cell, from 200 reservoirs.
- Six daily flow observations after an initial storage value.
- Five stock conditions: direct, model-recognized semantic net history, explicit correct net, masked history, and formula reminder.
- Two inflow/outflow column orders and two answer orders.
- Strict Q1 gate: all four net-recognition presentations correct.
- Stock-up probabilities averaged across all four stock presentations.
- Reservoir-cluster bootstrap, 10,000 replicates.
- Promotion required ≥50 gated items in every cell, ≥50 reservoirs, ≥5pp actual-history attraction with positive CI, positive explicit-correct-net CI, consistent directions and columns, in at least two families.

The contract and bank were frozen before model outcomes.

## Source and data audit

The source is ResOpsUS v2, Zenodo record 6612040, archive MD5 `d0684cbacf6196c246c73b858ab5b752`, CC-BY-4.0. The active builder scanned 678 official `time_series_all` files and found 719,074 eligible windows across 274 reservoirs after nonnegative-flow, continuity, rounded-sign, closure, net-margin, and inflow-trend filters.

The selected bank contains 600 windows from 200 reservoirs. A reservoir contributes at most two windows per cell, and selected starts from the same reservoir are at least 30 days apart. A 40-window source audit reproduced every displayed value from official CSVs to prompt precision. The bank SHA-256 is `27e2ca2cd1bf01c1172d55290dfb2d4ba4381c40af6f4d1fd58a2f3a3efecbf6`.

An early candidate bank admitted negative flow values. It was rejected before any model output was retained, the nonnegative-flow criterion was added, and the final bank was rebuilt and re-audited. All reported runs use only the final hash above.

## Models and raw coverage

| Family | Snapshot | Raw rows | Runtime |
|---|---|---:|---:|
| Qwen | Qwen3-8B `b968826…` | 14,400 | 391.1 s |
| Gemma | Gemma-3-12B-IT `96b6f1…` | 14,400 | 642.7 s |
| Llama | Meta-Llama-3.1-8B-Instruct-compatible `d10aef…` | 14,400 | 303.8 s |

The locally complete NousResearch mirror was used for the Llama-family checkpoint because the official local cache lacked a complete tokenizer. All inference used BF16 and the same final bank.

Raw SHA-256 checksums:

- Qwen: `835f3bf9e82fc9d13e90aaba2af43443a811f5839f551647084ba15af7731b09`
- Gemma: `56b85ace4279e4f1cf1e77cb792fd9f3c34062d90d179edca2feb5b09005a546`
- Llama: `10159e5633b7c6d643b5ce4156f76dffef825fcfc804fc85362f6c1194198d28`

## Recognition gate

| Family | Gated | Rate | Reservoirs | down/down | down/up | up/down | up/up |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen | 292 | 48.7% | 154 | 0 | 0 | 146 | 146 |
| Gemma | 300 | 50.0% | 156 | 0 | 0 | 150 | 150 |
| Llama | 127 | 21.2% | 94 | 0 | 0 | 18 | 109 |

The missing negative-net cells are not a sampling artifact: each input cell contains 150 items. Presentation-level Q1 accuracy identifies the failure:

| Family | Cell | Overall | inflow-first canonical / reversed | outflow-first canonical / reversed |
|---|---|---:|---:|---:|
| Qwen | net-down, inflow-down | 29.8% | 60.7% / 4.0% | 54.7% / 0.0% |
| Qwen | net-down, inflow-up | 9.8% | 24.7% / 2.0% | 12.7% / 0.0% |
| Gemma | net-down, inflow-down | 20.7% | 48.0% / 32.7% | 0.0% / 2.0% |
| Gemma | net-down, inflow-up | 11.5% | 31.3% / 14.7% | 0.0% / 0.0% |
| Llama | net-down, inflow-down | 49.7% | 98.7% / 0.0% | 100% / 0.0% |
| Llama | net-down, inflow-up | 45.3% | 82.0% / 0.0% | 99.3% / 0.0% |

Qwen and Gemma show a strong positive-net preference. Llama shows an extreme answer-order dependency: negative-net recognition is high when the correct answer occupies the canonical position and zero when the options reverse. These failures invalidate a local-computation-correct denominator for half of the 2×2.

## Stock-stage diagnostic

The full direction-controlled estimand and both column-order estimands are non-estimable for every family. `null` values in the machine-readable analysis deliberately represent missing strata, not zero effects.

For transparency, the positive-net-only direction differences are diagnostic and not confirmatory:

| Family | Condition | Inflow-direction difference | 95% reservoir-cluster CI |
|---|---|---:|---:|
| Qwen | direct | +11.72pp | [+6.71, +16.57] |
| Qwen | actual semantic net | −0.23pp | [−1.43, +0.81] |
| Qwen | explicit correct net | −0.22pp | [−1.45, +0.82] |
| Gemma | direct | +5.43pp | [+2.09, +8.89] |
| Gemma | actual semantic net | −4.91pp | [−8.29, −1.72] |
| Gemma | explicit correct net | −4.79pp | [−8.17, −1.59] |
| Llama | direct | +9.13pp | [+7.28, +11.01] |
| Llama | actual semantic net | +1.67pp | [+0.32, +2.97] |
| Llama | explicit correct net | +1.67pp | [+0.36, +2.96] |

The direct prompt can display an inflow-aligned difference in the surviving positive-net subset. Once the correct semantic net direction is placed into history, Qwen is approximately null, Gemma reverses direction, and Llama remains below the frozen 5pp threshold. This is not the proposed cross-family local-correct/downstream-ignore phenotype.

## Promotion audit

Every family fails the minimum gated items in all four cells, ≥5pp actual-history attraction, positive actual and explicit-correct-net CIs, and consistent net-direction and column-order checks. All families exceed 50 gated reservoirs, but that single check is insufficient. Promoted families: zero. Overall decision: `NO-PROMOTE`.

## Paper-level judgment

The broad question remains conceptually legitimate and the natural-data design is auditable, but D0 does not provide the stable local-recognition substrate required for an ACL/EMNLP/NAACL paper about downstream stock-flow correlation intrusion. The observed failure is dominated by polarity and presentation sensitivity before the proposed mechanistic dissociation can be identified.

Accordingly: do not add a second natural source merely to search for a favorable subset; do not weaken the four-presentation gate; do not retell the result as positive-net-only; preserve the benchmark, raw outputs, analysis, and failure report; move to the next registered topic.

## Artifact map

- `configs/d0_contract.json`: frozen contract.
- `data/d0_v1/d0_bank.jsonl`: final bank.
- `data/d0_v1/source_audit_sample.jsonl`: source audit sample.
- `data/d0_v1/scope_summary.json`: source and selection counts.
- `src/stock_flow_intrusion/`: builder, prompts, runner, analysis.
- `results/d0_{qwen,gemma,llama}.jsonl`: raw scored outputs.
- `results/d0_{qwen,gemma,llama}.metadata.json`: environments and snapshots.
- `results/d0_analysis.json`: standards-compliant combined analysis.
- `tests/`: construction, counterbalancing, estimand, missing-stratum, and diagnostic tests.
