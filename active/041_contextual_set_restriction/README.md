# 041 — Which Modifier Is Actually Doing the Identifying? Contextual Set Restriction in LLMs

Status: **KEEP / FULL CHAIN PASSED / DEEPENING**

Execution update (2026-09-04). Under `E0`, the obviousness constraint, the S0 result — omitting the
modifier that actually distinguishes the target costs more than omitting the redundant one — is a
capability denominator, not the contribution: its direction is predictable in advance and its
explanation is only that the description became less informative.

What carries the topic is the set of claims whose direction was not predictable:

- **Separable from ambiguity.** With restriction and description-uniqueness deliberately decorrelated,
  the role direction transfers across the uniqueness manipulation (0.867-0.929) in 4/4 families while
  a uniqueness direction classifies restriction at 0.363-0.451, i.e. at or below chance.
- **Graded, not binary.** When the same modifier removes 1, 2 or 3 candidates, the projection onto the
  role direction rises monotonically (+16% to +91% from k=1 to k=3) while the behavioural cost is flat
  or slightly negative in 3/4 families. The non-restricting modifier's projection falls through zero
  as the other's degree rises in 4/4, so the two are coded relative to each other.
- **Causally selective.** The frozen causal contract passes in 4/4 with held-out property families, a
  held-out surface form, shuffled-label and random controls, and property truth preserved.

Across Qwen3 1.7B to 32B the effect holds with the same sign at every size and the probe is at
ceiling throughout, so the scaling series is a robustness check rather than a claim. A 0.6B point
was run and discarded: sub-billion scale is not what this work is read against, and the
"representation present, behaviour absent" reading it would have supported does not survive its own
numbers, since 0.6B's behaviour is reliably non-zero on continuous metrics (+0.44 [+0.40, +0.47]).
A within-model task-load experiment (S8) was run to look for a representation/use gap at 8B-12B and
returned a negative result — on the candidate-load axis the probe degrades more than behaviour in all
four families — so that claim is dropped from the topic. It costs nothing: the graded result above is
already a representation/use gap of a cleaner kind, at normal scale, with full accuracy at 1.000.

The Leffel natural-language window replicates in 3/5 on an adequacy readout; a direct metalinguistic
"is this word needed" question fails everywhere to an over-informativeness bias. See
`EXPERIMENT_LOG.md`.

Date: 2026-09-01  
Route: **C — simple natural object first**

## A. Frozen natural question

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

The key point is that this is **context-conditioned**. The same adjective in the same target phrase can be identifying in one discourse context and non-identifying in another.

Frozen scientific object:

> **contextual set restriction / contrastive modifier role** — whether a modifier reduces the current live set of candidate referents.

This project deliberately does **not** claim that every redundant adjective is a syntactically or semantically `non-restrictive adjective` in every formal-semantic sense. The operational object is narrower and auditable: **does this modifier reduce the contextually live referent set?**

---

## B. Why this is a real scientific object

Restrictive versus non-restrictive / contrastive modification is an established object in semantics and psycholinguistics. A restrictive modifier helps identify the intended referent by limiting the set under discussion; a non-restricting use can provide a true property without narrowing that live set.

Leffel, Lauter, Westerlund & Pylkkänen (2014), *Restrictive vs. non-restrictive composition: a magnetoencephalography study*, gives an unusually clean human substrate. It keeps the lexical material of the critical answer fixed while changing the preceding question so the same modifier changes role:

```text
Q: Which chicken should the farmer slaughter next?
A: His fat chicken.      # fat is contrastive/restricting among chickens

Q: Will the farmer slaughter his chicken or his lamb?
A: His fat chicken.      # fat does not identify which live referent is meant
```

The paper explicitly defines restriction as **limiting the set of entities under discussion**, and reports a contextual neural sensitivity to the contrast. It began with 53 manually constructed stimulus sets, normed naturalness with 105 respondents, and retained 46 sets.

Leffel's dissertation further emphasizes an extensional/truth-conditional operationalization: empirical restrictiveness should be tested by whether adding/removing the modifier changes the relevant extension/truth conditions, rather than by treating particular adjective words as intrinsically restrictive.

Important source:

- Leffel et al. 2014: https://pmc.ncbi.nlm.nih.gov/articles/PMC4205928/

This is therefore not a label invented for an LLM benchmark.

---

## C. Strongest-neighbor audit — N0 / N1 / N2

### C1 — incremental reference-resolution models own candidate elimination as an algorithm

