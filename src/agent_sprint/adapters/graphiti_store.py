"""Day 10 · Graphiti (temporal knowledge graph) behind MemoryStore.

WHAT IT MUST DO
    Second backend for the same interface, with a fundamentally different
    data model -- a graph with valid-time edges rather than embedded notes.

TO BUILD
    [ ] FalkorDB or Neo4j from infra/mac/docker-compose.yml
        (settings.falkordb_url).
    [ ] Same interface, same two tests.
    [ ] The temporal query is where this model should win. Check whether it
        does, and what it costs in latency and ingestion time.

TOOL VERDICT (journal)
    Five questions. Plus: which of the two backends would you run in a bank,
    and is the answer about capability or about operability?
"""
