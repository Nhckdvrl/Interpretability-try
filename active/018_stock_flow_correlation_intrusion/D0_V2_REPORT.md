# 018 D0-v2 semantic-recognition report

**Run date:** 2026-08-31
**Contract:** `018-d0-v2-semantic-recognition`
**Decision:** `NO-PROMOTE / NO-MI / TERMINAL FOR THIS REGISTERED CLAIM`

## Executive result

D0-v2 performed the single bounded repair authorized after D0-v1: replace the
letter-position-dependent net-flow gate with direct semantic scoring of the
exact one-token responses `positive` and `negative`. The natural ResOpsUS
population, frozen 600-window bank, balanced 2×2 semantic cells, stock readout,
downstream controls, estimand, bootstrap, and promotion threshold were not
changed.

The repair made more of the bank measurable, but it did not establish Stock–Flow
Correlation Intrusion. No family passed the preregistered minimum of 50 gated
items in every cell. More decisively, among the three families for which the
direction-controlled estimand was calculable, the `actual_net_history` inflow
attraction was +1.23pp for Qwen, −3.88pp for Gemma, and +0.75pp for Phi. None
reached the frozen +5pp threshold; Qwen and Phi intervals include zero, while
Gemma is significantly opposite to the registered direction. Llama's positive-
net cells were absent, so its tempting negative-net-only +6.48pp diagnostic
cannot be used as a rescue.

The final family count is 0/4. No second source, mechanism experiment, polarity
selection, numeric-sign D0-v3, or additional recognition repair is authorized.

## Frozen design

- Source: ResOpsUS v2, Zenodo record 6612040.
- Bank: 600 natural seven-row windows, 150 in each `net direction × inflow
  trend` cell, spanning 200 dams.
- Bank SHA-256:
  `27e2ca2cd1bf01c1172d55290dfb2d4ba4381c40af6f4d1fd58a2f3a3efecbf6`.
- Recognition: exact next-token probability over `positive` versus `negative`,
  averaged across inflow-first and outflow-first tables.
- Gate: the higher mean semantic probability must match the gold net direction.
  Column order is a diagnostic, not an all-presentations competence gate.
- Stock readout: unchanged higher/lower probabilities averaged across two
  column orders and two answer orders.
- Conditions: `direct`, `actual_net_history`, `explicit_correct_net`,
  `masked_net_history`, and `formula_reminder`.
- Estimand: equal-weight mean of the inflow-up minus inflow-down stock-up
  probability contrast within positive-net and negative-net strata.
- Uncertainty: 10,000 bootstrap replicates clustered by `dam_id`.
- Family promotion: at least 50 gated items per semantic cell, at least 50 dams,
  actual-history attraction ≥5pp with CI lower bound above zero, explicit-correct-
  net CI lower bound above zero, and positive effects in both net directions and
  both column orders. Overall promotion required at least two families.

The complete contract is machine-readable in `configs/d0_v2_contract.json`.

## Models and immutable revisions

| Family | Model | Cached revision | Rows | Runtime |
|---|---|---|---:|---:|
| Qwen | `Qwen/Qwen3-8B` | `b968826d9c46dd6066d109eabc6255188de91218` | 13,200 | 351.8s |
| Gemma | `google/gemma-3-12b-it` | `96b6f1eccf38110c56df3a15bffe176da04bfd80` | 13,200 | 523.9s |
| Llama | `NousResearch/Meta-Llama-3.1-8B-Instruct` | `d10aef7999a2b5ba950ab3974312feeedbfe0b77` | 13,200 | 264.7s |
| Phi | `microsoft/Phi-4-mini-instruct` | `cfbefacb99257ffa30c83adab238a50856ac3083` | 13,200 | 134.6s |

The required Qwen, Gemma, and Llama families are present. Phi is a fourth
independent family; a cached Mistral tokenizer artifact was incomplete and was
not fetched or silently substituted during a run.

## Primary results

Cell counts below follow `net_down/inflow_down`, `net_down/inflow_up`,
`net_up/inflow_down`, `net_up/inflow_up`.

