"""Phase 3 for 014: do the entrainment heads THEMSELVES write toward an unseen alias?

Phase 2 answered "the same heads carry both components" but its proportionality
half rested on a ratio of medians whose CI always included zero. Here the same
question is asked with a per-item continuous quantity read straight off the
heads' write: direct logit attribution to the target's first token.

Non-circular by construction: heads were ranked on the phase-2 DISCOVERY half
using EXACT only, and everything below is measured on the held-out half.

Contract: configs/contract_r1.yaml, `phase3` block (2026-08-29-r3).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, str(Path(__file__).parent))
from run_phase1 import CONDITIONS, build_prompt, mention_for          # noqa: E402
from run_phase2 import HeadAblator, split_items                       # noqa: E402

SEED = 20260829


class DLAReader:
    """Reads the selected heads' write and projects it onto the target token."""

    def __init__(self, model, tok):
        self.model, self.tok = model, tok
        self.abl = HeadAblator(model)          # reuse its layer/head geometry
        self.layers = self.abl.layers
        self.hd = self.abl.head_dim
        core = model.model if hasattr(model, "model") else model
        self.norm = getattr(core, "norm", None) or getattr(core.language_model, "norm")
        self.W_U = model.get_output_embeddings().weight      # (vocab, d_model)
        self.captured: dict[int, torch.Tensor] = {}
        self.resid: torch.Tensor | None = None
        self.handles = []

    def arm(self, layers_needed):
        self.disarm()
        for L in sorted(set(layers_needed)):
            def hook(module, args, L=L):
                self.captured[L] = args[0][:, -1, :].detach()   # last position only
            self.handles.append(
                self.layers[L].self_attn.o_proj.register_forward_pre_hook(hook))

        def norm_hook(module, args):
            self.resid = args[0][:, -1, :].detach()
        self.handles.append(self.norm.register_forward_pre_hook(norm_hook))

    def disarm(self):
        for h in self.handles:
            h.remove()
        self.handles = []

    @torch.no_grad()
    def write_vectors(self, prompts, head_sets, batch_size=32):
        """-> {set_name: (n_prompts, d_model)} head writes, plus rms per prompt."""
        needed = {l for hs in head_sets.values() for l, _ in hs}
        self.arm(needed)
        outs = {k: [] for k in head_sets}
        rmss = []
        eps = getattr(self.norm, "variance_epsilon",
                      getattr(self.norm, "eps", 1e-6))
        for i in range(0, len(prompts), batch_size):
            chunk = prompts[i:i + batch_size]
            enc = self.tok(chunk, return_tensors="pt", padding=True).to(
                self.model.device)
            self.captured.clear()
            self.model(**enc)
            x = self.resid.float()
            rmss.append(torch.sqrt(x.pow(2).mean(-1) + eps).cpu())
            for name, hs in head_sets.items():
                w = torch.zeros(len(chunk), self.W_U.shape[1],
                                device=x.device, dtype=torch.float32)
                for L, h in hs:
                    sl = slice(h * self.hd, (h + 1) * self.hd)
                    xh = self.captured[L][:, sl].float()
                    W_O = self.layers[L].self_attn.o_proj.weight[:, sl].float()
                    w += xh @ W_O.T
                outs[name].append(w.cpu())
        self.disarm()
        return ({k: torch.cat(v) for k, v in outs.items()}, torch.cat(rmss))

    def dla(self, w, rms, target_ids):
        """((w / rms) * ln_weight) . W_U[target]  -- RMSNorm, so no centering."""
        g = self.norm.weight.float().cpu()
        normed = (w / rms.unsqueeze(-1)) * g
        U = self.W_U[target_ids].float().cpu()               # (n, d_model)
        return (normed * U).sum(-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--d0", default="data/frozen_d0.jsonl")
    ap.add_argument("--phase1-dir", default="results/phase1_r1")
    ap.add_argument("--phase2-dir", default="results/phase2_r1")
    ap.add_argument("--out-dir", default="results/phase3_r1")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--topk-frac", type=float, nargs="+", default=[0.03, 0.05])
    ap.add_argument("--n-random-controls", type=int, default=5)
    args = ap.parse_args()

    from analyze_common import capability_gate

    items = [json.loads(l) for l in open(args.d0, encoding="utf-8")]
    passed, _ = capability_gate(Path(args.phase1_dir) / f"{args.tag}__probe.jsonl")
    _, ev = split_items(items, passed)          # same split as phase 2
    ev_strict = [it for it in ev if it["strict_stratum"] == "opaque_strict"]
    print(f"{args.tag}: evaluation {len(ev)} items, {len(ev_strict)} opaque_strict")

    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(args.model)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="cuda").eval()
    reader = DLAReader(model, tok)
    total = reader.abl.n_layers * reader.abl.n_heads

    sweep = json.loads((Path(args.phase2_dir) / f"{args.tag}__sweep.json").read_text())
    ranked = [(r["layer"], r["head"]) for r in sweep["heads"]]

    head_sets = {}
    for frac in args.topk_frac:
        k = max(1, round(total * frac))
        head_sets[f"ent{frac}"] = ranked[:k]
        layers = [l for l, _ in ranked[:k]]
        for s in range(args.n_random_controls):
            r = random.Random(SEED + s)
            picks = {(l, r.randrange(reader.abl.n_heads)) for l in layers}
            while len(picks) < k:
                picks.add((r.choice(layers), r.randrange(reader.abl.n_heads)))
            head_sets[f"rand{frac}_{s}"] = sorted(picks)
    print(f"  {total} heads; sets: " +
          ", ".join(f"{k}={len(v)}" for k, v in head_sets.items() if "rand" not in k))

    prompts, keys, targets = [], [], []
    for it in ev:
        # first token of " <target>" is what the last prompt position predicts
        tid = tok.encode(" " + it["target_form"], add_special_tokens=False)[0]
        for c in it["carriers"][:2]:
            prompts.append(build_prompt(None, c["question"]))
            keys.append((it["item_id"], c["qid"], "NOCTX", "-")); targets.append(tid)
            for fname in ("F1", "F2"):
                for cond in CONDITIONS:
                    ctx = it["frames"][fname].format(M=mention_for(it, cond))
                    prompts.append(build_prompt(ctx, c["question"]))
                    keys.append((it["item_id"], c["qid"], cond, fname))
                    targets.append(tid)
    print(f"  {len(prompts)} prompts")

    writes, rms = reader.write_vectors(prompts, head_sets, args.batch_size)
    tgt = torch.tensor(targets)
    dla = {name: reader.dla(w, rms, tgt).tolist() for name, w in writes.items()}

    # ---- alignment test, computed here so only scalars are stored -------------
    # cos(w_cond - w_NOCTX, w_EXACT - w_NOCTX): is the write direction under an
    # alias more like the write when the target itself appeared than a
    # similarity-matched control is?
    idx = {}
    for n, k in enumerate(keys):
        idx[(k[0], k[1], k[2], k[3])] = n
    align = {}
    for name in [h for h in head_sets if h.startswith("ent")]:
        W = writes[name]
        rows = []
        for it in ev:
            for c in it["carriers"][:2]:
                base = W[idx[(it["item_id"], c["qid"], "NOCTX", "-")]]
                for fname in ("F1", "F2"):
                    dex = W[idx[(it["item_id"], c["qid"], "EXACT", fname)]] - base
                    if dex.norm() < 1e-6:
                        continue
                    row = dict(item_id=it["item_id"], qid=c["qid"], frame=fname)
                    for cond in ("ALIAS", "SEMREL", "UNREL"):
                        d = W[idx[(it["item_id"], c["qid"], cond, fname)]] - base
                        row[cond] = float(torch.nn.functional.cosine_similarity(
                            d, dex, dim=0)) if d.norm() > 1e-6 else float("nan")
                    rows.append(row)
        align[name] = rows

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / f"{args.tag}__dla.json").open("w") as f:
        json.dump(dict(keys=[list(k) for k in keys], dla=dla, n_heads_total=total,
                       topk_frac=args.topk_frac,
                       eval_items=[it["item_id"] for it in ev],
                       eval_items_strict=[it["item_id"] for it in ev_strict],
                       align=align), f)
    print(f"{args.tag}: phase 3 done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
