# Rejection — Use vs Mention / Asserted vs Quoted

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

When language contains the same proposition or harmful expression, does a model distinguish **using/asserting it** from merely **mentioning/quoting it**?

## Semantic aliases

- use vs mention
- asserted vs quoted
- endorsement vs quotation
- content commitment vs metalinguistic mention

## Why it looked promising

This is an unusually clean Route-C object: ordinary speakers understand the difference immediately, the lexical content can be held fixed, and the distinction matters for factuality, moderation, dialogue and attribution. A causal question would have been whether a context-general use/mention state is actually used downstream rather than merely decodable.

## Decisive kill evidence

Gligoric, Cheng, Zheng, Durmus & Jurafsky, **“NLP Systems That Can't Tell Use from Mention Censor Counterspeech, but Teaching the Distinction Helps”** (2024, arXiv:2404.01651) already owns the central scientific object in language models: systems confuse use with mention, this causes downstream content-moderation failures, and explicitly teaching/prompting the distinction mitigates them.

The remaining move — find an internal direction/circuit and causally steer it — is primarily **behavior/object -> mechanism** on the same conceptual distinction. Under `FINDING_RULES.md` N2, a stronger MI method is not enough concept-level delta.

Source: https://arxiv.org/abs/2404.01651

## Strongest-neighbor warning

Do not revive this as:

- quotation vs assertion representation;
- quoted misinformation vs endorsed misinformation;
- counterspeech vs hate-speech mechanism;
- a use/mention SAE feature;
- activation patching of quotation marks.

Those are method/domain variants of the occupied object unless a genuinely orthogonal semantic axis is found.

## Death code

`F2 / N0-N2 — strongest neighbor owns the natural distinction; proposed delta collapses to mechanization.`

## Resurrection condition

Only reconsider if a new question introduces an independent natural property that is not equivalent to use/mention, and that property remains paper-scale after the 2024 paper is removed.
