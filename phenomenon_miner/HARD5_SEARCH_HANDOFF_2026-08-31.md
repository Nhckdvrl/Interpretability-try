# Hard-5 Mechanistic Interpretability Topic Search — Handoff

Date: 2026-08-31  
Status: `NO PASS-REGISTER YET / 3 LIVE LEADS + 1 BACKUP / DO NOT INVENT A FIFTH`

This is the authoritative handoff for continuing the search in a fresh conversation. It deliberately contains fewer than five live leads because the repository's newer negative-memory audits killed two ideas that an earlier version of this file had mistakenly retained.

## 0. Authority / correction rule

Before trusting any attractive idea in chat history, read the repository's latest negative memory. In particular:

- `rejected_candidates/hamdi_search_terminal_addendum_2_2026-08-31.md` supersedes earlier `lead` / `HOLD` wording for the same objects.
- It terminally kills **Prevalence ≠ Diagnosticity** (`KILL-DATA`) and **Statistical Significance / Evidence Strength ≠ Effect Magnitude** (`KILL-MI-FIT / LOW_SURPRISE`).
- `rejected_candidates/late_search_addendum_2026-08-31.md` additionally freezes assertion≠presupposition, truth≠popular belief, plausible≠true, classic false-consensus under the current S0 contract, and warns not to promote significance≠replicability merely because BEAR/SCORE data are convenient.

Do not resurrect a dead scientific object by changing dataset, model, language, prompt, domain, or MI method.

---

# 1. Non-negotiable funnel

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

1. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
2. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
3. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
4. `phenomenon_miner/FAILED_TOPICS.md`
5. `phenomenon_miner/CURRENT_TOPICS.md`
6. `archive/README.md`
7. `rejected_candidates/README.md`
8. `rejected_candidates/hamdi_search_terminal_addendum_2_2026-08-31.md`
9. all relevant domain logs under `rejected_candidates/`

A clean dataset, a strong mother behavior, or a missing causal-intervention paper is never sufficient by itself.

---

# 2. Hamdi-style reference, re-checked directly in Slack

## Entity / ontology

The real-vs-imaginary work introduces **ontological existence** as an object separate from entity knowledge/familiarity. It tests domain transfer and held-out entities, then uses steering. A particularly informative dissociation is that `answer as if dragons were real` can change the model's answer while the internal imaginary/ontology signal remains active: compliance/play-along does not erase ontology.

Desired shape:

```text
world concept already contains genuinely distinct variables
→ externally establish both
→ ask whether model internally factorizes them
→ controls separate easy confounds
→ causal intervention tests the object
```

## Arbitrary choice / color

The starting point is the ordinary failure: `pick a random digit`, `flip a coin`, `choose any color` yields strong biases (7, blue, etc.) and poor requested-distribution following. Only after that behavior is visible does the mechanism question appear. Hamdi reports a reader-like arbitrary-choice mode signal and a separate randomness-amplitude writer/dial; the gated edit uses the reader state to selectively write the randomness direction.

Desired shape:

```text
ordinary behavioral anomaly already exists
→ internal state is a natural explanation target
→ competing reader / writer / dial mechanisms
→ causal intervention
```

Do not imitate the probe/SAE technique; imitate the selection of the scientific object.

---

# 3. LIVE LEAD A — Semantic Leakage / Task-Relevance Gate

Status: `LIVE BUT HIGH INTERNAL-COLLISION RISK / S0 CURRENT-OPEN-MODEL NOT DONE`

### Plain question

Why can an irrelevant fact in a prompt pull a model's answer toward a semantic association that has nothing to do with the task?

Example:

> `He likes yellow. He works as a ...` → `school bus driver`

### Mother

Gonen et al., **Does Liking Yellow Imply Driving a School Bus? Semantic Leakage in Language Models**, NAACL 2025 Long.

The mother reports semantic leakage across 13 model variants/settings, including Llama 2/3; a 2025 follow-up reproduces leakage across Qwen2.5 0.5B–7B.

### Potential new object

Not `where is semantic leakage?` but:

> Does the model represent **task relevance** separately from **semantic activation**, allowing irrelevant semantics to be read but gated away, or does any activated association automatically enter the generation writer?

Mechanistic forks:

1. **encoding contamination** — irrelevant semantics corrupt the target representation early;
2. **no relevance gate** — semantics stay distinct but the writer indiscriminately integrates active associations;
3. **gate represented but routing fails** — relevance is readable, but suppression is not causally enforced.

### Critical internal collision to audit BEFORE model calls

This may collide with the repository's successful **014 Alias Entrainment Transfer** and with 2026 contextual-entrainment work. 014 already establishes broad cross-surface learned-relation spillover; recent work also shows scale-dependent copying/entrainment of irrelevant contextual tokens.

The next conversation must first answer:

> Is `yellow → school-bus-driver` a genuinely different scientific object (task-relevance gating of semantic associations), or merely another cross-surface/contextual-entrainment instance already absorbed by 014?

