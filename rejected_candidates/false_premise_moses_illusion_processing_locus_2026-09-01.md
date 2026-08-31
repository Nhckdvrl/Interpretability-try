# Rejection — False-Premise / Moses-Illusion Processing Locus

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- Moses illusion in LLMs
- false-premise hallucination
- imperfect encoding vs retrieval vs partial match
- premise blindness
- false-presupposition acceptance
- latent knowledge overridden by misleading premise
- semantic illusion processing locus

## Natural question considered

> When an LLM accepts a subtly false premise despite knowing the relevant fact, is the premise encoded inaccurately, is correct knowledge not retrieved, or does a partial semantic match allow an almost-correct premise to pass verification?

The question has an unusually clean cognitive lineage: classic Moses-illusion work explicitly debated encoding, retrieval, and partial-match accounts. However, recent LLM work already occupies the causal false-premise / knowledge-override mechanism space too directly.

## Decisive kill evidence

### Direct LLM causal collision

**EMNLP 2024 Main — `Whispers that Shake Foundations: Analyzing and Mitigating False Premise Hallucinations in Large Language Models`** does not merely report false-premise behavior. It explicitly studies the internal mechanism and identifies a small subset of **false-premise heads** whose activity disrupts knowledge extraction; constraining roughly 1% of heads substantially improves robustness.

Recent 2026 sycophancy / premise-override work goes further with causal activation patching and logit-lens analyses showing how correct internal knowledge can be overridden or erased under conflicting contextual claims/authority. Thus `knowledge present but false premise wins` is already a heavily mechanized object.

### Behavior/data do not create a fresh delta

Modern public false-premise resources are strong — e.g. KG-FPQ and public false-premise/sycophancy response collections include Llama, Mistral and Qwen families — but that only makes the existing object easier to measure. It does not widen the novelty delta.

## N0 / N1 / N2 audit

```yaml
N0_object_ownership: crowded
reason: false-premise hallucination / known-fact override is already an explicit LLM research object

N1_causal_occupancy: FAIL
reason: EMNLP 2024 already identifies causal false-premise heads disrupting knowledge extraction; later causal sycophancy work studies knowledge override

N2_delta_width: FAIL
reason: reframing the internal failure as encoding-vs-retrieval-vs-match would chiefly refine an already mechanized premise-override phenomenon rather than establish a clearly independent LLM scientific question
```

## Nearest-neighbor warning

Future searches involving any of the following should treat this route as occupied unless the scientific object is genuinely different:

- false premise hallucination;
- latent knowledge vs context override;
- sycophancy under incorrect user claims;
- authority-induced erasure/override;
- premise verification heads/circuits.

## Do not revive by

- switching from KG-FPQ to Moses-illusion questions;
- using a different open model;
- renaming `false-premise heads` as a verification gate;
- probing an earlier token/layer;
- replacing activation patching with SAE, probing, or path patching;
- focusing on one confusability level.

## Resurrection condition

Only reconsider if a **separate, theory-level semantic-illusion object** is found whose diagnostic manipulation cannot be reduced to false-premise knowledge extraction / context override, with established modern open-model behavior and an unoccupied causal factorization.
