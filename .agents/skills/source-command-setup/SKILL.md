---
name: "source-command-setup"
description: "One-time environment setup for the sprint (plumbing zone only)"
---

# source-command-setup

Use this skill when the user asks to run the migrated source command `setup`.

## Command Template

Set up this repo for the sprint. This is plumbing: you may run commands and write files in `scripts/`, `infra/` and `docs/`, but do not create or edit anything in `src/agent_sprint/` except `config.py`. Do not read or print `.env`.

Work through these steps, reporting each result briefly and stopping to ask if anything fails:

1. Confirm `uv --version` and `mise --version` work. Run `mise trust && mise install` (installs the tool versions and CLIs pinned in `.mise.toml`: litellm, garak, promptfoo, MCP Inspector), then `uv sync` (core + dev only; later groups are installed per day).
2. If `.env` doesn't exist, copy `.env.example` to `.env` and tell Arun which keys he must fill in himself. Don't ask him to paste secrets into chat.
3. Start local services: `docker compose -f infra/mac/docker-compose.yml up -d`, then `docker compose -f infra/mac/docker-compose.yml ps`.
4. Tell Arun how to start Langfuse (see `infra/mac/README.md`); don't clone or start it unless he asks.
5. Seed the synthetic bank: `uv run python scripts/seed_bank.py`.
6. Run `uv run python scripts/check_env.py` and show the table. For anything failing, explain the likely cause (see `docs/workstation/vllm-workstation-setup.md` for the workstation) and suggest the fix.
7. Run `uv run pytest -q`.
8. Finish with a short checklist of what's green, what's red, and what Arun needs to do by hand.
