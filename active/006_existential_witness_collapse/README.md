# 006 — Existential Witness Collapse

Status: `READY-TO-SMOKE / HARNESS-READY-r4`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #4**.

```yaml
formal_n0_verdict: PASS
independent_auditor: GPT-5.6 Sol (fresh adversarial audit role)
d0_verdict: PASS
validation_authorized: true
```

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

A case counts only when the model first passes semantic forced-choice recognition for:

- a P witness exists;
- a Q witness exists;
- one shared witness is not established;
- distinct witnesses are not established.

It must also handle the explicit controls:

- `same_explicit` -> collapse action is justified;
- `distinct_explicit` -> collapse action is blocked.

The target error is then:

```text
recognition: identity is unresolved
controls:    same/distinct worlds handled correctly
use:         choose collapse_action in the unknown world anyway
```

This is `representation-correct -> illegal witness fusion`, not ordinary quantifier failure.

## r4 recognition contract

Recognition uses full semantic A/B alternatives, not Yes/No. A/B order is counterbalanced. Probe ids are retained for metric compatibility:

- `p_exists`
- `q_exists`
- `shared_entailment` = sameness is not established
- `identity_determined` = distinctness is not established

Recognition language is entity-general so the same contract can apply to people, organizations, clubs, or resources.

## Natural D0

D0 uses 40 real historical domestic-football Double source records from eight national settings. The real-source champion identity is kept in provenance but removed from the model-visible unknown record.

Source definition: a domestic Double requires **the same club** to win the top-tier league and primary domestic cup in the same season.

Source:
https://en.wikipedia.org/wiki/Double_(association_football)

Frozen assets:

- `N0_INDEPENDENT_AUDIT_2026-08-28.md`
- `D0_AUDIT.md`
- `data/frozen_d0_sources.jsonl`
- `data/build_frozen_d0.py`
- `data/source_manifest.md`
- `data/manual_audit_20.md`

Manual audit: `20 / 20 PASS`.

The deterministic builder must produce:

```text
sha256=6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0
```

## Matched conditions

- `unknown`: two existential winner facts; identities omitted;
- `paraphrase`: same information in a natural archival summary;
- `same_explicit`: same entity explicitly established;
- `distinct_explicit`: different entities explicitly established;
- `neutral_control`: extra same-season context with no identity information;
- `relation_reminder`: diagnostic only.

## Metrics

The scorer uses exact local A/B continuation log probability. No API and no LLM judge.

For a recognition/control-gated item:

```text
unknown_margin       = p_collapse(unknown) - 0.5
paraphrase_margin    = p_collapse(paraphrase) - 0.5
unknown_vs_distinct  = p_collapse(unknown) - p_collapse(distinct_explicit)
reminder_rescue      = p_collapse(unknown) - p_collapse(relation_reminder)
```

Promotion thresholds remain frozen in `configs/frozen_g0.json`.

## Hard kills / holds

- recognition floor -> `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`;
- enough gated cases preserve identity correctly -> `HARD-KILL-NO-ILLEGAL-JOIN`;
- paraphrase removes effect -> `HOLD-WORDING-ARTIFACT`;
- neutral context moves action comparably -> `HOLD-GENERIC-CONTEXT-ARTIFACT`;
- effect is concentrated in historically memorable season/country slices -> `HOLD-SOURCE-MEMORY-ARTIFACT`;
- exact N1 collision with the observed error destination -> KILL/ROUTE.

Do not lower thresholds, select favorable countries, switch to weaker models, or modify the phenotype after seeing smoke results.

## Authorized first shot

Only the frozen two-family smoke is authorized now:

```bash
cd active/006_existential_witness_collapse
python -m pip install -e '.[dev,run]'
pytest -q
python data/build_frozen_d0.py
existential-witness-run validate-data --data data/frozen_d0.jsonl
```

Then run exactly the planned Qwen3-8B and Gemma3-12B local models and summarize both with the frozen config. No N1, panel expansion, scaling curve, or mechanism work is authorized until the first-shot behavioral verdict is audited.
