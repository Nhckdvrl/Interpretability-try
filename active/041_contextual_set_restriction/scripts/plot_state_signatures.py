"""Key figure: two states at the same token, opposite causal signatures.

Left panel is the true-property continuation, right panel the contrasting one. Bars are role minus
shuffled, averaged over every depth whose held-out AUC is at least 0.6, with 95% bootstrap intervals
over held-out items. The right panel is the claim: removing the referential role raises support for
the alternative property, removing event relevance lowers it, in every family.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BOOTSTRAP = 5000
SEED = 20260904
MIN_AUC = 0.6
SHORT = {"Qwen3-8B": "Qwen3\n8B", "Meta-Llama-3.1-8B-Instruct": "Llama-3.1\n8B",
         "gemma-3-12b-it": "Gemma-3\n12B", "Mistral-Small-24B-Instruct-2501": "Mistral\n24B"}


def estimate(rows, meta, selector, label, rng):
    layers = [int(k) for k, v in meta["layers"].items() if v >= MIN_AUC]
    per_item = defaultdict(list)
    for row in rows:
        if not (row["held_out"] and row[selector]) or row["continuation_label"] != label:
            continue
        for layer in layers:
            role = row["scores"].get(f"L{layer}|role|a4")
            shuffled = row["scores"].get(f"L{layer}|shuffled|a4")
            if role is not None and shuffled is not None:
                per_item[row["item_id"]].append(role - shuffled)
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return values.mean(), np.percentile(draws, 2.5), np.percentile(draws, 97.5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--referential", type=Path, nargs="+", required=True)
    parser.add_argument("--event", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = defaultdict(dict)
    for kind, paths in (("referential", args.referential), ("event", args.event)):
        for path in paths:
            rows = [json.loads(line) for line in path.read_text().splitlines() if line]
            data[rows[0]["model_checkpoint"].split("/")[-1]][kind] = (rows[0], rows[1:])

    models = [m for m in SHORT if m in data]
    rng = np.random.default_rng(SEED)
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6), sharey=True)
    width, offset = 0.36, 0.19
    colours = {"referential": "#2f6fb5", "event": "#c8622a"}

    for ax, label, title in zip(
            axes, ("p", "p_contrast"),
            ("support for the TRUE property", "support for the CONTRASTING property")):
        for j, kind in enumerate(("referential", "event")):
            selector = "p_restricts" if kind == "referential" else "p_relevant_to_event"
            centres, lows, highs = [], [], []
            for model in models:
                meta, rows = data[model][kind]
                mean, low, high = estimate(rows, meta, selector, label, rng)
                centres.append(mean)
                lows.append(mean - low)
                highs.append(high - mean)
            x = np.arange(len(models)) + (offset if j else -offset)
            ax.bar(x, centres, width, color=colours[kind], alpha=0.85,
                   label=f"edit the {kind} state")
            ax.errorbar(x, centres, yerr=[lows, highs], fmt="none", ecolor="#333333",
                        elinewidth=1.1, capsize=3)
        ax.axhline(0, color="#444444", linewidth=0.9)
        ax.set_xticks(np.arange(len(models)))
        ax.set_xticklabels([SHORT[m] for m in models], fontsize=8.5)
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    axes[0].set_ylabel("change in explanation support\n(role − shuffled, nats/token)", fontsize=9)
    axes[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle("Editing the referential role and editing event relevance leave opposite marks "
                 "on the same readout", fontsize=10.5, y=1.02)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".png"):
        fig.savefig(args.output.with_suffix(suffix), bbox_inches="tight", dpi=200)
    print(f"wrote {args.output.with_suffix('.pdf')} and {args.output.with_suffix('.png')}")


if __name__ == "__main__":
    main()
