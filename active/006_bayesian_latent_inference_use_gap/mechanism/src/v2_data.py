#!/usr/bin/env python3
"""Generate and audit the frozen V2 causal-family datasets for project 006."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Iterable


PRIMARY_CONDITIONS = (
    "posterior_use",
    "posterior_ignore",
    "generic_use",
    "generic_ignore",
)


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def action_for(value: float, threshold: float) -> str:
    return "ACT" if value > threshold else "WAIT"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_key(*parts: object) -> str:
    return sha256_bytes("::".join(map(str, parts)).encode())


def dump_jsonl(rows: Iterable[dict], path: Path) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
        + ("\n" if rows else "")
    )
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(text.encode("utf-8"), mtime=0))
    else:
        path.write_text(text, encoding="utf-8")


def load_jsonl(path: Path) -> list[dict]:
    if path.suffix == ".gz":
        text = gzip.decompress(path.read_bytes()).decode("utf-8")
    else:
        text = path.read_text()
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_config(path: Path) -> tuple[dict, dict]:
    """Return resolved config and the source wrapper used to produce it."""
    source = json.loads(path.read_text())
    if "base_config" not in source:
        return source, source
    base_path = (path.parent / source["base_config"]).resolve()
    base, _ = load_config(base_path)
    resolved = {**base, **source["overrides"]}
    resolved["changed_factor"] = source["changed_factor"]
    resolved["base_config"] = str(base_path)
    return resolved, source


def evidence_llr(regime: dict, n_red: int, n_blue: int) -> float:
    p_red_a = regime["p_red_a"]
    p_red_b = regime["p_red_b"]
    return (
        n_red * math.log(p_red_a / p_red_b)
        + n_blue * math.log((1.0 - p_red_a) / (1.0 - p_red_b))
    )


def solve_prior(target: float, regime: dict, n_red: int, n_blue: int) -> float:
    return sigmoid(logit(target) - evidence_llr(regime, n_red, n_blue))


def select_decompositions(
    target: float,
    regimes: list[dict],
    count_pairs: list[list[int]],
    count: int,
    seed: int,
    prior_bounds: tuple[float, float],
) -> list[dict]:
    candidates = []
    for regime in regimes:
        for n_red, n_blue in count_pairs:
            prior = solve_prior(target, regime, n_red, n_blue)
            if not prior_bounds[0] <= prior <= prior_bounds[1]:
                continue
            check = sigmoid(logit(prior) + evidence_llr(regime, n_red, n_blue))
            if not math.isclose(check, target, abs_tol=1e-12):
                raise AssertionError((target, check))
            candidates.append(
                {
                    "likelihood_id": regime["id"],
                    "p_red_a": regime["p_red_a"],
                    "p_red_b": regime["p_red_b"],
                    "n_red": n_red,
                    "n_blue": n_blue,
                    "prior_a": prior,
                    "evidence_llr": evidence_llr(regime, n_red, n_blue),
                    "gold_p_a": target,
                }
            )
    candidates.sort(
        key=lambda row: stable_key(
            seed,
            f"{target:.6f}",
            row["likelihood_id"],
            row["n_red"],
            row["n_blue"],
        )
    )
    selected: list[dict] = []
    # First ensure likelihood-regime coverage, then fill deterministically.
    for regime in regimes:
        row = next(
            (item for item in candidates if item["likelihood_id"] == regime["id"]),
            None,
        )
        if row is not None and row not in selected:
            selected.append(row)
    for row in candidates:
        if row not in selected:
            selected.append(row)
        if len(selected) >= count:
            break
    if len(selected) < count:
        raise ValueError(
            f"Only {len(selected)} valid decompositions for target={target}; need {count}"
        )
    return selected[:count]


def numeral_text(value: float, format_id: str) -> str:
    if format_id == "decimal6":
        return f"{value:.6f}"
    if format_id == "percent2":
        return f"{100.0 * value:.2f}%"
    if format_id == "logodds6":
        return f"{logit(value):+.6f}"
    raise ValueError(format_id)


def evidence_text(evidence: dict, observation_order: str) -> str:
    n_red = evidence["n_red"]
    n_blue = evidence["n_blue"]
    if observation_order == "red_first":
        observed = f"red count {n_red:02d}; blue count {n_blue:02d}"
    elif observation_order == "blue_first":
        observed = f"blue count {n_blue:02d}; red count {n_red:02d}"
    elif observation_order == "sequence_blocks":
        observed = "sequence " + " ".join(["red"] * n_red + ["blue"] * n_blue)
    else:
        raise ValueError(observation_order)
    return (
        "A hidden source is Type A or Type B. "
        f"Prior P(A)={evidence['prior_a']:.8f}. "
        f"Type A emits red with probability {evidence['p_red_a']:.2f} and blue "
        f"with probability {1.0 - evidence['p_red_a']:.2f}; Type B emits red "
        f"with probability {evidence['p_red_b']:.2f} and blue with probability "
        f"{1.0 - evidence['p_red_b']:.2f}. Observations: {observed}."
    )


def posterior_prompt(evidence: dict, observation_order: str) -> str:
    return (
        evidence_text(evidence, observation_order)
        + " What is P(A | observations)? Answer as a probability with exactly two "
        "digits after the decimal point."
    )


def rule_text(threshold: float, words: dict, rule_form: str) -> str:
    high, low = words["ACT"], words["WAIT"]
    t = f"{threshold:.6f}"
    if rule_form == "gt_high_first":
        return (
            f"If the selected control value is greater than {t}, the policy selects "
            f"{high}; otherwise it selects {low}."
        )
    if rule_form == "le_low_first":
        return (
            f"The policy selects {low} when the selected control value is less than "
            f"or equal to {t}; otherwise it selects {high}."
        )
    raise ValueError(rule_form)


def control_record(value_text: str, condition: str, template_id: str) -> str:
    if condition == "posterior_use":
        value_type, mode = "POSTERIOR", "USE"
    elif condition == "posterior_ignore":
        value_type, mode = "POSTERIOR", "IGNORE"
    elif condition == "generic_use":
        value_type, mode = "DECISION_SCORE", "USE"
    elif condition == "generic_ignore":
        value_type, mode = "DECISION_SCORE", "IGNORE"
    else:
        raise ValueError(condition)
    if template_id == "record_v1":
        return (
            " Control record: "
            f"VALUE={value_text}; TYPE={value_type}; MODE={mode}."
        )
    if template_id == "record_v2":
        return (
            " Decision register: "
            f"VALUE={value_text}; TYPE={value_type}; MODE={mode}."
        )
    raise ValueError(template_id)


def role_instructions(format_id: str) -> str:
    if format_id == "decimal6":
        scale = "VALUE uses the 0-to-1 numerical scale."
    elif format_id == "percent2":
        scale = "VALUE uses percentage notation; convert it to the 0-to-1 scale."
    elif format_id == "logodds6":
        scale = "VALUE uses log-odds notation; convert it to the 0-to-1 scale."
    else:
        raise ValueError(format_id)
    return (
        " POSTERIOR means that VALUE is a supplied posterior probability. "
        "DECISION_SCORE means that VALUE is an independently supplied decision "
        "score on the same numerical scale and is not a probability derived from "
        "the evidence. "
        "When MODE=USE, VALUE is authoritative regardless of TYPE. When MODE=IGNORE, "
        "discard VALUE and compute P(A | observations) from the evidence. "
        + scale
    )


def make_surface_variants(config: dict) -> list[dict]:
    rows = []
    for action_id, words in config["action_vocabularies"].items():
        for mapping in config["option_mappings"]:
            for rule_form in config["rule_forms"]:
                for order in config["observation_orders"]:
                    for template_id in config["template_ids"]:
                        rows.append(
                            {
                                "action_vocabulary_id": action_id,
                                "action_words": words,
                                "option_mapping": mapping,
                                "rule_form": rule_form,
                                "observation_order": order,
                                "template_id": template_id,
                            }
                        )
    return rows


def build_families(config: dict) -> list[dict]:
    regimes = config["likelihood_regimes"]
    rows: list[dict] = []
    for block_i, block in enumerate(config["decision_blocks"]):
        threshold = float(block["threshold"])
        for evidence_target in block["evidence_targets"]:
            decompositions = select_decompositions(
                float(evidence_target),
                regimes,
                config["count_pairs"],
                config["decompositions_per_target"],
                config["seed"],
                tuple(config["prior_bounds"]),
            )
            for decomposition_i, evidence in enumerate(decompositions):
                evidence_id = (
                    f"{config['split']}-b{block_i}-z{float(evidence_target):.6f}-"
                    f"d{decomposition_i}-{evidence['likelihood_id']}-"
                    f"r{evidence['n_red']}b{evidence['n_blue']}"
                )
                for pair_i, pair in enumerate(block["external_pairs"]):
                    low, high = float(pair["low"]), float(pair["high"])
                    if not low < threshold < high:
                        raise ValueError((threshold, low, high))
                    family_id = f"{evidence_id}-p{pair_i}-{pair['band']}"
                    rows.append(
                        {
                            **evidence,
                            "split": config["split"],
                            "family_id": family_id,
                            "evidence_id": evidence_id,
                            "decomposition_index": decomposition_i,
                            "threshold": threshold,
                            "threshold_logit": logit(threshold),
                            "evidence_action": action_for(
                                float(evidence_target), threshold
                            ),
                            "external_low": low,
                            "external_high": high,
                            "external_band": pair["band"],
                            "numeral_format": config["numeral_format"],
                        }
                    )
    if len({row["family_id"] for row in rows}) != len(rows):
        raise AssertionError("family_id collision")
    return rows


def make_factorial_rows(config: dict, families: list[dict]) -> list[dict]:
    surfaces = make_surface_variants(config)
    rows: list[dict] = []
    for family in families:
        for surface in surfaces:
            words = surface["action_words"]
            mapping = surface["option_mapping"]
            option_a = words[mapping[0]]
            option_b = words[mapping[1]]
            surface_id = (
                f"{surface['action_vocabulary_id']}-{surface['rule_form']}-"
                f"map{mapping[0]}{mapping[1]}-{surface['observation_order']}-"
                f"{surface['template_id']}"
            )
            for value_side, value in (
                ("low", family["external_low"]),
                ("high", family["external_high"]),
            ):
                value_text = numeral_text(value, family["numeral_format"])
                for condition in PRIMARY_CONDITIONS:
                    use_external = condition.endswith("_use")
                    condition_action = (
                        action_for(value, family["threshold"])
                        if use_external
                        else family["evidence_action"]
                    )
                    prompt = (
                        evidence_text(family, surface["observation_order"])
                        + control_record(value_text, condition, surface["template_id"])
                        + role_instructions(family["numeral_format"])
                        + " A fixed policy is defined as follows: "
                        + rule_text(family["threshold"], words, surface["rule_form"])
                        + f" Option A is {option_a}. Option B is {option_b}."
                        + " Which option does the fixed policy select? Answer only A or B."
                    )
                    expected_label = "A" if mapping[0] == condition_action else "B"
                    variant_id = (
                        f"{family['family_id']}::{surface_id}::{condition}::{value_side}"
                    )
                    rows.append(
                        {
                            **family,
                            "surface_id": surface_id,
                            "action_vocabulary_id": surface["action_vocabulary_id"],
                            "action_words": words,
                            "option_mapping": mapping,
                            "rule_form": surface["rule_form"],
                            "observation_order": surface["observation_order"],
                            "template_id": surface["template_id"],
                            "condition": condition,
                            "value_type": (
                                "posterior"
                                if condition.startswith("posterior")
                                else "generic_decision_score"
                            ),
                            "mode": "use" if use_external else "ignore",
                            "value_side": value_side,
                            "serialized_value": value,
                            "serialized_text": value_text,
                            "condition_action": condition_action,
                            "expected_label": expected_label,
                            "variant_id": variant_id,
                            "prompt": prompt,
                            "prompt_sha256": sha256_bytes(prompt.encode()),
                        }
                    )
    return rows


def unique_evidence_rows(config: dict, families: list[dict]) -> list[dict]:
    rows = {}
    for family in families:
        for order in config["observation_orders"]:
            key = f"{family['evidence_id']}::{order}"
            rows[key] = {
                "split": family["split"],
                "evidence_surface_id": key,
                "evidence_id": family["evidence_id"],
                "family_ids": [],
                "observation_order": order,
                "likelihood_id": family["likelihood_id"],
                "prior_a": family["prior_a"],
                "p_red_a": family["p_red_a"],
                "p_red_b": family["p_red_b"],
                "n_red": family["n_red"],
                "n_blue": family["n_blue"],
                "gold_p_a": family["gold_p_a"],
                "posterior_prompt": posterior_prompt(family, order),
            }
    family_map: dict[str, set[str]] = defaultdict(set)
    for family in families:
        for order in config["observation_orders"]:
            family_map[f"{family['evidence_id']}::{order}"].add(family["family_id"])
    for key, row in rows.items():
        row["family_ids"] = sorted(family_map[key])
        row["prompt_sha256"] = sha256_bytes(row["posterior_prompt"].encode())
    return sorted(rows.values(), key=lambda row: row["evidence_surface_id"])


def validate_factorial(rows: list[dict]) -> dict:
    if len({row["variant_id"] for row in rows}) != len(rows):
        raise AssertionError("variant_id collision")
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        groups[(row["family_id"], row["surface_id"])].append(row)
        if not row["external_low"] < row["threshold"] < row["external_high"]:
            raise AssertionError(row["family_id"])
        if row["condition"].endswith("_use"):
            expected = action_for(row["serialized_value"], row["threshold"])
        else:
            expected = row["evidence_action"]
        if row["condition_action"] != expected:
            raise AssertionError(row["variant_id"])
    expected_cells = {
        (condition, side)
        for condition in PRIMARY_CONDITIONS
        for side in ("low", "high")
    }
    for key, group in groups.items():
        cells = {(row["condition"], row["value_side"]) for row in group}
        if cells != expected_cells or len(group) != 8:
            raise AssertionError((key, cells))
    return {
        "n_rows": len(rows),
        "n_family_surface_groups": len(groups),
        "n_families": len({row["family_id"] for row in rows}),
        "n_surfaces": len({row["surface_id"] for row in rows}),
        "conditions": list(PRIMARY_CONDITIONS),
    }


def chat_prefix(tokenizer, prompt: str) -> str:
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            enable_thinking=False,
            **kwargs,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], **kwargs
        )


def token_span(tokenizer, text: str, substring: str) -> tuple[int, int]:
    start = text.index(substring)
    before = tokenizer(text[:start], add_special_tokens=False).input_ids
    through = tokenizer(
        text[: start + len(substring)], add_special_tokens=False
    ).input_ids
    return len(before), len(through)


def audit_tokens(rows: list[dict], model: str, model_revision: str) -> dict:
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model,
        revision=model_revision,
        local_files_only=True,
        trust_remote_code=True,
    )
    audits = []
    fertility_by_group: dict[tuple[str, str, str], set[int]] = defaultdict(set)
    role_token_lengths: dict[str, set[int]] = defaultdict(set)
    for row in rows:
        raw_start, raw_end = token_span(tokenizer, row["prompt"], row["serialized_text"])
        rendered = chat_prefix(tokenizer, row["prompt"])
        chat_start, chat_end = token_span(tokenizer, rendered, row["serialized_text"])
        fertility = raw_end - raw_start
        chat_fertility = chat_end - chat_start
        if fertility != chat_fertility:
            raise AssertionError((row["variant_id"], fertility, chat_fertility))
        group = (row["family_id"], row["surface_id"], row["condition"])
        fertility_by_group[group].add(fertility)
        type_marker = "POSTERIOR" if row["value_type"] == "posterior" else "DECISION_SCORE"
        mode_marker = "USE" if row["mode"] == "use" else "IGNORE"
        role_token_lengths[type_marker].add(
            len(tokenizer(type_marker, add_special_tokens=False).input_ids)
        )
        role_token_lengths[mode_marker].add(
            len(tokenizer(mode_marker, add_special_tokens=False).input_ids)
        )
        audits.append(
            {
                "variant_id": row["variant_id"],
                "serialized_text": row["serialized_text"],
                "value_token_count": fertility,
                "raw_value_token_span": [raw_start, raw_end],
                "chat_value_token_span": [chat_start, chat_end],
            }
        )
    mismatched = {str(k): sorted(v) for k, v in fertility_by_group.items() if len(v) != 1}
    if mismatched:
        raise AssertionError(f"low/high token fertility mismatch: {mismatched}")
    posterior_len = next(iter(role_token_lengths["POSTERIOR"]))
    score_len = next(iter(role_token_lengths["DECISION_SCORE"]))
    use_len = next(iter(role_token_lengths["USE"]))
    ignore_len = next(iter(role_token_lengths["IGNORE"]))
    if posterior_len != score_len or use_len != ignore_len:
        raise AssertionError(
            {
                "POSTERIOR": posterior_len,
                "DECISION_SCORE": score_len,
                "USE": use_len,
                "IGNORE": ignore_len,
            }
        )
    counts = sorted({row["value_token_count"] for row in audits})
    return {
        "model": model,
        "model_revision": model_revision,
        "tokenizer_class": type(tokenizer).__name__,
        "n_prompts": len(audits),
        "value_token_counts": counts,
        "role_marker_token_counts": {
            key: sorted(values) for key, values in role_token_lengths.items()
        },
        "within_family_low_high_fertility_matched": True,
        "records_sha256": sha256_bytes(
            json.dumps(audits, sort_keys=True).encode()
        ),
    }


def current_git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()


def generate(config_path: Path, out_dir: Path, code_commit: str | None) -> dict:
    config, source_config = load_config(config_path)
    families = build_families(config)
    rows = make_factorial_rows(config, families)
    evidence = unique_evidence_rows(config, families)
    validation = validate_factorial(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "families": out_dir / "families.jsonl",
        "factorial": out_dir / "factorial.jsonl.gz",
        "evidence": out_dir / "evidence.jsonl",
    }
    dump_jsonl(families, paths["families"])
    dump_jsonl(rows, paths["factorial"])
    dump_jsonl(evidence, paths["evidence"])
    audit = audit_tokens(rows, config["model"], config["model_revision"])
    audit_path = out_dir / "TOKEN_AUDIT.json"
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    schema = {
        "version": 1,
        "independent_unit": "family_id",
        "repeated_units": ["surface_id", "condition", "value_side"],
        "primary_conditions": list(PRIMARY_CONDITIONS),
        "primary_estimands": [
            "G_posterior",
            "G_generic_control",
            "G_specific",
        ],
        "family_first_aggregation": True,
        "semantic_logit": "teacher-forced ACT-minus-WAIT in A/B coordinates",
        "inference_good": config["inference_good"],
    }
    schema_path = out_dir / "REPORT_SCHEMA.json"
    schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    checksums = {
        name: sha256_file(path)
        for name, path in {**paths, "token_audit": audit_path, "schema": schema_path}.items()
    }
    metadata = {
        "freeze_version": "v2-m12-1",
        "split": config["split"],
        "evidence_class": config["evidence_class"],
        "config_path": str(config_path),
        "config_sha256": sha256_file(config_path),
        "resolved_config_sha256": sha256_bytes(
            json.dumps(config, sort_keys=True).encode()
        ),
        "base_config": config.get("base_config"),
        "changed_factor": config.get("changed_factor"),
        "code_commit": code_commit or current_git_commit(),
        "model": config["model"],
        "model_revision": config["model_revision"],
        "seed": config["seed"],
        "validation": validation,
        "token_audit": audit,
        "output_sha256": checksums,
        "d2_opened": False if config["split"].startswith("d2") else None,
    }
    metadata_path = out_dir / "FREEZE.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--code-commit")
    args = parser.parse_args()
    print(
        json.dumps(
            generate(args.config, args.out_dir, args.code_commit),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
