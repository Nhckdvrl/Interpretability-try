# Rejected Candidates — Agent / Tool-Use Failures

**Domain:** tool-augmented LLM agents, runtime tool failures, result integration, recovery, state tracking, termination.  
**Status:** active breadth-first scan.  
**Rule:** only candidates that initially looked genuinely promising are recorded here. Trivial brainstorms are omitted.

The domain is scanned as a family rather than as isolated paper ideas. Every candidate below should be treated as negative knowledge for future searches unless its explicit resurrection condition is met.

---

## 1. Generic tool-result ignoring

**Natural question:** The agent calls the correct tool and receives the answer, so why does it still answer from its own memory instead of using the returned result?

**Why it initially looked good:** Extremely natural agent failure; clean split between missing encoding, memory override, and late routing/readout.

**Kill evidence:** `ToolFailBench` (2026) already makes Result-Ignore an explicit diagnostic failure mode. `Investigating Tool-Memory Conflicts in Tool-Augmented LLMs` (2026) directly studies tool knowledge vs parametric memory and evaluates conflict-resolution methods. A generic hidden-state follow-up risks becoming “context-memory conflict, but tool text.”

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as calculator-vs-memory, search-vs-memory, database-vs-memory, or by changing domain/model.

**Resurrection condition:** Need a tool-specific decisive contrast unavailable in ordinary static context-memory conflict, especially one involving stateful execution semantics.

**Key references:** https://arxiv.org/abs/2607.04686 ; https://arxiv.org/abs/2601.09760

---

## 2. Trusting tool success without verifying world state

**Natural question:** Why does an agent treat a tool’s apparent “success” response as proof that the intended real-world change actually happened?

**Why it initially looked good:** Concrete deployment failure; possible split between postcondition representation, intention/achievement confusion, and over-trust in success-shaped text.

**Kill evidence:** `Failing Tools` already finds missing verification/recovery steps to be a dominant failure mode. More decisively, `Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures` directly fixes the practical problem using postcondition verification, verify-before-retry, and idempotency keys. This creates a P3 problem: regardless of the internal explanation, the obvious repair is the same external verifier.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** HTTP 200, exit-code 0, acknowledgement text, GUI confirmation, delayed visibility, and partial success are the same family.

**Resurrection condition:** Reconsider only if authoritative postcondition evidence is already present in-context but the model still behaves as if the intended state had occurred, isolating an internal state-update failure.

**Key references:** https://openreview.net/pdf?id=j7YsSnA64D ; https://arxiv.org/abs/2608.02645

---

## 3. Blind retry after ambiguous / non-atomic failure

**Natural question:** A tool times out after possibly having executed; why does the agent repeat the action instead of checking whether it already happened?

**Why it initially looked good:** Vivid consequences such as duplicate writes/payments; apparently clean distinction between request-status and effect-status.

**Kill evidence:** `Verified Tool Calls` formalizes exactly this family of non-atomic failures and shows verify-before-retry + idempotency sharply reduces duplicate actions. The natural problem and obvious repair are already occupied.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** Retry bias, timeout confusion, duplicate-action tendency, and non-idempotent tool-use failure are the same mother question.

**Resurrection condition:** Need a surprising representation–policy dissociation, e.g. the model explicitly represents that the effect may already have occurred but still causally enters a retry policy.

**Key reference:** https://arxiv.org/abs/2608.02645

---

## 4. Generic recovery from broken / unavailable tools

**Natural question:** When the planned tool fails, why can’t the agent recognize that its original plan is broken and switch to a valid alternative?

**Why it initially looked good:** Natural long-horizon problem; mechanism split between failure detection, alternative-plan search, and persistence to the original path.

**Kill evidence:** `Failing Tools` systematically covers runtime faults and recovery; `PlanBench-XL` explicitly studies planning under missing/failing/distracting tools and reports severe collapse under blocking. The broad mother question is now benchmark-dense and too occupied.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Another tool ecosystem, agent framework, or injected failure family does not make this new.

**Resurrection condition:** Find a narrow dissociation where the agent internally knows the current path is impossible but remains causally committed to it, versus never representing failure at all.

**Key references:** https://openreview.net/pdf?id=j7YsSnA64D ; https://arxiv.org/abs/2606.22388

---

## 5. Generic premature stopping / declaring success too early

**Natural question:** Why does an agent stop and claim the job is finished while required objectives are still unmet?

**Why it initially looked good:** Instantly understandable; clean potential split among forgotten goals, false world-state belief, and termination/readout failure.

**Kill evidence:** Premature termination is already an explicit agent failure category, while `When Agents Commit Too Soon` (2026) studies hidden representational premature commitment, cross-model replication, monitoring, and intervention. It is not identical, but it occupies enough of the hidden early-commitment narrative that the generic version has poor headroom; explicit completion verification also gives an obvious non-mechanistic fix.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Early-stop bias, premature completion, premature answer, insufficient persistence are not enough by themselves.

**Resurrection condition:** A clean natural phenomenon where specific unmet goals remain internally represented at the stopping step but the termination policy selectively ignores them.

**Key reference:** https://arxiv.org/abs/2606.22936

---

## 6. Generic “agent should abstain instead of acting”

