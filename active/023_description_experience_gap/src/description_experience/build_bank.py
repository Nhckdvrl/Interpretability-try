"""Build and audit exact-frequency risky-choice stimuli."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_value(option: list[list[float]], scale: int) -> Decimal:
    return sum((Decimal(str(payoff * scale)) * Decimal(str(probability)) for payoff, probability in option), Decimal(0))


def percent(probability: float) -> str:
    value = int(round(probability * 100))
    return f"{value}%"


def exact_history(option: list[list[float]], scale: int, length: int, seed: int) -> list[int]:
    history: list[int] = []
    for payoff, probability in option:
        count = int(round(probability * length))
        if abs(count / length - probability) > 1e-9:
            raise ValueError(f"probability {probability} is not exact at N={length}")
        history.extend([int(payoff * scale)] * count)
    if len(history) != length:
        raise ValueError(f"support probabilities do not sum to one: {option}")
    random.Random(seed).shuffle(history)
    return history


def option_probability_text(option: list[list[float]], scale: int) -> str:
    return "; ".join(f"{percent(probability)} chance of payoff {int(payoff * scale):+d}" for payoff, probability in option)


def option_count_text(option: list[list[float]], scale: int, length: int) -> str:
    return "; ".join(
        f"payoff {int(payoff * scale):+d} occurred {int(round(probability * length))} times"
        for payoff, probability in option
    )


def stimulus(mode: str, displayed: dict[str, list[list[float]]], histories: dict[str, list[int]], scale: int, length: int) -> str:
    if mode == "description_probability":
        lines = [
            "The payoff distribution for one independent draw is stated explicitly.",
            f"Option A: {option_probability_text(displayed['A'], scale)}.",
            f"Option B: {option_probability_text(displayed['B'], scale)}.",
        ]
    elif mode == "description_counts":
        lines = [
            f"The complete empirical distribution is summarized as counts from exactly {length} recorded draws per option.",
            f"Option A: {option_count_text(displayed['A'], scale, length)}.",
            f"Option B: {option_count_text(displayed['B'], scale, length)}.",
            "Use these exact empirical frequencies for the next draw.",
        ]
    elif mode == "experience_exact":
        lines = [
            f"Below is the complete ordered record of exactly {length} past draws per option.",
            f"Option A history: {histories['A']}.",
            f"Option B history: {histories['B']}.",
            "Use these exact empirical frequencies for the next draw.",
        ]
    else:
        raise ValueError(mode)
    return "\n".join(lines)


def frequency_candidates(correct_probability: float) -> list[str]:
    correct = int(round(correct_probability * 100))
    foil = (correct + 25) % 105
    if foil > 100:
        foil -= 100
    if foil == correct:
        raise AssertionError("frequency foil collision")
    return [f"{correct}%", f"{foil}%"]


def build(gamble_data: dict, contract: dict) -> list[dict]:
    gambles = gamble_data["gambles"]
    if len(gambles) != contract["data"]["n_gambles"] or len({row["id"] for row in gambles}) != len(gambles):
        raise ValueError("unexpected or duplicate gamble inventory")
    records: list[dict] = []
    length = contract["data"]["history_length"]
    for gamble_index, gamble in enumerate(gambles):
        for label in ("A", "B"):
            probabilities = [row[1] for row in gamble[label]]
            if abs(sum(probabilities) - 1) > 1e-9:
                raise ValueError(f"probabilities do not sum to one: {gamble['id']}/{label}")
            exact_history(gamble[label], 1, length, 1)
        for scale in contract["data"]["amount_scales"]:
            canonical_ev = {label: expected_value(gamble[label], scale) for label in ("A", "B")}
            for option_order in contract["data"]["option_orders"]:
                mapping = {"A": "A", "B": "B"} if option_order == "canonical" else {"A": "B", "B": "A"}
                displayed = {display: gamble[canonical] for display, canonical in mapping.items()}
                target_display = next(display for display, canonical in mapping.items() if canonical == gamble["target"])
                displayed_ev = {display: canonical_ev[canonical] for display, canonical in mapping.items()}
                if displayed_ev["A"] > displayed_ev["B"]:
                    ev_gold = "A"
                elif displayed_ev["B"] > displayed_ev["A"]:
                    ev_gold = "B"
                else:
                    ev_gold = "TIE"
                for shuffle_index, shuffle_seed in enumerate(contract["data"]["shuffle_seeds"]):
                    histories = {}
                    for display, canonical in mapping.items():
                        stable_seed = shuffle_seed * 1000 + gamble_index * 10 + (0 if canonical == "A" else 1)
                        histories[display] = exact_history(gamble[canonical], scale, length, stable_seed)
                    unit_id = f"{gamble['id']}-s{scale}-o{option_order}-h{shuffle_index}"
                    for mode in contract["data"]["presentation_modes"]:
                        scenario_id = f"{unit_id}-{mode}"
                        shared = {
                            "scenario_id": scenario_id,
                            "unit_id": unit_id,
                            "gamble_id": gamble["id"],
                            "gamble_family": gamble["family"],
                            "human_direction": gamble["human_direction"],
                            "scale": scale,
                            "option_order": option_order,
                            "shuffle_index": shuffle_index,
                            "shuffle_seed": shuffle_seed,
                            "presentation_mode": mode,
                            "history_length": length,
                            "stimulus": stimulus(mode, displayed, histories, scale, length),
                            "target_display_label": target_display,
                            "display_mapping": mapping,
                            "displayed_expected_values": {key: str(value) for key, value in displayed_ev.items()},
                            "last_five_mean": {key: sum(value[-5:]) / 5 for key, value in histories.items()},
                        }
                        records.append({
                            **shared,
                            "item_id": f"{scenario_id}-choice",
                            "query_type": "choice",
                            "question": "Which option would you choose for one next draw?",
                            "candidates": ["A", "B"],
                            "gold_label": None,
                        })
                        records.append({
                            **shared,
                            "item_id": f"{scenario_id}-expected_value",
                            "query_type": "expected_value",
                            "question": "Using only the displayed probabilities or empirical frequencies, which option has the larger expected payoff?",
                            "candidates": ["A", "B", "TIE"],
                            "gold_label": ev_gold,
                        })
                        for display, query_type in (("A", "frequency_a"), ("B", "frequency_b")):
                            focal_payoff, focal_probability = displayed[display][0]
                            candidates = frequency_candidates(focal_probability)
                            records.append({
                                **shared,
                                "item_id": f"{scenario_id}-{query_type}",
                                "query_type": query_type,
                                "question": f"What percentage of the displayed outcomes for Option {display} have payoff {int(focal_payoff * scale):+d}?",
                                "candidates": candidates,
                                "gold_label": percent(focal_probability),
                            })
    audit(records, contract)
    return records


def audit(records: list[dict], contract: dict) -> None:
    expected = contract["data"]["expected_records"]
    if len(records) != expected or len({row["item_id"] for row in records}) != expected:
        raise ValueError(f"expected {expected} unique records, found {len(records)}")
    scenarios = {row["scenario_id"] for row in records}
    if len(scenarios) != contract["data"]["expected_scenarios"]:
        raise ValueError("unexpected scenario count")
    for scenario_id in scenarios:
        subset = [row for row in records if row["scenario_id"] == scenario_id]
        if {row["query_type"] for row in subset} != set(contract["data"]["query_types"]):
            raise ValueError(f"incomplete query set: {scenario_id}")
        if len({row["stimulus"] for row in subset}) != 1:
            raise ValueError(f"stimulus differs within scenario: {scenario_id}")
    counts = Counter((row["presentation_mode"], row["query_type"]) for row in records)
    if set(counts.values()) != {144}:
        raise ValueError(f"presentation/query cells not balanced: {counts}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gambles", type=Path, default=ROOT / "data" / "gambles.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    args = parser.parse_args()
    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    gamble_data = json.loads(args.gambles.read_text())
    records = build(gamble_data, contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    metadata = {
        "contract_id": contract["contract_id"],
        "gambles_sha256": sha256(args.gambles),
        "bank_sha256": sha256(args.output),
        "n_records": len(records),
        "n_scenarios": len({row["scenario_id"] for row in records}),
        "counts_by_query_type": dict(sorted(Counter(row["query_type"] for row in records).items())),
        "counts_by_presentation": dict(sorted(Counter(row["presentation_mode"] for row in records).items())),
        "counts_by_gamble_family": dict(sorted(Counter(row["gamble_family"] for row in records).items())),
    }
    args.output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
