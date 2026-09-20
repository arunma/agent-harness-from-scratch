"""Day 3 · Append-only JSONL audit log.

WHAT IT MUST DO
    Record what the agent did, in a form a compliance reviewer could read
    six months later without the code in front of them.

TO BUILD
    [ ] One JSON object per line. Append only -- never rewrite, never
        truncate.
    [ ] Per event: timestamp (UTC, ISO 8601), run id, turn number, tool name,
        arguments, permission decision and which rule made it, hook actions,
        result summary, duration, token usage.
    [ ] A run id that ties every line of one agent run together.
    [ ] Decide what must never land in the log: secrets, full PII, raw
        customer data. Redact at write time, not at read time.
    [ ] Readable back into a per-run timeline with a few lines of code.

DONE WHEN
    You can answer "what did the agent do to account X on Tuesday, and who
    approved it?" from the log alone.

FEEDS
    Day 5 tracing exports the same events to Langfuse. Day 11 mines 50 of
    these runs for the failure taxonomy. Day 14 cites this file in the
    governance mapping. Pick fields today that survive all three.
"""
