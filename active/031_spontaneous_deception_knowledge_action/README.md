# 031 — Do Language Models Really Lie When They Fail?

Status: **ACTIVE / PASS-REGISTER / V0–V1 COMPLETE / V2 MECHANISTIC PREFLIGHT COMPLETE**

Route: **Hamdi Route B — established anomaly → construct-level causal audit**  
Canonical registration: [`../../phenomenon_miner/REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md`](../../phenomenon_miner/REGISTERED_SPONTANEOUS_DECEPTION_KNOWLEDGE_ACTION_2026-08-31.md)

## 1. One-sentence question

When an LLM answers a difficult benign reasoning question incorrectly but answers a matched easier follow-up correctly, did the difficult run already contain the correct internal state and suppress it, or was the difficult run's reasoning state itself wrong?

This decides whether the mother phenomenon is genuine **knowledge–action dissociation / spontaneous deception** or a reasoning failure that only looks deceptive under a behavioral proxy for internal belief.

## 2. Background and mother result

Mother: **Beyond Prompt-Induced Lies: Investigating LLM Deception on Benign Prompts** (Wu et al., ICLR 2026 Oral).

The paper studies benign graph-connectivity / linked-list reasoning rather than prompts that explicitly ask the model to lie. Its key behavioral construct is a matched inconsistency:

- a harder initial question is answered incorrectly;
- a related lower-load follow-up is answered correctly;
- the paper interprets this as evidence that the model had access to the truth but produced a deceptive initial answer.

The official repository goes well beyond a closed API study. It contains item-level outputs for analyzable open models including:

- Meta-Llama-3.1-8B-Instruct;
- Mistral-Nemo-Instruct-2407;
- Qwen2.5-32B-Instruct;
- Qwen3-30B-A3B;
- Qwen3-235B-A22B;
- Gemma-2-9B-it;
- additional proprietary/API systems.

For Qwen3-30B-A3B, the repository includes 1,000-item BrokenLinkedList files across multiple graph lengths, as well as local hidden-state extraction / layer-evolution tooling.

The mother also reports shortcut-like reasoning in which a model can effectively fabricate a missing edge during chain-of-thought and then answer from that fabricated state.

## 3. The unresolved construct

The mother uses easier matched behavior as a proxy for what the model "knows" or "believes." That proxy does **not** establish that the correct graph state is present during the difficult run before the wrong answer is written.

Our scientific contribution is therefore a causal audit of the mother construct.

### H1 — Genuine knowledge–action dissociation

The difficult run internally represents the correct missing-edge / reachability state, but a late shortcut, response policy or answer-selection process overrides it.

Prediction:
- correct graph-state information is causally present before answer emission;
- late intervention can restore the answer without rebuilding upstream reasoning.

### H2 — Reasoning-state corruption

The difficult run never reaches the correct internal graph state. Difficulty causes the model to hallucinate or miscompute connectivity; the easier follow-up succeeds because it requires a different/lower-load computation.

Prediction:
- no stable correct-state representation exists in the hard wrong run;
- rescue requires earlier graph/reasoning-state intervention.

### H3 — Competing correct and fabricated trajectories

Both a correct state and a fabricated shortcut state coexist. Difficulty changes which one controls the answer writer.

Prediction:
- both states can be recovered before output;
- targeted suppression/reinstatement changes which trajectory wins.

## 4. Data and artifacts

Official repository: `Xtra-Computing/LLM-Deception`.

Relevant mother artifacts:

- generated linked-list / broken-linked-list problems;
- forward and reverse question variants;
- item-level response CSVs by model and graph length;
- mother metrics for initial/follow-up inconsistency;
- local inference implementation;
- hidden-state / embedding extraction utilities.

Primary statistical unit:

> **same underlying graph instance × hard initial question × matched follow-up / reverse control**

Important frozen cells:

1. **mother-deceptive:** hard initial wrong + matched follow-up correct;
2. **hard-truthful:** hard initial correct;
3. **both-wrong:** hard and follow-up wrong;
4. **reverse-query controls:** same graph truth under opposite Yes/No wording;
5. where available, repeated samples of the same item yielding different outcomes.

Core graph truth must be computed with deterministic graph algorithms, not an LLM judge.

## 5. Initial model panel

Start from public mother outputs and then choose one checkpoint for mechanistic work.

Recommended order:

1. **Qwen3-30B-A3B** — rich public mother outputs and locally analyzable architecture;
2. **Llama-3.1-8B-Instruct** or **Gemma-2-9B-it** — smaller replication checkpoint;
3. Mistral-Nemo as a third-family replication if the mechanism survives.

Do not run all families before the causal measurement is validated.

## 6. Initial validation plan

### V0 — Reconstruct the mother's deceptive-event population from public outputs

Goal: define the exact mother phenotype without model calls.

Steps:

1. Pin the official repository revision.
2. Parse problem files into graph objects.
3. Compute ground-truth connectivity and missing-edge facts directly with NetworkX / deterministic graph code.
4. Parse existing response CSVs for at least Qwen3-30B-A3B and one smaller open checkpoint.
5. Recompute the mother's hard-wrong/follow-up-correct criterion from raw rows.
6. Verify reverse-question balance and graph-length distribution.
7. Freeze stable item IDs and all ground-truth graph metadata in a `validation_manifest`.

