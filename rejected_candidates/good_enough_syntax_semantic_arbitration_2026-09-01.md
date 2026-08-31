# Rejection — Good-Enough Syntax–Semantic Arbitration

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- good-enough syntax–semantic arbitration
- structure-sensitive computation vs semantic shortcut
- plausibility-vs-syntax processing regime
- complexity-triggered semantic shortcut
- structural analysis vs semantic pattern matching
- processing-regime switching under syntactic difficulty
- semantic plausibility takeover under center embedding

## Natural question considered

> When syntax and semantic plausibility conflict, do LLMs continuously arbitrate between structure-sensitive and plausibility-based evidence, or does increasing processing difficulty trigger a shift from structural computation to a semantic shortcut?

The question is paper-scale in isolation, but it fails the strongest-neighbor novelty gate.

## Decisive kill evidence

The EACL 2026 Main mother paper **already owns the headline interpretation**, rather than merely reporting a behavior that leaves this theory-level question open:

- Madhusudan, Chen & Emami, *The Dog the Cat Chased Stumped the Model: Measuring When Language Models Abandon Structure for Shortcuts* (EACL 2026 Main): https://aclanthology.org/2026.eacl-long.19/
- The title itself states that the paper measures when models **abandon structure for shortcuts**.
- The abstract says the plausibility gap widens with complexity and explicitly interprets this as quantifying when models abandon structural analysis for semantic associations; it calls CenterBench the first framework to identify when models shift from structural analysis to pattern matching.
- The Introduction says the matched plausibility × complexity design is intended to quantify exactly **when and how models transition from structural analysis to semantic shortcuts**.
- Related-work framing connects the effect to human good-enough processing and positions CenterBench as identifying a continuous transition from structural analysis to semantic shortcuts.
- The Conclusion again claims the benchmark reveals precisely when and how models abandon structural analysis for semantic shortcuts.

Therefore the proposed headline

> `complexity rises -> structure-sensitive computation gives way to semantic shortcut / processing-regime shift`

is already the mother paper's central scientific object and interpretation.

## N0 / N1 / N2 audit

```yaml
N0_object_ownership: FAIL
reason: mother explicitly owns structure-vs-semantic-shortcut transition as its headline object

N1_causal_occupancy: not_needed_for_kill
reason: even if no activation-patching paper exists, adding MI would be behavior -> mechanism on an already-owned axis

N2_delta_width: FAIL
reason: the remaining delta is principally internal implementation/localization of the mother's claimed transition, not a new concept-level scientific question
```

## Why this cannot be rescued by MI

A paper described naturally as

> `CenterBench found that models shift from structural processing to semantic shortcuts as complexity rises; we investigate the internal mechanism of that shift.`

is exactly the forbidden mother-behavior -> mechanism pattern under the current PAPER-SCALE / Novelty-step / F8 rules. Calling the internal dynamics `arbitration`, `competition`, `gating`, or `regime selection` does not widen the scientific delta enough because the mother already frames the behavioral axis as a transition between the same two processing modes.

Do **not** revive by changing:

- CenterBench subset or question type;
- model family;
- language;
- probe / SAE / patching method;
- token position or layer;
- terminology (`good-enough`, `arbitration`, `semantic takeover`, `gating`, `race`, `regime shift`).

## Nearest-neighbor warning

Also nearby:

- Cong & Rayz (2025), *Language models demonstrate the good-enough processing seen in humans* — explicitly frames LMs through good-enough processing on comparative illusions.
- Lee & Shin (2026), *Probing Good-Enough Processing in Large Language Models with a Paraphrasing Task* — directly studies whether LLMs exhibit human-like good-enough syntactic comprehension.

These reinforce that `LLMs use good-enough processing` is itself not a fresh broad axis.

## Resurrection condition

Only reconsider if a **different independent scientific axis** is found that:

1. exists in psycholinguistic theory independently of CenterBench;
2. is not equivalent to structure-vs-semantic shortcut or complexity-triggered switching;
3. has natural theory-defined cross-cells already present in an executable substrate;
4. is not claimed or implied as the mother paper's main interpretation/future-work mechanism;
5. yields a concept-level N2 delta that remains paper-scale without mentioning CenterBench.

Absent that, this route is terminal for the current fresh search.
