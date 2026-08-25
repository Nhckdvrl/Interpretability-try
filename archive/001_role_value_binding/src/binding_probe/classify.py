from __future__ import annotations

import argparse
import ast
import json
import math
import re
from collections import Counter
from itertools import combinations
from typing import Any

from .bfcl import index_by_id, load_jsonl, one_function, user_text, write_jsonl

_TOOL_BLOCK = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.DOTALL)
_CODE_FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


def _norm(v: Any) -> Any:
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = " ".join(v.strip().lower().split())
        try:
            return float(s)
        except ValueError:
            return s
    if isinstance(v, list):
        return tuple(_norm(x) for x in v)
    if isinstance(v, dict):
        return tuple(sorted((str(k), _norm(val)) for k, val in v.items()))
    return str(v)


def value_matches(pred: Any, allowed: list[Any]) -> bool:
    p = _norm(pred)
    for x in allowed:
        if x == "":
            continue
        q = _norm(x)
        if isinstance(p, float) and isinstance(q, float):
            if math.isclose(p, q, rel_tol=1e-6, abs_tol=1e-8):
                return True
        elif p == q:
            return True
    return False


def _ast_func_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _ast_func_name(node.value)
        return f"{parent}.{node.attr}" if parent else None
    return None


def _parse_pythonish_call(raw: str) -> dict[str, Any] | None:
    """Parse BFCL prompt-mode outputs like `[math.gcd(num1=40, num2=50)]`.

    Only literal keyword arguments are accepted. No code is executed.
    """
    try:
        tree = ast.parse(raw.strip(), mode="eval").body
    except SyntaxError:
        return None
    if isinstance(tree, (ast.List, ast.Tuple)) and len(tree.elts) == 1:
        tree = tree.elts[0]
    if not isinstance(tree, ast.Call) or tree.args:
        return None
    name = _ast_func_name(tree.func)
    if name is None:
        return None
    args: dict[str, Any] = {}
    for kw in tree.keywords:
        if kw.arg is None:
            return None
        try:
            args[kw.arg] = ast.literal_eval(kw.value)
        except (ValueError, TypeError):
            return None
    return {"name": name, "arguments": args}


def parse_tool_call(raw: str) -> dict[str, Any] | None:
    candidates = _TOOL_BLOCK.findall(raw) or _CODE_FENCE.findall(raw)
    if not candidates:
        stripped = raw.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            candidates = [stripped]
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "name" in obj:
            args = obj.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    return None
            if isinstance(args, dict):
                return {"name": obj["name"], "arguments": args}
    return _parse_pythonish_call(raw)


def _literal_pattern(value: Any) -> re.Pattern[str] | None:
    if value == "" or isinstance(value, (list, dict, bool)) or value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    escaped = re.escape(s)
    # Do not let short literals match inside larger tokens (US in Australia, 1 in 10).
    # For numeric literals, dot is also protected so 1 does not match inside 1.5.
    is_numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
    boundary = r"[\w.]" if is_numeric else r"\w"
    left = rf"(?<!{boundary})" if (s[0].isalnum() or s[0] in "+-") else ""
    right = rf"(?!{boundary})" if s[-1].isalnum() else ""
    return re.compile(left + escaped + right, re.IGNORECASE)


def literal_occurrences(value: Any, text: str) -> int:
    pat = _literal_pattern(value)
    return len(pat.findall(text)) if pat is not None else 0


def _canonical_literal(allowed: list[Any], text: str) -> Any | None:
    # Prefer a non-empty scalar accepted value that occurs as a standalone literal in the query.
    for v in allowed:
        if literal_occurrences(v, text) > 0:
            return v
    return None


def binding_eligible_pairs(test: dict[str, Any], answer: dict[str, Any]) -> list[dict[str, Any]]:
    """Return strict direct-copy, same-type, required-slot pairs.

    A pair is eligible only if both required values have a scalar accepted value that occurs
    explicitly in the user text, both schema types match, and the values differ. This deliberately
    excludes inferred/default/derived values because they would confound extraction with binding.
    """
    fn = one_function(test)
    gt = answer["ground_truth"][0].get(fn["name"])
    if not isinstance(gt, dict):
        return []
    required = fn.get("parameters", {}).get("required", [])
    props = fn.get("parameters", {}).get("properties", {})
    text = user_text(test)
    items: list[tuple[str, str | None, Any]] = []
    for key in required:
        if key not in gt:
            continue
        literal = _canonical_literal(gt[key], text)
        if literal is None:
            continue
        typ = props.get(key, {}).get("type")
        items.append((key, typ, literal))
    out = []
    for (ka, ta, va), (kb, tb, vb) in combinations(items, 2):
        if ta != tb or _norm(va) == _norm(vb):
            continue
        out.append({"key_a": ka, "key_b": kb, "type": ta, "value_a": va, "value_b": vb})
    return out


