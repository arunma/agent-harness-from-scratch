# mcp_bank/ — learn zone (Day 8 entirely by hand, no SDK)

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 8 | `d08_stdio_server.py` | JSON-RPC 2.0 over stdin/stdout: `initialize`, `notifications/initialized`, `tools/list`, `tools/call`, `resources/list`, `resources/read`. Logs to stderr only. | MCP Inspector lists and calls your tools. |
| 8 | `d08_client.py` | Spawn the server, handshake, translate MCP tools to Anthropic tool definitions, route `tool_use` → `tools/call`. | Your harness uses the bank tools through MCP. |
| 9 | `d09_http_server.py` | Streamable HTTP transport, sessions, scope checks, approval-gated `open_dispute`. | Scope violations rejected server-side. |
| 9 | `d09_pinning.py` | Hash approved tool definitions; refuse changed descriptions (rug-pull). | Malicious second server detected. |
| 9 | `d09_fastmcp_server.py` | The same server with FastMCP, for comparison. | Line count and "what the SDK hides" in the journal. |

Data source: the SQLite bank from `scripts/seed_bank.py` (`settings.bank_db_path`).
