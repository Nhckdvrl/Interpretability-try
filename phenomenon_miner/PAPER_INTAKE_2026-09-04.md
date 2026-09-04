# Paper Intake Round — 2026-09-04

Status: **ROUND 1 IN PROGRESS — 1 CANDIDATE ALREADY KILLED ON COLLISION**

Purpose: build a wide, high-quality input base before proposing objects, per the standing
instruction to read many recent top-venue papers, note what each actually claims, then look for
intersections nobody has taken. Two rules apply throughout:

- **open code is a filter, not a bonus.** Papers without a runnable artifact are used only as
  collision evidence, never as a mother or a reproduction target.
- **verification level is recorded per entry.** `[V]` = abstract or PDF read; `[T]` = title-level
  only from an accepted-papers listing, not yet substantiated. `[T]` entries may not be used as
  novelty evidence in either direction until promoted to `[V]`.

## Venue coverage so far

| venue | status | notes |
|---|---|---|
| ACL 2026 (San Diego, Jul 2–7) | listing swept | 2,296 main + 2,163 findings; interpretability is the special theme this year |
| EMNLP 2026 (Budapest, Oct 24–29) | listing swept | ~2,700 main + ~2,500 findings, 263 industry, 87 demos, 48 TACL |
| EMNLP 2025 | targeted | reached through citation trails, not swept |
| NAACL 2026 | not yet swept | next |
| arXiv 2026 | targeted collision queries only | not a sweep |

---

## A. Context integration, segmentation and surface markers

1. **Information Integration in LLMs is Gated by Linguistic Structural Markers** — Wei Liu, Nai Ding, EMNLP 2025 main. `[V]` code: https://github.com/y1ny/IntegrationWindow
   - Measures an "information integration window" purely behaviourally: predict a target word from a local window of *k* words vs the full context, and take JS divergence between the two predictive distributions as the *local-prediction deficit*.
   - Deficit decays as a power law in window length and **drops sharply at the sentence boundary**, for humans and LLMs alike.
   - Deleting the last punctuation mark makes the boundary effect **nearly disappear**; "meaningless" sentences reduce but retain it. Conclusion: overt markers, not implicit syntax/semantics.
   - Exp 3 isolates comma vs conjunction in comma-conjunction pairs; Qwen2.5-Chinese retains a boundary effect on conjunctions alone.
   - **Weak points**: model panel is only GPT-2 and Qwen2.5; deleting the final period also destroys well-formedness and shifts local n-gram statistics at exactly the measured position; the JS measure conflates "integration window" with "how far local context already determines the distribution", and predictability is independently higher near boundaries.
   - **Obvious untested case**: they only ever *remove* markers. Desynchronising marker from structure — a period mid-clause, a genuine boundary with no marker — is the decisive test and was not run.

2. **Punctuation and Predicates in Language Models** — arXiv 2508.14067 (Aug 2025). `[V]` (abstract)
   - Asks necessity/sufficiency of punctuation for information propagation, using **activation interchange interventions** to test whether the period acts as a summarization boundary.
   - This is the mechanistic version of entry 1 and is the reason entry 1's open case is not free.

3. **LLM-Microscope: Uncovering the Hidden Role of Punctuation in Context Memory of Transformers** — arXiv 2502.15007, NAACL 2025. `[V]` (abstract)
   - Tokens usually treated as minor — punctuation, determiners, stopwords — carry high contextual load; removing them degrades MMLU and BABILong-4k even when only "irrelevant" tokens go.

4. **Think in Sentences: Explicit Sentence Boundaries Enhance Language Model's Capabilities** — ACL 2026 main. `[T]`

