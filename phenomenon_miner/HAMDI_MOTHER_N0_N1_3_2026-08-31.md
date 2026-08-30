# Hamdi-Style Mother-Paper Search — N0 + N1 Audit (2026-08-31)

Status: `THREE SURVIVORS / N0+N1 PASS / REGISTRATION ALLOWED / NO MODEL CALL AUTHORIZED`

This audit applies the repository's Natural-Question Gate and the stricter Hamdi-style rule:

```text
strong mother paper / established natural scientific object
→ ask what the mother leaves conceptually unresolved
→ require a title-level question that remains interesting without any dataset or MI tool
→ N0: mother-inclusion + internal-history audit
→ N1: strongest-neighbor + successor + exact-title-claim attack
→ if novelty survives only by narrowing to a benchmark/subtype/special prompt, KILL and replace
```

The goal is not to find three technically novel experiments. The goal is to find three **ACL/EMNLP-sized scientific questions** for which mechanistic interpretability is a natural way to answer the question rather than a reason to ask it.

## Final result

| id | candidate | N0 | N1 | verdict |
|---|---|---|---|---|
| 026 | Scientific Plausibility vs Testability | PASS | PASS | REGISTER |
| 027 | Rhetorical Force vs Implied Assertion | PASS | PASS | REGISTER |
| 028 | Event Causality vs Responsibility Framing | PASS | PASS | REGISTER |

One initially attractive candidate, **Falsehood vs Deceptive Intent**, was explicitly rejected during N1 because recent 2026 work already moves from lie detection to deception-specific / intent-targeted probes. We did not preserve it by shrinking to a special deception subtype.

---

# 026 — Scientific Plausibility vs Testability

## Natural question

> A hypothesis can sound scientifically plausible yet be impossible to test with a discriminating experiment; another hypothesis can be implausible but perfectly testable. Does an LLM internally treat “could this be true?” and “could we actually test it?” as different scientific judgments, or collapse them into one generic feasibility score?

This is a philosophy-of-science / scientific-reasoning distinction before it is an LLM benchmark distinction.

## Mother paper

Mohammadi, Gaur & Ferraro, **Experiments or Outcomes? Probing Scientific Feasibility in Large Language Models**, ACL 2026 Short.

- Paper: https://aclanthology.org/2026.acl-short.50/
- It defines scientific feasibility using two ingredients: consistency with established knowledge and whether experimental evidence could support or refute the claim.
- It evaluates feasibility under hypothesis-only / experiment / outcome / experiment+outcome conditions and finds outcome evidence more reliable than experimental descriptions.

The mother establishes that scientific feasibility judgment is a real LLM problem and that experiment information is a distinct source of difficulty. It does **not** ask whether the two semantic ingredients of feasibility are separate internal variables.

## Strong adjacent support

Kumbhar et al., **Hypothesis Generation for Materials Discovery and Design Using Goal-Driven and Constraint-Guided LLM Agents**, Findings NAACL 2025.

- Paper: https://aclanthology.org/2025.findings-naacl.420/
- Their expert-developed quality rubric explicitly separates **Scientific Plausibility**, **Testability**, and **Feasibility & Scalability**.

This is important conceptually: the distinction is not invented for our experiment. Scientists already judge these dimensions separately. But that work uses the dimensions for evaluation; it does not study whether an LM internally factorizes them.

## N0 — mother inclusion

### Mother already owns

- generic scientific feasibility classification;
- hypothesis-only vs experiment/outcome evidence conditions;
- experiment text can be brittle;
- scientific hypothesis generation/evaluation;
- separate external rubric dimensions for plausibility/testability in materials science.

### Mother does NOT own

- the internal relation between plausibility and testability;
- whether the model has independent representations/readers for the two judgments;
- whether a single generic “scientific feasibility” state merges them;
- a causal double dissociation between changing plausibility and changing testability;
- whether errors in feasibility arise because one component is absent, entangled, or read out incorrectly.

