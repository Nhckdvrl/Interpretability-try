# Rejected Candidate — Superseded Truth ≠ Never-True Falsehood

**Date:** 2026-08-31  
**Verdict:** `KILL / DIRECT_MECHANISM_COLLISION / INTERNAL-FAMILY-INCLUSION`  
**Do not register under another stale/current-fact name.**

## Natural question

> A statement can be false now because it used to be true but became outdated, or false because it was never true. Does the model internally distinguish those cases?

Example:

- “Angela Merkel is Germany's chancellor” — historically true, currently false.
- “Angela Merkel is Japan's prime minister” — never true.

The natural question is strong. The candidate is rejected because the scientific object is already occupied, not because the question is uninteresting.

## Exact external collision

### The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations

2026 preprint: https://arxiv.org/abs/2605.09195

This work already establishes essentially the full intended contribution package:

1. defines temporal drift / temporal validity as a model-internal property;
2. shows a residual-stream drift direction independent of correctness and uncertainty;
3. evaluates six instruction-tuned model families;
4. reports direct drift probes with controlled AUROC 0.83–0.95;
5. explicitly separates **STALE-RECALL** from **CONFABULATION**;
6. reports a dedicated stale-recall-vs-confabulation probe with high AUROC;
7. uses entity-matched cross-cutoff, byte-identical inputs to isolate model-internal temporal state;
8. analyzes MLP retrieval dynamics;
9. performs causal steering of the drift direction.

The proposed “historically true but now false vs never true” contrast is therefore not an untouched adjacent axis. It is substantially the same scientific distinction as stale recall / temporal drift versus confabulation/non-drift falsehood.

## Why narrowing does not rescue it

The following renames remain inside the collision:

- superseded truth;
- former truth;
- stale knowledge;
- historical validity;
- current-validity tag;
- temporal truth axis;
- once-true vs never-true;
- outdated fact representation.

Changing from office holders to sports teams, CEOs, geographic facts, Wikidata revisions, edited knowledge or another model cutoff does not alter the scientific object.

## Internal-history attack

The repository already has substantial negative and adjacent knowledge around **history/current-state / state update**:

- generic correction/retraction and context-memory conflict are explicitly marked crowded in `rejected_candidates/factuality_information_conflict.md`;
- `candidate_topics` Topic 26 investigated historical temporal scope versus present-day pull/reinstatement and was stopped on artifact support, not because temporal context is a new untouched scientific domain;
- Topic 05 warns against rephrasing temporal retention/access questions when the observable does not create a genuinely new identifiable object.

Thus this candidate would also be absorbed by the repository's broad current-state/history family even without the direct 2026 external collision.

## Why this is stronger than ROUTE

`ROUTE` would be appropriate if prior work covered only the broader mother phenomenon and our question introduced a new decisive axis. Here the strongest neighbor already covers:

```text
title-level object: temporal validity/drift
decisive contrast: stale-recall vs non-stale/confabulation
representation: independent residual-stream axis
controls: correctness + uncertainty independence
causal story: cross-cutoff + MLP dynamics + steering
```

There is no main-paper-sized independent narrative left in the proposed formulation.

## Resurrection condition

Only reopen the temporal domain if a **different natural scientific object** is identified whose decisive contrast is not temporal validity itself and whose expected mechanism/intervention differs from the drift paper.

Do not resurrect because a new dataset provides cleaner dates or because a different factual relation is easier to query.

## Final death code

```yaml
natural_question: strong
novelty: failed
mother_inclusion: failed
external_collision: direct_mechanism_collision
internal_history: absorbed_by_state_update_family
register_active: false
```

Full three-candidate N0: [`../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md).
