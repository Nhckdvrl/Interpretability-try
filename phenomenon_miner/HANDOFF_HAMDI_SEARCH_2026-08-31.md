# Hamdi-Style Interpretability Topic Search — Handoff (2026-08-31)

Status: **AUTHORITATIVE CHAT HANDOFF / 0 NEW PASS-REGISTER**

This file is the starting point for the next topic-search session. It records the latest state after the long 2026-08-31 natural-question → S0 → N0 → N1 search. If an older chat message or earlier candidate note conflicts with this file or the terminal rejection addenda referenced below, use the newer repository state.

---

## 1. Objective

Find ACL / EMNLP / NAACL-level **mechanistic interpretability scientific objects**, not generic MI experiments.

The desired shape is Hamdi-style:

```text
natural behavior / independent scientific distinction
→ scientific object is already interesting without dataset or MI
→ S0: the object is real and measurable before registration
→ N0: mother paper does not already own the title-level object
→ N1: strongest recent successor does not already own representation + causal intervention
→ mechanistic forks make genuinely different causal predictions
→ only then REGISTER
```

Do **not** optimize for returning a fixed number. The requested end goal is five hard topics, but zero is preferable to weak registrations.

---

## 2. Hamdi reference pattern to imitate

### A. Arbitrary/random-choice project

Behavior first: ordinary requests such as `pick a random digit`, `flip a coin`, or `choose any color` produce strongly biased distributions.

The scientific question became: **does the model internally represent that it is currently being asked to make an arbitrary/random choice, and what causal role does that state play?**

The important result was not merely a probe. The causal experiment falsified the simplest interpretation: the random-choice direction was a **switch/reader**, not a randomness dial. A separate late writer shaped entropy/output distribution. The reader×writer decomposition then predicted a gated low-rank intervention.

Lesson: prefer topics where causal MI can distinguish `switch vs dial`, `reader vs writer`, `overwrite vs parallel`, `shared scalar vs separate axes`, or another nontrivial mechanism. `two variables → two probe directions` is low-surprise and not enough.

### B. Knowledge vs ontology project

Prior work studied **epistemic access** (`do I know facts about x?`). Hamdi asked a genuinely different object: **does x exist in the real world?** Familiar fictional entities make the two axes naturally cross: models can know many facts about dragons/Hogwarts while representing them as fictional.

The project uses knowledge×ontology controls so rarity/familiarity cannot explain the ontology signal. An `answer as if dragons were real` instruction can flip behavior while the internal fictional-status signal remains, giving a strong representation–behavior dissociation.

Lesson: a good factorization axis is independently meaningful in the world, has natural cross-cells, and remains scientifically interesting even if the model separates the axes perfectly.

---

## 3. Authoritative gates to read before generating anything

Read these first:

- `README.md`
- `phenomenon_miner/NATURAL_QUESTION_GATE.md`
- `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
- `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
- `phenomenon_miner/FAILED_TOPICS.md`
- `archive/README.md`
- `rejected_candidates/README.md`
- every relevant `rejected_candidates/*.md` domain log

The S0 rule is especially important:

### Failure-mechanism

Before registration, the broad failure must already exist on analyzable modern open checkpoints, normally at least 2/3 families in the same direction, under ordinary faithful prompts. Human cognitive effects, closed-model effects, synthetic-only contrasts, or post-hoc filtered subsets do not count.

### Factorization/object

Before registration, both axes need independent external definitions/gold; the actual row artifact must be obtainable and parsed; decisive natural cross-cells must be counted; at least 20 source rows must be manually sanity-checked; central gold cannot be supplied by the tested LLM, an LLM judge, or new researcher annotation; the title cannot require synthetic 2×2 construction.

---

## 4. Current registration state

**New topics from this search: 0 PASS-REGISTER.**

Do not inherit any previous `lead`, `HOLD-SUBSTRATE`, or nice title as a registered candidate unless it survives the newest terminal addenda.

---

## 5. Only current non-terminal frontier lead

# Intervention Effect Direction ≠ Magnitude

Working natural question:

> A model may know whether an intervention moves people in the positive or negative direction while systematically misjudging how strongly it moves them. Are qualitative causal direction and quantitative causal magnitude computed differently?

Why it is interesting:

- 2026 Nature work evaluates 70 preregistered nationally representative US survey experiments, 469 real treatment effects and 119,330 participants. LLM-predicted treatment effects correlate strongly with real effects but are systematically too large; prominent open-weight models show the pattern.
- 2025 Nature Computational Science similarly reports that LLM replications of 156 psychology/management experiments tend to produce larger effect sizes than human studies.
- The title-level question is broader than static opinion-distribution fidelity: `which way does the intervention move the outcome?` versus `by how much?`.

