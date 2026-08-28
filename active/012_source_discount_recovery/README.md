# 012 — Source-Discount Recovery

Status: `KILLED-COLLISION / DISCOVERY-STOPPED`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #9**.

```yaml
formal_n0_verdict: KILLED-COLLISION
independent_auditor: Codex independent audit 2026-08-29
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model retain the identity and credibility of a source and remember the source's message, yet progressively stop applying that credibility to the message's downstream weight?

The target contradiction is not ordinary forgetting:

```text
source identity after delay: correct
source credibility after delay: correct
message direction after delay: correct
but low-credibility message influence rebounds and the high-vs-low source discount shrinks
and re-presenting source metadata selectively restores the discount
```

This is a source-message binding/use question. A case is ineligible if source identity, message direction, or the credibility relation is no longer accessible.

## Normative evidence contract

The low-credibility source must still be positively informative. A below-chance/adversarial source can make discount or reversal normatively correct and therefore cannot instantiate this phenomenon.

Formal D0 stores externally audited directional likelihood ratios:

```text
1 < low_target_lr < high_target_lr
0 < high_other_lr < low_other_lr < 1
```

The visible calibration/profile text must correspond to those relations, and the same message content is paired with the high- and low-credibility source. Source identity may not be correlated with target/other content.

Before behavioral influence is interpreted, the model must itself pass answer-order-counterbalanced probes showing:

- the low-source message is still positive evidence for the focal hypothesis;
- the high-source message is positive evidence;
- the high-source version is more diagnostic;
- after both short and long delays, it remembers the message's source, direction, and relative source credibility.

## Delay and baseline design

`immediate`, `short`, and `long` conditions each have a matched no-message baseline. Message influence is always measured relative to the baseline at the same delay, preventing ordinary long-context drift from being mistaken for source recovery.

The long-delay signature requires all of the following:

1. an immediate high-vs-low discount gap exists on both belief and action;
2. low-source influence rebounds with distance;
3. the high-vs-low discount gap shrinks;
4. high-source influence remains substantially retained, so the gap did not shrink merely because the high-source message was forgotten;
5. source identity/credibility/message probes remain correct at both short and long delays.

## Source-cue reinstatement

After the long delay, the harness compares:

- the ordinary long condition;
- a source-metadata reinstatement that names the source and restores its audited credibility metadata without repeating the message;
- a semantically inert, approximately length-matched control reminder.

The source reminder must selectively increase the high-vs-low discount gap. A generic reminder or extra-token effect cannot satisfy the contract.

## Statistical unit and readouts

Each natural scenario contains target-supporting and other-supporting directions. Directional effects are sign-normalized so positive influence always means movement toward the hypothesis supported by the message. Both directions must satisfy the signature; they are not treated as independent samples.

Belief and consequential-action readouts are co-primary. Each has two wordings and counterbalanced A/B order. Bootstrap inference is over scenario-level bidirectional pairs.

## Hard kills / holds

- source/evidence relation not understood → `HARD-KILL-SOURCE-EVIDENCE-CAPABILITY-FLOOR`;
- source/message/credibility memory fails after delay → `HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR`;
- the model does not initially weight high-source evidence more than low-source evidence while using both in the correct direction → `HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR`;
- weighting capability is intact but discount does not recover → `HARD-KILL-NO-SOURCE-DISCOUNT-RECOVERY`;
- the high-source signal itself collapses or the no-message baseline drifts excessively → `HOLD-GENERIC-DELAY-DEGRADATION`;
- source reminder is not selectively stronger than the matched-length reminder → `HOLD-NO-SELECTIVE-SOURCE-CUE-REINSTATEMENT`.

## Execution gate

`configs/frozen_g0.json` has `validation_authorized: false`. `source-discount-run run` checks this before loading D0 data or constructing a model. Formal model calls require independent N0, external D0/license/gold resolution, the repository-required 20-item manual audit, and authoritative registry authorization.

Safe pre-authorization work:

```bash
cd active/012_source_discount_recovery
python -m pip install -e '.[dev]'
pytest -q
source-discount-run validate-data --data data/frozen_d0.jsonl
```

Synthetic test fixtures demonstrate the decision logic only and are not behavioral evidence.
