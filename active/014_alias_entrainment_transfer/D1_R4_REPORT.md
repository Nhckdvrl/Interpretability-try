# 014 Alias Entrainment Transfer — D1 r4 report

日期：2026-08-30
结论：**CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC**

## 1. 结论先行

Qwen3-8B、Gemma-3-12B-IT 与 Llama-3.1-8B-Instruct 都强烈复现了 broad
cross-surface transfer：上下文只出现 surface A 时，从未出现的同实体 surface B 相对强关联、
不同 referent 的 `ASSOC_ANY` 控制获得额外 +2.90 至 +4.12 nats。这个差值在两个 frame、
两个方向、三家族及同类型 ASSOC sensitivity 中全部为正且 entity-cluster bootstrap CI 排除 0。

但 reference-specific money cell 没有通过。使用独立 foil 的 hard-identity gate 后，
`opaque_strict` 的 `ALIAS - ASSOC_ANY` 在三个家族都只有 mention 邻近 query 的 F2 为正；
mention 较早的 F1 CI 全部跨 0。未 gate 的全体 `opaque_strict` 在两个 frame、三个家族全部为
null。效应随 surface derivability 呈清楚梯度：compositional/partial 最大，opaque 较小，
opaque-strict 消失。

所以可支持的 ACL/EMNLP/NAACL 级叙事是：

> exact-token entrainment 会沿 learned surface-form relations 外溢，并与 mother entrainment
> machinery 共享上游原因；但经过强关联控制后，没有证据表明 shared referent 本身是特殊的
> causal unit。直接写入和结构梯度更符合 lexical/derivational path。

这不是 null 项目，但必须放弃 entity salience / reference identity 的强 claim。不能只取 F2、
某一方向或某类漂亮 alias 来续命。

## 2. Source 与 scope

- RedirectQA test 61,120 source rows；去重得到 10,226 个非退化 surface pairs、9,387 entities。
- 8,928 个 preregistered intended pairs 属于 `Aliases_and_Abbreviations` 或
  `Spelling_variants`；`Typical_Errors` 只保留作 diagnostic。
- raw bank 保留 all entity types、multiple aliases、both directions、Unicode，以及
  compositional/partial/opaque/opaque-strict 全部结构层。
- Wikidata 给出不同 referent 的真实关系候选；`P1889 different_from` 禁止作为 ASSOC。
- 7,771/10,226 source pairs 至少有一个 `ASSOC_ANY` candidate。
- Wikipedia `20231101.en` sentence scan：71,902 surfaces、200,454 requested ordered pairs、
  192,922,024 surface-sentence hits；实现版本 `d1-r4-cooc-v2`。
- 最终要求 `c(ASSOC,target) >= 1` 且
  `S(ASSOC→target) >= S(alias→target)`，同时禁止 target-token leakage。
- final bank：1,768 ordered items、1,471 surface pairs、1,370 entities；其中 confirmatory
  1,571 items、1,220 entities；1,288 items 有 `ASSOC_SAMETYPE` sensitivity。
- matched intended `opaque_strict` 在模型 gate 前有 323 entities，天然高于 60-entity floor。

所有 attrition 都在 raw population 之外单独报告；entity type、structure、direction、surface
class 与 capability 从未作为 construction convenience filter。确定性审计保存 source、ASSOC
candidate、matched control 与 unmatched source 各 20 rows。最终 matched-control sample 未发现
同指 ASSOC、target leakage 或 zero-joint control。

## 3. 实验合同

每个 ordered pair 固定 target surface B，并在同一 generic carrier 下比较：

1. `NOCTX`：无额外 mention；
2. `EXACT`：context 明示 B；
3. `ALIAS`：context 只出现同实体 A，B 不出现；
4. `ASSOC_ANY`：context 出现强关联但不同 referent 的 C；
5. `ASSOC_SAMETYPE`：若存在，使用与 target entity 同粗类型的 C。

