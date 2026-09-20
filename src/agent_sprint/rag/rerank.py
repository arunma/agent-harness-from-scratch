"""Day 7 · Rerank top 50 -> top 5.

WHAT IT MUST DO
    Reorder hybrid candidates with a cross-encoder, and tell you what that
    costs in latency.

TO BUILD
    [ ] Local reranker on the 5090 (bge-reranker-v2-m3 or Qwen3-Reranker)
        via settings.vllm_rerank_url.
    [ ] Cohere Rerank behind the same interface for comparison.
    [ ] Batch the candidates. One call per document is the naive version and
        it will dominate your latency number.
    [ ] Measure both: recall@5 with and without rerank, and added p50/p95
        latency per query.

DONE WHEN
    You can say what one point of recall cost you in milliseconds, and
    whether the managed reranker earned its API call.

READ
    https://docs.cohere.com/docs/rerank-overview
"""