If the answer is “another association spillover subtype,” `KILL-INTERNAL-COLLISION` before S0 calls.

### External N1 danger

ACL 2026 **Follow the Flow: On Information Flow Across Textual Tokens in Text-to-Image Models** causally traces a semantic-leakage analogue to cross-item encoder contamination. Therefore `semantic leakage comes from cross-token contamination` is not a safe broad novelty claim.

### Only if N0/internal-history survives

Run a predeclared 20–50 ordinary-prompt existence screen on current analyzable families:

- Qwen3-8B/14B;
- Gemma-3-12B;
- Llama-3.x.

Require ≥2/3 families with meaningful leakage above matched controls, and include natural/open-ended user-like prompts rather than only fill-in templates. If the effect only survives the mother's manually constructed protocol, `KILL-NATURALNESS/CAPABILITY`.

---

# 4. LIVE LEAD B — Right Direction, Wrong Magnitude in Human Intervention Prediction

Status: `LIVE / FATAL ARTIFACT CONTROL UNRESOLVED / OPEN-FAMILY EFFECT NOT FROZEN`

### Plain question

Why can a model often predict whether an intervention will move people **up or down**, yet systematically predict that it moves them **too much**?

### Mother evidence

Nature 2026, **Large language models can predict the results of social science experiments**:

- 70 preregistered nationally representative U.S. survey experiments;
- 469 experimental effects;
- 119,330 human participants;
- strong correlation between predicted and observed treatment effects;
- strong performance also reported for prominent open-weight models;
- systematic effect-size overestimation;
- secondary archive: 15 megastudies / 606 effects.

Independent 2025 Nature Computational Science work over 156 psychology/management scenario experiments also reports larger synthetic-LLM effects than human effects.

### Candidate scientific object

`qualitative causal direction` vs `quantitative causal strength`.

### Fatal alternative explanation

Recent synthetic-population work on **intervention-induced user drift** shows that changing the treatment can also change the implicit persona/population being simulated, creating selection/confounding that inflates or attenuates treatment estimates. Magnitude inflation therefore cannot be assumed to be an internal magnitude-computation failure.

### Immediate next task

Before MI:

1. obtain open-weight per-model source/supplementary predictions;
2. verify systematic magnitude inflation independently for ≥2 modern analyzable families, not merely high correlation;
3. reproduce an appropriate user-drift / negative-control correction;
4. require `sign broadly right + magnitude inflated` to persist after correction.

If correction removes the inflation, `KILL-ARTIFACT` immediately. Do not rescue by choosing only treatments where inflation remains.

---

# 5. LIVE LEAD C — Zero on Average Is Not No Effect: ATE ≠ Treatment-Effect Heterogeneity

Status: `FRESH FACTORIZATION LEAD / P0 PASS / N1 PROVISIONAL / S0 NOT DONE`

### Plain question

A treatment can have average effect near zero because it affects almost nobody, or because it strongly helps some people and strongly hurts others. Does a language model distinguish these two worlds?

### Why this is a real scientific object

`average treatment effect` and `treatment-effect heterogeneity` are foundational, independent causal-science quantities. A zero mean does not imply a degenerate response distribution.

### Mechanistic forks

1. **prototype-person scalar** — only an average response shift is represented;
2. **mean + heterogeneity factorization** — average effect and response variation are independent internal variables;
3. **mixture/subpopulation computation** — heterogeneity arises from multiple subgroup states rather than a single variance direction.

### N1 so far

No direct LLM mechanistic paper was found whose title-level object is internal factorization of ATE and HTE. Existing 2025–2026 HTE work is causal-inference methodology or uses LLM semantics as covariates/features for HTE estimators, not analysis of the LM's own population model.

### S0 required

Find a real experimental artifact with enough **independent interventions** and subgroup/site outcomes to objectively compute:

- average treatment effect;
- treatment-effect heterogeneity;
- natural cross-cells: low mean/low heterogeneity, low mean/high heterogeneity, high mean/low heterogeneity, high mean/high heterogeneity.

Potential instruments include megastudies or the Nature 2026 experiment archive if subgroup outcomes are public. Multi-site replication rows are not automatically independent treatment effects: e.g. Many Labs 2 has only 28 underlying analyses, so hundreds of site rows must not be counted as hundreds of scientific units.

### Strong collision boundary

Do not turn this into `average opinion ≠ population diversity`. ICLR 2026 already decodes full human answer distributions from residual streams, analyzes demographic distributions, uses SAE features and steering. Treatment-response heterogeneity must remain the causal object.

### Immediate next task

S0 artifact acquisition → exact independent-intervention counts → 2×2 counts → random-20 audit. If only a few dozen independent treatments survive, HOLD/KILL-DATA rather than pseudo-replicating rows.

---

# 6. BACKUP ONLY — Intervention-Expectation / Null-Effect Bias

Status: `NOT A CANDIDATE / FAILURE S0 REQUIRED`

### Plain question

Does merely being told that an intervention happened make a model expect that **something must change**, even when real humans show essentially no effect?

