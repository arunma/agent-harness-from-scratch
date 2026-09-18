# memory/ — learn zone

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 10 | `store.py` | A `MemoryStore` interface: add, search, consolidate, forget. | Your own implementation reuses the Day 6 embeddings. |
| 10 | `tasks.py` | File-backed task DAG with `blockedBy`; survives a kill. | Resumes mid-task. |
| 10 | `../adapters/mem0_store.py` etc. | Two adopted backends behind the same interface. | Temporal query and PDPA deletion tests pass on both. |