def _perfect_reassignment(pred_args: dict[str, Any], gt: dict[str, list[Any]], required: list[str]) -> dict[str, str] | None:
    """Check whether required predicted values are a one-to-one permutation of GT role values."""
    candidates: dict[str, list[str]] = {}
    wrong = 0
    for pkey in required:
        if pkey not in pred_args:
            return None
        is_self = value_matches(pred_args[pkey], gt.get(pkey, []))
        if not is_self:
            wrong += 1
        cands = [gkey for gkey in required if value_matches(pred_args[pkey], gt.get(gkey, []))]
        if not cands:
            return None
        if not is_self and pkey in cands:
            cands.remove(pkey)
        candidates[pkey] = cands
    if wrong < 2:
        return None

    order = sorted(required, key=lambda k: len(candidates[k]))
    used: set[str] = set()
    assignment: dict[str, str] = {}

    def dfs(i: int) -> bool:
        if i == len(order):
            return True
        pkey = order[i]
        for gkey in candidates[pkey]:
            if gkey in used:
                continue
            used.add(gkey)
            assignment[pkey] = gkey
            if dfs(i + 1):
                return True
            used.remove(gkey)
            assignment.pop(pkey, None)
        return False

    return assignment.copy() if dfs(0) else None


def _strict_natural_binding(
    test: dict[str, Any], answer: dict[str, Any], pred_args: dict[str, Any], reassignment: dict[str, str] | None
) -> bool:
    """Whether a permutation is inside the predeclared direct-copy/same-type binding test.

    This prevents us from retroactively calling an arbitrary parameter error a binding error.
    Every wrong predicted role must be mapped to a *different* role that belongs to the set of
    strict eligible role pairs derived before looking at model output.
    """
    if reassignment is None:
        return False
    eligible = binding_eligible_pairs(test, answer)
    allowed_edges = {
        frozenset((p["key_a"], p["key_b"]))
        for p in eligible
    }
    fn = one_function(test)
    gt = answer["ground_truth"][0].get(fn["name"], {})
    wrong_roles = [k for k in fn.get("parameters", {}).get("required", []) if not value_matches(pred_args[k], gt.get(k, []))]
    if len(wrong_roles) < 2:
        return False
    for role in wrong_roles:
        source_role = reassignment.get(role)
        if source_role is None or source_role == role:
            return False
        if frozenset((role, source_role)) not in allowed_edges:
            return False
    return True


def diagnose(test: dict[str, Any], answer: dict[str, Any], raw_output: str) -> dict[str, Any]:
    fn = one_function(test)
    fn_name = fn["name"]
    gt = answer["ground_truth"][0].get(fn_name, {})
    required = list(fn.get("parameters", {}).get("required", []))
    schema_keys = set(fn.get("parameters", {}).get("properties", {}).keys())
    eligible_pairs = binding_eligible_pairs(test, answer)
    call = parse_tool_call(raw_output)
    base = {"id": test["id"], "function": fn_name, "eligible_pairs": eligible_pairs, "strict_natural_binding": False}
    if call is None:
        return {**base, "label": "parse_failure"}
    if call["name"] != fn_name:
        return {**base, "label": "wrong_tool", "predicted_tool": call["name"], "predicted_args": call["arguments"]}
    args = call["arguments"]
    unknown = set(args) - schema_keys
    missing = set(required) - set(args)
    if unknown or missing:
        return {**base, "label": "schema_key_error", "unknown_keys": sorted(unknown), "missing_required": sorted(missing), "predicted_args": args}

    required_correct = all(value_matches(args[k], gt.get(k, [])) for k in required)
    optional_present = set(args) - set(required)
    optional_correct = all(value_matches(args[k], gt.get(k, [])) for k in optional_present if k in gt)
    if required_correct and optional_correct:
        return {**base, "label": "correct", "predicted_args": args}

    # Do not call something a pure binding error if an optional field is independently wrong.
    if not optional_correct:
        return {**base, "label": "mixed_value_error", "predicted_args": args}

    reassignment = _perfect_reassignment(args, gt, required)
    if reassignment is not None:
        strict = _strict_natural_binding(test, answer, args, reassignment)
        return {
            **base,
            "label": "pure_binding_permutation",
            "strict_natural_binding": strict,
            "predicted_args": args,
            "reassignment": reassignment,
        }
    return {**base, "label": "value_error", "predicted_args": args}


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--outputs", required=True, help="JSONL rows with id and raw_output")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    tests = index_by_id(load_jsonl(args.data))
    answers = index_by_id(load_jsonl(args.answers))
    outputs = load_jsonl(args.outputs)
    rows = [diagnose(tests[o["id"]], answers[o["id"]], o["raw_output"]) for o in outputs if o["id"] in tests and o["id"] in answers]
    write_jsonl(rows, args.out)
    counts = Counter(r["label"] for r in rows)
    eligible = sum(bool(r["eligible_pairs"]) for r in rows)
    strict = sum(bool(r.get("strict_natural_binding")) for r in rows)
    lo, hi = wilson_interval(strict, eligible)
    by_function = Counter(r["function"] for r in rows if r.get("strict_natural_binding"))
    print(json.dumps({
        "n": len(rows),
        "eligible": eligible,
        "counts": counts,
        "strict_natural_binding_errors": strict,
        "strict_binding_error_rate": strict / eligible if eligible else 0.0,
        "wilson95": [lo, hi],
        "strict_errors_by_function": by_function,
    }, indent=2, default=dict))


if __name__ == "__main__":
    main()
