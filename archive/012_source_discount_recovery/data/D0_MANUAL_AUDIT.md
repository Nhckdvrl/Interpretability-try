# D0 candidate audit — NetEaseCrowd source pairs

Candidates: `frozen_d0.jsonl`  
Raw CSV SHA256: `e9ebddfee58aaba5f64b1759506d5b7c3839b04bfb80a61b471358b4372430ee` (matches `RAW_MANIFEST.md`: yes)  
Audit seed: `20260829`  ·  LR margin: `2.0`  ·  min per class: cal `20` / val `10`

Scenarios: **108**  ·  capability domains: **4**  ·  unique annotators: **216**  ·  max scenarios in one (domain, label-pair) cell: **15**

Per domain: `capability-50` 45, `capability-52` 4, `capability-53` 14, `capability-56` 45

## Automated re-derivation over all rows

Each statistic is recomputed from the raw release and compared against the stored record and the model-visible text.

| check | rows passing |
|---|---|
| 1 workers globally unique | 108/108 |
| 2 calibration/validation tasks disjoint | 108/108 |
| 3 accuracy floor+ordering on both splits | 108/108 |
| 4 both-direction LR ordering on both splits | 108/108 |
| 5 visible profile matches raw history | 108/108 |
| 6 message identical across sources | 108/108 |
| 7 delay records from unrelated tasks | 108/108 |
| 8 delay carries no truth/answer/focal source | 108/108 |
| 9 reinstatement restores source only | 108/108 |
| 10 provenance complete | 108/108 |

No row fails any check.

Per (domain, label-pair) cell: `50:0v1` 15, `50:0v2` 15, `50:1v2` 15, `52:0v1` 2, `52:0v2` 1, `52:1v2` 1, `53:0v1` 6, `53:0v2` 3, `53:1v2` 5, `56:0v1` 15, `56:0v2` 15, `56:1v2` 15

Inferential stratification, fixed here rather than after the model runs: a cell is **primary** when the frozen bank gave it at least 5 scenarios. **8 primary cells / 101 scenarios** across 3 capabilities carry promotion, equally weighted by cell mean, with the interval from a bootstrap that resamples eligible cells and then scenarios within each resampled cell. **4 undersized cells / 7 scenarios** (`52:0v1` 2, `52:0v2` 1, `52:1v2` 1, `53:0v2` 3) are executed and reported, but cannot move PASS/HOLD/KILL and can never be promoted into the primary set afterwards.

## Fixed-seed manual audit sample (n=20)

Drawn stratified by cell, so every cell is represented before any cell is sampled twice. Read these rows against the rendered prompts in the companion file before signing.

