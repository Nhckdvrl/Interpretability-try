# Next Agent Prompt — 2026-09-01

继续 GitHub 仓库 `Nhckdvrl/Interpretability-try` 的 ACL / EMNLP / NAACL 风格 **LLM mechanistic interpretability 工作**。

这是 direct continuation。**当前 authoritative fresh PASS register 已经是 5/5，目标已完成。不要从旧的 4/5 或更早状态继续，也不要默认继续 count-filling 找题。**

## 一、第一步必须完整读取最新 authority

按顺序读：

1. `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1 唯一选题协议
3. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`
4. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md`
5. `rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`
6. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`
7. `active/034_prospective_memory_retrieval_architecture/README.md`
8. `active/035_shared_dynamic_context_update/README.md`
9. `active/036_metaphor_processing_route_selection/README.md`
10. `active/038_unresolved_reference_representation_architecture/README.md`
11. `active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md`
12. `active/040_numerical_identity_vs_qualitative_sameness/README.md`
13. `active/041_contextual_set_restriction/README.md`
14. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`
15. 本文件

## 二、authoritative state

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
CURRENT_HARD_AUDIT_TOPICS: 1
target: 5
remaining_needed: 0
fresh_search_status: TARGET_REACHED_STOP_BY_DEFAULT
registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction
hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
```

034 / 035 / 038 / 040 are frozen unless a genuinely new fatal collision appears. 036 remains HARD AUDIT / GPU PAUSED and is not needed to make the count.

## 三、040 remains frozen

Question:

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual object or merely two different objects of the same kind?**

Scientific distinction:

```text
numerical identity
!=
qualitative/type sameness
```

Strongest precursor: Davis & Altmann 2021 LSTM/RNN same-token vs different-token-same-type event representation. Therefore 040 dies if it only reproduces `the onion` vs `another onion`.

Required N2:

> abstract, reusable cross-surface numerical-identity state causally controlling token-specific history inheritance, separately from type knowledge.

Frozen first causal contract:

```text
identity intervention
→ changes token-specific HistoryTransferLogit
while preserving shared TypeKnowledgeLogit
```

Architecture comparison (dLLM / Mamba / RWKV) remains secondary only after primary AR evidence.

## 四、041 — fifth PASS

Status: **PASS-REGISTER / GPU AUTHORIZED / Route C**.

Frozen natural question:

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

Frozen object:

> **context-conditioned modifier set restriction / contrastive role** — whether a modifier actually reduces the currently live referent set, separately from ordinary property meaning.

Do not broaden this into generic `restrictive vs nonrestrictive syntax` or shrink it into `informative adjectives help reference`.

### Scientific anchor

Leffel et al. 2014 gives a same-lexical human semantics/neuroscience manipulation where context changes whether the same modifier limits the set under discussion. Their inventory was 53 manually constructed sets, naturalness-normed by 105 respondents and reduced to 46 sets.

### Strongest-neighbor concessions

Already owned and therefore **not** novelty:

- incremental reference resolution as candidate-set elimination;
- neural pragmatic reference and distractor sensitivity;
- adjective redundancy / overmodification;
- relative-clause restrictive/nonrestrictive form/punctuation behavior;
- current LLM/VLM pragmatic referring-expression success/failure.

041 survives only at the following N2 level:

> **abstract context-conditioned modifier role in a pretrained open AR LM, transferable across lexical/domain/surface families and causally controlling which modifier narrows reference while preserving property truth.**

### Decisive same-world role swap

```text
A = large red circle      # target
B = large blue circle
C = small red circle

target phrase = "the large red circle"
```

Keep all object facts and target phrase fixed.

```text
live set {A,B}: red restricts, large does not
live set {A,C}: large restricts, red does not
```

Thus the world facts, target, modifier truth, words, word order and candidate-set cardinality stay fixed; only the current alternatives change.

Gold:

```text
Restricts(m) =
  |Compatible(D_without_m, C)|
  >
  |Compatible(D, C)|
```

### Frozen cheap S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

First reproduce the frozen behavioral role swap with deterministic scoring:

```text
ModifierOmissionCost(m) =
  ReferentMargin(full)
  - ReferentMargin(without m)
```

Same lexical modifier should have high omission cost when it removes the live distractor and low cost when it does not. The identity of the costly modifier must swap with the live candidate set.

No prompt/subset search after null.

### Frozen first causal contract

```text
SetRestrictionRole intervention
→ changes modifier-specific referent narrowing / ReferentMargin
while
preserving PropertyTruthLogit
```

Mandatory controls:

- same-world role swap;
- held-out property/adjective and noun/domain families;
- role-matched / fact-mismatched transfer;
- arbitrary candidate labels and balanced positions;
- modifier order reversal;
- held-out wording of candidate-set introduction;
- raw property-truth and candidate-identity directions;
- shuffled/random controls.

Hard kill if the latent signal is only raw scene facts, candidate identity, salience, lexical position, generic reference competence, or `informative > redundant` behavior.

## 五、036 remains NOT PASS

Status:

```yaml
PASS_REGISTER: false
GPU_AUTHORIZED: false
verdict: HARD_AUDIT
```

The metaphor selector question survives, but the comparison-vs-categorization route metric remains underidentified. Do not repair it just to create a sixth topic.

## 六、final-search deaths now in failure memory

Do not revive:

1. **mass/count grammar vs conceptual individuation** — old neural mass/count syntax-semantics + BERT/contextual coercion already own the object; modern AR + MI is N2-thin.
2. **means vs side-effect / instrumental vs incidental harm** — directly an LLM factor in MoCa/OffTheRails; stronger intentionality-mediation variant lacks a frozen analyzable-open behavior anchor.

Detailed records live in `rejected_candidates/`.

## 七、failure-library discipline remains mandatory

For any future new candidate:

```text
one-sentence object
→ aliases
→ CANONICAL_FAILURE_INDEX
→ rejected_candidates + archive
→ strongest-neighbor BODY / appendix
→ N0/N1/N2
→ substrate
→ confound identifiability
→ causal use
```

Changing model/dataset/language/probe/SAE/steering/patching does not create a new object.

## 八、what to do next

The default task is **no longer fresh topic search**. The target is complete.

Unless the user explicitly asks for more ideas, next work should be one of:

1. execute a frozen cheap S0 for 041 or another registered topic;
2. prioritize the five topics by expected paper value / execution risk / compute cost;
3. write implementation code and preregistration for a chosen PASS;
4. respond to genuinely new fatal novelty evidence;
5. continue fresh search only if the user explicitly asks for >5 topics.

## 九、paper expansion rule

Read `PAPER_EXPANSION_REFERENCE_2026-09-01.md`.

```text
phenomenon
→ abstraction/generalization
→ causal use/specificity
→ mechanism-derived new falsifiable prediction
→ targeted verification
→ optional mitigation/generalization
```

Do not invent later stages before evidence earns them.

For 041, freeze only:

```text
1. same-world modifier-role behavioral double dissociation
2. cross-lexical/domain/surface abstraction
3. causal referent-narrowing specificity while preserving property truth
```

Only after Stage 3 reveals a stable mechanism may it generate a new failure prediction.

## Final discipline

> **Current honest register is 5/5: 034, 035, 038, 040, 041. 041 is contextual modifier set restriction, not generic reference resolution or adjective redundancy. The fresh-search target is complete; move to frozen experimental execution unless explicitly asked to search further.**
