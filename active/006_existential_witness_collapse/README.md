# 006 — Existential Witness Collapse

Status: `TERMINAL-KILLED / HARD-KILL-NO-ILLEGAL-JOIN`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #4**.

```yaml
formal_n0_verdict: PASS
independent_auditor: GPT-5.6 Sol (fresh adversarial audit role)
d0_verdict: PASS
behavioral_verdict: HARD-KILL-NO-ILLEGAL-JOIN
validation_authorized: false
```

See [`FINAL_VERDICT.md`](FINAL_VERDICT.md) for the terminal behavioral disposition.

## Mother question

Can a model correctly represent that two independent existential witnesses are not known to be identical, yet still operationally reuse them as one entity in a downstream action that requires a single shared witness?

```text
exists x: P(x)
exists y: Q(y)
-----------------
NOT ENTAILED: exists z: P(z) and Q(z)
```

The contract also does **not** assert that the witnesses are distinct. In the unknown world, both same-witness and distinct-witness worlds remain possible.

## Exact phenotype

A case counts only when the model passes semantic forced-choice recognition for:

- a P witness exists;
- a Q witness exists;
- one shared witness is not established;
- distinct witnesses are not established.

It must also handle the explicit controls:

- `same_explicit` -> collapse action is justified;
- `distinct_explicit` -> collapse action is blocked.

The target error was:

```text
recognition: identity is unresolved
controls:    same/distinct worlds handled correctly
use:         choose collapse_action in the unknown world anyway
```

This is `representation-correct -> illegal witness fusion`, not ordinary quantifier failure.

## Natural D0

D0 uses 40 real historical domestic-football Double source records from eight national settings. The real-source champion identity is kept in provenance but removed from the model-visible unknown record.

Source definition: a domestic Double requires **the same club** to win the top-tier league and primary domestic cup in the same season.

Frozen assets:

- `N0_INDEPENDENT_AUDIT_2026-08-28.md`
- `D0_AUDIT.md`
- `data/frozen_d0_sources.jsonl`
- `data/build_frozen_d0.py`
- `data/source_manifest.md`
- `data/manual_audit_20.md`

Manual audit: `20 / 20 PASS`.

Frozen D0 SHA256:

```text
6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0
```

## Frozen smoke result

Experiment commit: `aaf03c536e20b5cf83537c4f94a4e8a4476a0001`.

Qwen3-8B:

- recognition-gated: 40/40
- capability-gated: 40/40
- mean `p_collapse(unknown)`: `0.0000944`
- mean unknown margin: `-0.499906`
- bootstrap 95% CI: `[-0.499932, -0.499876]`
- strong cases: 0
- positive domains: 0/8
- verdict: `HARD-KILL-NO-ILLEGAL-JOIN`

Gemma3-12B:

- recognition-gated: 0/40
- downstream same/distinct controls handled correctly
- primary recognition failure was severe answer-order instability on the distinctness/identity probe
- harness verdict: `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`

No source-memory positive concentration was observed.

## Final disposition

The current frozen natural operationalization is terminally killed. Qwen3-8B cleanly passed the entire recognition/control denominator and overwhelmingly preserved identity uncertainty rather than illegally joining the witnesses. This directly satisfies the pre-registered hard-kill condition.

This does not prove that existential-witness conflation can never occur in any model or task. It means this discovery-track candidate failed its frozen natural first-shot test and must not be rescued by changing prompts, thresholds, datasets, model strength, or favorable slices.

No N1, panel expansion, scaling, or mechanism experiment is authorized.
