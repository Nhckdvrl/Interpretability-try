# Rejected Candidates — Decision-Making / Choice Anomalies

**Domain:** human-style decision phenomena where logically/utility-equivalent presentations or irrelevant alternatives change choices.  
**Search date:** 2026-08-26.

## Domain goal

A strong candidate should have a content-preserving or decision-theoretically irrelevant manipulation with a large behavioral effect, and should support a mechanism question that is more specific than “LLMs inherit human cognitive biases.”

---

# 1. Generic gain/loss framing effect

**Natural question:** Why does describing the same risky prospect in gain versus loss terms change an LLM’s choice?

**Why it initially looked good:**

- classic and immediately understandable;
- exact expected-value-equivalent pairs are trivial to generate;
- natural mechanism alternatives include numerical/probability representation, valence-driven utility distortion, and late policy/readout bias.

**Kill evidence:**

The broad behavior is no longer an open problem and is strongly model-class dependent. ACL 2026 Outstanding Paper `Mind the (DH) Gap!` evaluates 20 frontier and open models and finds a sharp split: reasoning models tend toward rational, framing-insensitive behavior, whereas conversational models are more framing/order/explanation sensitive and more human-like.  
https://aclanthology.org/2026.acl-long.479/

Other 2025–2026 human/LLM comparative studies likewise show that framing effects vary strongly across model generations and can even reverse direction relative to humans. Thus a generic “why do LLMs show framing effects?” paper risks choosing a model class that simply does not exhibit the effect, or explaining a behavior already subsumed by a broader risky-choice characterization.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** gain-vs-loss wording, lives-saved vs lives-lost, positive/negative probability framing, and generic prospect-theory replication are one family.

**Resurrection condition:** a narrow, stable framing manipulation that survives current reasoning models and produces a non-obvious mechanism not reducible to generic valence sensitivity.

---

# 2. Generic decoy / attraction / irrelevant-alternative effect

**Natural question:** Why can adding an objectively inferior third option change which of two original options an LLM prefers?

**Why it initially looked good:**

- violates Independence of Irrelevant Alternatives in a very intuitive way;
- exact decoy manipulations allow clean matched pairs;
- Findings EMNLP 2024 reports a robust attraction effect in GPT-3.5/4 hiring decisions, even after warnings about the bias;
- CogSci 2025 reports attraction, repulsion, compromise, and similarity context effects across GPT models.

**Kill evidence:**

The strongest published behavior evidence is concentrated on older/closed GPT generations rather than current open reasoning models. Meanwhile ACL 2026 shows that mathematical-reasoning training can substantially alter broad decision-bias profiles, with reasoning models much more invariant to framing/order than conversational models.  
https://aclanthology.org/2026.acl-long.479/

The mother claim “LLMs reproduce a famous human context effect” is also low-surprise unless a modern-model G0 reveals an unexpected boundary or inversion. At present, committing to mechanism analysis would require first gambling that the behavioral effect survives on suitable open models.

Behavior references:  
https://aclanthology.org/2024.findings-emnlp.405/  
https://escholarship.org/uc/item/4fv3t754

**Death code:** `ARTIFACT_FAILURE`

Here `ARTIFACT_FAILURE` means not that data are inaccessible, but that the available behavioral artifact is insufficiently aligned with the current open-model mechanism target; the natural modern-model prerequisite is not already established.

**Nearest-neighbor warning:** attraction effect, compromise effect, similarity effect, hiring decoys, product decoys, and “irrelevant alternative flips choice” are one family until a strong current-model G0 exists.

**Resurrection condition:** current open models show a large stable IIA violation under a public/programmable benchmark, ideally with a counterintuitive boundary condition that differs across model families.

---

# 3. Generic “asking for an explanation changes the decision”

**Natural question:** Why can asking an LLM to explain a risky choice alter the choice itself?

**Why it initially looked good:**

- exposes a natural process/behavior interaction;
- could distinguish pre-existing preference from explanation-induced recomputation;
- potentially relevant to chain-of-thought and decision support.

**Kill evidence:**

`Mind the (DH) Gap!` already treats decision rationale/explanation as a major experimental axis and shows model-class differences in sensitivity. More broadly, “reasoning changes answers” is far too broad and crowded to constitute a mother question without a sharper external phenomenon.  
https://aclanthology.org/2026.acl-long.479/

A likely method—force or suppress deliberation—also does not require a fine-grained mechanistic account and is already a ubiquitous inference-time control.

**Death code:** `NATURALNESS_FAILURE`

**Nearest-neighbor warning:** CoT changes preference, rationale-first vs answer-first, think/no-think risk choice, and explanation-induced consistency are not sufficient topics by themselves.

**Resurrection condition:** a specific decision phenomenon where explanation selectively reverses only one theoretically meaningful class of choices and mechanism diagnosis changes the repair.

---

# Survivor under audit: Description–Experience (Description–History) Gap

**Natural question:** Why does an LLM make different risky choices when the *same underlying outcome distribution* is given explicitly as probabilities versus shown through a history of sampled outcomes?

**Behavior foundation:** ACL 2026 Outstanding Paper `Mind the (DH) Gap!` studies 20 frontier/open models plus matched human data and a rational expected-payoff reference. Reasoning models are comparatively stable, whereas conversational models show a large description-history gap. Strikingly, moving from explicit descriptions to experience histories makes models more human-like and less like the rational agent. Code and processed LLM choice data are public.  
https://aclanthology.org/2026.acl-long.479/  
https://github.com/Yongyan-Zhang/mind-the-dh-gap

**Why this is not yet rejected:**

The current collision search found no mechanistic follow-up explaining *where* the representation pathway diverges between explicit probability descriptions and outcome histories. Human decision-science literature itself distinguishes several competing causes of the description–experience gap: sampling/information differences, ambiguity/preferences, representation, and memory.  
https://doi.org/10.1007/s11166-022-09393-w

For LLMs this yields clean competing mechanisms:

```text
A. probability-estimation failure:
   outcome histories never form the same latent probability representation as explicit descriptions;

B. rare-event weighting / utility transformation:
   probability is represented correctly, but history-derived probabilities are reweighted differently before valuation;

C. policy/readout split:
   both probability and value representations align, but a representation-mode-dependent decision policy selects differently.
```

These predict different patching/interchange outcomes and different repairs (state estimator / representation alignment vs value-calibration objective vs routing/readout intervention).

**Surprise potential:** high. The strongest possible result is not merely “history is harder,” but that the model may internally infer the same objective distribution and still deliberately route it through a different risk policy—or conversely that reasoning training specifically collapses two previously distinct representational pathways.

**Status:** `PRE-CANDIDATE / HIGH-PRIORITY SURVIVOR`. Needs exact mechanistic collision audit and a frozen cheap G0 on two current open model families before promotion.