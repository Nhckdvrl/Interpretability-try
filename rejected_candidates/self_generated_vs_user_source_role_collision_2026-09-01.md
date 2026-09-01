# Rejection — Self-Generated vs User-Provided Source Role

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

If exactly the same text appears in a conversation, does the model represent it differently depending on whether it previously said the text itself or the user supplied it?

## Semantic aliases

- self-authorship
- self-generated text recognition
- assistant vs user source role
- self-source bias
- source-aware context use

## Why it looked promising

This was a simple omitted-axis extension from contextual entrainment: token/content identity can be held fixed while source role changes, and source could plausibly affect later reuse or trust.

## Decisive kill evidence

ICLR 2025 `Inspection and Control of Self-Generated-Text Recognition Ability in Llama3-8b-Instruct` directly studies self-authorship recognition, identifies a residual-stream vector associated with perceived self-authorship, and causally steers that attribution. 2026 `Self-Generated Text Recognition: Quality Heuristics, Cross-Task Transfer, and Downstream Bias in LLM Evaluation` further studies conversation structure, including user-versus-assistant role placement, self-recognition, and downstream self-preference across many models.

Thus the core source-role/self-generated object is already both representationally and causally occupied. Reframing it as `source-aware entrainment` would not create a wide enough N2 delta.

## Strongest-neighbor warning

Do not revive as assistant-vs-user vector, self-source direction, source-aware context weighting, or self-generated-token entrainment by changing task/model.

## Death code

`F2 / N0-N1-N2 — direct self-authorship representation and causal-control occupancy.`

## Resurrection condition

Only a distinct source property not reducible to self-authorship or conversation-role identity could qualify.