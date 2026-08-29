# Finding Rules — 如何找一个值得做的 LLM 可解释性题目

版本：2026-08-29  
状态：`AUTHORITATIVE DISCOVERY RULES`

本文件合并旧的 `PROCESS.md`、`REQUIREMENTS.md`、`NOVELTY_GATE.md`、`CONFERENCE_SCALE_AUDIT.md` 和短版 mining guide 中仍然有效的规则。以后寻找新题只维护这一份。

---

## 1. 我们到底在找什么

目标不是“找一个没人写过的 benchmark drop”，也不是先选 SAE / attention head / patching 再找故事。

理想题目应同时具有：

```text
自然 mother question
+ 一句话反直觉矛盾
+ decisive contrast
+ 可预测的结构 signature / wrong destination
+ 至少两个 competing mechanisms
+ 可落地自然数据
+ 明确 hard kill
```

最好的句式通常是：

> **模型明明 A，却仍然 B。**

其中 A 不是自报告式“知道”，而是可独立验证的能力/表征/规则理解；B 是规范上不应该发生、且有结构的 downstream failure。

### 优先从这些地方找

1. **人人都能理解的自然 failure**：真实知识、证据、记忆、工具、行动、社会协调、状态更新。
2. **强 mother paper 的真空**：论文已经证明一个 scientific object 重要，但留下 causal role、scope boundary、representation→use、lifecycle、implementation switch 等真正下一问。
3. **两个应分离的心智步骤**：识别任务 ≠ 执行策略；知道来源 ≠ 正确加权；表示状态 ≠ 用状态行动。
4. **规范关系被破坏**：invariance、monotonicity、reversibility、composition、state transition、binding。
5. **现实系统里的路径冲突**：prior vs evidence、old state vs current state、surface success vs semantic rule、retrieval vs use。

### 不优先从这些地方找

- 先决定一个心理学 bias 名字，再去模型里找样本；
- 一个数据集 × 一个 perturbation；
- 只有 prompt wording / option order 敏感；
- 换语言、模型、领域、payload 就声称新题；
- 只有平均 accuracy drop，没有结构性错误落点；
- 只有 probe accuracy，没有可区分的 causal question；
- pure synthetic toy world 是唯一行为锚点。

---

## 2. 主会尺度怎么判断

题目可以很窄，但证据链必须厚。ACL/EMNLP/NAACL Main 风格通常不是靠“覆盖很多任务”变大，而是形成：

```text
一句话 phenotype
→ 跨模型/设置稳定
→ decisive controls
→ 结构 signature
→ causal mechanism
→ 机制导出的预测 / 修复
```

删掉模型名、数据集名和 transformation 名以后，如果仍能讲出一个现实世界中重要、反直觉、且存在两个竞争计算解释的问题，才有主会尺度的可能。

### 一票否决的“小题味”

- 研究问题离开某 benchmark 就不存在；
- 只是已有 mother phenomenon 的一个 item subtype；
- 需要五六个 arbitrary condition 才能描述现象；
- 结果只有“模型会犯错”，没有为什么这个错误特别奇怪；
- 方法贡献与科学问题彼此可替换，换个 probe 也能讲同样故事。

---

## 3. 题目必须在 discovery 阶段一次做透

新项目正式注册前必须同时通过：

```text
N0 breadth PASS
+ N1 depth PASS
+ D0 source-feasibility PASS
= DISCOVERY-PASS
```

**N0、N1 和数据搜索都属于找题，不属于题目已经确定后的补票。**

### 3.1 N0 — breadth novelty screen

先冻结一句 claim，再快速攻击：

- exact / near-exact LLM phenotype；
- mother phenomenon + LLM；
- decisive contrast / wrong destination；
- 同义词、旧术语和邻近 benchmark；
- repo 里已经死亡的同 family / rename；
- 明显已经占位的 mechanism story。

N0 的任务是尽快杀掉明显撞车，不是证明绝对“没人做过”。

### 3.2 N1 — depth novelty closure

只对 N0 survivor 做，而且仍然在注册之前。

至少检查：

1. strongest 3–5 papers 全文；
2. appendix / supplement / limitations；
3. public code、released prompts、dataset notes；
4. predecessor / successor / citation chain；
5. mother paper 是否已经顺手回答我们的下一问；
6. exact factorial / intervention 是否已经存在；
7. 既有机制是否完整吸收 causal question；
8. 邻近现象是否在更强模型上已经自然消失。

必须留下：

```yaml
strongest_neighbor:
what_it_already_solves:
our_decisive_difference:
why_not_a_rename:
mother_inclusion_test:
mechanism_occupancy:
scale_survival_risk:
hard_kill:
search_date:
```

只允许写“截至 search date 未检索到完整覆盖”，不写绝对 `first`。

### 3.3 D0 source-feasibility — 找题时就把数据找好

