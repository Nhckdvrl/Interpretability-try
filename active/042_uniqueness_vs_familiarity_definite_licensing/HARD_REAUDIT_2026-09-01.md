# 042 Hard Re-Audit — 2026-09-01

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED — PASSED AFTER FAMILIARITY CORRECTION**

## Frozen question

> When a definite description is licensed, does the model distinguish uniqueness from strong discourse familiarity as two different sources?

## Critical correction

The Srinivas–Rawlins–Heller 2×2 does **not** reduce familiarity to `entity appeared before vs did not appear before`.

Both potential referents are represented in the broader story. The relevant manipulation establishes **strong discourse familiarity** for the target through explicit interlocutor mention/re-mention before the critical definite.

Therefore the former generic `AntecedentRecallLogit` denominator was under-specified and has been replaced by:

```text
DialogueMentionFactLogit
EntityPresenceLogit
```

with mandatory recency/mention-count/salience controls.

## N0 / N1 / N2

- NAACL 2022 BERT article-system work owns abstract article prediction, not uniqueness × familiarity source factorization.
- Coreference/discourse models own use of uniqueness/salience/mention cues, not source-selective causal licensing while raw facts are preserved.
- Recent formal/experimental bridging work continues to separate uniqueness and familiarity but does not occupy the neural causal object.

Surviving N2:

> **source-specific internal licensing states for uniqueness and strong familiarity, with source-selective crossover and raw-source-fact preservation.**

## Strict locks

```yaml
Lock_A_orthogonal_2x2: PASS
Lock_B_cross_setting_abstraction: PASS
Lock_C_two_consequences: AVAILABLE
```

Critical cross:

```text
unique + not strongly familiar
vs
non-unique + strongly familiar
```

## Causal specificity

Uniqueness intervention must change licensing while preserving `CandidateStructureLogit`.

Strong-familiarity intervention must change licensing while preserving:

```text
DialogueMentionFactLogit
EntityPresenceLogit
```

If the effect is raw recency, mention count, salience or entity memory, terminate.

## Final verdict

```yaml
natural_object: PASS
human_2x2: PASS
familiarity_definition: CORRECTED
N0_N1_N2: PASS
strict_A: PASS
strict_B: PASS
specificity: PASS_WITH_HARD_KILLS
story_invariance: PASS
PASS_REGISTER: true
GPU_AUTHORIZED: true
```

042 remains registered under the stricter overlay.