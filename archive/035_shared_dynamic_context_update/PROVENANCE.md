# Provenance

The common-window audit uses:

- `xiaomeng-zhu/anaphora-accessibility` commit
  `5d44efa61b49ab270aace476620e9aeda5e55814`;
- `proviso-bench/Presupposition-and-Reasoning-in-Conditionals` commit
  `9dca0a9edb4ac358f80e565173de19fdcd20cc06`.

Both released files report the exact `meta-llama/Llama-3.1-8B-Instruct` checkpoint. The
audit parses deterministic mother scores/rating strings; it does not use the released
LLM-as-judge annotations.

The deterministic S0-2 gate uses all 90 released presupposition problem-set
items and all six mappings of low/mid/high to A/B/C. It uses forced candidate
log probabilities from the cached Llama mirror revision
`d10aef7999a2b5ba950ab3974312feeedbfe0b77`; no subset, generated judge, or
post-result label mapping is used.
