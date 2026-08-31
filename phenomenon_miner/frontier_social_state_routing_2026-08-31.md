# Frontier — Implicit Social-State Recognition ≠ Accommodation Routing

Status: **PRE-S0 / NOT REGISTERED / NO MI AUTHORIZED**

Date: 2026-08-31

## Natural question

> Can a language model correctly read an interlocutor's implicit social state (especially relative power) yet fail to route that inference into an appropriate response strategy?

This is intentionally narrower and more falsifiable than generic `social intelligence`, `sociopragmatics`, or `LLMs fail to adapt socially`.

The candidate only exists if the **same current open model on the same natural interaction substrate** shows a real dissociation:

1. it can infer the relevant social state from implicit context; but
2. its generated reply fails to exhibit the externally established accommodation response associated with that state.

If recognition is also poor, this reduces to ordinary implicit-social-understanding failure and dies.

---

## Why it looked good

### Strong 2026 mother anomaly

ACL 2026 `Know Your Place: Diagnosing Implicit Social Adaptation Failures in Chinese Large Language Models` reports `Social Agnosia`: models respond strongly to explicit power/arousal/epistemic-status conditioning but produce much more homogenized responses when the same social state is only implicit.

Crucially, the paper describes `Social Agnosia` as a **behavioral descriptor rather than an internal-mechanism claim**. Its evaluated models generate replies; it does not independently test whether those same models correctly recognize the implicit P/A/K state before failing to adapt. The P/A/K inference used for data validation is performed by a separate validator before model evaluation.

Therefore the mother leaves open a sharp alternative:

- **reader failure**: the model never recovered the latent social state;
- **routing/writer failure**: the state was recovered but did not causally control the response policy.

That alternative is scientifically meaningful even with all MI vocabulary deleted.

### External human behavioral law exists before the LLM task

Communication Accommodation Theory provides a non-researcher-invented behavioral prediction. `Echoes of Power` reports cross-domain power/coordination regularities: lower-power speakers generally coordinate more, and speakers coordinate more toward higher-power interlocutors. Muir et al.'s controlled human communication work likewise reports increased linguistic-style accommodation in low-power roles.

This means the response-side variable does not need to be a new LLM-judge label invented for this project.

---

## Negative-memory audit

Do **not** collapse this into or resurrect:

- `social power ≠ status/prestige` — terminal `KILL-DATA / SECOND-AXIS-PROXY`;
- generic `implicit social understanding` / ToM benchmark work;
- generic `style vector`, politeness steering, persona control, or role prompting;
- `recognition ≠ recall`;
- `encoded ≠ reportable` without a natural downstream action variable;
- C-ISA itself as the S0 substrate, because its 4,000 evaluation instances are controlled rewrites rather than a natural-interaction existence substrate.

This frontier is specifically **implicit social-state inference → natural response-policy routing**.

---

## S0 substrate requirements

Synthetic-only existence evidence is forbidden.

Preferred substrate must contain authentic human interaction plus an external/non-LLM power variable and a pre-existing accommodation measure. Candidate sources under audit:

1. **Wikipedia / U.S. Supreme Court interaction corpora from `Echoes of Power`**
   - authentic goal-directed exchanges;
   - external status/dependence variables;
   - public linguistic-coordination definition and code are available through ConvoKit;
   - very large interaction counts in the original work.

2. **English Speed Networking Conversational Transcripts (LDC2016T16)**
   - 388 human transcripts;
   - experimentally assigned high/low/neutral power roles;
   - collected specifically to study power-conditioned accommodation;
   - useful as a confirmatory substrate, but access/licensing must be resolved before relying on row-level data.

3. **Enron power-relation annotations**
   - authentic email threads and organization structure;
   - useful for recognition, but only usable for the title-level dissociation if a response-side accommodation target can be grounded without hand-labeling.

### Frozen G0 logic

Use at least 3 genuinely different current interpretable open model families.

For each family, on the same held-out natural exchanges:

