#!/usr/bin/env python3
"""Orchestrate the M12 freeze and enforce cross-split/one-factor invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from v2_data import generate, load_config, load_jsonl, sha256_file


CONFIGS = (
    "configs/dev/v2_d1.json",
    "configs/confirmatory/v2_d2_id.json",
    "configs/confirmatory/v2_d2_ood_likelihood.json",
    "configs/confirmatory/v2_d2_ood_composition.json",
    "configs/confirmatory/v2_d2_ood_numeric_range.json",
    "configs/confirmatory/v2_d2_ood_numeral_format.json",
    "configs/confirmatory/v2_d2_ood_template.json",
    "configs/confirmatory/v2_d2_ood_observation_order.json",
)

OOD_FIELD = {
    "likelihood_regime": "likelihood_regimes",
    "prior_count_composition": "count_pairs",
    "numeric_value_range": "decision_blocks",
    "numeral_format": "numeral_format",
    "prompt_template": "template_ids",
    "observation_order_family": "observation_orders",
}


def value_set(config: dict) -> set[float]:
    values = set()
    for block in config["decision_blocks"]:
        values.add(float(block["threshold"]))
        values.update(map(float, block["evidence_targets"]))
        for pair in block["external_pairs"]:
            values.update((float(pair["low"]), float(pair["high"])))
    return values


def audit_one_factor(config_path: Path) -> dict:
    resolved, source = load_config(config_path)
    factor = source["changed_factor"]
    expected = OOD_FIELD[factor]
    override_keys = set(source["overrides"])
    allowed = {"split", "evidence_class", expected}
    if override_keys != allowed:
        raise AssertionError(
            f"{config_path.name}: overrides {override_keys}, expected exactly {allowed}"
        )
    base, _ = load_config((config_path.parent / source["base_config"]).resolve())
    changed = {
        key
        for key in base
        if key not in {"split", "evidence_class"} and base.get(key) != resolved.get(key)
    }
    # changed_factor/base_config are provenance fields added by resolution.
    changed -= {"changed_factor", "base_config"}
    if changed != {expected}:
        raise AssertionError((config_path.name, changed, expected))
    return {
        "config": str(config_path),
        "changed_factor": factor,
        "changed_field": expected,
        "one_factor_only": True,
    }


def cross_split_audit(project: Path, metadata: dict[str, dict]) -> dict:
    d1_path = project / "configs/dev/v2_d1.json"
    d2_path = project / "configs/confirmatory/v2_d2_id.json"
    d1, _ = load_config(d1_path)
    d2, _ = load_config(d2_path)
    shared_fields = (
        "likelihood_regimes",
        "numeral_format",
        "action_vocabularies",
        "option_mappings",
        "rule_forms",
        "observation_orders",
        "template_ids",
        "inference_good",
    )
    for field in shared_fields:
        if d1[field] != d2[field]:
            raise AssertionError(f"D1/D2-ID mismatch in supported factor {field}")
    if value_set(d1) & value_set(d2):
        raise AssertionError(
            f"D1/D2-ID numeric overlap: {sorted(value_set(d1) & value_set(d2))}"
        )
    d1_counts = {tuple(pair) for pair in d1["count_pairs"]}
    d2_counts = {tuple(pair) for pair in d2["count_pairs"]}
    if d1_counts & d2_counts:
        raise AssertionError(f"D1/D2-ID count-pair overlap: {d1_counts & d2_counts}")
    d1_families = load_jsonl(project / "datasets/v2/d1/families.jsonl")
    d2_families = load_jsonl(project / "datasets/v2/d2_id/families.jsonl")
    if {row["family_id"] for row in d1_families} & {
        row["family_id"] for row in d2_families
    }:
        raise AssertionError("D1/D2-ID family overlap")
    for name, families in (("d1", d1_families), ("d2_id", d2_families)):
        actions = [row["evidence_action"] for row in families]
        if actions.count("ACT") != actions.count("WAIT"):
            raise AssertionError((name, actions.count("ACT"), actions.count("WAIT")))
    one_factor = []
    for relative in CONFIGS[2:]:
        one_factor.append(audit_one_factor(project / relative))
    return {
        "d1_d2_supported_factors_equal": list(shared_fields),
        "d1_d2_numeric_values_disjoint": True,
        "d1_d2_count_pairs_disjoint": True,
        "d1_d2_family_ids_disjoint": True,
        "evidence_actions_balanced_by_split": True,
        "one_factor_ood": one_factor,
        "dataset_summaries": {
            split: row["validation"] for split, row in sorted(metadata.items())
        },
    }


def run(project: Path, code_commit: str) -> dict:
    metadata = {}
    for relative in CONFIGS:
        config_path = project / relative
        config, _ = load_config(config_path)
        out_dir = project / "datasets/v2" / config["split"]
        metadata[config["split"]] = generate(config_path, out_dir, code_commit)
    audit = cross_split_audit(project, metadata)
    manifest = {
        "milestone": "M12",
        "freeze_version": "v2-m12-1",
        "code_commit": code_commit,
        "d1_status": "development-open",
        "d2_id_status": "sealed-unopened",
        "d2_ood_status": "sealed-unopened",
        "primary_independent_unit": "family_id",
        "primary_control": "topology-matched generic decision-score authority",
        "splits": metadata,
        "cross_split_audit": audit,
    }
    manifest_path = project / "manifests/M12_FREEZE.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    checksum_path = project / "manifests/M12_FREEZE.sha256"
    lines = [f"{sha256_file(manifest_path)}  {manifest_path.relative_to(project)}"]
    for split in sorted(metadata):
        split_dir = project / "datasets/v2" / split
        for name in (
            "families.jsonl",
            "factorial.jsonl.gz",
            "evidence.jsonl",
            "TOKEN_AUDIT.json",
            "REPORT_SCHEMA.json",
            "FREEZE.json",
        ):
            path = split_dir / name
            lines.append(f"{sha256_file(path)}  {path.relative_to(project)}")
    checksum_path.write_text("\n".join(lines) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--code-commit", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.project.resolve(), args.code_commit), indent=2))


if __name__ == "__main__":
    main()
