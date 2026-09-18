"""Smoke tests for the plumbing only (config and seed data)."""

import sqlite3

from agent_sprint.config import settings


def test_settings_load():
    assert settings.agent_model
    assert settings.vllm_chat_url.startswith("http")


def test_seeded_bank_has_data():
    if not settings.bank_db_path.exists():
        import pytest

        pytest.skip("Run scripts/seed_bank.py first")
    con = sqlite3.connect(settings.bank_db_path)
    assert con.execute("SELECT COUNT(*) FROM customers").fetchone()[0] > 0
    assert con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] > 0