Schlangen, Baumann & Atterer (SIGDIAL 2009) explicitly describe incremental reference resolution as words progressively reducing the set of possible referents. Later situated reference-resolution models similarly learn word meanings and incrementally narrow candidate sets.

Therefore 041 may **not** claim novelty as:

> `language models can use adjectives to eliminate distractors`.

That computational idea is old.

### C2 — neural pragmatic reference models own informativeness / redundancy behavior

Monroe et al. (TACL 2017), *Colors in Context*, uses recurrent neural speaker/listener models plus pragmatic inference for grounded reference. Fang et al. (CogSci 2022), *Color Overmodification Emerges from Data-Driven Learning and Pragmatic Reasoning*, directly studies redundant modifiers in neural agents. Human and computational referring-expression literatures also extensively study contrast sets, overspecification and modifier informativeness.

Therefore 041 may **not** claim novelty as:

- models are sensitive to distractors;
- informative adjectives help reference;
- redundant adjectives occur or incur processing cost;
- pragmatic reference can be modeled neurally.

### C3 — masked-LM relative-clause work is a strong wording warning, not ownership

Mosbach et al. (COLING 2020), *A Closer Look at Linguistic Knowledge in Masked Language Models: The Case of Relative Clauses in American English*, includes `RESTRICTIVE` metadata for relative clauses. But its restrictiveness annotation is tied largely to relative-clause grammatical form/punctuation, and the paper itself warns that models may rely on comma cues. It does not ask whether an identical lexical modifier switches an abstract set-restriction role solely because the live discourse candidate set changes.

Thus 041 cannot use comma/no-comma relative clauses as its primary evidence.

### C4 — current LLM/VLM referring-expression work owns pragmatic success/failure, not this latent object

Recent work such as COLM 2025 *Vision-Language Models Are Not Pragmatically Competent in Referring Expression Generation* studies whether generated descriptions uniquely identify a referent, contain excessive/irrelevant information, and align with human pragmatic preferences. INLG 2025 analyzes factors in LLM reference production. SCiL 2026 studies scalar adjective reasoning under overinformative contexts.

These are important behavioral neighbors. They do not isolate **the same lexical modifier changing functional role with the discourse candidate set**, nor causally test a transferable modifier-role state in an open-weight autoregressive LM.

### C5 — exact N2 delta

The required novelty is therefore not reference behavior and not modifier informativeness by itself:

> **Does a modern autoregressive LLM construct an abstract, reusable, context-conditioned set-restriction state for a modifier — tracking whether that modifier actually narrows the live referent set — and causally use that state to decide which modifier the model relies on for reference, separately from ordinary property knowledge?**

To earn this delta, the result must generalize across lexical property families and domains, and the causal effect must be specific to referent narrowing rather than simply editing scene facts, adjective meaning, salience or generic entity identity.

No strongest-neighbor search found a neural/LLM study that owns this exact object-level question.

---

## D. Why this is not generic entity tracking, reference resolution, or redundancy

- **Entity tracking** asks which states/attributes belong to already individuated entities.
- **Reference resolution** asks which entity a full expression denotes.
- **Overmodification/redundancy** asks whether a speaker/listener uses more description than communicatively necessary.
- **041** asks for the **functional role of each modifier inside the same expression**: which modifier currently removes alternatives from the live candidate set, despite identical lexical meaning and target truth.

The hard cross-case is:

```text
same target phrase
+ same target object
+ same world facts
+ same modifier truth
+ same number of live candidates

but

different discourse candidate set
→ the modifier that actually narrows reference swaps
```

If the result reduces to generic reference competence, distractor salience or redundant-adjective behavior, 041 fails N2.

---

## E. Deterministic substrate and controlled microscope

### E1 — natural human window

Use the Leffel et al. same-answer question–answer paradigm as the natural validation window. The released paper gives the experimental design, examples, item counts and human norming, and defines the manipulation independently of any LLM.

The human stimulus inventory is not used as a hidden source of model labels. The central gold is the externally established set-restriction relation.

### E2 — deterministic role-swap construction

The primary causal microscope is generated from explicit finite worlds whose gold is mathematically determined.

A canonical three-object world:

```text
A = large red circle      # target
B = large blue circle
C = small red circle

target phrase = "the large red circle"
```

Keep **all object facts and the target phrase fixed**.

```text
Context AB: the live choice is between A and B
  red   = RESTRICTING
  large = NON-RESTRICTING with respect to the live set

Context AC: the live choice is between A and C
  large = RESTRICTING
  red   = NON-RESTRICTING with respect to the live set
```

Thus the only manipulated information is which already-described alternatives are currently live candidates. The target label, target properties, lexical modifiers, word order, total world facts and candidate-set cardinality remain fixed.