### Internal-history check

Searches over `Interpretability-try` and `candidate_topics` for scientific plausibility/testability/feasibility did not recover an existing registered or archived scientific object. It is not a resurrection of the Bayesian-use-gap, causal-ladder, or generic representation→use families: the scientific object is the **factorization of two independently meaningful scientific judgments**, not a generic “the model knows X but fails to use X.”

**N0 verdict: PASS.**

## N1 — strongest-neighbor / successor attack

Search families:

```text
scientific plausibility testability LLM representation
scientific testability internal representation language model
falsifiability hypothesis LLM mechanistic
scientific feasibility LLM mechanistic interpretability
plausibility testability causal representation LLM
```

Strongest neighbors found:

1. ACL 2026 feasibility mother above — behavioral/diagnostic, no internal factorization.
2. Findings NAACL 2025 materials hypothesis work — separate evaluation dimensions, no MI.
3. HARPA (2025/2026 scientific ideation) — optimizes testability/feasibility of generated ideas, no internal representation story.
4. SFBench (2026) — expert feasibility benchmark, not plausibility-vs-testability mechanism.
5. FirstResearch (2026) — auditable/falsifiable research-question formation, not internal scientific judgment factorization.

No exact work found that claims a causal internal separation of **plausibility** and **testability** in LLM scientific reasoning.

### Anti-narrowing test

The surviving question does **not** depend on materials science, one benchmark, one kind of hypothesis, or one prompt. The paper can ask a domain-general science-reasoning question and use materials/biology/physics sources as instruments. If the project later requires “only materials hypotheses with this rubric” to stay novel, it must be ROUTE/KILL rather than silently narrowing the title.

**N1 verdict: PASS.**

## Safe title-level claim

> **Plausibility Is Not Testability: How Language Models Factorize Scientific Feasibility**

Forbidden title-level claims:

- “LLMs struggle with scientific feasibility”;
- “experiments are harder than outcomes”;
- “we propose a better feasibility benchmark”;
- “plausibility and testability are useful evaluation metrics.”

Those are prior work.

---

# 027 — Rhetorical Force vs Implied Assertion

## Natural question

> Recognizing that a question is rhetorical is not the same as understanding what the speaker is actually asserting. Does an LLM internally separate “this is a rhetorical speech act” from “this is the proposition/stance the speaker is committing to”?

Example:

> “Why should we force students to wear these garments anyway?”

A model may correctly know that this is not a genuine request for information, yet still fail to recover the implied stance that students should not be forced to wear them.

This is a standard pragmatic distinction between interrogative surface form, illocutionary force, and propositional/argumentative contribution.

## Mother papers

### EMNLP 2025 Main — SRAQ

Ikumariegbe, Blanco & Riloff, **Studying Rhetorically Ambiguous Questions**.

- https://aclanthology.org/2025.emnlp-main.1553/
- Same/similar surface questions can be rhetorical or informational depending on discourse context.
- Modern LMs struggle to recognize many rhetorical questions.

This establishes context-sensitive rhetorical force as a real behavioral object.

### ACL 2026 Main — representation mother

Yao et al., **Rhetorical Questions in LLM Representations: A Linear Probing Study**.

- https://aclanthology.org/2026.acl-long.5/
- Rhetorical status is linearly separable early and transfers across datasets at moderate AUROC.
- Multiple directions capture heterogeneous rhetorical cues rather than one universal RQ direction.

This establishes that rhetoricality is internally readable but heterogeneous. It still treats the target primarily as **rhetorical vs informational status**, not the proposition asserted by the rhetorical act.

## Independent linguistic anchor

Hautli-Janisz et al., **Questions in argumentative dialogue**, Journal of Pragmatics 2022.

