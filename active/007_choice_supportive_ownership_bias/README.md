# 007 — From answer visibility to ownership-specific commitment

**Status:** `ACTIVE-MECHANISM / REFRAMED AFTER G0`
**Validated:** 2026-08-27

## Revised mother question

The initial universal wording—“the same old answer selectively resists revision only when labeled as the model's own”—is too broad.

The supported question is:

> Why does a visible prior answer become a self-specific commitment in some model/task combinations, but a source-agnostic anchor in others?

This retains the natural choice-supportive phenomenon while making the observed cross-model boundary part of the explanandum rather than hiding it.

## Logic corrections

The first sensor scaffold had two problems: 12 greedy A/B decisions had almost no resolution, and an answer attributed to another model could rationally be treated as independent evidence. The corrected evaluation uses:

- full A/B continuation likelihoods;
- exact assistant-role serialization of the actual first answer versus `xx`, matching the published stateless protocol;
- neutral trials to isolate answer visibility from new evidence;
- opposing-evidence trials;
- an explicit other-model attribution condition;
- a 160-item GeoNames latitude replication with stage-one accuracy near the published target range;
- a synthetic sensor control to expose task dependence.

## Decisive latitude results

| Model | Stage-1 acc. | Own boost vs hidden (neutral) | Own−other (neutral) | Revision hidden | Revision own | Revision other |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-8B | 76.3% | +0.0146 | +0.0318 | 5.46% | 0.0007% | 5.63% |
| Gemma3-12B-IT | 85.0% | +0.0252 | +0.00004 | 19.47% | 0.0004% | 0.080% |

Qwen shows the strong ownership-specific contrast: other≈hidden while own nearly eliminates revision. Gemma shows a different phenotype: both own and other visible answers nearly eliminate revision, so its effect is source-agnostic anchoring under this local protocol. The synthetic sensor control is weaker and confirms that the phenotype is context dependent rather than a universal fixed bias.

## What survives and what does not

- **Does not survive:** a universal claim that all modern models uniquely protect self-authored answers.
- **Survives strongly:** visible prior answers causally gate later updating.
- **Novel mechanism target:** why attribution is source-selective in Qwen but source-agnostic in Gemma, and where that difference enters evidence integration.

This is aligned with the width of an ACL/EMNLP/NAACL mechanistic paper if kept to the Own/Other/Hidden causal contrast across two controlled task families. It should not be broadened into generic sycophancy, confirmation bias, or all forms of self-consistency.

## Files

- `g0.py` — synthetic sensor control with exact likelihood scoring;
- `latitude_g0.py` — GeoNames replication of the stateless shown/hidden/other protocol;
- `data/cases.jsonl`, `data/latitude_cases.jsonl` — frozen generated cases;
- `results/` — complete Qwen/Gemma runs and summaries;
- `tests/` — role serialization, evidence matching, and metric tests.

The latitude cases are deterministically derived from the GeoNames `cities15000` dump (`https://download.geonames.org/export/dump/cities15000.zip`, GeoNames data licensed under CC BY 4.0); the downloaded source archive is not vendored.

## Next step

Localize the visible-answer effect first, then test whether the causal component responding to assistant-role ownership differs from the component responding to any displayed answer. Add one non-latitude factual/reasoning dataset before making a task-general paper claim.
