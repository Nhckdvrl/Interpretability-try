# Rejection — Proactive Interference: Encoding/Updating vs Retrieval Competition

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- proactive interference encoding vs retrieval
- new-value update failure vs old-value retrieval intrusion
- working-memory interference locus
- stale-memory competition vs impaired encoding
- consolidation vs retrieval in LLM proactive interference
- old-value primacy vs recency retrieval failure

## Natural question considered

> When old in-context information prevents an LLM from using a newer update, was the new value already encoded/updated poorly, or is the new value represented but lost at retrieval because earlier memories win the competition?

This is a real, mature cognitive-science question: human PI literature has long debated encoding-stage and retrieval-stage contributions. The LLM phenotype and executable substrate are also unusually strong. Nevertheless, a 2026 strongest neighbor already owns the relevant theory-level interpretation.

## Strong substrate that initially made the route promising

Wang & Sun (2025), `Unable to Forget: Proactive Interference Reveals Working Memory Limits in LLMs Beyond Context Length`, provides PI-LLM and a public executable repository. It shows that repeated semantically related key-value updates cause retrieval of the newest value to collapse as stale values accumulate, including on modern Llama/Qwen/Mistral-class models. The public implementation exposes exact generators, configurations, raw-result structure and deterministic scoring.

Thus this route does **not** die because of missing behavior or data.

## Decisive N2 collision

Chattaraj & Raj (2026), `Transformers Remember First, Forget Last: Dual-Process Interference in LLMs` (arXiv:2603.00270), explicitly contrasts proactive and retroactive interference across 39 LLMs and already adopts the consolidation-vs-retrieval framework as its explanatory lens.

The paper states, at headline/contribution level rather than only in limitations, that:

- RI appears to probe whether initial encodings survive subsequent overwriting — a consolidation / representation-preservation process;
- PI probes whether attention can prioritize recent information over entrenched earlier encodings — a retrieval process;
- PI failures are active primacy intrusions rather than passive omission;
- PI is characterized as a retrieval-driven process and associated with winner-take-all / primacy behavior in transformer attention;
- the RI/PI dissociation is presented as evidence for distinct memory mechanisms.

Therefore the proposed question `is PI caused by poor encoding/updating of the recent value or retrieval competition from old values?` is no longer an unasked theory-level axis in LLMs. A causal activation-patching paper would primarily test/refine the recent paper's own mechanistic interpretation.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
scientific_lineage: PASS
exact_public_substrate: PASS
modern_open_family_behavior: PASS
N0_object_ownership: FAIL
N1_causal_occupancy: partially_open_but_irrelevant
N2_delta_width: FAIL
reason: strongest 2026 neighbor already interprets PI as retrieval/attention failure against entrenched earlier encodings and contrasts it with encoding/consolidation failure for RI
verdict: KILL-NOVELTY
```

## Why MI cannot rescue it

A natural paper description would now be:

> `Recent work argues PI is retrieval-driven while RI is consolidation-driven; we use activation patching to show where/how the PI retrieval failure occurs.`

That is the current protocol's forbidden behavior/theory-claim -> mechanism-refinement pattern. The absence of activation patching in the neighbor is not enough to create a concept-level N2 delta.

Do not revive by renaming the alternatives as:

- overwrite vs competition;
- update failure vs attention failure;
- memory trace corruption vs stale-value intrusion;
- storage vs access;
- consolidation vs retrieval;
- primacy bias vs recency gate.

## Nearest-neighbor warning

Also nearby are 2026 papers on quantization-amplified proactive interference and architecture-level forgetting/consolidation methods. Future PI candidates must treat the LLM interference object as already mechanism-crowded, not as a fresh behavioral anomaly.

## Resurrection condition

Only reconsider if a different, independently established PI theory axis is found that is not equivalent to encoding/consolidation vs retrieval/attention, is absent from the 2026 dual-process account, and has theory-diagnostic cross-cells already present in a public modern-open-model artifact.