- https://doi.org/10.1016/j.pragma.2021.10.029
- Their stable taxonomy distinguishes pure, challenge, rhetorical and assertive questioning.
- Crucially, rhetorical questioning is defined as a speaker **making an assertion in the guise of a question**.
- They release/describe large natural argumentative-dialogue resources in the IAT/AIF ecosystem.

QT30 provides 19,842 naturally occurring utterances / 280k words of broadcast debate with IAT-style argumentative annotation:
https://aclanthology.org/2022.lrec-1.352/

This gives the project a natural discourse object rather than a hand-written polarity trick.

## N0 — mother inclusion

### Already owned by prior work

- rhetorical vs informational classification;
- context changes RQ interpretation;
- LMs struggle with RQ recognition;
- rhetorical status is linearly decodable;
- RQ representation has multiple directions / heterogeneous cues;
- generic “RQs signal stance.”

### New scientific object

The new object is the **factorization of speech-act force and implied propositional content**:

```text
surface interrogative content
→ context-sensitive force: information-seeking / rhetorical / assertive / challenge
→ implied proposition / speaker commitment
→ downstream response / argument interpretation
```

A model can succeed at one stage and fail at the next. This is not equivalent to a stronger rhetoricality probe.

### Internal-history check

Repository searches for rhetorical question / implied assertion / stance did not find an existing active, archive, or rejected scientific object. The psycholinguistic failure library kills garden-path reanalysis, generic negation, and Stroop-like conflict, not pragmatic speech-act/content factorization.

**N0 verdict: PASS.**

## N1 — strongest-neighbor / successor attack

Exact search families:

```text
rhetorical question implied assertion LLM
rhetorical force implied stance language model representation
rhetorical question implied answer LLM mechanistic
speaker commitment rhetorical question LLM
argumentative question implicit stance LLM
```

Strongest neighbors:

1. ACL 2026 RQ probing paper — target is rhetoricality, not asserted proposition.
2. EMNLP 2025 SRAQ — target is contextual RQ/IQ recognition.
3. Argument-mining work — documents that rhetorical/assertive questions contribute propositions, but does not reverse-engineer LLM computation.
4. 2026 argument-classification analyses report failures on implicit criticism/RQs, again behavioral rather than causal internal factorization.

No direct work found that separately identifies and causally manipulates **rhetorical force** and **implied assertion/stance content** in LLMs.

### Anti-narrowing test

Do NOT narrow the project to “yes/no RQs usually imply the opposite polarity.” Linguistic work explicitly shows RQs are heterogeneous. A valid project must support multiple natural argumentative question types and treat implied content/stance as a discourse contribution, not just logical negation.

If usable data only supports one polar template, the project is not allowed to keep the ACL/EMNLP-wide title; it must be parked or killed.

**N1 verdict: PASS.**

## Safe title-level claim

> **Questions That Assert: Separating Rhetorical Force from Implied Stance in Language Models**

Forbidden claims:

- first RQ detection benchmark;
- first RQ representation probe;
- one universal rhetorical direction;
- RQ simply means negating the surface question.

---

# 028 — Event Causality vs Responsibility Framing

## Natural question

> “X helped cause Y” and “X is to blame / deserves credit for Y” are not the same judgment. When narratives frame the same event differently, does an LLM keep a relatively stable model of what caused what while separately representing who is being blamed or credited, or does framing rewrite the causal model itself?

This is natural in politics, law, news, accidents and social explanation. Causal contribution and responsibility attribution are related but not identical.

## Mother paper

Zhao et al., **Reframing Responsibility: Framing-Aware Event Causality Identification**, ACL 2026 Main.

- https://aclanthology.org/2026.acl-long.2173/
- Standard ECI is extended with structured framing attributes: responsibility target, evaluative framing, source type and epistemic modality.
- The dataset aligns English/Chinese/Arabic narratives with shared event anchors.
- Prompt-based LLMs struggle to recover complete framed causal claims; supervised joint models do substantially better.
- Data includes human refinement of causal relations and human annotation of responsibility/framing attributes.

