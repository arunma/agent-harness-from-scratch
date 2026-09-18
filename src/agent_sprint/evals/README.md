# evals/ — learn zone (Day 11 is the most important day)

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 6 | `retrieval_metrics.py` | recall@k, MRR over `data/golden/`. | Used by the embedding shoot-out. |
| 11 | `taxonomy.md` | Failure taxonomy from 50 real traces (open coding → groups). | Seeded from the MAST paper, grounded in your traces. |
| 11 | `scenarios/` | 20 τ-bench-style scenarios with an expected DB end-state. | Covers RAG questions and MCP tool flows. |
| 11 | `assertions.py`, `judges.py` | Code checks first; one LLM judge validated against your labels (TPR/TNR). | Judge agreement measured. |
| 11 | `runner.py` | pass^k runner (k=4); scorecard output. | `make eval` (or `uv run python -m agent_sprint.evals.runner`) prints a scorecard. |
