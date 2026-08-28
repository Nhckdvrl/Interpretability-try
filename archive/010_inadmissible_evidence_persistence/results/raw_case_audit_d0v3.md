# D0 v3 raw-case audit

Status: `EXPLORATORY-LOCAL / FINAL-CALIBRATION / TERMINAL-HOLD`

Both raw files contain 720 rows (24 cases × 30 request variants). Candidate
mapping was checked directly in the raw rows: under both answer orders,
`target_label` points to the option containing the target verdict and `p_target`
selects that label. The large struck sign reversals are therefore not a label
inversion in the scorer.

## Qwen3-8B

- Strongest negative: `d0v3-legalbench-34-reliability_based`. Admitted polarity
  delta `+0.99999`; struck delta `-0.98416`; all four natural struck variants
  are negative. In the pro-target member, admitted `P(target)` is approximately
  1 and struck `P(target)` approximately 0; the pro-other member reverses those
  probabilities under both answer orders. Neutral shift `0.12012` fails control.
- Strongest clean positive: `d0v3-legalbench-52-procedural_truth_neutral`.
  Admitted delta `+0.99999`, struck delta `+0.31348`, all four natural variants
  positive, neutral shift `0.04709`; this is the sole strong pair. One case
  cannot rescue the pooled result.
- Largest generic-context artifact:
  `d0v3-legalbench-37-reliability_based`, neutral shift `0.38709` versus struck
  delta `-0.12113`.
- Boundary/sign-flip example:
  `d0v3-legalbench-39-procedural_truth_neutral` has struck delta `+0.32703` but
  neutral shift `0.20722`, so it is not diagnostic.
- Explicit polarity diagnostic fails in 5/12 pairs, but this probe is no longer
  a capability gate. All 12 admitted pair gates pass.

## Gemma3-12B

- Strongest negative: `d0v3-legalbench-40-procedural_truth_neutral`. Admitted
  delta `+0.99999`, struck delta `-0.99987`, all four natural struck variants
  negative. Neutral shift `0.37033` fails control.
- Most positive pair: `d0v3-legalbench-52-procedural_truth_neutral`. Struck delta
  `+0.24510` and neutral shift `0.00314`, but only 2/4 natural variants are
  positive, so it fails wording/order consistency.
- Largest generic-context artifact:
  `d0v3-legalbench-49-procedural_truth_neutral`, neutral shift `0.76290` and
  struck delta `-0.99934`.
- All 12 admitted pair gates and all 12 direct polarity diagnostics pass. The
  failure is therefore not low polarity capability.

## Audit verdict

The capability repair worked: both models pass 12/12 paired admitted operators.
The experiment still fails because neutral struck context moves the verdict in
9/12 Qwen pairs and 10/12 Gemma pairs. Large negative struck deltas appear under
correct mappings and both exclusion reasons, but cannot be interpreted while
the generic-context control is broken. Per the frozen stop rule, this is logged
only as an inversion diagnostic; no new phenotype is declared and no v4 is run.
