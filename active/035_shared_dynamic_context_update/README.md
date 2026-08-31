# 035 — Shared Dynamic Context Update Across Discourse Phenomena

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-08-31

## A. Natural question

Do LLMs interpret discourse by maintaining a **shared dynamically updated local context** that supports different phenomena such as anaphora and presupposition, or do those phenomena rely on separate task-specific / lexical heuristics?

No benchmark name is needed to state the question. It is a classic formal-semantics question about whether meaning is computed as context change and whether apparently distinct discourse phenomena share that computation.

## B. Why this is paper-scale

Dynamic semantics and Discourse Representation Theory were developed precisely because sentence meaning is not always a static truth condition: processing one expression changes which referents and propositions are available to later expressions. Anaphoric accessibility and presupposition projection are two canonical applications of this idea.

The paper would therefore not be `ACL'25 anaphora errors -> find heads` or `CoNLL'26 presupposition -> find circuit`. It asks a broader architectural question:

> **Does an autoregressive LM actually implement a reusable discourse-state update operation across linguistic phenomena?**

A positive result supports a unified dynamic-semantic computation; a negative result supports phenomenon-specific or surface/static alternatives. Either changes how we understand discourse representation in LLMs.

## C. Scientific lineage

External theory predates neural LMs by decades:

- Kamp / Heim dynamic semantics and DRT: discourse introduces and updates information states.
- Local contexts: the interpretation of later material can depend on a temporary context constructed by earlier material, especially under conditionals, conjunction, negation and disjunction.
- Dynamic binding: indefinite discourse referents become accessible or inaccessible for later anaphora depending on embedding structure.
- Presupposition projection: whether a presupposition projects depends on what the relevant local context already supports.
- Binding/unification theories of presupposition explicitly relate presupposition resolution to anaphoric accessibility.

Useful theory references:

- https://plato.stanford.edu/entries/dynamic-semantics/
- https://plato.stanford.edu/entries/discourse-representation-theory/
- Chierchia, *Dynamics of Meaning: Anaphora, Presupposition, and the Theory of Grammar*.
- Schlenker, *Presupposition Projection: Two Theories of Local Contexts*.

## D. Strong mothers / established objects

### Mother 1 — ACL 2025 Main

`Meaning Beyond Truth Conditions: Evaluating Discourse Level Understanding via Anaphora Accessibility`

Paper: https://aclanthology.org/2025.acl-long.432/
Artifact: https://github.com/xiaomeng-zhu/anaphora-accessibility

Established object:

- LLMs show systematic sensitivity to discourse-level anaphora accessibility, with human/model alignment on some structural conditions and divergence on others;
- authors motivate the dataset directly from dynamic semantics;
- released experiments cover existential/universal accessibility, donkey conditionals, negation and disjunction;
- repository releases datasets, raw model outputs, accuracy results and inference scripts;
- configs include Llama-3.1-8B / Llama-3.1-8B-Instruct and Llama-3.2 checkpoints.

### Mother 2 — CoNLL 2026 Outstanding

`Presupposition and Reasoning in Conditionals: A Theory-Based Study of Humans and LLMs`

Paper: https://aclanthology.org/2026.conll-main.26/
Artifact: https://github.com/proviso-bench/Presupposition-and-Reasoning-in-Conditionals

Established object:

- presupposition projection in conditionals produces graded human judgments driven by antecedent-presupposition relevance / probability;
- LLMs show systematic but imperfect patterns; Llama-3.1-8B and Qwen2.5-7B are explicitly evaluated;
- model behavior can align with human ratings without coherent pragmatic explanations, motivating the possibility of shallow heuristics;
- public repo releases `problem_set.json`, local Llama/Qwen inference, per-item outputs and aggregation code.

The exact same `Llama-3.1-8B-Instruct` family can therefore be examined across both scientific windows without changing the core checkpoint merely to manufacture a cross-task comparison.

## E. Exact novelty delta

Existing work owns:

1. **anaphora accessibility behavior** and the claim that lexical cues can sometimes substitute for structural abstraction;
2. **presupposition projection behavior** and the claim that human-like ratings do not guarantee coherent pragmatic reasoning;
3. explainability analyses within individual presupposition tasks.

No strongest neighbor found in the 2025–2026 literature asks whether **the same causal local-context update operation is reused across anaphora and presupposition**.

Conceptual delta:

> `Does an LM handle phenomenon X?` / `does it use shallow cues on X?`
> **→ `Does the model possess a reusable dynamic discourse-state operation that explains multiple phenomena predicted by the same formal theory?`**

This is analogous in shape to the EMNLP 2025 Outstanding filler-gap paper: the contribution is shared abstract structure across constructions/phenomena, not simply richer localization of one mother.

## F. Venue-scale comparison

- **EMNLP 2025 Outstanding — shared filler-gap structure:** asks whether multiple constructions share an abstract causal mechanism. 035 asks whether anaphora and presupposition share dynamic local-context update.
- **NAACL 2025 — taxonomy vs similarity:** competing theoretical organizations exist before the dataset; causal evidence adjudicates them. Same here for unified dynamic update vs separate/static computation.
- **ACL 2025 `Meaning Beyond Truth Conditions`:** establishes the discourse-level behavioral object, but 035 moves from one diagnostic phenomenon to a cross-phenomenon theory of discourse computation.
- **CoNLL 2026 Outstanding presupposition:** establishes the second window, but does not own shared cross-phenomenon causal machinery.

## G. Data / substrate

```yaml
natural_or_synthetic: controlled linguistically normed stimuli; theory is external
anaphora_artifact: xiaomeng-zhu/anaphora-accessibility
presupposition_artifact: proviso-bench/Presupposition-and-Reasoning-in-Conditionals
central_gold:
  anaphora: formal accessibility conditions + released item metadata/results
  presupposition: normed high/mid/low antecedent-presupposition relation + human ratings
shared_checkpoint: Llama-3.1-8B-Instruct
why_dataset_is_only_a_measurement_window: local context, dynamic binding, and presupposition projection are formal-semantic objects that predate both datasets
external_validity_path:
  - additional dynamic-semantic operators (negation/disjunction/conjunction)
  - additional open checkpoints (Qwen/Mistral)
  - ordinary multi-sentence discourse
```

The key native structural bridge already exists: **conditional local context**. ACL'25 includes donkey-conditionals for anaphoric accessibility; CoNLL'26 studies presupposition inside conditionals. Both require reasoning about material available inside the antecedent-created local environment.

## H. Competing mechanisms and frozen predictions

### H1 — Shared dynamic local-context update

The model constructs a temporary discourse state from earlier/embedding material, and both referent accessibility and presupposition support read from that same updated state.

Predictions:

- matched antecedent/context changes induce a common representational transition across the two phenomena;
- a causal direction/path identified from **context update itself**, rather than final task label, transfers across anaphora and presupposition;
- patching the antecedent-updated local state from a condition where information is accessible/supported into an inaccessible/unsupported condition shifts both downstream anaphora and presupposition judgments in the theory-predicted direction;
- interventions at the shared update stage generalize across lexical triggers and discourse referents.

### H2 — Phenomenon-specific computations

Anaphora and presupposition are solved by distinct causal pathways despite surface behavioral compatibility with dynamic semantics.

Predictions:

- within-task causal states are robust but cross-task transfer is near zero after lexical/position controls;
- patching an accessibility state does not alter presupposition projection, and vice versa;
- each phenomenon generalizes internally across lexical items but not across the theoretical boundary.

### H3 — Static/global or lexical heuristic solution

The model does not construct a reusable local discourse state. Outputs follow lexical associations, trigger identity, operator templates, or global sentence plausibility.

Predictions:

- structural equivalence with lexical changes causes unstable representations/effects;
- global lexical/plausibility interventions dominate antecedent-local structural manipulations;
- cross-task transfer disappears and even within-task structural generalization fails once lexical shortcuts are neutralized.