> **KILL — `marker_vs_structure_segmentation` (2026-09-04).** The object "LLM context integration is
> segmented by punctuation tokens rather than by syntactic structure" is owned three ways:
> behaviourally by (1), mechanistically by (2) with interchange interventions on the period, and
> representationally by (3), with punctuation-as-attention-sink already established (Gu et al. 2025;
> Barbero et al. 2025). The un-run misplacement condition is a manipulation change on an owned
> object, which `STRICT_EXTENSION_GATE` E1 explicitly rules insufficient. Recorded so no later round
> re-proposes it.

---

## B. Binding, entity and state tracking

5. **A retrieval-conditioned rebinding circuit for dynamic entity tracking in LLMs** — arXiv 2606.08644 (Jun 2026). `[V]` (abstract) — **no code released**
   - Compact attention-head circuit that encodes swap-relevant binding information and reinstates it at readout; binding lives in query/key subspaces for Gemma, mainly key vectors for Llama; established by causal interventions.
   - Collision-relevant for anything proposing "where is the binding" in dynamic entity tracking.
6. **Cell-Based Representation of Relational Binding in Language Models** — arXiv 2604.19052. `[T]`
7. **Tracing Relational Knowledge Recall in Large Language Models** — arXiv 2604.19934. `[T]`
8. **How do Language Models Bind Entities in Context?** — arXiv 2310.17191 (binding-ID work; the standing prior). `[V]` (known)
9. **Structured Episodic Event Memory** — ACL 2026 main. `[T]`
10. **Different types of syntactic agreement recruit the same units within LLMs** — Kryvosheieva et al., ACL 2026 main. `[T]`

---

## C. Representation present / use absent

11. **What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness** — arXiv 2607.08046 (Jul 2026). `[V]` (abstract)
    - Removing an influential source changes the forecast while leaving the reasoning trace untouched; internal representations predict the direction of behavioural change in 84% of cases, including where the CoT conceals the perturbation.
12. **Unveiling Internal Reasoning Modes in LLMs: Latent Reasoning vs. Factual Shortcuts** — EMNLP 2026 main. `[T]`
13. **Too Consistent to Detect: A Study of Self-Consistent Errors in LLMs** — arXiv 2505.17656, EMNLP 2026. `[V]` (abstract)
14. **Towards Faithful Natural Language Explanations: A Study Using Activation Patching in LLMs** — EMNLP 2026 main. `[T]`
15. **Diagnosing Memorization in Chain-of-Thought Reasoning, One Token at a Time** — EMNLP 2026 main. `[T]`

> **Standing warning for this repo.** "The model represents X internally but does not use/say X" is a
> crowded frame as of mid-2026 (11, 12, 14, plus the older *LLMs know more than they show* line).
> This is the frame `034`'s surviving probe result would have needed, and is a second, independent
> reason its archive verdict is correct. Any future topic in this shape must own a *new* X, not a new
> demonstration of the shape.

---

## D. Mechanistic method / circuits

16. **Sparse Feature Coactivation Reveals Causal Semantic Modules in LLMs** — ACL 2026 main. `[T]`
17. **Multi-component Causal Tracing in Large Language Models** — ACL 2026 main. `[T]`
18. **Mechanistic Interpretability Should Prioritize Feature Consistency in Sparse Autoencoders** — ACL 2026 main. `[T]`
19. **A Mechanistic Account of Attention Sinks in GPT-2** / **Attention Sinks Are Provably Necessary in Softmax Transformers** — Ran-Milo et al., ACL 2026 main. `[T]`
20. **Crosscoding Through Time: Tracking Emergence & Consolidation of Linguistic Representations** — Bayazit, Mueller, Bosselut, ACL 2026 main. `[T]`
21. **On the Emergence and Test-Time Use of Structural Information in LLMs** — arXiv 2601.17869, ACL 2026 main. `[V]` (abstract)
    - Controlled dataset of linguistic structural transformations; emergence of structural learning correlates with complex reasoning, but **test-time compositional generation stays limited**.
22. **On Behalf of the Stakeholders: Trends in NLP Model Interpretability in the Era of LLMs** — Calderon & Reichart, ACL 2026, SAC award for Interpretability. `[T]`

