#!/usr/bin/env python3
"""G0 analysis. Implements PREREGISTRATION.md sections 9-11.

Event-grouped bootstrap. No threshold is computed from the data.
Writes results/summary.csv, results/analysis.json, results/<fam>/scored_<cond>.jsonl.
"""
from __future__ import annotations

import csv, json, math, random, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260831
NBOOT = 10000

# mistral: infrastructure hang on this host (see g0_report.md); phi is the
# documented repo-standard substitute, chosen before any result was inspected.
# mistral hung on this host before dispatching any batch; phi is the documented
# substitute fourth family (see results/mistral_infrastructure_failure.md).
FAMILIES = ["qwen", "gemma", "llama", "phi"]
ROLE_CONDS = ["role", "role_paraphrase", "role_findingonly", "role_narrativeonly"]

# S0 thresholds — frozen in PREREGISTRATION.md sec. 9, never recomputed here.
TH_REL, TH_ROLE, TH_GAP, N_FAMILIES_REQUIRED = 0.75, 0.62, 0.15, 2


def load_jsonl(p: Path):
    """Reads .jsonl, or the .gz beside it (raw panel outputs are stored gzipped)."""
    if not p.exists() and p.with_suffix(p.suffix + ".gz").exists():
        import gzip
        text = gzip.decompress(p.with_suffix(p.suffix + ".gz").read_bytes()).decode("utf-8")
    else:
        text = p.read_text(encoding="utf-8")
    return [json.loads(l) for l in text.splitlines() if l.strip()]


# ---------------------------------------------------------------- parsing ---
def parse_relevance(raw: str) -> str | None:
    t = raw.strip().upper()
    t = re.sub(r"^[^A-Z]*", "", t)
    if t.startswith("YES"):
        return "YES"
    if t.startswith("NO"):
        return "NO"
    has_y, has_n = re.search(r"\bYES\b", t), re.search(r"\bNO\b", t)
    if has_y and not has_n:
        return "YES"
    if has_n and not has_y:
        return "NO"
    return None


def parse_role(raw: str) -> str | None:
    t = raw.strip().upper().replace("*", "")
    t = re.sub(r"^[^A-Z]*", "", t)
    # CONTRIBUTING must be tested first: "CONTRIBUTING_FACTOR" contains no "CAUSE",
    # but a leading "CAUSE" check on "CAUSE OR CONTRIBUTING" would misfire.
    if t.startswith("CONTRIBUTING"):
        return "CONTRIBUTING_FACTOR"
    if t.startswith("CAUSE"):
        return "CAUSE"
    has_c, has_f = re.search(r"\bCAUSE\b", t), re.search(r"CONTRIBUTING", t)
    if has_f and not has_c:
        return "CONTRIBUTING_FACTOR"
    if has_c and not has_f:
        return "CAUSE"
    return None


# --------------------------------------------------------------- metrics ---
def balanced_accuracy(pairs, labels):
    """pairs: list of (gold, pred). Unparsed preds count as wrong."""
    per = {l: [0, 0] for l in labels}
    for g, p in pairs:
        per[g][1] += 1
        per[g][0] += int(p == g)
    recalls = [v[0] / v[1] for v in per.values() if v[1]]
    return (sum(recalls) / len(recalls)) if recalls else float("nan"), per


def macro_f1(pairs, labels):
    f1s = []
    for l in labels:
        tp = sum(1 for g, p in pairs if g == l and p == l)
        fp = sum(1 for g, p in pairs if g != l and p == l)
        fn = sum(1 for g, p in pairs if g == l and p != l)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    return sum(f1s) / len(f1s)


def boot_ci(stat_fn, ev_ids, rng, nboot=NBOOT):
    """Event-grouped bootstrap: resample events with replacement."""
    ev_ids = list(ev_ids)
    n = len(ev_ids)
    vals = []
    for _ in range(nboot):
        draw = [ev_ids[int(rng.random() * n)] for _ in range(n)]
        v = stat_fn(draw)
        if v is not None and not math.isnan(v):
            vals.append(v)
    if not vals:
        return None, None
    vals.sort()
    return round(vals[int(0.025 * len(vals))], 4), round(vals[min(int(0.975 * len(vals)), len(vals) - 1)], 4)


