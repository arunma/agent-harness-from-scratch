"""Check that every service the sprint uses is reachable (plumbing zone).

    uv run python scripts/check_env.py

Never prints secrets; only whether each one is set.
"""

from __future__ import annotations

import sqlite3

import httpx
from rich.console import Console
from rich.table import Table

from agent_sprint.config import settings

console = Console()


def probe(url: str, headers: dict | None = None) -> tuple[bool, str]:
    try:
        r = httpx.get(url, headers=headers or {}, timeout=4.0)
        return r.status_code < 400, f"HTTP {r.status_code}"
    except httpx.HTTPError as e:
        return False, type(e).__name__


def main() -> None:
    vllm = {"Authorization": f"Bearer {settings.vllm_api_key}"} if settings.vllm_api_key else {}
    checks: list[tuple[str, str, tuple[bool, str], str]] = []

    def add(name: str, where: str, result: tuple[bool, str], hint: str = "") -> None:
        checks.append((name, where, result, hint))

    add("ANTHROPIC_API_KEY", ".env", (bool(settings.anthropic_api_key), "set" if settings.anthropic_api_key else "missing"),
        "Add your key to .env")
    if settings.anthropic_api_key:
        add("Anthropic API", "api.anthropic.com",
            probe("https://api.anthropic.com/v1/models",
                  {"x-api-key": settings.anthropic_api_key, "anthropic-version": "2023-06-01"}),
            "Check the key and network")
    add("vLLM chat", settings.vllm_chat_url, probe(settings.vllm_chat_url + "/models", vllm),
        "Workstation up? Tailscale connected? VLLM_API_KEY matches?")
    add("vLLM embeddings", settings.vllm_embed_url, probe(settings.vllm_embed_url + "/models", vllm), "docker compose ps on the workstation")
    add("vLLM reranker", settings.vllm_rerank_url, probe(settings.vllm_rerank_url + "/models", vllm), "docker compose ps on the workstation")
    add("LM Studio", settings.lmstudio_url, probe(settings.lmstudio_url + "/models"), "Start the server in LM Studio (Developer tab)")
    add("LiteLLM gateway", settings.litellm_url, probe(settings.litellm_url + "/health/liveliness"),
        "litellm --config docs/workstation/litellm-config.yaml --port 4000")
    add("OpenSearch", settings.opensearch_url, probe(settings.opensearch_url), "docker compose -f infra/mac/docker-compose.yml up -d")
    add("Qdrant", settings.qdrant_url, probe(settings.qdrant_url + "/healthz"), "docker compose -f infra/mac/docker-compose.yml up -d")
    add("Langfuse", settings.langfuse_host, probe(settings.langfuse_host + "/api/public/health"), "See infra/mac/README.md")

    try:
        con = sqlite3.connect(f"file:{settings.bank_db_path}?mode=ro", uri=True)
        n = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        add("Synthetic bank", str(settings.bank_db_path), (True, f"{n} transactions"))
    except sqlite3.Error:
        add("Synthetic bank", str(settings.bank_db_path), (False, "not found"), "uv run python scripts/seed_bank.py")

    table = Table(title="Sprint environment")
    for col in ("Service", "Where", "Status", "If red"):
        table.add_column(col)
    for name, where, (ok, detail), hint in checks:
        table.add_row(name, where, f"[green]✓ {detail}[/]" if ok else f"[red]✗ {detail}[/]", "" if ok else hint)
    console.print(table)
    console.print("[dim]Postgres is checked on Day 6 when the w2-rag group (psycopg) is installed.[/]")


if __name__ == "__main__":
    main()
