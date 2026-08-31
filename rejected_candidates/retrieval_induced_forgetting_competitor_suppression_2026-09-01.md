# Retrieval-induced forgetting: competitor suppression vs non-inhibitory interference

Date: 2026-09-01  
Verdict: **KILL-BEHAVIOR**

## Semantic aliases

- retrieval-induced forgetting in LLMs
- retrieval practice competitor suppression
- adaptive forgetting after selective retrieval
- inhibitory memory control vs blocking/context account
- RIF in language models

## Natural question

When a model selectively retrieves one memory, does it actively suppress competing related memories, or does later forgetting arise from strengthened targets / changed retrieval context without weakening the competitors themselves?

This is a mature, benchmark-independent memory-science debate. Human RIF work distinguishes inhibitory suppression, strength/blocking, and context accounts using retrieval-specificity, independent-probe, recognition, and competition manipulations.

## Decisive kill evidence

Two broad searches found no established modern open-LLM phenotype corresponding to the canonical retrieval-practice effect:

1. study multiple related items;
2. selectively retrieve a subset;
3. later test related unpracticed items against unpracticed-category controls;
4. observe selective impairment of the related unpracticed items.

Searches for retrieval-induced forgetting, retrieval practice, competitor suppression, memory inhibition, Llama/Qwen, and transformers returned human/neural memory literature and external agent-memory retrieval systems, not a published LLM RIF effect on modern open checkpoints.

Therefore continuing would require constructing an RIF paradigm and running Llama/Qwen/Mistral to discover whether the basic phenomenon exists. Under the current discovery protocol, that is behavior lottery and cannot enter the authoritative register.

## Nearest-neighbor warning

Do not substitute proactive interference, long-context forgetting, RAG retrieval competition, or external memory-store pruning. Those are semantically different phenomena and do not establish retrieval-induced forgetting.

## Resurrection condition

Reopen only if a public paper/artifact demonstrates canonical Rp+ / Rp- / Nrp retrieval-induced forgetting on at least two relevant modern open model families with row-level stimuli and auditable scoring, while the inhibitory-vs-blocking/context mechanism remains unoccupied by LLM MI work.
