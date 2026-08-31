# Hamdi-Style Mechanistic Interpretability Topic Search — Authoritative Handoff

Date: 2026-08-31

Status: **AUTHORITATIVE NEXT-CHAT STATE / 0 PASS-REGISTER**

This file is the highest-priority state for the next conversation. If any old chat, `lead`, `HOLD`, `PRE-S0`, `PRE-CANDIDATE`, `survivor`, `under audit`, candidate note, or domain log conflicts with this file or the newest terminal addendum, **this file + the newest terminal addendum win**.

The goal remains up to five genuinely strong ACL / EMNLP / NAACL-style mechanistic-interpretability research topics. **Do not lower the bar to reach five.**

```yaml
PASS_REGISTER: 0
counts_toward_target_five: 0
MI_authorized_now: false
latest_terminal_addendum: rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md
```

**No candidate passes the current bar.**

---

# 1. Mandatory first read for the next conversation

Read in this order before doing any search or experiment:

1. `README.md`
2. `phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md` — this file
3. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-08-31.md`
4. `rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md` — newest terminal summary
5. `rejected_candidates/continuation_terminal_addendum_8_2026-08-31.md`
6. `rejected_candidates/continuation_terminal_addendum_7_2026-08-31.md`
7. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
8. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
9. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
10. `phenomenon_miner/FAILED_TOPICS.md`
11. `archive/README.md`
12. `rejected_candidates/README.md`
13. every rejection/domain file semantically close to a proposed new candidate

Do not rely on exact title matching. Search negative memory by scientific meaning and aliases.

---

# 2. Core search order — do not regress

The target is a **scientific object**, not an MI technique demo.

Required funnel:

```text
P0 natural question
→ semantic negative-memory audit
→ immediate strongest-neighbor/title collision attack
→ S0 real scientific substrate
→ current-open-model existence/capability
→ N0 mother-inclusion attack
→ N1 strongest-neighbor/successor attack
→ narrative width + anti-narrowing
→ MI fit + Hamdi surprise
→ PASS-REGISTER only after all gates
```

A serious topic should still sound interesting after deleting `dataset`, `benchmark`, `probe`, `SAE`, `feature`, `head`, `activation patching`, `steering`, and `circuit`.

Do not infer the question from a convenient dataset. Do not infer that a behavior exists because a mechanism story sounds elegant.

---

# 3. Negative-memory rule strengthened by the failed continuation

Before literature search for any new idea:

1. write the scientific object in one ordinary sentence;
2. generate 5–10 semantic aliases / nearest-neighbor formulations;
3. search `rejected_candidates/`, `archive/`, and `FAILED_TOPICS.md` for all of them;
4. if the same meaning is already terminal, stop unless the written resurrection condition is genuinely satisfied;
5. only then spend time on external literature or S0.

Changing model, dataset, language, prompt, subset, MI method, or adjective is **not** resurrection.

The final failed-conversation summary is:

- `rejected_candidates/continuation_terminal_addendum_9_2026-08-31.md`

Do not re-open any object listed there by synonym substitution.

---

# 4. What Hamdi-style quality means

The strongest examples follow:

```text
natural behavior
→ competing intuitive mechanisms
→ causal internal test
→ intuition is falsified or refined
→ mechanism predicts a simple/surprising intervention
```

The random-choice example is valuable because the intuitive `randomness dial` story was wrong: a switch/reader and a downstream writer/dial were separable, and the decomposition predicted a simpler intervention.

The entity knowledge/existence example is valuable because both axes already exist in the world and natural cross-cells exist independently of the model.

Therefore:

- do not manufacture a 2×2 first;
- do not start from `reader vs writer` vocabulary;
- the behavior or scientific distinction must force the mechanism question.

---

# 5. Current nonterminal execution frontiers

There are exactly four. **None is PASS-REGISTER.**

## A. Intervention Effect Direction ≠ Magnitude

Status:

```text
HOLD-FATAL-CONTROL / NOT REGISTERED / NO MI
```

Natural question:

> Can a model get the direction of an intervention effect right while systematically misjudging how large the effect is?

Why it remains interesting:

- strong 2026 real-human experimental substrate;
- many preregistered treatment effects;
- reported sign correspondence with systematic magnitude inflation;
- analyzable open-weight models appear in the broader result.

Fatal alternative:

`The Illusion of Intervention` shows intervention-induced user/persona drift. Treatment/control prompts may instantiate different latent respondent populations, making synthetic effect magnitude look inflated for the wrong reason.

Mandatory next step:

1. obtain the treatment-effect artifact/code;
2. obtain the user-drift artifact/code;
3. reproduce sign-correct/magnitude-inflated behavior on current interpretable open models;
4. implement the faithful drift/confounder correction;
5. residual disappears → `KILL-ARTIFACT` and write rejection;
6. only substantial residual across open families permits N1 and later MI.

No probes/SAEs/patching/steering before this control.

---

## B. Visual size → mass shortcut

Status:

```text
PRE-S0 / NOT REGISTERED / NO MI
```

Natural question:

> When a VLM estimates mass, does apparent/metric size systematically pull the estimate even after the object's true material/category information is accounted for?

Verified substrate facts:

- VisPhysQuant public `output.json`: 221 real objects;
- rows include true `weight_kg` and multi-view image paths;
- public Record3D RGB-D data exists;
- public code can compute metric image/view size from depth + intrinsics;
- there is no hidden precomputed modern per-view result artifact worth further searching for;
- `mass = volume × density/material` is already terminal and must not be revived.

Required G0:

- real objects only;
- same ordinary mass prompt;
- >=3 genuinely different current interpretable VLM families;
- save raw predictions;
- test whether apparent/metric size predicts signed/residual mass error under preregistered controls;
- broad >=2/3-family effect required;
- otherwise `KILL-S0`, no extreme-subset rescue.

---

## C. Mass-specific cross-view instability

Status:

```text
HOLD-OPEN-MODEL-EXISTENCE / NOT REGISTERED / NO MI
```

Natural question:

> If an object's mass is physically invariant, why can a VLM's mass estimate change strongly when only the camera view changes?

This is allowed to remain alive only as a **latent physical-property constancy** object. Generic perceptual constancy is already terminal.

Required G0:

- same real objects;
- >=4 views per object;
- identical prompt;
- deterministic decoding;
- >=3 current interpretable VLM families;
- quantify within-object log-mass dispersion;
- stable identity/category recognition control;
- image resize/crop and same-view rerun controls;
- broad >=2/3-family effect required or `KILL-S0`.

---

## D. NTSB causal relevance ≠ causal-role selection

Status:

```text
REGISTERED-FRONTIER / DELEGATED-G0 / NOT PASS-REGISTER / NO MI
```

This frontier is registered only for execution tracking and **does not count toward the target five**.

Correct scientific question:

> In a real accident, can a model correctly recognize which findings are causally relevant while still failing to distinguish findings investigators classify as causes from findings they classify as contributing factors?

Critical semantic correction:

```text
cm_inPC = finding was cited in the probable-cause statement as a cause OR contributing factor
legacy cause_factor = C vs F role distinction
```

Never use `cm_inPC=TRUE` as `principal cause` gold. Do not assume one unique cause per event. Use `cause vs contributing factor` / `causal-role selection`, not `one true root cause`.

The authoritative local execution files are:

1. `phenomenon_miner/REGISTERED_FRONTIER_NTSB_CAUSAL_ROLE_2026-08-31.md`
2. `phenomenon_miner/NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md`
3. `phenomenon_miner/NTSB_LOCAL_AGENT_PROMPT_2026-08-31.md`

The local agent must:

1. download official `avall.zip`;
2. parse MDB tables;
3. audit `cause_factor`, `cm_inPC`, years, missingness;
4. count mixed C/F events;
5. pass the preregistered natural-population threshold;
6. random-20 semantic/leakage audit;
7. freeze the sample/prompts;
8. run >=3 current open model families;
9. test causal relevance vs C/F role selection;
10. write `KILL-DATA`/`KILL-S0` immediately if gates fail.

No MI is authorized before that.

---

# 6. Topics killed in the final continuation — do not re-propose

The canonical full details are in Addendum 9. In shorthand, the following scientific objects are terminal:

- affective validation / emotional support ≠ epistemic endorsement;
- feedback/update direction ≠ correction magnitude / step size;
- social-cue recognition ≠ accommodation / socially appropriate action;
- population mean / aggregate fit ≠ heterogeneity / dispersion / correlation structure;
- object identity ≠ state-dependent affordance / actionability;
- stated preference ≠ revealed preference / actual choice;
- study-design/evidence-boundary recognition ≠ causal-claim generation;
- likelihood/probability ≠ desirability/valence;
- geographic metric distance/reality ≠ semantic/cultural/landmark salience.

Older terminal families in Addenda 2–8 and domain logs remain dead as well, including mass volume×density, generic perceptual constancy, belief-update gate/dial, popularity/quality, truth/belief, assertion/presupposition, prevalence/diagnosticity, statistical significance/effect size, recognition/recall, what/where, ratio bias, preference transitivity, anchoring, legal authority, privacy knowledge/action, and other logged objects.

Do not revive them by swapping nouns.

---

# 7. Search strategy for genuinely new mother families

Do not spend most of the next round re-checking the four frontiers. Continue systematic search for new scientific objects.

Priority sources:

- ACL / Findings ACL
- EMNLP / Findings EMNLP
- NAACL
- TACL / Computational Linguistics
- ICLR / ICML / NeurIPS
- Nature / Nature Machine Intelligence / Nature Computational Science
- strong 2025–2026 behavioral/cognitive papers with open models or reproducible artifacts

Most promising pattern:

> a strong paper contains a stable, counterintuitive residual anomaly in a table/ablation, but the paper does **not** name that anomaly as its headline scientific object and does not already perform the obvious MI successor.

Prefer:

- everyday deterministic/distributional failures visible under ordinary prompts;
- external-world grounded distinctions with deterministic/expert/human gold;
- broad current-open-model behavior;
- natural units and natural cross-cells;
- row-level artifact availability;
- an intuitive mechanism that a causal analysis could plausibly overturn.

Avoid obvious named distinctions whose titles can already be found in 2025–2026 papers.

---

# 8. Registration requirements

## Failure-mechanism candidate

Before PASS-REGISTER:

- behavior exists on current analyzable open checkpoints;
- default >=2/3 model families same qualitative direction;
- ordinary faithful prompt;
- no synthetic-only existence evidence;
- no post-hoc subset rescue;
- effect is scientifically substantial;
- item-level outputs/scorer/checkpoint revisions saved;
- N0/N1 pass;
- anti-narrowing pass;
- MI fork produces genuinely competing causal mechanisms and a potential surprising intervention.

## Factorization/internal-object candidate

Before PASS-REGISTER:

- axes independently defined outside the model;
- independent external/expert/human/deterministic gold;
- row-level artifact actually obtained and parsed;
- natural cross-cells counted;
- random-20 audit saved;
- attrition/restriction budget explicit;
- no researcher-created core labels;
- no LLM-judge central gold;
- no proxy second axis;
- no synthetic 2×2 manufactured to make the title true;
- N0/N1 and anti-narrowing pass.

---

# 9. Logging rule

Every seriously audited death must immediately be written to `rejected_candidates/` with:

- Natural question
- Why it looked good
- Kill evidence
- Death code
- Nearest-neighbor warning
- Resurrection condition

Also update the newest continuation addendum when a death is important enough to prevent semantic resurrection.

Do not leave negative knowledge only in chat.

---

# 10. Final instruction to the next agent

Do not start from MI vocabulary. Do not count frontiers as results. Do not lower the gate.

If nothing survives:

`No candidate passes the current bar.`

Then continue into **new mother families**, rather than renaming old dead objects.
