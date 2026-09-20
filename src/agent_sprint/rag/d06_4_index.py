"""Day 6 · Hybrid index: BM25 + dense, with filterable metadata.

WHAT IT MUST DO
    Get chunks into OpenSearch so both retrieval modes work and every piece
    of metadata is a filter, not a string in the body.

TO BUILD
    [ ] Mapping: text field for BM25, knn_vector for dense, and every
        metadata field typed and filterable (dates as dates).
    [ ] Embed with the day's model; keep the embedding call behind one
        function so the shoot-out can swap it.
    [ ] Hybrid query with a normalisation pipeline. Understand what RRF is
        doing before you accept its output.
    [ ] Three query paths you can run separately: BM25 only, dense only,
        hybrid. The shoot-out needs all three.
    [ ] Bulk index idempotently, keyed on chunk id, so a re-ingest updates
        rather than duplicates.

EXPERIMENT (today's number)
    Embedding shoot-out on your golden set: local (Qwen3-Embedding or BGE-M3
    on the 5090) vs managed (Voyage, Cohere), each as BM25 / dense / hybrid.
    Nudge k1 and b and watch what moves.

READ
    https://opensearch.org/docs/latest/search-plugins/hybrid-search/
    https://arxiv.org/abs/2104.08663  (BEIR: why BM25 is still hard to beat)
"""
