# Mistral-Small-24B-Instruct-2501 — infrastructure failure, not a scientific result

Three attempts, all hung **after** weights loaded (45.7 GB resident on GPU) and
after `flash_attn.py: Using FlashAttention version 2`, with 0% GPU utilisation
and frozen process CPU time. No batch was ever dispatched, so no item of the
frozen G0 sample was scored by this family.

| # | GPU | settings | outcome |
|---|---|---|---|
| 1 | 0 | CUDA graphs on, `max_model_len=8192` | hung ~36 min, process became an unkillable zombie still holding 45.7 GB |
| 2 | 1 | `enforce_eager=True`, `max_model_len=8192` | hung ~7 min at the same point |
| 3 | 1 | `enforce_eager=True`, `max_model_len=4096` | hung ~9 min at the same point |

The hang is at KV-cache profiling and is independent of CUDA-graph capture,
context length and GPU. It is a host/vLLM/model incompatibility, unrelated to the
NTSB task, the frozen items or the prompts.

**Substitution, decided before any model output was inspected or scored:**
`microsoft/Phi-4-mini-instruct` — the repository's standard fourth family in
`phenomenon_miner/MODEL_PANEL.md` — takes the fourth panel slot. This preserves
the preregistered denominator, so the S0 criterion remains **2 of 4** families
rather than being weakened to 2 of 3. Qwen, Gemma, Llama and Phi are four
genuinely different families, satisfying the handoff's ">= 3 genuinely different
open model families".