---

## E. Semantics / pragmatics behaviour

23. **CxMP: A Linguistic Minimal-Pair Benchmark for Evaluating Constructional Understanding in Language Models** — Oba & Sugawara, ACL 2026 **Outstanding Paper**, `aclanthology.org/2026.acl-long.2132/`. `[V]`
    - Construction Grammar framing: constructions are form–meaning pairings, and the benchmark asks whether models interpret the *semantic relations* a construction implies. Controlled minimal pairs across **nine** construction types including let-alone, caused motion and ditransitive.
    - Findings: constructional understanding develops **gradually** and stays limited for some constructions even at large scale, while **grammatical acceptability emerges earlier**; shallow heuristics show a **U-shaped** pattern over scale.
    - **Consequence for this repo's live slate.** CxMP does not cover the 041–045 distinctions (set restriction, uniqueness vs familiarity, stage vs individual, referential vs attributive), so it kills none of them directly. What it does establish is that *"controlled minimal pairs testing whether an LM reads meaning off form"* is now a top-venue-served frame with an Outstanding Paper on it. 041–045 therefore cannot carry their novelty in the minimal-pair battery; each must carry it in the causal/representational factorization, and each must say what it adds beyond CxMP's form-vs-meaning dissociation. Re-audit them against this before any of them advances.
    - Its own dissociation — acceptability before constructional meaning, with a U-shaped heuristic signature — is itself a candidate mother worth a `[V]` read of the full paper.
24. **How Hypocritical Is Your LLM judge? Listener–Speaker Asymmetries in the Pragmatic Competence of Large Language Models** — Sieker & Zarrieß, ACL 2026 Findings, arXiv 2604.15873. `[V]`
    - Compares the same models as pragmatic **listeners** (judging appropriateness of an output) and as pragmatic **speakers** (generating an appropriate output). Finds a robust asymmetry: many models are substantially better listeners than speakers, and the two roles are only weakly aligned.
    - Behavioural/evaluation paper only — no mechanism. The obvious follow-up (is the listener-competent representation present but unread during generation?) lands squarely in the crowded "represents but does not use" frame in section C, so it is **not** free. If this is developed, the object has to be the *asymmetry's controller*, not another demonstration of representation-without-use.
25. **Rhetorical Questions in LLM Representations: A Linear Probing Study** — Yao et al., ACL 2026 main. `[T]`
26. **It's Not What You Say, It's How You Say It: Evaluating LLM Responses to Expressions of Belief** — Du et al., ACL 2026 main. `[T]`
27. **LVLMs and Humans Ground Differently in Referential Communication** — Zeng et al., ACL 2026 main. `[T]`
28. **Using Perspectival Words Is Harder Than Vocabulary Words for Humans** — Dong et al., ACL 2026 main. `[T]`
29. **On the Same Wavelength? Evaluating Pragmatic Reasoning in Language Models across Broad Concepts** — arXiv 2509.06952. `[T]`

---

## F. Instruction following and multi-instruction control

30. **Revisiting the Reliability of Language Models in Instruction-Following** — Dong et al., ACL 2026 main. `[T]`
31. **How Memory Management Impacts LLM Agents** — Xiong et al., ACL 2026 main. `[T]`
32. **DecIF: Improving Instruction-Following through Decomposition** — Hui et al., ACL 2026 main. `[T]`

> Relevant to the `034` archive verdict: this cluster is where instruction position/priority bias
> lives, and it is why `034`'s surviving effect is an owned object.

---

## Next actions

1. Promote `[T]` → `[V]` for entries 23, 24, 25, 26, 27 first — they sit directly on the repo's live
   041–045 slate and on `038`, so their content changes existing registrations, not just new ones.
2. Sweep NAACL 2026 and the ACL/EMNLP 2026 findings listings, which are not yet covered.
3. Only then draw the intersection map. No object is proposed from `[T]` evidence.