### Prior

2025 synthetic-experiment work reports many human-null experiments becoming significant in LLM-simulated populations, alongside general effect-size inflation.

### Why it might be Hamdi-like

If robust on current open models, the behavior itself is surprising and naturally suggests an internal `intervention happened → change expected` mode/gain prior rather than a generic quantitative-calibration story.

### Why it is not registered

- current multi-family open-model effect not frozen;
- low synthetic-response variance can create false significance;
- user drift can create apparent treatment effects;
- must distinguish effect on raw mean difference from effect on p-value only.

### Immediate next task

Only if Leads A–C fail or stall: construct a cheap source-grounded open-family S0 from real null-effect experiments, score raw treatment differences before significance, and require ≥2/3 current families. Kill if the effect is only a variance/statistical artifact.

---

# 7. EXPLICITLY DEAD — do not carry forward as leads

The following were attractive during this conversation but are terminal under current evidence:

- **Statistical Significance / Evidence Strength ≠ Effect Magnitude** — `KILL-MI-FIT / LOW_SURPRISE`; without an independently established natural open-model failure, hidden-state separation of explicit numeric quantities is method decoration. BEAR remains a useful instrument only if such a future behavior appears.
- **Prevalence ≠ Diagnosticity / Cue Validity** — `KILL-DATA`; clean direct human double-gold exists only at too-small scale, while larger norms replace real prevalence with proxies such as production frequency/distinctiveness.
- **Assertion ≠ Presupposition** — missing natural same-proposition/different-status population.
- **Truth ≠ Popular Belief** — 2025 KaBLE/Nature MI-level epistemic object already occupies fact/belief/knowledge; `popular` is adjective narrowing.
- **Plausible ≠ True** — no broad same-unit dual-gold population; surrounding truth/plausibility representation space crowded.
- **Significance ≠ Replicability** — SCORE already owns credibility/replicability assessment; BEAR convenience is not novelty.
- **False Consensus Effect** — current published evidence relies on four classic hypothetical stories and imposed choices; does not satisfy the modern open-family natural-failure S0.
- plus all objects already frozen in `rejected_candidates/semantic_pragmatic_factorization.md`, `risk_uncertainty_factorization.md`, `social_norm_factorization.md`, `social_simulation_factorization.md`, and the Hamdi addenda.

---

# 8. Fresh search directions ONLY AFTER current leads are adjudicated

Do not brainstorm another giant list first. If a live lead dies, search strong 2025–2026 mothers for **named, large, cross-open-family anomalies that the mother does not already mechanistically explain**.

Promising paper-family search terms, not candidates:

- reasoning enhancement that introduces a qualitatively new failure;
- capability scaling that reverses one specific natural behavior;
- relevance / irrelevance routing anomalies not reducible to 014 contextual entrainment;
- natural agent/tool failures with deterministic availability/state gold, but avoid generic `knows tool absent but uses it` and benchmark-only hallucination;
- scientific/social simulation anomalies with real-world outcome gold and open checkpoints.

Explicitly avoid Temporal Forgetting (`forgotten ≠ erased` family is internally banned), generic task switching, compositionality gap, truth/belief directions, semantic-relation inventories, and representation→causality followups.

---

# 9. Next-conversation execution order

1. **Read negative memory first** — especially `hamdi_search_terminal_addendum_2_2026-08-31.md`.
2. **Lead A: Semantic Leakage** — first do N0/internal collision against `014 Alias Entrainment Transfer` + 2026 contextual entrainment. No model calls until this is resolved.
3. **Lead B: Direction vs Magnitude** — resolve user-drift fatal alternative and open-family magnitude inflation.
4. **Lead C: ATE vs HTE** — acquire real subgroup experimental artifact and count independent interventions/cross-cells.
5. **Backup null-effect expectation** — only if one of A–C dies/stalls; modern open-family S0 first.
6. Only then search for additional mothers, continuing until **five actual PASS-REGISTER survivors** or until the evidence justifies fewer. Never manufacture a fifth to satisfy the target count.

---

# 10. Rejection-writing rule

Whenever a candidate dies, immediately add it to the appropriate `rejected_candidates/*.md` file (or create a new domain log) with:

- Natural question;
- why it initially looked good;
- exact kill evidence;
- death code;
- nearest-neighbor warning including renamed variants;
- resurrection condition.

Then update `rejected_candidates/README.md` if a new log is created.

---

# 11. PASS-REGISTER contract

A future `active/029_*` or later topic can be created only after:

```text
P0 PASS
+ type-specific S0 PASS
+ actual row-level artifact / current open-model outputs committed
+ exact cross-cell/effect counts
+ random-20 audit where applicable
+ N0 PASS
+ 3 strongest N1 neighbors attacked
+ internal-history PASS
+ title unchanged by all audits
+ MI-fit with 2–3 genuinely competing causal mechanisms
= PASS-REGISTER
```

The eventual target is five hard candidates. **Five is not permission to lower any gate.**
