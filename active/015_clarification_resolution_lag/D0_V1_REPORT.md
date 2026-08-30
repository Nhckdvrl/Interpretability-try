# 015 Clarification Resolution Lag — D0 v1 report

日期：2026-08-30
结论：**NO-PROMOTE — matched-history fatal control not passed**

## 1. 结论先行

在预注册的 recognition gate 内，Qwen3-8B、Gemma-3-12B-IT 和
Llama-3.1-8B-Instruct 都出现了很小的
`DIRECT_RESOLVED - AMBIGUITY_HISTORY` accuracy 差值。但中性的等轮次
`MATCHED_HISTORY` 也造成同量级差值；真正识别 ambiguity-specific residual 的
`MATCHED_HISTORY - AMBIGUITY_HISTORY` 在三个家族都不显著。

因此，这轮结果支持“额外对话历史会造成很小的行为变化”，不支持“先前的 ambiguity
state 在 clarification 后特异性残留”。按运行前 README 的 KILL/ROUTE 规则，这一版不进入
full validation、PRACTIQ 扩展或机制实验，也不通过筛 subtype 缩窄题目续命。

## 2. Source 与 scope

- Source：`Apocalypse-AGI-DAO/CondAmbigQA-2K`，dataset v2.0，Apache-2.0；HF
  fingerprint `454e3246b10dddf6`。
- 2,000 个 source questions，3,822 个 source properties。
- 1,451 个问题有至少两个解释，产生 4,426 个完整保留的有向 target–distractor pairs。
- 549 个单 property 问题保留在 raw/source bank，但不具备本实验所需的 paired contrast。
- 所有 4,426 个方向均通过空值、答案相等和规范化字符串包含检查；没有为效果做 validity
  删除。
- matched measurement 层为每个 target 通过稳定 hash 选择一个 distractor，共 3,273
  pairs。全量 ordered-pair bank 没有被覆盖或删除。
- D0 是从 matched bank 按预注册 hash 做的 400-pair 成本样本，覆盖 376 个独立问题；
  property-count 分布为 2: 267，3: 129，4: 2，5: 2。
- 已保存完整 2,000-row source snapshot、raw question/property projections、all-pair bank、
  matched bank、40-row source audit，以及 20 survivor + 20 non-selected alternative 的
  attrition audit。

人工 source audit 没有发现 question/property index、condition 或 answer 串位。部分 source
interpretations 在语义上天然接近，例如同一角色的长期演员与短暂替演；这类 case 没有被人工
删掉，而是由运行前定义的 wrong-condition 双顺序 capability gate 决定是否可用于 phenotype。

## 3. 实验合同

每个 pair 固定同一个 question、target condition、target answer 与另一个 source-valid answer：

1. `DIRECT`：question 与 resolving condition 同轮提供；
2. `AMBIGUITY_HISTORY`：question → generic ambiguity clarification → 同一 condition；
3. `MATCHED_HISTORY`：question → 同词数 neutral history → 同一 condition；
4. `WRONG_CONDITION`：换成 distractor 的 source condition，gold 必须翻到 distractor answer。

所有条件都跑 target-first 与 target-second 两个 answer order。主 gate 要求同一 pair 在
`DIRECT` 与 `WRONG_CONDITION` 的两个顺序全部正确。估计量先在 pair 内合并 answer order，
再按 question 做 10,000 次 cluster bootstrap，避免一个多-property question 被当作多个独立
问题。

## 4. 模型与完整性

| model | revision | records | gated pairs | gated rate |
|---|---|---:|---:|---:|
| Qwen3-8B | `b968826d9c46dd6066d109eabc6255188de91218` | 3,200 | 285 | 71.25% |
| Gemma-3-12B-IT | `96b6f1eccf38110c56df3a15bffe176da04bfd80` | 3,200 | 366 | 91.50% |
| Llama-3.1-8B-Instruct | `d10aef7999a2b5ba950ab3974312feeedbfe0b77` | 3,200 | 245 | 61.25% |

两者均使用本地 HF cache、BF16、官方 chat template 和精确下一 token A/B 归一化概率；A/B
均验证为各模型的单 token continuation。数据 SHA256：
`db93784aebd3001531bf4c9221d9aafb5b1a4ba286b658c5e3b8c571f6e81641`。

