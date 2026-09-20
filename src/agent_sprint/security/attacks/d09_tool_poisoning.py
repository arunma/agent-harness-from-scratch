"""Day 9 · Malicious MCP server, and the rug-pull.

WHAT IT MUST DO
    Show that trusting a tool description is trusting a stranger, and that
    pinning is the only thing standing between you and a silent swap.

TO BUILD
    [ ] Server A: instructions hidden in a tool description at first
        connect. Try the places a review UI truncates -- long descriptions,
        trailing whitespace, unicode.
    [ ] Server B: benign at approval, malicious on the next tools/list.
        That is the rug-pull.
    [ ] A cross-server attack: a tool on one server whose description tells
        the model to call a tool on another.
    [ ] Measure with and without d09_pinning.py.

DONE WHEN
    Pinning blocks the rug-pull, and you can name the attack it does not
    block.

READ
    https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
"""