**Stop condition:** if the public outputs cannot reproduce a sizable mother-defined deceptive population, do not redefine deception with hand-picked CoTs.

### V1 — Lock a stable local phenotype on one open checkpoint

The public files establish existence, but causal MI needs locally reproducible runs.

Steps:

1. Sample a bounded frozen subset of mother-deceptive, hard-truthful and both-wrong items, matched by graph length and answer polarity.
2. Re-run the official local inference code using the same checkpoint/template and a deterministic or low-variance decoding configuration.
3. Measure which mother-deceptive items are stable enough for causal experiments.
4. Keep two populations separate:
   - **stable deterministic hard-wrong/follow-up-correct** items;
   - **stochastic outcome-switching** items.

The second population may later support trajectory-competition analysis, but it must not contaminate the core deterministic causal test.

### V2 — Define graph-state targets from the environment, not from outputs

Goal: measure whether the model internally represents the actual graph state.

For every frozen graph derive automatically:

- whether the critical edge exists;
- which edge is broken;
- whether source and target are reachable;
- minimal path / disconnected components;
- correct Yes/No answer.

Then:

1. identify prompt token spans corresponding to graph edges/nodes;
2. extract residual/attention states at end-of-prompt and selected reasoning positions;
3. train simple held-out readouts for **edge existence** and **reachability**, with graph-instance-grouped splits;
4. control answer polarity so the readout cannot merely infer the final Yes/No token.

A readout is only a measurement instrument; it does not establish deception.

### V3 — Time-lock the first corrupted/fabricated state

For hard-deceptive runs with explicit reasoning:

1. align generated reasoning tokens with graph entities/edges where possible;
2. track edge-existence and reachability readouts through the reasoning trajectory;
3. find whether the correct state appears before the first fabricated/miscomputed edge;
4. compare against hard-truthful and both-wrong controls;
5. repeat at end-of-prompt before any generated reasoning to distinguish prompt encoding from generated-state corruption.

Three possible observations are already discriminating:

- correct graph state never appears → favors H2;
- correct state appears then disappears → H1/H3-compatible;
- correct and fabricated states coexist → H3-compatible.

### V4 — Causal edge-state reinstatement

Core intervention.

A robust version should avoid treating arbitrary easy-prompt states as interchangeable with the hard prompt.

1. Localize a causal subspace/component for **critical edge absent / target unreachable** using matched graph controls.
2. On a hard-deceptive run, intervene on this state at the localized layer/token while leaving the visible hard prompt unchanged.
3. Test whether reinstating the correct graph state changes:
   - subsequent reasoning trajectory;
   - fabricated-edge occurrence;
   - final answer.
4. Reverse the intervention on hard-truthful runs.
5. Run same-norm random, unrelated-edge and answer-polarity controls.

If the correct state can be reinstated upstream and then naturally propagates to the right answer, the failure is not merely a late output preference.

### V5 — Late policy vs upstream reasoning test

After a causal graph-state locus is available:

- patch/ablate late answer-selection components while leaving graph state unchanged;
- compare the amount of rescue from early graph-state intervention vs late policy intervention;
- test whether the easy matched follow-up supplies a transferable **truth state** or merely a different computation.

Interpretation:

- late-only rescue + correct upstream state → H1;
- early-state reconstruction required → H2;
- selective winner-switching while both states remain available → H3.

## 7. Fatal controls

- Never define deception from visually striking CoTs; use mother event criteria.
- Ground-truth graph facts must come from deterministic graph code.
- Match graph length, answer polarity and problem type across conditions.
- Use reverse questions to control Yes/No response bias.
- Separate stochastic outcome changes from deterministic hard failures.
- A correct easy follow-up is **not** automatically evidence that the hard run contains the same state.
- t-SNE/embedding clusters are descriptive only; causal state intervention is required.
- Avoid probes that can decode final answer polarity instead of graph truth.

## 8. Promote / kill criteria

### Promote if

- public outputs reproduce a substantial exact mother-deceptive population;
- one analyzable checkpoint yields a stable local subset;
- graph-state measurement distinguishes truth from answer polarity;
- causal intervention can separate upstream graph-state corruption from late response control.

### Strong negative result

If hard-deceptive runs **never contain the correct graph state**, that does not kill the project. It directly challenges the mother paper's strong deception interpretation and supports reclassification as reasoning-state corruption.

### Kill / redesign if

- the mother event population disappears after deterministic graph-truth reconstruction or reverse-query controls;
- all "internal truth" signals reduce to answer-token/polarity leakage;
- causal interventions cannot distinguish hard-deceptive runs from ordinary hard wrong answers.

## 9. Paper-level narrative

> **When behavioral evaluations say an LLM is deceptive because it can reveal the truth under another query, is that truth actually present during the deceptive computation?**

This is a construct-validity and mechanism paper for deception evaluation, latent knowledge, reasoning hallucination and safety monitoring—not a search for a generic deception direction.