## 5. 主要结果

下表均为 recognition-gated、question-cluster-equal 的 accuracy 百分点差与 95% bootstrap CI。

| model | DIRECT − AMBIGUITY | DIRECT − MATCHED | MATCHED − AMBIGUITY |
|---|---:|---:|---:|
| Qwen3-8B | +1.379 [+0.551, +2.390] | +1.287 [+0.368, +2.206] | +0.092 [−0.551, +0.735] |
| Gemma-3-12B-IT | +0.723 [+0.145, +1.517] | +0.434 [+0.072, +0.939] | +0.289 [−0.289, +1.012] |
| Llama-3.1-8B-Instruct | +1.064 [+0.213, +2.340] | +1.277 [+0.426, +2.340] | −0.213 [−1.064, +0.426] |

概率 readout 给出相同结论：

| model | DIRECT − AMBIGUITY | DIRECT − MATCHED | MATCHED − AMBIGUITY |
|---|---:|---:|---:|
| Qwen3-8B | +0.911 [+0.206, +1.756] | +0.738 [+0.106, +1.476] | +0.173 [−0.285, +0.664] |
| Gemma-3-12B-IT | +0.669 [+0.131, +1.421] | +0.333 [+0.056, +0.713] | +0.336 [−0.110, +0.973] |
| Llama-3.1-8B-Instruct | −2.777 [−3.693, −1.895] | −2.639 [−3.518, −1.752] | −0.138 [−0.357, +0.074] |

这些是概率百分点。关键第三列在三个家族都跨 0，因此不能把 DIRECT 与 HISTORY 的差值归因于
ambiguity state。

作为不加 capability gate 的 broad check，Qwen 的 mean-order accuracy 是 DIRECT 91.38%、
AMBIGUITY 93.25%、MATCHED 92.25%；Gemma 分别为 97.25%、96.75%、96.75%；Llama
分别为 88.88%、92.63%、92.00%。这也不支持一个跨家族、broad population 上稳定的
ambiguity-history penalty。Qwen 有 A/B 总体位置差异（93.25% vs 89.19%），Llama 也有
反向位置差异（85.69% vs 94.25%），Gemma 基本没有（96.88% vs 96.69%）；主测量的双顺序
反平衡与 hard gate 防止该偏好成为 phenotype。

## 6. 判定

预注册 PROMOTE 要求 matched-history effect 明显更小，并在至少两个模型家族出现
ambiguity-specific lag。实际结果是：

- 三个家族的 direct–ambiguity 小 accuracy 差值都存在；
- 三个家族的 neutral matched history 都解释了同量级差值；
- 三个家族的 matched–ambiguity CI 都跨 0；
- Llama 的 probability readout 甚至显示两种 history 都提高而不是降低 gold probability；
- ungated broad result 不稳定，Qwen 方向甚至相反；
- 没有理由启动 probe、patch、head ablation 或按 question type 挑选 money cell。

所以 D0 v1 的规范结论是 **NO-PROMOTE / matched-history fatal control not passed**。这不是一个
达到 ACL/EMNLP/NAACL main 证据链的正现象；继续把题缩到某个 question subtype 会改变原始
scientific population，违反本项目的 scope 纪律。

## 7. Reproduction

在本目录、`/home/xiang/miniconda3/envs/fgvd/bin/python` 下运行：

```bash
PYTHONPATH=src python -m clarification_lag.build_bank \
  --contract configs/d0_contract.json --output-dir data/d0_v1 --audit-n 40

PYTHONPATH=src python -m clarification_lag.run_choices \
  --model Qwen/Qwen3-8B --model-label qwen3_8b \
  --data data/d0_v1/d0_smoke_pairs.jsonl --contract configs/d0_contract.json \
  --output results/qwen3_8b_d0_v1.jsonl --device cuda:0 --batch-size 32

PYTHONPATH=src python -m clarification_lag.analyze \
  --inputs results/qwen3_8b_d0_v1.jsonl results/gemma3_12b_it_d0_v1.jsonl \
  --output results/d0_v1_summary.json --bootstrap-replicates 10000
```

Gemma 使用同一 runner，将 model/model-label/output 分别替换为
`google/gemma-3-12b-it`、`gemma3_12b_it` 和
`results/gemma3_12b_it_d0_v1.jsonl`。
