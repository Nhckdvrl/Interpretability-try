# 014 — Scale axis (contract amendment r1c)

**Status:** descriptive / generality. This axis carries **no promote or kill authority**;
phase 1 had already returned `PROMOTE`. Its job was to decide which of two pre-declared
stories the paper tells, and both readings were written down before any rung was run.

**Data:** `data/frozen_d0.jsonl`, unchanged. **Metric:** unchanged.
**Ladder:** Qwen3 at 0.6B / 1.7B / 4B / 8B / 14B / 32B (one family, one tokenizer, one
recipe), plus Gemma-3 4B/12B as a two-point secondary.

Capability grows with scale, so every rung gates a different item set and a naive
across-size comparison is confounded. The pre-registered **primary readout is therefore
the common gated set** — the 71 items every rung of the ladder passes — with each
model's own gated set reported alongside.

---

## 1. Qwen3 ladder

### Primary — common gated set (71 items, 27 of them `opaque_strict`)

| params | own gate rate | `EXACT` | `ALIAS−SEMREL` | `ALIAS−SEMREL` (strict) | transfer ratio (strict) |
|---:|---:|---:|---:|---:|---:|
| 0.6B | 0.32 | 9.92 | 2.17 | 0.96 | 0.097 |
| 1.7B | 0.71 | 11.47 | 2.79 | 0.96 | 0.076 |
| 4B | 0.82 | 13.06 | 2.35 | 1.07 | 0.081 |
| 8B | 0.81 | 15.74 | 3.26 | 2.08 | 0.143 |
| 14B | 0.91 | 14.81 | 2.94 | 1.67 | 0.127 |
| 32B | 0.91 | 13.62 | 2.61 | 1.98 | 0.164 |

### Secondary — each model's own gated set

| params | n gated | n strict | `EXACT` | `ALIAS−SEMREL` (strict) | transfer ratio (strict) |
|---:|---:|---:|---:|---:|---:|
| 0.6B | 95 | 32 | 9.96 | 1.03 | 0.095 |
| 1.7B | 212 | 98 | 12.08 | 0.77 | 0.077 |
| 4B | 246 | 109 | 12.70 | 0.68 | 0.063 |
| 8B | 244 | 103 | 15.21 | 0.83 | 0.068 |
| 14B | 273 | 124 | 14.52 | 0.80 | 0.069 |
| 32B | 274 | 123 | 13.49 | 0.94 | 0.093 |

### Trends (Spearman vs log₁₀ params, exact permutation p, n = 6 rungs)

| series | rho | exact p |
|---|---:|---:|
| transfer ratio, strict — **common set** | +0.771 | 0.103 |
| `ALIAS−SEMREL`, strict — common set | +0.771 | 0.103 |
| `EXACT` — common set | +0.771 | 0.103 |
| transfer ratio, strict — own gated set | −0.200 | 0.714 |
| **alias-knowledge gate rate** | **+0.943** | **0.017** |

With six rungs, |rho| must reach 0.886 for p < 0.05. **The only trend that clears
significance is the capability gate.**

## 2. Gemma-3 (two rungs, descriptive only)

| params | own gate | `EXACT` | `A−S` strict (common set, n=101) | transfer ratio (strict) |
|---:|---:|---:|---:|---:|
| 4B | 0.84 | 16.54 | 1.04 | 0.088 |
| 12B | 0.91 | 18.57 | 1.92 | 0.175 |

Same direction as Qwen3's weak upward trend, but two points cannot establish one.

## 3. Reading

Against the two readings frozen in advance, the result sits closer to
`reading_if_flat_or_falling`, with an honest caveat that it is **underpowered between
"flat" and "mildly rising"**:

1. **The entity-level component is not emergent.** At 0.6B, on the items that model
   actually knows, the alias component is already ~0.10 of exact-form entrainment —
   the same share as 32B on its own gated set (0.093). Whatever this mechanism is, a
   0.6B model already has it. It is not a large-model capability.

2. **On matched items the absolute effect roughly doubles** (0.96 → 1.98 nats), and the
   share rises from 0.097 to 0.164 — but rho = +0.771, p = 0.103, non-monotone, and
   resting on only 27 strict items. This is suggestive, not a finding, and must not be
   reported as "transfer increases with scale".

3. **On each model's own gated set the share is flat** (0.063–0.095, rho = −0.200,
   p = 0.714). Per the contract this readout could not be substituted for the primary,
   and it is reported here because the contract required it be shown alongside.

4. **What unambiguously scales is knowledge, not mechanism.** The alias-knowledge gate
   goes 0.32 → 0.91 (rho +0.943, p = 0.017) — the single significant trend on this axis.
   Bigger models do not entrain aliases *more efficiently*; they know *more aliases*.

## 4. Consequence for the paper

The scale story is about coverage, not about a change in mechanism, which is the cleaner
narrative: the entity-level component of contextual entrainment is a **structural**
property present from 0.6B upward, and scale mainly determines how many alias pairs fall
inside it.

This is also worth stating against [*Better and Worse with Scale*](https://arxiv.org/abs/2604.13275),
which reports that entrainment from *semantic* contexts systematically decreases with
scale. The alias component here does not decrease; if anything it mildly increases. The
two are not in direct contradiction — that paper measured exact-token entrainment under
semantically related contexts, not unseen-alias transfer — but the contrast is reportable
and is a natural thing for a reviewer to ask about.

## 5. Limits

- The common gated set has only 27 `opaque_strict` items, because 0.6B gates just 95/300.
  Every common-set number in §1 rests on that thin cell.
- Instruction-tuned Qwen3 checkpoints only; no base models, so tuning is not separated
  from scale.
- Six rungs is the practical floor for a rank correlation; nothing here should be read as
  a scaling law.
