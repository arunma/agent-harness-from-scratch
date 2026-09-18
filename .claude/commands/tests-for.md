---
description: Write failing pytest tests that specify a component's behaviour (not the implementation)
argument-hint: <component, e.g. "permission engine" or "RRF fusion">
---
Arun wants tests for: $ARGUMENTS

1. Ask him (briefly) for the interface he intends — function or class names and signatures — unless it already exists in `src/agent_sprint/`. Don't invent the design for him.
2. Write tests under `tests/` that specify behaviour: the happy path, edge cases, and at least one failure mode that matters for a bank (e.g. a denied action, a restricted document, a malformed tool call).
3. Tests must fail right now for the right reason (missing or unimplemented code), not because of test bugs. Run `uv run pytest <file> -q` to confirm.
4. Don't write any implementation code. Summarise what each test pins down in one line.
