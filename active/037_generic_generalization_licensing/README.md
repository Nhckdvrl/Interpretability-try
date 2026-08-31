# 037 — What Licenses a Generic Generalization? Statistics vs Conceptual Relations

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01

## A. Natural question

When a language model accepts a generic generalization such as `Birds lay eggs` or `Mosquitoes carry malaria`, what licenses that generalization: **how prevalent the property is within the kind**, a **flexible probabilistic combination of prevalence and diagnosticity/cue validity**, or a **principled/causal conceptual relation** between the kind and the property that cannot be reduced to those statistics?

The question is independent of any benchmark name. It is a long-standing problem in the semantics and psychology of generic language: true generics tolerate exceptions, some are accepted at very low prevalence, and some high-prevalence accidental properties still sound poor in generic form.

## B. Why this is paper-scale

Generic statements are a basic way humans communicate category-level knowledge. Their acceptance is famously not governed by a simple numerical threshold: only mature female birds lay eggs, very few mosquitoes carry malaria, yet the corresponding generics are natural; conversely, high-prevalence accidental properties need not license a natural generic.

Several mature theories compete over what matters:

1. **prevalence/statistical accounts** emphasize the proportion of kind members with the property, `P(F|K)`;
2. **flexible probabilistic accounts** combine prevalence with cue validity/diagnosticity, roughly `P(K|F)`, and allow their importance to depend on relation type;
3. **conceptually based accounts** argue that principled, causal, developmental, dangerous/striking, or otherwise explanatory kind–property relations can license generics beyond what prevalence/cue validity alone predicts.

The contribution is not `a generics dataset has errors -> find a generic head`. It asks:

> **What kind of computation determines whether an LLM treats a property as characteristic enough of a kind to state generically?**

The answer bears on category knowledge, default generalization, semantics, stereotype-like generalization and how LMs compress statistical versus causal/conceptual knowledge.

## C. Scientific lineage

The external debate predates LLMs by decades.

### Prevalence / statistical information

Work on generic truth conditions has repeatedly tested whether acceptance can be reduced to the proportion of instances possessing the property. Classic low-prevalence generics such as `Mosquitoes carry malaria` and `Birds lay eggs` show that a fixed prevalence threshold is insufficient, but prevalence remains an important predictor for many statistical generics.

### Flexible probabilistic account

Ryu, Yang & Park (2022), *Flexible Acceptance Condition of Generics from a Probabilistic Viewpoint*, directly measures:

- prevalence `P(F|K)`;
- cue validity / diagnosticity `P(K|F)` relative to an explicit superordinate comparison class;
- human generic acceptability.

Using 84 target generics from Prasada et al. (2013), the paper proposes a systematic flexible account: IS-A generics are mainly prevalence-driven; high-cue-validity feature generics can be licensed even at low prevalence, with prevalence modulating degree of acceptability; low-cue-validity feature generics are mainly prevalence-driven.

### Conceptual / causal account

Prasada, Khemlani, Leslie & Glucksberg (2013), *Conceptual distinctions amongst generics*, examines majority/minority characteristic, striking, statistical and false generalizations. It argues that prevalence and acceptability dissociate, that cue validity alone does not explain the hard cases, that minority-characteristic generics involve principled connections, and that striking generics can be licensed by causal relations.

Cimpian, Gelman & Brandone (2009/2010) provide controlled evidence that theory-based/developmental expectations, danger and distinctiveness alter generic judgments even when prevalence is matched. These studies explicitly contrast generics with quantified controls.

The disagreement is therefore scientific, not invented for the present project.

## D. Strong mothers / established LLM object

### Mother 1 — Findings ACL 2026

`Generics are not quantificational: A new path from language models to semantic theory`

Established object:

- large-scale comparison of naturally occurring generics and quantificational counterparts;
- evidence that language models recover semantic/distributional facts distinguishing generics from explicit quantifiers;
- argues against treating generics as simply implicit quantification;
- experiments include modern open families such as OLMo-3, Mistral/Mixtral, Llama-3.1, Qwen3 and Gemma.

This mother asks whether generic semantics is quantificational. It does **not** ask which property-level licensing architecture determines whether an individual generic is acceptable.

### Mother 2 — COLING 2025

`Generics are puzzling. Can language models find the missing piece?`

Established object:

- ConGen: 2,873 naturally occurring generic and quantified sentences in context;
- generic acceptability is highly context-sensitive;
- naturally occurring generics can express weak generalizations;
- public code/data; Mistral/Mixtral family experiments.

It studies implicit quantification/context sensitivity, not prevalence-vs-diagnosticity-vs-conceptual licensing.

### Mother 3 — Computational Linguistics 2024

`Exceptions, Instantiations, and Overgeneralization: ...`

Establishes large-scale LLM behavior around exceptions and generic property inheritance over hundreds of thousands of exemplars. It does not causally adjudicate generic licensing theories.

### Additional broad substrate

MGen provides millions of naturally occurring generic/quantified examples for later external validation; recent default-reasoning work establishes that LLM generics participate in defeasible reasoning but does not occupy the present licensing question.

## E. Exact novelty delta — N0 / N1 / N2

### N0 — object ownership

No strongest 2024–2026 LLM neighbor found owns:

> `What licenses an individual generic generalization: prevalence, flexible probabilistic diagnosticity, or conceptual/causal relation?`

Recent LLM papers own quantificationalism, contextual sensitivity, weak generics, exception handling, property inheritance and default reasoning.

### N1 — causal occupancy

No 2024–2026 mechanistic-interpretability work found performs theory-diagnostic causal interventions separating prevalence, diagnosticity/cue validity and conceptual/causal licensing in modern open-weight LLMs.

### N2 — delta width

The new question is not:

> `ACL'26 found that generics differ from quantifiers; we find the layer responsible.`

The concept-level step is:

> `LLMs have a distinct generic-generalization behavior`
> **→ `What information licenses the generalization in the first place, and which of the long-standing scientific accounts best describes the computation?`**

The factors and competing accounts were defined in human semantics/psycholinguistics before the LLM mothers and come with published natural and controlled cross-cells.

## F. Venue-scale comparison

- **NAACL 2025 — taxonomy vs similarity in property inference:** a mature cognitive competition is instantiated in LMs and causal evidence adjudicates it. 037 has the same form: statistical/flexible-probabilistic/conceptual accounts of generic licensing.
- **EMNLP 2025 Outstanding — shared filler-gap structure:** external linguistic theory defines the question before MI; interventions test the abstract computation. Same here.
- **ACL 2026 Main — tool irrelevance:** controlled factors separate natural variables rather than create the object. Human generic experiments already independently manipulate prevalence, distinctiveness and conceptual information.
- **Findings ACL 2026 — generics are not quantificational:** establishes the broad modern-LLM generic object; 037 asks a wider property-licensing question not answered by the quantificationalism comparison.

## G. Data / substrate

### Native human-gold substrate — Prasada 2013 / Ryu 2022

Ryu et al. (2022) reuses **84 target generics** from Prasada et al. (2013), with:

- 60 generally acceptable and 24 unacceptable statements;
- item-level human acceptability;
- item-level prevalence;
- explicit superordinate comparison category;
- item-level cue validity;
- diverse relation types, including difficult low-prevalence cases.

The article prints the item-level metric tables; the underlying Prasada project has a public OSF project with code/data/analyses (`https://osf.io/qdp3f/`).

Representative published hard cases include `Mosquitoes carry malaria`, whose prevalence is low but cue validity and acceptability are high, as well as striking/minority-characteristic/statistical/false-generalization classes.

### Frozen controlled causal microscope — Cimpian et al. 2010

The original human study uses novel animal kinds and independently manipulates established licensing variables.

Experiment 1:

- 30 items;
- five prevalence levels: 10%, 30%, 50%, 70%, 90%;
- plain vs dangerous+distinctive vs non-distinctive control information;
- generic vs `most` wording control.

Experiment 4 separates the conceptual factors:

- **plain**;
- **dangerous** property information;
- **distinctive** property information.

The same target kind/property can therefore be judged under matched prevalence while danger or distinctiveness changes. The article provides exact templates/material descriptions and Appendix stimuli.

Danger is not a new project-specific label: it is a published `striking-property` manipulation motivated by the generics literature. Distinctiveness is a direct diagnosticity/cue-validity manipulation: whether the property distinguishes the target kind from alternative kinds.

### Independent conceptual control — Cimpian et al. 2009/2010

A separate published experiment holds overall prevalence constant while changing the **developmental/causal organization** of the property: it can arise systematically in all adults but no young members, or be randomly distributed across ages. Humans prefer the theory-consistent developmental pattern for generics despite equal or lower overall prevalence.