F1 为 mention 较早的 `"{M} was in the news last week."`，F2 为 mention 更靠近 query 的
`"Yesterday's report briefly mentioned {M}."`。所有条件都精确计分相同 continuation
`" " + target_form`，主量是 continuation log-probability 相对 NOCTX 的变化，因此 tokenization
与 target length 在 item 内完全一致。

Q1 在全部 intended matched population 上检验 `ALIAS - ASSOC_ANY`。Q2 只在
hard-identity-gate-passed、intended、`opaque_strict` items 上检验相同差值。Gate 以不同实体、
同粗类型、token-length matched、与 target/seen/ASSOC 无 token overlap 的独立 rotated foil
做 A/B 双顺序测试；ASSOC 自己禁止作 foil。主统计先在同 entity 的多 surface/方向内平均，
再取 entity median 并做 10,000 次 entity-cluster bootstrap。

预注册判据要求 Q1/Q2 在至少两个模型家族和 **两个 frame** 都为正；单独 F2 不算通过。

## 4. 数据与实现完整性时间线

为了不隐藏负面工程 provenance，本轮三次 integrity correction 全部记录：

1. 模型调用前，source audit 发现 additive smoothing 会让两边 joint count 都为 0 的候选
   vacuously 打平。加入 `c(ASSOC,target) >= 1`，重冻 bank 后才首次运行。
2. 首次结果后，line count 1,768 但 unique ID 1,754，定位为 casefold hash collision。
   改成 exact source surface hash、增加 builder/runner/analyzer 唯一性断言，旧输出废弃，三家族重跑。
3. 第二次 integrity review 发现用 ASSOC 自身作 gate foil 与 Q2 循环。改为独立 rotated foil，
   再次重冻 bank，并将三家族全部重跑。前两轮数值不进入最终报告。

这些修订都加强 control 或修复标识完整性，没有按 effect direction 删除 entity type、surface
stratum、方向或模型。最终 bank 1,768/1,768 IDs 唯一，三家族 metadata 均记录 SHA256：
`917d178533925088fe1641a72e7481eb97e18c237466416cc15608391978db37`，且 tokenizer
boundary shifts 均为 0。

## 5. 模型与完整记录

| model | revision | items | probe records | main records | gate passed |
|---|---|---:|---:|---:|---:|
| Qwen3-8B | `b968826d9c46dd6066d109eabc6255188de91218` | 1,768 | 7,072 | 14,952 | 1,607 |
| Gemma-3-12B-IT | `96b6f1eccf38110c56df3a15bffe176da04bfd80` | 1,768 | 7,072 | 14,952 | 1,658 |
| Llama-3.1-8B-Instruct | `d10aef7999a2b5ba950ab3974312feeedbfe0b77` | 1,768 | 7,072 | 14,952 | 1,672 |

均使用本地 HF cache、BF16 和相同 continuation scorer。Q2 最终有效 entities 分别为 Qwen
261、Gemma 271、Llama 282，均显著高于预注册 floor；Q2 失败不是 denominator 不足。

## 6. Q1 broad result

下表是 entity-equal median `ALIAS - ASSOC_ANY` nats 与 95% bootstrap CI，n=1,220 entities。

| model | F1 | F2 |
|---|---:|---:|
| Qwen3-8B | +3.446 [+3.063, +3.823] | +3.567 [+3.224, +4.022] |
| Gemma-3-12B-IT | +4.117 [+3.494, +4.664] | +4.079 [+3.542, +4.727] |
| Llama-3.1-8B-Instruct | +3.216 [+2.814, +3.557] | +2.897 [+2.530, +3.271] |

Q1 三家族全部通过。`ASSOC_SAMETYPE` sensitivity 在 F1/F2 也全部显著：Qwen
+2.991/+3.105，Gemma +3.573/+3.282，Llama +2.731/+2.372 nats。两个方向分别覆盖
1,083 个 alias→canonical entities 与 398 个 canonical→alias entities，六个 family×frame
方向结果全部显著为正。Exact mother control 相对 ASSOC 也在三家族两个 frame 全部强正。

