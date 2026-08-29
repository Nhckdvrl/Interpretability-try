# 现象发现、审计、验证与机制流程

版本：2026-08-29  
状态：`FROZEN v4 — novelty 与 data feasibility 全部前置到 discovery`

## 核心原则

**一个题目被正式注册之前，就应该已经知道：它为什么新、最强邻居是谁、数据从哪里来、license/gold 是否成立、预计有多少独立样本，以及如果没有现成 paired data 应如何从公开自然 source 稳定构造。**

`active/` 不是继续找论文、找数据或修选题的地方。那些工作属于 `candidate_pool/` 的 discovery 阶段。

## 唯一合法流水线

```text
mother question / natural phenomenon
→ candidate card + decisive contrast + competing mechanisms
→ N0 breadth audit
→ N1 depth audit
→ D0 source-feasibility audit
→ DISCOVERY-PASS
→ formal project registration
→ materialize/freeze the already-selected D0
→ READY-TO-SMOKE
→ two-family behavioral smoke
→ raw-case / scorer / capability / artifact audit
→ cross-family / cross-size / strong-model generality
→ mechanism prerequisites
→ white-box mechanism
→ mechanism-derived method
```

**没有 post-smoke routine N1，也没有 post-registration data search。**

---

## 1. Discovery package：注册之前一次做透

### N0 — breadth novelty audit

N0 是候选生成阶段的广度筛查，目的是快速杀掉明显撞车、换皮和 mother-inclusion：

- exact / near-exact LLM phenotype；
- decisive contrast / wrong destination；
- mother phenomenon + LLM；
- 同义词、旧术语与邻近 benchmark；
- 2024–2026 ACL/EMNLP/NAACL/ICLR/ICML/NeurIPS/arXiv/OpenReview；
- repo 内已经死亡的 family / rename。

N0 的结果是 `PASS / HOLD / KILLED-COLLISION`。通过 N0 只代表值得继续做深审，不代表可注册。

### N1 — depth novelty closure

N1 **也属于选题阶段**。它不是等 smoke 出结果后再查一次，而是在决定“这个题值得成为项目”前把最危险的 collision 做透。

至少完成：

1. 最近 3–5 篇最强邻居全文，而非只看标题/摘要；
2. appendix / limitations / supplementary / public code / released prompts；
3. citation chain：关键 predecessor、successor、同作者后续版本；
4. mother-paper inclusion：新问题是否已经在正文或 appendix 顺手回答；
5. decisive-contrast inclusion：别人是否已做同一 factorial / intervention；
6. mechanism occupancy：若行为已知，是否连核心 causal explanation 也已占位；
7. scale survival evidence：邻近现象是否在更强模型上已经自然消失；
8. 明确写出 `why_not_a_rename` 和最强 kill condition。

N1 通过后，novelty package 视为 **closed for registration**。之后不因为“已经跑了模型”而形式性地再做一遍。

### D0 source-feasibility — 数据也必须在选题阶段做实

在正式注册之前，必须提交一个**可执行的数据路径**，不能只写“之后找某个公开数据集”。至少包括：

- exact source / dataset / corpus / benchmark 名称与版本；
- URL/DOI/repository 或稳定获取路径；
- license / redistribution / adaptation 条件；
- natural statistical unit 是什么；
- gold 来自哪里，如何程序化验证；
- 目标 manipulation/contrast 如何从 source 得到；
- 预计 eligible 独立样本数，且说明估计方法；
- 至少 20 个真实 source examples / candidate pairs 的人工 feasibility audit；
- nuisance/confound 列表；
- 若需构造数据：完整 deterministic construction recipe、seed、过滤规则、gold proof 与 external natural anchor。

### 没有现成 paired data 时

允许“构造”，但必须在 discovery 阶段证明构造方法真实可执行，而不是注册以后再发明：

```text
public natural source
→ deterministic / programmatic transformation
→ independently provable gold relation
→ dry-run confirms enough eligible units
→ sampled naturalness/artifact audit
```

纯 synthetic toy prompt bank 不能单独承担 paper-level naturalness / generality。若 central D0 需要构造，至少要有公开自然 source 和独立 external validation anchor。

如果候选阶段仍无法回答“数据到底从哪里来、能拿到多少、gold 怎么来、license 是否允许”，则状态只能是 `HOLD-DISCOVERY-DATA`，**不得先注册 active project**。

---

## 2. DISCOVERY-PASS 才允许 formal registration

新项目的注册最低条件：

```yaml
n0_breadth_verdict: PASS
n1_depth_verdict: PASS
d0_source_feasibility_verdict: PASS
strongest_neighbor_checked: true
full_text_and_appendix_checked: true
exact_data_source_locked: true
license_resolved: true
gold_path_resolved: true
eligible_count_estimated: true
sample_feasibility_audit: PASS
```

只有这一步以后才创建/晋级正式 project contract。

注册以后，禁止把“再找一个更合适的数据集”“再换一个 operationalization”“再补一个 novelty story”当作普通开发步骤。若必须换 source、换核心 contrast、换 mother question，项目退回 discovery 并重新审计受影响部分。

---

## 3. D0 freeze：后置只剩机械冻结，不再找数据

正式注册后的 D0 工作只允许：

- 按 discovery 阶段已经锁定的 source/version/recipe materialize；
- 记录 exact IDs / rows；
- byte/hash freeze；
- 校验 gold、independence、split、provenance；
- 验证 discovery 阶段抽查的 source examples 在最终 materialization 中仍成立；
- 若 transformation 有变化，再补相应人工 audit。

如果 materialization 发现 source 数量不够、license 不可用、gold 不稳定或必须更换构造逻辑，**不是“继续 D0 找数据”**，而是退回 candidate pool 的 discovery audit。

---

## 4. Behavior → generality → mechanism

READY-TO-SMOKE 后先跑便宜的两个独立家族；随后做 raw-case/scorer/capability/artifact audit。

smoke 通过后直接进入：

```text
cross-family / cross-size confirmation
→ strong-model kill test
→ mechanism prerequisites
```

不再设置一个常规的 post-smoke novelty gate。文献审计已经是题目成立的前置工作。

### 什么时候才重开 novelty？

只允许三类触发：

1. 项目核心 claim / decisive contrast / mechanism question 被实质改写；
2. 审计后出现一篇具体的新论文，明显可能形成 collision；
3. reviewer / collaborator 指出一个此前漏掉的具体 strongest neighbor。

这叫 **novelty refresh**，不是流程上的 N1。

---

## 5. 状态机

```text
IDEA
→ DISCOVERY-AUDITING
   ├─ N0-BREADTH
   ├─ N1-DEPTH
   └─ D0-SOURCE-FEASIBILITY
→ DISCOVERY-PASS
→ REGISTERED
→ D0-FREEZE
→ READY-TO-SMOKE
→ BEHAVIOR-VERIFIED
→ GENERALITY-CHECK
→ MECHANISM-READY
→ ADVANCE

任何 discovery 子门失败 → HOLD / KILLED（仍留 candidate_pool）
任何正式项目 terminal failure → archive
```

## 6. Legacy projects

v4 不要求对已经存在的项目机械补做一次重复 N1。已有项目保留其历史审计决议；只有核心 claim 改变或出现具体新 collision 时才 refresh。

同理，legacy `HOLD-D0` 项目不作为新流程的模板。**新项目若连 source feasibility 都未解决，不得进入 active。**

权威模型调用状态仍只看 [`candidate_pool/AUDIT_REGISTRY.md`](candidate_pool/AUDIT_REGISTRY.md)。
