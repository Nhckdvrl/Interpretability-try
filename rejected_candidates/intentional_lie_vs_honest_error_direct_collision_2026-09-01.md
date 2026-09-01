# Rejection — Intentional Lie vs Honest Error

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

When a model says something false, is it internally different when it **knows the truth and lies** versus when it is **simply mistaken**?

## Semantic aliases

- deception vs honest error
- lie vs hallucination
- known-false output vs mistaken output
- intentional/strategic deception vs wrongness

## Why it looked promising

This is an exceptionally strong Route-C question in isolation: a false answer alone does not tell us whether the system is deceptive or merely wrong, and the output can be exactly matched while the latent epistemic situation differs.

## Decisive kill evidence

Nyoma, **“Rift: A Conflict Signature for Deception in Language Models”** (arXiv:2606.17229, June 2026) already asks the exact internal question: whether a model that lies while knowing the truth has a measurable internal signature that distinguishes it from honest error.

Its key control explicitly matches wrong outputs between a deceptive model and a naive liar / honest-error-like control, and reports a residual-rank conflict signature across Qwen2.5 and Phi-3 family models, including separation from hallucinations and cross-family transfer.

Sources:

- https://arxiv.org/abs/2606.17229
- https://github.com/Omibranch/Rift

This is not merely behavioral ownership; it is already **internal-representation / mechanistic occupancy of the exact natural contrast**. Any new activation patching, SAE, steering or alternative detector would be method-level delta unless it introduced a new scientific object.

## Strongest-neighbor warning

Do not revive as:

- deception vs hallucination direction;
- lie detector from activations;
- knowledge-conflict signature;
- deceptive-vs-mistaken residual geometry;
- cross-model deception representation;
- steering or patching the RIFT contrast.

## Death code

`F2 / N0-N1-N2 — exact 2026 internal-object and representation collision.`

## Resurrection condition

Only reconsider if the question moves to a genuinely different natural property of deception not already equivalent to `knows truth but misleads vs is simply wrong`, and that property has independent scientific value.
