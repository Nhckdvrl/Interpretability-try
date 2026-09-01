# Rejection — Habitual/Dispositional vs Episodic Event Representation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a language model distinguish what someone **habitually/typically does** from what they are **doing in one particular episode**? `Mary smokes` need not mean Mary is smoking now, and `Mary is smoking now` need not make her a habitual smoker.

## Semantic aliases

- habitual vs episodic
- disposition/generalization vs current event
- regularity vs particular occurrence
- habitual aspect

## Why it looked promising

The distinction is natural, theoretically mature, and supported by public annotated corpora. It has clear downstream consequences because habitual statements tolerate exceptions whereas episodic statements refer to particular events.

## Decisive kill evidence

The exact scientific object has already been studied in language-model representations. TACL 2019 `Decomposing Generalization: Models of Generic, Habitual, and Episodic Statements` explicitly decomposes generic, habitual, and episodic readings into real-valued semantic properties, constructs a corpus covering the English Web Treebank, and probes contextual ELMo representations for those properties. SitEnt/DiSCo-style annotation likewise treats boundedness/habituality as a dedicated semantic attribute with episodic versus habitual values.

Thus the contribution `modern Qwen/Llama distinguish habitual from episodic internally and causal steering changes use` would primarily update the model generation and MI strength while keeping the already-owned representation object.

## Strongest-neighbor warning

Do not revive as habituality vector, disposition-vs-episode steering, simple-present-vs-progressive patching, or exception-tolerance circuit.

## Death code

`F2 / N0-N2 — direct contextual-language-model representation ownership of habitual versus episodic generalization.`

## Resurrection condition

Only a distinct event/generalization property not equivalent to habituality, genericity, or episodicity could reopen this area.