# Rejected Candidates — Agent / Tool Use / Execution

**Domain:** tool-augmented LLM agents operating over stateful external environments.  
**Search status:** active scan, 2026-08-26.  
**Rule:** only candidates that initially looked genuinely promising are recorded here. Obvious brainstorms are omitted.

## Domain boundary

Natural phenomena in scope include:

- a tool call returns something unexpected or wrong and the agent reacts incorrectly;
- the environment changes but the agent fails to update its belief about the current state;
- the agent repeats, skips, or prematurely terminates tool-mediated workflows;
- external tool evidence conflicts with parametric memory;
- a task succeeds while the agent nevertheless has a wrong or incomplete model of the environment.

The goal is **not** to study function-calling syntax or benchmark accuracy per se. A surviving interpretability question must isolate a concrete behavioral failure and distinguish competing internal explanations such as observation parsing, state update, planning/routing, and late readout.

---

# 1. Generic runtime-tool failure recovery

**Natural question:** Why can an agent use tools well on the normal path, yet collapse when a tool becomes unavailable, stale, corrupted, or semantically wrong?

**Why it initially looked good:**

- extremely natural deployment problem;
- public stateful benchmarks now exist;
- failures are abundant rather than hypothetical;
- clean perturbation pairs can be generated automatically.

**Kill evidence:**

This mother question is already densely benchmarked and behaviorally decomposed.

- `FAILING TOOLS: Benchmarking LLM Agent Recovery Under Runtime Tool Failures` explicitly evaluates detection, transient/permanent fault discrimination, retry/fallback, verification, and uncertainty communication under availability denial, data staleness, silent no-ops, corrupted state, schema mismatch, disambiguation failure, and cascades. No tested model exceeds 11.47% under its base recovery evaluator.  
  https://openreview.net/pdf?id=j7YsSnA64D
- `When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents` / ToolMaze separately studies explicit-vs-implicit and transient-vs-permanent failures and reports strong degradation from over-trusting corrupted outputs and futile trial-and-error loops.  
  https://arxiv.org/abs/2606.05806
- `PlanBench-XL` further evaluates long-horizon planning when tools are missing, failing, or distracting and shows large degradation when failures lack explicit signals or require longer alternative routes.  
  https://arxiv.org/abs/2606.22388

A generic mechanism paper asking “what inside the model causes tool failure recovery problems?” would be downstream of an already crowded taxonomy and would have difficulty finding one decisive contrast broad enough for a Main-paper narrative.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive by swapping in another API domain, another tool benchmark, or another failure type while keeping the mother question “why agents fail when tools fail.”

**Resurrection condition:** A new failure must reveal a qualitatively different internal variable or dissociation not already captured by detection / retry / fallback / verification / replanning.

---

# 2. Success-shaped tool output / silent no-op trust

**Natural question:** Why does an agent sometimes believe an action succeeded merely because the tool response looks successful, even when the intended world-state change never occurred?

**Why it initially looked good:**

- one-sentence, production-realistic failure;
- very clean intended-state vs actual-state contrast;
- seems to permit observation-understanding vs state-update vs planner-use explanations.

**Kill evidence:**

`FAILING TOOLS` already includes **silent no-ops**, corrupted state, missing verification, and explicit scoring of whether the agent calls confirmation functions when available. Its dominant failure is missing verification/recovery rather than simply choosing the wrong tool.  
https://openreview.net/pdf?id=j7YsSnA64D

More importantly, the obvious method does not require knowing the internal mechanism: an authoritative postcondition/state check after a mutating tool call directly tests whether the intended effect occurred. State-grounded agent systems likewise enforce a backend-is-truth invariant through an authoritative state manager.  
https://arxiv.org/abs/2606.16307

Therefore a mechanism result risks becoming scientifically optional: whether the model failed because of observation parsing, optimistic prior, or late planner routing, the engineering repair can remain the same “verify authoritative state before committing.”

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** “HTTP 200 bias”, “success token bias”, “tool says done so model trusts it”, and “silent write failure” are the same family unless the proposed decisive contrast changes the required repair.

**Resurrection condition:** Evidence that two internal failure modes require meaningfully different repair policies and cannot both be solved by authoritative postcondition verification.

---

# 3. Blind retry / repeating a failed tool call

**Natural question:** Why does an agent repeat essentially the same failed action instead of changing strategy after receiving an error?

**Why it initially looked good:**

- common and immediately understandable;
- trajectories naturally provide success/failure matched pairs;
- could in principle separate failure-detection from replanning failure.

**Kill evidence:**

This behavior is already a central axis of current recovery benchmarks rather than an unclaimed phenomenon.

- `FAILING TOOLS` explicitly evaluates whether the model distinguishes transient from permanent faults and retries or falls back appropriately.  
  https://openreview.net/pdf?id=j7YsSnA64D
- ToolMaze reports complex tool topologies trapping agents in futile trial-and-error loops and specifically separates systematic replanning from blind trial-and-error.  
  https://arxiv.org/abs/2606.05806

The likely headline “the model detects the error but fails to route into replanning” is plausible but currently too close to the benchmark authors’ own decomposition; without a much more surprising dissociation, adding activation patching would look like mechanistic annotation of an existing story.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Same-call retry loops, retry-budget misuse, and failure to switch tools are not separate topics by themselves.

