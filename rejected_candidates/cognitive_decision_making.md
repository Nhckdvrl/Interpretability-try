# Rejected Candidates — Cognitive Decision-Making Biases

**Domain:** economic choice, legal judgment, anchors, authority, risk, sunk cost, framing-style decision biases.  
**Status:** active breadth-first scan; strong survivors are kept outside this rejected log until killed.

---

## 1. Generic authority / expert-hint override

**Natural question:** Why does the model abandon a correct answer when the same wrong suggestion is attributed to a more authoritative person?

**Why it initially looked good:** The graded authority hierarchy is natural, safety-relevant, and creates a clean conflict between factual evidence and social source cues.

**Kill evidence:** `A Mechanistic View of Authority Hierarchy in LLM Sycophancy` (July 2026) directly mechanizes this exact phenomenon across Llama-3.1-8B, Qwen3-8B, and Gemma-2-9B. It reports a graded authority effect and localizes a late-layer process in which correct-answer representations are actively erased in proportion to perceived authority, with causal/intervention analyses. The proposed mother question is therefore occupied, not merely behaviorally adjacent.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Judge vs doctor vs professor vs manager personas, medical vs legal QA, or calling the effect “authority anchoring” does not create novelty.

**Resurrection condition:** Need a distinct non-sycophancy phenomenon where authority changes a different computation despite the factual representation remaining causally intact.

**Key reference:** https://arxiv.org/abs/2607.00415

---

## 2. Generic numerical anchoring in judgment

**Natural question:** Why does an irrelevant number pull an LLM's estimate or judgment toward it?

**Why it initially looked good:** Classic, intuitive cognitive bias with real deployment consequences; easy matched-pair G0 and potential separation between initial estimate and anchor integration.

**Kill evidence:** By 2026 the behavioral space is crowded: anchoring has been repeatedly benchmarked, recent work characterizes dependence on model confidence / post-training, and legal studies test authority-conditioned anchors. More importantly, combining anchoring with an authority cue now approaches the direct mechanism collision above. A generic “find anchor direction / heads and suppress them” paper has insufficient narrative headroom and low surprise.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Sentencing anchors, prices, arbitrary IDs, high/low anchors, plausible anchors, or another domain are the same broad mother question.

**Resurrection condition:** Need a sharp, counterintuitive subtype with a decisive contrast not explained by generic confidence, plausibility, or authority weighting, and with mechanism-dependent repair.

---

## 3. Generic certainty effect / risk-aversion representation

**Natural question:** Why does a model disproportionately prefer a guaranteed outcome over a risky option with higher expected value?

**Why it initially looked good:** Very natural economic phenomenon; public code/data exist from `Instructed to Bias`; instruction tuning appears to amplify the effect, making post-training mechanism tempting.

**Kill evidence:** The broader risk-preference space has become too mechanistically occupied. 2026 work directly identifies and steers internal representations of risk preference, while ICLR 2026 risky-choice work analyzes learned reasoning mechanisms including risk aversion, certainty effect, probability weighting, and related constructs. Even if the exact probability-1 discontinuity has not been fully circuit-mapped, a paper framed as “internal mechanism of the certainty effect” risks looking like a narrow instance of an existing risk-representation line.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Allais paradox, probability=1 specialness, guaranteed-vs-99%, or another lottery benchmark does not automatically create a new narrative.

**Resurrection condition:** Reopen only with a surprising discontinuity unique to certainty that cannot be reduced to a continuous risk-preference representation and that predicts a distinct intervention.

**Key references:** https://aclanthology.org/2024.tacl-1.43/ ; https://openreview.net/forum?id=gyPUMAq5xN

---

## 4. Generic sunk-cost effect / escalation of commitment

**Natural question:** Why does prior investment make a model continue a losing course of action when only future costs and benefits should matter?

**Why it initially looked good:** Extremely natural practical failure for autonomous agents; prior effort, money, or tool calls could plausibly distort continuation decisions.

**Kill evidence:** The behavioral prerequisite is unstable. A 2026 systematic quantitative assessment finds sunk-cost effects largely absent across current models and highly prompt-sensitive; a recent contamination-aware factorial study likewise reports essentially zero sunk-cost effect across its conditions. Other work can elicit escalation under strong social/organizational pressure, but that turns the mother question into a context/social-dynamics problem rather than a robust intrinsic sunk-cost phenomenon. This is too fragile for a clean mechanistic G0.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** Prior tokens spent, prior tool calls, project investment, “don't give up now,” or persona pressure should not be used to manufacture the effect.

**Resurrection condition:** A robust modern open-model paired benchmark must show that *past irrecoverable investment alone*, with future payoffs held fixed, causally changes continuation decisions across paraphrases and models.

**Key references:** https://arxiv.org/abs/2508.01545 ; https://www.mdpi.com/2079-9292/15/11/2428

---

## 5. Generic outcome bias in legal / moral judgment

**Natural question:** Why is exactly the same prior decision judged more negligent or blameworthy merely because the eventual outcome happened to be worse?

**Why it initially looked good:** Outcome information is normatively irrelevant to ex-ante decision quality, so the matched-pair phenomenon is natural, consequential, and potentially surprising.

**Kill evidence:** The behavioral result is not stable enough on the open models needed for mechanism work. `Debiasing Legal Judgment: Outcome Effects in Open-source LLMs` (2026) re-tests eight current open-source models and finds little to no outcome bias, with only small effects in Cogito and DeepSeek-R1. That makes a broad causal-mechanism project likely to depend on cherry-picked model/task settings.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** Accident severity, damages, medical outcome, sentencing consequence, or moral luck are surface variants unless robust open-model behavior is independently established.

**Resurrection condition:** A strong, prompt-stable effect across multiple current open models and domains, with outcome held strictly irrelevant to the ex-ante decision criterion.

**Key reference:** https://doi.org/10.1628/jite-2026-0017

---

# Current lessons from the domain

1. Classic cognitive-bias names are not research questions by themselves; many have either weak modern behavior or crowded behavioral literature.
2. The best surviving candidates need a **within-item contradiction** stronger than “bias score > 0”: e.g. the model explicitly recognizes a decoy is dominated yet lets it alter A-vs-B preference, or can solve the same logic when normatively framed but not descriptively framed.
3. Instruction-tuning-induced human-like bias is attractive, but mechanism novelty must survive 2026 work on confidence, risk, authority, and preference representations.
4. Prefer phenomena with a cheap paired G0 and a result that can falsify the project immediately.