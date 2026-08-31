# NTSB causal-relevance / causal-role substrate audit — S0 result

Date: 2026-08-31
Status: **`S0 PASS / G0 READY / NOT REGISTERED / NO MI`**

This result supersedes the prior `ARTIFACT-EXECUTION-BLOCKER` wording for the
NTSB frontier. It does **not** promote the topic to `PASS-REGISTER`: no current
open-model behavioral dissociation has yet been established.

## 1. Official artifact actually downloaded and parsed

Source: NTSB aviation download directory, `avall.zip`.

The audit was executed on a GitHub-hosted runner because the chat binary-fetch
path could enumerate but not retrieve the NTSB octet-stream endpoint. The runner
successfully downloaded the **official NTSB file**, unzipped the MDB, enumerated
tables, exported `findings` and `events` with `mdbtools`, and ran the deterministic
audit in this repository.

Frozen SHA-256:

```text
avall.zip  0cf30a610d18eb109035b83106c227b248f27c6cff794ce622548f44c455238a
```

Workflow run: `33362750201` (`NTSB S0 artifact audit`), all execution steps
completed successfully.

## 2. Exact findings counts

Official export contains:

| quantity | count |
|---|---:|
| finding rows | 72,381 |
| events with findings | 24,262 |
| events with >=2 findings | 21,240 |
| `Cause_Factor = C` | 37,764 |
| `Cause_Factor = F` | 5,758 |
| `Cause_Factor = blank` | 28,859 |
| `cm_inPC = T` | 61,041 |
| `cm_inPC = F` | 11,340 |
| events containing >=1 C and >=1 F | **3,506** |
| events with >=2 `cm_inPC=T` findings | 19,252 |

Exact `Cause_Factor × cm_inPC` cross-table:

| legacy role | `cm_inPC=F` | `cm_inPC=T` |
|---|---:|---:|
| blank | 11,340 | 17,519 |
| C | 0 | 37,764 |
| F | 0 | 5,758 |

The mixed-role population is therefore not a schema mirage or tiny tail: **3,506
real investigations contain both an NTSB Cause and an NTSB Factor**.

## 3. Critical semantics: two different golds, not one label

The NTSB release notes define `cm_inPC` as whether a finding is cited in the
probable-cause statement **as either a cause or a contributing factor**. Historical
`Cause_Factor` encoded the finer legacy role: `C = Cause`, `F = Factor`, blank =
other Finding.

The official migration is visible in the actual artifact:

- every legacy `C` row is `cm_inPC=T`;
- every legacy `F` row is `cm_inPC=T`;
- 17,519 legacy-blank rows are also now `cm_inPC=T`;
- from 2021 onward `Cause_Factor` is no longer populated, while `cm_inPC`
  continues to be populated.

Therefore **`cm_inPC` must never be used as a principal-cause / cause-vs-factor
label**. It is the relevance/inclusion gold. The C/F analysis must be restricted
to the historical population where the official role label exists.

This changes the scientific formulation from a vague `principal cause` selector
to the cleaner ordinary question:

> **If a model can identify which facts mattered to an accident, can it distinguish
> what caused the accident from what merely contributed to it?**

## 4. Deterministic random-20 audit

The repository audit ranks mixed-C/F event IDs by
`SHA256("2026-08-31-ntsb-s0" || ev_id)` and saves the first 20 events. The sample
contains 83 finding rows.

Manual semantic sanity from this frozen audit shows ordinary investigation-level
role distinctions rather than coding noise. Examples include:

- failure to maintain directional control (`C`) vs crosswind (`F`);
- inadequate wind compensation (`C`) vs recognition/experience conditions (`F`);
- walking into a rotating propeller (`C`) vs low experience / inadequate briefing
  (`F`).

The random audit also confirms that some findings are neither C nor F and have
`cm_inPC=F`, giving a natural relevance stage before conditional role selection.

## 5. Narrative availability and anti-leakage population

A second official workflow (`33362944073`) exported `narratives` from the same
frozen `avall.zip` and joined it to the 3,506 mixed-C/F events.

Results:

| population check | count |
|---|---:|
| mixed C/F events | 3,506 |
| with usable accident narrative + probable-cause narrative | **3,503** |
| missing probable-cause narrative | 3 |
| input narrative contains phrase `probable cause` | 1 |
| input narrative contains phrase `contributing factor(s)` | 6 |
| leak-clean usable population | **3,496** |

Input text is frozen as the NTSB Final Narrative (`narr_accf`) when available,
falling back to the Preliminary Narrative (`narr_accp`). The NTSB Probable Cause
Narrative (`narr_cause`) is held out from the ordinary model input and reserved for
an oracle/interface control.

Legacy public `finding_description` strings often append literal ` - C` / ` - F`.
The population builder strips that suffix before any tested-model prompt. The
first deterministic 300-event manifest additionally excludes the seven events
whose input narrative contains explicit `probable cause` / `contributing factor`
role language.

Frozen source SHA for this second workflow is identical:

```text
0cf30a610d18eb109035b83106c227b248f27c6cff794ce622548f44c455238a
```

## 6. What S0 now establishes — and what it does not

Established:

1. objective expert role gold exists without new annotation;
2. row-level official artifact was actually downloaded and parsed;
3. mixed causal roles are broad (3,506 investigations);
4. nearly all mixed-role cases have ordinary narrative input;
5. the core labels can be hidden from the input without inventing synthetic worlds;
6. relevance (`cm_inPC`) and legacy role (`C/F`) are empirically and semantically
   distinct.

Not established:

- that current open models recognize relevance well;
- that they systematically fail only at C-vs-F role selection;
- that the resulting behavior is broad across >=2/3 interpretable families;
- that N0/N1 survive recent accident-causality / actual-causation neighbors;
- any internal mechanism.

So the only authorized next stage is **behavioral G0**. No probe, SAE, activation
patching or steering is authorized.

## 7. Hard kill after S0

If current open models do not show the following broad dissociation, terminate:

```text
high causal-relevance identification
+ substantially weaker cause-vs-factor role assignment
+ oracle/interface control passes
+ same direction in >=2/3 current open families
```

A generic `cause vs factor classification is hard` result is insufficient and is
already close to recent incident-analysis work. The behavior must specifically
show that **relevance is intact while downstream causal-role selection fails**.

No rescue by Part-91-only subsets, fatalities, one accident type, one model,
longer chain-of-thought, another prompt, or a redefinition of `C/F`.
