"""Day 9 · Streamable HTTP transport, sessions and scopes.

WHAT IT MUST DO
    Serve the same tools remotely, with server-side authorisation that the
    client cannot talk its way past.

TO BUILD
    [ ] Starlette or FastAPI. POST for JSON-RPC; streamed responses where
        the spec calls for them.
    [ ] Session handling via the session header: issue, validate, expire.
    [ ] Bearer tokens carrying scopes: disputes:read, disputes:write.
    [ ] Scope checks SERVER-SIDE, per tool. The client's approval UI is not
        a security control.
    [ ] open_dispute: a write tool requiring human approval in the harness
        AND disputes:write on the server. Two independent gates.
    [ ] Reject the confused-deputy cases the spec's security page lists.
    [ ] Walk the OAuth 2.1 flow on paper; note in the journal which parts
        you stubbed and what that would cost in production.

DONE WHEN
    A token without disputes:write is refused by the server even when the
    harness would have allowed the call.

READ
    https://modelcontextprotocol.io/specification/latest/basic/authorization
    https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch15-mcp.md -- the host side of what you are serving: transport
        taxonomy, OAuth discovery chain, connection states, session-expiry
        detection. The parts the spec leaves to the implementer.
"""
