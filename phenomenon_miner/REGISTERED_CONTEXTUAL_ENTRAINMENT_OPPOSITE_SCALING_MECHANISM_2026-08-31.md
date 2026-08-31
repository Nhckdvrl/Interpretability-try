# PASS-REGISTER 05 — Why Bigger Models Ignore Lies but Copy Noise

Date: 2026-08-31  
Status: **PASS-REGISTER**  
Route: **B — established anomaly -> unasked causal computation**

## Natural question

Why does scaling make language models **better at resisting meaningful false context but worse at mechanically copying meaningless context**?

Does a larger model contain one increasingly strong copying mechanism that is selectively gated by semantics, two genuinely distinct circuits whose strengths scale in opposite directions, or a common upstream entrainment process whose competition/readout changes only late in the network?

## Behavioral mother

Kukreja et al., **Better and Worse with Scale: How Contextual Entrainment Diverges with Model Size**, Findings of ACL 2026.

Using the same contextual-entrainment object introduced by Niu et al. (2025), the mother measures the context-induced logit shift of a distractor token under four context types on two open scaling families:

- Cerebras-GPT: 111M–13B
- Pythia: 410M–12B

The behavioral result is a robust **sign split**:

- semantic contexts (`Counterfactual`, `Related`) show **negative scaling** of distractor entrainment;
- non-semantic contexts (`Random`, `Irrelevant`) show **positive scaling**.

The mother reports that the largest models are roughly four times more resistant to counterfactual misinformation while being about twice as prone to arbitrary-token copying, and the opposite trends replicate across both model families.

It also performs no-context baseline checks showing that gold-token capability scales uniformly and distractor-token salience without context does not explain the sign split.

Most importantly, the mother explicitly states in its limitations that it characterizes **behavioral scaling without mechanistic decomposition**, does not analyze heads/layers/circuits, and identifies as future work whether copying and filtering arise from distinct circuits with independent scaling properties.

## Mechanistic predecessor

Niu et al., **Llama See, Llama Do: A Mechanistic Perspective on Contextual Entrainment and Distraction in LLMs**, ACL 2025 Outstanding Paper.

This paper establishes that contextual entrainment itself is causal/mechanistic and identifies sparse **entrainment heads** using differentiable masking. Ablating these heads attenuates contextual entrainment. It also shows that semantic factors modulate entrainment magnitude.

That predecessor therefore closes the weak question `which heads cause entrainment?`.

It does **not** explain the 2026 discovery that semantic and non-semantic entrainment acquire opposite scaling exponents across model size.

## Why this is not a behavior lottery

The exact anomaly is already the mother’s headline result:

- two independent open model families;
- multiple sizes in each family;
- same token-level entrainment metric;
- semantic and non-semantic conditions on the same LRE-style factual-query object;
- strong power-law fits with opposite signs;
- no-context capability and distractor-salience controls already reported.

No new G0 is required to discover whether the sign split exists.

The Pythia ladder is fully open and particularly suitable for mechanistic comparison across scale.

## Exact scientific object

For a factual query with gold token `g` and context distractor `d`, the mother measures:

`Delta_d = logit(d | context) - logit(d | no context)`

The unit is therefore exactly the **context-induced causal/logit advantage of the same distractor token**, with context semantics manipulated while query and output vocabulary remain comparable.

The new object is not another benchmark error. It is the **internal decomposition that makes the same entrainment quantity scale with opposite signs as a function of semantic content**.

## Competing causal hypotheses

### H1 — Shared copying writer + scaling semantic gate

A common entrainment/copying circuit boosts previously seen tokens in every context, and this writer becomes stronger with scale. Larger models additionally develop a stronger semantic-conflict/filter mechanism that suppresses the writer only when the context has interpretable semantic relation to the query.

Predictions:
- entrainment-head causal effect grows with scale in both semantic and non-semantic conditions before filtering;
- large-model semantic conditions recruit an additional filter/memory pathway;
- ablating the semantic gate in large models should make Counterfactual/Related contexts move toward the positive scaling profile of Random/Irrelevant contexts;
- ablating the shared entrainment writer should attenuate both classes.

### H2 — Distinct copying and filtering circuits

Mechanical copying and semantic filtering are implemented by separable circuit families whose causal strengths scale independently.

Predictions:
- head/pathway overlap between non-semantic copying and semantic suppression is low or systematically decreases with scale;
- selective ablation yields a double dissociation;
- copying-circuit strength increases with parameter count while semantic-filter strength independently increases enough to reverse the net semantic effect.

### H3 — Common upstream entrainment, late competition/readout

The same upstream entrainment mechanism operates similarly across conditions; the apparent sign split emerges only from late competition with parametric memory / contextual answer pathways or residual-stream readout geometry.

