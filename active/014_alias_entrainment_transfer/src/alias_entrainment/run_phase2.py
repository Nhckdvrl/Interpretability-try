"""Phase 2 for 014: are entrainment heads carrying the alias-transfer component?

Two stages, deliberately separated so head selection cannot contaminate the test:

  sweep   ablate every attention head individually on a DISCOVERY half of the
          items and rank heads by how much they reduce the exact-reappearance
          effect. Heads are defined purely by the mother's phenomenon
          (`EXACT`), with no reference to aliases.
  ablate  zero the top-k heads jointly and re-measure all four conditions on the
          held-out EVALUATION half, against layer-matched random-head controls.

Head ablation = zeroing that head's slice of the input to o_proj, i.e. removing
its write to the residual stream while leaving every other head untouched.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import torch

from run_phase1 import CONDITIONS, Scorer, build_prompt, mention_for

SEED = 20260829


def find_layers(model):
    """Return the list of decoder layers across Llama / Qwen / Gemma wrappers."""
    for path in ("model.layers", "model.language_model.layers",
                 "language_model.model.layers", "model.model.layers"):
        obj = model
        try:
            for part in path.split("."):
                obj = getattr(obj, part)
            if hasattr(obj[0], "self_attn"):
                return obj
        except AttributeError:
            continue
    raise RuntimeError("could not locate decoder layers")


class HeadAblator:
    """Zeroes chosen (layer, head) writes by masking o_proj's input slices."""

    def __init__(self, model):
        self.layers = find_layers(model)
        cfg = model.config
        cfg = getattr(cfg, "text_config", cfg)
        self.n_layers = len(self.layers)
        self.n_heads = cfg.num_attention_heads
        o_in = self.layers[0].self_attn.o_proj.in_features
        self.head_dim = o_in // self.n_heads
        assert o_in == self.n_heads * self.head_dim, (o_in, self.n_heads)
        self.handles = []

    def set(self, heads: list[tuple[int, int]]):
        self.clear()
        by_layer: dict[int, list[int]] = {}
        for layer, head in heads:
            by_layer.setdefault(layer, []).append(head)
        for layer, hs in by_layer.items():
            idx = torch.tensor(
                [i for h in hs for i in range(h * self.head_dim, (h + 1) * self.head_dim)])

            def pre_hook(module, args, idx=idx):
                x = args[0].clone()
                x[..., idx.to(x.device)] = 0
                return (x,) + args[1:]

            self.handles.append(
                self.layers[layer].self_attn.o_proj.register_forward_pre_hook(pre_hook))

    def clear(self):
        for h in self.handles:
            h.remove()
        self.handles = []


