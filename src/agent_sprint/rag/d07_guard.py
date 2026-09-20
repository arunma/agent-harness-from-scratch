"""Day 7 · RAG guardrails: entitlements, PII, injection, grounding.

WHAT IT MUST DO
    Make it structurally impossible for the wrong chunk to reach the prompt,
    and catch the ones that reach it carrying instructions.

TO BUILD
    [ ] Entitlement filter IN THE QUERY, not after retrieval. Post-filtering
        means the restricted chunk was already retrieved, scored and, in a
        sloppy pipeline, logged.
    [ ] PII redaction at ingestion with Presidio. Decide what is redacted
        and what is masked-but-searchable.
    [ ] Injection scan of retrieved chunks before they enter the prompt.
        A planted policy document is Day 14's rag_poisoning attack.
    [ ] Grounding check on the generated answer against the retrieved text.
    [ ] The "not found" threshold shared with d07_answer.py.

DONE WHEN
    A test proves a restricted chunk never reaches the prompt -- not that it
    was filtered from the output, that it never got that far.

READ
    https://github.com/microsoft/presidio
    https://docs.nvidia.com/nemo/guardrails/   (retrieval rails)
"""