| Family | Gated / 600 | Gated cells | Dams | Actual-history attraction (95% CI) | Explicit-correct-net (95% CI) | Promote |
|---|---:|---|---:|---:|---:|---|
| Qwen | 444 | 102 / 45 / 148 / 149 | 187 | +1.23pp [−0.16, +2.77] | +1.10pp [−0.33, +2.56] | No |
| Gemma | 353 | 39 / 14 / 150 / 150 | 168 | −3.88pp [−6.36, −1.63] | −3.83pp [−6.37, −1.58] | No |
| Llama | 303 | 150 / 150 / 0 / 3 | 159 | not estimable | not estimable | No |
| Phi | 388 | 79 / 10 / 149 / 150 | 174 | +0.75pp [−0.57, +2.01] | +0.71pp [−0.65, +1.97] | No |

Qwen was closest to the gate but its 45-item conflict cell is below the frozen
minimum. Its direct-prompt attraction was +5.00pp [1.39, 8.63], but it collapsed
after either the model-recognized semantic net direction or the correct net
direction was explicitly carried forward. That pattern contradicts the proposed
"correct local computation but downstream ignores it" phenotype rather than
supporting it.

Gemma's direct condition was +5.42pp [2.57, 8.25], but actual and explicit net
history reversed the effect. Phi remained small and null. Llama produced a
positive negative-net-only diagnostic, but the missing positive-net comparison
makes the registered direction-controlled estimand undefined. Selecting that
polarity would violate the frozen anti-rescue rule.

## Measurement audit

Semantic scoring removed arbitrary A/B answer-letter reversal from the gate,
but it did not eliminate family-specific polarity and table-order sensitivity.
For example, Qwen's net-down recognition accuracy was 86.7% versus 9.3% across
the two column orders in the inflow-down cell, and 78.7% versus 0% in the
inflow-up cell. Gemma and Phi showed the same weaker-negative pattern. Llama
showed the opposite polarity failure: all 300 negative-net items passed, while
only 3/300 positive-net items passed.

This diagnostic is important but not a reason for another gate repair. D0-v2
was the preregistered bounded measurement repair, and the downstream effect is
already below threshold or opposite in every estimable family.

## Adjudication

The broad natural question remains scientifically intelligible, but this
registered ResOpsUS phenotype does not clear its behavioral prerequisite. The
result is terminal `NO-PROMOTE / NO-MI`, not a claim that every possible LLM can
never exhibit a human stock-flow heuristic. The repository must not turn the
null into a narrower polarity-, prompt-, family-, or subset-specific paper.

No further literature search is needed for this adjudication. D0-v2 tests the
already registered claim directly; additional N1 work cannot repair a failed
behavioral prerequisite.

## Artifacts and reproduction

- Raw family rows and run metadata: `results/d0_v2/{qwen,gemma,llama,phi}.jsonl`
  and matching `.metadata.json` files.
- Machine-readable joint analysis: `results/d0_v2/analysis.json`.
- Frozen configuration: `configs/d0_v2_contract.json`.
- Runner and analyzer: `src/stock_flow_intrusion/run_model_v2.py` and
  `src/stock_flow_intrusion/analyze_v2.py`.

From this project directory, with the environment dependencies available:

```bash
PYTHONPATH=src python -m stock_flow_intrusion.run_model_v2 \
  --model Qwen/Qwen3-8B --family qwen --bank data/d0_v1/d0_bank.jsonl \
  --output results/d0_v2/qwen.jsonl --device cuda:0 --batch-size 32

PYTHONPATH=src python -m stock_flow_intrusion.analyze_v2 \
  results/d0_v2/qwen.jsonl results/d0_v2/gemma.jsonl \
  results/d0_v2/llama.jsonl results/d0_v2/phi.jsonl \
  --output results/d0_v2/analysis.json --replicates 10000

python -m pytest -q
```

Raw SHA-256 values are:

```text
qwen   4afabafa5df437e15d34817116c947c3cd63e9bc4e96d34566187be11e990fdd
gemma  bdf703321e5676b63a00ae5002b6871943c2fff7e3c72b3f4aba3d57fa8b1de4
llama  d3cbbc98a706be4e708e6db95435fb24b42bf85f144d4deb6894124c5024c5cb
phi    266b42ae698763821d4fa86897b7358ab90c868d7160c2b64c78927478d65bf6
joint  115b1497f4541a5fdfc4b6e3dad5fda660982d26a4b7ac1048938d31894802d4
```
