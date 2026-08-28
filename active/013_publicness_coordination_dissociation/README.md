# 013 — Publicness–Coordination Dissociation

Status: `ACTIVE-PREFLIGHT / N0-PASS / D0-HOLD / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #3**.

```yaml
formal_n0_verdict: PASS
independent_auditor: Codex independent audit 2026-08-29
d0_verdict: HOLD
validation_authorized: false
```

## Mother question

When every participant has the same first-order fact, can a model correctly recognize the higher-order epistemic consequences of a public event yet fail to use that publicness when choosing a coordination action?

The target contrast is:

```text
same proposition
same recipients
both participants know the proposition
private separate receipt  <->  mutually observable public announcement
model correctly reports the public event's higher-order receipt knowledge
but natural publicness changes coordination policy far less than an explicit-common-knowledge bridge
```

This is not a generic "LLMs fail common knowledge" task. If the model cannot infer the public event's higher-order consequences, the candidate is at a ToM/public-announcement capability floor and cannot count as the target dissociation.

## D0 contract

Formal D0 must come from an externally anchored coordination/common-knowledge task or published experimental material. It must independently establish:

- identical proposition and recipients across private/public conditions;
- both participants actually receive and know the proposition in both conditions;
- separate private receipts are not mutually observable and do not generate common knowledge;
- the public event is mutually observable and, under the task's information structure, licenses the relevant common-knowledge operator;
- the task payoff/protocol independently predicts more coordination under public/common knowledge than separate private receipt;
- participant roles and action payoffs are symmetric enough for a participant-swap control;
- paraphrase and length-control versions preserve the same information relation.

`policy_gold_text` is audit metadata only. It is deliberately absent from every model-visible prompt. Putting the policy rationale into the prompt would turn the experiment into explicit rule following and invalidate the scientific question.

## Capability gate

For both participant perspectives and both answer orders, the model must correctly establish:

- self knows the proposition;
- the other participant also knows it in the described world;
- whether the information event was mutually observable;
- whether the participant can know that the other received the proposition;
- whether the participant can know that the other knows that self received it;
- one additional recursive receipt-knowledge level.

These probes separate publicness representation from downstream policy use.

## Explicit common-knowledge bridge

Each scenario has three matched states:

1. `private`: same first-order fact delivered separately and privately;
2. `public`: the natural public event that should generate the relevant higher-order epistemic state;
3. `explicit_ck`: the epistemic consequence is stated explicitly, without stating what action to take.

For each participant:

```text
ck_gain     = P(coordinate | explicit_ck) - P(coordinate | private)
public_gain = P(coordinate | public)      - P(coordinate | private)
dissociation = ck_gain - public_gain
```

A target case requires a substantial `ck_gain` (proving the action interface can use the state) while `public_gain` realizes only a small fraction of it, despite the publicness/recursive-knowledge capability probes being correct.

## Surface controls

The primary private/public/explicit-CK triplet is repeated with:

- independently audited natural paraphrases;
- approximately length-matched versions preserving the same epistemic structure.

Every control uses its own matched private/public/explicit-CK triplet. This prevents a different private baseline or a longer explicit bridge from creating a false dissociation.

Both participants must show the effect; scenario-level inference treats the participant pair as one statistical unit. Two action wordings and both A/B orders are retained as within-case robustness checks.

## Hard kills / holds

- public/private first-order or recursive epistemic structure is not understood → `HARD-KILL-PUBLICNESS-TOM-CAPABILITY-FLOOR`;
- explicit common knowledge does not change the coordination policy → `HARD-KILL-COORDINATION-POLICY-CAPABILITY-FLOOR`;
- natural publicness is used almost as strongly as the explicit-CK bridge → `HARD-KILL-NO-PUBLICNESS-COORDINATION-DISSOCIATION`;
- the signature disappears under paraphrase or matched-length controls → `HOLD-WORDING-OR-LENGTH-ARTIFACT`;
- the apparent effect is materially specific to one participant role → `HOLD-PARTICIPANT-ASYMMETRY`.

## Execution gate

`configs/frozen_g0.json` has `validation_authorized: false`. `publicness-coordination-run run` checks authorization before data/model construction. Formal model calls require independent N0, an external D0 with license/gold resolution, the required 20-item manual audit, and an authoritative registry update.

Safe pre-authorization work:

```bash
cd active/013_publicness_coordination_dissociation
python -m pip install -e '.[dev]'
pytest -q
publicness-coordination-run validate-data --data data/frozen_d0.jsonl
```

Synthetic test fixtures are only logic tests and do not count as evidence for the phenomenon.