## 7. Q2 reference-specific result

下表是独立 gate 后 `opaque_strict` 的 `ALIAS - ASSOC_ANY`。

| model | entities | F1 | F2 | both-frame pass |
|---|---:|---:|---:|---:|
| Qwen3-8B | 261 | +0.851 [−0.027, +1.412] | +0.833 [+0.320, +1.380] | no |
| Gemma-3-12B-IT | 271 | +0.159 [−0.718, +0.978] | +1.127 [+0.112, +1.802] | no |
| Llama-3.1-8B-Instruct | 282 | +0.619 [−0.035, +1.278] | +0.787 [+0.108, +1.162] | no |

F2 三家族为正，但 F1 三家族都跨 0，因此 Q2 passing families = 0。只报告 F2 为 money cell
会把原问题缩成 recency-sensitive adjacent mention，不允许这样改题。

更强的 falsification 是不加 model gate 的 323-entity `opaque_strict` population：Qwen
F1/F2 为 −0.027/+0.266，Gemma −0.357/+0.352，Llama +0.019/+0.182，六个 CI 全部跨 0。

结构梯度则高度稳定：

- compositional：三家族中位数约 +4.59 至 +7.32 nats；
- partial：约 +4.34 至 +6.83；
- opaque：约 +1.72 至 +2.54，仍全部显著；
- opaque-strict：约 −0.36 至 +0.35，全部不显著。

这与 phase 3 “entrainment heads 的 direct write 偏 lexical/seen-form，随 orthographic overlap
增强”一致，而不是 shared referent 在最不透明 surface 间提供稳定 residue。

## 8. 最终判定与论文路由

按 r4 contract：Q1 三家族通过，Q2 零家族通过，最终 verdict 固定为
**CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC**。

可以保留并发展：

- exact-string entrainment 之外的 broad learned cross-surface spillover；
- 三家族、双 frame、双方向与强 ASSOC 控制的一致性；
- compositional → partial → opaque → opaque-strict 的结构梯度；
- phase 2 的 shared upstream cause；
- phase 3 的 lexical direct-write boundary。

必须删除或明确否定：

- entity/reference-specific salience 已成立；
- entrainment heads 表示共享 referent；
- F2-only residual 可替代 both-frame criterion；
- 通过 person-only、单方向或漂亮 opaque alias subset 复活 Q2。

014 仍具有论文潜力：正贡献不是“发现 entity circuit”，而是为 ACL 2025 mother phenomenon
建立跨 surface 的外溢范围及其 lexical/reference 边界，并用因果 phase 2/3 与大规模 r4 behavior
形成统一叙事。下一步若继续，应围绕已成立的 learned-relation/structure gradient 做非
reference-specific mechanism synthesis；reference-specific Phase 4 不授权。

## 9. Reproduction

在本目录、`/home/xiang/miniconda3/envs/fgvd/bin/python` 下：

```bash
python src/alias_entrainment/build_d1_candidates.py
python src/alias_entrainment/fetch_wikidata.py
python src/alias_entrainment/build_d1_assoc.py --api-workers 8
python src/alias_entrainment/count_cooccurrence.py --workers 16
python src/alias_entrainment/build_d1_bank.py
python src/alias_entrainment/audit_d1_r4.py

PYTHONPATH=src python -m alias_entrainment.run_d1_r4 \
  --model Qwen/Qwen3-8B --tag qwen3_8b --device cuda:0 --batch-size 32

PYTHONPATH=src python -m alias_entrainment.analyze_d1_r4 \
  --tags qwen3_8b gemma3_12b_it llama31_8b_it
```

如果只因 exact-surface ID schema 修复而已有冻结 ASSOC metadata，可用
`refresh_assoc_pair_ids.py` 机械更新 pair IDs；正常从头重建不需要该步骤。
