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

# Non-rejected neighboring lead

- **Right Direction ≠ Right Magnitude for intervention effects** remains under audit. It is not automatically killed by opinion-distribution work because its target is causal treatment-effect sign/strength rather than static population response distributions. However, variance collapse must be a fatal control: if magnitude inflation is fully explained by synthetic-population underdispersion or sampling mechanics, the intervention-effect topic must be killed rather than reframed.
