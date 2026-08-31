# 034 — Prospective Memory Retrieval Architecture

Status: **PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-08-31

## A. Natural question

When a language-model agent must remember to do something later while continuing other work, does the future intention stay under strategic monitoring, re-enter computation only when a relevant cue triggers spontaneous retrieval, or switch between these modes depending on cue/context?

This question is independent of any benchmark name. It is the classic prospective-memory retrieval-architecture question: **strategic monitoring vs spontaneous retrieval vs dynamic/multiprocess control**.

## B. Why this is paper-scale

Prospective memory is a distinct form of goal-directed memory: an agent must maintain an intention while performing an ongoing task and recover it at the right future opportunity. Human prospective-memory research has long debated whether successful retrieval requires resource-consuming monitoring or can be triggered bottom-up by sufficiently focal cues; dynamic multiprocess accounts predict context-dependent switching.

The contribution is therefore not `PM-Bench fails -> find the failing layer`. It is: **what retrieval architecture supports future intentions in LLM agents?** The answer matters for long-horizon agents, tool use, reminders, delegated tasks, and any system that must remember latent goals without continuously rehearsing them.

## C. Scientific lineage

Key external theory objects predate LLMs:

- McDaniel & Einstein multiprocess theory of prospective memory.
- Strategic monitoring: maintaining an intention and checking the environment incurs ongoing-task cost.
- Spontaneous retrieval: focal cues can reactivate an intention without continuous monitoring.
- Dynamic multiprocess accounts: monitoring is engaged when target contexts/cues are expected and relaxed when spontaneous retrieval is sufficient.

Useful theory references:

- https://pubmed.ncbi.nlm.nih.gov/31886687/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7007322/
- prospective-memory monitoring / cue-focality literature cited by PM-Bench and TriggerBench.

## D. Strong mothers / established behavior

### PM-Bench

Public artifact: https://github.com/genglinliu/PMBench

The release contains:

- deterministic `data/synthetic_week_v9.json`;
- scorer/runtime and local model runner;
- eight model backbones x eight configurations = 64 released trajectories;
- open families including Llama-3.3-70B-Instruct, Mistral Small 3.2 24B, and Qwen3-8B/14B/32B;
- time-based intentions, event-based intentions, regular/irregular intentions, explicit cue IDs, and hidden state channels;
- monitoring/query actions and TP/FP/FN outcomes.

Released baseline behavior is substantial but imperfect rather than floor/ceiling. Across all eight models, single-baseline micro Set-F1 is about 59.4%; proactive/heartbeat variants change recall and false positives. Open-family examples include Llama-3.3-70B baseline Set-F1 64.4%, with meaningful variation under reminder/monitoring scaffolds.

### Independent corroboration

2026 prospective-memory work such as TriggerBench independently establishes that LLMs can retain retrospective content while failing to execute delayed intentions, especially under longer/overloaded contexts. TriggerBench's currently public GitHub is not used as the central substrate because the repository does not expose the promised full artifact.

## E. Exact novelty delta

Strongest nearby LLM work owns:

1. measuring prospective-memory success/failure;
2. comparing external TODO/heartbeat/memory scaffolds;
3. documenting context-length/overload effects.

It does **not** causally adjudicate the classic retrieval theories inside native open-weight LLMs using theory-diagnostic cue/context manipulations.

The delta is therefore:

> `Does prospective memory work? / which scaffold helps?`
> **→ `What retrieval architecture implements future intentions: monitoring, spontaneous cue-triggered retrieval, or dynamic switching?`**

This is not a generic behavior-to-mechanism step because the competing computations are an independent scientific debate with distinct behavioral and causal predictions.

## F. Venue-scale comparison

- **EMNLP 2025 Outstanding — filler-gap shared structure:** mature external theory question -> causal LM evidence. 034 follows the same shape: mature PM retrieval theories -> causal evidence in LLM agents.
- **NAACL 2025 — taxonomy vs similarity in property inference:** competing theories exist before the dataset and all outcomes preserve the headline question. Same here for monitoring vs spontaneous retrieval vs dynamic control.
- **ACL 2026 — tool irrelevance:** controlled task factors isolate natural variables rather than create them. Here cue focality/observability and target-context expectation are natural PM variables; PM-Bench is the microscope.
- **ACL 2025 Outstanding — contextual entrainment:** broad behavior plus causal mechanism. 034 already inherits broad cross-family PM behavior and asks a theory-grounded causal question rather than merely localizing an error.

## G. Data / substrate

```yaml
natural_or_synthetic: controlled simulated agent week + external behavioral corroboration
central_artifact: genglinliu/PMBench
central_gold: deterministic intended-action set, cue IDs/times/channels, action logs, state-query logs
why_dataset_is_only_a_measurement_window: prospective memory, cue focality, monitoring, spontaneous retrieval, and intention execution all predate PM-Bench
natural_cross_cells:
  - visible/event cues that arrive in the ordinary interaction stream
  - time-based intentions that require temporal monitoring
  - hidden-state event cues that require explicit state queries
  - regular vs irregular future intentions
external_validity_path:
  - long-horizon tool agents
  - reminder/delegation tasks
  - independent prospective-memory benchmarks
```

The controlled extension below is allowed because it manipulates established PM variables rather than inventing the scientific distinction.

## H. Competing mechanisms and frozen predictions

### H1 — Strategic monitoring

The intention remains causally active before cue occurrence. The model recurrently checks time/state/context for opportunities.

Predictions:

