"""Day 3 · PreToolUse / PostToolUse hooks.

WHAT IT MUST DO
    Give you a seam to observe, block or rewrite a tool call without editing
    the tool or the loop.

TO BUILD
    [ ] PreToolUse: sees tool name and arguments; may allow, block with a
        message, or return modified arguments.
    [ ] PostToolUse: sees the result; may redact or annotate it before it
        reaches the model.
    [ ] Registration by tool name and by wildcard.
    [ ] A hook that raises must not take down the loop. Decide -- and write
        down -- whether a broken hook fails open or closed.
    [ ] Ordering when several hooks match the same tool.
    [ ] Today's defensive use: a PostToolUse hook that scans returned text
        for injected instructions before the model reads it.

DONE WHEN
    The Day 3 attack results table has a row for "hook filtering" that is
    measurably different from the prompt-hardening row.

WATCH OUT
    Hooks are where "the agent did X" becomes provable. Keep the interface
    narrow; every later day wants to hang something off it.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s04_hooks
"""
