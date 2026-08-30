# 017 D0 v1 report — Cross-Modal Resolution Inertia

**Decision:** `NO-PROMOTE`

**Date:** 2026-08-30

**Contract:** `configs/d0_contract.json` (`017-d0-v1`)

## Bottom line

三家族都出现过某种 history-dependent degradation，但没有形成同一个、能通过严格控制的 **interpretation-specific cross-modal inertia** phenotype：

- Qwen 的 ordinal commitment 强于控制，但 exact-label 主对比方向相反；
- Gemma 的 exact-label persistence 点估计较大，但有效 gate / cluster 数不足，控制差值 CI 不过零；
- Llama 的 text-first persistence 最强且 denominator 足够，但 masked condition 几乎完全复制该效应，说明主要是 text-first / late-image processing cost，而不是旧 interpretation 的身份被保留。

至少两个家族通过全部冻结门槛的要求没有满足（实际为 0/3）。不能在结果后把题目收窄成“Qwen ordinal wording effect”或“Llama late-image cost”；这两者都是与原研究问题不同的 family-specific phenomena。

## Data and integrity

官方 source 固定为：

- annotations: `THUNLP-MT/MUCAR@930eb28610c9799ee0caf81c7c0b59ac33cb372c`；
- images: `kevindragon221/MUCAR@3a28f23644e54a58c6131b41fe762a04869ee7cc`；
- source annotation SHA-256: `9d100e26587386352143acc3ea81ba152e21aebcd7f1db9155b4f01b6391fb22`；
- materialized bank SHA-256: `19fe5f8068a901dce5ce70a3183aa9c5f301dd1ddadaacef17dc164b3fc169f0`。

372 条 dual-ambiguity annotations 中，186 条 `image_id` 唯一命中 released image，覆盖 English / Chinese / Malay = 64 / 64 / 58、39 个 `pair_id` clusters、38 张唯一图像。另外 186 条的 ID 缺少 `-1` / `-2` 后缀且两个候选图均存在；实验没有猜映射，也没有按 gold 选图。排除清单和两个候选路径完整保存在 ignored data artifact `data/d0_v1/excluded_release_mapping_defects.jsonl`。

每次 inference 前逐图重算 SHA-256。186 个 item ID、question、二元 options、gold mapping 全部通过完整性检查。25 条将分离的 source `context` 与 `question` 正确拼接。所有 image-bearing conditions 对同一 item 使用 byte-identical source image。

## Models and records

| Family | Released model revision | Precision | Records | Runtime |
|---|---|---:|---:|---:|
| Qwen | `Qwen3-VL-2B-Instruct@89644892...` | BF16 | 2,604 | 424 s |
| Gemma | `gemma-3-12b-it@96b6f1ec...` | BF16 | 2,604 | 359 s |
| Llama | `Llama-3.2-11B-Vision-Instruct-bnb-4bit@25bca24a...` | released 4-bit conversion | 2,604 | 649 s |

每家族为 186 items × 2 option orders × 7 conditions。Llama 的量化差异是 family-level limitation；本实验不比较跨家族 effect magnitude。

## Gated money cell

Gate: within item-order, `text_only wrong AND simultaneous correct`。CI 为按 source `pair_id` 跨语言聚类的 10,000 次 bootstrap 95% interval。

| Family | Gated item-orders | Pair clusters | Actual-label persistence | Ordinal persistence | Masked persistence | Matched persistence | Image-first persistence |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen | 56 | 21 | .321 [.188, .462] | .679 [.475, .855] | .429 [.250, .608] | .411 [.254, .569] | .393 [.228, .561] |
| Gemma | 45 | 20 | .667 [.452, .841] | .556 [.324, .773] | .489 [.289, .673] | .444 [.250, .650] | .333 [.200, .477] |
| Llama | 67 | 29 | .687 [.566, .795] | .687 [.565, .793] | .672 [.547, .783] | .209 [.086, .371] | .149 [.058, .258] |

### Paired fatal controls

| Family | Actual − matched | Ordinal − matched | Ordinal − masked | Simultaneous − actual gold probability |
|---|---:|---:|---:|---:|
| Qwen | −.089 [−.280, .091] | .268 [.095, .465] | .250 [.133, .385] | .145 [.023, .277] |
| Gemma | .222 [−.111, .531] | .111 [−.292, .490] | .067 [−.085, .231] | .560 [.373, .722] |
| Llama | .478 [.317, .611] | .478 [.316, .610] | .015 [.000, .053] | .390 [.278, .486] |

Option-order gates remained populated in both directions: Qwen 29/27, Gemma 24/21, Llama 24/43 canonical/reversed. All three languages also remained in every family gate. Thus the verdict is not caused by a single empty language or option order.

## Frozen-gate audit

| Requirement | Qwen | Gemma | Llama |
|---|:---:|:---:|:---:|
| ≥50 gated item-orders | pass | fail | pass |
| ≥25 pair clusters | fail | fail | pass |
| actual−matched ≥.10 and CI >0 | fail | fail | pass |
| ordinal−matched CI >0 | pass | fail | pass |
| ordinal−masked CI >0 | pass | fail | fail |
| actual gold-probability drop CI >0 | pass | pass | pass |
| **family promotes** | **no** | **no** | **no** |

## Interpretation and paper-level judgment

The broad causal question remains interesting, but D0 does not support the proposed paper claim at ACL / EMNLP / NAACL standard.

1. **Not a unified cross-family phenotype.** The strongest response form changes by family: ordinal for Qwen, exact label for Gemma, and any text-first history for Llama.
2. **The strongest adequately powered result fails the identity control.** Llama's masked persistence (.672) is essentially the same as actual / ordinal (.687). The treatment therefore does not need the old interpretation's identity.
3. **Static multimodal capability is not the explanation, but neither is interpretation inertia.** The gate already requires simultaneous success. The remaining Llama effect is best described as a sequential-format or late-image integration cost.
4. **The official-release defect limits recovery by brute-force scaling.** Half the target population cannot be mapped without author-provided corrections. Guessing suffixes would contaminate the causal test.

### Route

Do not spend the next experiment on narrower wording searches inside 017. Reopen only if the dataset authors provide a deterministic mapping for the missing 186 rows or if a new benchmark supplies substantially more uniquely mapped dual-ambiguity clusters. Even then, the masked control must remain fatal. The current artifacts are preserved as a complete negative result and the pipeline proceeds to 018.

## Reproducibility artifacts

- preregistration: `configs/d0_contract.json`;
- builder / prompts / runner / analyzer: `src/cross_modal_inertia/`;
- tests: `tests/` (8 passed);
- raw outputs: `results/d0_{qwen,gemma,llama}.jsonl`;
- model metadata: corresponding `*.metadata.json`;
- combined analysis: `results/d0_analysis.json`.

Raw-output SHA-256:

```text
qwen  0b51dbd18bff576b9cb7b4ee058bad733721d71df400382c59cc8bfef6f7253c
gemma 0919acdc2e2e9f0dea36c1880bb5a52383e9fb916a3b423f165b28dd791d3018
llama d8fe87b1e03e8bdec9506a96c9bf75383faeb0ca855b7f33a44d5cdd7e801ab8
```
