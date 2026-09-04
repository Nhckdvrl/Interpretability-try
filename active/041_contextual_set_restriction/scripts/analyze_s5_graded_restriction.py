"""Binary role or graded reduction? Read the S1 direction on worlds that vary how much a modifier narrows."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

DEGREES = [0, 1, 2, 3]


def cluster_bootstrap(units: dict[str, float], seed: int, n_boot: int) -> dict:
    keys = sorted(units)
    values = np.array([units[key] for key in keys])
    rng = np.random.default_rng(seed)
    draws = [float(values[rng.integers(0, len(keys), len(keys))].mean()) for _ in range(n_boot)]
    return {"estimate": float(values.mean()), "ci95": [float(v) for v in np.quantile(draws, [0.025, 0.975])]}


def s1_direction(s1_path: Path, fraction: float, train_families: list[str]):
    lines = [json.loads(line) for line in s1_path.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    rows = [row for row in lines if row["record_type"] == "example"]
    bundle = np.load(s1_path.with_name(metadata["states_file"]))
    keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
    position = list(metadata["depth_fractions"]).index(fraction)
    entries = []
    for row in rows:
        if (row["description_condition"] != "full" or row["mapping_index"] != 0
                or row["surface_form"] != "np" or row["family"] not in train_families):
            continue
        for slot in ["dim1", "dim2"]:
            key = f"{row['state_key']}|{slot}"
            if key in keys:
                entries.append((keys[key], int(slot == row["restricting_dimension"])))
    indices = np.array([e[0] for e in entries]); labels = np.array([e[1] for e in entries])
    features = bundle["states"][indices, position, :].astype(np.float32)
    centre, scale = features.mean(0), features.std(0) + 1e-6
    normalised = (features - centre) / scale
    direction = normalised[labels == 1].mean(0) - normalised[labels == 0].mean(0)
    direction = direction / max(float(np.linalg.norm(direction)), 1e-9)
    return direction, centre, scale, position


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--s1-results", type=Path, nargs="+", required=True)
    parser.add_argument("--depth-fraction", type=float, default=0.5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    n_boot = int(config["bootstrap_samples"])
    train_families = ["size_color", "texture_color", "fill_height"]
    test_families = ["material_color", "pattern_length", "color_curvature"]
    models = []
    for model_index, (path, s1_path) in enumerate(zip(args.inputs, args.s1_results)):
        lines = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        rows = [row for row in lines if row["record_type"] == "example"]
        seed = int(config["seed"]) + 100 * model_index

        margins = defaultdict(list)
        for row in rows:
            margins[(row["world_id"], row["description_condition"])].append(row["referent_margin"])
        means = {key: float(np.mean(values)) for key, values in margins.items()}
        degree_of = {row["world_id"]: row["restriction_degree"] for row in rows}
        behaviour = {}
        for degree in DEGREES:
            worlds = [w for w, d in degree_of.items() if d == degree]
            restricting = {w: means[(w, "full")] - means[(w, "drop_dim2")]
                           for w in worlds if (w, "full") in means and (w, "drop_dim2") in means}
            other = {w: means[(w, "full")] - means[(w, "drop_dim1")]
                     for w in worlds if (w, "full") in means and (w, "drop_dim1") in means}
            behaviour[str(degree)] = {
                "n_worlds": len(restricting),
                "omission_cost_graded_modifier": cluster_bootstrap(restricting, seed + degree, n_boot),
                "omission_cost_other_modifier": cluster_bootstrap(other, seed + 10 + degree, n_boot),
                "accuracy_full": float(np.mean([row["correct"] for row in rows
                                                if row["world_id"] in set(worlds)
                                                and row["description_condition"] == "full"])),
            }
        slope_units = {}
        for world, degree in degree_of.items():
            if degree == 0 or (world, "full") not in means:
                continue
            slope_units[world] = ((means[(world, "full")] - means[(world, "drop_dim2")]) - 0.0) / degree
        behaviour["per_unit_cost_over_degrees_1_to_3"] = cluster_bootstrap(slope_units, seed + 40, n_boot)

        direction, centre, scale, position = s1_direction(s1_path, args.depth_fraction, train_families)
        bundle = np.load(path.with_name(metadata["states_file"]))
        # NpzFile decompresses on every __getitem__, so pull the array out once
        states = bundle["states"]
        keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
        projections = defaultdict(list)
        for row in rows:
            if (row["description_condition"] != "full" or row["mapping_index"] != 0
                    or row["surface_form"] != "np" or row["family"] not in test_families):
                continue
            for slot, graded in [("dim2", True), ("dim1", False)]:
                key = f"{row['state_key']}|{slot}"
                if key not in keys:
                    continue
                vector = states[keys[key], position, :].astype(np.float32)
                value = float(((vector - centre) / scale) @ direction)
                projections[(row["restriction_degree"], graded)].append(value)
        projection_summary = {
            str(degree): {
                "graded_modifier": float(np.mean(projections[(degree, True)])),
                "other_modifier": float(np.mean(projections[(degree, False)])),
                "n": len(projections[(degree, True)]),
            } for degree in DEGREES
        }
        models.append({
            "model": metadata["model_checkpoint"], "depth_fraction": args.depth_fraction,
            "held_out_families": test_families,
            "behaviour_by_degree": behaviour, "projection_by_degree": projection_summary,
        })
    result = {"contract": "does the modifier-token role state scale with how much the modifier narrows the set",
              "models": models}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output)}))


if __name__ == "__main__":
    main()