| scenario | low | high | cal acc | val acc | cal tLR lo→hi | val tLR lo→hi | cal oLR hi←lo | val oLR hi←lo | cal n/class | val n/class | 10 checks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `50:0v1:001` | 7276 | 9294 | 0.587 → 0.904 | 0.637 → 0.880 | 2.62 → 21.39 | 4.75 → 10.17 | 0.321 → 0.091 | 0.212 → 0.052 | 60 | 33 | all pass |
| `50:0v1:015` | 13592 | 13616 | 0.578 → 0.788 | 0.557 → 0.782 | 2.33 → 6.50 | 2.55 → 6.75 | 0.299 → 0.100 | 0.326 → 0.153 | 150 | 102 | all pass |
| `50:0v2:006` | 2079 | 7729 | 0.575 → 0.796 | 0.573 → 0.830 | 4.18 → 9.74 | 4.95 → 14.86 | 0.327 → 0.134 | 0.354 → 0.154 | 43 | 26 | all pass |
| `50:0v2:010` | 7265 | 13714 | 0.568 → 0.797 | 0.585 → 0.853 | 2.66 → 5.72 | 3.28 → 16.00 | 0.460 → 0.205 | 0.344 → 0.152 | 57 | 31 | all pass |
| `50:1v2:003` | 2163 | 7266 | 0.580 → 0.876 | 0.614 → 0.853 | 2.91 → 11.73 | 3.48 → 7.73 | 0.301 → 0.081 | 0.241 → 0.081 | 171 | 105 | all pass |
| `50:1v2:007` | 2060 | 7543 | 0.600 → 0.843 | 0.595 → 0.848 | 4.65 → 11.94 | 2.13 → 10.74 | 0.261 → 0.097 | 0.297 → 0.111 | 28 | 13 | all pass |
| `52:0v1:001` | 67 | 126 | 0.686 → 0.825 | 0.678 → 0.829 | 2.06 → 5.27 | 2.01 → 5.79 | 0.367 → 0.065 | 0.390 → 0.091 | 224 | 124 | all pass |
| `52:0v1:002` | 249 | 252 | 0.653 → 0.770 | 0.645 → 0.817 | 1.74 → 6.93 | 1.66 → 8.33 | 0.464 → 0.216 | 0.476 → 0.120 | 186 | 131 | all pass |
| `52:0v2:001` | 59 | 91 | 0.599 → 0.895 | 0.591 → 0.891 | 2.15 → 5.59 | 2.15 → 5.67 | 0.410 → 0.029 | 0.413 → 0.032 | 944 | 627 | all pass |
| `52:1v2:001` | 57 | 128 | 0.611 → 0.732 | 0.624 → 0.741 | 1.50 → 3.68 | 1.59 → 4.47 | 0.570 → 0.091 | 0.557 → 0.134 | 145 | 85 | all pass |
| `53:0v1:005` | 4550 | 3950 | 0.551 → 0.641 | 0.567 → 0.714 | 2.38 → 4.96 | 2.53 → 6.37 | 0.471 → 0.234 | 0.379 → 0.135 | 28 | 12 | all pass |
| `53:0v1:006` | 2225 | 263 | 0.583 → 0.685 | 0.556 → 0.688 | 2.17 → 4.84 | 1.94 → 4.67 | 0.424 → 0.186 | 0.436 → 0.207 | 80 | 53 | all pass |
| `53:0v2:002` | 2731 | 1054 | 0.555 → 0.692 | 0.554 → 0.680 | 2.54 → 6.32 | 3.36 → 6.76 | 0.392 → 0.162 | 0.390 → 0.180 | 407 | 270 | all pass |
| `53:0v2:003` | 1468 | 3014 | 0.554 → 0.670 | 0.585 → 0.731 | 2.00 → 4.17 | 5.23 → 13.87 | 0.391 → 0.130 | 0.512 → 0.250 | 25 | 18 | all pass |
| `53:1v2:004` | 1682 | 948 | 0.566 → 0.719 | 0.550 → 0.695 | 2.29 → 6.32 | 2.29 → 8.11 | 0.439 → 0.215 | 0.519 → 0.254 | 87 | 51 | all pass |
| `53:1v2:005` | 936 | 2077 | 0.551 → 0.725 | 0.568 → 0.677 | 1.99 → 4.71 | 2.30 → 5.52 | 0.423 → 0.201 | 0.493 → 0.178 | 24 | 19 | all pass |
| `56:0v1:010` | 3136 | 9082 | 0.745 → 0.891 | 0.614 → 0.958 | 3.00 → 8.48 | 5.16 → 24.50 | 0.153 → 0.072 | 0.415 → 0.130 | 22 | 11 | all pass |
| `56:0v1:012` | 6160 | 9288 | 0.573 → 0.806 | 0.565 → 0.786 | 2.53 → 11.61 | 2.21 → 4.49 | 0.264 → 0.117 | 0.292 → 0.073 | 35 | 26 | all pass |
| `56:0v2:010` | 8818 | 9385 | 0.601 → 0.876 | 0.632 → 0.868 | 4.45 → 18.27 | 4.49 → 14.03 | 0.206 → 0.076 | 0.174 → 0.073 | 494 | 353 | all pass |
| `56:1v2:011` | 6884 | 6646 | 0.603 → 0.824 | 0.605 → 0.885 | 3.07 → 7.43 | 3.11 → 12.27 | 0.354 → 0.118 | 0.340 → 0.158 | 67 | 38 | all pass |

## Human audit

Recorded result on the sampled rows: **20/20 PASS (2026-08-29)**

The reader confirmed, on the rendered prompts rather than on this table, that each scenario reads as a real annotation-review task carrying the released question, that the intervening records hold only unrelated task/task-set/completion-time metadata with no answer, truth, reported option or focal annotator, and that the source reminder restores identity, accuracy and report-specific likelihood ratios without restating which option was reported.
