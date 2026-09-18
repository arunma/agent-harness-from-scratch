"""Settings loaded from .env (plumbing zone).

Usage:
    from agent_sprint.config import settings
    settings.vllm_chat_url
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    # Frontier model
    anthropic_api_key: str = field(default_factory=lambda: _env("ANTHROPIC_API_KEY"), repr=False)
    agent_model: str = field(default_factory=lambda: _env("AGENT_MODEL", "claude-sonnet-5"))
    judge_model: str = field(default_factory=lambda: _env("JUDGE_MODEL", "claude-haiku-4-5-20251001"))
    hard_model: str = field(default_factory=lambda: _env("HARD_MODEL", "claude-opus-5"))

    # Workstation (vLLM over Tailscale)
    vllm_api_key: str = field(default_factory=lambda: _env("VLLM_API_KEY"), repr=False)
    vllm_chat_url: str = field(default_factory=lambda: _env("VLLM_CHAT_URL", "http://workstation:8000/v1"))
    vllm_embed_url: str = field(default_factory=lambda: _env("VLLM_EMBED_URL", "http://workstation:8001/v1"))
    vllm_rerank_url: str = field(default_factory=lambda: _env("VLLM_RERANK_URL", "http://workstation:8002/v1"))
    vllm_chat_model: str = field(default_factory=lambda: _env("VLLM_CHAT_MODEL", "qwen3-8b"))
    vllm_embed_model: str = field(default_factory=lambda: _env("VLLM_EMBED_MODEL", "qwen3-embed"))
    vllm_rerank_model: str = field(default_factory=lambda: _env("VLLM_RERANK_MODEL", "bge-rerank"))

    # Mac
    lmstudio_url: str = field(default_factory=lambda: _env("LMSTUDIO_URL", "http://localhost:1234/v1"))
    litellm_url: str = field(default_factory=lambda: _env("LITELLM_URL", "http://localhost:4000"))
    database_url: str = field(default_factory=lambda: _env("DATABASE_URL", "postgresql://sprint:sprint@localhost:5433/sprint"))
    opensearch_url: str = field(default_factory=lambda: _env("OPENSEARCH_URL", "http://localhost:9200"))
    qdrant_url: str = field(default_factory=lambda: _env("QDRANT_URL", "http://localhost:6333"))
    falkordb_url: str = field(default_factory=lambda: _env("FALKORDB_URL", "redis://localhost:6380"))
    langfuse_host: str = field(default_factory=lambda: _env("LANGFUSE_HOST", "http://localhost:3000"))

    # Managed comparisons
    voyage_api_key: str = field(default_factory=lambda: _env("VOYAGE_API_KEY"), repr=False)
    cohere_api_key: str = field(default_factory=lambda: _env("COHERE_API_KEY"), repr=False)

    # Data
    bank_db_path: Path = field(default_factory=lambda: ROOT / _env("BANK_DB_PATH", "data/bank.db"))
    corpus_dir: Path = ROOT / "data" / "corpus"
    golden_dir: Path = ROOT / "data" / "golden"


settings = Settings()
