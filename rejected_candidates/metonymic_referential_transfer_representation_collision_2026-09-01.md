# Rejection Record — Metonymic Referential Transfer Representation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

When an expression such as `The White House announced...` uses one entity to refer to a related entity or institution, does a language model internally shift from the literal denotation to the intended metonymic referent rather than merely exploiting lexical association?

## Semantic aliases

- literal vs metonymic reference
- referential transfer
- metonymic meaning shift
- building-for-institution / container-for-content representation
- semantic shift under metonymy

## Why it looked promising

Metonymy is pervasive, naturally understandable, and benchmark-independent. Modern datasets also provide human-annotated literal/metonymic examples and discourse-level coreference cases, so the project initially looked like a clean Route-C object with a causal interpretation path.

## Decisive kill evidence

The scientific object is already occupied at multiple levels:

1. **Pedinotti & Lenci, COLING 2020 — `Don't Invite BERT to Drink a Bottle: Modeling the Interpretation of Metonymies Using BERT and Distributional Representations`** explicitly asks whether contextual Transformer representations capture the **meaning shift associated with metonymic expressions**. Thus `metonymic semantic shift in internal representations` is not a new representational object.

2. **ConMeC, NAACL 2025 Long** provides 6,000 human-annotated common-noun sentences labeled literal vs metonymic and evaluates LLM metonymy resolution. The paper explicitly frames metonymic interpretation as identifying the intended related concept rather than the literal noun.

3. **`Not All Disneys Are the Same: Making Coreference Metonymy-Aware`, LREC 2026** moves the object to discourse-level reference. It annotates metonymic mentions in CoNLL-2012, shows LLM/coreference degradation on metonymic clusters, corrects clusters to semantic rather than surface reference, and introduces a metonymy-aware LLM procedure for semantic ambiguities introduced by metonymic shifts.

4. Logical-metonymy work has separately tested Transformer/LLM recovery of covert event content, further crowding a generic `literal input -> context-induced related meaning` mechanism claim.

Therefore a modern open-weight activation-patching/steering project on `White House -> institution` would mainly replace earlier contextual-representation and behavioral analyses with stronger mechanistic methods. The concept-level question is already owned.

## Strongest-neighbor warning

Do not revive as:

- metonymy direction;
- literal-to-metonymic steering;
- building-to-institution activation patching;
- semantic referent transfer circuit;
- local vs discourse metonymy hidden state;
- metonymic coreference mechanism.

Changing from BERT to Llama/Qwen, from detection to patching, or from sentence-level to a different metonymy dataset does not widen N2 enough.

## Death code

`F2 / N0-N2 — metonymic meaning shift and semantic-reference transfer are already direct computational/representational objects; remaining delta is stronger MI.`

## Resurrection condition

Only reconsider if a different independent scientific question is found inside metonymic processing that is not equivalent to detecting, resolving, or representing the literal-to-related referential shift and has its own theory-driven competing predictions.
