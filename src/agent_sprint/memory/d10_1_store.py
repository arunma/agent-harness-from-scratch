"""Day 10 · MemoryStore: selection, extraction, consolidation, forgetting.

WHAT IT MUST DO
    Give the agent memory across runs, behind an interface narrow enough
    that two adopted backends can sit behind it unchanged.

TO BUILD
    [ ] The interface first: add, search, consolidate, forget. Design it
        before you look at Mem0's API, or you will inherit their model.
    [ ] Your own implementation, reusing the Day 6 embeddings and index.
    [ ] Selection: what is worth remembering from a run. Not everything.
    [ ] Extraction: turn a transcript into memory items with a subject
        (customer? account? user?) you can later delete by.
    [ ] Consolidation: merge or supersede contradicting memories. "Customer
        moved house" must beat "customer lives at the old address".
    [ ] Retrieval scored on more than similarity -- recency and importance
        matter (Generative Agents).
    [ ] forget(subject) that actually removes, across every derived store.
    [ ] Baseline to beat: the same four operations over Markdown files with
        frontmatter and one always-loaded index file -- no embeddings at
        all. If your vector version doesn't win on the temporal query, the
        embeddings are decoration.

DONE WHEN
    A temporal query ("address changed last month -- which is current?") and
    a PDPA deletion both pass against your implementation.

READ
    https://arxiv.org/abs/2310.08560   (MemGPT)
    https://arxiv.org/abs/2304.03442   (Generative Agents: recency,
                                        importance, relevance)
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch11-memory.md -- the file-based baseline above as one harness
        actually ships it: four-type taxonomy, write and recall paths,
        staleness, MEMORY.md as the always-loaded index.
"""
