"""Day 7 · Answers with citations that map to document, page and section.

WHAT IT MUST DO
    Generate an answer from retrieved chunks where every claim points at a
    specific place in a specific version of a specific document.

TO BUILD
    [ ] Pass chunks as documents to the Citations API rather than pasting
        them into the prompt.
    [ ] Map each returned citation back to doc_id, version, page, section
        path -- the metadata chunk.py attached.
    [ ] Render citations in a form a compliance officer would accept.
    [ ] An evidence threshold: below it, answer "not found in policy". An
        agent that always answers is worse than one that sometimes declines.
    [ ] Expose search_policy(query, filters) as a harness tool, with
        effective-date and issuer filters, so Day 12's flows can use it.

DONE WHEN
    Every sentence in an answer is traceable, and a question the corpus does
    not cover returns a refusal rather than a plausible paragraph.

READ
    https://docs.claude.com/en/docs/build-with-claude/citations
"""
