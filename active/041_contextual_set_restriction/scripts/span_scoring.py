"""Length-normalised log probability of a character span, shared by B0 and B1.

A token whose character span straddles a window boundary is assigned to the earlier window, per the
frozen tokenizer-handling rule in `B1_PREANALYSIS_FREEZE.md`; the number of such tokens is returned
so it can be reported per model.
"""

from __future__ import annotations

import torch


@torch.inference_mode()
def score_spans(tokenizer, model, texts: list[str], spans: list[list[tuple[int, int]]],
                batch_size: int) -> list[list[dict[str, float]]]:
    """For each text, return one record per requested (start, end) character span."""
    tokenizer.padding_side = "right"
    results: list[list[dict[str, float]]] = []
    for start in range(0, len(texts), batch_size):
        chunk = texts[start: start + batch_size]
        chunk_spans = spans[start: start + batch_size]
        batch = tokenizer(chunk, add_special_tokens=True, padding=True, return_tensors="pt",
                          return_offsets_mapping=True)
        offsets = batch.pop("offset_mapping")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}
        logits = model(**batch, use_cache=False).logits.float().log_softmax(-1)
        for i, spans_for_text in enumerate(chunk_spans):
            n = int(lengths[i])
            token_logprobs = logits[i, :-1].gather(
                -1, batch["input_ids"][i, 1:].unsqueeze(-1)).squeeze(-1)
            record = []
            for span_start, span_end in spans_for_text:
                total, count, straddling = 0.0, 0, 0
                for position in range(1, n):
                    char_start, char_end = (int(offsets[i, position, 0]), int(offsets[i, position, 1]))
                    if char_end <= char_start:            # special or padding token
                        continue
                    if char_start >= span_end or char_end <= span_start:
                        continue
                    if char_start < span_start or char_end > span_end:
                        straddling += 1
                        if char_start < span_start:       # belongs to the earlier window
                            continue
                    total += float(token_logprobs[position - 1])
                    count += 1
                record.append({
                    "sum_logprob": total,
                    "n_tokens": count,
                    "mean_logprob": total / count if count else float("nan"),
                    "straddling_tokens": straddling,
                })
            results.append(record)
        if start % (batch_size * 25) == 0:
            print({"scored": start + len(chunk), "total": len(texts)}, flush=True)
    return results


@torch.inference_mode()
def score_segments(tokenizer, model, segment_lists: list[list[str]],
                   batch_size: int) -> list[list[dict[str, float]]]:
    """Score consecutive text segments without needing offset mappings.

    `segment_lists[i]` is `[prefix, segment_1, ..., segment_k]`; the first element is context and is
    not scored. Boundaries come from tokenising the cumulative prefixes, so a token that straddles a
    boundary falls into the earlier segment -- the same rule the offset path applies explicitly.

    This path exists because some tokenizers (Mistral's MistralCommonBackend) refuse
    `return_offsets_mapping`. It is verified to agree with the offset path to floating-point
    tolerance on a tokenizer that supports both; see `logs/span_scoring_equivalence.txt`.
    """
    tokenizer.padding_side = "right"
    boundaries = []
    texts = []
    for segments in segment_lists:
        cumulative, counts = "", []
        for segment in segments:
            cumulative += segment
            counts.append(len(tokenizer(cumulative, add_special_tokens=True)["input_ids"]))
        boundaries.append(counts)
        texts.append(cumulative)

    results: list[list[dict[str, float]]] = []
    for start in range(0, len(texts), batch_size):
        chunk = texts[start: start + batch_size]
        chunk_bounds = boundaries[start: start + batch_size]
        batch = tokenizer(chunk, add_special_tokens=True, padding=True, return_tensors="pt")
        batch = {key: value.to(model.device) for key, value in batch.items()}
        logits = model(**batch, use_cache=False).logits.float().log_softmax(-1)
        for i, counts in enumerate(chunk_bounds):
            token_logprobs = logits[i, :-1].gather(
                -1, batch["input_ids"][i, 1:].unsqueeze(-1)).squeeze(-1)
            record = []
            for segment_index in range(1, len(counts)):
                lo, hi = counts[segment_index - 1], counts[segment_index]
                values = [float(token_logprobs[position - 1]) for position in range(lo, hi)]
                total = float(sum(values))
                record.append({
                    "sum_logprob": total,
                    "n_tokens": len(values),
                    "mean_logprob": total / len(values) if values else float("nan"),
                    "straddling_tokens": 0,
                })
            results.append(record)
        if start % (batch_size * 25) == 0:
            print({"scored": start + len(chunk), "total": len(texts)}, flush=True)
    return results


def supports_offsets(tokenizer) -> bool:
    try:
        tokenizer("probe text", return_offsets_mapping=True)
        return True
    except Exception:
        return False
