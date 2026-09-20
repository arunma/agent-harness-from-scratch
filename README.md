# agent-harness-from-scratch

A three-week, hands-on sprint on building LLM agents for a regulated setting: the harness from scratch, production RAG, MCP by hand, memory, evals, inference economics, security and governance, and finally an AI-driven engineering culture playbook. The throughline is one capstone: a **Dispute & Ops Agent for a synthetic digital bank**.

- **The plan:** open `docs/plan.html` in a browser (tables, links, tick-boxes that remember your progress). `docs/plan.md` is the same plan for Claude Code and editors.
- **Workstation (RTX 5090) setup:** `docs/workstation/vllm-workstation-setup.md`.

## What this is (and isn't)

This is a **personal, curated learning path** — not original research or a production framework. The daily structure follows [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) for the harness build order (`s01_agent_loop` through `s17_goal_loop`); the rest of the reading list is credited inline in `docs/plan.md`. All code under `src/agent_sprint/` is written by hand against those references — copy the plan, not the answers.

## Quick start (Mac Studio)

`main` moves forward as each day's work lands, so it won't always match the plan's starting point. `v0.1.0` is the scaffold before any day's code exists — stub files only, each with what to build and nothing more — so check that out if you want the same blank slate.

```bash
# 1. Tools
brew install uv mise       # or: curl -LsSf https://astral.sh/uv/install.sh | sh
# Docker (OrbStack or Docker Desktop), LM Studio, Tailscale, Claude Code

# 2. Project
git clone https://github.com/arunma/agent-harness-from-scratch.git
cd agent-harness-from-scratch
git checkout v0.1.0        # optional: the pre-Day-1 scaffold, instead of main's latest
cp .env.example .env       # fill in keys yourself
mise trust && mise install # python 3.12, node, litellm, garak, promptfoo, MCP Inspector — see .mise.toml
uv sync                    # core + dev only; later groups arrive day by day

# 3. Let Claude Code do the plumbing
claude
> /setup
```

Add `eval "$(mise activate zsh)"` to your `~/.zshrc` once — mise then loads `.env` and puts the tools above on `PATH` per directory, so you never `export ANTHROPIC_API_KEY=...` by hand before running `litellm` or `garak`.

`/setup` starts the Mac services, seeds the synthetic bank, checks every endpoint (Anthropic, vLLM on the workstation, LM Studio, LiteLLM, OpenSearch, Qdrant, Langfuse) and runs the smoke tests. It doesn't touch the code you'll write.

## Working with Claude Code without it doing the learning for you

`CLAUDE.md` splits the repo into zones:

| Zone | Where | Who writes it |
|---|---|---|
| **Learn** | `src/agent_sprint/**` (except `config.py`) | **You.** Claude explains, hints, reviews and writes failing tests, but doesn't write the implementation unless you explicitly ask. |
| **Plumbing** | `scripts/`, `infra/`, `docs/`, `config.py`, `tests/test_smoke.py`, `.claude/` | Claude may write freely. |
| **Journal** | `journal/` | Claude drafts the day's entry (`/journal`) from the diff and conversation; you review and revise it before it counts. |

Commands (in `.claude/commands/`):

| Command | What it does |
|---|---|
| `/setup` | One-time environment setup (plumbing). |
| `/day 6` | Brief for the day: goals, installs, the number to produce, which files you'll create. |
| `/hint 2 <problem>` | Hint ladder: 1 nudge · 2 pointer to docs · 3 pseudocode · 4 small snippet. |
| `/review` | Reviews your uncommitted changes; describes fixes, doesn't apply them. |
| `/tests-for <component>` | Failing tests that pin down behaviour for the interface *you* designed. |
| `/explain <concept>` | Concept first, then a worked example with real numbers. |
| `/quiz 5` | Five questions from your journal; grades your answers. |
| `/journal` | Drafts today's `journal/day-NN.md` from the day's diff and conversation. You review and revise it. |

Claude Code also has a built-in **Learning** output style that leaves `TODO(human)` gaps for you to fill; it pairs well with these rules if you want it (see Claude Code's output-style settings).

`.claude/settings.json` blocks Claude from reading or editing `.env`.

## Daily loop

1. `claude` → `/quiz` on yesterday, then `/day N`.
2. Write your prediction for today's number before you run the experiment.
3. Install the day's group, e.g. `uv sync --group w2-rag` (groups are cumulative: add each new `--group`, or use `uv sync --all-groups` once you've reached Week 3).
4. Read → build → adopt → read, per `docs/plan.html`. Use `/hint`, `/explain`, `/review` as you go.
5. `/journal` to get a draft of today's entry, then review and revise it yourself. Commit.

## Dependency groups (staged by day)

| Group | Day | Main packages |
|---|---|---|
| *(core)* | 1 | anthropic, httpx, openai, pydantic, python-dotenv, rich, typer |
| `w1-tokens` | 1 | transformers, tokenizers |
| `w1-structured` | 2 | instructor |
| `w1-guardrails` | 3 | nemoguardrails |
| `w1-tracing` | 5 | langfuse, langsmith, opentelemetry |
| `w2-rag` | 6–7 | docling, opensearch-py, qdrant-client, psycopg, pgvector, tiktoken, voyageai, cohere, presidio, ragas |
| `w2-mcp` | 8–9 | mcp, fastmcp, starlette, uvicorn |
| `w2-memory` | 10 | mem0ai, graphiti-core, letta-client, langmem |
| `w3-evals` | 11 | inspect-ai |
| `w3-frameworks` | 12 | langgraph, claude-agent-sdk, openai-agents, pydantic-ai |
| `w3-security` | 14 | agentdojo |

CLIs that live outside the venv — LiteLLM proxy, garak, promptfoo, MCP Inspector — are pinned in `.mise.toml` (`mise install`); Spec Kit's git-based install doesn't fit mise cleanly and stays manual, see `infra/mac/README.md`. Google ADK is left out of the lock on purpose; if you pick it for Day 12, `uv add --group w3-frameworks google-adk`.

`uv.lock` is uv's universal lockfile, so the same file covers macOS and Linux. If a package misbehaves on Apple Silicon, `uv lock --upgrade-package <name>` and re-sync.

## Layout

```
agent-harness-from-scratch/
├── CLAUDE.md / AGENTS.md        zone rules for coding agents
├── .mise.toml                   tool versions, .env loading, litellm task
├── .claude/                     commands + permissions
├── docs/                        plan (html + md), workstation guide and configs
├── infra/mac/                   docker compose for Postgres, OpenSearch, Qdrant, FalkorDB
├── scripts/                     seed_bank.py, check_env.py
├── src/agent_sprint/
│   ├── config.py                settings from .env (plumbing)
│   ├── harness/  rag/  mcp_bank/  memory/
│   ├── evals/  security/  workflows/  adapters/     ← you write these (each has a README)
├── data/                        bank.db, corpus/, golden/ (git-ignored)
├── journal/                     TEMPLATE.md + your daily notes
├── notebooks/
└── tests/
```
