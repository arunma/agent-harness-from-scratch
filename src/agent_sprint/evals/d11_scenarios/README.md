# d11_scenarios/ — Day 11

Twenty tau-bench-style scenarios, written by hand. The eval set *is* the spec.

Each scenario needs, at minimum:

- **id** and a one-line description
- **initial state** — what the bank database looks like before the run
- **user input** — the request, and any follow-up turns if it is multi-turn
- **expected end state** — the rows that must exist in the database afterwards
- **required / forbidden tool calls**
- **assertions** — which checks from `d11_assertions.py` apply
- **judge rubric** — only for what code cannot check

Pick the format (JSON, YAML, Python) before you write the second one.

Coverage to hit:

- RAG questions reusing the Day 6 golden set, including one whose answer is *not* in the corpus
- MCP tool flows through the Day 8/9 server, including a scope violation
- The approval gate on `open_dispute`
- At least one scenario per category in `d11_taxonomy.md`
- At least one injection attempt from `security/attacks/`
