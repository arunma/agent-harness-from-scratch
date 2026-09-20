"""Day 6 · Parse the MAS corpus into structured documents.

WHAT IT MUST DO
    Turn the PDFs in data/corpus/ into layout-aware structure: sections in
    reading order, tables as tables, page numbers preserved.

TO BUILD
    [ ] uv sync --group w2-rag. Parse with Docling.
    [ ] Keep, per element: section path (heading hierarchy), page number,
        character offsets into the source, element type.
    [ ] Tables survive as tables. A flattened table is a retrieval bug you
        will not find until Day 7.
    [ ] Deterministic doc_id, plus a content hash for Day 7 lifecycle work.
    [ ] Cache parses to disk. Docling is slow; do not re-parse on every run.

COMPARISON (today's number)
    One table-heavy MAS PDF: Docling vs Claude's native PDF input. Same
    document, same question. Report what each one got wrong, and the cost.

DONE WHEN
    You can point at the parse of the worst table in the corpus and say
    which approach you would ship.

READ
    https://docling-project.github.io/docling/
    https://docs.claude.com/en/docs/build-with-claude/pdf-support
"""