def split_items(items, passed, seed=SEED):
    """Discovery / evaluation halves, split by ENTITY so no entity spans both.

    Discovery uses only `opaque_strict` items (head ranking should be driven by
    the same clean cell the phase-1 effect lives in). Evaluation keeps ALL
    gate-passed items: the primary readout is still the `opaque_strict` subset,
    but scoring the wider set costs nothing extra per ablation configuration and
    gives a better-powered secondary. (Amendment r2a, before the ablate run.)
    """
    elig = [it for it in items if it["item_id"] in passed]
    # Stratify the entity split so the opaque_strict cell -- the primary readout --
    # is halved evenly instead of being left to chance by a global shuffle.
    ent_stratum = {it["item_id"].split("::")[0]: it["strict_stratum"] for it in elig}
    disc = set()
    for st in sorted(set(ent_stratum.values())):
        group = sorted(e for e, v in ent_stratum.items() if v == st)
        random.Random(f"{seed}-{st}").shuffle(group)
        disc.update(group[:len(group) // 2])
    return ([it for it in elig if it["item_id"].split("::")[0] in disc
             and it["strict_stratum"] == "opaque_strict"],
            [it for it in elig if it["item_id"].split("::")[0] not in disc])


def jobs_for(items, conditions, n_carriers=1, frames=("F1",)):
    jobs, keys = [], []
    for it in items:
        cont = " " + it["target_form"]
        for c in it["carriers"][:n_carriers]:
            jobs.append((build_prompt(None, c["question"]), cont))
            keys.append((it["item_id"], c["qid"], "NOCTX", "-"))
            for fname in frames:
                for cond in conditions:
                    ctx = it["frames"][fname].format(M=mention_for(it, cond))
                    jobs.append((build_prompt(ctx, c["question"]), cont))
                    keys.append((it["item_id"], c["qid"], cond, fname))
    return jobs, keys


def deltas_from(keys, scored):
    base, cells = {}, {}
    for k, s in zip(keys, scored):
        if k[2] == "NOCTX":
            base[(k[0], k[1])] = s["logprob_sum"]
    for k, s in zip(keys, scored):
        if k[2] != "NOCTX":
            cells.setdefault((k[0], k[2]), []).append(s["logprob_sum"] - base[(k[0], k[1])])
    return {k: sum(v) / len(v) for k, v in cells.items()}


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return (xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])) if n else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["sweep", "ablate"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--phase1-dir", default="results/phase1_r1")
    ap.add_argument("--out-dir", default="results/phase2_r1")
    ap.add_argument("--batch-size", type=int, default=48)
    ap.add_argument("--sweep-items", type=int, default=60)
    ap.add_argument("--topk-frac", type=float, nargs="+", default=[0.01, 0.03, 0.05, 0.10])
    ap.add_argument("--n-random-controls", type=int, default=5)
    args = ap.parse_args()

    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from analyze_common import capability_gate

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(args.d0, encoding="utf-8")]
    passed, _ = capability_gate(Path(args.phase1_dir) / f"{args.tag}__probe.jsonl")
    disc, ev = split_items(items, passed)
    ev_strict = [it for it in ev if it["strict_stratum"] == "opaque_strict"]
    print(f"{args.tag}: discovery {len(disc)} items (opaque_strict), "
          f"evaluation {len(ev)} items of which {len(ev_strict)} opaque_strict")

    t0 = time.time()
    scorer = Scorer(args.model, batch_size=args.batch_size)
    abl = HeadAblator(scorer.model)
    print(f"  {abl.n_layers} layers x {abl.n_heads} heads = {abl.n_layers * abl.n_heads}")

    if args.mode == "sweep":
        sub = disc[:args.sweep_items]
        jobs, keys = jobs_for(sub, ("EXACT",))
        clean = deltas_from(keys, scorer.score(jobs))
        base = median([clean[(it["item_id"], "EXACT")] for it in sub])
        print(f"  clean EXACT on discovery subset: {base:+.3f} nats ({len(jobs)} prompts/ablation)")

        rows = []
        for layer in range(abl.n_layers):
            for head in range(abl.n_heads):
                abl.set([(layer, head)])
                d = deltas_from(keys, scorer.score(jobs))
                abl.clear()
                v = median([d[(it["item_id"], "EXACT")] for it in sub])
                rows.append(dict(layer=layer, head=head, exact=v, drop=base - v))
            done = (layer + 1) * abl.n_heads
            print(f"  layer {layer + 1}/{abl.n_layers} ({done} heads, "
                  f"{time.time() - t0:.0f}s)", flush=True)
        rows.sort(key=lambda r: -r["drop"])
        (out / f"{args.tag}__sweep.json").write_text(json.dumps(
            dict(clean_exact=base, n_items=len(sub), heads=rows), indent=2))
        print("  top 15 entrainment heads (layer, head, drop in nats):")
        for r in rows[:15]:
            print(f"    L{r['layer']:>2} H{r['head']:>2}  {r['drop']:+.3f}")

    else:
        sweep = json.loads((out / f"{args.tag}__sweep.json").read_text())
        ranked = [(r["layer"], r["head"]) for r in sweep["heads"]]
        total = abl.n_layers * abl.n_heads
        jobs, keys = jobs_for(ev, CONDITIONS, n_carriers=2, frames=("F1", "F2"))
        print(f"  evaluation: {len(jobs)} prompts per condition set")

        results = {}
        abl.clear()
        results["clean"] = deltas_from(keys, scorer.score(jobs))

        rng = random.Random(SEED)
        for frac in args.topk_frac:
            k = max(1, round(total * frac))
            results[f"top{frac}"] = deltas_from(keys, (abl.set(ranked[:k]),
                                                       scorer.score(jobs))[1])
            abl.clear()
            # layer-matched random controls: same number of heads drawn from the
            # same layers, so any generic damage from ablation is matched
            layers = [l for l, _ in ranked[:k]]
            for s in range(args.n_random_controls):
                r = random.Random(SEED + s)
                picks = {(l, r.randrange(abl.n_heads)) for l in layers}
                while len(picks) < k:
                    picks.add((r.choice(layers), r.randrange(abl.n_heads)))
                results[f"rand{frac}_{s}"] = deltas_from(
                    keys, (abl.set(sorted(picks)), scorer.score(jobs))[1])
                abl.clear()
            print(f"  k={k} ({frac:.0%}) done, {time.time() - t0:.0f}s", flush=True)

        payload = {name: {f"{i}|{c}": v for (i, c), v in d.items()}
                   for name, d in results.items()}
        (out / f"{args.tag}__ablate.json").write_text(json.dumps(
            dict(eval_items=[it["item_id"] for it in ev],
                 eval_items_strict=[it["item_id"] for it in ev_strict],
                 n_heads_total=total,
                 topk_frac=args.topk_frac, deltas=payload), indent=2))
        print(f"  wrote {out / f'{args.tag}__ablate.json'}")

    print(f"{args.tag}: {args.mode} done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
