# D0 audit — Weak-Evidence Backfire

Date: 2026-08-29  
Verdict: `PASS`  
Frozen byte contract: locally materialized `data/frozen_d0.jsonl`  
SHA-256: `d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a`  
Items: **30**  
Domains: **2**  
Manual random audit: **20/20 PASS**

## External sources

### Breast Cancer Wisconsin (Diagnostic)

- UCI DOI: `10.24432/C5DW2B`
- license: **CC BY 4.0**
- task: malignant vs benign diagnosis from fine-needle-aspiration measurements
- frozen scenarios: **20** measurement-feature contracts

### Wine

- UCI DOI: `10.24432/C5PC7J`
- license: **CC BY 4.0**
- task: chemical-analysis-based cultivar provenance
- only cultivar 1 vs cultivar 2 records are used, making the frozen population binary and exhaustive
- frozen scenarios: **10** chemical-feature contracts

The exact source arrays are the scikit-learn packaged copies of these UCI datasets. Every row stores the SHA-256 of the exact numeric source arrays used for derivation. `data/build_frozen_d0.py` rebuilds the JSONL deterministically from those arrays; `data/verify_frozen_d0.py` requires a byte-for-byte rebuild and the frozen SHA above.

## Split and LR discipline

For each source population the builder performs one fixed class-wise split with seed `20260829`:

```text
60% calibration / threshold selection
40% D0 stability validation
```

No model output is involved in either split. Threshold candidates are selected only from calibration values. A feature is admitted to frozen D0 only if the same weak/strong direction and ordering survives the disjoint validation rows.

Likelihood ratios use Jeffreys 0.5-cell smoothing on the 2×2 event/class table. For target-support cues:

```text
1 < LR_weak < LR_strong
LR_strong >= 1.20 * LR_weak
```

For other-support cues, expressed as target/other LR:

```text
0 < LR_strong < LR_weak < 1
LR_strong <= LR_weak / 1.20
```

Those margin constraints hold in both calibration and validation. Across the 30 frozen rows, validation weak-target LR is about `1.113–1.834`, validation strong-target LR `1.602–8.893`, validation weak-other LR `0.481–0.933`, and validation strong-other LR `0.040–0.614`.

## Model-visible threshold / gold consistency

An earlier candidate D0 was rejected during this audit because some rounded threshold sentences did not reproduce their stored calibration counts. The final frozen D0 fixes that bug: the exact numeric threshold appearing in the model-visible evidence string is the same threshold used to compute every stored calibration/validation count and LR.

This is tested in two independent ways:

1. the deterministically materialized JSONL must satisfy the behavioral loader's LR and held-out constraints;
2. `verify_frozen_d0.py` reloads the original sklearn/UCI arrays, rebuilds all 30 rows from source, and requires **byte-for-byte equality** with the locally materialized `frozen_d0.jsonl` and the frozen SHA above.

## Neutral control

Finite real data should not be forced to produce an empirical LR mathematically equal to 1. The old exact-equality requirement would incentivize an artificial random token. The r5 contract therefore requires a real observation from the same source population with:

```text
0.90 <= LR_neutral_calibration <= 1.10
0.90 <= LR_neutral_validation  <= 1.10
```

The actual frozen controls are tighter: calibration LR `1.005–1.031`, validation LR `0.996–1.035`. The model probe asks whether the cue is **approximately non-diagnostic with nearly equal class-conditional rates**, not whether its LR is mathematically exactly 1.

## Naturalness / transformation audit

- hypotheses are the real source class labels;
- weak and strong evidence are nested threshold statements on the **same recorded feature and same direction**;
- model-visible calibration reports source-derived conditional counts, not verbal “weak/strong” labels;
- the `strong_gt_weak` capability probe no longer calls the alternatives `WEAK-CANDIDATE` / `STRONG-CANDIDATE`; it uses neutral `OBSERVATION 1/2` labels;
- the no-evidence baseline contains no case-specific observation;
- pragmatic-completeness states only the fixed reporting protocol and removes the inference that stronger unreported evidence was suppressed;
- action alternatives are symmetric routing decisions, avoiding asymmetric treatment utility.

The four most redundant breast geometry derivatives (`mean perimeter`, `mean area`, `worst perimeter`, `worst area`) were deliberately excluded from the 30-item set to reduce obvious item-level pseudoreplication.

## Manual audit sample

A fixed 20-row sample was drawn with seed `20260829` and checked against source-derived calibration/validation metadata, exact threshold text, LR direction/order, neutral stability, binary class definition, provenance/license, and prompt leakage:

```text
breast:01:mean_radius
breast:02:mean_texture
breast:03:mean_smoothness
breast:05:mean_concavity
breast:06:mean_concave_points
breast:09:perimeter_error
breast:11:compactness_error
breast:14:worst_radius
breast:15:worst_texture
breast:16:worst_smoothness
breast:17:worst_compactness
breast:19:worst_concave_points
breast:20:worst_symmetry
wine:01:alcohol
wine:02:ash
wine:03:alcalinity_of_ash
wine:04:magnesium
wine:05:total_phenols
wine:06:flavanoids
wine:07:proanthocyanins
```

Result: **20/20 PASS**.

## Statistical limitation

The 30 prompts are distinct feature-level natural scenarios, but they come from two source datasets and therefore are not 30 independent populations. This is acceptable for the first frozen smoke only because the promotion rule separately requires positive signal in both domains. A result driven by one domain is a fail. Any surviving effect must undergo N1 and additional external-dataset replication before a generality or mechanism claim.