### E3 — model-independent gold

For a target description `D`, modifier `m`, world `W`, and live candidate set `C`, define:

```text
Compatible(D, C) = candidates in C satisfying D

Restricts(m) =
  |Compatible(D_without_m, C)|
  >
  |Compatible(D, C)|
```

The label is therefore computed from explicit denotations and the live candidate set; no LLM judge and no manual post-hoc label creation is required.

### E4 — scale and generalization families

Generate balanced worlds across prespecified families:

- color × size;
- material × shape;
- texture × color;
- natural-object attributes;
- person/role descriptions where properties are ordinary and non-sensitive;
- held-out lexical paraphrases of the candidate-set introduction.

Primary discovery and validation splits are disjoint in adjective/property family and noun/domain family.

The synthetic worlds are a **causal microscope**. The scientific distinction comes from independent semantic/psycholinguistic theory, and the Leffel materials provide a natural-language validation window.

---

## F. Prespecified model scope

Primary mechanistic panel:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

Both are analyzable open-weight autoregressive Transformer families. Existing open-model work establishes substantial basic reference/discourse competence; 041 does not require a published exact restrictiveness phenotype before registration under Route C.

A family contributes to the causal claim only after passing the frozen cheap S0 below.

No architecture comparison is part of the novelty claim.

---

## G. Frozen S0 — capability, not behavior lottery

### S0-1 — basic reference capability

On all prespecified role-swap worlds, deterministic forced-choice scoring must show that the model can identify the target from the full description above a frozen capability threshold and is not at floor/ceiling for all diagnostic readouts.

### S0-2 — behavioral modifier-role sensitivity

For modifier `m`, define:

```text
ReferentMargin =
  log P(target label) - log P(distractor label)

ModifierOmissionCost(m) =
  ReferentMargin(full description)
  - ReferentMargin(description without m)
```

Required qualitative double dissociation:

- when `m` is the only modifier that removes the live distractor, omitting it should have a substantially larger cost;
- when the same lexical `m` is non-restricting in the paired context, omission cost should be much smaller;
- the pattern must swap when the live candidate set swaps.

This is a reproduction/capability gate for the frozen object. If both primary families fail, terminate the current model scope; do not prompt-search or rename the topic.

### S0-3 — surface controls

The behavior must survive:

- reversing modifier order;
- arbitrary entity labels;
- paraphrased candidate-set introductions;
- held-out adjective and noun families;
- matched one-modifier controls;
- equal candidate-set size and equal total world facts.

---

## H. Frozen first causal-use contract

Central question:

> **Is contextual set restriction merely decodable from the hidden state, or does the model actually use a modifier-role representation to decide which modifier should eliminate a competing referent?**

### H1 — role-state estimation

Estimate a low-dimensional `SetRestrictionRole` direction/subspace at prespecified modifier/integration positions using training worlds in which:

- the same lexical modifier appears in both roles across different items;
- adjective identity, modifier position, target label, domain and candidate-set membership are balanced;
- train and test property/noun families are disjoint.

Do not select a best layer using causal-test performance.

### H2 — primary causal specificity test

On held-out role-swap worlds, remove/attenuate the estimated restrictive-role component for one modifier while leaving the input text and world unchanged.

Frozen prediction:

```text
role intervention on the actually restricting modifier
→ larger drop in ReferentMargin

than the same intervention on the same lexical modifier
when it is non-restricting in the paired context
```

The key statistic is the **Role × Intervention interaction**, averaged over held-out lexical/domain families, not the best layer/head.

### H3 — property-truth preservation

The same intervention must preserve ordinary knowledge of the described property.

Define a separate forced-choice `PropertyTruthLogit`, e.g. whether A is red/large and whether B/C have those properties.

Required pattern:

```text
SetRestrictionRole intervention
  changes modifier-specific referent elimination / ReferentMargin
  while preserving PropertyTruthLogit
```

If the intervention simply makes the model forget that an object is red/large, the causal claim fails.

### H4 — the decisive confound: scene facts vs abstract role

Because restrictiveness is computed from context, a decoder can trivially exploit raw candidate facts. Therefore a valid 041 result requires all of the following:

1. **same-world role swap:** all object properties remain identical; only which alternatives are live changes;
2. **role-matched / fact-mismatched generalization:** a role direction learned from one property/domain family must work on held-out families with different object facts;
3. **active-candidate control:** balance candidate identities/positions so a direction cannot be a particular A/B/C or recency signal;
4. **property residual/control:** explicitly compare against directions for raw property truth and candidate identity;
5. **shuffled-label/random-subspace controls:** causal effects must exceed matched controls;
6. **cross-surface transfer:** the role effect must survive held-out wording of the discourse candidate set.