The mother establishes both the natural phenomenon (causal explanations are framed/contested) and a source population with aligned events.

## N0 — mother inclusion

### Mother already owns

- framed causal explanations exist;
- different narratives assign responsibility differently;
- FrECI structured output task;
- multilingual aligned event anchors;
- prompt LLM baseline failure;
- supervised joint modeling improves extraction.

### New object

The paper does **not** ask whether LLM internals contain separable computations for:

```text
A. event-causal relation: what caused what?
B. responsibility/evaluative frame: who is blamed, credited, exonerated or undermined?
```

Nor does it test whether framing changes only B while preserving A, or penetrates/reconstructs A itself.

That internal factorization is the scientific question.

### Internal-history check

Repository searches for cause/responsibility/blame/framing found no registered/archived duplicate. The cognitive-decision rejection log warns against generic authority/source-status bias. 028 is not that family:

- source credibility/authority is not the target;
- source identity is merely conditioning context;
- the target is proposition-level **causality vs responsibility** factorization under matched event anchors.

If the project turns into “different sources bias LLMs,” it must be killed as a generic source/framing story.

**N0 verdict: PASS.**

## N1 — strongest-neighbor / successor attack

Search families:

```text
cause blame LLM responsibility attribution representation
causal responsibility LLM mechanistic
FrECI internal representation mechanism
responsibility framing event causality language model
causal attribution blame mechanistic interpretability LLM
```

Strongest neighbors:

1. FrECI itself — behavior/dataset/task, not internal factorization.
2. Behavioral attribution-bias work in 2026 — studies human-like attribution biases, not LLM causal circuitry.
3. Human responsibility / actual-causality work — studies formal responsibility or human judgments, not how LLMs represent framed narratives.
4. Generic document-level ECI work — causal extraction without responsibility framing.
5. AI-governance / AI-harm responsibility literature — different scientific target (who is responsible for AI outcomes), not language-model interpretation of causal narratives.

No direct work found that gives a causal internal decomposition of event causality and blame/credit framing in LLMs.

### Anti-narrowing test

The title-level question must remain:

> **Does framing alter responsibility attribution while preserving an event-causal core, or does it rewrite the causal representation itself?**

It may use FrECI political narratives for discovery, but the scientific claim cannot become “one source-type label is decodable on FrECI.” At least one second natural framing source/domain or a strong cross-lingual/source-held-out generalization is required before a main-paper claim.

**N1 verdict: PASS.**

## Safe title-level claim

> **Cause Is Not Blame: Separating Event Causality from Responsibility Framing in Language Models**

Forbidden claims:

- first framing-aware ECI task;
- LLMs struggle on FrECI;
- source identity is decodable;
- political text causes bias;
- generic “framing affects outputs.”

---

# Candidate explicitly killed during this search

## Falsehood vs Deceptive Intent

Natural question was strong: lying and deception are not identical because a speaker can deceive with literally true statements.

However, N1 found the 2026 literature already moving directly into deception-specific internal signals and targeted instruction-pair probes intended to capture deceptive intent rather than content patterns, alongside work showing lie detectors fail on non-lying deception.

Keeping novelty would require restricting the project to a special subtype of listener-belief manipulation or a particular deception setting. That violates the anti-narrowing rule.

**Verdict: KILL / DO NOT REGISTER.**

---

# Registration discipline for 026–028

Passing N0+N1 means the **scientific question** is allowed into `active/`. It does not mean behavior or data is already frozen.

Before any fresh model call, each project must separately produce:

1. source-provenance audit;
2. exact population / label definition;
3. capability or mother-behavior prerequisite;
4. deterministic or source-grounded scoring wherever possible;
5. minimal restriction budget;
6. an explicit condition under which data limitations force PARK rather than title narrowing.

No probe, SAE, patching or steering is authorized until that project's behavioral/data contract exists.