Current status: **HOLD-FATAL-CONTROL / NOT REGISTERED**.

Fatal alternative explanation:

2026 **The Illusion of Intervention** shows that treatment prompts can induce **user drift**: treatment and control conditions cause the model to instantiate different latent respondent/persona populations. This creates selection/confounding bias that can inflate or shrink synthetic treatment effects; targeted confounder controls materially change/stabilize the estimate.

Required next step before any MI:

1. obtain the Nature treatment-effect artifact / code and the user-drift paper artifact;
2. determine whether sign-correct / magnitude-inflated behavior survives a faithful negative-control / user-drift correction;
3. verify the residual on analyzable open models, not just closed frontier systems;
4. if magnitude inflation disappears after correction, record `KILL-ARTIFACT` and stop;
5. only if a large residual survives, run N1 specifically for `causal effect sign vs strength internal representation / intervention` and then formulate competing mechanisms.

Do not start probes/SAEs/patching before this fatal control.

---

## 6. Topics explicitly TERMINAL from the late search

The newest authority is:

- `rejected_candidates/hamdi_search_terminal_addendum_2_2026-08-31.md`
- `rejected_candidates/late_search_addendum_2026-08-31.md`

Important terminal objects include:

- Assertion ≠ Presupposition — `KILL-DATA`; natural same-proposition asserted/presupposed population missing.
- Polysemy ≠ Homonymy — `KILL-NOVELTY`; lexical ambiguity object already internally studied.
- Coreference ≠ Bridging — `KILL-N0`; mother taxonomy owns identity vs associative reference.
- Prevalence ≠ Diagnosticity/Cue Validity — `KILL-DATA`; direct same-item human double gold too small; production frequency is not prevalence.
- Statistical significance / evidence strength ≠ effect magnitude — `KILL-MI-FIT`; BEAR data are excellent, but no established natural open-model significance-as-magnitude failure; probing two explicit numbers would be low-surprise method decoration.
- Expert/novice knowledge or curse-of-knowledge simulation — `KILL-N0`; 2026 mothers already own capability-vs-human-difficulty divergence.
- Claim content ≠ claim scope — `KILL-N0`; scientific overgeneralization mother owns scope preservation.
- Truth ≠ popular/human belief — `KILL-N1`; Nature Machine Intelligence 2025 KaBLE already owns belief/knowledge/fact distinction. `population belief` is adjective narrowing unless a qualitatively new phenomenon first appears.
- Plausible ≠ true — `KILL-DATA/NARRATIVE`; no broad natural same-statement truth×plausibility double gold and nearby representation work is crowded.
- Classic false-consensus effect — current S0 `KILL`; old mother relies on four scenarios and imposed choices. It may only re-enter after a fresh modern open-family ordinary-prompt existence screen satisfying its explicit resurrection condition.
- Statistical significance ≠ replicability — do not promote from SCORE/BEAR alone; replicability prediction is already a SCORE scientific object.

Earlier domain logs additionally kill: deontic facilitation, motivated reasoning evidence-vs-decision, ownership/self-attribution, intended-vs-perceived sarcasm, literal-vs-figurative meaning, said-vs-implicated content, emotion-vs-cause, dialogue-act-vs-affect, definiteness-vs-specificity, taxonomic-vs-thematic, animacy-vs-agentivity, agency-vs-experience, local accessibility-vs-global salience, likelihood-vs-severity, epistemic-vs-aleatoric uncertainty, moral judgment-vs-legality, mean opinion-vs-population diversity, generic VLM perception-vs-prior/color conflicts, and the repository-wide archived failures.

Do not resurrect these by swapping dataset/model/language/prompt/MI tool.

---

## 7. BEAR substrate: preserve as infrastructure, not a live topic

BEAR / `wwiecek/BEAR_data` is worth remembering as a data source even though significance-vs-magnitude is terminal under the current contract.

Verified facts:

- public data submodule contains `SCORE_replications.rds`, `SCORE_all_claims.rds`, `OSC.rds`, `ManyLabs2.rds`, etc.;
- SCORE source contains 548 original/replication rows = 274 matched original + 274 matched replication, with 267 retained by BEAR;
- SCORE all-claims has 3,066 source rows and 1,946 retained claim rows;
- BEAR processing retains effect estimate `b`, uncertainty `se`, and evidence statistics `z/p`; SCORE matched rows join original and replication by `claim_id` and keep `orig.*` values.

