# 016 Mixed-Status Event Attraction — D0 v1 report

日期：2026-08-30  
结论：**NO-PROMOTE — same-status matched control explains the stitched-context effect**

## 1. 结论先行

Qwen3-8B、Gemma-3-12B-IT 与 Llama-3.1-8B-Instruct 在加入另一事件后，
分给该事件状态的概率都有上升。但当加入的是与 target **同状态**的匹配事件时，三个家族也
出现几乎同量级的变化。真正检验 mixed-status specificity 的
`MIXED_STATUS_NATURAL - SAME_STATUS_NATURAL` 在三个家族的主顺序 95% CI 均跨 0，
toward-neighbor 离散转移也不稳定。

完整原始 discourse 相对 target-local 在三个家族都提高 neighbor-label probability，但这个
条件同时恢复了更多 source-authored 语境，无法排除合法 discourse inference；而 no-explicit-
relation 层的 stitched mixed-minus-same 对比仍为 null。因此当前证据只支持一般性的
multi-event/context sensitivity，不支持 factuality status 在事件间特异性 attraction。

按预注册 PROMOTE/KILL 规则，本题不进入 full validation 或机制实验，也不把题目缩到单个
`PS+ -> CT+` 方向续命。

## 2. Source、标签与 scope

- Source：`upasanachatterjee/maven-fact` 的 train + validation；对应 Li et al.,
  Findings of EMNLP 2024。
- source fingerprints：train `c330566e8fdb425c`，validation
  `8b9b75cab58de6bb`。
- 按 MAVEN-FACT 定义冻结五类标签：`CT+` certain happened/will happen、`PS+`
  possible happened/will happen、`PS-` possible not happen、`CT-` certain not happen、
  `Uu` unknown。Prompt 只提供自然语言选项，不暴露 annotation code。
- 3,623 documents、91,719 mentions；label counts 为 CT+ 86,650、PS+ 2,718、
  CT- 1,876、PS- 337、Uu 138。
- 完整保存 1,916 documents 中的 350,834 个 ordered mixed-status pairs；存在同状态控制后，
  得到 88,522 个 matched pairs，覆盖 1,915 documents。
- D0 成本层按 direction 稳定 hash 抽 576 pairs、332 documents：16 个 primary ordered
  directions各 40 条，涉及 Uu 的方向各 12 条。distance、event type、relation 与
  same-sentence 都只是分析 factor，没有为效果筛除。
- D0 中 181/576 pairs 有 source explicit temporal/causal/subevent relation，61/576 在同句；
  其余均保留。

20 条 source audit 未发现 document、trigger、offset、label、句子窗口或关系映射串位。个别
source label 从普通语言直觉看有争议，但没有人工改 gold 或删样本。完整 source snapshot、
raw mentions、all-pair bank、matched bank、D0 bank、scope summary 与 audit sample 均保存在
本地 ignored `data/d0_v1/`，可由 builder 确定性重建。

## 3. 实验合同

每个 ordered `(target, mixed neighbor)` pair 另配一个同文档、同 target label 的 control
event。固定六个条件：

1. `TARGET_LOCAL`；
2. `SAME_STATUS_NATURAL`；
3. `SAME_STATUS_REVERSED`；
4. `MIXED_STATUS_NATURAL`；
5. `MIXED_STATUS_REVERSED`；
6. `FULL_LOCAL_DISCOURSE`。

每个条件再跑 canonical/reversed 两种 A–E answer order，共 12 records/pair。Target 与 context
trigger 分别用结构标签标出；same-status control 采用相同 prompt 结构。完整 discourse 是包含
两事件的原始连续窗口，不做句子拼接。

主 gate 要求 `TARGET_LOCAL` 在两个答案顺序都正确。主估计量先对 answer order 做 pair 内平均，
再按 document 做 10,000 次 cluster bootstrap。核心量是 neighbor label probability 的
`MIXED - SAME`，而不是普通 accuracy drop；同时报告恰好转向 neighbor label 的离散转移、
反向呈现、完整 discourse、每个方向以及 relation/same-sentence strata。

## 4. 模型与完整性

| model | revision | records | locally recognized | primary non-Uu |
|---|---|---:|---:|---:|
| Qwen3-8B | `b968826d9c46dd6066d109eabc6255188de91218` | 6,912 | 135/576 (23.44%) | 125 |
| Gemma-3-12B-IT | `96b6f1eccf38110c56df3a15bffe176da04bfd80` | 6,912 | 133/576 (23.09%) | 120 |
| Llama-3.1-8B-Instruct | `d10aef7999a2b5ba950ab3974312feeedbfe0b77` | 6,912 | 88/576 (15.28%) | 78 |

