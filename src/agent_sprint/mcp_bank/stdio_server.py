"""Day 8 · MCP server over stdio, by hand. No SDK.

WHAT IT MUST DO
    Speak JSON-RPC 2.0 over stdin/stdout well enough that MCP Inspector
    cannot tell it from a real server.

TO BUILD
    [ ] Newline-delimited JSON on stdin; responses on stdout.
    [ ] LOG TO STDERR ONLY. One stray print() to stdout corrupts the stream
        and the failure is baffling. Get this right first.
    [ ] Lifecycle: initialize (protocol version + capabilities), then the
        notifications/initialized notification. Notifications have no id and
        get no response -- handle that distinction explicitly.
    [ ] tools/list with JSON Schema inputSchema per tool.
    [ ] tools/call returning content blocks, with isError for tool failures.
        Note the difference between a JSON-RPC error and a tool error, and
        write it in this docstring once you are sure.
    [ ] Tools over the SQLite bank at settings.bank_db_path:
        get_customer, list_transactions.
    [ ] resources/list and resources/read over the policy corpus.
    [ ] JSON-RPC error codes for the real cases: parse error, method not
        found, invalid params.

DONE WHEN
    MCP Inspector connects, lists your tools and resources, and calls them.

READ
    https://www.jsonrpc.org/specification
    https://modelcontextprotocol.io/specification/latest/basic/lifecycle
    https://modelcontextprotocol.io/specification/latest/basic/transports
"""
