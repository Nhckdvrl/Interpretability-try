# Mechanistic Interpretability Topic Search — Handoff (2026-08-31)

Status: **NO NEW PASS-REGISTER SURVIVOR YET. SEARCH MUST CONTINUE; DO NOT PAD TO FIVE.**

This handoff is the authoritative continuation point for the current ACL / EMNLP / NAACL-style mechanistic-interpretability topic search. The user ultimately wants **five genuinely hard topics**, but quantity never overrides the gates. If only 0–3 pass, keep searching rather than lowering the bar.

---

## 0. Read these first, in this order

1. `README.md`
2. `phenomenon_miner/NATURAL_QUESTION_GATE.md`
3. `phenomenon_miner/SCIENTIFIC_SUBSTRATE_GATE.md`
4. `phenomenon_miner/S0_FUNNEL_2026-08-31.md`
5. `phenomenon_miner/FAILED_TOPICS.md`
6. `archive/README.md`
7. `rejected_candidates/README.md`
8. all relevant domain logs in `rejected_candidates/`, especially:
   - `semantic_pragmatic_factorization.md`
   - `hamdi_search_addendum_2026-08-31.md`
   - `hamdi_search_terminal_addendum_2_2026-08-31.md`
   - `risk_uncertainty_factorization.md`
   - `social_norm_factorization.md`
   - `social_simulation_factorization.md`

Internal negative evidence outranks an attractive external mother. A different dataset/model/prompt/language/MI method does not revive a dead scientific object.

---

## 1. Search philosophy to preserve

The desired pattern is Hamdi-style **scientific-object selection**, not generic MI brainstorming.

### Template A — natural behavior → internal object

Example from `#r_hamdi` arbitrary/random-choice work:

```text
ordinary behavior: arbitrary choice is visibly biased
→ does the model represent “I am in arbitrary-choice mode”?
→ reader switch or entropy dial?
→ reader and writer separate?
→ causal gating / intervention
```

The behavior exists before the SAE/probe.

### Template B — mother axis A → naturally orthogonal axis B

Example entity line:

```text
knowledge / familiarity ≠ ontology / real-world existence
```

The two variables are independently meaningful in the world. Even perfect factorization would still be scientifically informative.

### Forbidden rescue pattern

```text
mother establishes behavior/object
→ nobody patched it yet
→ call patching the novelty
```

or

```text
dataset has two labels
→ train two probes
→ call the labels new scientific objects
```

Both have produced many deaths in this repository.

---

## 2. Mandatory funnel

```text
generate many internally
→ Natural Question Gate
→ classify Type 1 failure-mechanism or Type 2 factorization/object
→ S0 Scientific Substrate
→ open-model capability/existence sanity where required
→ N0 mother inclusion
→ N1 strongest-neighbor/successor attack
→ internal-history collision audit
→ ACL/EMNLP narrative-width audit
→ MI-fit / competing-mechanism audit
→ anti-narrowing audit
→ only then PASS-REGISTER
```

### Type 1 failure-mechanism

Before registration:
- failure must already occur on analyzable open checkpoints;
- default at least 2/3 modern open families in same direction;
- ordinary faithful prompts, not post-hoc filtered/synthetic cells;
- substantive effect, not tiny significance.

### Type 2 factorization/object

Before registration:
- both axes have independent external definitions;
- central gold is source/human/expert/program/database grounded;
- row-level artifact is actually obtained and parsed;
- decisive natural cross-cells are actually counted;
- random >=20 source rows manually sanity-checked;
- no new central manual labels, no LLM-judge primary gold;
- separation and non-separation both tell a title-level story.

---

## 3. Current surviving leads — NOT registrations

### Lead A — World Truth ≠ Collective / Popular Belief

**Plain question**

> Does a model separately know what is true and what people tend to believe is true, or does popularity of a belief leak into its world model?

This is deliberately **not** `Mary believes p` / first-person belief attribution. The proposed second axis is **empirical population belief prevalence / perceived truth**, i.e. a social model of what ordinary people accept.

