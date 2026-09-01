# Rejection — Ownership vs Current Possession

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

If Alice owns a ball but lends it to Bob, does a language model distinguish **who owns the object** from **who currently possesses or uses it**?

## Semantic aliases

- ownership vs possession
- owner vs holder
- enduring ownership vs current physical control
- loan vs transfer of ownership
- property relation vs possession state

## Why it looked promising

This is an unusually clean everyday distinction. Human ownership research explicitly shows that ownership persists despite changes in current possession and that people weigh intentions and physical possession differently. Open human materials provide natural loan/borrow/take/transfer contrasts.

Initially, the LLM literature appeared to contain mainly generic ownership or robot-learning work rather than this exact contrast.

## Decisive kill evidence

Zhu et al. (2026), `Reasoning Depth and Environment Complexity: A Controlled Study of RLVR Data Allocation across Logical Reasoning Tasks` (arXiv:2605.26934), has a headline about RLVR data allocation, but its dynamic reasoning world explicitly represents every object state as separate **owner, possessor, integrity** slots.

Its event semantics make exactly the intended distinction:

- gift / sale / exchange update both ownership and possession;
- loan / return update **possession only while the owner remains unchanged**.

The paper uses these states in deductive and abductive object-state reasoning and benchmarks a large panel of contemporary off-the-shelf models including Qwen3/Qwen2.5, DeepSeek-derived models, Kimi and others.

Under the post-039 rule, this is direct scientific-object ownership even though the title is not about ownership. A new owner-vs-possessor probe/steering/patching study would primarily turn an already-explicit state factorization into stronger MI.

## Strongest-neighbor warning

Do not revive as owner/holder direction, loan-vs-gift circuit, possession-without-ownership benchmark, ownership-state tracking, or current-use-vs-property steering.

## Death code

`F2 / N0-N2 — exact owner-versus-possessor state factorization is already a modern LLM reasoning object.`

## Resurrection condition

Only a distinct ownership property not reducible to owner/possessor state tracking or transfer semantics could reopen this family.