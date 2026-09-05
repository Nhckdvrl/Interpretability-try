"""Figure: the human effect in an LM, on Davies & Richardson's own 48 items.

Reading time is replaced by mean token surprisal over their two windows. Negative is the direction
that eases processing, so their result predicts negative bars. Semantic relevance transfers and
referential licensing does not, which is why B1 replaces the referential factor with a denotational
manipulation whose gold is computed from the described properties.
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
SHORT = {"Qwen3-8B": "Qwen3\n8B", "Meta-Llama-3.1-8B-Instruct": "Llama-3.1\n8B",
         "gemma-3-12b-it": "Gemma-3\n12B", "Mistral-Small-24B-Instruct-2501": "Mistral\n24B"}


def effects(path, window_index):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    cells = defaultdict(dict)
    for row in rows[1:]:
        cells[row["item_id"]][(row["semantic_relevance"], row["referential_relevance"])] = (
            row["np_surprisal"], row["wrapup_surprisal"])
    items = sorted(cells)

    def value(item, sem, ref):
        return cells[item][(sem, ref)][window_index]

    referential = np.array([
        (value(i, "plus_sem", "two_referents") + value(i, "minus_sem", "two_referents")) / 2
        - (value(i, "plus_sem", "one_referent") + value(i, "minus_sem", "one_referent")) / 2
        for i in items])
    semantic = np.array([
        (value(i, "plus_sem", "one_referent") + value(i, "plus_sem", "two_referents")) / 2
        - (value(i, "minus_sem", "one_referent") + value(i, "minus_sem", "two_referents")) / 2
        for i in items])
    return rows[0]["model_checkpoint"].split("/")[-1], referential, semantic


def band(values, rng):
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return values.mean(), np.percentile(draws, 2.5), np.percentile(draws, 97.5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4), sharey=True)
    colours = {"referential relevance": "#7a7a7a", "semantic relevance": "#2f6fb5"}
    for ax, window_index, title in zip(axes, (0, 1),
                                       ("noun-phrase window", "wrap-up window")):
        rng = np.random.default_rng(SEED)
        names, series = [], {"referential relevance": [], "semantic relevance": []}
        errors = {"referential relevance": [[], []], "semantic relevance": [[], []]}
        for path in args.results:
            model, referential, semantic = effects(path, window_index)
            names.append(SHORT.get(model, model))
            for key, values in (("referential relevance", referential),
                                ("semantic relevance", semantic)):
                mean, low, high = band(values, rng)
                series[key].append(mean)
                errors[key][0].append(mean - low)
                errors[key][1].append(high - mean)
        x = np.arange(len(names))
        for j, key in enumerate(series):
            position = x + (0.18 if j else -0.18)
            ax.bar(position, series[key], 0.34, color=colours[key], alpha=0.85, label=key)
            ax.errorbar(position, series[key], yerr=errors[key], fmt="none", ecolor="#333333",
                        elinewidth=1.1, capsize=3)
        ax.axhline(0, color="#444444", linewidth=0.9)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8.5)
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("change in surprisal (nats/token)\nnegative eases processing", fontsize=8.5)
    axes[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle("Davies & Richardson's items in an LM: the semantic half transfers, "
                 "the referential half does not", fontsize=10.5, y=1.03)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".png"):
        fig.savefig(args.output.with_suffix(suffix), bbox_inches="tight", dpi=200)
    print(f"wrote {args.output.with_suffix('.png')}")


if __name__ == "__main__":
    main()
