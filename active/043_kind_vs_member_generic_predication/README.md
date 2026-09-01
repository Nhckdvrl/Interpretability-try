# 043 — Kind-Level vs Member-Level Generic Predication

Status: **STRICT HARD AUDIT / GPU PAUSED / NOT REGISTERED**  
Date: 2026-09-01  
Route under audit: A/B/C hybrid  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## Frozen natural question

> **When a model reads a generic statement, does it treat the property as predicated directly of the kind, or as a generalization involving members of that kind?**

Canonical examples:

```text
Dinosaurs are extinct.   # clear direct kind predication
Tigers are striped.      # canonical characterizing generic
```

This is a real and important formal-semantic distinction. The project is **not** rejected as scientifically meaningless. It is paused because the stronger post-5/5 gate exposed unresolved theory-gold and substrate problems that make immediate GPU authorization unjustified.

## Why the former STRICT-PASS was too optimistic

### 1. The surrounding LLM object family is already heavily occupied

Existing work already owns:

- generic exceptions, instantiations, and property inheritance in LLMs;
- generic-vs-quantificational organization;
- abstractness/inclusiveness dimensions of generic noun phrases;
- statistical-vs-principled licensing of generic generalizations (former 037 fatal collision).

Therefore 043 cannot survive as `generic reasoning + stronger MI`, `member inheritance mechanism`, or `kind-like representation`.

### 2. Direct-kind vs characterizing is not a universally theory-neutral gold partition

The traditional Carlson/Krifka analysis distinguishes direct kind predication from characterizing generics, and clear cases such as `Dinosaurs are extinct` remain useful. But contemporary formal work includes analyses on which characterizing generics themselves involve kind reference / kind predication. Thus the broad headline `property belongs to kind vs members` is not a simple observational label in the same sense as 040 numerical identity.

A valid project must therefore either:

1. restrict itself to **consensus-clear operational cases** where independent diagnostics converge; or
2. become an explicit Route-B theory-adjudication paper with competing semantic analyses and discriminating predictions.

It may not silently treat one formal analysis as ground truth.

### 3. A real experimental substrate exists, but the exact causal object is not yet sufficiently auditable

Ionin, Montrul & Santos (2011) experimentally distinguish two sources of genericity: characterizing/sentence-level genericity and kind reference. Lazaridou-Chatzigoga & Alexiadou extend the exact design to Greek with 20 test items and context-based acceptability judgments.

This is useful external evidence, but the test materials are optimized for determiner/kind-reference distribution, not for a large model-independent internal `PredicationLevel` label inventory. The strongest direct-kind examples also remain highly lexically diagnostic (`extinct`, `widespread`, `common`, `rare`).

Under the strict extension gate, `we can create a classifier and hold out some predicates` is not enough to declare the central confound solved.

## What remains genuinely promising

A resurrected 043 could ask whether one causal state jointly predicts **multiple independent consequences** of clear predication-level cases while transferring beyond lexical predicate families.

Candidate independent diagnostics already justified by formal semantics include:

1. **MemberInheritance** — whether a property is licensed to an arbitrary member/exemplar;
2. **IndefiniteSingularCompatibility** — characterizing generics can often be realized with an individual-denoting indefinite singular, while clear direct-kind predications cannot on the relevant reading.

The second diagnostic is now frozen to `IndefiniteSingularCompatibility`; no post-hoc switch to whichever Q-adverb or construction happens to work is allowed.

## Strict locks after re-audit

```yaml
Lock_A_same_surface_or_orthogonal_role_swap: NOT_YET_SATISFIED
Lock_B_cross_predicate_and_surface_transfer: REQUIRED_AND_PLAUSIBLE
Lock_C_two_independent_diagnostics:
  - MemberInheritance
  - IndefiniteSingularCompatibility
  status: FROZEN_BUT_NOT_YET_SUFFICIENT_FOR_REGISTRATION
```

The strict overlay requires two strong locks, but the lack of a clean Lock A matters here because the dominant superficial explanation is exactly predicate lexical semantics.

## Required resurrection condition

043 may return to `STRICT-PASS-REGISTER / GPU AUTHORIZED` only after **one** of the following is obtained before GPU:

### Option A — auditable consensus-clear inventory

A reconstructible/public inventory large enough for held-out causal analysis where every included item is classified by at least two independent non-model diagnostics:

```text
predication-level source classification
+ member-applicability diagnostic
+ indefinite-singular compatibility diagnostic
```

Ambiguous/theory-contested items must be excluded by a rule frozen before model runs.

### Option B — genuine same-lexical/context factorization

A theory-grounded construction in which substantially the same predicate/content changes direct-kind vs characterizing role by context, without changing the lexical cue that defines the class.

### Option C — explicit Route-B theory adjudication

Two live semantic theories must make different intervention/generalization predictions on the same materials; the paper question then becomes the theory debate rather than a presumed latent label.

## If resurrected: causal specificity requirement

Any future `PredicationLevel` intervention must change both:

```text
MemberInheritanceLogit
IndefiniteSingularCompatibilityLogit
```

while preserving:

```text
GenericTruthLogit
PredicateContentLogit
```

Mandatory controls:

- predicate-only baseline;
- held-out entire predicate families;
- noun/kind domain holdout;
- generic-vs-episodic direction;
- abstractness/inclusiveness controls;
- random/shuffled subspaces.

If predicate-only classification or content destruction explains the effect, kill.

## Relationship to former 037

Former 037 asked:

> what licenses a generic generalization — statistical prevalence/cue validity or principled/causal structure?

043 asks a different object: predication level inside generic statements. Thus 037 does **not** directly kill 043. The current pause is instead caused by the stricter identifiability/theory-gold/substrate standard.

## Current verdict

```yaml
natural_question: PASS
scientific_object: REAL_BUT_THEORY_CONTESTED_AT_BROAD_LEVEL
N0_direct_neural_ownership: NOT_FOUND
N2_if_narrow_cross_diagnostic_object: PLAUSIBLE
external_experimental_anchor: EXISTS
model_independent_large_item_gold: INSUFFICIENTLY_FROZEN
lexical_predicate_confound: SEVERE
Lock_A: FAIL_FOR_NOW
Lock_B: REQUIRED
Lock_C: FROZEN
story_invariance: PASS
verdict: CONTINUE-HARD-AUDIT
PASS_REGISTER: false
GPU_AUTHORIZED: false
```

## One-line freeze

> **043 remains scientifically promising but is no longer counted. Do not run GPU. It can return only with an auditable consensus-clear predication-level inventory, a genuine same-lexical factorization, or a properly reformulated theory-adjudication contract. `Generic behavior + causal MI` is not enough.**