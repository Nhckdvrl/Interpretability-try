# 006 claim–evidence ledger

All current white-box evidence is `D0 / exploratory`. “Supported” below means supported within the discovery corpus, not paper-confirmed. D0 was run in a dirty worktree before the mechanism code had a producing commit; its honest revision is therefore `unknown / dirty D0`, not the later publication commit.

| ID | Claim | Status | Evidence artifact | Code | Config / run manifest | Producing revision | Next decisive test |
|---|---|---|---|---|---|---|---|
| C0 | Qwen2.5 separates posterior estimation, direct policy use, and explicit-belief execution | Exploratory supported | `results/qwen25_14b_phase0_summary.json` | `src/mechanism_behavior.py` | `configs/phase0_behavior.json`; no run manifest | unknown / dirty D0 | Reproduce on frozen D2-ID and one generalization setting |
| C1 | A serialized number explicitly assigned the posterior role is sufficient to control bridge policy execution | Exploratory supported | `results/qwen25_14b_phase2_span_summary.json` | `src/residual_interchange.py`, `src/summarize_phase2.py` | CLI only; no frozen Phase-2 config/manifest | unknown / dirty D0 | Held-out family and topology-matched role interchange |
| C2 | Whole-number replacement is sufficient, while the final numeric token alone is insufficient | Exploratory supported | `MECHANISM_LOG.md`; gold number/statement summaries | `src/belief_span_cache.py`, `src/residual_interchange.py` | CLI only; no frozen Phase-2 config/manifest | unknown / dirty D0 | Eight single positions, prefix/suffix, leave-one-out, punctuation/digit controls |
| C3 | Source-span intervention efficacy decays over layers 16–24 | Exploratory supported | `results/qwen25_14b_phase2_span_summary.json` | `src/residual_interchange.py` | CLI only; no frozen Phase-2 config/manifest | unknown / dirty D0 | Locate a receiver and exact head/MLP/path; until then do not call it a handoff |
| C4 | The literal serialized value remains decodable at the source after swap efficacy disappears | Exploratory supported | `results/qwen25_14b_probe_belief_span_joint_summary.json` | `src/probe_belief_span.py` | CLI only; selected layers after D0 inspection | unknown / dirty D0 | Held-out values/formats, raw-token baselines, family-clustered inference |
| C5 | Direct prompts form an abstract posterior state homologous to bridge | Unresolved | Query probes are suggestive but confounded | `src/probe_timeline.py` | D0 exploratory CLI | unknown / dirty D0 | Held-out likelihood/posterior-equivalence causal formation tests |
| C6 | A causal role reader gates posterior transport | Hypothesis only | None | Planned in V2-D | V2 freeze pending | not run | Exact content × role four-cell intervention and generic-compliance subtraction |
| C7 | A middle-layer attention/MLP path transports belief into the comparator | Hypothesis only | Source-decay trajectory motivates it | Planned in V2-C | V2 freeze pending | not run | AtP* screen followed by exact path confirmation |
| C8 | Comparator/writer is distinct from late A/B binding | Hypothesis only | None | Planned in V2-E | V2 freeze pending | not run | Posterior × threshold factorial plus mapping swaps |
| C9 | A low-rank reader-gated edit selectively repairs direct use failures | Method prediction only | None | Planned in V2-F | Conditional on validated natural path | not run | No-gold gated edit versus random/unconditional controls |
| C10 | The mechanism generalizes across models and a natural benchmark | Unresolved | Behavioral model differences only | Planned replication | Model/task freeze pending | not run | One contrast model or one external task, then optional stretch replication |

## Governance rules

- A claim moves to `confirmatory supported` only from frozen D2-ID outputs; D2-OOD/T1 establish generalization separately.
- Layer, component, latent, rank, or strength selection must cite a D1 artifact.
- Every numeric table must be generated from saved raw rows by a committed script.
- Superseded files remain excluded from canonical summaries and are named in the manifest.
- Failed hypotheses are recorded; they are not removed from this ledger.
