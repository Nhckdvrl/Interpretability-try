# Hamdi-Style Interpretability Topic Search — Authoritative Handoff (2026-08-31, FINAL CONTINUATION STATE)

Status: **AUTHORITATIVE NEXT-CHAT HANDOFF / 0 NEW PASS-REGISTER**

This file is the single highest-priority state for the next conversation. If an older chat message, candidate file, `lead`, `PRE-CANDIDATE`, `HOLD`, `survivor`, or `under audit` label conflicts with this handoff or the latest terminal addendum, **use this handoff + newest terminal addendum**.

The user wants up to five genuinely hard ACL / EMNLP / NAACL-style mechanistic-interpretability topics. **Do not lower the bar to reach five.** The current search has produced **0 new `PASS-REGISTER`**. That is an evidence-based result, not permission to relabel a HOLD.

---

# 1. Read these files first, in this order

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — this file
3. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
4. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
5. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
6. `phenomenon_miner/FAILED_TOPICS.md`
7. `archive/README.md`
8. `rejected_candidates/README.md`
9. `rejected_candidates/continuation_terminal_addendum_6_2026-08-31.md` — latest terminal log
10. `rejected_candidates/continuation_terminal_addendum_5_2026-08-31.md`
11. earlier terminal addenda and any domain log relevant to a new idea

Newest terminal files override stale positive wording in older domain logs.

---

# 2. Core philosophy — do not regress

The target is a **scientific object**, not an MI demo.

Required funnel:

```text
P0 Natural Question
→ classify Failure-mechanism / Factorization-object
→ internal negative-memory audit
→ S0 actual scientific substrate
→ open-model existence/capability
→ N0 mother-inclusion attack
→ N1 strongest-neighbor/successor attack
→ narrative-width + anti-narrowing
→ MI-fit + Hamdi-surprise
→ only then PASS-REGISTER
```

A good topic should remain meaningful after deleting the words `dataset`, `benchmark`, `probe`, `SAE`, `feature`, `head`, `activation patching`, and `steering`.

Do not infer a phenomenon from a convenient dataset. Do not infer behavior from a pretty mechanism story.

---

# 3. What the Hamdi examples actually teach

## Random/arbitrary choice

The behavior came first: ordinary prompts such as `pick a random digit`, `flip a coin`, `choose any color` show obvious biased output distributions.

Then the internal question became interesting. A choice-mode representation existed, but causal work showed it was a **switch/reader**, not the intuitive `randomness dial`; a distinct downstream writer shaped entropy/output distribution. That decomposition predicted a simple low-rank/gated intervention.

Important lesson from Hamdi's own Slack thread: a strong MI result should ideally **predict a qualitatively simpler intervention or falsify the intuitive mechanism**, not merely localize where the failure occurs. He deliberately avoided adding technically possible extra distribution families when they would weaken the aesthetic/scientific story.

## Knowledge vs ontology/existence

The question existed before the dataset: knowing facts about an entity and representing that entity as actually existing are different cognitive/world-model properties. Familiar fictional entities naturally cross the axes.

Important lesson: a factorization topic must have **independently meaningful external variables and natural cross-cells**. The 2×2 is a test of the question, not the source of the question.

---

# 4. S0 contracts

## Failure-mechanism

Before registration:

- the behavior already exists on analyzable **current open checkpoints**;
- default promotion criterion: at least 2/3 relevant model families same direction;
- ordinary faithful prompts;
- no post-hoc subset rescue;
- no synthetic-only existence evidence;
- save item-level outputs, scorer and exact checkpoint revisions;
- effect must be scientifically substantial, not merely nonzero.

## Factorization/internal-object

Before registration:

- axis A and B independently defined outside the model;
- independent source/expert/human/deterministic gold;
- row-level artifact actually obtained and parsed;
- natural cross-cells actually counted;
- random-20 sanity audit saved;
- attrition/restriction budget explicit;
- no new researcher labels for the core axis;
- no LLM-judge central gold;
- no synthetic 2×2 manufactured to make the title true.

If the artifact is unavailable, the cross-cells vanish, or the second axis is only a proxy: KILL.

---

# 5. Current registration state

```yaml
new_PASS_REGISTER: 0
registered_new_topics: []
```

**No candidate passes the current bar.**

There is one old high-priority HOLD plus three newly discovered exploratory frontiers. None counts toward five. No MI is authorized on any of them yet.