def main() -> None:
    events = {e["ev_id"]: e for e in load_jsonl(ROOT / "items" / "g0_events.jsonl")}
    role_items = {i["item_id"]: i for i in load_jsonl(ROOT / "items" / "g0_roles.jsonl")}
    rng = random.Random(SEED)

    out: dict = {"thresholds": {"relevance_BA_min": TH_REL, "role_BA_max": TH_ROLE,
                                "gap_min": TH_GAP, "families_required": N_FAMILIES_REQUIRED},
                 "families": {}}
    rows = []

    for fam in FAMILIES:
        fdir = ROOT / "results" / fam
        if not ((fdir / "raw_relevance.jsonl").exists()
                or (fdir / "raw_relevance.jsonl.gz").exists()):
            continue
        fam_out: dict = {"manifest": json.loads((fdir / "manifest.json").read_text())}

        # ---------------- Task A ------------------------------------------
        rel = load_jsonl(fdir / "raw_relevance.jsonl")
        rel_scored = []
        for r in rel:
            p = parse_relevance(r["raw"])
            r.pop("first_token_logprobs", None)
            rel_scored.append({**r, "pred": p, "correct": p == r["gold"]})
        (fdir / "scored_relevance.jsonl").write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in rel_scored), encoding="utf-8")

        by_ev_rel = defaultdict(list)
        for r in rel_scored:
            by_ev_rel[r["ev_id"]].append((r["gold"], r["pred"]))
        rel_pairs = [(r["gold"], r["pred"]) for r in rel_scored]
        rel_ba, rel_per = balanced_accuracy(rel_pairs, ["YES", "NO"])

        def rel_stat(draw):
            pr = [x for e in draw for x in by_ev_rel[e]]
            v, _ = balanced_accuracy(pr, ["YES", "NO"])
            return v

        rel_ci = boot_ci(rel_stat, list(by_ev_rel), random.Random(SEED))
        fam_out["task_A_relevance"] = {
            "n_items": len(rel_scored), "n_events": len(by_ev_rel),
            "gold_counts": dict(Counter(r["gold"] for r in rel_scored)),
            "balanced_accuracy": round(rel_ba, 4), "ci95": rel_ci,
            "macro_f1": round(macro_f1(rel_pairs, ["YES", "NO"]), 4),
            "recall_per_class": {k: {"correct": v[0], "n": v[1], "recall": round(v[0] / v[1], 4)}
                                 for k, v in rel_per.items() if v[1]},
            "unparsed": sum(1 for r in rel_scored if r["pred"] is None),
            "accuracy_raw": round(sum(r["correct"] for r in rel_scored) / len(rel_scored), 4),
        }

        # ---------------- Task B + controls -------------------------------
        for cond in ROLE_CONDS:
            p = fdir / f"raw_{cond}.jsonl"
            if not (p.exists() or p.with_suffix(".jsonl.gz").exists()):
                continue
            rr = load_jsonl(p)
            sc = []
            for r in rr:
                pr = parse_role(r["raw"])
                r.pop("first_token_logprobs", None)
                sc.append({**r, "pred": pr, "correct": pr == r["gold"]})
            (fdir / f"scored_{cond}.jsonl").write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in sc), encoding="utf-8")

            by_ev = defaultdict(list)
            for r in sc:
                by_ev[r["ev_id"]].append((r["gold"], r["pred"]))
            pairs = [(r["gold"], r["pred"]) for r in sc]
            ba, per = balanced_accuracy(pairs, ["CAUSE", "CONTRIBUTING_FACTOR"])

            def stat(draw, by_ev=by_ev):
                pr = [x for e in draw for x in by_ev[e]]
                v, _ = balanced_accuracy(pr, ["CAUSE", "CONTRIBUTING_FACTOR"])
                return v

            entry = {
                "n_items": len(sc), "n_events": len(by_ev),
                "balanced_accuracy": round(ba, 4),
                "ci95": boot_ci(stat, list(by_ev), random.Random(SEED)),
                "macro_f1": round(macro_f1(pairs, ["CAUSE", "CONTRIBUTING_FACTOR"]), 4),
                "recall_per_class": {k: {"correct": v[0], "n": v[1], "recall": round(v[0] / v[1], 4)}
                                     for k, v in per.items() if v[1]},
                "confusion": dict(Counter(f"{g}->{p or 'UNPARSED'}" for g, p in pairs)),
                "unparsed": sum(1 for r in sc if r["pred"] is None),
                "pred_distribution": dict(Counter(r["pred"] or "UNPARSED" for r in sc)),
            }
            if cond == "role":
                # sensitivity: drop the "Contributed to outcome" modifier (Control 4)
                keep = [(r["gold"], r["pred"]) for r in sc
                        if not role_items[r["item_id"]]["contributed_to_outcome_modifier"]]
                kba, _ = balanced_accuracy(keep, ["CAUSE", "CONTRIBUTING_FACTOR"])
                entry["ba_excluding_contributed_to_outcome_modifier"] = round(kba, 4)
                entry["n_excluded_modifier_items"] = len(sc) - len(keep)
                # by year (Control 6)
                yr = defaultdict(list)
                for r in sc:
                    yr[events[r["ev_id"]]["ev_year"]].append((r["gold"], r["pred"]))
                entry["ba_by_year"] = {
                    y: {"n": len(v), "ba": round(balanced_accuracy(v, ["CAUSE", "CONTRIBUTING_FACTOR"])[0], 4)}
                    for y, v in sorted(yr.items())}
                # --- Addendum 1 sec. 3.2: does role accuracy ride the in-envelope
                # finding-text length cue (length alone = 0.668 BA)? ---
                lens = sorted(len(role_items[r["item_id"]]["finding"]) for r in sc)
                q1, q2 = lens[len(lens) // 3], lens[2 * len(lens) // 3]
                terc = defaultdict(list)
                for r in sc:
                    L = len(role_items[r["item_id"]]["finding"])
                    terc["short" if L <= q1 else "mid" if L <= q2 else "long"].append(
                        (r["gold"], r["pred"]))
                entry["ba_by_finding_text_length_tercile"] = {
                    k: {"n": len(v), "chars": f"<= {q1}" if k == "short" else
                        f"{q1 + 1}-{q2}" if k == "mid" else f"> {q2}",
                        "ba": round(balanced_accuracy(v, ["CAUSE", "CONTRIBUTING_FACTOR"])[0], 4),
                        "frac_pred_CAUSE": round(
                            sum(1 for _, p in v if p == "CAUSE") / len(v), 4)}
                    for k, v in terc.items()}
                # --- Addendum 1 sec. 3.3: finding_no is NOT in the evidence
                # envelope; any monotone trend means the model recovered the
                # coder ordering convention from semantics alone. ---
                pos = defaultdict(list)
                for r in sc:
                    n = int(r["item_id"].rsplit(":", 1)[1])
                    pos[min(n, 8)].append((r["gold"], r["pred"]))
                entry["ba_by_finding_no"] = {
                    str(k) + ("+" if k == 8 else ""): {
                        "n": len(v),
                        "gold_frac_CAUSE": round(
                            sum(1 for g, _ in v if g == "CAUSE") / len(v), 4),
                        "pred_frac_CAUSE": round(
                            sum(1 for _, p in v if p == "CAUSE") / len(v), 4),
                        "ba": round(balanced_accuracy(v, ["CAUSE", "CONTRIBUTING_FACTOR"])[0], 4)}
                    for k, v in sorted(pos.items())}
            fam_out[cond] = entry

        # ---------------- gap + within-event dissociation ------------------
        if "role" in fam_out:
            role_ba = fam_out["role"]["balanced_accuracy"]
            gap = round(rel_ba - role_ba, 4)
            by_ev_role = defaultdict(list)
            for r in load_jsonl(fdir / "scored_role.jsonl"):
                by_ev_role[r["ev_id"]].append((r["gold"], r["pred"]))

            def gap_stat(draw):
                a, _ = balanced_accuracy([x for e in draw for x in by_ev_rel[e]], ["YES", "NO"])
                b, _ = balanced_accuracy([x for e in draw for x in by_ev_role[e]],
                                         ["CAUSE", "CONTRIBUTING_FACTOR"])
                return a - b if not (math.isnan(a) or math.isnan(b)) else float("nan")

            gap_ci = boot_ci(gap_stat, list(by_ev_rel), random.Random(SEED))

            # per-event: relevance all-correct AND role wrong somewhere
            rel_ok, role_ok = {}, {}
            for e, v in by_ev_rel.items():
                rel_ok[e] = all(g == p for g, p in v)
            for e, v in by_ev_role.items():
                role_ok[e] = all(g == p for g, p in v)
            common = set(rel_ok) & set(role_ok)
            cell = Counter((rel_ok[e], role_ok[e]) for e in common)
            fam_out["dissociation"] = {
                "relevance_BA_minus_role_BA": gap,
                "gap_ci95_event_bootstrap": gap_ci,
                "n_events_compared": len(common),
                "relevance_all_correct_and_role_wrong": cell[(True, False)],
                "relevance_all_correct_and_role_all_correct": cell[(True, True)],
                "relevance_wrong_and_role_wrong": cell[(False, False)],
                "relevance_wrong_and_role_all_correct": cell[(False, True)],
                "fraction_relevance_correct_role_wrong": round(cell[(True, False)] / max(len(common), 1), 4),
            }
            para = fam_out.get("role_paraphrase", {}).get("balanced_accuracy")
            fo = fam_out.get("role_findingonly", {}).get("balanced_accuracy")
            fam_out["s0_criterion"] = {
                "relevance_BA>=0.75": rel_ba >= TH_REL,
                "role_BA<=0.62": role_ba <= TH_ROLE,
                "gap>=0.15": gap >= TH_GAP,
                "gap_ci_excludes_0": bool(gap_ci[0] is not None and gap_ci[0] > 0),
                "paraphrase_role_BA<=0.62": (para is not None and para <= TH_ROLE),
                "all": all([rel_ba >= TH_REL, role_ba <= TH_ROLE, gap >= TH_GAP,
                            gap_ci[0] is not None and gap_ci[0] > 0,
                            para is not None and para <= TH_ROLE]),
            }
            fam_out["control_lexical_artifact"] = {
                "finding_only_BA": fo, "full_context_BA": role_ba,
                "kill_triggered": bool(fo is not None and fo >= role_ba - 0.02 and fo >= TH_ROLE),
            }
            rows.append({
                "family": fam, "model_id": fam_out["manifest"]["model_id"],
                "n_events": fam_out["task_A_relevance"]["n_events"],
                "n_relevance_items": fam_out["task_A_relevance"]["n_items"],
                "n_role_items": fam_out["role"]["n_items"],
                "taskA_relevance_BA": rel_ba, "taskA_ci_low": rel_ci[0], "taskA_ci_high": rel_ci[1],
                "taskB_role_BA": role_ba,
                "taskB_ci_low": fam_out["role"]["ci95"][0], "taskB_ci_high": fam_out["role"]["ci95"][1],
                "gap": gap, "gap_ci_low": gap_ci[0], "gap_ci_high": gap_ci[1],
                "taskB_paraphrase_BA": para,
                "taskB_findingonly_BA": fo,
                "taskB_narrativeonly_BA": fam_out.get("role_narrativeonly", {}).get("balanced_accuracy"),
                "taskA_unparsed": fam_out["task_A_relevance"]["unparsed"],
                "taskB_unparsed": fam_out["role"]["unparsed"],
                "s0_all": fam_out["s0_criterion"]["all"],
            })
        out["families"][fam] = fam_out

    # ---------------- baselines (Control 1) --------------------------------
    golds = [i["gold"] for i in role_items.values()]
    cnt = Counter(golds)
    maj = max(cnt, key=cnt.get)
    out["control1_label_prior"] = {
        "role_gold_counts": dict(cnt),
        "majority_class": maj,
        "majority_class_accuracy": round(cnt[maj] / len(golds), 4),
        "majority_class_balanced_accuracy": 0.5,
        "stratified_random_balanced_accuracy": 0.5,
    }
    mp = ROOT / "audit" / "metadata_leak_audit.json"
    if mp.exists():
        md = json.loads(mp.read_text())
        out["control0_metadata_stupid_baselines"] = {
            "source": "audit/metadata_leak_audit.json (PREREGISTRATION_ADDENDUM_1.md)",
            "grouped_cv_balanced_accuracy": md["balanced_accuracy"],
            "reading": (
                "Task-B balanced accuracy must be read against META=0.697 and "
                "META+LEN=0.797, not against 0.5. Finding-text length alone reaches "
                "0.668 and IS inside the model's evidence envelope; finding position "
                "reaches 0.693 and is NOT (each item shows one isolated finding), so "
                "part of the C/F gold is coder ordering convention no model can "
                "recover from the evidence given."),
            "evidence_envelope_check": md["evidence_envelope_check"],
        }
    out["scope_note"] = (
        "C is not a unique 'principal cause'. NTSB determines one or more probable "
        "causes; multiple C findings per event are normal. The object is "
        "cause vs contributing factor, never root-cause analysis.")
    out["data_side_lexical_ceiling_note"] = (
        "A leave-one-out finding-text lookup table built from corpus annotation "
        "statistics (unavailable to the models) reaches C/F balanced accuracy 0.758 "
        "inside mixed-role events. See PREREGISTRATION.md sec. 12.")

    n_pass = sum(1 for r in rows if r["s0_all"])
    out["verdict"] = {
        "families_run": len(rows),
        "families_meeting_full_criterion": n_pass,
        "required": N_FAMILIES_REQUIRED,
        "s0_pass": n_pass >= N_FAMILIES_REQUIRED,
    }

    (ROOT / "results" / "analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    if rows:
        with (ROOT / "results" / "summary.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print(json.dumps({"verdict": out["verdict"], "control1": out["control1_label_prior"],
                      "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
