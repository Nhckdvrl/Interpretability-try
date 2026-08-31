# Continuation Terminal Addendum 7 — 2026-08-31

Status: **CONTINUATION TERMINAL LOG / 0 NEW PASS-REGISTER**.

This file records serious candidates audited after `continuation_terminal_addendum_6_2026-08-31.md`. The authoritative handoff and newest terminal addendum override stale positive wording elsewhere.

---

## 1. Affective validation / emotional support ≠ epistemic endorsement

**Natural question.** When a user is sad or vulnerable, can a model validate the user's feelings without also treating the user's factual belief as more worthy of agreement? In ordinary conversation, emotional support and factual endorsement are different social acts.

**Why it initially looked good.** Nature 2026 reports a striking, broad behavior: warmth fine-tuning reduces factual accuracy across multiple model architectures and makes models substantially more likely to affirm incorrect user beliefs, with the warm–original accuracy gap especially enlarged when the user expresses sadness. This creates an unusually natural mechanistic fork: one generic `support/agree` control signal versus separable affective-validation and epistemic-endorsement computations. The question is understandable without any benchmark or MI vocabulary and matters directly for assistants used for support, advice, tutoring and companionship.

**Kill evidence.** The strongest-neighbor search directly occupies the title-level distinction. `Personalization Increases Affective Alignment but Has Role-Dependent Effects on Epistemic Independence in LLMs` (2026) explicitly separates *affective alignment* (including emotional validation / hedging / deference) from *epistemic alignment or independence* (belief adoption, position stability and resistance to influence), and studies how personalization changes the two differently. `Social Sycophancy: A Broader Understanding of LLM Sycophancy` (2025) also explicitly includes emotional validation as one of several face-preserving sycophancy behaviours. The Nature warmth paper itself already owns the behavior that warmth plus sadness disproportionately increases false-belief affirmation. Therefore an MI project asking whether emotional validation and epistemic endorsement are separate representations would be a direct hidden-state/mechanism successor to an already named affective-versus-epistemic object rather than a new ACL/EMNLP/NAACL-level scientific object.

**Death code.** `KILL-N1 / DIRECT-AFFECTIVE-VS-EPISTEMIC-ALIGNMENT-COLLISION`

**Nearest-neighbor warning.** Do not resurrect as `empathy vs agreement`, `validation vs factual endorsement`, `support vs correction`, `kindness vs truth`, `sadness-gated sycophancy`, `warmth reader vs truth writer`, tutoring-specific supportive correction, another emotion, another persona, or by adding probes/SAEs/activation patching. Those are the same occupied affective-alignment versus epistemic-independence family unless a new behavior forces a different computation.

**Resurrection condition.** A distinct natural behavioral phenomenon must first show a causal structure that cannot be represented as affective/social alignment versus epistemic agreement/independence—for example, a broad current-open-family effect with a different externally defined operator and a decisive intervention prediction not already implied by sycophancy/personalization work.

**Key references.**

- Ibrahim, Hafner & Rocher (Nature, 2026), `Training language models to be warm can reduce accuracy and increase sycophancy`: https://www.nature.com/articles/s41586-026-10410-0
- Kelley & Riedl (PsyArXiv, 2026), `Personalization Increases Affective Alignment but Has Role-Dependent Effects on Epistemic Independence in LLMs`: https://doi.org/10.31234/osf.io/ez7cu
- Cheng et al. (2025), `Social Sycophancy: A Broader Understanding of LLM Sycophancy`: https://arxiv.org/abs/2505.13995

---

# Current result after this audit

```yaml
new_PASS_REGISTER: 0
registered_new_topics: []
new_terminal_kills:
  - affective_validation_vs_epistemic_endorsement: KILL-N1
```

**No candidate passes the current bar.**
