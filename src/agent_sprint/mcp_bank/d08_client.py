"""Day 8 · MCP client by hand. Your harness becomes an MCP host.

WHAT IT MUST DO
    Spawn the server, complete the handshake, and make its tools
    indistinguishable from native tools to d01_loop.py.

TO BUILD
    [ ] Spawn d08_stdio_server.py as a subprocess; own its stdin/stdout, and
        surface its stderr somewhere you will actually read.
    [ ] Handshake: initialize -> read result -> send notifications/initialized.
    [ ] Request ids you generate and match responses against. Do not assume
        responses arrive in order.
    [ ] Translate MCP inputSchema into Anthropic tool definitions. Namespace
        the names so two servers cannot collide.
    [ ] Route tool_use -> tools/call, and MCP content blocks back into
        tool_result.
    [ ] Wire-tap: log every message in both directions, with direction and
        timestamp. The journal wants the sequence diagram.
    [ ] Shutdown: close stdin, wait, then kill. A leaked server process per
        run will bite you by Day 11.

DONE WHEN
    Your Day 1 loop calls bank tools through MCP without knowing MCP exists,
    and the journal has the handshake sequence diagram drawn from your log.
"""
