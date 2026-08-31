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

## 2026-08-31 — V2 mechanistic preflight

- Frozen recipient rule: Meta-Llama-3.1-8B, positive-direction only, V0 independently rescored mother-deceptive **and** V1 deterministic mother-deceptive.
- Frozen population: 24 hard-deceptive recipients and 13 stable hard-truthful controls. All hard graphs are length 10, broken at position 5, unreachable, with correct answer `No`.
- Generated deterministic graph state for every item: full chain, present edges, missing edge and index, source/target components, reachability, correct answer, and prompt fact/entity character spans.
- Population artifact: ignored `artifacts/v2_population.jsonl`, SHA-256 `6acbc2ca1d3888dcbd00721b5b0d49a46eca4bbbfa1f56f49812b9ce7074068e`; tracked summary `results/v2_population_summary.json`.
- Layer-wise answer-state trace: 33 residual states at the hard/easy prompt-final token. Hard-deceptive runs stay substantially below hard-truthful/easy controls through the late stack, briefly approach the correct `No` direction at layer 31, and return to the wrong direction at the final state. This is an answer-token logit lens, not a graph-state probe.
- One easy follow-up (`...i0613:740fa6e92318`) is numerically unstable under the hidden-state instrumentation path and is excluded from transplantation, leaving 23 recipients.
- Whole-state transplantation upper bound: matched-easy replacement rescues 100% at layers 20–30, but shuffled-easy replacement also rescues 100% with nearly identical mean margin gains. Same-norm random replacements rescue only 0–8.7%; hard-truthful donors rise from 78.3% at layer 20 to 100% at layer 30.
- Interpretation: the intervention primitive works, but the rescue is a generic cross-item answer-state transfer. It does **not** show that the hard run contains or lacks a graph-specific correct reachability state.
- Tracked outputs: `results/v2_answer_state_trace_summary.json` and `results/v2_transplant_preflight_summary.json`. Raw activations and per-item interventions remain ignored artifacts.

Next gate: identify an answer-polarity-controlled reachability/missing-edge subspace with graph-instance-grouped evaluation, then patch only that subspace. Matched patching must beat shuffled-answer-state and random controls before it can address the paper-level deception criterion.

## 2026-08-31 — V3 within-run state measurement gate

The paper-level target was deliberately narrowed before this run. Cross-query success was not treated as the claim. The only promotion route was a graph-instance-specific state trajectory inside the hard computation: correct state never formed, formed then corrupted, or remained intact but unused.

- Built a same-graph calibration panel from 256 non-recipient graphs plus the 24 frozen recipients: 192 train, 64 held-out test and 24 recipient graphs; 1,680 prompts total.
- For every graph, visible facts and graph identity remain fixed. Queries vary between two within-component reachable pairs and one cross-gap unreachable pair, each under positive and reverse wording. `Yes`/`No` is exactly balanced within every graph.
- Behavioral pairwise accuracy remains strongly direction-dependent: held-out positive reachable queries score 85.9–95.3%, positive cross-gap only 14.1%, while reverse cells range from 40.6–51.6%.
- Extracted all 33 prompt-final residual states from the local frozen Llama checkpoint.
- Mean-difference reachability instrument failed: best held-out invariant AUROC 0.522; cross-polarity AUROCs 0.525 and 0.516; recipient AUROC 0.421.
- A stronger dual-ridge linear probe with graph-group fit/validation/test and validation-only regularization also failed: best held-out invariant AUROC 0.532; cross-polarity AUROCs 0.538 and 0.530; recipient AUROC 0.465. No layer passed the frozen semantic/polarity gate.
- Causal patching was not run. Without a held-out, polarity-invariant relational measurement, a patch would again risk transferring query wording or answer policy rather than graph state.

Decision: **KILL 031 as a main mechanistic project.** The result does not prove that correct graph state never formed; it shows that the planned causal distinction is not identifiable with this final-token residual measurement, and further probe/token-position search would violate the predeclared stopping rule. V0–V2 remain a useful benchmark audit and negative-control record, but they do not support a sufficiently novel paper-level claim.
