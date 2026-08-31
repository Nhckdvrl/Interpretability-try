# Hard-5 Mechanistic Interpretability Topic Search — Handoff

Date: 2026-08-31  
Status: `NO PASS-REGISTER YET / 5 CONTINUATION LEADS RANKED / NEGATIVE MEMORY UPDATED`

This handoff exists so a new conversation / researcher can continue the search without re-generating the same dead ideas or weakening the repository gates.

---

# 0. Non-negotiable process

Use the repository's authoritative order:

```text
Natural Question / P0
→ classify Failure-mechanism vs Factorization/object
→ S0 scientific substrate
→ open-model existence/capability contract
→ N0 mother-inclusion attack
→ N1 strongest-neighbor attack
→ internal-history audit
→ narrative-width + anti-narrowing
→ MI-fit
→ only then PASS-REGISTER
```

Read first:

- `phenomenon_miner/NATURAL_QUESTION_GATE.md`
- `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
- `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
- `phenomenon_miner/FAILED_TOPICS.md`
- `archive/README.md`
- `rejected_candidates/README.md`
- all relevant domain logs under `rejected_candidates/`

A clean dataset, a strong mother behavior, or a missing causal-intervention paper is **not** sufficient by itself.

---

# 1. What Hamdi-style topic selection means here

Two successful shapes were re-checked directly in Slack `#r_hamdi`.

## Entity / ontology shape

Hamdi's real-vs-imaginary work treats **ontological existence** as a new scientific object rather than a proxy for entity familiarity. The project explicitly separates ontology from knowledge/familiarity, tests domain transfer and held-out entities, and then uses causal steering. An especially important result is that an instruction such as `answer as if dragons were real` can change the model's answer while its internal imaginary/ontology signal remains active: compliance/play-along does not erase the ontology representation.

Lesson:

```text
world concept already has two genuinely distinct variables
→ establish both externally
→ ask whether model internally factorizes them
→ controls separate easy confounds
→ causal intervention tests the object
```

## Arbitrary-choice / color shape

Hamdi starts from an obvious behavior: `pick a random digit`, `flip a coin`, `choose any color` produces strongly biased outputs (e.g. 7, blue) and models fail to follow requested sampling proportions. Only **after the behavior** does he ask whether the model contains an internal state meaning `I am being asked to make an arbitrary choice`. He finds a reader-like mode signal and a second randomness-amplitude writer/dial, then uses a gated edit.

Lesson:

```text
ordinary behavioral anomaly already exists
→ internal state is a natural explanation target
→ competing reader / writer / dial mechanisms
→ causal intervention
```

Do not imitate the probe/SAE technique; imitate the selection of the scientific object.

---

# 2. Current ranked continuation leads

None is `PASS-REGISTER` yet. They are ranked by how much of the hard contract is already satisfied.

---

## Lead A — How Big, and How Certain? Effect Magnitude ≠ Evidence Precision

### Status

`STRONGEST FACTORIZATION LEAD / HOLD-S0-COUNTS / N1 PROVISIONAL PASS`

### Plain question

A scientific effect can be **large but estimated imprecisely**, or **tiny but known very precisely**. Does a language model represent `how big is the effect?` separately from `how strong/precise is the evidence?`, or collapse both into one generic `strength of result` signal?

### Why it is natural

This is not `p-value trivia`. Statistical inference distinguishes the estimated magnitude from its uncertainty. `p < .05` or a z statistic is a combination of estimate and standard error; it does not define effect magnitude.

### Type

`Factorization/internal-object`

### Strong substrate discovered

**BEAR — Benchmarks of Empirical Accuracy in Research**

- code repo: https://github.com/wwiecek/BEAR
- data submodule: https://github.com/wwiecek/BEAR_data
- BEAR stores standardized effect estimate `b`, standard error `se`, and/or `z = b/se` across many real research databases;
- the public data repo contains row-level `SCORE_all_claims.rds`, `SCORE_replications.rds`, `OSC.rds`, `ManyLabs2.rds` and many other sources;
- SCORE all-claims source contains natural claim/statistical-evidence text, not just aggregate p-values;
- SCORE replication source contains matched original and replication outcomes;
- Many Labs 2 stores site-level correlation effect estimates and standard errors for 28 preregistered analyses.

