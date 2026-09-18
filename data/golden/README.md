# Golden set (Day 6)

Suggested format, one JSON object per line in `golden.jsonl`:

```json
{"id": "q001", "question": "How long does a customer have to raise a card dispute?", "relevant_chunk_ids": ["..."], "notes": "tests section-level retrieval"}
```

Aim for 30 questions: a mix of exact-term lookups (BM25 should win), paraphrases (dense should win), table lookups, and at least three questions whose answer changed between document versions.