**Why it remains alive**

- `TruthfulQA` established imitative falsehoods: models reproduce popular human misconceptions.
- Allen et al., Science Advances 2021 provides a promising natural same-item substrate: **207 Facebook-flagged news articles**, **3 professional fact-checkers** who researched every article, and **1,128 US laypeople** who rated headline+lede accuracy; roughly ~100 lay ratings/article. Thus the same natural claim can carry expert-grounded veracity and population perceived-accuracy.
- Data/materials are declared public at `https://osf.io/hts3w/`.
- Preliminary N1 search did **not** find a direct causal MI paper on `world truth × collective belief prevalence`.

**Strongest danger**

Suzgun et al., Nature Machine Intelligence 2025, **Language models cannot reliably distinguish belief from knowledge and fact**, KaBLE: 13,000 questions / 13 epistemic tasks / 24 models. It owns `belief vs fact` broadly for attributed mental states.

Also dangerous:
- TruthfulQA / truth directions / truthfulness steering are crowded;
- ICLR 2026 opinion-distribution work decodes and steers human opinion distributions.

**N0 question that must be answered before proceeding**

Is `collective belief prevalence` genuinely a different scientific object from KaBLE's binary attributed belief, or is “popular/collective” merely the adjective that keeps `belief vs fact` alive? Do not assume PASS.

**Immediate S0 blocker**

The OSF page is publicly cited but normal web access returned 403 in this session. **Do not count the paper-level N=207 as S0.** Obtain the row artifact by OSF API/download/mirror, inspect schema, compute:

```text
expert true  × crowd-high-belief
expert true  × crowd-low-belief
expert false × crowd-high-belief
expert false × crowd-low-belief
```

Thresholds must be frozen before looking at the cell counts. Also inspect continuous disagreement, not only arbitrary median bins.

Random-audit >=20 articles. Check whether crowd ratings measure `truth belief` rather than publisher trust/style. Check whether disagreement cells are numerous enough; the mother reports high crowd–factchecker agreement, so S0 may still die for sparse discordant cells.

**Potential mechanistic forks if and only if S0+N0+N1 pass**

1. one truth-like scalar contaminated by social frequency;
2. separate world-truth and social-belief representations;
3. shared proposition content plus separate truth/social-model readers.

A decisive intervention must change predicted human belief without changing the model's own factual answer, and vice versa.

**Current verdict:** `HOLD-S0-N0`.

---

### Lead B — Causal Direction ≠ Causal Magnitude in Social-Intervention Prediction

**Plain question**

> A model can often tell whether an intervention pushes people up or down, yet systematically predicts that it moves them much more than it really does. Are effect direction and effect magnitude separate computations?

**Mother**

Ashokkumar et al., Nature 2026, **Large language models can predict the results of social science experiments**:
- 70 preregistered nationally representative US survey experiments;
- 469 experimental effects;
- 119,330 human participants;
- LLM predictions strongly correlate with real effects, including open-weight models;
- predicted effect sizes are systematically too large.

This behavior is much stronger than a synthetic statistics benchmark.

**Fatal alternative that blocks registration now**

Lin et al. 2026, **The Illusion of Intervention: Your LLM-Simulated Experiment is an Observational Study**, shows `user drift`: treatment prompts can change the latent simulated persona/population across treatment conditions. This confounding can inflate or attenuate apparent treatment effects. Negative-control outcomes and targeted persona/confounder specification can reduce the bias.

Therefore `sign roughly right / magnitude too large` cannot yet be interpreted as an internal sign-vs-magnitude factorization problem.

**Required pre-registration control**

Reproduce magnitude inflation on open models **after a user-drift / negative-control correction that preserves the target intervention**. If the magnitude excess disappears, `KILL-ARTIFACT` immediately.

Even if it survives, redo N0: the Nature mother already reports direction/correlation and effect-size inflation. The project must show that `qualitative causal direction vs quantitative causal strength` is a new scientific object, not merely “mechanism of the mother result.”