If these controls cannot distinguish an abstract modifier role from raw distractor facts, terminate the latent-object claim.

---

## I. Story invariance

### Result A — abstract contextual restriction

The same modifier acquires a cross-surface, cross-domain role state based on the current referent set, and that state causally determines which modifier the model relies on for reference while preserving property truth.

### Result B — local but non-abstract computation

Models resolve the role-swap behavior, but the internal signal does not generalize across lexical/domain families or cannot be separated from raw candidate facts. The model uses local reference computations without a reusable abstract set-restriction state.

### Result C — superficial/reference collapse

Behavior is explained by lexical position, candidate identity, scene facts, salience or generic reference heuristics; no robust role-specific causal state survives controls.

All three answer the same question:

> **Does the model represent and use which modifier is currently doing the referent narrowing?**

No null permits a pivot to generic adjective informativeness, reference resolution accuracy, or a best-head paper.

---

## J. Fatal controls / hard kills

1. **New direct collision:** prior neural/LLM work is found that already causally identifies a context-conditioned modifier set-restriction state with same-lexical role swaps -> `KILL-NOVELTY`.
2. **Reference-resolution collapse:** only generic target-vs-distractor competence is shown -> `KILL-N2`.
3. **Redundancy collapse:** the result is only `informative adjectives matter more than redundant adjectives`, with no abstract held-out causal role state -> `KILL-N2`.
4. **Scene-fact collapse:** the role signal is fully explained by which distractor has which property or which candidate is active -> `KILL-IDENTIFIABILITY`.
5. **Property-destruction:** intervention changes ordinary property truth as much as referent narrowing -> no role-specific causal claim.
6. **Lexical/position collapse:** effect fails held-out adjectives, nouns, modifier positions or candidate-set paraphrases -> no abstract state claim.
7. **Best-layer-only result:** a localized decodable feature without functional specificity -> `KILL-SCALE`.
8. **Behavior lottery prohibited:** failed S0 cannot be rescued by searching prompts/subsets or redefining `restrictiveness`.

---

## K. Venue-scale comparison

- **EMNLP 2025 Outstanding — shared filler-gap structure:** uses causal cross-construction transfer to establish an abstract linguistic representation rather than surface decodability. 041 similarly requires cross-lexical/domain transfer of a context-defined semantic role.
- **ACL 2026 — Do LLMs Know Tool Irrelevance?:** cleanly dissociates semantic relevance from structural matching and requires causal decision specificity. 041 dissociates property truth from referential diagnosticity and requires the intervention to change reference while preserving property knowledge.
- **ACL 2025 Outstanding — Llama See, Llama Do:** shows how a simple, broad phenomenon becomes paper-scale through characterization, causal mechanism and consequence. 041 follows the same simplicity-first shape.
- **Leffel et al. 2014 human MEG:** provides the independent natural semantics/neuroscience object and same-lexical context manipulation; the LLM contribution is not to rename this human result, but to test abstract reusable causal implementation in modern pretrained models.

---

## L. Paper-expansion discipline

Do not pre-invent a circuit or failure mode.

Conditional evidence ladder:

```text
1. same-world behavioral role-swap double dissociation
2. cross-lexical / cross-domain / cross-surface abstraction
3. causal referent-narrowing specificity while preserving property truth
4. only if a stable mechanism is found: derive a new falsifiable failure prediction
5. targeted behavioral verification
6. optional mitigation/generalization
```

Stages 4–6 are not preregistered stories; earlier evidence must earn them.

---

## M. Registration verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
route: C
human_scientific_substrate: PASS
model_independent_gold: PASS
controlled_role_swap: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS_WITH_HARD_N2_KILLS
analyzable_open_checkpoints: PASS
exact_modern_open_published_phenotype_required: false
story_invariance: PASS
central_confound_identifiability: PASS_WITH_HARD_KILL
frozen_S0_contract: PASS
frozen_causal_use_contract: PASS
GPU_AUTHORIZED: true
verdict: PASS-REGISTER
```

## One-line freeze

> **041 asks whether modern LLMs build and causally use an abstract, context-conditioned modifier set-restriction role — which property is actually narrowing the live referent set — separately from the modifier's ordinary property meaning. Generic reference resolution, distractor sensitivity, redundancy behavior, relative-clause punctuation and raw scene facts are neighbors or controls, not substitutes for the frozen object.**