SCORE itself covers thousands of manually extracted social/behavioral research claims and publishes open data/code/materials.

### Why it may be novel

A focused N1 search on 2025–2026 work did **not** find a direct mechanistic LLM paper whose title-level object is internal factorization of effect estimate vs statistical precision / uncertainty. Existing work teaches/reporting significance and effect sizes, or uses statistics to evaluate LLMs, rather than reverse-engineering how an LM represents scientific results.

### Mechanistic forks

1. **Generic result-strength scalar:** magnitude, certainty and significance collapse into one state.
2. **Estimate × precision factorization:** effect magnitude and uncertainty are separately encoded; significance/evidence is computed downstream.
3. **Normalized-evidence-first:** a z/significance-like state dominates internally and raw magnitude is only reconstructed from scale/context.

### Decisive causal experiment

Use natural scientific result/claim text with independent `b` and `se` gold. Identify cases with similar magnitude/different precision and similar precision/different magnitude. Causally interchange/steer the candidate internal variables and require a double dissociation:

- magnitude intervention changes quantitative effect-size judgment but minimally changes evidence-strength/significance judgment;
- precision intervention changes certainty/evidence judgment but minimally changes effect-size judgment.

### Fatal controls

- remove / mask explicit `p < .05`, `significant`, star markers and significance language;
- control sample size as a possible lexical proxy;
- normalize heterogeneous effect-size scales or use source subsets with a common standardized measure;
- hold scientific domain out;
- distinguish reading a reported number from reconstructing the scientific quantity;
- do not create the central 2×2 with synthetic statistic templates if natural rows do not suffice.

### Immediate next task

**S0 only. Do not run MI yet.** Materialize / parse BEAR/SCORE row-level artifacts and count:

- rows with usable natural claim/result text;
- rows with effect estimate + SE/CI;
- magnitude bins × precision bins (predeclare thresholds based on source-native scale or quantiles, then sensitivity analysis);
- independent claim/study counts, not duplicated site/statistic rows;
- random 20 audit;
- attrition reasons;
- whether one broad title can survive without restricting to one discipline or one effect-size family.

If the usable natural-text population collapses to a tiny or single-domain subset, `KILL-DATA` rather than synthesizing examples.

---

## Lead B — Why Does Irrelevant Meaning Leak? Semantic Presence ≠ Task Relevance

### Status

`STRONG FAILURE LEAD / HOLD-MODERN-OPEN-FAMILY S0 / N1 CAUTION`

### Plain question

Why can an irrelevant fact in a prompt pull a language model's answer toward a semantic association that has nothing to do with the task?

Example:

> `He likes yellow. He works as a ...`  
> → `school bus driver`

### Mother

Gonen et al., **Does Liking Yellow Imply Driving a School Bus? Semantic Leakage in Language Models**, NAACL 2025 Long.

- 109 matched prompts across colors, foods, animals, occupations, names, idioms, etc.;
- semantic leakage is strong across 13 model variants/settings;
- Llama 2 and Llama 3 open-weight families show Leak-Rate far above 50%;
- instruction-tuned Llama variants leak more than pretrained variants;
- an independent 2025 follow-up reproduces leakage in Qwen2.5 0.5B–7B and releases generations/evaluation code.

### Hamdi-style extension

Do **not** ask `which layer causes semantic leakage?`.

Ask a new internal-object question:

> Does an LM represent **task relevance** separately from **semantic activation**, so that irrelevant semantics can be read but gated away, or does any activated association automatically enter the writer/generation pathway?

### Mechanistic forks

1. **Encoding contamination:** the irrelevant concept changes the representation of the target/completion slot early; leakage already exists before task readout.
2. **No relevance gate:** semantic representations remain separate, but the output writer indiscriminately integrates active associations.
3. **Relevance represented but gating fails:** a decodable relevant/irrelevant state exists, yet suppression/routing does not causally block the association.