---

# 6. Priority frontier 1 — Intervention Effect Direction ≠ Magnitude

Natural question:

> A model may correctly predict whether an intervention moves an outcome up or down while systematically misjudging how strongly it moves the outcome. Are qualitative causal direction and quantitative causal magnitude genuinely different computations?

Current state:

```text
HOLD-FATAL-CONTROL / NOT REGISTERED / NO MI AUTHORIZED
```

Why it remains the highest-priority frontier:

- 2026 Nature work covers 70 preregistered nationally representative US survey experiments, 469 real treatment effects, 119,330 participants;
- predicted effects correspond strongly with real effects while magnitude is systematically inflated;
- prominent open-weight models participate in the reported pattern;
- `direction` and `magnitude` are natural properties of the same causal effect.

Fatal alternative:

2026 `The Illusion of Intervention` shows intervention-induced user/persona drift: treatment/control prompts can cause the model to instantiate different latent respondent populations. This can create selection/confounding bias and alter synthetic treatment-effect magnitude.

Mandatory next actions, in order:

1. obtain the Nature treatment-effect artifact/code and the user-drift paper artifact/code;
2. reproduce `direction mostly correct + magnitude inflated` on analyzable current open models;
3. implement the user-drift paper's faithful negative-control / confounder correction;
4. measure the residual magnitude inflation;
5. residual disappears → `KILL-ARTIFACT`, write rejection, do not subset-rescue;
6. only if a substantial residual survives across open families → N1 exact mechanism audit;
7. only after that may probes/SAEs/patching/steering begin.

Candidate mechanisms only after the fatal control:

- one signed causal-strength scalar;
- qualitative sign state + separate quantitative gain writer;
- population-response representation from which both are downstream statistics;
- apparent effect representation is actually latent-population identity drift.

---

# 7. Exploratory frontier 2 — Visual size → mass shortcut

Current state:

```text
PRE-S0 / NOT REGISTERED / NO MI
```

Natural question if the behavior exists:

> When estimating an object's mass, does a VLM use physical/material evidence, or does apparent/metric size act as a shortcut that systematically pulls the estimate?

What is already verified:

- VisPhysQuant public `output.json` was actually fetched and parsed: **221 real objects**;
- rows provide `ID`, `weight_kg`, and multi-view image paths;
- the public Drive also provides `r3d_data.zip` (~14.27 GB) with Record3D RGB-D data;
- public code `draw_bbox_axis.py` deterministically computes metric `x_length` / `y_length` from depth + camera intrinsics, so size does not require our hand labeling;
- the PhysQuantAgent GitHub tree contains scripts only; **there is no precomputed per-view Qwen3-VL result artifact** to discover by further repository searching;
- PhysQuantAgent's general mass-decomposition method is not novelty for us: volume×density/material factorization is already terminal because 2026 physical-mass papers explicitly own that decomposition.

Fatal missing evidence:

There is **no established current-open-family phenotype that signed/residual mass error systematically follows visual/metric size**. Generic mass error is not evidence of a size shortcut.

Required G0:

- use real VisPhysQuant/ABO-style objects, no synthetic balloon/lead 2×2;
- current interpretable VLM families, default >=3 families;
- identical ordinary mass-estimation prompt;
- save raw per-item predictions;
- fit whether size predicts signed/residual mass error after reasonable object/category/material controls that are defined before seeing results;
- if no substantial >=2/3-family effect: `KILL-S0` immediately;
- do not rescue by picking a product subtype or extreme size subset.

If it survives, N0/N1 must then attack `visual weight estimation`, `size-weight illusion`, `mass estimation`, `physical property representation`, `shortcut`, `SAE`, `patching`, `steering`.

---

# 8. Exploratory frontier 3 — Mass-specific cross-view instability / latent physical-property constancy

Current state:

```text
HOLD-OPEN-MODEL-EXISTENCE / NOT REGISTERED / NO MI
```

Natural observation behind the lead:

Older open-VLM qualitative mass-estimation results show that the **same real object's estimated mass can change by large factors across camera views**, despite the true mass being invariant. 2026 PhysQuantAgent also motivates multi-view aggregation because raw observations can yield unstable mass estimates.

Why this is not simply generic perceptual constancy:

Generic color/size/shape perceptual constancy is already terminal: a CogSci 2025 mother evaluates it broadly, and subsequent work owns size constancy. Mass is different because it is a **latent physical property**, not a directly visible surface property. This distinction must be earned behaviorally; it cannot be asserted for novelty.

