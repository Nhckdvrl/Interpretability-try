# 006 Frozen D0 Data

Status: `D0-PASS / READY-TO-SMOKE`

The natural D0 panel is frozen as:

- `frozen_d0_sources.jsonl`: 40 externally anchored historical domestic-Double source records;
- `build_frozen_d0.py`: deterministic identity-redaction transformation;
- `source_manifest.md`: all 40 source records;
- `manual_audit_20.md`: random 20-item manual audit, 20/20 PASS.

Source definition and historical tables:

https://en.wikipedia.org/wiki/Double_(association_football)

The model-visible unknown record deliberately omits the historical champion identity. Source club identity remains only in provenance metadata. This preserves the natural source while making the record itself compatible with both a shared-witness and a distinct-witness world.

Build the exact frozen JSONL before validation/model execution:

```bash
python data/build_frozen_d0.py
```

Expected output SHA256:

```text
6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0
```

Then validate:

```bash
existential-witness-run validate-data --data data/frozen_d0.jsonl
```

Do not edit generated rows after building them. If the hash changes, stop before model loading.