### Strongest N1 attack

ACL 2026 **Follow the Flow: On Information Flow Across Textual Tokens in Text-to-Image Models** already shows a mechanistic semantic-leakage analogue in T2I: cross-item information can contaminate text-encoder token representations, and patching a cleaned representation sharply reduces misinterpretation.

This does **not automatically kill** the LLM-text topic, but it means `cross-token contamination causes leakage` cannot be claimed broadly as new. The LLM project must distinguish encoding contamination from a **task-relevance gate / writer-routing** mechanism and show an LLM-specific title-level object.

### Fatal S0 issue

The original mother uses manually constructed matched prompts. The repository forbids registering a failure that exists only inside a synthetic protocol. Before registration, reproduce the phenomenon in current analyzable families with ordinary faithful prompts, ideally including open-ended / natural user-like contexts rather than only fill-in templates.

### Immediate next task

Run a predeclared 20–50 prompt sanity on at least:

- Qwen3-8B or 14B;
- Gemma-3-12B;
- Llama-3.1/3.2/3.3 analyzable checkpoint.

Require ≥2/3 families, meaningful Leak-Rate above control, and a visible ordinary-example effect. Include a natural/open-ended subset and lexical-overlap controls. If only the old Llama/Qwen2.5 templates work, `KILL-CAPABILITY/NATURALNESS`.

---

## Lead C — Right Direction ≠ Right Magnitude in Human-Behavior Intervention Prediction

### Status

`HOLD-FATAL-CONTROL / HOLD-OPEN-FAMILY`

### Plain question

Why can a language model often predict whether a social intervention will move people **up or down**, yet systematically predict that it moves them **too much**?

### Mother evidence

Nature 2026, **Large language models can predict the results of social science experiments**:

- 70 preregistered nationally representative U.S. survey experiments;
- 469 experimental effects;
- 119,330 human participants;
- predictions strongly correlate with observed treatment effects;
- correlations remain high for prominent open-weight models;
- predicted effects systematically overestimate effect sizes;
- secondary archive: 15 megastudies / 606 effects.

Independent Nature Computational Science 2025 evidence across 156 psychology/management scenario experiments similarly reports high main-effect replication but consistently larger LLM effect sizes.

### Scientific object

`qualitative causal direction` vs `quantitative causal strength`.

### Fatal alternative explanation

Recent work on **intervention-induced user drift** shows that changing a synthetic participant's treatment can also change the latent persona/population being simulated, producing confounding/selection effects that inflate or attenuate estimated treatment effects. Therefore the published magnitude inflation cannot be assumed to be an internal `magnitude computation` failure.

### Immediate next task

Before any MI:

1. obtain the open-weight per-model source/supplementary results;
2. verify systematic magnitude inflation independently for ≥2 modern analyzable families;
3. apply / reproduce a user-drift or negative-control correction;
4. require the sign-right / magnitude-inflated signature to persist after correction.

If correction removes the effect, `KILL-ARTIFACT` immediately.

---

## Lead D — Common Is Not Telltale: Prevalence ≠ Diagnosticity

### Status

`HOLD-SUBSTRATE-SCALE / N1 PROVISIONAL PASS`

### Plain question

An attribute being common in a category is not the same as the attribute telling you that something belongs to that category.

Examples:

- `Birds have eyes`: very high `P(eyes | bird)`, but eyes are not very diagnostic of being a bird.
- `Mosquitoes carry malaria`: lower prevalence, but malaria-carrying is much more category-diagnostic.

### Existing substrate

Psycholinguistic generic norms provide the **same 84 generic statements** with independently elicited:

- generic acceptability;
- prevalence;
- superordinate-category judgments;
- cue validity / diagnosticity.

For feature-describing generics, prevalence and cue validity are close to uncorrelated (`r ≈ .11`), empirically confirming that the two human variables are not the same axis.

### Why not registered

