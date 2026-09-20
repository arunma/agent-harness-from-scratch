# Governance mapping

> Day 14. Two pages a CRO could read. Every control traced from the code up.

## Scope

What the agent does, what data it touches, what it can change without a human.

## Control mapping

One row per control that exists in this repo. No aspirational rows.

| Control | Where it lives | IMDA Agentic AI dimension | MAS materiality lens (impact / complexity / reliance) | Evidence |
|---|---|---|---|---|
| Permission engine (allow/deny/ask) | `harness/permissions.py` | | | |
| Pre/PostToolUse hooks | `harness/hooks.py` | | | |
| Append-only audit log | `harness/audit.py` | | | |
| Context policy / data minimisation | `harness/context.py` | | | |
| Tracing and retention | `harness/tracing.py` | | | |
| RAG entitlement filter | `rag/guard.py` | | | |
| PII redaction at ingest | `rag/guard.py` | | | |
| Supersession and deletion | `rag/lifecycle.py` | | | |
| MCP scopes | `mcp_bank/http_server.py` | | | |
| MCP tool pinning | `mcp_bank/pinning.py` | | | |
| Human approval on writes | | | | |
| Eval gate before release | `evals/runner.py` | | | |

**Evidence** means a test, a log line or a scorecard — not a paragraph.

## Irreversible actions

Every action the agent can take that cannot be undone, and the gate on each.
A prompt is not a gate.

## Data

- What leaves the machine, and to where
- Where traces containing customer data may legally live
- Retention and deletion, and how deletion is proved (PDPA)

## Residual risk

What is still open, who would own it, and what it would cost to close.

## Sources

- IMDA Model AI Governance Framework for Agentic AI
- CSA *Securing Agentic AI* + Addendum
- MAS Guidelines on AI Risk Management
- MAS Technology Risk Management Guidelines
