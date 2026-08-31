# Hamdi-Style Topic Search — Current Handoff

Date: 2026-08-31  
Status: **AUTHORITATIVE CURRENT STATE — FRESH SEARCH RESET**

```yaml
CURRENT_FRESH_PASS_REGISTER: 0
CURRENT_FRESH_ACTIVE_TOPICS: 0
fresh_target: LLM mechanistic interpretability only
required_protocol: PAPER-SCALE v2
archived_reaudit:
  - 029_etr_human_like_fallacy
  - 030_spatial_reference_frame_transformation
  - 031_spontaneous_deception_knowledge_action
  - 032_temporal_forgetting_mechanism
  - 033_contextual_entrainment_opposite_scaling
latest_terminal_execution: 031 V3 reachability measurement gate failed
```

## Mandatory reads for next conversation

Only:

1. root [`README.md`](../README.md)
2. [`FINDING_RULES.md`](FINDING_RULES.md) — **must read in full; v2 adds PAPER-SCALE / F8**
3. this handoff

Then inspect `archive/029–033` only when a new idea semantically overlaps. Do not reread all old addenda by default.

## Why the previous 5/5 slate was revoked

031 exposed a selection failure, not merely an experimental null. The project moved through several different headline claims as gates failed:

```text
spontaneous deception
→ cross-query latent-belief validity
→ within-run graph-state corruption
```

V3 correctly stopped when held-out/polarity-invariant reachability measurement failed (best ridge AUROC 0.532; cross-polarity 0.538/0.530; recipient 0.465; 0 passing layers). But the deeper lesson is that the original question was too benchmark-dependent and did not have stable paper-scale identity.

Therefore the remaining slate was re-audited under a stricter standard rather than assumed valid by sunk cost.

## Re-audit verdicts

### 029 — Human-Like Fallacies

**ARCHIVE / SCALE + PROVENANCE.**

The ICLR mother is strong, but the proposed extension is caught between two bad scales:

- without ETR/PyETR specifics, `does behavioral similarity imply mechanistic similarity?` is too generic;
- with ETR/PyETR specifics, the paper becomes a narrow mechanistic verification of one cognitive theory on a synthetic generator.

The exact final 383-item exclusion manifest is also unavailable. Do not spend MI compute unless a future candidate supplies a broader independent scientific object.

### 030 — Spatial Reference Frames

**ARCHIVE / CURRENT TARGET MISMATCH, not scientific terminal kill.**

Reference-frame transformation is a legitimate broad question, but it is VLM. The next search is explicitly LLM-focused. Preserve provenance only.

### 031 — Spontaneous Deception / Graph State

**TERMINAL KILL / F8 + V3 measurement gate.**

Do not revive by changing probe/token position/subset or by returning to construct-validity framing. Canonical lesson: a runnable causal experiment does not imply a paper-scale question.

### 032 — Temporal Forgetting Mechanism

**ARCHIVE / SCALE.**

Temporal Forgetting is a broad ACL Main phenomenon, but our extension was primarily `which internal stage/circuit explains this mother phenomenon?`. The hypotheses (upstream erosion vs middle reasoning vs late readout vs distributed change) are mostly localization categories rather than an independently motivated scientific debate. This is too close to generic mechanistic follow-up under the new bar.

### 033 — Opposite-Scaling Contextual Entrainment

**ARCHIVE / DELTA-WIDTH + DATA.**

The behavior is real and broad, but ACL 2025 Outstanding already owns contextual entrainment mechanism, while Findings ACL 2026 already frames semantic filtering and mechanical copying as functionally distinct and explicitly suggests mechanistic decomposition. A writer/gate/two-circuit follow-up would mostly mechanize the mother’s interpretation/future work. Exact item-level mother data is also not released. Not enough novelty width for the current target.

## Next search protocol

The next agent must **not** start from `mother → mechanism gap` alone.

For every candidate, before dataset search or GPU, write a PAPER CARD containing:

1. one-sentence question with no dataset names;
2. independent scientific object;
3. why a non-benchmark reader should care;
4. comparison to at least 3 strong ACL/EMNLP/NAACL Main/Outstanding papers on topic scale;
5. exact conceptual delta from strongest prior work;
6. why this is not merely mechanizing a mother/future-work line;
7. whether dataset is natural or merely a controlled measurement window;
8. 2–3 competing hypotheses whose outcomes preserve the same headline question.

Hard kill if:

- removing benchmark name destroys the question;
- negative results would force changing the headline object;
- hypotheses are just early/middle/late localization;
- novelty is `behavior → mechanism` with no new theoretical object;
- synthetic dataset creates the central scientific distinction;
- current story needs post-hoc narrowing to sound broad.

## Venue-scale anchors

Use these as calibration, not as topic templates:

- ACL 2025 Outstanding — `Llama See, Llama Do`: broad new contextual entrainment phenomenon across models/settings → causal heads + mitigation.
- EMNLP 2025 Outstanding — filler-gap shared structure: mature linguistic theory question → causal LM evidence.
- NAACL 2025 — property inheritance: classic taxonomy vs similarity cognitive debate → behavioral + causal representational evidence.
- NAACL 2025 — `Racing Thoughts`: unified hypothesis for a class of contextualization errors → causal evidence + intervention.
- ACL 2026 Main — tool irrelevance: natural semantic relevance vs structural matching conflict → controlled dataset, competing pathways, mitigation.

## Current active state

No fresh 029–033 project remains active. `active/014_alias_entrainment_transfer` is separate established paper development; other legacy/HOLD directories do not count as fresh topics.

## One-line instruction for next agent

> **Find an LLM scientific question that would still deserve an ACL/EMNLP/NAACL paper if the benchmark name disappeared from the abstract; only then look for a mother, data, and MI method.**
