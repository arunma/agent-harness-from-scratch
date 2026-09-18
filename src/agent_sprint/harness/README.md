# harness/ — learn zone (you write this)

The agent loop and everything around it. Built by hand in Week 1; every later day plugs into it.

| Day | File (suggested) | What it must do | Done when |
|---|---|---|---|
| 1 | `raw_call.py` | One Messages API call with tools over raw `httpx`, printing `tool_use`, `stop_reason`, `tool_result`. | You can explain every field in the response. |
| 1 | `chat_template.py` | Render a tools-enabled chat template with a small open model's tokenizer; hand-parse the tool call. | Journal has the rendered string and token IDs. |
| 1 | `loop.py` | The agent loop: call → tool_use? → execute → append result → repeat. | Rewritten from memory in < 80 lines. |
| 2 | `tools.py` | Tool registry + dispatch map; parallel calls; errors returned as observations. | 10-task × 3-description experiment table. |
| 3 | `permissions.py`, `hooks.py`, `audit.py` | allow / deny / ask rules; `PreToolUse` / `PostToolUse`; append-only JSONL audit. | Memo-injection attack results, with and without each defence. |
| 4 | `planning.py`, `subagent.py` | TodoWrite tool; subagent with fresh `messages[]`. | Single vs multi-agent numbers. |
| 5 | `skills.py`, `context.py`, `tracing.py` | On-demand skills; four-stage compaction; OTel spans. | Traces visible in Langfuse; cache hit rate logged. |

Interfaces are yours to design. `/tests-for <component>` will write failing tests once you've decided the shape.