### Modern open-model premise

Published 2025–2026 work already establishes nontrivial generic processing on genuinely different open families including:

- Qwen3;
- Llama-3.1;
- OLMo-3;
- Mistral/Mixtral;
- Gemma.

The project therefore does not require a GPU lottery to discover whether current open LMs possess a measurable generic-generalization object.

```yaml
natural_or_synthetic:
  native: human-normed natural generic statements
  microscope: published human psycholinguistic novel-kind experiments
central_gold:
  - human acceptability
  - prevalence P(F|K)
  - cue validity P(K|F)
  - published relation classes/manipulations
row_level_artifact:
  - 84-item published tables + Prasada OSF project
  - exact Cimpian experiment materials/templates and appendices
open_checkpoint:
  - Qwen3 family
  - Llama-3.1 family
  - OLMo-3 / Mistral / Gemma as preregistered replication options
modern_open_family_evidence: published multi-family generic behavior in 2026 Findings + earlier modern LLM generics work
why_dataset_is_only_a_measurement_window: generic licensing, prevalence, cue validity and conceptual/causal connections are independent scientific objects predating LLMs
external_validity_path:
  - ConGen natural contextual generics
  - MGen millions of natural generics
  - large exception/property-inheritance corpora
```

## H. Competing mechanisms and frozen predictions

### H1 — Prevalence-dominant statistical licensing

The model principally treats a generic as licensed when enough members of kind `K` possess property `F`; the computation is dominated by `P(F|K)`.

Predictions:

- changing prevalence while holding kind/property/conceptual information fixed has a large causal effect on generic acceptance;
- distinctiveness/cue-validity information adds little once prevalence is controlled;
- danger/developmental-causal information adds little once prevalence and surface comprehensibility are controlled;
- low-prevalence accepted natural items should be difficult to explain after controlling lexical memorization.

### H2 — Flexible probabilistic licensing

The model combines prevalence with diagnosticity/cue validity, with their weights depending on the relation type, broadly matching Ryu et al.'s flexible probabilistic account.

Predictions:

- prevalence has a robust causal effect;
- distinctiveness / cue-validity information has an additional causal effect, especially for feature-describing low-prevalence items;
- prevalence × diagnosticity interactions follow the published human pattern;
- once those probabilities are controlled, danger or theory-based causal organization should contribute little independent generic-specific effect.

### H3 — Conceptual / causal licensing

The model can treat a kind–property relation as characteristic because of principled, causal, developmental or striking conceptual structure that is not reducible to prevalence and cue validity.

Predictions:

- prevalence and diagnosticity can matter but are insufficient;
- at matched prevalence and diagnosticity, published danger/causal/developmental manipulations retain a generic-specific causal effect;
- this residual conceptual effect is not reproduced for matched `most`-quantified controls;
- native human low-prevalence conceptual generics remain licensed after statistical covariates are accounted for.

These are competing computations, not early/middle/late localization categories.

## I. Story invariance

- **Result A — prevalence dominates:** LLM generic licensing is substantially more threshold/statistical than human conceptually flexible generic judgment.
- **Result B — prevalence + diagnosticity interact:** LLMs implement a flexible probabilistic licensing rule resembling comparative-probability accounts.
- **Result C — conceptual residual survives:** LLMs use kind–property causal/principled information that cannot be reduced to prevalence/cue validity alone.

All outcomes answer exactly:

> **What licenses generic generalizations in LLMs?**

No outcome requires retitling the paper as a benchmark failure or layer-localization study.

## J. Frozen S0

### S0-0 — broad existence (already satisfied)

Modern open families already exhibit systematic generic behavior in published work. This satisfies the broad Route-A premise.

### S0-1 — native 84-item measurement

Use **all 84** Ryu/Prasada items; do not select by model effect. Reproduce the human-style acceptability judgment on two preregistered modern families first (primary: Qwen3 and Llama-3.1; third family only as replication, not rescue).

The measurement gate requires:

- output scale/task understood;
- nondegenerate acceptability distribution;
- ordinary lexical comprehension intact;
- generic judgments distinguish at least basic accepted/unaccepted human items above chance / nontrivially.

If this fixed measurement window collapses on both families, terminate rather than prompt/subset hunt.

### S0-2 — published controlled cells

Use the Cimpian stimuli/manipulations as published, preserving all valid items rather than selecting effect-positive ones:

1. prevalence levels;
2. plain vs distinctive evidence;
3. plain vs dangerous evidence;
4. generic vs `most` control where available;
5. developmental-causal vs random-distribution control as independent conceptual replication.

The central variables and cross-cells are human experimental manipulations, not synthetic factors invented after seeing LM outputs.

## K. First mechanistic experiment contract

The first causal analysis is frozen before GPU use.

### K1 — matched evidence pairs

For the same novel kind/property and target judgment, construct source/recipient pairs from the published controlled conditions that differ in exactly one scientific factor:

- **prevalence pair**: higher vs lower `P(F|K)`;
- **diagnosticity pair**: distinctive vs matched non-distinctive/plain information at fixed prevalence;
- **conceptual pair**: dangerous vs matched plain information at fixed prevalence, with developmental-causal vs random organization as independent replication.

### K2 — causal intervention

At the point where the model has read the evidence and must judge the target generic, perform activation/path patching from the factor-high condition into its factor-low matched recipient and vice versa.

Do not select a best layer for the primary claim. For each factor, integrate the signed target-logit recovery over the prespecified full model depth after normalizing by the clean/corrupt behavioral logit gap.

### K3 — frozen primary causal statistic

```text
licensing_causal_signature = (
  E_prevalence,
  E_diagnosticity,
  E_conceptual
)

where E_factor = across-depth AUC of normalized causal recovery
for the matched intervention that changes only that published factor.
```

Primary theory patterns:

```text
H1 prevalence-dominant:
  E_prevalence >> 0
  E_diagnosticity ~ 0 after prevalence control
  E_conceptual ~ 0

H2 flexible probabilistic:
  E_prevalence > 0
  E_diagnosticity > 0 with the published prevalence/relation interaction
  E_conceptual ~ 0 after statistical controls

H3 conceptual/causal:
  E_prevalence and/or E_diagnosticity may be > 0
  BUT E_conceptual remains > 0 at matched prevalence/diagnosticity
  and the conceptual residual is generic-specific
```

The full signature and confidence intervals are reported; no post-hoc scalar threshold defines a theory winner.

### K4 — generic-specificity interaction

A required fatal-control statistic accompanies the primary signature:

```text
conceptual_generic_specificity =
  E_conceptual(generic judgment)
  - E_conceptual(matched MOST-quantified judgment)
```

A conceptual-licensing claim requires this interaction to be positive and robust. If danger/distinctiveness merely acts as a generic sentiment/keyword cue and shifts `most` equally, H3 fails.

## L. Fatal controls / hard kills

1. **`most` quantifier control:** conceptual licensing effects must be specific to generics, reproducing the logic of the original human experiment.
2. **Evidence comprehension:** verify that the model understands prevalence percentages, distinctiveness and danger independently of the generic judgment.
3. **Lexical keyword control:** paraphrase `dangerous`, `distinctive`, `unique`, etc.; include matched non-generic tasks so effects cannot be attributed to one cue word.
4. **Native validation:** conceptual claims must also be compatible with the 84 natural human-gold generics; the novel-kind microscope alone cannot define the paper object.
5. **No item hunting:** all valid published items/cells are frozen before model outputs.
6. **No best-layer selection:** primary effect is the across-depth normalized causal AUC signature.
7. **Shuffled donors:** factor-matched patching must exceed shuffled lexical/context donors.
8. **Probability confound:** conceptual pairs must hold prevalence fixed; diagnosticity must be explicitly measured/held where claimed.
9. **Prompt rescue forbidden:** if the frozen acceptability measurement fails on both primary families, terminate rather than prompt search.
10. **Novelty kill:** if a newly found modern-open LLM study already causally adjudicates generic licensing by prevalence vs diagnosticity vs conceptual/causal relation, terminate for novelty.

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
central_human_gold: PASS
published_natural_cross_cells: PASS
published_controlled_microscope: PASS
modern_open_model_premise: PASS
route_A_omitted_axis: PASS
story_invariance: PASS
competing_mechanisms: PASS
frozen_S0_contract: PASS
frozen_first_causal_statistic: PASS
fatal_controls: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

Registration freezes the scientific question, the 84-item native window, the published Cimpian controlled cells, the three-component causal signature and the generic-vs-`most` fatal interaction. GPU may be used only to answer this frozen question; a null cannot trigger a narrower benchmark or layer story.
