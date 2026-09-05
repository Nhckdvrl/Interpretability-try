"""Key figure: the two functions are computed at different depths, with opposite causal marks.

Top row: held-out probe AUC against depth for each state. The event-relevance state is decodable
almost immediately; the referential state only after a third to a half of the stack.

Bottom row: the causal effect of editing each state, on support for the contrasting-property
explanation, at every layer. In its own window each state moves the readout, and they move it in
opposite directions.
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
COLOURS = {"referential": "#2f6fb5", "event": "#c8622a"}


def load(tag, label, directory):
    files = [directory / f"v4dense_{label}_fold_{fold}_{tag}.jsonl" for fold in ("a", "b")]
    metas, rows = [], []
    for path in files:
        if not path.exists():
            return None, None, None
        content = [json.loads(line) for line in path.read_text().splitlines() if line]
        metas.append(content[0])
        rows.append((content[0], content[1:]))
    layers = sorted(int(k) for k in metas[0]["layers"])
    auc = [float(np.mean([m["layers"][str(layer)] for m in metas])) for layer in layers]
    return layers, auc, rows


def effect(rows, layer, rng):
    per_item = defaultdict(list)
    for meta, items in rows:
        selector = meta["label"]
        for row in items:
            if not (row["held_out"] and row[selector]):
                continue
            if row["continuation_label"] != "p_contrast":
                continue
            role = row["scores"].get(f"L{layer}|role|a4")
            shuffled = row["scores"].get(f"L{layer}|shuffled|a4")
            if role is not None and shuffled is not None:
                per_item[row["item_id"]].append(role - shuffled)
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return np.nan, np.nan, np.nan
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return values.mean(), np.percentile(draws, 2.5), np.percentile(draws, 97.5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", required=True, help="tag=Display pairs")
    parser.add_argument("--directory", type=Path, default=Path("results/raw"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pairs = [m.split("=") for m in args.models]
    fig, axes = plt.subplots(2, len(pairs), figsize=(4.3 * len(pairs), 5.4), sharex=False)
    axes = np.atleast_2d(axes)
    if axes.shape[0] == 1:
        axes = axes.T

    for column, (tag, display) in enumerate(pairs):
        top, bottom = axes[0, column], axes[1, column]
        for state, label in (("referential", "p_restricts"),
                             ("event", "p_relevant_to_event")):
            layers, auc, rows = load(tag, label, args.directory)
            if layers is None:
                continue
            depth = np.array(layers) / max(layers)
            top.plot(depth, auc, color=COLOURS[state], linewidth=1.8, label=f"{state} state")
            rng = np.random.default_rng(SEED)
            means, lows, highs = [], [], []
            for layer in layers:
                mean, low, high = effect(rows, layer, rng)
                means.append(mean)
                lows.append(low)
                highs.append(high)
            bottom.plot(depth, means, color=COLOURS[state], linewidth=1.8, label=f"edit {state}")
            bottom.fill_between(depth, lows, highs, color=COLOURS[state], alpha=0.18, linewidth=0)
        top.axhline(0.5, color="#888888", linewidth=0.8, linestyle=":")
        top.set_ylim(0.45, 1.02)
        top.set_title(display, fontsize=11)
        bottom.axhline(0, color="#444444", linewidth=0.9)
        for ax in (top, bottom):
            ax.spines[["top", "right"]].set_visible(False)
            ax.set_xlabel("relative depth", fontsize=8.5)
        if column == 0:
            top.set_ylabel("held-out probe AUC", fontsize=9)
            bottom.set_ylabel("effect of the edit on support for\nthe contrasting property "
                              "(nats/token)", fontsize=8.5)
            top.legend(frameon=False, fontsize=8.5, loc="upper left")
            bottom.legend(frameon=False, fontsize=8.5, loc="lower left")

    fig.suptitle("Event relevance is available early and the referential role only past mid-stack "
                 "in 4/4; their edits push the same readout opposite ways in 3/4",
                 fontsize=11, y=1.0)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".png"):
        fig.savefig(args.output.with_suffix(suffix), bbox_inches="tight", dpi=200)
    print(f"wrote {args.output.with_suffix('.png')}")


if __name__ == "__main__":
    main()