正式注册前必须知道：

```yaml
source:
version:
license:
statistical_unit:
gold_source:
extraction_or_construction_recipe:
estimated_eligible_count:
feasibility_audit_ids: []   # >=20 real examples
external_validation_anchor:
```

最低要求：

- exact source/version 已锁定；
- license/adaptation/redistribution 条件明确；
- gold 来自原数据、正式 protocol、可执行语义或数学/程序 oracle；
- statistical unit 真实独立；
- dry-run 能估出足够 eligible cases；
- 随机人工看至少 20 个真实 source examples/pairs；
- nuisance/confound 在模型调用前列清楚。

#### 没有现成 paired data 时

允许：

```text
public natural source
→ deterministic/programmatic transformation
→ independently provable gold
→ dry-run confirms yield
→ >=20 sample naturalness/artifact audit
```

不允许：先注册题目，再发明 generator 或到处换数据源凑数量。

如果 source/gold/license/count 仍答不清，只能是 `HOLD-DISCOVERY-DATA`。

---

## 4. Candidate card：一个题至少要填到这个程度

```yaml
title:
mother_question:
plain_language_contradiction:
decisive_contrast:
structural_signature:
competing_mechanisms: []
hard_kill:

n0:
  obvious_neighbors: []
  verdict: PASS | HOLD | KILLED

n1:
  strongest_papers: []
  full_text_checked: true
  appendix_checked: true
  code_or_supplement_checked: true
  citation_chain_checked: true
  mother_inclusion_test:
  why_not_a_rename:
  mechanism_occupancy:
  scale_survival_risk:
  verdict: PASS | HOLD | KILLED

d0_feasibility:
  source:
  version:
  license:
  statistical_unit:
  gold_source:
  recipe:
  estimated_eligible_count:
  feasibility_audit_ids: []
  external_validation_anchor:
  verdict: PASS | HOLD | KILLED
```

填不完整就继续 discovery；不要创建 active project 等以后补洞。

---

## 5. DISCOVERY-PASS 之后才发生什么

题目确定 ≠ 现象已经成立。

```text
DISCOVERY-PASS
→ formal registration
→ materialize/freeze 已锁定 D0
→ READY-TO-SMOKE
→ two-family behavioral smoke
→ raw-case/scorer/capability/artifact audit
→ 3/5 family + size sequence
→ strong-model kill test
→ MECHANISM-READY
→ white-box mechanism
→ mechanism-derived prediction/method
```

注册后的 D0 **只做 materialization/freeze**：exact IDs、hash、split、provenance、gold verification。若发现必须换 source 或核心 recipe，退回 discovery。

模型 panel 的具体 checkpoint 约定见 [`MODEL_PANEL.md`](MODEL_PANEL.md)。

---

## 6. Behavior first：机制不能救行为

- matched control 上先证明模型有基础能力；
- 两个便宜独立家族先做 fatal smoke；
- 正式 generality 至少 3/5 家族同方向；
- 至少一个家族做三尺寸序列；
- 尽早做强模型 kill test；
- 看 paired raw trajectories 和 wrong destinations，不只看均值；
- deterministic scorer 优先，不依赖昂贵 LLM judge；
- behavior/generality 没过，不扫大量 layer/head/SAE 来“证明内部其实有东西”。

---

## 7. Stop-loss：什么时候必须砍

以下任一成立，默认 KILL / ROUTE / HOLD：

- exact/near-exact collision；
- mother paper 已逻辑包含 decisive contrast；
- 剩余 novelty 只是换 benchmark/domain/readout；
- 自然数据不存在，只能依赖任意 synthetic prompt；
- gold 需要研究者主观判断；
- capability gate 没过；
- effect 主要由 answer order、length、format、prompt artifact 解释；
- 跨模型不是同一个 phenotype；
- 强模型几乎消失且没有重要 scaling transition；
- 需要看完结果后改 subset、阈值、readout 或名字才能续命。

失败后记录到 [`FAILED_TOPICS.md`](FAILED_TOPICS.md)。**失败知识的价值是阻止 rename revival，不是给旧题找补。**

---

## 8. Novelty 什么时候可以重开

没有 routine post-smoke N1。只有三种触发：

1. core claim / decisive contrast / mechanism question 实质改变；
2. audit date 后出现具体新论文；
3. reviewer/collaborator 指出此前漏掉的具体 strongest neighbor。

此时做 targeted `NOVELTY-REFRESH`，只检查受影响部分。

---

## 9. 最终一句原则

> **找题阶段的目标不是尽快拥有一个题，而是尽快知道这个题是否值得存在。**

一个真正进入实验的题，应该已经做到：文献边界清楚、自然数据可拿、gold 可冻结、hard kill 已写好。GPU 只负责证伪现象，不负责替选题收拾残局。
