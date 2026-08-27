# Mental Simulations Become History — exploratory gate, not promoted

## One-sentence question

When a text describes an event, does the model keep separate **the event's content** from **whether that event actually occurred**?

Examples include an attack that was planned, a rescue that was attempted, an evacuation that was cancelled, a claim that was denied, and an outcome imagined counterfactually. These texts can describe an event richly without asserting that it happened.

## Why this is not 006

- The distinction is independently defined in linguistics and philosophy: event content versus event factuality/actuality.
- Labels come from natural documents and public human annotation, not from a task rule or a latent variable invented for the experiment.
- There is no privileged system message, advice source, authority hierarchy, or prompt-defined bridge.
- The same property is required in news, history, medicine, law, plans, and narratives.

The eventual mechanism could still turn out to have a representation/use split. That similarity in mechanism is acceptable; what made 006 weak was that both the latent state and its downstream use were artifacts of our interface.

## Public data

- MAVEN-Fact: 112,276 event mentions with certain/possible, positive/negative factuality labels and supporting evidence.
- FactBank, MEANTIME, UW, and UDS-IH2: established event factuality corpora.
- Natural cognitive-process narratives provide planned, imagined, intended, remembered, and perceived event complements.

## G0 results (2026-08-27)

Neutral prompt, one natural sentence, one highlighted event trigger, deterministic YES/NO/UNCERTAIN output; no system prompt.

| Model | Overall | Certain actual | Certain non-actual | Possible/uncertain |
|---|---:|---:|---:|---:|
| Qwen3-8B | 64.7 | 72 | 61 | 61 |
| Gemma3-12B | 75.3 | 81 | 67 | 78 |

These numbers are **not yet publishable evidence**. Some MAVEN-Fact labels rely on evidence outside the extracted sentence, and some local labels intentionally annotate the factuality of the mention rather than all document-level entailments. Direct negation and failed-attempt cues are often handled well. The raw error rate therefore overstates the phenomenon.

## Candidate phenotype worth testing

**Mental simulations become history:** after reading a natural narrative, models later report what a participant planned, expected, feared, imagined, or merely considered as part of what happened in the external timeline.

This is a source-monitoring failure at the event level. The content of a mental event is retained, but its source tag — externally realized versus internally simulated — is not reliably preserved when the narrative is reconstructed.

This is stronger and more natural than event-factuality classification. It predicts an asymmetric delayed-use error:

- factual event content remains available;
- non-actuality status is initially detectable;
- during later summarization, retrieval, or causal reasoning, the event content survives while the actuality tag is lost or bypassed.

## Frozen promotion gate

Promote only if all hold:

1. Document-level evidence removes annotation artifacts.
2. At least three model families and two sizes show the same directional error.
3. The error is selective for non-actual events; ordinary factual event memory remains high.
4. The effect survives neutral prompt paraphrases and does not depend on a system role.
5. A stronger model does not reduce the gap to a trivial level.
6. Literature search finds no white-box account of actuality-status loss during downstream reuse.

## Existing cross-scale behavioral support

CogNarr (Liu et al., 2026, DOI 10.1016/j.ipm.2026.105025) evaluates 20 models and reports persistent confusion between factual events and participants' cognitive processes across small and large models, including GPT-4.1, DeepSeek-v3, and Claude-3-Sonnet. Imagination recognition is substantially weaker than factual-event recognition. This occupies the broad behavior, but the paper does not provide a white-box account of how event content is separated from its mental/external source.

This external result is why the hypothesis is not expected to vanish merely by moving from an 8B to a frontier model. It is not evidence that our narrower downstream-reuse phenotype already holds; that still needs a clean G0.

## Mechanistic opening if promoted

- Decode actuality separately from event identity/content across layers.
- Compare the same event under factual, intended, denied, hypothetical, and counterfactual operators.
- Patch actuality-bearing states while preserving event content.
- Trace whether status is erased, overwritten, or simply not routed during later summary/answer generation.

## Current status

**EXPLORATORY / NOT PROMOTED.** Conceptually deep enough; behavioral evidence is not yet clean enough.
