"""Build and audit the frozen 024 D0 bank from the public human source."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "configs" / "d0_contract.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def payoff(game: str, human: str, opponent: str) -> int:
    tables = {
        "PD": {("F", "F"): 5, ("F", "J"): 10, ("J", "F"): 0, ("J", "J"): 8},
        "BoS": {("F", "F"): 10, ("F", "J"): 0, ("J", "F"): 0, ("J", "J"): 7},
    }
    return tables[game][human, opponent]


def infer_opponent(game: str, human: str, score: int) -> str | None:
    candidates = [opponent for opponent in ("F", "J") if payoff(game, human, opponent) == score]
    if len(candidates) == 1:
        return candidates[0]
    return None


def download_source(destination: Path, contract: dict) -> None:
    source = contract["source"]
    url = (
        "https://raw.githubusercontent.com/eliaka/repeatedgames/"
        f"{source['commit']}/{source['path']}"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response, destination.open("wb") as out:
        out.write(response.read())


def load_rows(raw_path: Path, contract: dict) -> list[dict]:
    if not raw_path.exists():
        download_source(raw_path, contract)
    observed_hash = sha256(raw_path)
    expected_hash = contract["source"]["sha256"]
    if observed_hash != expected_hash:
        raise ValueError(f"raw source SHA mismatch: {observed_hash} != {expected_hash}")
    with raw_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build(rows: list[dict]) -> list[dict]:
    corrupt_trajectories = set()
    for row in rows:
        human = "F" if int(row["action"]) == 0 else "J"
        if infer_opponent(row["game"], human, int(row["score"])) is None:
            corrupt_trajectories.add((int(row["id"]), row["game"]))
    expected_corrupt = {(17, "BoS"), (38, "BoS"), (153, "PD")}
    if len(rows) == 3900 and corrupt_trajectories != expected_corrupt:
        raise ValueError(
            f"unexpected corrupt trajectory set: {sorted(corrupt_trajectories)} != {sorted(expected_corrupt)}"
        )

    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for source_index, row in enumerate(rows):
        participant = int(row["id"])
        game = row["game"]
        if (participant, game) in corrupt_trajectories:
            continue
        human = "F" if int(row["action"]) == 0 else "J"
        score = int(row["score"])
        opponent = infer_opponent(game, human, score)
        if opponent is None:
            raise AssertionError("corrupt trajectories must have been excluded")
        grouped[participant, game].append(
            {
                "source_index": source_index,
                "human_action": human,
                "opponent_action": opponent,
                "human_score": score,
                "opponent_policy": row["opponent"],
            }
        )

    bank: list[dict] = []
    for (participant, game), decisions in sorted(grouped.items()):
        if len(decisions) != 10:
            raise ValueError(f"participant {participant} / {game} has {len(decisions)} rounds")
        history: list[dict] = []
        for round_index, decision in enumerate(decisions, start=1):
            bank.append(
                {
                    "item_id": f"{game.lower()}-p{participant:03d}-r{round_index:02d}",
                    "participant_id": participant,
                    "game": game,
                    "round": round_index,
                    "opponent_policy": decision["opponent_policy"],
                    "history": list(history),
                    "human_action": decision["human_action"],
                    "descriptive_target_f": int(decision["human_action"] == "F"),
                    "normative_target_f": 1.0 if game == "PD" else 10.0 / 17.0,
                    "source_index": decision["source_index"],
                }
            )
            history.append(
                {
                    "round": round_index,
                    "human_action": decision["human_action"],
                    "opponent_action": decision["opponent_action"],
                    "human_score": decision["human_score"],
                }
            )
    return bank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=ROOT / "data" / "raw" / "repgames.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    args = parser.parse_args()

    contract = json.loads(CONTRACT_PATH.read_text())
    rows = load_rows(args.raw, contract)
    bank = build(rows)
    if len(rows) != 3900 or len(bank) != 3870:
        raise ValueError(f"expected raw=3900/bank=3870, found raw={len(rows)}, bank={len(bank)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for item in bank:
            handle.write(json.dumps(item, sort_keys=True) + "\n")

    counts = Counter((item["game"], item["round"] > 1) for item in bank)
    metadata = {
        "contract_id": contract["contract_id"],
        "raw_sha256": sha256(args.raw),
        "bank_sha256": sha256(args.output),
        "n_items": len(bank),
        "n_participants": len({item["participant_id"] for item in bank}),
        "n_complete_trajectories": len({(item["participant_id"], item["game"]) for item in bank}),
        "excluded_trajectories": ["BoS-p017", "BoS-p038", "PD-p153"],
        "counts": {f"{game}_{'primary' if primary else 'round1'}": n for (game, primary), n in counts.items()},
    }
    metadata_path = args.output.with_suffix(".metadata.json")
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
