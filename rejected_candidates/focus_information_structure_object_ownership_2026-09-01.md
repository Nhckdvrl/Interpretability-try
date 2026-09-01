# Rejection — focus/background / information-structural focus

Date: 2026-09-01  
Verdict: **KILL-NOVELTY under STRICT_EXTENSION_GATE**

## Natural question

Does a language model maintain which constituent is currently in discourse focus / answers the Question Under Discussion, separately from background information?

## Semantic aliases

- focus vs background
- information structure
- discourse focus
- contextual focus
- Question Under Discussion / QUD
- focused constituent
- lexical vs contextual focus
- focus maintenance
- focus representation
- discourse-new / discourse-relevant constituent

## Why promising

Focus is a mature linguistic object with natural QUD manipulations and broad downstream consequences. It initially looked like a clean Route-C / theory-driven topic.

## Decisive kill evidence

Chung & Koo (PLOS ONE 2026), `Focus shifts in contextual and lexical cue interactions in GPT models`, directly studies GPT-2 family and GPT-Neo while manipulating:

- contextual focus through preceding who/what questions;
- lexical focus through `only`;
- cases where these cues agree or compete;
- downstream ellipsis/remnant surprisal.

The authors explicitly conclude that the tested models maintain discourse-level focus representations while integrating contextual and lexical focus cues.

This is object-level ownership, not merely a neighboring benchmark.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC13278579/

## Strongest-neighbor warning

A new modern-open-LM patching/SAE study of the same focus object would largely be:

```text
already-owned focus phenomenon/object
+ newer backbone
+ stronger MI
```

That fails the stricter post-5/5 standard.

## Death code

`KILL-NOVELTY / N0-N2 OBJECT OWNED`

## Resurrection condition

Only reopen with a genuinely orthogonal scientific axis that the focus paper does not already manipulate, plus a separate causal consequence. `Where is focus encoded?` is not a resurrection.

## Do not revive by

- Qwen/Llama instead of GPT-2;
- activation patching;
- SAE features;
- different focus benchmark;
- different language;
- focus vs background probe;
- rebranding QUD focus as discourse salience.
