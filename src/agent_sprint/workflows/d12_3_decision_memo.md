# Workflow or agent? A memo for a regulated flow

> Day 12. One page. Write it after the numbers, not before.

## The comparison

Same flow, same tools, same eval suite. Only the control flow differs.

| | LangGraph workflow | Free agent |
|---|---|---|
| pass^k (k=4) | | |
| Cost per task | | |
| p50 / p95 latency | | |
| Tokens per task | | |
| Auditability | | |
| Behaviour on the unexpected case | | |

## Where each one broke

Not the aggregate — the specific failures, and which taxonomy category each
belongs to.

## The rule

When is a regulated flow a workflow, and when is it an agent? State it as a
test someone else could apply to a flow you have never seen.

## The hybrid

Which parts of this flow are fixed and which are genuinely open-ended. Most
real systems are a graph with one agentic node; say where that node belongs
here.

## What would change my mind

The number that would move this decision the other way.