Fatal missing evidence:

No sufficient item-level modern-open-family cross-view mass artifact was found. The PhysQuantAgent repo has no hidden result file to keep searching for.

Required G0:

- choose at least 3 current interpretable VLM families (e.g. Qwen3-VL plus two genuinely different current open multimodal families);
- temperature/deterministic decoding fixed;
- same real object, >=4 views, identical prompt;
- quantify within-object prediction dispersion in log-mass space;
- compare against stable object-identity/category recognition as a control;
- control image resize/crop pipeline and same-view reruns;
- promotion requires substantial same-object instability in >=2/3 families across a broad object set;
- one-family or cherry-picked-object effect → `KILL-S0`.

If it survives, the scientific object must stay `latent physical-property inference under irrelevant view change`, not generic perceptual constancy.

---

# 9. Exploratory frontier 4 — Causal relevance ≠ principal/actual-cause selection in real investigations

Current state:

```text
PRE-G0 / ARTIFACT-EXECUTION-BLOCKER / NOT REGISTERED / NO MI
```

Natural question:

> In a real accident, several findings can be causally relevant, yet investigators distinguish principal/probable causes from contributing factors. Can a model recognize causal relevance but fail at causal selection?

Why it is potentially interesting:

This is not merely `cause vs non-cause`. The competing mechanisms could be:

- one causal-strength scalar with a threshold;
- causal-relevance representation plus a separate actual/principal-cause selector;
- normality/responsibility/necessity-like downstream selection over already causal findings;
- failure to bind a causal role to the correct finding.

Do not tell this mechanism story unless the behavioral dissociation actually exists.

Artifact status is now concrete:

- NTSB officially publishes aviation data from 1982-present as `avall.zip`;
- official directory: `https://data.ntsb.gov/avdata`;
- on 2026-08-31 the directory lists `avall.zip`, created **2026-08-01**, size **95,636,276 bytes**;
- official release documentation preserves structured findings, including legacy `cause_factor` (`C` / `F`) and newer probable-cause inclusion metadata (`cm_inPC`);
- official NTSB data page: `https://www.ntsb.gov/safety/data/pages/Data_Stats.aspx`;
- this chat's web layer could enumerate the file but the binary download endpoint returned cache-miss, so the MDB was **not parsed**.

Next action — do not repeat web/schema searching:

1. in a normal-network shell, download the official `avall.zip` from the NTSB directory;
2. extract the MDB;
3. enumerate tables/columns, especially `findings`;
4. count `cause_factor=C/F`, `cm_inPC`, years, missingness;
5. count accidents with multiple findings and mixed roles;
6. save a random-20 row audit;
7. determine whether the units/text let us ask an ordinary model question without reconstructing a hidden label by hand;
8. only then run current-open-family G0.

The official C/F taxonomy is **not itself the topic**. Promotion requires an open-model behavioral dissociation: causal relevance is substantially intact while principal-cause selection is systematically wrong. If that dissociation does not exist, `KILL-S0`.

Strong N1 warnings already known:

- `AC-Reason` and related work own formal actual-causation reasoning;
- medical-incident work already distinguishes cause vs contributing-factor extraction;
- therefore novelty cannot be `LLMs do actual causation` or `cause vs factor classification`.

The only plausible title-level object is **causal relevance vs causal selection in natural expert investigations**, if the behavioral effect is large and broad.

---

# 10. Latest terminal negative knowledge — must read addendum 6 before brainstorming

`rejected_candidates/continuation_terminal_addendum_6_2026-08-31.md` newly kills/finalizes:

- numeric heaping / round-number attraction — `KILL-S0`;
- subliminal-learning learner-channel vs reader-channel — `KILL-N1`, direct mechanism crowding;
- disease commonness/prevalence vs lethality — `KILL-DATA`;
- power vs status — `KILL-DATA`, second-axis proxy;
- authorship/source vs endorsement/commitment — `KILL-INTERNAL-HISTORY`;
- mass volume×density/material factorization — `KILL-N0`;
- unit/representation invariance — `KILL-N0`, NUMCoT/numeracy mother;
- anchoring reader/writer — `KILL-N1`, direct mechanism/circuit work;
- apparent brightness vs intrinsic luminosity — `KILL-N1`, AstroPT/scientific-ground-truth MI collision;
- earthquake magnitude vs local intensity — `KILL-S0`;
- absolute count vs proportion / ratio bias — `KILL-S0`;
- pairwise preference vs transitive/global ranking — `KILL-N0`;
- occupational income vs prestige/status — `KILL-N0`, 2026 multidimensional-prestige mother;
- manipulation-strategy detection vs human belief-change magnitude — `KILL-N0`;
- inattentional blindness / visual presence vs report — `KILL-N0`;
- legal case content vs authority/applicability — `KILL-N0`;
- belief-expression framing vs context/prior integration — `KILL-N0`;
- healthfulness vs sustainability — `KILL-P0/S0`, data-first axis/no open-model halo phenotype;
- institutional role vs prominence (`capital` vs `largest city`) — `KILL-N1`, relational-fact circuit collision.

Addendum 5 already terminalizes:

- belief-update gate vs update magnitude;
- sentience/suffering vs intelligence as animal moral-status basis;
- implicit preference adaptation vs inhibition;
- privacy knowledge vs privacy-preserving action;
- generic perceptual constancy;
- relational-property essentialization (`invasive` as global trait).

Do not resurrect any of these with another dataset, language, model, prompt, subset, domain, or MI method unless the written resurrection condition is actually satisfied.

---

# 11. Earlier high-value terminal families — never reopen casually

Among many others, these are firmly dead:

- Statistical Evidence/Significance ≠ Effect Magnitude — `KILL-MI-FIT`; BEAR is infrastructure only.
- Prevalence ≠ Diagnosticity — `KILL-DATA`.
- Truth ≠ Popular/Human Belief — `KILL-N1`.
- Assertion ≠ Presupposition — `KILL-DATA`.
- Premise reversal blocks fallacies — `KILL-S0`, PyETR synthetic-only existence substrate.
- Deontic facilitation — terminal internal negative.
- Description–History gap — mother owns behavior; mechanism-only successor.
- recognition ≠ recall / encoded ≠ retrievable name — direct 2026 recognition/recall object.
- content memory ≠ source memory — direct mother.
- what ≠ where — direct VLM classification/localization mechanism work.
- category membership ≠ typicality — direct concept-typicality MI work.
- popularity/fame ≠ quality — direct disentangling/steering object.
- strong memory ≠ executive control.
- rank fidelity ≠ absolute calibration.
- moral ordering ≠ moral intensity.
- generic physical conservation under transformation — mother owns headline behavior; old PRE-CANDIDATE is terminal.

Search the rejection logs instead of relying on this abbreviated list.

---

# 12. Search prior for the next chat

Do not spend the whole chat only auditing the four frontiers. Continue finding new scientific objects.

## Priority 1 — 2025–2026 strong mother anomaly → lateral new object

Scan:

- ACL / Findings ACL
- EMNLP / Findings EMNLP
- NAACL
- ICLR
- ICML
- NeurIPS
- TACL / Computational Linguistics
- Nature
- Nature Machine Intelligence
- Nature Computational Science
- high-quality CogSci/behavioral work only when it uses current open models or provides an unusually strong external substrate

Look for **tables/ablations with a stable dissociation that the mother did not itself name as the scientific object**.

Reject immediately when the obvious paper is `mother reports X → we explain X with activation patching`.

## Priority 2 — everyday deterministic / distributional behavior

Ordinary prompts where the effect is visible without a benchmark, analogous in spirit to arbitrary choice but not the same family.

Requirements:

- broad domains;
- current open families;
- simple deterministic scorer or direct distribution statistic;
- effect precedes mechanism story.

## Priority 3 — external-world scientific structure

A world-grounded factorization is allowed only when:

- variables are independently meaningful in the world;
- independent gold exists for both;
- same natural units/objects;
- natural cross-cells;
- broad row-level artifact;
- no new core labels;
- even perfect model separation would still be a scientific finding;
- strongest-neighbor MI search does not already own the object.

Promising abstract shapes, not candidate titles:

- intrinsic quantity vs relational/context-bound quantity;
- latent stable property vs irrelevant observation change;
- causal relevance vs downstream causal-role selection;
- upstream state vs downstream selector **only when behavior first forces this distinction**.

Do not mechanically search `X != Y`.

---

# 13. Anti-patterns — do not waste another cycle

Especially avoid:

- temporal forgetting / stale state;
- task-switch carryover;
- ambiguity-history hysteresis;
- evidence-more-hurts variants;
- local-success/global-composition gap;
- generic truth/belief/factuality/uncertainty axes;
- ownership/self-attribution;
- semantic relation inventories;
- sentiment/emotion/dialogue-act pairings;
- synthetic moral/logic 2×2;
- generic `knows/can do X but doesn't use X`;
- `representation exists -> is it causal?`;
- `mother behavior -> which layer/head/circuit?`;
- changing only dataset/model/language/prompt/MI tool after a collision;
- LLM-judge central gold;
- hand-labeling the missing axis;
- proxying the title variable with a nearby available column;
- adding adjectives to rescue a narrow title after N1 collision.

---

# 14. Required N1 attack

For every serious candidate, actively search at least three strongest 2025–2026 neighbors using combinations of:

```text
representation
latent
direction
feature
circuit
SAE
activation patching
causal intervention
steering
disentangle
factorization
mechanism
```

Cover arXiv, ACL Anthology, OpenReview, PMLR and strong journal proceedings as appropriate.

Do not search only for supportive citations. Search to kill the idea.

---

# 15. Rejection logging contract

Any idea that reaches serious audit and dies must be written to the appropriate `rejected_candidates/` log immediately, with:

- Natural question
- Why it looked good
- Kill evidence
- Death code
- Nearest-neighbor warning
- Resurrection condition

The purpose is to prevent renaming the same dead scientific object later.

---

# 16. Survivor output contract

Only true survivors should be shown as candidates. Each must include exactly the user's 20 sections:

1. Plain question
2. One example
3. Why this matters
4. Topic type
5. Mother paper
6. Hamdi-style extension
7. S0 Scientific Substrate
8. Open-model viability
9. N0
10. N1 — at least 3 strongest neighbors
11. Internal-history audit
12. Exact novelty
13. Forbidden claims
14. Mechanistic forks
15. Decisive causal experiment
16. Fatal controls
17. ACL/EMNLP title
18. Four-sentence abstract skeleton
19. Anti-narrowing verdict
20. Final verdict

Five means five `PASS-REGISTER`, not five HOLDs.

If none passes, explicitly state:

> `No candidate passes the current bar.`

Then continue searching new mother families rather than lowering gates.

---

# 17. Machine-readable state

```yaml
handoff_date: 2026-08-31
new_PASS_REGISTER: 0
registered_new_topics: []
MI_authorized_now: false

frontiers:
  intervention_effect_direction_vs_magnitude:
    state: HOLD-FATAL-CONTROL
    priority: 1
    blocker: treatment-induced user/persona drift may explain magnitude inflation
    next_action: reproduce open-model effect then apply faithful negative-control/confounder correction
    kill_if: residual magnitude inflation disappears or is not substantial cross-family

  visual_size_to_mass_shortcut:
    state: PRE-S0
    priority: 2
    verified_artifact: VisPhysQuant 221 real objects; weight_kg + multiview paths; RGB-D archive public
    blocker: size-dependent signed/residual mass error not established on current open families
    next_action: real-object current-VLM G0; no MI
    kill_if: <2/3 families or no substantial size-error relation

  mass_cross_view_instability:
    state: HOLD-OPEN-MODEL-EXISTENCE
    priority: 2
    blocker: no sufficient modern item-level multi-family per-view result artifact
    next_action: same-object multiview deterministic G0 on >=3 current open VLM families
    kill_if: instability not broad and >=2/3-family

  ntsb_causal_relevance_vs_principal_selection:
    state: PRE-G0 / ARTIFACT-EXECUTION-BLOCKER
    priority: 2
    official_artifact: https://data.ntsb.gov/avdata
    avall_snapshot: 2026-08-01, 95636276 bytes
    blocker: MDB not yet downloaded/parsed in current environment
    next_action: download avall.zip in normal-network shell; audit findings C/F/cm_inPC; then G0
    kill_if: no broad mixed-role natural population or no relevance-vs-selection model dissociation

latest_terminal_log: rejected_candidates/continuation_terminal_addendum_6_2026-08-31.md
next_agent_prompt: phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md
```

Final discipline:

> **Inherit evidence, not attractive titles. Scientific object first, observable behavior/data second, novelty attack third, MI last. A mechanism is valuable when it changes what we think the computation is or predicts a decisive intervention—not merely when a probe decodes a label.**
