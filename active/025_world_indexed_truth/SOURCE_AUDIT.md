# 025 D0 source audit

The exact factual inventory is saved in `data/source_facts.json`.

| Domain | Authority | Frozen use |
|---|---|---|
| Solar system | NASA Science, *About the Planets*, retrieved 2026-08-31 | ordinal positions 1–8 |
| Chemistry | IUPAC, *Periodic Table of Elements*, retrieved 2026-08-31 | selected atomic numbers |
| Arithmetic | deterministic local evaluator | exact integer results |

False actual-world propositions are not separately asserted facts. They are
constructed by rotating the true value within a domain, so the claimed value
is guaranteed to differ from the audited value. The builder rejects duplicate
IDs, arithmetic mismatches, unexpected domain counts, or a false proposition
whose rotated value accidentally equals the source value.

The local-world gold is licensed only by the explicit stipulation in that
context. It is not presented as evidence about reality. Aligned controls repeat
the actual truth value locally; conflict cases invert it. Thus the experiment
does not ask which source should win: both answers remain legitimate and the
query names the evaluation world.
