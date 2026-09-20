"""Day 9 · Tool-definition pinning: the rug-pull defence.

WHAT IT MUST DO
    Notice when an approved server changes what its tools claim to do.

TO BUILD
    [ ] Canonical serialisation of a tool definition -- name, description,
        inputSchema -- then hash it. Key ordering and whitespace must not
        change the hash, or you get false alarms forever.
    [ ] A pin store: server -> tool -> approved hash, on disk.
    [ ] On every connect, re-hash and compare. Decide the response to a
        mismatch: refuse the tool, refuse the whole server, or ask.
    [ ] First-connect approval flow that shows the human the full
        description, including any whitespace-hidden instructions.

ATTACK IT PROVES (Day 9, replayed on Day 14)
    A second server with instructions buried in a tool description, and one
    that changes its description after approval.

DONE WHEN
    The rug-pull is detected and blocked, and you can say what pinning does
    NOT protect against.

READ
    https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
"""