Only ~84 independent target statements (roughly ~64 feature-describing generics) are available in the clean same-item norm. Repeated participant ratings do not create more independent semantic units. That is likely too thin for a multi-family ACL/EMNLP mechanistic paper.

### Rule

Do **not** expand by LLM-generating thousands of concept-feature pairs and scoring them ourselves. That would destroy S0.

### Immediate next task

Search specifically for a larger published concept-property norm in which the **same items** receive independent human `prevalence / production frequency` and `cue validity / diagnosticity / category likelihood` ratings. If no such artifact exists, keep HOLD or KILL-DATA; do not rescue with proxies.

---

## Lead E — Zero on Average Is Not No Effect: Average Effect ≠ Effect Heterogeneity

### Status

`FRESH FACTORIZATION LEAD / P0 PASS / N1 PROVISIONAL / S0 NOT DONE`

### Plain question

A treatment can have average effect near zero because it truly affects nobody, or because it strongly helps some people and strongly hurts others. Does a language model distinguish these two worlds?

### Why it is natural

`average treatment effect` and `treatment-effect heterogeneity` are foundational, independent causal-science objects. A zero mean does not imply a degenerate distribution of individual/subgroup effects.

### Why MI is natural

A model that simulates one prototype person may encode only a population-average response. A model with a genuine population model may represent treatment modifiers / heterogeneous response structure separately.

### Mechanistic forks

1. **Prototype-person scalar:** only an average response shift is represented; heterogeneity is absent.
2. **Mean + heterogeneity factorization:** average treatment effect and variation across subgroups are independent internal variables.
3. **Mixture/subpopulation representation:** heterogeneity emerges from multiple subgroup states rather than one explicit variance direction.

### N1 so far

No direct LLM mechanistic paper was found that studies internal factorization of ATE and HTE. Recent HTE papers are causal-inference methodology or use LLM semantics as input features for HTE estimators, not analysis of an LM's own internal human-response model.

### S0 problem to solve

Need a real experimental artifact with enough **independent interventions** and subgroup/site treatment effects to compute objective:

- mean treatment effect;
- cross-subgroup/site heterogeneity;
- natural cross-cells: low mean/low heterogeneity, low mean/high heterogeneity, high mean/low heterogeneity, high mean/high heterogeneity.

Potential instruments:

- the 2026 Nature treatment-effect archive if subgroup source data are public;
- megastudies with many interventions and subgroup outcomes;
- multi-site replication experiments (but beware: 28 Many Labs 2 underlying effects may be too few and site variation is not identical to individual HTE).

Do not equate ordinary opinion-distribution diversity with treatment-effect heterogeneity; ICLR 2026 already mechanistically studies full human opinion distributions, SAE features and steering.

### Immediate next task

S0 artifact search + exact cross-cell counts only. If the only clean source has a few dozen independent interventions, HOLD/KILL rather than calling hundreds of site rows independent units.

---

# 3. Backup failure lead — Intervention-Expectation / Null-Effect Bias

`NOT YET A CANDIDATE.`

Nature Computational Science 2025 reports that when human experiments have null results, the tested LLM simulations often generate significant effects anyway (roughly 68–83% depending on model), alongside general effect-size inflation.

Natural question:

> Does merely being told that an intervention happened create an internal expectation that *something must change*?

This could be a stronger failure-mechanism story than generic effect-size inflation, but it is not registered because:

- only one clearly open model family in that mother is readily analyzable;
- low synthetic-response variance and user drift can create false positives;
- a modern Qwen/Gemma/Llama existence screen is mandatory.

Do not promote without S0.

---

# 4. Newly frozen deaths in this search

See:

- `rejected_candidates/semantic_pragmatic_factorization.md`
- `rejected_candidates/hamdi_search_addendum_2026-08-31.md`
- `rejected_candidates/late_search_addendum_2026-08-31.md`
- `rejected_candidates/risk_uncertainty_factorization.md`
- `rejected_candidates/social_norm_factorization.md`

Important new terminal/negative memories include:

