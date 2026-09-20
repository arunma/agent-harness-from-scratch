"""Day 6 · Structured extraction per document, with a review queue.

WHAT IT MUST DO
    Pull the fields a regulated search needs to filter on, and refuse to
    index anything it could not extract confidently.

TO BUILD
    [ ] A Pydantic model per document: issuer, notice number, effective
        date, applicability, superseded_by, obligations.
    [ ] Fill it with structured outputs against the parsed text.
    [ ] Validate. Failures go to a review queue, never to the index.
    [ ] Decide what is fatal (no effective date) and what is tolerable
        (missing applicability). Write the rule down.
    [ ] Record the validation failure rate. That number is today's output.

DONE WHEN
    The failure rate is measured, and you have read three failures and know
    whether the parse, the schema or the model was at fault.

WATCH OUT
    Extracted dates drive Day 7 supersession. A silently wrong effective
    date means citing a withdrawn notice as current.

READ
    https://docs.claude.com/en/docs/build-with-claude/structured-outputs
"""