三家族均使用本地 HF cache、BF16、各自官方 chat template 与精确下一 token A–E 归一化概率；
A–E 都验证为单 token continuation。三个结果 metadata 的 input SHA256 一致：
`80896fd2a63cc0e305b488ac270f111507e753ff65b4712f1529703942f9cba0`。
低 recognition rate 本身也是预注册 kill 风险，尤其说明 rare-status directions 的有效样本不足。

## 5. 主要结果

下表为 primary non-Uu、recognition-gated pairs 上 neighbor-label probability 的百分点差与
document-cluster 95% CI。

| model | MIXED − LOCAL | SAME − LOCAL | MIXED − SAME | reversed MIXED − SAME | FULL − LOCAL |
|---|---:|---:|---:|---:|---:|
| Qwen3-8B | +4.438 [+1.358, +8.117] | +1.946 [+0.116, +4.228] | +2.491 [−0.158, +5.523] | +2.000 [+0.276, +4.275] | +7.227 [+3.154, +11.936] |
| Gemma-3-12B-IT | +3.733 [+1.594, +6.231] | +3.543 [+1.559, +5.897] | +0.190 [−1.737, +2.316] | −0.834 [−2.728, +0.900] | +5.079 [+2.485, +8.012] |
| Llama-3.1-8B-Instruct | +2.032 [+1.381, +2.758] | +2.168 [+1.507, +2.913] | −0.136 [−0.588, +0.384] | +0.098 [−0.424, +0.673] | +3.077 [+2.255, +3.974] |

关键第三列没有一个家族通过 CI；Qwen 只在 reversed 呈现显著，缺乏 order robustness。
`MIXED - SAME` 的 exact toward-neighbor transition 分别为 Qwen +1.65pp
[−1.65, +4.96]、Gemma 0.00pp [0.00, 0.00]、Llama +1.33pp [0.00, +4.00]，同样没有
跨家族稳定的 directional error。

Qwen 的 `PS+ -> CT+` 是最大的单方向信号：specific probability +17.58pp
[+0.71, +36.06]，但有效 n=16；Gemma n=24 时为 +4.43pp [−2.71, +12.02]，Llama n=7
时为 +2.15pp [−0.71, +6.31]，没有家族复现。它也与 CT+ 的极端基率和完整 discourse 中
可能存在的合法证据纠缠，不能作为缩窄后的新题。

no-explicit-relation 层的 specific `MIXED - SAME` 为 Qwen +0.80pp
[−1.29, +3.71]、Gemma +0.97pp [−1.08, +3.42]、Llama −0.29pp
[−0.72, +0.11]，三个家族都为 null。相反，`FULL - LOCAL` 在该层仍为正，进一步说明
完整语境变化不是 status-attraction 的诊断性证据。

## 6. 判定

预注册 PROMOTE 要求至少两个家族出现稳定 toward-neighbor attraction、same-status control
显著更弱、document bootstrap CI 不含 0，并覆盖至少两个方向或一个理论清晰的极强方向。
实际结果是：

- 表面的 `MIXED - LOCAL` 三家族为正，但 `SAME - LOCAL` 也三家族为正；
- 诊断性的 `MIXED - SAME` 三家族均未通过主顺序 CI；
- 离散 toward-neighbor transition 不稳定；
- 最大单方向只出现在 Qwen，Gemma 与 Llama 不复现；
- full-discourse effect 跨家族存在，但没有排除合法新增证据，且 no-relation stitched 对比为 null；
- recognition denominator 只有 15%–23%，稀有状态方向尤其薄弱。

因此 D0 v1 的规范结论是 **NO-PROMOTE / same-status matched control not passed**。该结果没有
达到 ACL/EMNLP/NAACL 级 broad phenomenon 的行为基础；不做 probe、patch 或 head ablation，
也不按方向、event type 或 relation 事后收窄。

## 7. Reproduction

在本目录、`/home/xiang/miniconda3/envs/fgvd/bin/python` 下运行：

```bash
PYTHONPATH=src python -m mixed_status_attraction.build_bank \
  --contract configs/d0_contract.json --output-dir data/d0_v1 --audit-n 20

PYTHONPATH=src python -m mixed_status_attraction.run_choices \
  --model Qwen/Qwen3-8B --model-label qwen3_8b \
  --data data/d0_v1/d0_smoke_pairs.jsonl --contract configs/d0_contract.json \
  --output results/qwen3_8b_d0_v1.jsonl --device cuda:0 --batch-size 32

PYTHONPATH=src python -m mixed_status_attraction.analyze \
  --inputs results/qwen3_8b_d0_v1.jsonl results/gemma3_12b_it_d0_v1.jsonl \
           results/llama31_8b_instruct_d0_v1.jsonl \
  --output results/d0_v1_summary.json --bootstrap-replicates 10000
```

Gemma 与 Llama 使用同一 runner，model 分别为 `google/gemma-3-12b-it` 与本地完整 cache
对应的 `NousResearch/Meta-Llama-3.1-8B-Instruct`。
