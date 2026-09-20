"""Day 7 · Documents change under you. Supersession and deletion.

WHAT IT MUST DO
    Re-ingest an amended notice so the old one stops being cited, and delete
    a document so completely you can prove it.

TO BUILD
    [ ] Re-ingest: new version indexed, old version marked superseded.
        Decide whether superseded chunks are removed or kept-but-filtered --
        an auditor may need "what did the policy say in March?".
    [ ] Retrieval defaults to current-as-of-now; an explicit as-of date
        overrides it.
    [ ] Deletion removes the chunks from the index AND from every cache,
        embedding store and derived artefact. Enumerate those before you
        start; the list is longer than it looks.
    [ ] A verification query for each: the superseded notice is no longer
        cited; the deleted document returns nothing anywhere.

DONE WHEN
    Both proofs run as tests. This is PDPA, and it is the first thing an
    auditor asks for.
"""
