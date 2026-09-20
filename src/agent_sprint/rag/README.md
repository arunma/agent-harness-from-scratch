# rag/ — learn zone (you write the pipeline; the tools are adopted)

Production RAG over public MAS documents in `data/corpus/`. You don't hand-write BM25 or embeddings; you *do* own ingestion, metadata, filtering, citations, guardrails and lifecycle.

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 6 | `d06_1_ingest.py` | Parse PDFs with Docling into structured sections. | One table-heavy PDF compared with Claude's native PDF input. |
| 6 | `d06_2_extract.py` | Pydantic schema per document (issuer, notice number, effective date, applicability, superseded-by, obligations); failures to a review queue. | Validation failure rate recorded. |
| 6 | `d06_3_chunk.py`, `d06_4_index.py` | Structure-aware chunks with full metadata; index into OpenSearch hybrid. | Every chunk carries doc, version, page, section path, offsets, access level. |
| 6 | `../evals/d06_retrieval_metrics.py` | recall@k and MRR over `data/golden/`. | Embedding shoot-out table. |
| 7 | `d07_1_rerank.py`, `d07_2_answer.py` | Rerank top 50 → 5; answers with citations mapped to document, page, section. | Recall and latency with and without rerank. |
| 7 | `d07_3_guard.py` | Entitlement filter in the query, PII redaction at ingest, injection scan of chunks, grounding check, "not found" threshold. | A restricted chunk provably never reaches the prompt. |
| 7 | `d07_4_lifecycle.py` | Re-ingest supersedes old versions; delete removes from index and caches. | Superseded notice no longer cited; deleted doc gone. |
