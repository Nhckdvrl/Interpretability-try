# Execution progress

## 2026-08-31 — V0 public-output reconstruction

- Upstream: `Xtra-Computing/LLM-Deception` at `ac49e131f124d006347223daf158c65f8133e602`.
- Reconstructed 12,000 unique graph instances and 21,915 valid model-instance rows for Qwen3-30B-A3B and Meta-Llama-3.1-8B-Instruct.
- Directed reachability was recomputed from released graph metadata. It agrees with every JSON and CSV ground-truth answer.
- The Qwen3 correctness columns agree with independent response rescoring. The Llama files contain 357 initial and 592 follow-up correctness-column disagreements; independent final-Yes/No rescoring systematically raises the estimated deceptive-event rate.
- Frozen full manifest: ignored artifact `artifacts/v0_validation_manifest.jsonl`, SHA-256 `1852f943ba4eeb5403da8f2114868ef3022025d06ecf0a71282230964a281fb1`.
- Tracked summary: `results/v0_summary.json`.

## 2026-08-31 — V1 deterministic local replay

- Local cached model: NousResearch mirror of Meta-Llama-3.1-8B-Instruct, snapshot `d10aef7999a2b5ba950ab3974312feeedbfe0b77`.
- Frozen population: length 10, 32 instances per source cell for each of regular and reverse wording; 192 instances total.
- Decoding: greedy, Transformers backend, 16 new tokens, mother conversation-history format.
- Regular-query mother-deceptive stability: 24/32 (75.0%).
- Reverse-query mother-deceptive stability: 11/32 (34.4%); 18/32 become hard-truthful.
- Interpretation: begin causal work on the stable regular-query subset. Keep reverse wording as a polarity control rather than pooling it into the recipient population.
- Tracked summary: `results/v1_llama_replay_summary.json`.

The first vLLM attempt failed during FlashInfer warm-up because the installed sampler mis-detected the Blackwell SM 12.x device. No environment was created or altered; the run continued with the existing environment's working PyTorch/Transformers stack.
