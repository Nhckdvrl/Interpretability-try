# Rejection — Tool Usefulness / Relevance vs Tool Necessity

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

A tool can be relevant or helpful without being necessary. Does an LLM distinguish `this tool could help` from `I cannot reliably solve this without the tool`?

## Semantic aliases

- tool relevance vs necessity
- optional vs indispensable tool
- when to use tools
- unnecessary tool calls
- tool overuse

## Why it looked promising

This was a natural omitted-axis extension from tool-irrelevance work. Relevance and necessity are plainly distinct, and model capability creates natural cross-cells where a tool is useful but optional versus genuinely needed.

## Decisive kill evidence

ACL 2025 `Adaptive Tool Use in Large Language Models with Meta-Cognition Trigger` already derives representation-space signals for whether external tools should be invoked. In 2026, `LLM Agents Already Know When to Call Tools -- Even Without Reasoning` introduces When2Tool, explicitly labels tool-necessary versus tool-unnecessary cases, finds tool necessity linearly decodable in hidden states with AUROC 0.89--0.96 across six models, and uses the signal to reduce unnecessary calls. `Model-Adaptive Tool Necessity Reveals the Knowing-Doing Gap in LLM Tool Use` further defines necessity relative to each model's actual capability and decomposes hidden cognition of necessity from the final tool-call action.

Thus the exact scientific object `tool necessity as an internal state distinct from execution` is already directly occupied. A new activation patching/steering study would be stronger MI on the same object.

## Strongest-neighbor warning

Do not revive as optional-vs-required tool vector, tool-necessity circuit, relevant-but-unneeded contrast, or cognition-to-tool-call patching.

## Death code

`F2 / N0-N1-N2 — direct behavioral and hidden-state ownership of tool necessity.`

## Resurrection condition

Only a different tool property with an independent scientific meaning and unoccupied internal object could reopen this family.