**Natural question:** Why does an agent keep taking actions when the request is impossible, underspecified, contradictory, or impossible with the available tools?

**Why it initially looked good:** Natural action-vs-restraint problem with clean paired tasks and possible inability-detection vs action-policy split.

**Kill evidence:** `AgentAbstain` (2026) already provides a systematic benchmark of this exact family with 263 paired tasks across 42 executable environments and eight abstention scenarios. Generic “find an abstention direction and steer it” is an obvious follow-up rather than a fresh mother question.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Impossible tasks, insufficient tools, contradictory requests, missing prerequisites, and ambiguity are all within the same abstention family.

**Resurrection condition:** Need a surprising, selective action-compulsion mechanism where impossibility is internally recognized but action proceeds anyway, and intervention does not simply increase blanket refusal.

**Key reference:** https://agentabstain.github.io/

---

## 7. Intended postcondition overwrites authoritative observed state

**Natural question:** The agent intended action A to change the world to state X, but the tool / environment explicitly shows that X did not happen. Why might later planning still proceed as if the intended state X were true?

**Why it initially looked good:** This was the strongest remaining edge after killing generic tool failure. It isolates a potentially surprising state-update bug: intention and observation could both be represented, yet the planner might consume the intended postcondition rather than the authoritative observation. That would be more specific than static tool-memory conflict.

**Kill evidence:** The practical and representational space has tightened substantially. `ToolGate` (Findings of ACL 2026) explicitly maintains trusted symbolic world state, formalizes each tool with preconditions and postconditions, and commits state updates only after runtime postcondition verification. `Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures` independently uses postcondition verification / verify-before-retry / idempotency to prevent exactly the consequences produced by incorrect state commitment. `PABU` (2026) also directly frames agent operation as explicit belief/progress-state updating. Even if an internal “intention overwrites observation” circuit were discoverable, the obvious successful method would still be an external verified-state layer that works irrespective of that circuit. Under P3 this is now a method collision, and the remaining mechanism story is too close to an already explicit belief/state-update framing.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** Do not revive as stale state, optimistic state update, intended-vs-actual postcondition, delayed visibility, partial execution, GUI state mismatch, or planner consuming an old belief. Those are the same execution-semantics family unless the verifier is already present and demonstrably insufficient.

**Resurrection condition:** Only reopen if authoritative verified state is already supplied in a trusted structured channel, ordinary verification wrappers still fail, and a selective internal causal mechanism makes the planner override that trusted state. The resulting mechanism must imply a repair that is not simply “verify/track state externally.”

**Key references:** https://aclanthology.org/2026.findings-acl.470/ ; https://arxiv.org/abs/2608.02645 ; https://arxiv.org/abs/2602.09138

---

## 8. LLM-native operational anomalies are not acceptable mother phenomena

**Natural-question test:** If removing `LLM / prompt / tool / CoT / instruction tuning` makes the question disappear, the topic does not satisfy the repository's phenomenon-first requirement.

**Killed examples from the August 27 search round:**

- multilingual tool-call argument serialization mismatch;
- thinking-mode-induced scope/refusal collapse;
- reasoning-vs-response instruction-following gap;
- LLM-judge persuasion by visible reasoning traces.

**Why they initially looked good:** Unlike earlier failed cognitive-bias candidates, these had large, already-reported effects on modern open-weight models, often tens of percentage points, and cheap local evaluation paths.

**Why they are still rejected:** Their mother questions are artifacts of LLM operation itself. They start from a model-specific failure and then search for a mechanism, rather than from a natural phenomenon or independently meaningful concept that happens to reveal a broad LLM failure. This violates the repository's I1 / phenomenon-first preference and is not the style exemplified by the lab's random-choice and real-vs-fictional projects.

**Death code:** `MOTHER_QUESTION_NOT_NATURAL`

**Nearest-neighbor warning:** Do not resurrect by replacing one interface with another, changing language, swapping reasoning mode, or using a different agent benchmark. Large effect size is necessary but not sufficient.

**Resurrection condition:** Only reconsider if the exact behavior can be grounded in an independently established natural phenomenon (not merely an engineering analogue) and the research question remains meaningful after deleting all LLM-specific vocabulary.

---

# Current lessons from the domain

1. Tool-use behavior papers are moving extremely fast in 2026; many intuitive failure modes are already explicitly benchmarked.
2. “Behavior exists but mechanism not yet done” is not enough. If a simple external verifier fixes the problem regardless of mechanism, the mechanism fails the method-closure requirement.
3. **Stateful execution semantics are no longer a safe generic survivor.** Verified symbolic state, postconditions, and belief-update frameworks now occupy much of the obvious space.
4. A viable future agent topic needs a decisive contrast that remains broken *despite* correct external verification/state tracking, so that the internal mechanism is genuinely necessary to the fix.
5. Surprise criterion: “agents are bad when tools fail” is unsurprising. A viable topic should expose a stronger dissociation that existing verified-state wrappers cannot already solve.
6. **Phenomenon-first is stricter than behavior-first.** A huge open-model failure is still unsuitable if the mother phenomenon only exists because LLMs, prompts, tools, or inference modes exist.