Use BEAR only if a **new natural behavior/object independently motivates it**. Do not reverse the order and invent a topic from its columns.

---

## 8. Search directions that are currently safer

Do **not** continue generating classic two-axis psychology/linguistics labels mechanically; that route produced many N0/N1 collisions.

Priority order for the next conversation:

1. **Strong 2025–2026 mother anomaly → unresolved internal scientific question.** Search ACL/EMNLP/NAACL/ICLR/ICML/NeurIPS/Nature for a large, cross-model, surprising open-weight behavior whose paper does *not* already complete representation + causal intervention.
2. **Everyday deterministic behavior.** Look for ordinary prompts where a stable bias is visible without a benchmark or complex protocol, analogous to arbitrary choice. Require modern open-family evidence before registration.
3. **External-world orthogonal axis.** Only if both axes have source-authored/objective row-level gold and natural cross-cells at scale. Immediately N1-search exact object synonyms plus representation/direction/feature/circuit/steering.
4. Prefer a question whose causal MI could reveal a nontrivial structure (`switch vs dial`, `reader vs writer`, `upstream prior vs downstream selector`, `parallel states vs overwrite`) rather than merely locating a signal.

Avoid:

- `mother behavior → which layer causes it?`;
- `representation exists → is it causal?`;
- another semantic relation inventory;
- another truth/belief/factuality axis;
- another local-success/global-composition or generic knows-but-does-not-use story;
- temporal forgetting / stale-state variants;
- evidence-more-hurts variants;
- task-switch / ambiguity-history / ownership variants;
- synthetic 2×2 moral/logical worlds;
- LLM-judge central gold.

---

## 9. Useful search leads that were inspected but should NOT be promoted automatically

These are observations, not candidates:

- 2026 `Partition, Prompt, Aggregate` reports a macro fallacy where subgroup estimates aggregate better than direct population estimates. Do not use it: it collides with repository `Local Success, Global Composition Failure` / generic knows-but-does-not-use logic unless a genuinely different object appears.
- 2026 negative-constraint / ironic-rebound papers already contain circuit tracing, activation patching and priming-vs-override mechanisms. The `don't say X` family is occupied.
- generic current-color / canonical-color or visual-prior conflicts route to the already terminal VLM perception–knowledge-conflict family; the multimodal rejection log explicitly warns that changing to a color conflict does not restore novelty.
- moral intent × outcome has a good philosophical 2×2 but the readily available datasets are researcher-constructed vignettes; under current factorization S0 this is not a natural substrate.
- debiasing-backfires, self-correction, correlated-majority/self-consistency and similar recent anomalies are high N0 risk because their mothers already define the external phenomenon; only retain them if a *different* scientific object emerges, not merely an MI follow-up.

---

## 10. Mandatory workflow for the next session

For every new idea:

```text
P0 plain question + one ordinary example + why care
→ classify Failure or Factorization
→ search internal negative memory BEFORE external deep dive
→ S0 actual artifact/effect audit
→ KILL immediately on missing cross-cell / synthetic-only behavior / weak family support
→ N0 assume mother already owns it; prove otherwise
→ N1 find the three strongest successors, especially 2025–2026 + arXiv
→ title-level anti-narrowing check
→ MI-fit + Hamdi-surprise check
→ only complete survivors may be called PASS-REGISTER
```

For S0 factorization, save actual counts and 20-row audit artifacts to the repo before registration. For failure topics, save item-level open-model outputs and predeclared effect signature.

Every killed serious idea must be appended to the relevant `rejected_candidates/` domain log with a nearest-neighbor warning and resurrection condition.

---

## 11. Final handoff state

```yaml
new_PASS_REGISTER: 0
current_nonterminal_leads:
  - name: Intervention Effect Direction != Magnitude
    status: HOLD-FATAL-CONTROL
    blocker: user-drift / treatment-induced population confounding must be ruled out first
terminal_second_wave:
  - Assertion != Presupposition
  - Prevalence != Diagnosticity
  - Statistical Evidence != Effect Magnitude
  - Truth != Popular Belief
  - Plausibility != Truth
  - Polysemy != Homonymy
  - Coreference != Bridging
  - Expert Knowledge != Novice Knowledge
  - Claim Content != Scope
search_target: keep searching until up to five truly hard survivors; zero is acceptable
```

One-line discipline:

> **Do not inherit attractive titles. Inherit only evidence. The next topic must already be real before MI, and MI must reveal what the computation is—not merely where a label can be decoded.**
