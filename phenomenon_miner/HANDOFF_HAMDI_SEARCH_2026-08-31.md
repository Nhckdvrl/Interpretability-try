# Hamdi-Style Topic Search — Current Handoff

Date: 2026-09-01  
Status: **AUTHORITATIVE CURRENT STATE — FRESH REGISTER 5/5 COMPLETE AFTER 039**

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
fresh_register_target: 5
fresh_register_status: COMPLETE_AFTER_039_REGISTRATION
fresh_target: LLM mechanistic interpretability only
required_protocol: PAPER-SCALE v2.1
registered_projects:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 036_metaphor_processing_route_selection
  - 038_unresolved_reference_representation_architecture
  - 039_same_kind_vs_go_together_semantic_relation
archived_after_registration:
  - 037_generic_generalization_licensing
current_search_style: simplicity-first / Route C legal
current_task: stop count-filling; execute frozen S0/causal contracts and monitor only for fatal collisions
```

## Mandatory reads

Read first:

1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md) — **v2.1 authoritative protocol; strict ≠ complicated**
3. this handoff
4. registered project READMEs:
   - [`034`](../active/034_prospective_memory_retrieval_architecture/README.md)
   - [`035`](../active/035_shared_dynamic_context_update/README.md)
   - [`036`](../active/036_metaphor_processing_route_selection/README.md)
   - [`038`](../active/038_unresolved_reference_representation_architecture/README.md)
   - [`039`](../active/039_same_kind_vs_go_together_semantic_relation/README.md)
5. [`NEXT_AGENT_PROMPT_2026-09-01.md`](NEXT_AGENT_PROMPT_2026-09-01.md)

037 is archived; do not treat a physically stale link or historical note as authorization.

---

## Current register

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> When an agent must remember a future intention while continuing other work, is retrieval supported by strategic monitoring, cue-triggered spontaneous retrieval, or dynamic switching?

No headline edits unless a new fatal collision appears.

### 035 — Shared Dynamic Context Update Across Discourse Phenomena

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> Do anaphora accessibility and presupposition projection reuse a shared dynamically updated local discourse context, or rely on separate/static computations?

No narrowing back to one discourse phenomenon.

### 036 — Metaphor Processing Route Selection

**PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED.**

> What selects comparison vs categorization in metaphor comprehension: conventionality, aptness, or no discrete route switch?

The 2026 hard audit found adjacent metaphor probing/norm work but no direct collision that already factorizes the conventionality×aptness selector with causal open-model evidence. Its question remains naturally explainable without the causal machinery, so v2.1 does not demote it merely for having a detailed frozen contract.

### 038 — Unresolved Reference Representation Architecture

**PASS-REGISTER / GPU AUTHORIZED — v2.1 RE-AUDIT PASSED.**

> When language does not yet identify one unique referent, does the model keep several possibilities alive, leave the reference unresolved, or prematurely pick one?

AmbiCoref + Correct-Detect + It Depends supply matched ambiguity substrate, modern-family behavior, and deterministic candidate metadata. The 2026 hard novelty attack still found no direct activation/patching paper owning parallel-candidate vs underspecified vs premature-commitment representation.

### 039 — Same Kind or Go Together? Taxonomic vs Thematic Semantic Relations

**PASS-REGISTER / GPU AUTHORIZED. Route C.**

> When two concepts are related, does the model distinguish **same kind** from **go together in an event/scenario** as different, causally usable semantic relations?

Why this passed rather than becoming another taxonomy paper:

- the scientific object is independent human cognitive semantics, not an LLM benchmark;
- Landrigan & Mirman provide 659 public word pairs where **every pair has both taxonomic and thematic human ratings** plus `Difference_Score`;
- NAACL 2025 causal property-inference work owns **taxonomy vs categorical similarity**, not thematic relation type;
- NeurIPS 2025 TaxonomiGQA owns taxonomic deployment; its `non-taxonomic` negatives are concepts outside the WordNet hypernym chain, not controlled thematic matches;
- 2026 LLM taxonomic–thematic triad work owns **cross-cultural surrogate fidelity**, not the reusable internal relation-type question;
- no 2025–2026 direct modern-open-LM causal patching/steering work on taxonomic-vs-thematic relation type was found in the hard search.

Frozen first causal test is deliberately simple: learn a relation-type state from neutral pair representations using continuous human ratings, then test whether ± relation steering **bidirectionally changes independent taxonomic-vs-thematic choice** while overall-relatedness, lexical, similarity and co-occurrence controls do not.

Full contract: [`active/039_same_kind_vs_go_together_semantic_relation/README.md`](../active/039_same_kind_vs_go_together_semantic_relation/README.md).

---

## Deregistered 037 — do not revive

Former 037 generic generalization licensing is **KILL-NOVELTY / ARCHIVED**.

Fatal collision: Hu, van Paridon & Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language` (`arXiv:2607.04523`) directly tests the principled-vs-statistical generic-property distinction while controlling prevalence/cue validity. Causal MI would be too close to behavior/factorization -> mechanism under N2.

Archive: [`archive/037_generic_generalization_licensing/`](../archive/037_generic_generalization_licensing/)

---

## v2.1 simplicity rule that must survive execution

The search error before v2.1 was not “too strict”; it was **confusing strictness with pre-writing an elaborate cognitive architecture**.

The legal Route-C flow is:

```text
simple natural object / robust ordinary phenomenon
→ benchmark-removal + normal-scope
→ strongest-neighbor N0/N1/N2
→ auditable existing axis / substrate
→ obvious confounds
→ one minimal causal-use question
→ richer mechanism only if the data earn it
```

Still forbidden:

- behavior lottery on GPU;
- benchmark construct becoming the headline;
- `prior behavior paper -> our activation patching` as the entire N2 delta;
- probe-only paper whose final claim is “feature decodable”;
- changing the scientific object after null results;
- protecting a 5/5 count from fatal evidence.

---

## Serious deaths added in the 039 search round

All were written immediately to `rejected_candidates/`:

- use vs mention / asserted vs quoted — direct object ownership;
- speaker commitment / factivity — direct NAACL 2025 projection-belief object;
- typicality vs frequency/commonness — crowded LM typicality object including 2026 open-model work;
- action precondition vs effect — direct COLING 2025 world-model object;
- hard constraint vs soft preference — direct 2026 LLM-planning object;
- cause vs enabling condition — fine-grained causal NLP already labels Cause/Enable/Prevent;
- epistemic vs deontic modality — BlackboxNLP 2025 directly compares the two modal domains;
- final goal vs subgoal status — synthetic hierarchy / unsurprising-label scale failure.

Immediately preceding simplification-search deaths already in the repo include impossible-vs-improbable, truth-vs-plausibility, once-true-vs-never-true, knowledge stability, memorized-vs-inferred source, trait-vs-state, and function-vs-appearance essentialism.

Do not revive any of these by changing model, benchmark, SAE/probe/patching method, or wording.

---

## Execution priority after register completion

Count-filling search is finished. Recommended next work:

1. **039 S0 first** because it is the cleanest new Route-C object and has cheap deterministic human gold.
2. Then 038 S0 / matched ambiguity causal test.
3. 036 only after confirming its frozen stimulus reconstruction and obvious route-selection behavior.
4. 034/035 remain frozen and can be scheduled according to compute/implementation readiness.

For 039, do not start with SAE hunting. First reproduce the obvious continuous relation axis and independent triad sensitivity; only then do intervention.

## One-line instruction

> **The fresh register is genuinely 5/5 again: keep the questions simple, keep novelty/evidence strict, and move from topic search to frozen execution unless new fatal evidence appears.**
