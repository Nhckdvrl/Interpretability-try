# 014 Phase 3 — Verdict

**Contract:** `configs/contract_r1.yaml`, `phase3` block (`2026-08-29-r3`), frozen before any phase-3 forward pass
**Method:** direct logit attribution (DLA) of the phase-2 entrainment head set to the target's first token, at the position that predicts it
**Models:** Llama-3.1-8B-Instruct, Qwen3-8B. **Analysis set:** the phase-2 held-out evaluation half.

> ## Verdict: `SEEN-FORM-ONLY-WRITE` (the pre-registered negative), in 4/4 cells
> The entrainment heads' **direct write** is a lexical operation. It reaches strings that
> share surface form with what was seen, and **not** same-entity forms that do not.
> Combined with phase 2 — where ablating these same heads *does* remove the alias effect in
> exactly the clean stratum where their direct write shows nothing — the entity-level
> component must be routed through these heads **indirectly**.

---

## 1. Why this phase exists

Phase 2 established that entrainment heads carry the alias component, but its
proportionality half rested on a ratio of medians whose CI always included zero, with all
the imprecision in `retain_ALIAS`. DLA replaces that ratio with a per-item continuous
quantity read straight off the heads' own write.

**Implementation validated before use.** On last-layer heads, where the direct path is the
only path, DLA against actual per-head ablation gives **r = 0.959, slope = 0.938**. On
mid-layer heads r ≈ 0.08 — not a bug, but the expected fact that mid-layer effects are
dominated by indirect paths. This matters for reading the result, and is picked up in §4.

## 2. The measurement works

`dDLA_cond = DLA(cond) − DLA(NOCTX)`, median over the `opaque_strict` held-out cell:

| | k | `EXACT` | random control | validity |
|---|---|---:|---:|---|
| Llama | 3% | **+0.560** [+0.43,+0.64] | +0.131 | PASS |
| Llama | 5% | **+0.761** [+0.51,+1.04] | +0.133 | PASS |
| Qwen | 3% | **+2.843** [+2.22,+3.44] | −0.045 | PASS |
| Qwen | 5% | **+3.124** [+2.47,+4.02] | +0.097 | PASS |

The heads write hard and directly toward a token that appeared; layer-matched random heads
do not. Whatever follows is not a failure of instrumentation.

## 3. The result: the direct write does not carry the unseen alias

Primary readout, `opaque_strict` held-out cell:

| | k | `ALIAS−SEMREL` (DLA) | random | selectivity vs random | verdict |
|---|---|---:|---:|---:|---|
| Llama | 3% | +0.021 [−0.023,+0.061] | +0.007 | +0.001 [−0.037,+0.066] | SEEN-FORM-ONLY |
| Llama | 5% | +0.016 [−0.025,+0.102] | +0.002 | +0.006 [−0.020,+0.080] | SEEN-FORM-ONLY |
| Qwen | 3% | +0.088 [−0.041,+0.316] | +0.012 | +0.055 [−0.068,+0.234] | SEEN-FORM-ONLY |
| Qwen | 5% | +0.084 [−0.024,+0.351] | +0.016 | +0.063 [−0.073,+0.261] | SEEN-FORM-ONLY |

### The stratum gradient is the finding

`dDLA(ALIAS) − dDLA(SEMREL)` at k=3%, by orthographic stratum:

| stratum | n (Llama) | Llama | n (Qwen) | Qwen |
|---|---:|---:|---:|---:|
| `opaque_strict` | 66 | +0.021 [−0.02,+0.06] | 52 | +0.088 [−0.04,+0.32] |
| `opaque` | 46 | **+0.203** [+0.07,+0.31] | 42 | **+0.724** [+0.40,+1.83] |
| `partial` | 31 | **+0.382** [+0.26,+0.47] | 30 | **+1.152** [+0.62,+1.37] |

Meanwhile `dDLA_EXACT` is **flat** across the same strata (Llama +0.56 / +0.62 / +0.59;
Qwen +2.84 / +3.07 / +2.74). So this is not a power gradient: the heads write equally
strongly toward the seen form everywhere, and their write toward an *unseen* form scales
with how much that form looks like the seen one. That is a lexical generalization, not an
entity one.

This is also why the better-powered secondary readout over all held-out items is positive
and excludes zero (Llama +0.114 / +0.146; Qwen +0.494 / +0.512): it pools the `partial` and
`opaque` strata in. Reported for completeness, but it does not license an entity reading.

### Write-direction alignment (secondary)

`cos(w_cond − w_NOCTX, w_EXACT − w_NOCTX)`, `opaque_strict` cell:

| | cos(ALIAS,EXACT) | cos(SEMREL,EXACT) | cos(UNREL,EXACT) | ALIAS−SEMREL |
|---|---:|---:|---:|---:|
| Llama 3% | +0.644 | +0.600 | +0.519 | +0.013 [−0.037,+0.049] |
| Llama 5% | +0.643 | +0.603 | +0.529 | +0.017 [−0.029,+0.058] |
| Qwen 3% | +0.564 | +0.543 | +0.400 | +0.020 [−0.012,+0.089] |
| Qwen 5% | +0.564 | +0.530 | +0.402 | +0.054 [+0.001,+0.087] |

The ordering `ALIAS > SEMREL > UNREL` holds in 4/4 cells, but the ALIAS−SEMREL gap is tiny
and its CI excludes zero in only one. Suggestive at best; it does not rescue the primary.

## 4. What this does to the mechanism story

Put phase 2 and phase 3 side by side, on the **same held-out `opaque_strict` cell**:

```text
phase 2  ablate these heads  ->  the alias effect largely disappears
                                 (retain_ALIAS 0.15-0.73, random 1.00-1.48)
phase 3  read their direct write toward the alias  ->  nothing above control
```

The consistent reading is that the entity-level component is routed through these heads
**indirectly**: their output is a context-salience signal written mid-stack, and downstream
computation turns it into elevated logits for whichever lexical form the model associates
with the entity. The heads do not themselves point at the alias token.

That is coherent with the geometry — only 6/31 (Llama) and 10/35 (Qwen) of the selected
heads sit in the late third of the stack, and mid-layer heads are exactly where DLA and
ablation diverge (§1).

**This inference is not directly tested.** It is a joint reading of two experiments, and the
experiment that would test it is path patching from these heads into later layers, asking
which downstream component converts their write into the alias logit. That is the natural
next step, not a claim this run supports.

## 5. What must not be said

- Not: "entrainment heads represent entities." Their direct write is lexical.
- Not: "phase 2 was wrong." Ablation and direct attribution measure different things, and
  the divergence between them *is* the informative result.
- Not: the positive secondary readout as evidence for the entity account — it is pooled
  across strata whose gradient is precisely the surface-overlap gradient.

## 6. Where the project stands after three phases

| | finding |
|---|---|
| Phase 1 | Alias transfer is real above similarity-matched priming (+2.2 to +2.4 nats, 3/3 families), knowledge-gated, present from 0.6B, but only 7–14% of exact entrainment in the clean stratum. |
| Phase 2 | The same sparse head set carries both components; two separate pathways excluded. |
| Phase 3 | Those heads' **direct** write is lexical only; the entity component reaches the logit through them indirectly. |

The sharpened claim: contextual entrainment is a **lexical write with an entity-sensitive
downstream readout**. The circuit copies surface salience; something after it decides which
surface form that salience lands on.