**Resurrection condition:** A strong natural dissociation such as correct explicit diagnosis of a permanent fault coexisting with a causally separable internal action policy that still repeats the blocked path, plus a repair unavailable from ordinary replanning prompts.

---

# 4. Generic tool-dependency / prerequisite ordering failures

**Natural question:** Why does an agent skip prerequisites or call later tools before obtaining information required by them?

**Why it initially looked good:**

- natural multi-step workflow failure;
- dependency DAGs give deterministic gold;
- ordering errors are cheap to detect and reproduce.

**Kill evidence:**

The planning space is already heavily benchmarked around exactly these long-horizon dependency and blocked-path issues. `PlanBench-XL` uses large tool ecosystems where agents must infer implicit subgoals, retrieve relevant tools, uncover intermediate evidence, and adapt when functions are blocked. Severe blocking drops GPT-5.4 from 51.90% to 11.36%, with longer alternative paths especially difficult.  
https://arxiv.org/abs/2606.22388

As a mechanism topic, “prerequisite representation vs planner ordering” currently lacks a surprising external phenomenon beyond the expected fact that long dependency chains are harder. It also risks becoming a graph-planning benchmark paper with interpretability appended later.

**Death code:** `LOW_SURPRISE`

**Nearest-neighbor warning:** Do not repackage as “dependency awareness”, “implicit subgoal representation”, or “tool DAG circuit” unless there is a counterintuitive behavioral dissociation first.

**Resurrection condition:** A natural setting where the model demonstrably knows every prerequisite relation individually yet systematically violates one specific class of dependencies during execution, with a non-obvious boundary condition.

---

# 5. Generic Tool–Memory Conflict

**Natural question:** When a tool result contradicts what the model already believes, why does the agent sometimes ignore the tool and fall back to parametric memory?

**Why it initially looked good:**

- concrete and important in tool-augmented systems;
- public behavior paper reports substantial failures, especially on STEM tasks;
- obvious competing explanations: tool output not encoded, encoded but loses arbitration, or late answer readout reverts to memory.

**Kill evidence:**

The exact behavior has already been introduced as `Tool-Memory Conflict (TMC)` and systematically studied across conditions; prompting and RAG-based resolution methods were also evaluated and found insufficient.  
https://arxiv.org/abs/2601.09760

More importantly, the nearest parent problem — context vs parametric memory conflict — already has strong mechanistic work. `Taming Knowledge Conflicts in Language Models` (ICML 2025) challenges the simple context-head / memory-head story, finds superposition of contextual and parametric information in influential heads, and introduces a test-time attention intervention (JuICE).  
https://proceedings.mlr.press/v267/li25c.html

By 2026, task dependence of context-memory conflict has also been studied explicitly across different knowledge requirements.  
https://aclanthology.org/2026.findings-acl.202/

Thus “find the internal direction/pathway that decides tool vs memory and steer it” risks being a tool-output instantiation of an already mature context-memory conflict narrative.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Calculator-vs-memory, search-vs-memory, code-execution-vs-memory, and database-vs-memory are not distinct topics unless the tool interaction introduces a genuinely new causal variable beyond external textual evidence.

**Resurrection condition:** A decisive contrast unique to *actions/tools* rather than context, e.g. conflict between an agent’s predicted post-action state and an authoritative observed state after the agent itself caused the transition.

---

# 6. “Agents do not understand their environment” as a generic world-model question

**Natural question:** Do tool-using agents actually understand the environment they operate in, or can they succeed without a grounded world model?

**Why it initially looked good:**

- highly natural and potentially surprising;
- `Task2Quiz` gives deterministic, public environment-grounded QA rather than subjective labels;
- task success and environment understanding are empirically dissociable.

**Why the generic version is rejected:**

`Task2Quiz / T2QBench` already makes this mother question explicit and reports that task success is a poor proxy for environment understanding; recent memory mechanisms do not substantially improve grounded environment understanding, and insufficient proactive exploration is identified as a major bottleneck.  
https://arxiv.org/abs/2601.09503

A paper that merely adds probes to ask “does the model encode environment state?” would be too close to that narrative and could easily collapse into decodability without a specific failure event.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** “task success ≠ world understanding”, “agents lack world models”, and “environment knowledge is decodable” are not sufficient mother questions anymore.

**Resurrection condition:** Narrow to a concrete **state-transition failure** with matched pre-action / intended-postcondition / observed-postcondition cases and ask where the model’s belief update goes wrong. That is a different question from whether global environment knowledge exists at all.

---

# Domain lesson so far

The crowded part of agent/tool-use research is now clear:

```text
tool fails
→ agent should detect / retry / fallback / verify / replan
```

This is behaviorally important but already benchmark-rich, and many repairs can be implemented in the harness without needing mechanistic understanding.

The more promising unclaimed edge is narrower:

```text
before action: model represents intended postcondition
actual tool execution: environment changes (or fails to)
after observation: model forms some belief about current state
next action: planner consumes or ignores that belief
```

A viable interpretability topic must identify a **natural dissociation among these stages**, not merely show that the agent failed. In particular, the potentially interesting question is whether an agent can correctly represent both its intention and the authoritative observation yet still internally overwrite the observed world with its intended world, or whether the failure occurs earlier because the observation never becomes a stable state representation.

This surviving edge is intentionally **not** entered as a rejected candidate yet; it remains under collision audit.