- a decodable/causally usable intention state persists during pre-cue ongoing-task turns;
- ablating that state **before** the cue selectively reduces later PM execution even when the cue itself is preserved;
- stronger monitoring-demand conditions (time/hidden-state/nonfocal cues) show greater pre-cue intention influence and greater ongoing-task/query cost;
- adding an explicit monitoring opportunity rescues nonfocal conditions more than already-focal visible cues.

### H2 — Spontaneous cue-triggered retrieval

The intention need not remain causally active during ordinary pre-cue processing; a focal cue reinstates it when encountered.

Predictions:

- pre-cue intention-state interventions have weak effect once the encoded intention remains in context;
- a sharp causal transition appears at cue presentation;
- patching/reinstating the cue-linked intention state at cue time rescues execution;
- focal visible cues can succeed with little monitoring/query activity, whereas nonfocal/hidden cues fail unless monitoring is externally supplied.

### H3 — Dynamic multiprocess control

The model strategically monitors only when the current context makes target occurrence likely or cue processing is nonfocal; otherwise it relies on spontaneous retrieval.

Predictions:

- pre-cue intention influence is conditional on target-context expectation / cue observability rather than globally present or absent;
- identical intentions switch causal signatures when cue focality/observability changes;
- intervention effects cross over: pre-cue monitoring-state disruption hurts expected/nonfocal conditions, while cue-time retrieval disruption hurts focal conditions more strongly.

These are computation-level alternatives, not early/middle/late localization labels.

## I. Frozen S0 / causal microscope

### S0-0 — existence (already satisfied by released artifact)

Requirement: substantial imperfect prospective-memory behavior on >=2 genuinely different open families, with auditable trajectories and exact scoring.

**PASS from released PM-Bench:** Llama, Mistral and Qwen families have non-floor/non-ceiling behavior and complete logged runs.

### S0-1 — native diagnostic cells

Use the released deterministic week first, before creating new stimuli:

1. visible event-triggered intentions;
2. time-triggered intentions;
3. hidden-channel event-triggered intentions requiring explicit query;
4. matched regular/irregular intentions where possible.

Do not select cells post hoc by effect size. Freeze all valid items satisfying the structural definitions.

### S0-2 — controlled focality/context clone

For a subset of intentions, make minimal meaning-preserving clones that manipulate only established PM retrieval variables:

- **focal-visible:** cue phrase itself appears in the ongoing input;
- **nonfocal/indirect:** the same opportunity is indicated without lexical cue overlap;
- **expected context:** preceding context makes the target channel/event class likely;
- **unexpected context:** same cue occurs without target-context expectation.

Task/action gold and underlying future intention remain identical. This is a causal microscope, not the source of the research question.

### Hard behavioral gate before expensive MI

The diagnostic contrast must be measurable on at least two of Qwen3 / Llama-3.3 / Mistral families under greedy or otherwise frozen decoding. Kill rather than rescue if:

- all cue/context cells are ceiling or floor;
- focal/nonfocal manipulation mainly changes basic comprehension of the cue;
- no common qualitative signature exists across at least two families;
- apparent monitoring effects vanish after controlling for whether the cue information was actually visible to the model.

A cheap forward-pass behavioral verification of the **frozen** contract is allowed; changing the question/cells after null is not.

## J. First mechanistic experiment contract

1. Reproduce a frozen subset of PM-Bench on analyzable open checkpoints (Qwen3-8B/14B, Mistral Small where infrastructure permits; Llama family for cross-family replication).
2. At encoding, pre-cue ongoing turns, cue arrival, and action decision, measure the causal availability of the **specific intention identity**, not generic task correctness.
3. Use matched clean/corrupted pairs that preserve ongoing-task content while changing which future intention is active.
4. Perform activation/path patching between these pairs at the pre-cue and cue-time stages.
5. Test the **interaction predicted by H1/H2/H3** across focal-visible vs monitoring-demand conditions. The target statistic is not `best layer`; it is the causal interaction between retrieval regime and intervention timing.
6. Include shuffled-donor, lexical-overlap, cue-comprehension, and ordinary retrospective-memory controls.

Primary discriminating statistic:

```text
(intervention effect pre-cue - intervention effect at cue)
    x
(focal-visible - monitoring-demand condition)
```

The sign/pattern of this interaction maps to the frozen theory predictions above.

## K. Story invariance

- **Result A — monitoring dominates:** future intentions remain actively monitored; LLM PM resembles sustained prospective control.
- **Result B — spontaneous retrieval dominates:** intentions are largely dormant until cues causally reinstate them.
- **Result C — crossover/dynamic:** LLMs switch between monitoring and spontaneous retrieval depending on cue/context.

All three results answer exactly:

> **What retrieval architecture supports prospective memory in LLM agents?**

No result requires retitling the paper as construct validity, benchmark failure, or layer localization.

## L. Fatal risks

1. Cue observability vs cognitive focality must not be conflated.
2. External heartbeat scaffolds are behavioral evidence, not themselves the claimed native mechanism.
3. Agent calls expose a fresh forward pass over conversation history; analyses must distinguish information present in context from information causally selected for current computation.
4. Do not claim human-like mechanisms from behavioral similarity alone; the paper's contribution is the causal architecture in LLMs.

## Registration verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
venue_comparators: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
substrate: PASS
existing_behavior: PASS
open_family_evidence: PASS
story_invariance: PASS
competing_mechanisms: PASS
frozen_S0_contract: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

Registration means the question and experiment contract are frozen; nulls terminate or answer the same question rather than trigger narrative narrowing.
