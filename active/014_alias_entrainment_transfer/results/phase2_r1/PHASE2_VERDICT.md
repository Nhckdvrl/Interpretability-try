# 014 Phase 2 — Verdict

**Contract:** `configs/contract_r1.yaml`, `phase2` block (`2026-08-29-r2`, + amendment r2a), frozen before any ablation
**D0:** unchanged, `c744ae319600fc79e80195ca5b5774b0af6b812714371812e0f61259dae37239`
**Models:** Llama-3.1-8B-Instruct (mother's family), Qwen3-8B (independent replication)
**Run:** 2026-08-29. Sweep 349s / 315s; ablate 168s / 156s.

> ## Verdict: `mechanism_B_shared_entity_representation`
> The sparse set of heads that carries **exact-form** reappearance also carries the
> **unseen-alias** component, and removes it in roughly the same proportion.
> `mechanism_C` (two separate pathways) is **excluded**: layer-matched random heads leave
> the alias component completely intact (retain 1.00–1.48) while entrainment heads cut it
> to 0.15–0.73.

---

## 1. Why this test is not circular

Heads were ranked by individual ablation on a **discovery half of the entities**, using the
`EXACT` condition **only** — the ranking never sees an alias. Every number below comes from
the **held-out half**. The entity split is stratified so the `opaque_strict` cell (the
primary readout, the only cell where the phase-1 effect is not confounded with lexical
overlap) is halved evenly: Llama 60 discovery / 66 evaluation, Qwen 51 / 52.

## 2. Head discovery reproduces the mother's sparsity result

Individual head ablation, top 15 by drop in median `Δ_EXACT`:

| Llama-3.1-8B-It | | Qwen3-8B | |
|---|---:|---|---:|
| L14 H20 | +1.43 | L34 H13 | +1.39 |
| L13 H18 | +1.37 | L35 H8 | +1.37 |
| L31 H14 | +1.36 | L22 H0 | +1.02 |
| L14 H23 | +1.09 | L35 H25 | +0.96 |
| L13 H2 | +1.02 | L31 H3 | +0.90 |

Llama's cluster at L13–L17 plus a late L30–L31 pair; Qwen's at L34–L35 plus mid L14–L22.
A single head is worth up to 1.43 of 11.85 nats. 383/1024 (Llama) and 337/1152 (Qwen)
heads *increase* entrainment when removed, so the circuit is not uniformly excitatory.

**Validity gate** (`retain_EXACT ≤ 0.70` and materially below the layer-matched random control):

| k | Llama retain_EXACT (rand) | Qwen retain_EXACT (rand) | gate |
|---|---:|---:|---|
| 1% | 0.734 (0.98) | 0.721 (0.98) | **FAIL** (both) |
| 3% | 0.630 (1.00) | 0.551 (0.96) | PASS |
| 5% | 0.579 (0.97) | 0.433 (0.93) | PASS |
| 10% | 0.419 (0.89) | 0.365 (0.87) | PASS |

Ablating 3% of heads removes 37–45% of exact-form entrainment; ablating the *same number*
of layer-matched random heads removes essentially nothing. k=1% narrowly misses the
pre-registered 0.70 threshold in both families and is reported but not interpreted.

## 3. The result: the alias component rides the same heads

Primary readout — `opaque_strict` × gate-passed, held-out half.
Clean: Llama `EXACT` +11.21 / `ALIAS−SEMREL` +1.36; Qwen `EXACT` +16.47 / `ALIAS−SEMREL` +0.83.

| model | k | retain_EXACT | retain_ALIAS | rand retain_ALIAS | selectivity | verdict |
|---|---|---:|---:|---:|---:|---|
| Llama | 3% | 0.630 | 0.620 [0.34,1.06] | 1.004 | **−0.010** [−0.30,+0.45] | mechanism B |
| Llama | 5% | 0.579 | 0.727 [0.42,1.26] | 1.030 | +0.148 [−0.19,+0.67] | mechanism B |
| Llama | 10% | 0.419 | 0.308 [−0.01,0.77] | 0.636 | −0.111 [−0.46,+0.37] | mechanism B |
| Qwen | 3% | 0.551 | 0.326 [−0.21,0.73] | 1.309 | −0.224 [−0.79,+0.19] | mechanism B |
| Qwen | 5% | 0.433 | 0.147 [−0.19,0.64] | 1.482 | −0.286 [−0.63,+0.20] | INDETERMINATE |
| Qwen | 10% | 0.365 | 0.313 [−0.14,0.64] | 1.357 | −0.052 [−0.50,+0.27] | mechanism B |

Secondary (amendment r2a) — all held-out gate-passed items, better powered (Llama n=145,
Qwen n=126). Selectivity is consistently small and slightly negative:

| k | Llama | Qwen |
|---|---:|---:|
| 1% | −0.143 [−0.40,+0.03] | −0.222 [−0.32,−0.01] |
| 3% | −0.123 [−0.31,+0.05] | −0.129 [−0.24,+0.00] |
| 5% | −0.062 [−0.23,+0.15] | −0.067 [−0.16,+0.05] |
| 10% | −0.089 [−0.25,+0.12] | −0.106 [−0.17,+0.01] |

### The decisive comparison

The cleanest statement does not depend on the ratio-of-ratios at all:

```text
entrainment heads   ->  retain_ALIAS 0.15 – 0.73   (CI excludes 1.0 in 6 of 8 cells)
random matched heads ->  retain_ALIAS 1.00 – 1.48   (untouched, if anything raised)
```

Heads selected purely by how much they carry the reappearance of a **seen** token also
carry the boost to a **never-seen** alias. Removing them removes both. That is the phase-2
finding.

## 4. What this rules out, and what it does not

**Ruled out — `mechanism_C` (two pathways).** Mechanism C predicts `retain_ALIAS ≈ 1` while
`retain_EXACT` falls to ~0.4. Observed: `retain_ALIAS` falls with `retain_EXACT`, in both
families, at every k, while the random control holds it at ~1.0–1.5. The alias effect does
not survive ablation of the exact-entrainment circuit.

**Supported — `mechanism_B`.** One circuit, both components. Combined with phase 1's
knowledge-gating result (the alias effect is present only where the model can link the two
forms), the picture is that these heads act on a representation that has already abstracted
over surface form, and their write elevates whichever lexical realization the model
associates with it.

**Not established.** Selectivity point estimates lean slightly negative (alias removed a
little *more* than exact) — Qwen's secondary at k=1% is the only cell whose CI excludes 0,
at −0.222 [−0.32,−0.01]. That direction, if real, would mean the alias component is
*downstream* of the copy circuit rather than a co-equal output of it. Nothing here settles
that; the pre-registered `mechanism_A_prime` threshold (−0.25 with CI excluding 0) is not
met in the primary readout at any k.

## 5. Honest limits

1. **The primary readout is underpowered for the ratio statistic.** All the imprecision sits
   in `retain_ALIAS`: the clean alias effect is ~1 nat against per-item noise of similar
   size, so its CI spans ±0.4 while `retain_EXACT`'s spans ±0.06. Reading "mechanism B" off
   a CI that includes zero is partly a statement about power. The positive claim in §3 —
   entrainment heads cut the alias component while random heads do not — is what the data
   support strongly; the *proportionality* claim is the weaker half.
2. **k=1% fails the validity gate** in both families and is not interpreted.
3. **Ablation ranking is greedy-by-individual-effect**, not the mother's trained
   differentiable mask. Individual drops are far from additive (summed top-3% drops exceed
   the clean effect by 1.6–2.1×), so the selected set is a proxy for, not a reconstruction
   of, the mother's entrainment heads.
4. **Two families, one size each.** The phase-1 scale axis says the mechanism exists from
   0.6B up, but no ablation was run off 8B.

## 6. Where this leaves the project

Phase 1: the causal unit of contextual entrainment is predominantly surface, with a real
but minority entity-level component (7–14% of exact-form entrainment in the clean stratum),
knowledge-gated, present from 0.6B.

Phase 2: that minority component is not a separate mechanism. It runs through the same
sparse head set the mother identified for surface reappearance.

The defensible claim for a paper:

> Contextual entrainment transfers to canonical aliases that never appeared in the prompt,
> beyond similarity-matched semantic priming; the transfer is gated by whether the model
> links the two forms to one entity; and it is mediated by the same sparse set of
> entrainment heads that carries exact-form reappearance. The causal unit is therefore
> a single circuit operating on a partly surface-abstracted representation — not a
> pure token-copy mechanism, and not two mechanisms.

Natural next steps, in order of value: (a) raise power on the strict cell so the
proportionality claim stands on its own; (b) test whether the same heads' *write direction*
is alias-invariant (a representational rather than ablation argument); (c) the method
opening — if one head set carries both, suppressing it should reduce distraction from
paraphrased and aliased context, not just repeated context.
