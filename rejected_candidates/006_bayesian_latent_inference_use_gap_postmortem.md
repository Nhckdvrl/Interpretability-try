# 006 Bayesian latent inference → downstream-use gap — Postmortem

**Verdict:** `KILL / DO NOT SALVAGE AS CURRENT TOPIC`
**Date:** 2026-08-27

## Why 006 is not a good topic

The project accumulated three independent failures that jointly invalidate it as a preferred research direction.

1. **External validity is not established.** The custom closed-form prompts produce a strong phenotype mainly on Qwen2.5-14B, while Gemma3-12B and Qwen3-8B do not reproduce the same inference→use pattern. Later meta-G0 runs additionally expose label collapse / mapping fragility. This is exactly the kind of prompt- and operationalization-dependent phenotype the repository now tries to avoid.
2. **The broad behavioral claim is already occupied.** BayesBench already reports that stronger latent-state inference does not reliably transfer to downstream prediction across multiple open models and public environments. Our synthetic behavior therefore is neither a robust new phenomenon nor a clean external replication.
3. **The mother question is too task-constructed.** The project begins from a synthetic posterior-report/policy-use interface and then asks where that interface fails. The scientific object is therefore substantially created by our prompt design, rather than beginning from a natural phenomenon that exists independently of LLM prompting.

## General lesson

Do not promote a formal/computational construct merely because it admits clean analytic gold and attractive H1/H2/H3 mechanism branches. A clean scorer cannot compensate for weak external validity or an artificial mother phenomenon.

Future candidates must first satisfy:

- natural phenomenon independent of LLM task design;
- strong exact modern open-model evidence already visible in public data;
- matched controls that do not depend on fragile label binding;
- mechanism question not already occupied by the behavioral source paper;
- method branches that depend on the causal diagnosis.

The existing 006 code/results should remain useful only as negative methodological evidence, not as a topic to rescue by further prompt tuning or weaker-model search.
