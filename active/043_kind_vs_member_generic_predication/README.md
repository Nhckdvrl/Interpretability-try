# 043 — Is the Property About the Kind, or About Its Members? Generic Predication Level in LLMs

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED WITH LEXICAL-CONFOUND HARD KILL**  
Date: 2026-09-01  
Route: **A/C — classic semantic distinction inside an already-studied generic family**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When a model reads a generic statement, does it know whether the property belongs to the kind itself, or is instead a generalization about individual members of that kind?**

Classic contrast:

```text
Dinosaurs are extinct.   # property of the kind dinosaur
Tigers are striped.      # generalization about individual tigers
```

Formal-semantics terminology:

- **direct kind predication / D-generic** — a predicate is applied to the kind as an entity;
- **characterizing generic / I-generic** — the statement characterizes members/instances of the kind.

No individual dinosaur is itself `extinct` in the relevant sense; extinction is a property of the dinosaur kind. By contrast, individual tigers can be striped.

The scientific object is **predication level**, not generic-vs-specific language and not quantifier strength.

---

## B. Why this is independently real

The distinction is standard in formal semantic work on generics and kinds. Carlson/Krifka-style theories explicitly separate direct kind predication from characterizing generics. Reference works such as the Cambridge Handbook of Formal Semantics and the Stanford Encyclopedia of Philosophy use exactly this contrast.

The distinction also has independent grammatical consequences:

1. **member/exemplar inheritance** differs: a characterizing property can normally be instantiated by members, while a pure kind property such as extinction cannot be inherited by an arbitrary member;
2. **indefinite-singular realization** differs: characterizing generics can have forms such as `A tiger has stripes`, whereas direct kind predication normally cannot be rendered as `A dinosaur is extinct` on the relevant reading;
3. **overt Q-adverb interaction** differs for clear kind predicates such as `extinct` versus characterizing predicates. Current formal work continues to use this diagnostic.

Thus the object exists independently of any LLM dataset.

---

## C. The surrounding LLM space is crowded

043 passes only because its claim is narrower than existing genericity work.

### C1 — Computational Linguistics 2024 — exceptions, instantiations and inheritance

Allaway et al. study ~17k generics and ~370k generated exemplars, explicitly testing exceptions, instantiations, overgeneralization and property inheritance in LLMs.

**Occupies:**

- generic reasoning;
- exemplar generation;
- property inheritance from generics;
- overgeneralization / exceptions.

Therefore 043 may not claim novelty as `LLMs overgeneralize generics` or `do LLMs inherit generic properties to examples?`.

### C2 — Findings ACL 2026 — generics vs quantification

`Generics are not quantificational` compares thousands of generics with quantificational counterparts using LM probabilities and uses the results in a semantic-theory argument.

**Occupies:** generic-vs-quantifier semantic organization in LMs.

043 is not allowed to become a generic-vs-most/all paper.

### C3 — LREC-COLING / ABRICOT 2024 — abstractness and inclusiveness

Recent genericity annotation work decomposes noun-phrase genericity into continuous abstractness and inclusiveness. ABRICOT even keeps the same noun phrase while context changes these dimensions and asks language models to recover them.

This is a major N2 warning because `kind-like / abstract NP representation` is not itself new.

**Does not own:** direct-kind predication versus member-level characterizing predication when **both sides remain generic**, with predication-level causal consequences.

### C4 — exact surviving N2

The only acceptable 043 claim is:

> **Modern LLMs maintain an abstract predication-level state that distinguishes a true generic property of the kind itself from a characterizing property inherited by members, and causally use that state to control member inheritance and independent generic-form diagnostics while preserving the truth/content of the generic proposition.**

If the result becomes `generic abstractness`, `inheritance behavior`, or `kind predicate vocabulary`, kill it.

---

## D. Strict Extension Gate

### Lock A — orthogonal identifiability: PARTIAL, strengthened by anti-lexical controls

The central danger is severe: lexical predicates such as `extinct`, `widespread`, `common`, `rare` can themselves reveal kind-level selection.

Therefore 043 cannot pass by training a classifier on `extinct` vs `striped`.

Required design:

1. hold noun kind/domain balanced;
2. use multiple semantically distinct direct-kind predicate families;
3. use multiple characterizing predicate families;
4. leave entire predicate families out of discovery;
5. use constructional diagnostics where the **same proposition type** is tested through alternative generic forms;
6. explicitly compare against predicate-selectional-semantic directions.

Lock A is considered satisfied only because the first causal claim is not defined from lexical classification and the project also requires Locks B+C. Failure of held-out predicate-family transfer is an immediate hard kill.

### Lock B — cross-setting abstraction: PASS

Mandatory transfer across:

- predicate family;
- noun/kind domain;
- bare plural vs generic definite / alternative generic forms where licensed;
- at least one held-out language/constructional realization if a clean resource is available.

### Lock C — two independent theory-diagnostic consequences: PASS

At least two independent diagnostics are frozen:

1. **MemberInheritance** — whether the generic property is licensed to transfer to a member/exemplar;
2. **GenericForm/Q-adverb diagnostic** — compatibility with an individual-denoting indefinite singular and/or overt quantificational-adverb realization, chosen from theory-grounded held-out materials.

A latent state is not called `PredicationLevel` unless it causally affects both diagnostics in the theory-predicted direction.

---

## E. Substrate

### E1 — formal-theory anchor

Start from independently classified examples in formal genericity literature: clear direct kind predicates and clear characterizing generics.

The labels come from semantic diagnostics, not from model outputs.

### E2 — large generic window

Existing generic datasets (including the CL 2024 generic inventory) provide nouns/properties and member exemplars. They can be filtered only by a **preregistered external predication-level criterion**; model behavior may not define the classes.

