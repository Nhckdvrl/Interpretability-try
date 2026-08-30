"""Build and exhaustively audit the frozen world-indexed truth bank."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRAMES = ("fictional_chronicle", "hypothetical", "rule_simulation")
PARAPHRASES = ("direct", "evaluation", "setting_aside")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluated_value(relation: dict) -> int:
    if relation["domain"] != "arithmetic":
        return int(relation["value"])
    operands = relation["operands"]
    operations = {
        "+": lambda: operands[0] + operands[1],
        "-": lambda: operands[0] - operands[1],
        "*": lambda: operands[0] * operands[1],
        "square": lambda: operands[0] ** 2,
    }
    return int(operations[relation["operator"]]())


def proposition(relation: dict, value: int) -> str:
    if relation["relation"] == "planet_ordinal":
        ordinals = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}
        return f"{relation['subject']} is the {ordinals[value]} planet from the Sun."
    if relation["relation"] == "atomic_number":
        return f"The atomic number of {relation['subject']} is {value}."
    return f"{relation['subject']} equals {value}."


def stipulation_text(statement: str, local_truth: bool, frame: str) -> str:
    valuation = statement if local_truth else f"it is not the case that {statement}"
    templates = {
        "fictional_chronicle": (
            "Consider a fictional chronicle whose world may differ from reality. "
            f"Within that chronicle, it is a settled fact that {valuation}"
        ),
        "hypothetical": (
            "Consider an explicitly stipulated hypothetical scenario, not a claim about reality. "
            f"For that scenario, assume that {valuation}"
        ),
        "rule_simulation": (
            "Consider a rule-defined simulation whose rules may differ from reality. "
            f"Inside that simulation, the rulebook establishes that {valuation}"
        ),
    }
    return templates[frame]


def question(statement: str, query_world: str, paraphrase: str, frame: str) -> str:
    local_name = {
        "fictional_chronicle": "the fictional chronicle",
        "hypothetical": "the stipulated hypothetical",
        "rule_simulation": "the rule-defined simulation",
    }[frame]
    templates = {
        ("actual", "direct"): f"In the actual world, is this statement true: {statement}",
        ("actual", "evaluation"): f"Evaluate the statement according to real-world facts: {statement}",
        ("actual", "setting_aside"): f"Setting aside the local scenario, is this true in reality: {statement}",
        ("local", "direct"): f"In {local_name}, is this statement true: {statement}",
        ("local", "evaluation"): f"Evaluate the statement according to {local_name}: {statement}",
        ("local", "setting_aside"): f"Regardless of actual-world facts, is this true inside {local_name}: {statement}",
    }
    return templates[query_world, paraphrase]


def rotated_false_value(relation: dict, domain_values: dict[str, list[int]]) -> int:
    values = domain_values[relation["domain"]]
    index = values.index(int(relation["value"]))
    return values[(index + 1) % len(values)]


def build(source: dict) -> list[dict]:
    relations = source["relations"]
    if len(relations) != 32 or len({row["id"] for row in relations}) != 32:
        raise ValueError("expected 32 unique source relations")
    for row in relations:
        if evaluated_value(row) != int(row["value"]):
            raise ValueError(f"source evaluation mismatch: {row['id']}")

    domain_values: dict[str, list[int]] = {}
    for domain in ("solar_system", "chemistry", "arithmetic"):
        domain_values[domain] = [int(row["value"]) for row in relations if row["domain"] == domain]
    if {domain: len(values) for domain, values in domain_values.items()} != {
        "solar_system": 8,
        "chemistry": 12,
        "arithmetic": 12,
    }:
        raise ValueError("unexpected source-domain counts")

    items: list[dict] = []
    proposition_index = 0
    for relation in relations:
        true_value = int(relation["value"])
        candidates = ((True, true_value), (False, rotated_false_value(relation, domain_values)))
        for actual_truth, claimed_value in candidates:
            if (claimed_value == true_value) != actual_truth:
                raise AssertionError("truth construction failure")
            statement = proposition(relation, claimed_value)
            proposition_id = f"{relation['id']}-{'t' if actual_truth else 'f'}"
            for relation_index, local_relation in enumerate(("aligned", "conflict")):
                local_truth = actual_truth if local_relation == "aligned" else not actual_truth
                context_index = proposition_index * 2 + relation_index
                frame = FRAMES[context_index % len(FRAMES)]
                context_id = f"{proposition_id}-{local_relation}"
                context = stipulation_text(statement, local_truth, frame)
                for query_offset, query_world in enumerate(("actual", "local")):
                    paraphrase = PARAPHRASES[(context_index + query_offset) % len(PARAPHRASES)]
                    gold = actual_truth if query_world == "actual" else local_truth
                    items.append(
                        {
                            "item_id": f"{context_id}-{query_world}",
                            "context_id": context_id,
                            "proposition_id": proposition_id,
                            "source_relation_id": relation["id"],
                            "domain": relation["domain"],
                            "proposition": statement,
                            "actual_truth": actual_truth,
                            "local_truth": local_truth,
                            "local_relation": local_relation,
                            "world_frame": frame,
                            "context": context,
                            "query_world": query_world,
                            "query_paraphrase": paraphrase,
                            "question": question(statement, query_world, paraphrase, frame),
                            "gold_label": "TRUE" if gold else "FALSE",
                        }
                    )
            proposition_index += 1
    audit(items)
    return items


def audit(items: list[dict]) -> None:
    if len(items) != 256 or len({row["item_id"] for row in items}) != 256:
        raise ValueError("bank must contain 256 unique queries")
    contexts: dict[str, list[dict]] = {}
    for row in items:
        contexts.setdefault(row["context_id"], []).append(row)
    if len(contexts) != 128:
        raise ValueError("bank must contain 128 contexts")
    for context_id, pair in contexts.items():
        if len(pair) != 2 or {row["query_world"] for row in pair} != {"actual", "local"}:
            raise ValueError(f"broken query pair: {context_id}")
        if len({row["context"] for row in pair}) != 1 or len({row["proposition"] for row in pair}) != 1:
            raise ValueError(f"context or proposition changed within pair: {context_id}")
    propositions: dict[str, list[dict]] = {}
    for row in items:
        propositions.setdefault(row["proposition_id"], []).append(row)
    if len(propositions) != 64:
        raise ValueError("bank must contain 64 propositions")
    for proposition_id, rows in propositions.items():
        if {row["local_relation"] for row in rows} != {"aligned", "conflict"}:
            raise ValueError(f"missing local relation: {proposition_id}")
    counts = Counter((row["query_world"], row["gold_label"]) for row in items)
    if set(counts.values()) != {64}:
        raise ValueError(f"query-world/label cells are not balanced: {counts}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "data" / "source_facts.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "d0_bank.jsonl")
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    items = build(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, sort_keys=True) + "\n")
    metadata = {
        "contract_id": json.loads((ROOT / "configs" / "d0_contract.json").read_text())["contract_id"],
        "source_sha256": sha256(args.source),
        "bank_sha256": sha256(args.output),
        "n_items": len(items),
        "n_contexts": len({row["context_id"] for row in items}),
        "n_propositions": len({row["proposition_id"] for row in items}),
        "counts_by_domain": dict(sorted(Counter(row["domain"] for row in items).items())),
        "counts_by_relation": dict(sorted(Counter(row["local_relation"] for row in items).items())),
        "counts_by_query_world": dict(sorted(Counter(row["query_world"] for row in items).items())),
        "counts_by_world_frame": dict(sorted(Counter(row["world_frame"] for row in items).items())),
        "counts_by_paraphrase": dict(sorted(Counter(row["query_paraphrase"] for row in items).items())),
    }
    args.output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
