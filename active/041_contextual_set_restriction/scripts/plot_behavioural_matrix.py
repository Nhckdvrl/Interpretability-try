"""Figure: the behavioural selectivity matrix on the explanation readout.

Each panel is one model. Bars are the change in P's omission consequence on the explanation
continuation, for the true property and for the contrasting one, under each manipulation. The
signature is the crossing: the referential manipulation raises the true property and lowers the
contrasting one, the event manipulation does the reverse.
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
SHORT = {"Qwen3-8B": "Qwen3-8B", "Meta-Llama-3.1-8B-Instruct": "Llama-3.1-8B",
         "gemma-3-12b-it": "Gemma-3-12B", "Mistral-Small-24B-Instruct-2501": "Mistral-24B"}


def consequences(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    support = {}
    for row in rows[1:]:
        support[(row["world_id"], row["r_condition"], row["e_condition"], row["cue_index"],
                 row["continuation_label"], row["description_condition"])] = row["explanation_support"]
    per = defaultdict(list)
    for row in rows[1:]:
        if row["description_condition"] != "full":
            continue
        base = (row["world_id"], row["r_condition"], row["e_condition"], row["cue_index"],
                row["continuation_label"])
        per[(row["r_condition"], row["e_condition"], row["item_id"],
             row["continuation_label"])].append(support[base + ("full",)] - support[base + ("drop_p",)])
    return rows[0]["model_checkpoint"].split("/")[-1], per


def contrast(per, label, keep, index, rng):
    def side(value):
        items = defaultdict(list)
        for key, values in per.items():
            if key[3] != label or key[index] != value:
                continue
            items[key[2]].extend(values)
        return np.array([float(np.mean(items[i])) for i in sorted(items)])
    values = side(keep[0]) - side(keep[1])
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return values.mean(), np.percentile(draws, 2.5), np.percentile(draws, 97.5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--explanation", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = [consequences(p) for p in args.explanation]
    fig, axes = plt.subplots(1, len(data), figsize=(3.0 * len(data), 3.4), sharey=False)
    axes = np.atleast_1d(axes)
    colours = {"true property": "#2f6fb5", "contrasting property": "#c8622a"}

    for ax, (model, per) in zip(axes, data):
        rng = np.random.default_rng(SEED)
        width, offset = 0.34, 0.18
        for j, (label, name) in enumerate((("p", "true property"),
                                           ("p_contrast", "contrasting property"))):
            centres, lows, highs = [], [], []
            for index, keep in ((0, ("R_plus", "R_minus")), (1, ("E_plus", "E_minus"))):
                mean, low, high = contrast(per, label, keep, index, rng)
                centres.append(mean)
                lows.append(mean - low)
                highs.append(high - mean)
            x = np.arange(2) + (offset if j else -offset)
            ax.bar(x, centres, width, color=colours[name], alpha=0.85, label=name)
            ax.errorbar(x, centres, yerr=[lows, highs], fmt="none", ecolor="#333333",
                        elinewidth=1.1, capsize=3)
        ax.axhline(0, color="#444444", linewidth=0.9)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["referential\nmanipulation", "event\nmanipulation"], fontsize=8.5)
        ax.set_title(SHORT.get(model, model), fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    axes[0].set_ylabel("change in P's omission consequence\non explanation support (nats/token)",
                       fontsize=8.5)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("The two manipulations move the two explanations in opposite directions",
                 fontsize=11, y=1.03)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".png"):
        fig.savefig(args.output.with_suffix(suffix), bbox_inches="tight", dpi=200)
    print(f"wrote {args.output.with_suffix('.png')}")


if __name__ == "__main__":
    main()
