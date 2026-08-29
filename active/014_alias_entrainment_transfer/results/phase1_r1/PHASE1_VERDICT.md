# 014 Phase 1 — Verdict

**Contract:** `configs/contract_r1.yaml` (`2026-08-29-r1`; amendments r1a and r1b both recorded, both made before the model calls they affect, both tightening)
**D0:** `data/frozen_d0.jsonl`, sha256 `c744ae319600fc79e80195ca5b5774b0af6b812714371812e0f61259dae37239`, 300 items / 150 entities
**Run:** 2026-08-29, three families, 9,900 scored forward passes each, 0 tokenizer boundary shifts
**Harness invariants:** `tests/test_harness_invariants.py`, 8 passed — including the one the experiment rests on, that the scored string never occurs in the prompt in the `ALIAS` condition.

> ## Verdict: `PROMOTE`
> Every frozen criterion is met in all three families. **The answer to the mother question is "both, and mostly the surface form."** A canonical alias that never appeared is entrained above a similarity-matched non-coreferent control — but in the cleanest stratum that transfer is worth only **7–14%** of exact-form entrainment. Two qualifications in §4 must travel with the claim.

---

## 1. Headline

Δ = logP(target | context + carrier) − logP(target | carrier), nats, median over gated items:

| | Llama-3.1-8B-It | Qwen3-8B | Gemma-3-12B-It |
|---|---:|---:|---:|
| gated items | 276/300 | 244/300 | 272/300 |
| probe order gap | +0.030 | −0.153 | +0.037 |
| `EXACT` (target itself appeared) | **+11.55** | **+15.21** | **+18.78** |
| `ALIAS` (alias appeared, target absent) | +4.91 | +5.69 | +11.41 |
| `SEMREL` (max-similarity non-coreferent) | +2.24 | +3.23 | +9.00 |
| `UNREL` (low-similarity same type) | +0.59 | +1.32 | +6.51 |

The ordering `EXACT ≫ ALIAS > SEMREL > UNREL` holds in every family.

## 2. Frozen hypotheses

| | Llama-3.1-8B-It | Qwen3-8B | Gemma-3-12B-It |
|---|---|---|---|
| **H1** `EXACT` ≥ 1.0, frac>0 ≥ 0.80 | +11.55, 1.00 **PASS** | +15.21, 1.00 **PASS** | +18.78, 1.00 **PASS** |
| **H2** `ALIAS − UNREL` | +4.27 [+3.52,+5.01] **PASS** | +4.21 [+3.67,+5.09] **PASS** | +4.03 [+3.50,+5.00] **PASS** |
| **H3** `ALIAS − SEMREL` | +2.24 [+1.77,+2.86] | +2.22 [+1.61,+2.86] | +2.38 [+1.51,+2.98] |
| H3 · similarity-matched | +0.99 [+0.68,+1.52] | **+0.24 [−0.30,+0.93]** | +0.95 [+0.28,+1.73] |
| H3 · `opaque_strict` | +1.23 [+0.79,+1.79] | +0.83 [+0.21,+1.47] | +1.17 [+0.52,+2.49] |
| H3 · regression `is_alias` | +2.13 (t=+12.6) | +1.74 (t=+7.1) | +2.03 (t=+7.8) |
| **H3 verdict** | **PASS** | **PASS** (see §4.2) | **PASS** |
| transfer ratio ≥ 0.15 | 0.25 **PASS** | 0.19 **PASS** | 0.24 **PASS** |

**H4:** H3 passes in **3 / 3** families, with near-identical point estimates (+2.24 / +2.22 / +2.38) across three unrelated pretraining pipelines. That agreement is the single most reassuring feature of the result.

Regression is `Δ ~ sim + orth_sim + n_tokens + is_alias` with item fixed effects (within-item demeaning), fitted on `ALIAS`/`SEMREL`/`UNREL`. External semantic similarity is by far the largest term (β ≈ +12 to +16): **ordinary semantic priming is real and large.** `is_alias` is what survives on top of it.

## 3. Controls that could have killed this and did not

**3.1 The semantic control is not a strawman.** `SEMREL` is the maximum-similarity non-coreferent same-type entity under an external encoder (BGE), never the model under test: `Katy Perry` ← `Kim Kardashian`, `Stephen King` ← `H. P. Lovecraft`, `Rowan Atkinson` ← `Simon Pegg`, `Soviet Union` ← `Russia`, `Elizabeth II` ← `Benazir Bhutto`. In 157/300 items it is *more* embedding-similar to the target than the alias is.

**3.2 Not orthography.** Median `orth_sim` to target: alias 0.39, SEMREL 0.21, UNREL 0.23 — SEMREL selection is explicitly constrained never to be orthographically closer to the target than the alias, so it stays a *semantic* control. `orth_sim` is a mandatory covariate and is itself significant (β +1.6 to +3.0); `is_alias` survives it. The `opaque_strict` stratum (no shared word, not an acronym, character overlap < 0.40; n = 103–126) holds in all three families.

**3.3 The stratum gradient is the honest warning.** `ALIAS − SEMREL` by orthographic stratum:

| | partial | opaque | opaque_strict |
|---|---:|---:|---:|
| Llama | +6.05 | +1.96 | +1.23 |
| Qwen | +5.85 | +2.00 | +0.83 |
| Gemma | +4.79 | +1.65 | +1.17 |

