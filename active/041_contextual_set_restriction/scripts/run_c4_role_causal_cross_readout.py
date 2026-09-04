"""C4: does the referential-role state causally drive the explanation readout?

B1 showed a directed asymmetry: making a modifier referentially load-bearing redistributes
explanatory support toward the true property and away from the contrasting one. This asks whether
that coupling is carried by the modifier's referential-role state.

Procedure, reusing the S1 estimator and the S3 edit unchanged:

  1. capture the residual state at the P-modifier token on full `np` descriptions;
  2. estimate a mass-mean restriction-role direction with half the property families held out,
     picking the depth by held-out probe AUC and never by causal performance;
  3. apply the frozen S3 counterfactual replacement at that token,
         h' = h + alpha * (mu_opposite - h . d) * d,
     which pushes a restricting modifier toward the non-restricting class mean and vice versa;
  4. read out, on held-out families only, whichever quantity this context defines.

Two contexts, run separately because their prompts differ:
  reference   -- chat-templated forced choice, ReferenceMargin (reproduces S3 on the new worlds)
  explanation -- raw text, ExplanationSupport for the true property and for the contrasting one

The decisive cell is the explanation context: an edit to a *referential* state that moves an
*explanation* readout property-specifically is the causal form of the R->E coupling.

Controls come from S3 and cost one pass each: a shuffled-label direction and a random unit
direction.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "phenomenon_miner"))
from model_scoring import load_model, resolve_snapshot  # noqa: E402

ALPHAS = [2.0, 4.0]
DEPTH_FRACTIONS = [0.25, 0.375, 0.5, 0.625, 0.75]
SYSTEM = "Answer the final multiple-choice question using only A, B or C. Do not explain."
OPTIONS = ["A", "B", "C"]
SEED = 20260904


def decoder_layers(model):
    for path in ("model.layers", "model.language_model.layers", "language_model.model.layers"):
        node = model
        try:
            for part in path.split("."):
                node = getattr(node, part)
            return node
        except AttributeError:
            continue
    raise AttributeError("Cannot locate decoder layers")


def format_chat(tokenizer, text: str) -> str:
    for candidate in ([{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
                      [{"role": "user", "content": f"{SYSTEM}\n\n{text}"}]):
        for kwargs in ({"enable_thinking": False}, {}):
            try:
                return tokenizer.apply_chat_template(
                    candidate, tokenize=False, add_generation_prompt=True, **kwargs)
            except Exception:
                continue
    raise ValueError("No usable chat template")


def modifier_position(tokenizer, prompt: str, np_span: str, modifier: str) -> int | None:
    """Token index of the last token of the P modifier inside the critical noun phrase."""
    start = prompt.rfind(np_span)
    if start < 0:
        return None
    offset = np_span.find(modifier)
    if offset < 0:
        return None
    char_end = start + offset + len(modifier)
    ids = tokenizer(prompt[:char_end], add_special_tokens=True)["input_ids"]
    return len(ids) - 1


@torch.inference_mode()
def forward(model, tokenizer, prompts, batch_size, capture_positions=None, layers=None,
            block_index=None, direction=None, mu=None, alpha=0.0, positions=None,
            score_fn=None):
    """One pass. Optionally captures residuals, optionally edits one token, always scores."""
    tokenizer.padding_side = "right"
    device_direction = None if direction is None else torch.from_numpy(direction).to(model.device)
    captured, scored = [], []
    for start in range(0, len(prompts), batch_size):
        chunk = prompts[start: start + batch_size]
        chunk_positions = None if positions is None else positions[start: start + batch_size]
        batch = tokenizer(chunk, add_special_tokens=True, padding=True, return_tensors="pt")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}

        handle = None
        if block_index is not None and device_direction is not None:
            def hook(_module, _inputs, output):
                changed = output[0] if isinstance(output, tuple) else output
                for i, position in enumerate(chunk_positions):
                    if position is None:
                        continue
                    vector = changed[i, position].to(torch.float32)
                    axis = device_direction.to(torch.float32)
                    delta = alpha * (float(mu[start + i]) - float(vector @ axis))
                    changed[i, position] = (vector + delta * axis).to(changed.dtype)
                return (changed,) + output[1:] if isinstance(output, tuple) else changed
            handle = decoder_layers(model)[block_index].register_forward_hook(hook)

        output = model(**batch, output_hidden_states=capture_positions is not None, use_cache=False)
        if handle is not None:
            handle.remove()

        if capture_positions is not None:
            for i in range(len(chunk)):
                position = capture_positions[start + i]
                if position is None:
                    captured.append(None)
                    continue
                captured.append(np.stack([
                    output.hidden_states[layer][i, position].float().cpu().numpy()
                    for layer in layers]))
        scored.extend(score_fn(output.logits, batch, lengths, start, len(chunk)))
        if start % (batch_size * 40) == 0:
            print(json.dumps({"scored": start + len(chunk), "total": len(prompts)}), flush=True)
    return captured, scored


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--context", choices=["reference", "explanation"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    rows = [r for r in rows if r["readout"] == args.context
            and r["description_condition"] == "full"
            and (args.context == "explanation" or r["surface_form"] == "np")]
    if args.context == "reference":
        rows = [r for r in rows if r["mapping_index"] == 0]

    tokenizer, model = load_model(args.model_path, config["dtype"])
    n_blocks = config["models"][args.model]["n_blocks"]
    layers = sorted({int(round(f * n_blocks)) for f in DEPTH_FRACTIONS})

    if args.context == "reference":
        prompts = [format_chat(tokenizer, r["prompt_text"]) for r in rows]
        spans = [r["np_span"] for r in rows]
        option_ids = [tokenizer(prompts[0] + o, add_special_tokens=True)["input_ids"][-1]
                      for o in OPTIONS]

        def score_fn(logits, batch, lengths, start, n):
            out = []
            for i in range(n):
                final = logits[i, int(lengths[i]) - 1].float().log_softmax(-1)
                values = {o: float(final[t]) for o, t in zip(OPTIONS, option_ids)}
                gold = rows[start + i]["gold_option"]
                others = torch.tensor([v for o, v in values.items() if o != gold])
                out.append(values[gold] - float(torch.logsumexp(others, 0)))
            return out
    else:
        prompts = [r["prefix"] + r["continuation"] for r in rows]
        spans = [r["critical_sentence"] for r in rows]
        boundaries = [len(tokenizer(r["prefix"], add_special_tokens=True)["input_ids"])
                      for r in rows]

        def score_fn(logits, batch, lengths, start, n):
            out = []
            logprobs = logits.float().log_softmax(-1)
            for i in range(n):
                lo, hi = boundaries[start + i], int(lengths[i])
                values = [float(logprobs[i, p - 1, batch["input_ids"][i, p]]) for p in range(lo, hi)]
                out.append(sum(values) / len(values) if values else float("nan"))
            return out

    # The P adjective comes from the frozen item table, never from string surgery on the prompt:
    # the wrap-up phrases also contain "the", which a naive scan picks up instead.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "b1_builder", Path(__file__).resolve().parent / "build_b1_function_cross.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    p_value = {item[0]: item[5] for item in builder.ITEMS}
    positions = [modifier_position(tokenizer, prompt, span, p_value[row["item_id"]])
                 for prompt, span, row in zip(prompts, spans, rows)]

    print(json.dumps({"rows": len(rows), "located": sum(p is not None for p in positions)}),
          flush=True)

    captured, baseline = forward(model, tokenizer, prompts, args.batch_size,
                                 capture_positions=positions, layers=layers, score_fn=score_fn)

    families = sorted({r["item_id"] for r in rows})
    held_out = set(families[len(families) // 2:])
    labels = np.array([r["p_restricts"] for r in rows])
    valid = np.array([c is not None for c in captured])
    states = np.stack([c if c is not None else np.zeros_like(captured[0]) for c in captured])
    train = np.array([r["item_id"] not in held_out for r in rows]) & valid
    test = np.array([r["item_id"] in held_out for r in rows]) & valid

    rng = np.random.default_rng(SEED)
    best = None
    for index, layer in enumerate(layers):
        features = states[:, index]
        positive = features[train & labels].mean(0)
        negative = features[train & ~labels].mean(0)
        direction = positive - negative
        direction = direction / (np.linalg.norm(direction) + 1e-8)
        projection = features @ direction
        pos, neg = projection[test & labels], projection[test & ~labels]
        auc = float((pos[:, None] > neg[None, :]).mean())
        print(json.dumps({"layer": layer, "held_out_auc": round(auc, 4)}), flush=True)
        if best is None or auc > best["auc"]:
            shuffled_labels = rng.permutation(labels[train])
            train_features = features[train]
            shuffled = (train_features[shuffled_labels].mean(0)
                        - train_features[~shuffled_labels].mean(0))
            shuffled = shuffled / (np.linalg.norm(shuffled) + 1e-8)
            random = rng.standard_normal(features.shape[1]).astype("float32")
            random = random / np.linalg.norm(random)
            best = {"auc": auc, "layer": layer, "index": index,
                    "role": direction.astype("float32"),
                    "shuffled": shuffled.astype("float32"), "random": random}

    index = best["index"]
    features = states[:, index]
    means = {}
    for name in ("role", "shuffled", "random"):
        projection = features[train] @ best[name]
        means[name] = (float(projection[labels[train]].mean()),
                       float(projection[~labels[train]].mean()))

    results = {"baseline": baseline}
    for name in ("role", "shuffled", "random"):
        positive_mean, negative_mean = means[name]
        for alpha in ALPHAS:
            opposite = np.where(labels, negative_mean, positive_mean)
            _, per_row = forward(
                model, tokenizer, prompts, args.batch_size,
                block_index=best["layer"], direction=best[name], mu=opposite, alpha=alpha,
                positions=positions, score_fn=score_fn)
            results[f"{name}|a{alpha:g}"] = per_row
            print(json.dumps({"edit": f"{name}|a{alpha:g}", "done": len(per_row)}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": "c4_role_causal_cross_readout_v1",
            "context": args.context, "model_checkpoint": checkpoint, "model_revision": revision,
            "layer": best["layer"], "held_out_auc": best["auc"], "alphas": ALPHAS,
            "held_out_families": sorted(held_out), "n_rows": len(rows),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for i, row in enumerate(rows):
            handle.write(json.dumps({
                "record_type": "example",
                **{k: v for k, v in row.items() if k not in {"prompt_text", "prefix"}},
                "held_out": row["item_id"] in held_out,
                "scores": {name: values[i] for name, values in results.items()},
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "layer": best["layer"],
                      "held_out_auc": best["auc"]}))


if __name__ == "__main__":
    main()
