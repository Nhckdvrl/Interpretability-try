# 041 Hard Re-Audit — 2026-09-01

Verdict: **PASS-REGISTER / GPU AUTHORIZED — DEEP N0/N1/N2 + IDENTIFIABILITY AUDIT PASSED**

## Frozen question

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

Frozen object:

> **context-conditioned modifier set restriction / contrastive role** — whether a modifier actually reduces the currently live referent set, separately from ordinary property meaning.

The project does not require the broad claim that every contextually redundant adjective has full formal-semantic non-restrictive/appositive scope. The operational object is narrower: **live-set narrowing**.

## Why the audit was necessary

The nearest literatures are unusually mature. Reference-resolution work has modeled candidate elimination for decades; neural pragmatic models already react to distractors; overmodification work already studies redundant adjectives; masked-LM work has touched restrictive/non-restrictive relative clauses.

Therefore a simple claim such as `LLMs know which adjective is informative` would be dead on arrival. 041 survives only if the remaining object is materially stronger than those predecessors.

## External scientific anchor

Leffel, Lauter, Westerlund & Pylkkänen (2014), *Restrictive vs. non-restrictive composition: a magnetoencephalography study*, manipulates whether the same lexical material restricts the set under discussion by changing preceding context.

Canonical same-answer example:

```text
Which chicken should the farmer slaughter next?
His fat chicken.       # fat restricts among chickens

Will the farmer slaughter his chicken or his lamb?
His fat chicken.       # fat does not identify which live referent is intended
```

The study started with 53 manually constructed sets, used 105 respondents for naturalness norming, retained 46 sets, and tested contextual neural sensitivity to restriction. This establishes a real human semantics/processing object independently of LLMs.

Leffel's dissertation additionally stresses operational tests based on whether a modifier changes extension/truth conditions rather than treating lexical items as intrinsically restrictive.

## Strongest computational / neural neighbors

### 1. Schlangen, Baumann & Atterer — SIGDIAL 2009 incremental reference resolution

This work explicitly characterizes incremental reference resolution as words successively reducing the set of possible referents.

**Occupies:** candidate-set elimination as a reference-resolution algorithm.  
**Does not occupy:** whether a pretrained LM develops a same-lexical, context-conditioned modifier-role representation that generalizes across property/domain families and is causally separable from property truth.

Consequence: 041 may not claim `adjectives eliminate distractors` as new.

### 2. Monroe et al. — TACL 2017 `Colors in Context`

Uses recurrent neural speaker/listener models and pragmatic inference in a grounded color reference game.

**Occupies:** neural context-sensitive reference, pragmatic speaker/listener reasoning, distractor sensitivity.  
**Does not occupy:** a causal internal `restricting vs non-restricting role of the same modifier` object.

### 3. Fang et al. — CogSci 2022 color overmodification

Uses neural agents to study when redundant color modifiers emerge, including environmental frequency/salience and pragmatic reasoning.

**Occupies:** modifier redundancy/overmodification behavior and a neural learning account.  
**Does not occupy:** the context-conditioned role state frozen by 041.

Consequence: if 041 reduces to `informative > redundant modifier`, kill N2.

### 4. Mosbach et al. — COLING 2020 masked-LM relative clauses

Includes restrictive/non-restrictive relative-clause metadata and tests masked LMs on relative-clause knowledge. The operational annotation is heavily tied to relative-clause grammatical form/punctuation; the paper warns models may exploit comma cues.

**Occupies:** restrictive/non-restrictive RC form/grammatical behavior in BERT-like models.  
**Does not occupy:** same lexical adjective, same target phrase, same world, context-only live-set role swap with causal role specificity.

Consequence: punctuation-coded RCs cannot serve as 041's primary evidence.

### 5. Recent LLM/VLM referring-expression work

COLM 2025 *Vision-Language Models Are Not Pragmatically Competent in Referring Expression Generation* evaluates unique identification, excessive/irrelevant information and human pragmatic preference. INLG 2025 analyzes LLM reference production factors; SCiL 2026 studies adjective reasoning under overinformative contexts.

**Occupies:** modern model pragmatic reference success/failure, reference production variation, overinformativeness effects.  
**Does not occupy:** the exact abstract causal modifier-role state.

## N0 / N1 / N2 conclusion

### N0 — object ownership

The broad behaviors are occupied; the exact remaining object is not:

> **a modifier's internal functional role as contextually set-restricting versus non-restricting, with lexical meaning held fixed.**

### N1 — causal occupancy

No strongest neighbor found performs the decisive causal factorization:

```text
change/remove internal restriction-role component
→ change which modifier supports referent elimination
while
preserving ordinary property truth
```

### N2 — delta width

The novelty is not `old reference behavior + Llama + patching`.

The required delta is:

> **a reusable context-conditioned semantic-role state whose causal effect transfers across lexical/domain/surface families and is specific to referent narrowing rather than scene/property representation.**

If cross-family abstraction and causal specificity fail, N2 collapses and the project dies rather than shrinking to generic reference behavior.

## Decisive same-world identifiability microscope

Use worlds such as:

```text
A = large red circle      # target
B = large blue circle
C = small red circle

target phrase = "the large red circle"
```

All world facts, target, phrase, modifier words, modifier order and modifier truths are held fixed.

```text
live candidates {A,B}:
  red   = restricting
  large = non-restricting

live candidates {A,C}:
  large = restricting
  red   = non-restricting
```

The manipulation changes only which already-known alternatives are currently live. Thus a simple `different visual/scene facts` explanation is unavailable.

Model-independent gold:

```text
Restricts(m) =
  |Compatible(D_without_m, C)|
  >
  |Compatible(D, C)|
```

## Frozen behavioral S0

Define:

```text
ReferentMargin = log P(target) - log P(distractor)

ModifierOmissionCost(m) =
  ReferentMargin(full)
  - ReferentMargin(without m)
```

Required qualitative signature:

- high omission cost for the modifier that uniquely eliminates the live competitor;
- low cost for the same lexical modifier when it is non-restricting in the paired context;
- the costly modifier swaps when the live set swaps;
- held-out lexical/domain/surface controls pass.

If both primary model families fail the frozen capability/role-swap gate, terminate the model scope. No prompt/subset fishing.

## Frozen first causal signature

Estimate a `SetRestrictionRole` direction/subspace from balanced training contexts and held-out lexical/domain families.

Primary causal prediction:

```text
attenuate restriction-role component
on the actually restricting modifier
→ larger drop in ReferentMargin

than the same intervention on that lexical modifier
when non-restricting in the paired context
```

Primary statistic: **Role × Intervention interaction**, not best layer/head.

Specificity denominator:

```text
PropertyTruthLogit
```

The intervention must preserve whether each candidate truly has the property.

## Scene-fact vs role hard gate

A role decoder can trivially exploit context facts unless the design is strict. Therefore the abstract-role claim requires:

1. same-world role swap;
2. role-matched / fact-mismatched cross-family transfer;
3. candidate identities and positions balanced;
4. held-out adjective/property families;
5. held-out noun/domain families;
6. modifier-order reversal;
7. held-out candidate-set wording;
8. explicit raw-property and candidate-identity control directions;
9. shuffled-label and random-subspace controls;
10. property-truth preservation under causal intervention.

If these fail, verdict is `KILL-IDENTIFIABILITY`, not `weak evidence for a role state`.

## Relationship to active 038 and 040

### vs 038

038 asks how a **still-unresolved referential variable** is represented: parallel alternatives, underspecification, or premature commitment.

041 assumes a candidate set is available and asks which **modifier operation narrows that set**. It does not study ambiguity architecture or pronoun commitment.

### vs 040

040 asks numerical identity vs qualitative/type sameness and token-specific history inheritance.

041 holds entity identity and property truth fixed and asks whether a property has a **contextual referential function**. It does not ask whether two mentions are the same individual.

The causal readouts are therefore different:

```text
040: HistoryTransferLogit vs TypeKnowledgeLogit
041: ReferentMargin / modifier narrowing vs PropertyTruthLogit
```

## New-work fatal novelty condition

Kill 041 immediately if a prior or new neural/LLM paper is found that jointly does the following scientific object:

1. same lexical modifier changes restricting/non-restricting role by discourse context or live referent set;
2. internal representation is studied in a pretrained neural LM;
3. role is shown to transfer beyond specific modifier words/scenes;
4. causal intervention changes referent narrowing independently of ordinary property representation.

A paper satisfying only `models use distractors`, `models dislike redundancy`, or `restrictive RCs differ from nonrestrictive RCs` is a neighbor, not this direct collision.

## Final verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
route: C
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS_WITH_HARD_KILLS
human_scientific_anchor: PASS
deterministic_gold: PASS
same_world_role_swap: PASS
scene_fact_identifiability: PASS_WITH_HARD_KILL
story_invariance: PASS
frozen_S0: PASS
frozen_first_causal_signature: PASS
PASS_REGISTER: true
GPU_AUTHORIZED: true
```

041 remains registered. Do not broaden it into generic pragmatics/reference resolution, and do not downgrade its causal specificity to decodability.
