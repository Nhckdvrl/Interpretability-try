# 024 D0 v1 Report — Mother Behavior Reproduction

**Contract:** `024-d0-v1-mother-reproduction`

**Verdict:** `HOLD_INCONCLUSIVE_D0`

**Mechanism authorization:** false

## Outcome

The open-pair preflight does not pass the frozen promotion gate. Gemma 3 1B
and Llama 3.2 1B show clean native-format base advantages; Qwen3 1.7B is null,
and SmolLM2 360M significantly reverses. All four pairs pass the decision-mass
and informativeness gates, so this is genuine family heterogeneity rather than
an invalid-token artifact.

The result is not a hard kill. The native median base-minus-aligned correlation
is positive (+.070), three families have a numerically positive native delta,
and three families favor base under the shared-plain control. However, only two
of four families meet the predeclared native family-pass rule; promotion
required at least three.

## Audited population

The upstream source provides 3,900 real participant decisions from repeated
Prisoner's Dilemma and Battle of the Sexes. Four impossible action/payoff rows
occur in three participant-game trajectories. Excluding those complete
trajectories before model calls leaves:

- 3,870 decisions in 387 complete ten-round trajectories;
- 3,483 round 2-10 decisions in the primary analysis;
- 195 participants represented;
- 1,746 primary PD decisions and 1,737 primary BoS decisions.

The deterministic bank SHA-256 is
`f62fb370fd7a4f989da7d609da69abc0b6b6e3245b798f7dd1eb68cf3dbc9057`.

## Exact paired checkpoints

| family | base revision | aligned revision |
|---|---|---|
| Qwen3 1.7B | `ea980cb0a6c2ae4b936e82123acc929f1cec04c1` | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` |
| Gemma 3 1B | `fcf18a2a879aab110ca39f8bffbccd5d49d8eb29` | `dcc83ea841ab6100d6b47a070329e1ba4cf78752` |
| Llama 3.2 1B | `9535bd9b1d1dea6acafbdc4813b728796aeb28da` | `5a8abab4a5d6f164389b1079fb721cfab8d7126c` |
| SmolLM2 360M | `f8027fd0eaeea54caa13c31d31b9fdc459c38b49` | `a10cc1512eabd3dde888204e902eca88bddb4951` |

The access-driven pair amendments are recorded in the frozen contract. No
affected family had a forward pass before its final pair was fixed.

## Primary native-format result

Pearson correlations use normalized `p(F)` against the observed human action,
on all round 2-10 decisions. Confidence intervals are 2,000-replicate
participant-cluster bootstrap intervals for `r_base - r_aligned`.

| family | base r | aligned r | delta r | 95% CI | base/aligned mass | pass |
|---|---:|---:|---:|---:|---:|---|
| Qwen | .522 | .519 | +.003 | [-.018, +.025] | .885 / 1.000 | no |
| Gemma | .502 | .257 | +.245 | [+.205, +.285] | .828 / 1.000 | yes |
| Llama | .480 | .343 | +.137 | [+.098, +.173] | .831 / .999 | yes |
| SmolLM | .264 | .356 | -.091 | [-.118, -.063] | .881 / .917 | no; reversal |

Aggregate frozen checks:

- native family passes: 2/4 (required 3/4);
- native mass passes: 4/4;
- native median delta-r: +.070 (required at least +.050);
- shared-plain positive families: 3/4.

## Shared-plain format control

| family | base r | aligned r | delta r | 95% CI | mass gate |
|---|---:|---:|---:|---:|---|
| Qwen | .522 | .334 | +.189 | [+.159, +.219] | pass |
| Gemma | .502 | .302 | +.199 | [+.174, +.224] | pass |
| Llama | .480 | .441 | +.040 | [+.027, +.054] | pass |
| SmolLM | .264 | .371 | -.106 | [-.139, -.074] | fail (.685 aligned mass) |

The Qwen contrast changes from null under native formatting to a large base
advantage under shared plain text. SmolLM reverses under both formats. Prompt
format therefore moderates the observable paired difference; it cannot be
treated as a nuisance already ruled out by this four-pair pilot.

## Game and normative-target diagnostics

The native effect also does not generalize uniformly across the two games:

- Gemma: PD +.350 delta-r; BoS -.003 (null);
- Llama: PD +.100; BoS +.146;
- Qwen: PD -.033; BoS +.017;
- SmolLM: PD -.200 reversal; BoS +.028.

PD supplies an independent normative target: `F` is strictly dominant. Native
alignment moves mean probability toward that target for Llama and SmolLM, but
away from it for Qwen and Gemma. Thus D0 does not support a family-general claim
that post-training simply strengthens the explicit PD normative action.

## Scientific adjudication

This pilot provides evidence that the mother object is accessible in some open
pairs, but not yet a stable four-family behavioral foundation for mechanistic
claims. Starting probes now would risk explaining Gemma/Llama-specific behavior
while calling it a general alignment transformation.

Topic 024 remains scientifically broad and potentially ACL/EMNLP/NAACL-sized:
the degradation-vs-retention-vs-late-arbitration question is unchanged. It is
placed on hold rather than narrowed. A future reactivation must freeze a
scale-matched replication using larger mother-listed pairs and the same natural
population, metrics, prompt families, and negative-family reporting. D0 v1
does not authorize hidden-state extraction, probing, patching, or steering.

## Reproducibility artifacts

- `configs/d0_contract.json`: outcome-independent contract and access amendments;
- `data/raw/repgames.csv`: pinned public source;
- `data/d0_bank.jsonl`: audited deterministic bank;
- `src/alignment_arbitration/`: build, scoring, validation and analysis code;
- `results/d0/*.jsonl`: all 46,440 checkpoint-format decision records;
- `results/d0/*.metadata.json`: exact revisions and decision-token IDs;
- `results/d0_analysis.json`: complete metrics, per-game and round trajectories;
- `results/d0_summary.csv`: compact frozen comparison table.
