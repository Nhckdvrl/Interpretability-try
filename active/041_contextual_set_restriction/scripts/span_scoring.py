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