**Potential forks only after the fatal control**

1. one generic intervention-strength signal;
2. separate sign and magnitude channels;
3. correct sign representation but social-simulation gain/readout exaggerates magnitude.

**Current verdict:** `HOLD-FATAL-CONTROL + N0-REAUDIT`.

---

## 4. Recently killed attractive leads — do not re-search

Full reasons live in rejection logs. Important newest deaths:

- `Assertion ≠ Presupposition` — `KILL-DATA`: no broad natural same-proposition asserted/presupposed double-status artifact; constructed counterparts are synthetic central contrast.
- `Polysemy ≠ Homonymy` — `KILL-NOVELTY`: recent lexical-ambiguity representation work already owns the object.
- `Coreference ≠ Bridging` — `KILL-N0`: GUMBridge mother owns identity-vs-associative reference; MI would be direct follow-up.
- `Prevalence ≠ Diagnosticity` — `KILL-DATA`: direct double-gold norms too small; larger feature-production norms are not real-world prevalence.
- `Statistical significance/evidence ≠ effect magnitude` — `KILL-MI-FIT`: excellent empirical-data substrate (BEAR/SCORE) but no established natural open-model conflation; with explicit statistics it risks being trivial number parsing.
- `Knowing the answer ≠ knowing what a novice would know` — `KILL-N0`: ACL 2026 mothers already explicitly own intrinsic capability vs human difficulty / proficiency simulation and call it curse of knowledge.
- `Claim content ≠ claim scope` — `KILL-N0`: 2025 scientific-summarization mother already owns scope overgeneralization.
- `Wrong ≠ Illegal` — `KILL-N0`: Social Chemistry 101 explicitly defines and models moral judgment, legality and other social-norm dimensions jointly.
- `Average opinion ≠ population diversity` — direct ICLR 2026 internal opinion-distribution decoding + SAE + steering collision.
- `Likelihood ≠ severity` — direct 2026 expected-harm decomposition/probing collision.
- `Epistemic ≠ aleatoric uncertainty` — direct internal-probe/decomposition literature.
- `Givenness/local accessibility ≠ global salience` — 2026 mother owns the local-prominence-vs-global-salience object.
- `Taxonomic ≠ thematic`, `animacy ≠ agentivity`, `agency ≠ experience`, sarcasm intent/perception, literal/figurative, emotion/cause — all frozen in domain logs.

Do not resurrect any of these by changing dataset/model/tool.

---

## 5. High-priority search strategy for the next session

Do **not** start by searching more pairs of linguistic labels. The yield was poor because N0 immediately turns them into `existing taxonomy → MI`.

Prioritize these mother shapes:

### Search lane 1 — Stable behavioral mismatches where two readouts disagree

Look for strong 2025–2026 ACL/EMNLP/NAACL/ICLR/ICML/NeurIPS papers showing, across modern open models:

```text
A behavior is correct in one natural sense
but systematically wrong in another natural sense
```

The mismatch itself must be the natural phenomenon, not a benchmark filter.

Examples of search forms (not candidate claims):
- right ranking but wrong calibration/scale;
- correct relation but wrong boundary/scope **only if mother does not already own scope**;
- correct object/content but wrong source/world/social attribution **only with natural gold**;
- correct individual prediction but wrong aggregate structure, or reverse, **only if not covered by opinion-distribution work**.

### Search lane 2 — World variable vs social variable

This is the most promising analogue to Hamdi `knowledge ≠ ontology`.

Look for the same natural units with independent objective/world labels and independent human-population labels:
- truth vs collective belief;
- actual behavior vs perceived norm (not synthetic norm messages);
- observed prevalence vs normative approval;
- expert classification vs public conceptualization.

But N0 must ensure this is not simply `belief vs fact`, `descriptive vs normative`, or another dead family.

### Search lane 3 — Mother-paper unexplained reversal, not merely a gap

Look for authors explicitly reporting a **reversal/backfire/paradox** across open families but not providing an internal account. The mechanism should pose at least 2–3 plausible competing computations. Avoid synthetic-only induction pipelines.

