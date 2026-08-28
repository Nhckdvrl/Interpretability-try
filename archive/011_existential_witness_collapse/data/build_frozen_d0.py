from __future__ import annotations

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen_d0_sources.jsonl"
OUT = HERE / "frozen_d0.jsonl"
SOURCE_URL = "https://en.wikipedia.org/wiki/Double_(association_football)"
SOURCE_DATASET = "Wikipedia: Double (association football), domestic Double tables"
SOURCE_LICENSE = "CC BY-SA 4.0"
EXPECTED_SHA256 = "6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0"

TRUE_GOLD = (
    "p_exists_gold",
    "q_exists_gold",
    "shared_witness_not_entailed_gold",
    "identity_underdetermined_gold",
    "joint_witness_possible_gold",
    "distinct_witness_possible_gold",
    "premises_do_not_identify_witnesses_gold",
    "same_explicit_authorizes_collapse_gold",
    "distinct_explicit_blocks_collapse_gold",
    "unknown_requires_identity_check_gold",
    "action_pair_matched_gold",
    "paraphrase_equivalent_gold",
    "neutral_control_equivalent_gold",
    "matched_base_gold",
    "natural_setting_gold",
)


def _load_sources() -> list[dict]:
    rows = []
    for lineno, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid source JSONL line {lineno}") from exc
        required = ("country_key", "country", "league", "cup", "club", "season")
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in required):
            raise ValueError(f"source line {lineno}: missing required text field")
        rows.append(row)
    if len(rows) != 40:
        raise ValueError(f"frozen source panel must contain exactly 40 rows, got {len(rows)}")
    if len({(r["country_key"], r["season"]) for r in rows}) != len(rows):
        raise ValueError("duplicate country-season source record")
    return rows


def build_record(src: dict) -> dict:
    key = src["country_key"]
    country = src["country"]
    league = src["league"]
    cup = src["cup"]
    club = src["club"]
    season = src["season"]
    sid = f"football:{key}:{season.replace('–', '-')}"

    row = {
        "scenario_id": sid,
        "domain": f"football_{key}",
        "premise_p": f"The archived {season} {country} season record establishes that at least one club won the {league}.",
        "premise_q": f"The archived {season} {country} season record establishes that at least one club won the {cup}.",
        "premise_paraphrase": (
            f"The {season} {country} season summary records a champion of the {league} and a champion "
            f"of the {cup}; in this excerpt, the champion names are omitted."
        ),
        "p_property": f"won the {league} in the {season} {country} season",
        "q_property": f"won the {cup} in the {season} {country} season",
        "shared_requirement": (
            f"A season may be entered in the domestic-Double register only if one and the same club "
            f"won both the {league} and the {cup}."
        ),
        "decision_context": (
            "A sports archivist must decide whether the domestic-Double entry is already justified "
            "by the current identity-redacted record."
        ),
        "collapse_action": "Enter the season in the domestic-Double register as already established.",
        "preserve_action": (
            "Keep the Double entry unresolved until the champion identities are shown to be the same club."
        ),
        "same_witness_addendum": (
            f"The full record explicitly states that one and the same club won both the {league} and the {cup}."
        ),
        "distinct_witness_addendum": (
            f"The full record explicitly states that the {league} champion and the {cup} winner were different clubs."
        ),
        "neutral_addendum": f"Both competitions belong to the same {season} {country} football season.",
        "source": {
            "dataset": SOURCE_DATASET,
            "record_id": f"{country}:{club}:{season}",
            "split": key,
            "license": SOURCE_LICENSE,
            "url": SOURCE_URL,
            "provenance": "external-derived-redacted-identity",
            "source_world": "same_witness",
            "source_club": club,
            "source_season": season,
            "memory_risk": "low",
        },
    }
    for field in TRUE_GOLD:
        row[field] = True
    return row


def render() -> str:
    rows = [build_record(src) for src in _load_sources()]
    return "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)


def main() -> None:
    text = render()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"frozen D0 hash mismatch: {digest} != {EXPECTED_SHA256}")
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} ({text.count(chr(10))} rows)")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