These are competing architectures, not early/middle/late localization categories.

## I. Story invariance

- **Result A — shared transfer:** evidence for a reusable dynamic local-context operation spanning discourse phenomena.
- **Result B — strong within-task / no cross-task transfer:** evidence that LLM discourse competence is implemented through phenomenon-specific computations rather than a unified dynamic state.
- **Result C — lexical/global controls explain both:** evidence against dynamic local-context implementation despite apparent behavioral competence.

All outcomes answer exactly:

> **Do LLMs implement a shared dynamic discourse-context update?**

No negative result requires changing the headline to benchmark validity or a particular layer.

## J. Frozen S0

### S0-0 — artifact and behavior

Already satisfied:

- ACL'25 releases raw data/results and runnable Llama configs for anaphora accessibility;
- CoNLL'26 releases raw Llama/Qwen outputs and runnable local inference for presupposition;
- `Llama-3.1-8B-Instruct` is a native overlap checkpoint;
- both mothers report systematic nontrivial behavior rather than total task incapacity.

### S0-1 — exact common structural window

Primary comparison is frozen to **conditional local-context construction**:

1. anaphora: donkey / conditional configurations where an antecedent referent is or is not accessible to a later anaphor;
2. presupposition: conditionals where antecedent information does or does not support the consequent's presupposition.

Do not choose lexical subsets after seeing MI results.

### S0-2 — minimal shared-update pairs

For each phenomenon construct clean/corrupt pairs that alter only the information contributed by the conditional antecedent while preserving:

- main connective and sentence skeleton;
- approximate token length;
- downstream anaphor/presupposition trigger;
- target referent/proposition lexical identity where possible.

The donor state must correspond to a theory-defined local-context difference, not an arbitrary correct-vs-incorrect output.

### S0-3 — cheap behavioral verification

Before expensive causal sweeps, verify on the frozen overlapping Llama checkpoint that:

- the selected mother items reproduce the published qualitative accessibility/projection sensitivity;
- comprehension of antecedent/target lexical content is intact;
- neither side is pure floor/ceiling.

This is reproduction of a fixed contract, not behavior discovery. Failure terminates the project on that checkpoint rather than changing the scientific question.

## K. First mechanistic experiment contract

1. Run the released ACL'25 and CoNLL'26 subsets on the same Llama-3.1-8B-Instruct checkpoint under frozen deterministic scoring.
2. Identify representations of the **antecedent-induced context difference** at structurally matched token positions, not labels such as `accessible`/`high` alone.
3. Perform within-task causal patching to establish a local-context state in each domain.
4. Perform **cross-task causal transfer**:
   - donor learned/identified from anaphora -> recipient presupposition;
   - donor from presupposition -> recipient anaphora.
5. Measure a preregistered cross-task transfer ratio relative to matched within-task causal effect.
6. Repeat with lexical/operator controls and shuffled donors.
7. Only after the shared-vs-specific result is established, localize pathways/heads as explanatory detail.

Primary statistic:

```text
cross_task_transfer_ratio =
  mean(|causal effect of theory-matched cross-domain donor|)
  /
  mean(|causal effect of matched within-domain donor|)
```

Interpret jointly with directionality and control-donor effects; do not choose a threshold post hoc to create `shared`.

## L. Fatal controls / hard kills

- If cross-task transfer is driven by shared lexical tokens (`if`, pronouns, possessives) rather than context content, claim fails.
- If the anaphora and presupposition conditions do not reproduce on the exact overlapping checkpoint, stop or replicate on a prespecified alternative; do not subset hunt.
- If a newly found 2025–2026 neighbor already demonstrates cross-phenomenon shared dynamic-context causal machinery, KILL-NOVELTY.
- Do not claim `dynamic semantics is true` from representational similarity alone; causal cross-domain transfer is required for the shared-computation claim.

## Registration verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
venue_comparators: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
substrate: PASS
existing_behavior: PASS
shared_checkpoint: PASS
story_invariance: PASS
competing_mechanisms: PASS
frozen_S0_contract: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```