- speaker intent ≠ listener sarcasm perception — prior title-level object;
- literal ≠ figurative meaning — direct causal-mechanism collision;
- said ≠ implicated — missing paired literal target;
- emotion ≠ cause — representation/cause disentanglement already occupied;
- dialogue act ≠ affect — long-standing joint representation object;
- definiteness ≠ specificity — BCCWJ natural 2×2 has a zero cell (`definite + nonspecific = 0`);
- taxonomic ≠ thematic — semantic-relation MI + internal W41 collision;
- animacy ≠ agentivity — available annotation ontology cannot provide intended orthogonal cells;
- agency ≠ experience — direct mechanistic steering collision;
- givenness/local accessibility ≠ global salience — 2026 mother directly owns the object;
- deontic facilitation — internal archive 004 matched experiment terminal (`0/32` strong pairs);
- motivated reasoning evidence-vs-decision — small protocol + persona activation-patching collision;
- self-attribution/ownership confidence — mother owns behavior + internal archive 007 collision;
- likelihood ≠ severity — direct 2026 internal decomposition collision;
- epistemic ≠ aleatoric uncertainty — direct probe/decomposition literature;
- average opinion ≠ population diversity — ICLR 2026 residual-stream distribution decoding + SAE steering;
- wrong/morally bad ≠ illegal — Social Chemistry 101 mother itself explicitly owns multidimensional moral/legal norms;
- assertion ≠ presupposition — no natural same-proposition/different-status population;
- truth ≠ popular belief — Nature Machine Intelligence 2025 KaBLE owns truth/belief/knowledge object; `popular` would be adjective narrowing;
- plausible ≠ true — no broad natural dual-gold population; surrounding representation space crowded;
- classic false consensus effect — current S0 fails because evidence is four old hypothetical scenarios with imposed choices;
- significance ≠ replicability — SCORE already owns replicability/credibility assessment; BEAR data convenience is not novelty.

---

# 5. Search patterns to avoid next

Kill or route immediately unless genuinely new evidence changes the object:

```text
representation exists → is it causal?
behavior paper → we localize a layer/head
same known phenomenon → another dataset/domain/language
clean joint labels → therefore hidden-state factorization is a paper
classic human bias → assume modern open LLM also has it
synthetic 2×2 → call the resulting contrast a natural phenomenon
one family positive → general ACL title
missing gold → use LLM judge / our own annotation for the headline variable
N1 collision → save novelty by adding an adjective/subtype
```

---

# 6. Recommended execution order in the next conversation

Do not brainstorm 30 more topics first. Finish the current highest-EV gates in this order:

1. **Lead A — Effect Magnitude ≠ Evidence Precision**  
   Materialize BEAR/SCORE → exact row schema/counts → random-20 → cross-cells → N1 final.

2. **Lead B — Semantic Leakage / Task-Relevance Gate**  
   Current open-family 20–50 prompt existence screen → natural/open-ended subset → if 2/3 families pass, N0/N1 exact object audit.

3. **Lead C — Direction ≠ Magnitude**  
   resolve user-drift fatal alternative + per-open-family effect inflation. Kill if corrected effect disappears.

4. **Lead E — ATE ≠ HTE**  
   search/load subgroup experimental source → count independent interventions/cross-cells. Kill if only site-row pseudo-N.

5. **Lead D — Prevalence ≠ Diagnosticity**  
   search only for larger same-item human norm. Do not spend model calls until scale problem is solved.

Only after one of these dies should the search expand to a new mother family.

---

# 7. Registration discipline

A future `active/029_*` or later directory may be created only when the candidate has:

```text
P0 PASS
+ type-specific S0 PASS
+ actual row-level artifact / open-model outputs committed
+ exact cross-cell/effect counts
+ random-20 audit where applicable
+ N0 PASS
+ 3 strongest N1 neighbors attacked
+ internal-history PASS
+ title unchanged by all audits
= PASS-REGISTER
```

The desired eventual output is five hard candidates, but **five is not a reason to lower any gate**.
