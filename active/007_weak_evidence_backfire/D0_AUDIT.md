# D0 audit — Weak-Evidence Backfire

Date: 2026-08-29  
Verdict: `PASS`  
Frozen artifact: `data/frozen_d0.jsonl` (deterministically materialized by `data/materialize_frozen_d0.py`)  
Items: **25**  
Domains: **2**  
Manual random audit: **20/20 PASS**

## External sources

### Breast Cancer Wisconsin (Diagnostic)

- UCI dataset DOI: `10.24432/C5DW2B`
- license: **CC BY 4.0**
- natural task: malignant vs benign diagnosis from fine-needle-aspiration measurements
- frozen scenarios: 15 distinct measurement features

### Wine

- UCI dataset DOI: `10.24432/C5PC7J`
- license: **CC BY 4.0**
- natural task: chemical-analysis-based cultivar provenance
- only cultivar 1 vs cultivar 2 records are used, making the frozen decision binary and exhaustive within the filtered source population
- frozen scenarios: 10 distinct chemical features

The frozen derivation used the scikit-learn 1.8.0 packaged copies of these UCI datasets. SHA-256 hashes of the exact numeric source arrays are stored in every record so local regeneration can detect a source-version mismatch.

## Split discipline

Feature thresholds are never justified by the same rows used for held-out confirmation.

For every source dataset:

1. make one fixed stratified split with seed `20260829`;
2. use 60% only to select thresholds and compute the model-visible calibration frequencies;
3. use the disjoint 40% only as a pre-model D0 stability check;
4. require the same direction and weak/strong ordering on the held-out split.

For target-support evidence:

```text
1 < LR_weak_cal < LR_strong_cal
1 < LR_weak_val < LR_strong_val
```

For other-support evidence, expressed as target/other LR:

```text
0 < LR_strong_cal < LR_weak_cal < 1
0 < LR_strong_val < LR_weak_val < 1
```

Across the 20 manually audited rows, held-out weak-target LR ranged from about `1.155` to `1.322`; strong-target LR ranged from `1.664` to `7.935`. Held-out weak-other LR ranged from about `0.705` to `0.869`; strong-other LR ranged from about `0.129` to `0.440`.

## Neutral control correction

The old r4 schema required `neutral_lr == 1` exactly. That is inappropriate for finite real data: an informative, nontrivial empirical cue will almost never have an estimated LR mathematically equal to one. Enforcing exact equality would push D0 toward an artificial random token.

The D0-compatible contract instead requires a real cue from the same external dataset whose LR is near one in **both** partitions:

```text
0.90 <= neutral_lr_calibration <= 1.10
0.90 <= neutral_lr_validation  <= 1.10
```

The frozen 25 rows are much tighter than the allowed bound: calibration neutral LR is about `1.010–1.031`, held-out neutral LR about `1.005–1.035`.

## Naturalness and transformation audit

The transformation is deliberately minimal:

- hypotheses are the source dataset's real class labels;
- evidence is a threshold statement about one real recorded feature;
- weak and strong cues are nested thresholds on the **same feature and same direction**;
- the model-visible calibration text reports empirical class-conditional counts from the fixed calibration partition;
- no evidence wording says “weak”, “strong”, “slight”, or otherwise labels the expected evidential strength;
- the no-evidence baseline contains no case-specific observation;
- the completeness protocol states only the experimental reporting rule, preventing omission-of-stronger-cue pragmatics from becoming evidence;
- action choices are symmetric workflow-routing decisions rather than asymmetric medical or financial utilities.

## Manual audit sample

The fixed audit sample was drawn with seed `20260829`. IDs:

```text
breast:01:mean_radius
breast:02:mean_texture
breast:03:mean_smoothness
breast:05:mean_concavity
breast:08:radius_error
breast:09:compactness_error
breast:10:concavity_error
breast:11:worst_radius
breast:12:worst_texture
breast:14:worst_compactness
wine:01:alcohol
wine:02:alcalinity_of_ash
wine:03:magnesium
wine:04:total_phenols
wine:05:flavanoids
wine:06:nonflavanoid_phenols
wine:07:proanthocyanins
wine:08:color_intensity
wine:09:od280/od315_of_diluted_wines
wine:10:proline
```

For all 20, the audit checked class exhaustivity in the filtered population, nested cue direction, calibration LR ordering, held-out LR ordering, neutral near-one stability, distinct cue text, source/license/provenance, and absence of case-specific evidence from the baseline.

## Remaining limitation before interpreting a smoke

Feature-level scenarios within one UCI dataset are not fully independent biological/chemical studies. The frozen G0 therefore keeps each feature as one scenario but any positive result must be interpreted with domain balance and followed by N1 / cross-dataset replication. A result driven only by one UCI domain does not satisfy the frozen `min_positive_domains=2` gate.
