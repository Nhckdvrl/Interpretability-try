# Hamdi-Style Topic Search — Current Handoff

Date: 2026-09-01  
Status: **AUTHORITATIVE CURRENT STATE — FRESH REGISTER 5/5, SIMPLICITY RE-AUDIT ACTIVE**

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
fresh_register_target: 5
fresh_register_status: COMPLETE
fresh_target: LLM mechanistic interpretability only
required_protocol: PAPER-SCALE v2.1
registered_projects:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 036_metaphor_processing_route_selection
  - 037_generic_generalization_licensing
  - 038_unresolved_reference_representation_architecture
current_search_style: simplicity-first / Route C allowed
current_task: re-audit 036-038 under v2.1 and replace any weak/over-engineered topic rather than protecting count
```

## Mandatory reads

Read first:

1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md) — **v2.1 authoritative protocol; strict ≠ complicated**
3. this handoff
4. all five registered project READMEs under `active/034_*`–`active/038_*`
5. [`NEXT_AGENT_PROMPT_2026-09-01.md`](NEXT_AGENT_PROMPT_2026-09-01.md)

Only inspect old `rejected_candidates/` / `archive/` when semantic overlap requires it.

---

## Current register

### 034 — Prospective Memory Retrieval Architecture

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> When an agent must remember a future intention while continuing other work, is retrieval supported by strategic monitoring, cue-triggered spontaneous retrieval, or dynamic switching?

Keep frozen unless fatal novelty collision appears.

### 035 — Shared Dynamic Context Update Across Discourse Phenomena

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

> Do anaphora accessibility and presupposition projection reuse a shared dynamically updated local discourse context, or rely on separate/static computations?

Keep frozen unless fatal novelty collision appears.

### 036 — Metaphor Processing Route Selection

**PASS-REGISTER / GPU AUTHORIZED, UNDER v2.1 SIMPLICITY RE-AUDIT.**

> What selects comparison vs categorization in metaphor comprehension: conventionality, aptness, or no discrete route switch?

Why it was registered: classic Career-of-Metaphor vs aptness debate; human 2×2 stimuli orthogonalize conventionality and aptness; recent modern open LLM metaphor/norm evidence; no direct causal LLM adjudication found.

Re-audit question: is this still a naturally explainable paper-level question under v2.1, or did the frozen causal machinery make it look stronger than the actual object? Do not demote merely because the experiment contract is elaborate; demote only for scale/novelty/substrate weakness.

### 037 — Generic Generalization Licensing

**PASS-REGISTER / GPU AUTHORIZED, UNDER v2.1 SIMPLICITY RE-AUDIT.**

> Why do some properties support statements like `Birds lay eggs` or `Mosquitoes carry malaria` despite many exceptions: prevalence, probabilistic diagnosticity, or a principled conceptual/causal relation?

Why it was registered: mature generics theory, published human prevalence/cue-validity/conceptual manipulations, modern open-family generic behavior, no direct causal LLM adjudication found.

Re-audit question: can the headline be stated simply enough that the theory serves the natural phenomenon rather than vice versa?

### 038 — Unresolved Reference Representation Architecture

**PASS-REGISTER / GPU AUTHORIZED, UNDER v2.1 SIMPLICITY RE-AUDIT.**

> When language does not yet identify one unique referent, does the model keep several possibilities alive, leave the reference unresolved, or prematurely pick one?

Key substrate improvement that justified registration:

- AmbiCoref supplies human-validated ambiguous/unambiguous minimal pairs with the same participants/pronoun/skeleton;
- Correct-Detect establishes the Llama-3.1 phenotype;
- It Depends independently supplies Qwen3/Llama/DeepSeek persistent-ambiguity behavior and deterministic candidate-set metadata;
- central scoring does not require an API judge.

This is currently the most obviously v2.1-compatible of 036–038: the ordinary-language question is simple even though the causal contract is detailed.

---

## 2026-09-01 protocol correction — simplicity prior

The search had become over-engineered after correctly learning the 031/F8 lesson. `FINDING_RULES.md` v2.1 now preserves strict novelty/evidence gates while explicitly allowing **Route C: simple phenomenon / simple latent object first**.

Universal strict core remains:

```text
natural one-sentence question / phenomenon
+ explainable without AI/MI jargon
+ benchmark-removal
+ normal paper scope
+ venue-scale comparison
+ N0/N1/N2
+ exact/auditable substrate
+ analyzable open checkpoint
+ established phenomenon/axis
+ story-invariant headline
+ minimal falsifiable causal-use contract
+ confound controls / hard kills
```

No longer universal hard requirements:

- three mature mechanisms for every topic;
- exact mathematical first interaction statistic for every topic;
- two perfectly matched published modern families for every topic.

Route B still needs theory-level competing mechanisms. Route C can discover mechanism structure during execution as long as the scientific object does not change.

---

## What the Hamdi-style calibration teaches

Do **not** copy another researcher's unpublished object. Copy the search shape:

1. start from a strong established object / everyday model behavior;
2. identify one simple orthogonal property or surprising regularity;
3. design matched controls against the obvious confound;
4. ask whether the model carries and causally uses that property;
5. let richer mechanism structure emerge later.

The target shape is closer to:

> `Can the model distinguish X from Y even when obvious correlate Z is matched?`

or

> `Why does a stable everyday bias appear across otherwise different choices?`

than to an over-written three-stage architecture question.

External research-taste calibration also supports this top-down/model-biology style: start from interesting high-level model facts, use the simplest decisive experiment, then descend into mechanism.

---

## Recent serious deaths

All serious deaths belong in `rejected_candidates/` immediately. Recent frozen deaths include good-enough processing, agreement/similarity attraction, proactive interference locus, negation architecture, linguistic convergence mechanism split, regular polysemy shared structure, implicit-causality production/comprehension sharing, analogy relational-transfer mechanism, morphology rule-vs-analogy, sound-symbolism mechanism, thematic-fit event-schema mechanism, verbatim-vs-gist native traces, shared frame state, and literal-vs-pragmatic enrichment.

Do not revive these by changing model/dataset/language/probe/SAE/patching method.

---

## Current task

The register currently reads 5/5, but **count is not protected**.

1. Re-audit 036/037/038 under v2.1 simplicity + actual ACL/EMNLP paper standards.
2. In parallel, continue a fresh simplicity-first search for stronger replacements.
3. If a registered topic has a fatal scale/novelty/substrate problem, demote it and write a rejection/archive record even though this reopens the register.
4. If all five survive, stop adding topics merely for count and move toward frozen experiment execution.

## One-line instruction

> **Keep novelty and evidence strict, keep questions simple. The register is currently 5/5, but replace any topic that only looks strong because its mechanism contract is complicated.**
