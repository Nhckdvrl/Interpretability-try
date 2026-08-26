# 002 — Dominated decoy dissociation

**Status: PRE-CANDIDATE**  
**Stage: Frozen behavioral G0 only. Do not start mechanism work before promotion.**

## Mother question

> Why can an option that a language model correctly recognizes as strictly dominated, and almost never chooses, still causally reverse its preference between two other options?

The phenomenon is the classic attraction/decoy effect, but this project targets a stricter item-level dissociation:

1. With only `{A, B}`, the model clearly prefers the competitor.
2. The inserted decoy `C` is strictly dominated by the target and the model explicitly recognizes that fact.
3. The model assigns little probability to choosing `C` itself.
4. Nevertheless, adding `C` reverses the model's preference from the competitor to the target.

If this coexistence is not stable in modern open-weight models, kill the project before any interpretability analysis.

## Prior behavioral basis

This G0 is motivated by existing public behavioral work rather than by a hidden-state hypothesis:

- Itzhak et al., **Instructed to Bias: Instruction-Tuned Language Models Exhibit Emergent Cognitive Bias**, TACL 2024. Public data/generator: `itay1itzhak/InstructedToBias`.
- **Irrelevant Alternatives Bias Large Language Model Hiring Decisions**, Findings of EMNLP 2024. Independent evidence for attraction effects in a hiring/qualification setting.

Those papers establish the broad phenomenon, not our stricter same-item dissociation.

## Frozen G0 design

### Unit of analysis

A base choice contains two non-dominated alternatives:

- `A`: lower cost, lower quality
- `B`: higher cost, higher quality

For every base choice we create mirror treatments:

- `C_A`: strictly worse than `A` on both displayed attributes
- `C_B`: strictly worse than `B` on both displayed attributes

The mirror design prevents a fixed preference for one side of the price/quality tradeoff from masquerading as an attraction effect.

### Domains

First pass: phone, car, frying pan, apartment. These follow the two-attribute price/quality paradigm in prior decoy work. Numerical tradeoffs and three decoy strengths are generated programmatically, so dominance gold is exact and requires no annotation.

Do **not** add more domains to rescue a failed G0.

### Prompt controls

Every scenario is evaluated with:

- 3 semantically equivalent choice templates;
- all 2 binary option permutations;
- all 6 ternary option permutations;
- 2 orderings of the direct dominance check.

Choice scores are deterministic teacher-forced likelihoods for complete candidate strings. We do not assume `A/B/C` are single tokenizer tokens and do not use sampling as the primary metric.

### Gates

A scenario is eligible only if:

- **Dominance gate:** the target beats its decoy with probability `>= 0.80` in both direct dominance orderings.
- **Decoy rejection gate:** maximum probability assigned to choosing the decoy across ternary variants is `<= 0.10`.

Among gated items, a **strong reversal** requires:

- binary competitor probability `>= 0.60`;
- after adding the target-dominated decoy, target probability renormalized over `{target, competitor}` is `>= 0.60`;
- both conditions hold for at least `2/3` of their respective prompt/order variants.

Primary endpoint: number/rate of strong reversals among gated scenarios.  
Secondary endpoint: mean item-level target-probability shift (`attraction_delta`) among gated scenarios.

The ternary target probability is renormalized over A/B only to isolate the A/B preference shift; the separate decoy-rejection gate prevents hiding meaningful mass on C.

## Frozen promotion / kill rule

Run in order:

1. `Qwen/Qwen3-8B`
2. `google/gemma-3-12b-it`
3. `Qwen/Qwen3-14B` as confirmation after the first two

Promote **PRE-CANDIDATE → ACTIVE** only if the first pass shows:

- effect in at least 2 open-weight models;
- at least 2 domains per passing model;
- at least 50 strong-reversal scenarios per passing model;
- strong-reversal rate among gated scenarios `>= 5%` per passing model;
- positive mean attraction delta in every domain used to claim generality.

**KILL** if the effect appears only under one template/order, one model family, or only after weakening gates. Do not rescue it with weaker models, cherry-picked decoy strengths, or a new benchmark.

These are scientific promotion gates, not significance tests. If G0 passes, the mechanism stage should add paired bootstrap CIs/permutation tests on item-level deltas.

## Why a passing G0 would matter

A positive item simultaneously says:

> “The model knows C is worse than the target.”  
> “The model does not want C.”  
> “But merely seeing C changes what it wants between A and B.”

That creates several genuinely different mechanism hypotheses:

- contextual normalization rewrites the target's latent value;
- a correct local dominance computation gives the target an inappropriate comparison bonus;
- A/B values remain stable but late arbitration/readout changes;
- instruction tuning installs a comparison heuristic absent or weaker in base models.

These predict different interventions and different repair methods. None should be pursued before G0 passes.

## Usage

```bash
cd projects/002_decoy_dissociation
python -m pip install -e '.[test]'
pytest -q

# Generate frozen scenario bank.
decoy-generate --out data/scenarios.jsonl

# Smoke test.
decoy-run \
  --model Qwen/Qwen3-8B \
  --data data/scenarios.jsonl \
  --out results/qwen3_8b_smoke.jsonl \
  --limit 20

decoy-summarize \
  --data data/scenarios.jsonl \
  --results results/qwen3_8b_smoke.jsonl \
  --out results/qwen3_8b_smoke_summary.json

# Full G0: remove --limit and repeat on Gemma 3 12B IT.
```

## Expected scale

With the frozen grids and 3 decoy strengths, the generator creates thousands of mirror target-decoy scenarios. Each scenario expands to 26 deterministic evaluations:

- 6 binary choice cases (3 templates × 2 orders)
- 18 ternary choice cases (3 templates × 6 orders)
- 2 dominance checks

This is intentionally large enough for item-level filtering while keeping all gold structure programmatic.

## Non-goals at G0

Do not add probes, SAE features, attention-head searches, activation patching, steering vectors, fine-tuning, or mitigation methods before promotion.
