# AGENTS.md

This is a learning repository. Read `CLAUDE.md` — its zone rules apply to every coding agent:
agents may write plumbing (`scripts/`, `infra/`, `docs/`, config), but must not write implementation
code under `src/agent_sprint/` (except `config.py`) unless the human explicitly asks. Offer hints,
reviews and failing tests instead. Never edit `journal/`. Never read or print `.env`.
