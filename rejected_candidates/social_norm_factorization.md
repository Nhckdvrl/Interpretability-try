# Rejected Candidates — Social Norm Factorization

**Domain:** social norms, morality, legality, descriptive/injunctive norms and related social-evaluation axes.  
**Status:** negative-memory ledger, 2026-08-31.

---

# 1. Moral Wrongness ≠ Legality (`Wrong ≠ Illegal`)

**Natural question:** An action can be morally wrong while legal, and legality is not the same thing as moral approval. Does a language model internally represent moral evaluation and legal status as different variables?

**Why it initially looked good:**

- morality and legality are genuinely different concepts in ordinary life;
- unlike the earlier W36 attempt that would have spliced LegalBench and ETHICS, SOCIAL-CHEM-101 provides the **same natural action** with human `action-moral-judgment` and `action-legal` annotations at large scale;
- the public Hugging Face mirror contains ~356k rows and both fields in the same row, so the old S0 artifact objection appeared potentially recoverable.

**Kill evidence:**

N0 fails before a full S0 count is worth doing. The SOCIAL CHEMISTRY mother does not merely happen to expose two annotation columns. Its explicit scientific formalism is to **partition social expectations using theoretically motivated dimensions**. It separately defines:

- `legality` as a prescriptive-norm attribute;
- `cultural pressure` as a descriptive-norm attribute;
- `social judgment` as subjective moral judgment.

The paper then jointly analyzes moral judgment, agreement, cultural pressure and legality in Figure 5, and its modeling objectives explicitly predict, label, condition on and generate the full attribute set. Thus the distinction between moral judgment and legality is already part of the mother’s title-level multidimensional object. Replacing its attribute modeling with modern probes/SAEs/patching would be the prohibited shape **“mother already defines the dimensions → we do MI.”** A large 2×2 substrate cannot repair an N0 scientific-object collision.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as `wrong vs illegal`, `moral vs legal`, `morality vs legality`, `ethical permissibility vs legal status`, or by using SOCIAL-CHEM-101 with newer open models / causal interventions. Do not claim novelty merely because the 2020 mother did not use mechanistic-interpretability tools.

**Resurrection condition:** A new natural phenomenon involving morality and law whose headline is **not** simply their multidimensional separation—for example, a stable behavioral anomaly with competing mechanisms that the Social Chemistry formalism does not already define. Such a candidate must re-enter P0/S0/N0 from scratch.

**References:**

- Forbes et al., EMNLP 2020, *Social Chemistry 101: Learning to Reason about Social and Moral Norms*: https://aclanthology.org/2020.emnlp-main.48/
- Official code/schema: https://github.com/mbforbes/social-chemistry-101
- Public row-level mirror: https://huggingface.co/datasets/wassname/social_chemistry_101

---

# Non-rejected neighboring lead

- **Descriptive norm ≠ injunctive norm (`Common ≠ Right`)** remains conceptually attractive, but current same-behavior public sources found in this search have only tens of independent behaviors. Do not register unless a broad row-level natural substrate appears; experimental manipulations that simply tell participants “most people do X” do not satisfy S0.
