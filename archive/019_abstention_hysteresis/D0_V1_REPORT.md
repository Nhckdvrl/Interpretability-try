# 019 D0 v1 Report — Abstention Hysteresis

**Decision:** `NO-PROMOTE`

**Date:** 2026-08-30

**Contract:** `019-d0-v1`

## Bottom line

The preregistered abstention-hysteresis hypothesis is rejected. Across Qwen, Gemma, and Llama, retaining a prior epistemic abstention did not make abstention sticky after the complete evidence arrived. It sharply reduced final abstention relative to seeing the identical complete final payload directly.

This is not a refusal-specific reverse effect suitable for a post-hoc paper. A neutral response after the same incomplete first turn produced most of the same recovery benefit, and the residual self-refusal-versus-neutral contrast was small and inconsistent across families. The defensible conclusion is recovery facilitation from the incomplete-to-complete conversational transition, not abstention hysteresis.

## Frozen design

- Two source-grounded multi-hop QA sources: HotpotQA distractor validation and MuSiQue validation.
- 300 items, 150 per source; Hotpot bridge/comparison each 75; MuSiQue 2/3/4-hop each 50.
- Incomplete evidence removes every source-provided supporting paragraph.
- Gold/alias strings must be absent from the remaining evidence.
- Every final condition ends with the same complete-evidence user payload verbatim.
- Gate: full-evidence capability correct by alias-normalized EM or token F1 ≥.80, and generated initial response to incomplete evidence abstains.
- Conditions: direct, self-generated abstention, teacher abstention, nonliteral paraphrase, same-context neutral history, and unrelated answered history.
- Outcomes: generated abstention, length-normalized `ANSWER` versus `ABSTAIN` continuation probability, and answer correctness.
- Paired item bootstrap with 10,000 replicates.

Promotion required ≥50 gated items per source per family, a self-minus-direct abstention increase ≥5pp with positive CI, a positive probability-shift CI, positive teacher/paraphrase directions, stronger self effects than controls, positive effects in both sources, and at least two promoted families. The contract was frozen before formal outcomes.

## Data construction and provenance

| Source | Revision | Arrow SHA-256 | Eligible | Selected |
|---|---|---|---:|---:|
| HotpotQA | `1908d6af…` | `ee53452a…` | 5,144 | 150 |
| MuSiQue | `c8f4f8c…` | `cf31d78a…` | 1,593 | 150 |

The final bank SHA-256 is `c385061a7757a2e57f6be69a1e82723c64b66c5401878068dc67494a8cdb0a12`. Complete contexts range from 2,448 to 11,993 characters, median 7,468. Removed support contains two paragraphs for 200 items, three for 50, and four for 50. A 40-item audit records source IDs, removed titles, questions, answers, and full-evidence hashes.

A two-item engineering smoke revealed a valid alias mismatch (`Louis-Hector Berlioz` versus `Hector Berlioz`). Before formal runs, capability correctness was frozen to source-normalized alias EM or token F1 ≥.80. This repair preceded every hysteresis outcome.

## Models and coverage

| Family | Snapshot | Raw records | Gated | Runtime |
|---|---|---:|---:|---:|
| Qwen | Qwen3-8B `b968826…` | 1,355 | 91 | 1,059.9 s |
| Gemma | Gemma-3-12B-IT `96b6f1…` | 1,490 | 118 | 1,932.8 s |
| Llama | Meta-Llama-3.1-8B-Instruct-compatible `d10aef…` | 1,280 | 76 | 836.3 s |

The locally complete NousResearch mirror supplied the Llama-family checkpoint because the official local cache lacked a complete tokenizer. All inference used BF16, greedy generation, and the same bank.

Raw SHA-256 checksums:

- Qwen: `4a85296726c18780169e8d6d7bd52bf2e120be9fab604326b5ed019a2058d048`
- Gemma: `a28ea8570fb5e212254ee772d87d13b50fedd86463c791b5dcadab0f2306967a`
- Llama: `9a8b7f78f3536daaeb092dd8e582ba06e975e3e2856413f214b1117694df21c2`

## Recognition gate

| Family | Total gate | Rate | HotpotQA | MuSiQue | Per-source threshold |
|---|---:|---:|---:|---:|---:|
| Qwen | 91 | 30.3% | 68 | 23 | fail |
| Gemma | 118 | 39.3% | 69 | 49 | fail by one |
| Llama | 76 | 25.3% | 55 | 21 | fail |

The denominator shortage blocks promotion, but is not the substantive failure: every family's primary effect points strongly opposite to hysteresis.

## Primary result

| Family | Direct abstention | Self-history abstention | Difference | 95% CI | Probability difference | 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| Qwen | 46.2% | 5.5% | −40.7pp | [−50.5, −30.8] | −43.1pp | [−50.9, −35.3] |
| Gemma | 13.6% | 2.5% | −11.0pp | [−16.9, −5.1] | −19.0pp | [−24.4, −13.9] |
| Llama | 25.0% | 1.3% | −23.7pp | [−34.2, −14.5] | −27.7pp | [−31.6, −24.0] |

