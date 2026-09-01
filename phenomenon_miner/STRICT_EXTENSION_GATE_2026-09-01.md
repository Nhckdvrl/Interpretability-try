# Strict Extension Gate — post-5/5 topic search

Date: 2026-09-01  
Status: **MANDATORY OVERLAY FOR NEW TOPICS AFTER THE BASE 5/5 REGISTER**

This file does not weaken or replace `FINDING_RULES.md` v2.1. Every rule there still applies. This overlay only **raises** the acceptance threshold for topics 042+ after the original 5-topic target was reached.

## Why the bar is higher now

The first five surviving topics taught a recurring lesson: in 2024–2026, many natural behaviors are already studied behaviorally, and often older RNN/BERT/ELMo work already owns the corresponding representational object. Once the behavior/object is owned, `newer open model + probe/SAE/activation patching` is not enough for a fresh Main-paper topic.

Therefore the extension search uses a stronger prior:

> **If prior computational work already owns the behavioral scientific object, mechanistic depth alone does not create novelty. The new paper must introduce an orthogonal scientific factorization/object and identify its causal use.**

## E1 — Exact-object novelty remains mandatory

N0/N1/N2 from `FINDING_RULES.md` remain hard. In particular:

- behavior -> mechanism is insufficient when the same object is already owned;
- model-family, language, benchmark, probe, SAE, steering, patching or architecture swaps do not create a new object;
- old RNN/BERT/ELMo ownership counts;
- 2024–2026 paper bodies, appendices and supplementary experiments must be searched, not only titles/abstracts.

## E2 — Two-lock novelty beyond the new object

A candidate must first have a **new orthogonal scientific object/axis**. If the surrounding behavioral family is already occupied, the candidate must additionally satisfy **at least two** of the following three locks before PASS:

### Lock A — orthogonal / role-swap identifiability

There is a natural cross-case, same-surface manipulation, role swap, or equivalent design in which the headline object changes while the strongest obvious lexical/content correlate is held fixed.

Examples of the desired shape:

- same lexical modifier, same scene facts, different live candidate set -> its restricting role changes;
- same adjective, different context/cue -> stage-level vs individual-level reading changes;
- same definite description, uniqueness and familiarity manipulated independently.

If exact same-surface manipulation is impossible for principled reasons, an equally strong factorization plus held-out cue family is required.

### Lock B — cross-setting abstraction

The object must have a preregistered transfer test across at least two of:

- lexical/property family;
- construction/surface realization;
- discourse domain;
- language with an independently motivated realization;
- task/readout that instantiates the same scientific distinction.

A direction that only works on the discovery wording does not count as the object.

### Lock C — two independent theory-diagnostic consequences

At least two downstream signatures must be independently grounded in the scientific theory/object. They may not be two rephrasings of the same grammatical cue.

This is the lesson from 036: one metric that merely correlates with a proposed processing route is not enough to identify the route.

## E3 — Raw-content preservation / specificity denominator

The first causal intervention must include a neighboring capability that should be preserved.

Canonical form:

```text
intervene on X-role / X-source / X-level state
-> change X-sensitive downstream decision
while preserving
raw factual/property/content knowledge needed by both conditions
```

Examples:

- 041: referent narrowing changes while `PropertyTruthLogit` is preserved;
- a definiteness-source topic must preserve candidate-count / antecedent facts while changing how those facts license `the`;
- a predication-level topic must preserve proposition/predicate truth while changing member inheritance.

If the intervention merely deletes the underlying fact, the causal scientific claim fails.

## E4 — Stronger substrate rule

Route C still does **not** require an exact published Llama/Qwen phenotype. However, one of the following must exist before GPU:

1. a real human/scientific manipulation with row-level or reconstructible controlled materials; or
2. deterministic model-independent gold whose factorization is licensed by established theory and contains natural cross-cells.

Synthetic controlled clones are allowed only as a causal microscope after the scientific object is externally fixed.

Central labels may not be created by an LLM judge.

## E5 — Stronger causal registration rule

Before PASS, freeze:

1. object-sensitive primary downstream readout;
2. at least one specificity/preservation denominator;
3. random/shuffled/content-control interventions;
4. held-out transfer family;
5. hard kill if the effect reduces to the strongest superficial correlate.

Decodability alone cannot carry any 042+ topic.

## E6 — Stronger strongest-neighbor test

For every serious 042+ candidate, explicitly search:

```text
human/scientific object
+ old computational/RNN work
+ BERT/ELMo/contextual representations
+ 2024–2026 LLM behavior
+ 2024–2026 internal/causal work
+ methods/appendix hidden factorization
```

If prior work owns the exact object but lacks MI, the candidate is normally dead.

## E7 — Registration checklist for 042+

```yaml
base_FINDING_RULES_v2_1: PASS
new_orthogonal_object_or_axis: PASS
old_neural_object_ownership: CLEAR
recent_LLM_object_ownership: CLEAR
strongest_neighbor_body_search: PASS
external_scientific_substrate_or_deterministic_gold: PASS
central_confound_identifiable: PASS
specificity_denominator_frozen: PASS
held_out_transfer_frozen: PASS
additional_locks_A_B_C_passed: '>=2/3'
story_invariance: PASS
behavior_lottery: false
verdict: STRICT-PASS-REGISTER | CONTINUE-HARD-AUDIT | KILL
```

## 041 second-audit calibration

041 remains above this raised bar only under its narrow frozen claim:

> a same-lexical, context-conditioned **modifier set-restriction role** that transfers beyond particular scenes/properties and causally changes referent narrowing while preserving property truth.

Recent referring-expression work already owns hard-distractor discrimination, minimal necessary descriptors, descriptor-deletion sufficiency, and discriminative reference generation. Therefore none of those behavioral claims are novel for 041. If 041 collapses to `which descriptor is necessary/informative`, it is dead.

## One-line rule

> **After 5/5, a natural behavior is no longer enough when the behavior is already owned: a new topic needs an orthogonal scientific object, hard identifiability, cross-setting abstraction or multiple theory consequences, and causal specificity that preserves the neighboring capability.**
