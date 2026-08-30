# 014 — Alias Entrainment Transfer

**中文一句话：** 上下文里只出现一个实体的名字 A，会不会把从未出现过、但与 A 指向同一对象的名字 B 也一起“带热”？如果会，这真的是 entity/reference identity，还是模型只是学过 A 和 B 经常相关？

**Status:** `D1-R4 COMPLETE / CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC`
**Created:** 2026-08-29
**Top-10 rank:** #3
**Canonical next contract:** [`configs/contract_d1_r4.yaml`](configs/contract_d1_r4.yaml)
**New D1 model call authorized:** **NO** — r4 已完成；Q2 未通过，不再用新模型或 subset 复活 reference claim。

---

## 1. Mother paper

Niu et al., ACL 2025 Main **Outstanding Paper**：

[*Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs*](https://aclanthology.org/2025.acl-long.791/)

Code: https://github.com/frankniujc/entrainment

Mother phenomenon：

> 一个 token 只要刚刚在 context 中出现过，它后续的 logit/probability 就会系统升高，即使这个 token 与当前问题无关，甚至是随机 token。

Mother paper 还找到一批 causally important **entrainment heads**：ablate 后 exact-token entrainment 明显减弱。

这部分已经被 mother 做掉，不能当我们的贡献。

---

## 2. 我们最初的问题

Mother 的 target token 本身都真的在 context 里出现过。

因此一个自然问题是：

> **contextual entrainment 的 causal unit 是“刚刚看见过的字符串”，还是“刚刚被激活的实体/概念”？**

例子：

```text
context 只出现：International Business Machines
后面 target 是：IBM
```

`IBM` 三个字符从没出现过。

如果 `IBM` 仍被提升，说明 exact surface repetition 不是全部故事。

但仅仅看到 transfer 还不能自动推出“entity representation”。这正是当前项目已经学到的最重要教训。

---

## 3. Phase 1 — 行为现象已经成立

原始四/五条件框架：

```text
NOCTX   无额外 context
EXACT   context 直接出现 target surface B
ALIAS   context 出现另一个 surface A，但 B 不出现
SEMREL  context 出现语义相关、不同指的实体 C
UNREL   原计划为弱相关/无关实体 D
```

目标量沿用 mother 的 logit shift：

```text
Δ_cond = log P(B | context_cond + carrier/query)
       - log P(B | no-context carrier/query)
```

### 已经观察到

三家族：

- Llama-3.1-8B-Instruct
- Qwen3-8B
- Gemma-3-12B-IT

都出现很强 EXACT mother effect。

更重要的是，`ALIAS - SEMREL` 在不同家族上约为 **+2.2 nats 量级**，说明一个从未出现过的 related surface form 确实可以被 context 中的另一个名字提升。

在后来人工 audit-clean + `opaque_strict` 子集上，effect 仍约：

```text
Llama: +2.06 nats
Qwen:  +1.31 nats
Gemma: +2.25 nats
```

三者 CI 都排除 0。

因此下面这个 behavioral reading 当前是可靠的：

> **contextual entrainment can transfer across learned surface-form relations.**

它不是一个 null 项目。

---

## 4. Phase 2 — shared upstream cause，但不是 entity proof

我们用 EXACT condition 定位 mother-like entrainment heads，再做 ablation。

结果：同一批 heads 的 ablation 同时减弱 EXACT 与 ALIAS transfer。

这排除了一个很简单的解释：

```text
EXACT 走 entrainment heads
ALIAS 完全走另一个独立 pathway
```

所以可以说 EXACT / ALIAS 至少共享一部分 upstream causal machinery。

**但这不等于这些 heads 表示 entity identity。**

当前正确措辞：

```text
shared upstream cause
```

而不是：

```text
shared entity representation
```

---

## 5. Phase 3 — direct write 更像 lexical / seen-form

DLA / direct-write 分析给了一个很重要的反证：

- entrainment heads 对 EXACT seen target 的 direct write 很强；
- 对 unseen alias 的 direct write 在严格子集上基本为 null；
- alias DLA 随 orthographic overlap 增强。

所以目前更合理的 picture 是：

```text
这些 heads 的直接输出偏 lexical / seen-form
但它们参与了一个更上游/更共享的过程，使 learned relation 的另一 surface 也受到影响
```

这进一步阻止我们把故事直接写成“entity neuron/head”。

---

## 6. 150-pair audit 暴露的 construct 问题

后来的完整 alias audit 是项目转折点。

旧 alias bank 中：

```text
compositional relations: ~39%
genuine conventional coreference: ~33%
outright non-coreferent: ~5%
```

也就是说，旧的 `opaque_strict` 只保证**正字法不透明**，并不保证是“两个名字真正指同一个实体”的 hard identity pair。

例子里可能混入：

- stage name / real name；
- title / person；
- geographic nickname；
- loose learned association；
- 甚至错误 pair。

因此旧 D0 证明的是：

```text
cross-surface learned-relation transfer
```

而不是：

```text
reference identity specifically causes transfer
```

---

## 7. UNREL bug

旧 UNREL builder 也发现了真实实现 bug：所谓 `UNREL` 并不是按最低 semantic similarity 正确选出的控制。

因此：

- 旧 UNREL-based conclusions 作废；
- 不能再用 `ALIAS > UNREL` 证明 anything strong；
- 当前 primary construct question 必须依赖新的 `ASSOC` control，而不是修补旧 UNREL。

这是 provenance，不允许从历史结果里删掉。

---

## 8. 为什么 `ALIAS > SEMREL` 仍不足以证明 entity identity

这是当前最核心的 conceptual point。

假设：

```text
A = International Business Machines
B = IBM
```

如果模型训练中反复学到 A 和 B 强关联，那么即使它没有一个真正共享的“entity identity state”，A 也完全可能通过 learned pair association 提升 B。

而一个普通 `SEMREL`：

```text
C = Microsoft
```

与 B 的关系结构并不匹配 A-B。

所以：

```text
ALIAS > SEMREL
```

最多说明 **A-B 特殊 learned relation 超过普通 semantic relatedness**。

它不能区分：

```text
H_entity: A 和 B 因共同 referent transfer
H_assoc:  A 和 B 因强 pair-specific learned association transfer
```

knowledge gate 也不能区分，因为两种 hypothesis 都预测“模型没学过 A-B 时 transfer 小”。

---

## 9. 当前真正的 D1：ALIAS vs ASSOC

所以 r4 的核心不是再找更漂亮的 alias，而是建立匹配控制：

```text
ALIAS:
A 与 B 真正 corefer / hard identity

ASSOC_ANY:
C 与 B 强关联、训练语料里高 co-occurrence
但 C 与 B 明确不是同一个 referent
```

决定性问题：

```text
Q1 broad:
ALIAS > ASSOC_ANY ?

Q2 hard reference-specific:
在 hard-identity + opaque_strict stratum 中
ALIAS > ASSOC_ANY ?
```

如果 Q1 有但 Q2 不稳定，合理结论是：

```text
CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC
```

而不是继续筛到只剩 20 个“最漂亮” entity pair。

---

## 10. r4 scientific population

Canonical contract：[`configs/contract_d1_r4.yaml`](configs/contract_d1_r4.yaml)

当前 scope 原则：

- RedirectQA broad surface-form population；
- all entity types；
- both valid directions；
- multiple aliases per entity；
- surface relation / type / direction / capability 都是 factor/stratum，不是 construction filter；
- primary control = `ASSOC_ANY`；
- sensitivity control = `ASSOC_SAMETYPE`；
- Wikipedia 20231101.en sentence co-occurrence 用来量化 association；
- Q2 preregistered capability floor：每家族至少 60 unique subject IDs。

最重要的是：**不能再为了让 Q2 成立一路加过滤条件。**

---

## 11. 下一次模型调用前必须完成

当前 registry 明确：**new D1 model call = false**。

先做：

```text
1. materialize broad r4 raw bank
2. materialize matched ASSOC_ANY bank
3. source-population audit
4. ASSOC/control audit
5. scope/attrition summary
6. 随机 source rows / ASSOC matches / high-attrition strata 人工抽查
7. 检查 Q2 hard-identity stratum 是否天然达到 60 unique subjects/family 的 source feasibility
8. freeze + record new dataset SHA
```

如果第 7 步做不到：

> **drop entity/reference-specific claim。**

不允许：

- 再限定 person-only；
- 只留某一种 alias type；
- 只留某个 direction；
- 只留模型容易认识的 tiny money subset；
- 用 phase-4 mechanism story 救 construct。

---

## 12. 当前 novelty

Mother ACL 2025 的核心是 **exact token contextual entrainment**。

当前项目已可靠扩展出的事实是：

> **entrainment is not strictly confined to exact strings that appeared in context; it can transfer to unseen but learned-related surface forms.**

但 paper-level novelty 还取决于 r4 最终回答哪一个：

### Outcome A — reference-specific survives

如果 hard identity `ALIAS > ASSOC_ANY`：

> surface repetition 之外还存在对 shared referent 特别敏感的 transfer component。

这是最强故事。

### Outcome B — only broad learned relation survives

如果 ALIAS 与 matched ASSOC 差不多：

> mother 的 lexical entrainment 可以沿 learned relations spill over，但没有证据说明 referential identity 是特殊 causal unit。

这仍然可能是一个很有价值的 negative boundary paper，尤其结合 phase 2/3：shared upstream machinery + lexical direct write。

---

## 13. 后续 mechanism 只在 construct 闭合后做

如果 r4 支持 reference-specific component，再问：

```text
A. entity state 在哪一层形成？
B. entrainment heads 是读 entity state，还是只做 lexical amplification？
C. unseen alias transfer 通过哪条 path 落到 target token？
```

如果 r4 不支持 entity-specific，则 mechanism 改成：

```text
learned association 如何通过 shared upstream cause 调制 lexical entrainment？
```

不能继续沿旧“entity salience circuit”叙事硬走。

---

## 14. 当前结论

最短版本：

```text
YES: cross-surface transfer is real.
YES: exact and alias transfer share upstream causal machinery.
YES: entrainment heads' direct write is mainly lexical/seen-form.
NO: current evidence does not establish entity/reference-specific salience.
NEXT: r4 ALIAS vs ASSOC construct validation, data-first.
```

该项目已经过了“现象有没有”的阶段；现在成败只取决于我们能否用**不缩 scope 的 hard association control**回答 reference identity 是否真的特殊。

---

## 15. 2026-08-30 D1 r4 final update

r4 已完成 broad RedirectQA、Wikipedia sentence cooccurrence、`ASSOC_ANY`、同类型 sensitivity、
双方向、双 frame、独立 hard-identity gate，以及 Qwen3-8B、Gemma-3-12B-IT、
Llama-3.1-8B-Instruct 三家族全量运行。

Q1 broad `ALIAS - ASSOC_ANY` 在三家族两个 frame 全部为正，entity-bootstrap CI 全部排除 0；
同类型 ASSOC 与两个方向也全部复现。Q2 gated `opaque_strict` 虽达到 261–282 entities/family，
但三个家族都只有邻近 frame F2 显著，F1 CI 跨 0，违反预注册的 both-frame requirement。
ungated `opaque_strict` 两个 frame 在三家族也全部跨 0；最大效应反而出现在 compositional 与
partial strata。

最终 verdict 是 **CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC**。保留 broad learned-relation
transfer、shared upstream cause 与 lexical/structure gradient；明确放弃“shared referent 是特殊
causal unit”的说法，不进入 reference-specific Phase 4，不按 F2 或某个 alias subtype 收窄。
完整审计、数值、修订时间线和复现命令见 [`D1_R4_REPORT.md`](D1_R4_REPORT.md)。