Correctness moves in the recovery direction: +30.8pp for Qwen, +6.8pp for Gemma, and +26.3pp for Llama. Gemma's correctness CI includes zero, while abstention and continuous-mode outcomes do not.

By source:

| Family | HotpotQA | MuSiQue |
|---|---:|---:|
| Qwen | −42.6pp [−54.4, −30.9] | −34.8pp [−56.5, −17.4] |
| Gemma | −4.3pp [−10.1, 0.0] | −20.4pp [−32.7, −8.2] |
| Llama | −16.4pp [−27.3, −7.3] | −42.9pp [−61.9, −23.8] |

No source-family cell supports positive hysteresis.

## Fatal controls

Generated-abstention differences relative to direct:

| Family | Self | Teacher | Paraphrase | Same-context neutral | Answered history |
|---|---:|---:|---:|---:|---:|
| Qwen | −40.7pp | −44.0pp | −42.9pp | −37.4pp | +4.4pp |
| Gemma | −11.0pp | −10.2pp | −13.6pp | −13.6pp | −7.6pp |
| Llama | −23.7pp | −23.7pp | −19.7pp | −19.7pp | +9.2pp |

Teacher and paraphrased refusal do not preserve abstention. Neutral history after the same incomplete user turn already yields nearly the same facilitation. The self-minus-neutral residual is −3.3pp for Qwen, +2.5pp for Gemma, and −3.9pp for Llama. Its sign is not family-stable, so the result cannot be attributed to a self-generated refusal state.

The unrelated answered-history control is approximately zero for Qwen, facilitative for Gemma, and abstention-increasing for Llama. Generic conversation length or a previous answer does not explain the consistent incomplete-to-complete recovery.

## Protocol and classifier audit

Initial incomplete responses follow the requested `ANSWER`/`ABSTAIN` prefix in all 900 cases. Final Qwen outputs are fully prefix-compliant. Llama has two non-prefix final outputs. Gemma often drops the prefix after paraphrased or neutral histories and directly emits a short answer; 40 such outputs were inspected and contained answers or attempted answers, not missed epistemic refusals.

A deterministic 72-row audit sample covers `answer`, `abstain`, and `other` prefixes. Every sampled `abstain` prefix is classified as abstention; no sampled `answer` or `other` response is. Independent continuation probabilities reproduce the negative result, so it is not a regex artifact.

## Novelty audit

Three close lines of work constrain the claim:

1. *Post-Abstention* (Varshney & Baral, 2023) re-attempts low-confidence selective-QA instances using paraphrase ensembles, top-N reranking, and human intervention. It does not preserve refusal history or restore removed evidence.
2. Abstain-R1 (Findings ACL 2026) trains abstention and identification of missing information, but does not test recovery after that information arrives.
3. *Over-Searching in Search-Augmented Large Language Models* (EACL 2026) shows a multi-turn snowball: histories of unrelated unanswerable questions encourage abstention on a fixed final query. It establishes history dependence, but not a same-question unanswerable-to-answerable transition with equivalent final payloads.

The transition-equivalent design remains distinguishable, but novelty risk is moderate-to-high. A strong positive result would have needed clean refusal-specific controls. D0 instead finds no positive effect.

## Paper-level judgment

019 should not proceed as an ACL/EMNLP/NAACL paper under the registered hypothesis. The evidence is not merely underpowered: all three families, both response decisions and continuation scores, and both sources point away from hysteresis. The neutral control shows that most facilitation belongs to seeing incomplete and then complete versions, not to having abstained.

It would be post-hoc narrowing to rename the project “evidence-update history helps QA,” retain only a favorable source, or study the inconsistent self-versus-neutral residual. The current design was not built to isolate which aspect of repetition, contrast, recency, or evidence change causes facilitation. Preserve the negative result and stop.

## Artifact map

- `configs/d0_contract.json`: frozen design and promotion rule.
- `data/d0_v1/d0_bank.jsonl`: final paired evidence bank.
- `data/d0_v1/scope_summary.json`: source revisions, hashes, and counts.
- `data/d0_v1/source_audit_sample.jsonl`: 40-item provenance audit.
- `data/d0_v1/response_audit_sample.jsonl`: 72-row classifier audit.
- `src/abstention_hysteresis/`: builder, prompts, runner, analysis, and audit utility.
- `results/d0_{qwen,gemma,llama}.jsonl`: complete raw responses and scores.
- `results/d0_{qwen,gemma,llama}.metadata.json`: exact model/runtime metadata.
- `results/d0_analysis.json`: standards-compliant combined analysis.
- `tests/`: construction, payload equivalence, parsing, gate, and bootstrap tests.