Most of the naive alias effect is lexical overlap. Only the right-hand column is evidence about entity identity, and it is ≈1 nat, not ≈2.3.

**3.4 Not recency or mention position.** F1 puts the mention at the start of the context, F2 immediately before the query. The effect is the same size in both (Llama +2.35/+2.14, Qwen +2.20/+1.96, Gemma +1.94/+2.34). Not a locality artifact.

**3.5 Not acronym expansion.** long→short and short→long both show it (Llama +2.30/+2.20, Qwen +2.31/+2.16). Gemma is asymmetric (+1.24 canonical→alias vs +2.75 alias→canonical), i.e. it transfers more readily *toward* the canonical name — worth following up, not a threat to the claim.

**3.6 It tracks whether the model can actually link the two forms.** The strongest positive evidence for entity mediation, from data already collected. Split by the counterbalanced two-option alias probe:

| `ALIAS − SEMREL` | gate passed | gate failed |
|---|---:|---:|
| Llama | +2.24 (n=276) | −1.20 (n=24) [−2.10,+0.17] |
| Qwen | +2.22 (n=244) | −0.99 (n=56) [−1.59,+0.61] |
| Gemma | +2.38 (n=272) | +0.06 (n=28) [−1.66,+1.83] |

Formal interaction, `Δ ~ sim + orth + n_tokens + is_alias + is_alias×gate_passed`, item FE, all 300 items:

| | `is_alias` | `is_alias × gate_passed` |
|---|---:|---:|
| Llama | +0.33 (t=+0.77, n.s.) | **+1.83 (t=+4.04)** |
| Qwen | +0.81 (t=+2.23) | **+0.90 (t=+2.19)** |
| Gemma | +1.10 (t=+1.82, n.s.) | +0.85 (t=+1.32, n.s.) |

In Llama the alias-specific component exists **only** where the model can link the forms — the bare `is_alias` term goes to zero. Qwen splits it about evenly. This is what a mis-measured-similarity artifact would *not* predict, because the external encoder does not know which pairs a given model happens to have learned. Gemma's interaction is not significant, but its gate-failed cell has n=28.

**3.7 The mother-faithful metric agrees.** First-token logit deltas: `EXACT` +5.23 / +6.82 / +3.69; `ALIAS − SEMREL` +0.54 [+0.35,+0.82] / +1.11 [+0.71,+1.51] / +0.94 [+0.51,+1.19]; `opaque_strict` +0.19 / +0.32 / +0.37, all CIs excluding 0.

## 4. Qualifications that must travel with the claim

**4.1 The causal unit is still predominantly surface.** Transfer ratio restricted to `opaque_strict` is **0.14 / 0.07 / 0.11**. The headline 0.19–0.25 is inflated by the `partial` stratum. The defensible statement is that entrainment has a real but minority entity-level component — not that entrainment is entity-level.

**4.2 Qwen3-8B's similarity-matched subset is null.** +0.24 [−0.30,+0.93]. It satisfies the contract only on the letter ("same sign") and should be reported as a null. That subset is selected on `sim(SEMREL,B) ≥ sim(ALIAS,B)`, which biases against `ALIAS` by construction — which is why the contract also required the regression, which is better powered. Still, Qwen's evidence rests on the regression and the strict stratum, not on the matched subset.

**4.3 Residual similarity mis-measurement is not fully excluded.** `sim` is BGE's estimate of relatedness, not the model's. §3.6 is the argument against that explanation; it is an argument, not a proof, and it is weakest exactly in the family (Gemma) where the interaction fails to reach significance.

**4.4 Instruction-tuned models only, one size per family.** Both the mother paper's scale analysis and the 2026 scale sign-split paper make size the obvious next axis, and it is untested here.

**4.5 Entity types are skewed** (184 person / 96 country-or-region / 20 city), inherited from PopQA's relation mix.

## 5. What this changes about the mother phenomenon

*Llama See, Llama Do* established that reappearance of a **surface token** raises its later logits, and both 2026 successors kept scoring strings that literally appeared. This run says that is not the whole causal story: a form that never appeared is also elevated, above a similarity-matched non-coreferent control, in three families — and in Llama and Qwen that elevation exists only where the model can link the two forms to one entity. Context salience therefore propagates at least partly through a representation that survives a change of lexical realization.

It equally says the surface account is not wrong. Exact reappearance is worth +11.6 to +18.8 nats; the cleanest alias transfer is worth about +1. The honest headline is **graded, not binary**: entrainment is a lexical mechanism with a real entity-level minority component.

## 6. Phase 2 (authorized by the contract, not yet run)

Locate entrainment heads with the mother's differentiable-masking method on the `EXACT` condition, then ask whether zeroing them removes the alias-transfer component `(Δ_ALIAS − Δ_SEMREL)` **selectively**, or merely scales every condition down together.

- Same heads, proportionate suppression of both components → mechanism B: entrainment operates on an already-canonicalized entity representation.
- Exact component removed, alias component survives → mechanism C: two distinct pathways, and the paper becomes *two kinds of entrainment*.
- Alias component removed but exact component survives → the alias effect is downstream of the same copy circuit after all.

Analysis set for phase 2 is the `opaque_strict` × gate-passed cell (n = 103–126 per family) — the only cell where the behavioural effect is not confounded with lexical overlap.
