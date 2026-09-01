# 044 Hard Re-Audit — 2026-09-01

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED — TWO-DIAGNOSTIC IDENTIFIABILITY REPAIRED**

## Frozen question

> Does a true property characterize an individual as such, or only a particular spatiotemporal stage of that individual?

## Why the audit mattered

The initial strict card correctly required two independent consequences but left the second diagnostic to be selected later from several possibilities. Under the post-5/5 gate that is under-frozen and risks metric shopping.

The second diagnostic is now fixed before GPU.

## External object and anti-duration requirement

IL/SL is a classic semantic distinction but cannot be equated with temporary/permanent.

Mandatory counterexamples include:

- stage-level treatment of long-lasting/permanent-looking properties (`estar muerto` / dead);
- temporally restricted descriptions that can occur with individual-level/`ser` configurations (`queen for a day`);
- same adjective with context/copula-induced IL-like vs SL-like readings.

If duration predicts the full effect, 044 fails.

## Exact frozen diagnostics

### Diagnostic 1 — SituationBoundLogit

Preference for a continuation that anchors the property to the current/relevant situation or stage versus an individual-characterizing continuation.

### Diagnostic 2 — DepictiveCompatibilityLogit

Depictive secondary predication is the fixed independent diagnostic. Classic linguistic work treats clear stage-level predicates as naturally compatible with depictive secondary predication, while clear individual-level predicates are degraded unless coerced to a stage reading.

Use only consensus-clear items/readings selected by linguistic criteria before model runs.

No switch to existential-there, lifetime effects, perception reports, or another diagnostic after results.

## N0 / N1 / N2

Older corpus semantics owns IL/SL labels and neural work owns neighboring aspect/event/habituality objects. Targeted searches found no direct neural/LLM study of a same-lexical context-conditioned IL/SL state with causal cross-surface transfer and two independent consequences.

Surviving N2:

> **an abstract predication-level state, distinct from property truth, duration and copula identity, that jointly controls situation anchoring and depictive compatibility.**

## Strict locks

```yaml
Lock_A_same_lexical_anti_duration: PASS
Lock_B_cross_setting_transfer: PASS
Lock_C_two_exact_diagnostics:
  - SituationBoundLogit
  - DepictiveCompatibilityLogit
  status: PASS
```

## Unified-object hard kill

The same causal `PredicationLevel` intervention must shift both diagnostics in the predicted direction while preserving `PropertyTruthLogit`.

If the two diagnostics systematically dissociate, the unified latent-object claim terminates. We do not report whichever diagnostic worked.

## Final verdict

```yaml
natural_object: PASS
N0_N1_N2: PASS
same_lexical_cross: PASS
anti_duration: PASS
strict_A: PASS
strict_B: PASS
strict_C: PASS
specificity_denominator: PropertyTruthLogit
metric_shopping_repair: PASS
PASS_REGISTER: true
GPU_AUTHORIZED: true
```

044 remains registered.