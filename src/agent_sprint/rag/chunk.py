"""Day 6 · Structure-aware chunking.

WHAT IT MUST DO
    Split on the document's own structure, not on a character count, and
    carry enough metadata that a chunk can be cited and filtered.

TO BUILD
    [ ] Split on parsed sections. Sub-split only when a section exceeds the
        budget, and then at a boundary the document itself provides.
    [ ] Every chunk carries: doc_id, version, section path, page, character
        offsets, effective date, access level.
    [ ] Never split a table across chunks.
    [ ] Decide overlap policy and justify it against your golden set, not
        against a blog post.
    [ ] Contextual retrieval: a short document-level context prefix per
        chunk (Day 7 compares LLM-written context vs contextual embeddings).

DONE WHEN
    Every chunk can be traced back to document, page and section, and a
    citation rendered from it would satisfy an auditor.

READ
    https://www.anthropic.com/news/contextual-retrieval
"""
