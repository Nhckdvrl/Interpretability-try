# Rejection — deontic permission vs dynamic ability modal sense

Date: 2026-09-01  
Verdict: **KILL-NOVELTY under STRICT_EXTENSION_GATE**

## Natural question

When the same modal such as `can` is used, does the model distinguish permission granted by a norm/authority from ability/capacity of the subject?

## Semantic aliases

- permission vs ability
- deontic vs dynamic modality
- modal verb sense
- can permission vs can ability
- normative possibility vs capacity
- authority-licensed action vs capability
- root modal sense
- modality type

## Why promising

The distinction is natural, cross-linguistic and can be expressed with the same surface modal word, apparently giving an attractive same-lexical contrast.

## Decisive kill evidence

Modal-sense classification is already an established computational object. Earlier datasets explicitly label epistemic, deontic/bouletic and dynamic/ability senses.

Most importantly, Wagner & Zarrieß (IWCS 2023), `Probing BERT’s ability to encode sentence modality and modal verb sense across varieties of English`, directly probes contextualized BERT representations for distinct modal senses and reports sense-specific representations for individual modal verbs, while asking whether an abstract modal-sense representation exists independently of the verb.

Source: https://aclanthology.org/2023.iwcs-1.3/

This already owns the exact representation-level scientific object strongly enough that `modern autoregressive LLM + causal direction` is method/backbone novelty unless a genuinely new semantic object is added.

## Strongest-neighbor warning

The fact that the 2023 paper finds weak verb-independent abstraction is **not** a free novelty slot. Simply testing whether Qwen/Llama has a more abstract permission-vs-ability state is a model-generation upgrade of an already asked question.

## Death code

`KILL-NOVELTY / N0-N2 OBJECT OWNED`

## Resurrection condition

Only reopen with an orthogonal modal-theory factor that prior modal-sense work does not already ask, with independent cross-cells and downstream causal consequences. A stronger probe/steering method is insufficient.

## Do not revive by

- replacing BERT with Llama/Qwen;
- doing activation patching or SAE;
- restricting to `can`;
- changing English variety/language;
- calling the direction `permission state`;
- using agent/tool permission scenarios without a new scientific factorization.
