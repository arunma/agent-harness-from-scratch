"""Day 3 · The permission engine: allow / deny / ask.

WHAT IT MUST DO
    Decide, before a tool runs, whether it may run -- from the tool name and
    its arguments, never from the model's stated intent.

TO BUILD
    [ ] Three outcomes: allow, deny (with a reason the model sees), ask
        (block for a human).
    [ ] Rules matched on tool name plus argument shape. write_file into
        runs/ and write_file into .env are different decisions.
    [ ] Rules are data, not code paths. Config in, decision out.
    [ ] Decide precedence -- first match wins? most specific wins? -- and
        write it in this docstring once you have chosen. Default is deny.
    [ ] An ask decision needs a real prompt and a recorded answer. A
        remembered "always allow" is itself an auditable event.
    [ ] Decisions testable with no model in the loop.

DONE WHEN
    You can express "read anything under data/, never write outside runs/,
    always ask before open_dispute" as rules, with a test for each.

WATCH OUT
    The engine sees arguments the model wrote. Path traversal, symlinks, and
    SQL that reads like a SELECT but is not, are yours to catch.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s03_permission
    https://genai.owasp.org/llm-top-10/  (LLM06 Excessive Agency)
"""