Predictions:
- early/middle causal contribution profiles remain similar across semantic and non-semantic contexts and across scale;
- divergence appears late;
- late residual/pathway patching can switch the semantic condition toward the random-context logit effect without changing earlier entrainment states.

These hypotheses make different causal predictions and directly test the behavioral mother’s proposed functional interpretation.

## Core experiment

### 1. Reproduce the mother’s metric, not a new benchmark

Use the exact LRE-style items and four context conditions. Primary mechanistic ladder: Pythia sizes used by the mother; replicate key results on Cerebras-GPT if tooling permits.

### 2. Scale-conditioned entrainment-head discovery

Adapt the ACL 2025 differentiable-mask recipe separately for `Random/Irrelevant` and `Counterfactual/Related` conditions at multiple Pythia sizes.

Measure:
- circuit overlap;
- causal effect size after ablation;
- layer distribution;
- normalized causal strength vs model size, rather than raw head count alone.

### 3. Semantic-filter difference-in-differences

Construct matched pairs preserving query and, where possible, distractor identity while changing only whether the contextual occurrence carries semantic relation/conflict.

Localize components whose intervention effect is specifically:

`(semantic - no-context) - (nonsemantic - no-context)`

rather than generic copying.

### 4. Decisive interventions

- Ablate candidate semantic-filter components in large models: does counterfactual entrainment revert toward the positive non-semantic scaling regime?
- Ablate entrainment heads: does the positive random-copying scaling law collapse, and how much semantic entrainment remains?
- Patch semantic -> non-semantic and reverse at candidate layers while holding the query/distractor constant.
- Test memory/context-head pathways as a competing late-control account.

The paper must explain the **sign reversal**, not merely report different head sets.

## Fatal controls

- Use the mother’s exact logit-shift metric; do not replace the scientific object with accuracy.
- Preserve no-context controls so general capability scaling cannot masquerade as filtering.
- Preserve distractor identity where possible across semantic/non-semantic matched interventions; control token frequency and baseline logit.
- Compare normalized intervention effects across differently sized architectures; raw number of heads is not a valid scaling measure.
- Require causal ablation/patching; probe separability alone does not establish two circuits.
- Include both semantic conditions and both non-semantic conditions so the result is not a Counterfactual-vs-Random one-off.
- A component called an entrainment head in the 2025 recipe does not automatically count as a new discovery; novelty lies in the **factorization and scaling law of causal computations**.

## Strongest-neighbor audit

### ACL 2025 Outstanding — `Llama See, Llama Do`

Directly owns generic contextual entrainment mechanism and entrainment-head localization/ablation. Therefore this candidate explicitly excludes `find entrainment heads` as a contribution.

### 2026 `Sentence-Level Contextual Entrainment in Large Language Models`

Extends entrainment to sentence-level probability across many models and reports that a small percentage of attention heads controls the phenomenon. It does not analyze the mother’s **opposite semantic-vs-nonsemantic scaling sign split** or causally decompose copying from semantic filtering across a scale ladder.

### Knowledge-conflict memory/context-head work

Provides an important competing mechanism for factual context-vs-parametric-memory competition, but does not explain why arbitrary non-semantic copying strengthens while semantic distraction weakens under scale on the same contextual-entrainment metric.

### Mother’s own limitation

The Findings ACL 2026 mother explicitly states that its analysis is behavioral and lacks mechanistic decomposition, specifically proposing future work on whether copying and filtering arise from distinct circuits with independent scaling properties.

A fresh direct-neighbor search through August 2026 did not find a paper that closes this exact causal scaling question.

## Anti-narrowing / ACL–EMNLP narrative

The paper-level question is broader than contextual entrainment heads:

> **Does model scaling improve contextual judgment by suppressing a copying reflex, or does it strengthen both the reflex and a separate semantic control system?**

This distinction matters for:
- retrieval-augmented generation;
- noisy and adversarial context;
- misinformation robustness;
- long-context systems;
- scaling laws for internal mechanisms;
- whether larger models become globally less distractible or merely more selectively distractible.

All principal outcomes are scientifically meaningful:
- H1: scaling strengthens a low-level copying primitive and independently strengthens a semantic gate;
- H2: two causal systems have opposing internal scaling laws;
- H3: the split is a late competition/readout effect, falsifying the mother’s natural distinct-circuit interpretation.

## Registration decision

**PASS-REGISTER.**

Reason: strong 2026 behavioral mother + ACL Outstanding mechanistic predecessor + exact open-model scale ladders + pre-established opposite-sign anomaly + mother explicitly leaves the causal decomposition open + three mutually distinguishable mechanisms + causal interventions that explain a scaling paradox rather than merely localize another head.
