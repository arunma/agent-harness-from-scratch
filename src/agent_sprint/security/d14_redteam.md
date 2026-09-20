# Red-team results

> Day 14. Every finding maps to an OWASP agentic category.

## Setup

- Target: (which commit, which defences enabled)
- Date:
- Tools: garak · promptfoo red team · Moonshot · AgentDojo (banking suite)

## Per-tool runs

For each: command, config, what it probed, what it found, false positives.

### garak

### promptfoo

### Moonshot (AI Verify Foundation)

### AgentDojo — banking suite

Report **utility** and **attack success rate**, with and without your defences
at the tool-execution seam. Utility alone is the trap: a defence that blocks
every attack and half the legitimate work is not a defence.

| Config | Utility | Attack success rate |
|---|---|---|
| No defences | | |
| Defences on | | |

## Your own attacks, replayed

| Attack | Baseline ASR | With defences | Which defence moved it |
|---|---|---|---|
| Memo injection (Day 3) | | | |
| RAG poisoning (Day 7) | | | |
| MCP tool poisoning (Day 9) | | | |

## Findings

One row per finding: severity, what it is, OWASP Top 10 for Agentic
Applications (2026) category, whether it is fixed, and if not, why not.

## What I could not test

Honest list. This is the section a reviewer reads first.
