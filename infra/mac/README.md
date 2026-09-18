# Mac services

```bash
docker compose -f infra/mac/docker-compose.yml up -d                     # Postgres, OpenSearch, Qdrant
docker compose -f infra/mac/docker-compose.yml --profile memory up -d    # + FalkorDB, on Day 10
```

| Service | URL | Used on |
|---|---|---|
| Postgres + pgvector | `localhost:5433` (user/pass/db `sprint`) | Days 6–7 (alternative index), 10 |
| OpenSearch | `http://localhost:9200` | Days 6–7 |
| Qdrant | `http://localhost:6333` | Day 6 comparison |
| FalkorDB | `localhost:6380` | Day 10 (Graphiti) |
| Langfuse | `http://localhost:3000` | Day 5 onward |

## Langfuse (Day 5)

Langfuse v3 needs several services (Postgres, ClickHouse, Redis, object storage), so use its own compose file rather than this one:

```bash
git clone https://github.com/langfuse/langfuse.git ~/src/langfuse
cd ~/src/langfuse && docker compose up -d        # web UI on http://localhost:3000
```

Create a project in the UI, then put its public and secret keys in `.env` (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`). Full guide: https://langfuse.com/self-hosting

## LiteLLM gateway

```bash
mise run litellm    # wraps: litellm --config docs/workstation/litellm-config.yaml --port 4000
```

`ANTHROPIC_API_KEY` and `VLLM_API_KEY` come from `.env` via mise's `[env]` block in `.mise.toml` — no manual `export` needed once `eval "$(mise activate zsh)"` is in your shell rc (or run `mise exec -- litellm ...` for a one-off).

## Tools installed outside the project venv

These are CLIs you run occasionally; keeping them out of the project avoids dependency clashes. LiteLLM, garak, promptfoo and MCP Inspector are pinned in `.mise.toml` — `mise install` fetches them, `mise ls` shows what's installed.

| Tool | Install | Day |
|---|---|---|
| LiteLLM proxy | `mise install` (`pypi:litellm`, extras `proxy`) | 5, 13 |
| garak | `mise install` (`pypi:garak`) | 14 |
| promptfoo | `mise install` (`npm:promptfoo`) | 14 |
| MCP Inspector | `mise install` (`npm:@modelcontextprotocol/inspector`) | 8 |
| Moonshot | see https://github.com/aiverify-foundation/moonshot | 14 |
| Spec Kit | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` — git-based install, doesn't fit mise's pypi backend cleanly | 16 |