### Search lane 4 — Strong natural databases with independently authored axes

Only after a natural question already exists, look for:
- real-world databases;
- expert + public judgments on same units;
- human behavioral records plus source/expert gold;
- deterministic program/database oracles.

Do not let a two-column schema create the question.

---

## 6. Search findings that were considered but should not become leads without re-audit

- ACL 2026 `Do Emotions Influence Moral Judgment in LLMs?` reports emotion-induced moral reversals up to 20%, but the core emotion infusion is a researcher-generated manipulation; it is high risk under failure S0 and the mother itself owns emotion→moral judgment.
- 2026 personality-measurement instability is questionnaire/order sensitive and risks a measurement-object problem.
- self-consistency backfire on GPQA exists for small Qwen/Llama in a workshop paper, but the repository already contains weak-evidence/backfire and selection-effect negative history; do not promote without a fresh naturalness/internal-collision audit.
- temporal forgetting is explicitly forbidden internal-history territory.
- culture/language stance differences collide with the repository’s language/culture disentanglement kill.

---

## 7. Required final output for every true survivor

Do not output a lightweight shortlist. Every survivor must contain all 20 fields:

1. Plain question
2. One example
3. Why this matters
4. Topic type
5. Mother paper
6. Hamdi-style extension
7. S0 Scientific Substrate — actual artifact URL, schema, objective gold, total N, exact label/cross-cell counts, matched counts if relevant, random-20 audit, attrition, restriction budget, new annotation requirement
8. Open-model viability / failure existence
9. N0 mother-inclusion audit
10. N1 strongest neighbors (>=3, including 2025–2026/arXiv)
11. Internal-history audit
12. Exact novelty
13. Forbidden claims
14. Mechanistic forks (>=2–3)
15. Decisive causal experiment
16. Fatal controls
17. ACL/EMNLP title
18. Four-sentence abstract skeleton
19. Anti-narrowing verdict under all required constraints
20. Final verdict: only `PASS-REGISTER`, `HOLD-SUBSTRATE`, `KILL-NOVELTY`, `KILL-NATURALNESS`, `KILL-CAPABILITY`, `KILL-DATA`, `KILL-INTERNAL-COLLISION`

`PASS-REGISTER` is allowed only after actual row-level S0 and N0/N1 are complete. Paper-level sample counts are never S0 counts.

---

## 8. Target for the continuation

The user asked for **five sufficiently hard topics**. Interpret this as:

> Keep searching until five topics genuinely pass the gates; never manufacture five by weakening the gates.

Current registered-new-topic count from this search: **0**.

Current serious leads worth immediate work: **2**, both HOLD, neither allowed to register yet.

If the two current leads die, write their terminal reasons into `rejected_candidates/` before searching replacements.

---

## 9. Useful external references to begin from

- Allen et al. 2021, *Scaling up fact-checking using the wisdom of crowds*: https://pmc.ncbi.nlm.nih.gov/articles/PMC8442902/ ; data: https://osf.io/hts3w/
- Suzgun et al. 2025, *Language models cannot reliably distinguish belief from knowledge and fact*: https://www.nature.com/articles/s42256-025-01113-8
- Lin et al. 2022, TruthfulQA: https://aclanthology.org/2022.acl-long.229/
- Ashokkumar et al. 2026, *Large language models can predict the results of social science experiments*: https://www.nature.com/articles/s41586-026-10742-x
- Lin et al. 2026, *The Illusion of Intervention*: https://arxiv.org/abs/2605.20767
- Hamdi Slack channel: `#r_hamdi` (`C0ATPT9P8SV`) — specifically inspect the arbitrary-choice reader/writer thread and entity knowledge/ontology project for **selection logic**, not for methods to copy.

---

# One-line handoff

> Continue searching from natural scientific objects; kill aggressively at S0/N0/N1; record every real death; and do not call anything a candidate merely because a dataset has two labels or because a mother paper has not yet been activation-patched.
