# Interpretability Topic Search

用于寻找 **ACL / EMNLP / NAACL 风格、自然、清楚、题目幅度正常且可机制化的 LLM scientific questions**。

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
CURRENT_HARD_AUDIT_TOPICS: 1
fresh_register_target: 5
fresh_register_status: TARGET_REACHED
required_protocol: PAPER-SCALE v2.1
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
remaining_needed: 0
```

## Fresh authoritative register

| project | status | one-line question |
|---|---|---|
| [`034_prospective_memory_retrieval_architecture`](active/034_prospective_memory_retrieval_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Future intentions: strategic monitoring, spontaneous cue-triggered retrieval, or dynamic switching? |
| [`035_shared_dynamic_context_update`](active/035_shared_dynamic_context_update/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | Do anaphora and presupposition reuse a shared dynamic local-context update? |
| [`038_unresolved_reference_representation_architecture`](active/038_unresolved_reference_representation_architecture/) | **PASS-REGISTER / GPU AUTHORIZED / HARD RE-AUDIT PASSED** | When reference is still unresolved, does the model keep alternatives, underspecify, or prematurely commit? |
| [`040_numerical_identity_vs_qualitative_sameness`](active/040_numerical_identity_vs_qualitative_sameness/) | **PASS-REGISTER / GPU AUTHORIZED / FROZEN** | If two things are exactly alike, does the model still know whether they are literally the same individual or merely two different things of the same kind? |
| [`041_contextual_set_restriction`](active/041_contextual_set_restriction/) | **PASS-REGISTER / GPU AUTHORIZED** | In the same description, does the model know which modifier is actually narrowing the live referent set and which modifier is merely extra description in the current context? |

**Current honest fresh PASS register: 5/5. Count does not protect any topic from a future fatal collision.**

## 041 — fifth PASS after broad high-mortality search

Frozen object:

> **Context-conditioned modifier set restriction:** whether a modifier actually reduces the currently live set of possible referents, separately from the modifier's ordinary property meaning.

Natural question:

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

Why it survives the final audit:

- restrictive/non-restrictive or contrastive modification is an independent semantics/psycholinguistics object;
- Leffel et al. 2014 provides a same-lexical human manipulation where context changes whether an identical adjective/determiner restricts the live referent set;
- old incremental reference-resolution and neural pragmatic-reference work already owns distractor elimination, informativeness and redundancy behavior, so 041 explicitly **does not** claim those as novelty;
- the N2 delta is an **abstract reusable modifier-role state** in a pretrained autoregressive LLM, cross-lexical/domain and causally used for reference while property truth is preserved;
- the strongest confound is frozen as a hard kill: if the signal is only raw distractor facts, candidate identity, lexical position, salience, or generic reference competence, terminate.

The decisive controlled microscope uses a **same-world three-object role swap**: all world facts, target, target phrase, modifier words and modifier truth stay fixed; only the live candidate set changes, causing which modifier actually rules out the alternative to swap.

First causal specificity contract:

```text
SetRestrictionRole intervention
→ changes modifier-specific referent narrowing / ReferentMargin
while
preserving PropertyTruthLogit
```

See [`active/041_contextual_set_restriction/README.md`](active/041_contextual_set_restriction/README.md).

## 040 — frozen identity object

040 remains **numerical identity vs qualitative/type sameness**, not generic entity tracking. Its first causal contract remains:

```text
identity intervention
→ changes token-specific HistoryTransferLogit
while
preserving shared TypeKnowledgeLogit
```

Davis & Altmann 2021 is a serious RNN precursor. If 040 reduces to `the` vs `another`, generic coreference/binding, or the old event-specific RNN effect, kill it.

## 036 — still not counted

[`036_metaphor_processing_route_selection`](active/036_metaphor_processing_route_selection/) remains:

**HARD AUDIT / CONTINUE-PAPER-SCALE / GPU PAUSED / NOT PASS-REGISTER.**

The selector question (`conventionality vs aptness -> comparison vs categorization`) survives novelty, but the former causal metric was underidentified. It may return only after a clean two-signature route-identification contract is frozen.

## 037 / 039

- 037: **KILL-NOVELTY / ARCHIVED**.
- 039: **KILL-NOVELTY / ARCHIVED** after deeper object-ownership audit. Taxonomic-vs-thematic relation type was already directly studied in language-model representations/behavior; stronger MI alone was not enough.

Canonical lesson:

> **Object ownership, not title ownership.**

## Discovery / dedupe discipline

Before HARD AUDIT, check:

1. [`phenomenon_miner/FINDING_RULES.md`](phenomenon_miner/FINDING_RULES.md) — v2.1 authoritative protocol;
2. [`rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`](rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md) — semantic dedupe memory;
3. `rejected_candidates/` + `archive/` aliases;
4. strongest-neighbor paper bodies, not title wording.

Changing model, dataset, language, probe, SAE, patching or steering does not create a new scientific object.

## How to grow a surviving topic into a Main-paper package

See [`phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`](phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md).

Evidence-based pattern:

```text
phenomenon / natural object
→ broad characterization / clean factorization
→ abstraction or cross-setting transfer
→ causal use / specificity
→ mechanism-derived falsifiable prediction
→ targeted behavioral confirmation
→ optional mitigation / architecture generalization
```

For 041 specifically, freeze only the first three earned stages now:

```text
same-world modifier-role double dissociation
→ cross-lexical/domain/surface abstraction
→ causal referent-narrowing specificity while preserving property truth
```

Only after a stable mechanism is found may it generate a new failure prediction, targeted verification, or mitigation.

## Current authority

1. `phenomenon_miner/FINDING_RULES.md` — sole discovery protocol, v2.1
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — current handoff
3. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md` — audit state
4. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md` — execution flow
5. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md` — post-selection evidence ladder
6. this README — register count and entrypoint

## One-line discipline

> **Simple is good. Trivial is not. Method-only novelty is not. The fresh target is now honestly 5/5: 034, 035, 038, 040, 041. Future work should execute frozen S0/causal contracts or react only to genuinely new fatal novelty evidence, not reopen count-filling search by default.**