**Recognition task**
- infer relative power / status direction from interaction context without exposing the gold role label in the prompt;
- exact external role/status metadata is the gold;
- report accuracy / balanced accuracy with item-level outputs.

**Accommodation task**
- ask for the next reply in the conversational situation, without explicit role/style instruction;
- compute a preregistered linguistic-coordination statistic following the published human measure;
- test the direction of power-conditioned accommodation against the established human pattern, not against an LLM judge.

**Necessary dissociation for promotion**
- recognition must be clearly above a preregistered competence threshold;
- accommodation must remain substantially attenuated, absent, or reversed relative to the human power effect;
- the same qualitative dissociation must hold in >=2/3 open families;
- no post-hoc marker selection, corpus subtype rescue, or language switch.

Suggested preregistration threshold before observing model results:

```text
recognition balanced accuracy >= 0.70
AND
human-reference power→coordination effect replicates in the selected natural substrate
AND
model power→coordination effect <= 0.25 × human effect OR wrong sign
in >=2/3 current open families
```

Thresholds can be made stricter before first model run, but not relaxed afterward.

---

## N0 / N1 audit so far

### N0 mother inclusion

`Know Your Place` owns the broad behavioral object `implicit social adaptation failure` and the explicit-vs-implicit capability gap. It **does not currently establish the within-model recognition→accommodation dissociation**. Therefore the candidate is not yet killed by mother inclusion, but the title must remain about the dissociation rather than `Social Agnosia mechanisms`.

### N1 strongest-neighbor search

Current 2025–2026 search finds work on:

- implicit social-context understanding;
- social hierarchy/formality evaluation;
- style/persona vectors and controllable response style;
- communication accommodation behavior;
- social-order preferences;

but no exact paper yet found that demonstrates the same-model phenomenon `implicit power recognized correctly yet not used to control natural reply accommodation`, much less a direct mechanistic explanation of that routing gap.

This is **not an N1 pass yet**. Search must continue before registration.

---

## Anti-narrowing test

The candidate dies if it only works after choosing:

- one special hierarchy relation;
- one dialogue domain;
- a post-hoc politeness marker;
- one language;
- one weak checkpoint;
- explicit role labels;
- an LLM judge as the central accommodation gold.

A surviving version should support a broad statement:

> Current LMs can recover an implicit social relation that humans naturally use to regulate interaction, but fail to route that recovered relation into the corresponding response policy.

---

## MI fit — only if S0 and N1 survive

Competing mechanisms:

1. **Reader failure** — power/social state is not represented robustly from implicit context.
2. **Representation-without-routing** — state is decodable/causal upstream but disconnected from the response-policy writer.
3. **Generic safe/default writer dominance** — the social-state signal reaches generation but loses to a stronger homogenizing response prior.
4. **Explicit-instruction bypass** — explicit labels activate a separate instruction-following route rather than amplifying the ordinary social-state representation.

A Hamdi-level result would need to do more than localize `power`. The attractive outcome is a causal decomposition that predicts a simple intervention: e.g. activating an existing social-state→writer gate restores appropriate accommodation without explicit role prompting or broad style steering.

No probes, SAE, patching or steering are authorized before the behavioral dissociation and N1 survive.

---

## Current verdict

```yaml
status: PRE-S0
PASS_REGISTER: false
MI_authorized: false
promising_reason: strong_2026_mother_plus_external_human_behavioral_law
fatal_blockers:
  - current_open_model_same_input_recognition_vs_accommodation_G0_not_run
  - natural_row_level_substrate_not_yet_frozen
  - N1_exact_neighbor_audit_not_complete
```

**Do not count this toward the target five.**

### Immediate death condition

If current open models that fail to accommodate also fail implicit power recognition on the same natural inputs, write:

`KILL-S0 / NO-RECOGNITION-TO-ROUTING-DISSOCIATION`

### Resurrection restriction after death

Do not revive by switching language, adding explicit role labels, changing the style metric after seeing results, choosing only easy hierarchy examples, or replacing the natural corpus with C-ISA-like synthetic rewrites.
