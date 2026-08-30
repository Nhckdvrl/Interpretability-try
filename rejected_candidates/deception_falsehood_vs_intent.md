# Rejected Candidate — Falsehood ≠ Deceptive Intent

**Status:** `KILL AT N1 / DO NOT REGISTER`  
**Death code:** `NARRATIVE_COLLISION / ANTI-NARROWING STOP`

## Natural question

> Saying something false and trying to deceive someone are not the same thing. Does an LLM represent deceptive communicative intent separately from proposition truth?

This initially looked strong because the conceptual distinction is natural:

- false statement without deceptive intent: error, fiction, role-play;
- deceptive false statement: lie;
- truthful statement without deception: ordinary truth;
- truthful statement used to intentionally mislead: non-lying deception.

It also appeared ideal for a Hamdi-style adjacent-axis project: `truth value ≠ communicative intent`.

## Why it was killed

N1 found that the 2025–2026 literature has moved beyond generic lie detection into the exact conceptual neighborhood:

- EMNLP 2025 representation work studies truthful vs deceptive instructions and representational flips;
- 2026 work explicitly tests the limits of lie-detector approaches on **deception without lying**, showing truth-oriented probes do not cover all deception;
- ICML 2026 targeted instruction-pair work explicitly motivates probes intended to capture **deceptive intent rather than content-specific patterns**;
- additional 2026 deception representation work studies internally detectable conflict/signatures.

The remaining space would have to be narrowed to a special listener-belief manipulation subtype, discourse form, or deception setting.

That violates the repository's anti-narrowing rule: if a broad natural title becomes novel only after adding several subtype qualifiers, the project is no longer an ACL/EMNLP-scale independent narrative.

## Nearest-neighbor warning

Do not revive as:

- misleading truth vs lie;
- truth probe vs deception probe;
- listener-belief manipulation;
- deception intent direction;
- lie-without-falsehood / paltering;
- role-play vs deception;
- another deception benchmark with SAE/patching.

These require a genuinely different scientific object, not another 2×2 surface realization of truth × intent.

## Resurrection condition

Only reopen if a future natural mother phenomenon reveals a **different communicative variable** that is not already captured by deceptive-intent probing and that yields a broad independent mechanism story with a decisive contrast not present in the current deception literature.
