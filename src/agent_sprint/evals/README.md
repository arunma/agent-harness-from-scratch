# evals/ — learn zone (Day 11 is the most important day)

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 6 | `d06_retrieval_metrics.py` | recall@k, MRR over `data/golden/`. | Used by the embedding shoot-out. |
| 11 | `d11_1_taxonomy.md` | Failure taxonomy from 50 real traces (open coding → groups). | Seeded from the MAST paper, grounded in your traces. |
| 11 | `d11_2_scenarios/` | 20 τ-bench-style scenarios with an expected DB end-state. | Covers RAG questions and MCP tool flows. |
| 11 | `d11_3_assertions.py`, `d11_4_judges.py` | Code checks first; one LLM judge validated against your labels (TPR/TNR). | Judge agreement measured. |
| 11 | `d11_5_runner.py` | pass^k runner (k=4); scorecard output. | `make eval` (or `uv run python -m agent_sprint.evals.runner`) prints a scorecard. |
