# D0 candidate audit — NetEaseCrowd source pairs

Candidates: `d0_candidates_netease.jsonl`  
Raw CSV SHA256: `e9ebddfee58aaba5f64b1759506d5b7c3839b04bfb80a61b471358b4372430ee` (matches `RAW_MANIFEST.md`: yes)  
Audit seed: `20260829`  ·  LR margin: `2.0`  ·  min per class: cal `20` / val `10`

Scenarios: **22**  ·  capability domains: **4**  ·  unique annotators: **44**  ·  max scenarios in one (domain, label-pair) cell: **2**

Per domain: `capability-50` 6, `capability-52` 4, `capability-53` 6, `capability-56` 6

## Automated re-derivation over all rows

Each statistic is recomputed from the raw release and compared against the stored record and the model-visible text.

| check | rows passing |
|---|---|
| 1 workers globally unique | 22/22 |
| 2 calibration/validation tasks disjoint | 22/22 |
| 3 accuracy floor+ordering on both splits | 22/22 |
| 4 both-direction LR ordering on both splits | 22/22 |
| 5 visible profile matches raw history | 22/22 |
| 6 message identical across sources | 22/22 |
| 7 delay records from unrelated tasks | 22/22 |
| 8 delay carries no truth/answer/focal source | 22/22 |
| 9 reinstatement restores source only | 22/22 |
| 10 provenance complete | 22/22 |

No row fails any check.

## Fixed-seed manual audit sample (n=20)

Read these rows against the rendered prompts in the companion file before signing.

| scenario | low | high | cal acc | val acc | cal tLR lo→hi | val tLR lo→hi | cal oLR hi←lo | val oLR hi←lo | cal n/class | val n/class | 10 checks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `50:0v1:001` | 2185 | 114 | 0.551 → 0.962 | 0.553 → 0.972 | 2.45 → 18.75 | 2.34 → 33.19 | 0.837 → 0.022 | 0.858 → 0.026 | 23 | 16 | all pass |
| `50:0v2:001` | 7799 | 7736 | 0.565 → 0.851 | 0.556 → 0.951 | 2.44 → 6.62 | 3.00 → 7.06 | 0.334 → 0.138 | 0.407 → 0.023 | 22 | 17 | all pass |
| `50:0v2:002` | 13761 | 1493 | 0.570 → 0.854 | 0.576 → 0.914 | 2.69 → 5.93 | 3.15 → 22.21 | 0.301 → 0.118 | 0.383 → 0.065 | 23 | 12 | all pass |
| `50:1v2:002` | 355 | 10013 | 0.563 → 0.879 | 0.560 → 0.868 | 1.91 → 11.96 | 1.83 → 17.41 | 0.519 → 0.096 | 0.511 → 0.106 | 182 | 130 | all pass |
| `52:0v1:001` | 249 | 91 | 0.653 → 0.887 | 0.645 → 0.891 | 1.74 → 6.67 | 1.66 → 6.34 | 0.464 → 0.032 | 0.476 → 0.036 | 906 | 634 | all pass |
| `52:0v1:002` | 67 | 126 | 0.686 → 0.825 | 0.678 → 0.829 | 2.06 → 5.27 | 2.01 → 5.79 | 0.367 → 0.065 | 0.390 → 0.091 | 224 | 124 | all pass |
| `52:0v2:001` | 59 | 113 | 0.599 → 0.848 | 0.591 → 0.842 | 2.15 → 7.76 | 2.15 → 9.65 | 0.410 → 0.084 | 0.413 → 0.128 | 225 | 149 | all pass |
| `52:1v2:001` | 57 | 128 | 0.611 → 0.732 | 0.624 → 0.741 | 1.50 → 3.68 | 1.59 → 4.47 | 0.570 → 0.091 | 0.557 → 0.134 | 145 | 85 | all pass |
| `53:0v1:001` | 3322 | 99 | 0.567 → 0.799 | 0.551 → 0.809 | 2.64 → 6.14 | 2.61 → 5.73 | 0.425 → 0.159 | 0.471 → 0.099 | 148 | 85 | all pass |
| `53:0v1:002` | 2443 | 2359 | 0.554 → 0.788 | 0.565 → 0.718 | 2.97 → 6.98 | 3.58 → 14.67 | 0.490 → 0.146 | 0.532 → 0.220 | 47 | 26 | all pass |
| `53:0v2:001` | 1874 | 1329 | 0.557 → 0.700 | 0.565 → 0.732 | 3.01 → 6.31 | 3.16 → 9.57 | 0.472 → 0.228 | 0.524 → 0.090 | 21 | 19 | all pass |
| `53:0v2:002` | 2731 | 1054 | 0.555 → 0.692 | 0.554 → 0.680 | 2.54 → 6.32 | 3.36 → 6.76 | 0.392 → 0.162 | 0.390 → 0.180 | 407 | 270 | all pass |
| `53:1v2:001` | 2116 | 2274 | 0.552 → 0.797 | 0.557 → 0.706 | 1.93 → 6.66 | 1.73 → 6.61 | 0.504 → 0.096 | 0.484 → 0.123 | 59 | 45 | all pass |
| `53:1v2:002` | 1682 | 773 | 0.566 → 0.730 | 0.550 → 0.746 | 2.29 → 7.00 | 2.29 → 5.71 | 0.439 → 0.158 | 0.519 → 0.109 | 63 | 31 | all pass |
| `56:0v1:001` | 9490 | 9082 | 0.561 → 0.891 | 0.573 → 0.958 | 1.53 → 8.48 | 1.63 → 24.50 | 0.513 → 0.072 | 0.458 → 0.130 | 22 | 11 | all pass |
| `56:0v1:002` | 6160 | 9257 | 0.573 → 0.916 | 0.565 → 0.912 | 2.53 → 87.59 | 2.21 → 82.21 | 0.264 → 0.103 | 0.292 → 0.045 | 45 | 37 | all pass |
| `56:0v2:001` | 7597 | 7974 | 0.550 → 0.907 | 0.551 → 0.926 | 2.48 → 11.93 | 2.40 → 25.74 | 0.500 → 0.008 | 0.499 → 0.040 | 58 | 39 | all pass |
| `56:0v2:002` | 13587 | 7316 | 0.562 → 0.831 | 0.559 → 0.968 | 2.95 → 6.74 | 2.71 → 57.35 | 0.337 → 0.162 | 0.346 → 0.015 | 37 | 29 | all pass |
| `56:1v2:001` | 9347 | 9159 | 0.560 → 0.907 | 0.552 → 0.929 | 2.46 → 15.81 | 2.59 → 39.79 | 0.386 → 0.068 | 0.408 → 0.025 | 95 | 61 | all pass |
| `56:1v2:002` | 8683 | 8744 | 0.566 → 0.894 | 0.559 → 0.923 | 2.72 → 6.62 | 2.32 → 23.40 | 0.706 → 0.075 | 0.762 → 0.113 | 22 | 12 | all pass |

## What still needs a human

The checks above are mechanical. Signing `d0_verdict: PASS` additionally requires a reader to confirm, on the sampled prompts, that the scenario reads as a natural annotation-review setting, that the intervening records carry no case evidence, and that the source reminder restores only who spoke and how well calibrated they are.