### E3 — controlled causal microscope

For each held-out generic proposition, construct deterministic questions/continuations that test:

```text
GenericTruthLogit
MemberInheritanceLogit
IndefiniteSingularCompatibility
QAdverbCompatibility
```

Human/theory-defined predication level is central gold. No API judge.

---

## F. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### S0-1 — proposition comprehension

Require the model to know the base proposition well enough that the generic truth/readout is meaningful. Exclude only items using a prespecified fact-knowledge rule, never by selecting desired inheritance effects.

### S0-2 — behavioral predication double dissociation

For clear theory-grounded items:

```text
characterizing generic:
  GenericTruth high
  MemberInheritance relatively licensed

pure direct-kind predication:
  GenericTruth high
  MemberInheritance not licensed in the same way
```

This separates `sentence is true` from `property belongs to arbitrary member`.

### S0-3 — second diagnostic

The same item classes must show the expected distinction on an independently motivated constructional diagnostic (indefinite-singular and/or Q-adverb compatibility) without selecting the diagnostic after seeing model activations.

### S0-4 — lexical shortcut controls

- held-out direct-kind predicate families;
- held-out characterizing predicate families;
- nonce or paraphrased property descriptions only when truth can be deterministically specified from context;
- matched frequency/length;
- predicate-only baselines;
- noun-only baselines.

If predicate-only classification explains the entire effect and no held-out family transfer exists, terminate.

---

## G. Frozen causal-use contract

### G1 — estimate `PredicationLevel`

Estimate a low-dimensional state from training families with noun/domain/predicate balancing. No best-layer selection on final tests.

### G2 — primary consequence: member inheritance

On held-out true generic propositions:

```text
steer toward MEMBER-CHARACTERIZING
→ increase MemberInheritanceLogit

steer toward DIRECT-KIND
→ reduce inappropriate member inheritance
```

while preserving:

```text
GenericTruthLogit
PredicateContentLogit
```

If the edit simply makes `extinct` or `striped` less semantically available, the claim fails.

### G3 — independent consequence

The same direction/subspace must causally affect a prespecified second diagnostic:

- indefinite-singular generic compatibility; and/or
- Q-adverb compatibility.

It must generalize to held-out predicates and nouns.

### G4 — controls

- direct predicate lexical-semantic direction;
- generic-vs-episodic direction;
- abstractness/inclusiveness controls inspired by LREC/ABRICOT;
- random/shuffled labels/subspaces;
- frequency/length matched donors.

The headline result is a cross-diagnostic causal state, not a high probe score.

---

## H. Story invariance

### Result A — reusable predication-level state

The model represents whether a generic property applies to the kind or characterizes members and uses the distinction to regulate inheritance and generic-form behavior.

### Result B — correct behavior without abstract state

The model handles many items but the signal is predicate-family local; generic reasoning is implemented through lexical/selectional knowledge rather than a reusable predication-level object.

### Result C — inheritance collapse

The model treats direct-kind and characterizing generics through the same member-level generalization machinery, helping explain systematic overinheritance from kind-level truths.

All outcomes retain the same object.

---

## I. Fatal kills

1. New direct neural/LLM work already factorizes D-generics vs I-generics internally and causally -> `KILL-NOVELTY`.
2. Predicate vocabulary alone carries the result -> `KILL-LEXICAL-CONFOUND`.
3. No held-out predicate-family transfer -> no abstract predication-level claim.
4. Only member inheritance is measured -> `KILL-N2` relative to CL 2024.
5. Only generic-vs-quantifier behavior is measured -> `KILL-N2` relative to Findings ACL 2026.
6. Only NP abstractness/inclusiveness is decoded -> `KILL-N2` relative to LREC/ABRICOT.
7. Intervention changes generic truth/content as much as predication consequences -> `KILL-SPECIFICITY`.
8. The two independent diagnostics cannot be jointly explained by the same causal state -> terminate the unified object claim rather than choosing one successful metric.

---

## J. Venue-scale comparison

- **CL 2024 generic reasoning:** establishes a broad behavior family and inheritance failures; 043 asks an orthogonal semantic factorization that predicts when inheritance is licensed at all.
- **EMNLP 2025 Outstanding filler-gap:** the object must transfer across constructions and causal consequences rather than exist only as decodable class labels.
- **ACL 2026 Tool Irrelevance:** semantic factors are dissociated and intervention specificity is required.
- **ACL 2025 Llama See, Llama Do:** a simple object earns paper scale through broad characterization, causal specificity and consequences—not through a complicated title.

---

## K. Strict registration verdict

```yaml
base_FINDING_RULES_v2_1: PASS
new_orthogonal_object_or_axis: PASS_PREDICATION_LEVEL
old_neural_exact_object_ownership: CLEAR_IN_SEARCH
recent_LLM_surrounding_family: HEAVILY_OCCUPIED
N2: PASS_ONLY_FOR_NARROW_CROSS_DIAGNOSTIC_OBJECT
external_formal_semantic_anchor: PASS
Lock_A_role_swap_or_equivalent: PASS_WITH_LEXICAL_HARD_KILL
Lock_B_cross_setting_abstraction: PASS
Lock_C_two_independent_consequences: PASS
specificity_denominators:
  - GenericTruthLogit
  - PredicateContentLogit
central_confound: PREDICATE_LEXICAL_SELECTION
central_confound_identifiable: PASS_WITH_HARD_KILL
behavior_lottery: false
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **043 is not a generic-reasoning paper. It asks whether LLMs causally distinguish a property of the kind itself from a member-level generic property. The same state must generalize across predicate families and control at least two independent semantic consequences while preserving the base generic proposition; otherwise the topic dies.**
