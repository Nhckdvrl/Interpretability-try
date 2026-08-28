# 006 — Final Verdict

Status: `TERMINAL-KILLED / HARD-KILL-NO-ILLEGAL-JOIN`

Experiment commit: `aaf03c536e20b5cf83537c4f94a4e8a4476a0001`

## Frozen smoke integrity

- tests: `25 passed`
- frozen D0: 40 scenarios, 8 domains
- D0 SHA256: `6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0`
- Qwen raw rows: 1280
- Gemma raw rows: 1280
- no N1, panel expansion, scaling, or mechanism run was performed

## Qwen3-8B: decisive behavioral null

Qwen3-8B passed the full frozen capability denominator:

- recognition-gated: 40/40
- capability-gated: 40/40
- all 8 domains: 5 gated each
- strong cases: 0
- positive domains: 0

Primary readout:

- mean `p_collapse(unknown)`: `0.0000944347`
- mean unknown margin: `-0.4999056`
- bootstrap 95% CI: `[-0.4999324, -0.4998760]`
- mean paraphrase margin: `-0.4998068`
- mean unknown-minus-distinct: `0.00004278`
- natural variant positive fraction: `0`

This is not a weak or noisy negative result. The model recognized that identity was unresolved, passed explicit-same and explicit-distinct downstream controls, and then overwhelmingly selected the identity-preserving action in the unknown world. The frozen hard-kill criterion is therefore satisfied exactly:

`HARD-KILL-NO-ILLEGAL-JOIN`

## Gemma3-12B: not a valid positive denominator

Gemma3-12B had 0/40 recognition-gated cases, so it cannot provide a formal phenotype estimate under the frozen contract.

The failure is narrower than generic existential inability: existence probes and the no-shared-witness probe were near ceiling, while the `identity_determined` semantic forced choice was strongly answer-order unstable (case-level averages near 0.5 with one reversed order collapsing). The harness-level verdict remains:

`HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`

Gemma nevertheless handled explicit same/distinct downstream controls and assigned extremely low collapse probability in the unknown condition, so it provides no rescue signal for the target phenotype.

## Scientific disposition

The **current frozen natural operationalization** of Existential Witness Collapse is terminally killed. It produced no illegal witness fusion in the one model that cleanly passed the entire capability gate, and no positive evidence in the second family.

This does **not** prove that no LLM under any task can ever conflate existential witnesses. It means the present candidate, as a discovery-track behavioral claim under this natural D0 and frozen operator, has failed its pre-registered first-shot test and must not be rescued by prompt changes, weaker models, favorable slicing, threshold changes, or alternate datasets.

No N1 is warranted because there is no observed positive phenotype whose error destination requires a second novelty search.

Final disposition:

`TERMINAL-KILLED / HARD-KILL-NO-ILLEGAL-JOIN`
