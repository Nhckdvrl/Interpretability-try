# Rejected Candidates — Social Simulation / Population Factorization

**Domain:** LLMs as survey respondents, social simulators, population models and experimental surrogates.  
**Status:** negative-memory ledger, 2026-08-31.

---

# 1. Average Opinion ≠ Population Diversity

**Natural question:** A model may know what a population thinks on average without knowing how much people disagree. Does it represent the population center separately from population heterogeneity?

**Why it initially looked good:**

- mean opinion and population dispersion are independently meaningful;
- real surveys provide both on the same questions;
- LLM silicon samples often exhibit variance collapse / “average persona” behavior;
- this could plausibly explain inflated simulated treatment effects.

**Kill evidence:**

N1 is a direct internal-representation collision. ICLR 2026 **What Do Large Language Models Know About Opinions?** is explicitly the first study of LLMs’ *internal* knowledge of human opinion distributions. It trains residual-stream probes to predict complete human answer distributions across 22 demographic groups, identifies the layer at which distributional knowledge emerges, traces signals to attention-head SAE features, and causally steers output distributions. Since a full answer distribution already contains central tendency and dispersion, narrowing the new project to “mean versus variance” would be slicing a statistic inside an occupied internal object rather than introducing a new scientific object.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as mean-vs-variance, average-person-vs-heterogeneity, central-tendency-vs-disagreement, population-center-vs-spread, or “variance exists internally but unembedding loses it.” The ICLR 2026 opinion-distribution paper already owns internal distribution recovery and final-readout bottlenecking.

**Resurrection condition:** A population variable not recoverable as merely another statistic/function of the opinion distribution, with independent external gold and a distinct causal computation.

**Reference:** https://proceedings.iclr.cc/paper_files/paper/2026/hash/ebfd0d632e950922baad6ecb64cdc407-Abstract-Conference.html

---

# Non-rejected neighboring lead: Intervention Effect Direction ≠ Magnitude

**Natural question:** A model may correctly predict whether an intervention moves an outcome up or down while systematically misestimating how strongly it moves the outcome. Are qualitative causal direction and quantitative causal magnitude computed differently?

**Why it remains distinct from the killed opinion-distribution topic:** the target is a **causal treatment effect** rather than a static population answer distribution. 2026 Nature work reports strong correspondence between LLM-predicted and real treatment effects across 70 preregistered nationally representative survey experiments / 469 effects while also finding systematic effect-size inflation; 2025 large-scale scenario-replication work independently reports larger synthetic effect sizes than human studies.

**Current status:** `HOLD-FATAL-CONTROL / NOT REGISTERED`.

**Fatal controls:**

1. **Population underdispersion / variance collapse.** If oversized effects are fully explained by synthetic respondents being too homogeneous, the proposed sign-vs-magnitude mechanism is not established.
2. **Intervention-induced user drift.** 2026 **The Illusion of Intervention** shows that treatment and control prompts can make an LLM instantiate different latent respondent/persona populations. This selection/confounding effect can inflate or shrink synthetic treatment effects, and targeted confounder controls can materially change/stabilize estimates. Therefore the headline magnitude-inflation phenotype is not interpretable until user drift is controlled.

**Required next step before any MI:** obtain the relevant treatment-effect and user-drift artifacts and test whether `direction mostly correct + magnitude systematically inflated` survives a faithful negative-control/confounder correction on analyzable open models. If the residual disappears, record `KILL-ARTIFACT` and do not rescue by narrowing to a subset. If a large residual survives, only then complete N1 for `causal effect sign vs strength internal representation` and formulate causal mechanistic forks.

**No probe / SAE / patching is authorized while this fatal control is unresolved.**
