# Next Agent Prompt — 2026-09-01

继续 GitHub 仓库 `Nhckdvrl/Interpretability-try` 的 ACL / EMNLP / NAACL 风格 **LLM mechanistic interpretability 找题与 hard-audit 工作**。

这是 fresh topic search 的直接 continuation。**当前 authoritative register 是 4/5，不是旧 prompt 的 2/5，也不是短暂出现过的 5/5。** Former 039 已在更深 N2 audit 中被撤销。

## 第一步：先读当前 authority

必须先完整读取：

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1 唯一选题协议
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — 当前 authoritative handoff
4. `active/034_prospective_memory_retrieval_architecture/README.md`
5. `active/035_shared_dynamic_context_update/README.md`
6. `active/036_metaphor_processing_route_selection/README.md`
7. `active/038_unresolved_reference_representation_architecture/README.md`
8. `rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`
9. 本文件

只在语义重合或新 fatal evidence 出现时定向查其他 `rejected_candidates/` / `archive/`。

## 当前 authoritative register

```yaml
CURRENT_FRESH_PASS_REGISTER: 4
CURRENT_FRESH_ACTIVE_TOPICS: 4
target: 5
status: OPEN_AFTER_039_DEREGISTRATION
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 036_metaphor_processing_route_selection
  - 038_unresolved_reference_representation_architecture
archived:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
remaining_needed: 1
```

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> 当 agent 一边继续当前任务、一边要记住未来意图时，它依靠持续 strategic monitoring、cue-triggered spontaneous retrieval，还是动态切换？

不要修改 headline，除非发现新 fatal novelty collision。

### 035 — Shared Dynamic Context Update

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> anaphora accessibility 与 presupposition projection 是否复用一个动态更新的 local discourse context，还是各有独立/static computation？

不要缩回单独 anaphora / presupposition mechanism。

### 036 — Metaphor Processing Route Selection

**PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE.**

> metaphor comprehension 中 comparison vs categorization 的 route 由 conventionality、aptness，还是没有离散 route switch 来决定？

必须重新用 039 级别的标准搜：

- Career-of-Metaphor + LLM / transformer / causal / representation；
- conventionality × aptness + LLM；
- comparison vs categorization metaphor processing in LLMs；
- modern open-model metaphor probing 是否已经把 novelty/conventionality 解释为 route switch；
- 不只看标题，要读实验与 discussion 是否拥有同一 scientific interpretation。

### 038 — Unresolved Reference Representation

**PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT ACTIVE.**

> 指代还无法唯一确定时，模型是同时保留多个候选、保持 underspecified，还是过早 commit？

必须重新搜：

- unresolved reference / pronoun ambiguity + LLM hidden states / activation / causal;
- simultaneous candidate activation / multiple antecedents in transformers;
- semantic underspecification + LLM representations;
- coreference uncertainty / ambiguity detection internals;
- early commitment / reanalysis in LLM reference resolution；
- 2025–2026 papers that may own the object even under a different headline.

## 037 — 已撤销，禁止复活

Former `037_generic_generalization_licensing` is **KILL-NOVELTY / ARCHIVED** due to the direct 2026 principled-vs-statistical generic-property collision.

## 039 — 已撤销，禁止用 MI 方法升级复活

Former 039 asked whether LLMs distinguish **taxonomic similarity / same kind** from **thematic relatedness / go together** as a reusable causal relation state.

It is **KILL-NOVELTY / ARCHIVED / GPU NOT AUTHORIZED**.

The deeper audit found:

1. 2026 `Disentangling Similarity and Relatedness in Topic Models` explicitly studies taxonomic similarity vs thematic relatedness with the same 659-pair TxThmNorms data, language-model embeddings, and modern LLM two-axis judgments including Qwen;
2. CoNLL 2025 `Human-likeness of LLMs in the Mental Lexicon` studies Llama semantic-relatedness representations encompassing taxonomic/thematic relations;
3. 2026 cross-cultural-surrogate work directly tests LLaMA/Qwen taxonomic–thematic forced choice and explicitly analyzes taxonomic vs thematic reasoning in explanations.

Thus `hidden direction + steering + causal transfer` would mostly be stronger MI on an already-owned object and fails N2.

Detailed record: `rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`.

### 039 lesson — mandatory for every future Route C candidate

Do not ask only:

> `Has anyone done activation patching on this exact axis?`

Ask:

> **`Has prior work already treated this exact natural distinction as a model property, representation, behavior, reasoning mode, or explanatory axis—even if its headline is about something else?`**

If yes, stronger MI alone normally does not save novelty.

## v2.1 最重要纪律

Route C 合法：

```text
simple natural object / surprising phenomenon
→ benchmark-removal
→ N0/N1/N2
→ exact auditable substrate
→ obvious confounds
→ minimal causal-use question
→ mechanism 在执行中长出来
```

仍然绝对禁止：

- GPU lottery 决定现象是否存在再改题；
- behavior/representation paper -> patching/SAE 而没有新 object；
- probe-only / best-layer paper；
- null 后换 headline；
- 为了显得学术把简单题包装成多阶段 architecture；
- 为保护 register 数量忽略 fatal collision。

## 当前工作顺序

严格按：

```text
1. hard re-audit 036
2. hard re-audit 038
3. 对 034/035 做 lightweight fatal-collision-only scan
4. 得到真正 clean 的 surviving count
5. 再 broad-search 一个 replacement
6. serious death 立即写 rejection record
7. 只有完整 N0/N1/N2 + substrate + causal-use contract 后才允许新 PASS
```

不要因为 `remaining_needed: 1` 就只生成一个候选。仍应准备 10+ simple candidates，让 novelty gate 杀掉绝大多数。

## 当前 recent serious deaths

包括：

- use vs mention / asserted vs quoted;
- speaker commitment / factivity;
- typicality vs frequency/commonness;
- action precondition vs effect;
- hard constraint vs soft preference;
- cause vs enabling condition;
- epistemic vs deontic modality;
- final goal vs subgoal status;
- concrete vs abstract representation;
- causal vs correlational relation;
- intentional lie vs honest error;
- taxonomic vs thematic relation type (former 039).

Do not revive by changing model/dataset/language/probe/SAE/patching method.

## 最终一句执行指令

> **当前是 4/5。先把 036/038 像 039 一样按“object ownership 而非标题 ownership”狠狠干一遍，再找 replacement。宁可保持 4/5，也不要再草率制造一个假 PASS。**
