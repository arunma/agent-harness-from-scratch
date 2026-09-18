.PHONY: sync services seed check test eval lint

sync:            ## core + dev dependencies
	uv sync

services:        ## start Mac services
	docker compose -f infra/mac/docker-compose.yml up -d

seed:            ## (re)create the synthetic bank
	uv run python scripts/seed_bank.py

check:           ## check every endpoint the sprint uses
	uv run python scripts/check_env.py

test:
	uv run pytest -q

eval:            ## Day 11: your eval runner prints the scorecard
	uv run python -m agent_sprint.evals.runner

lint:
	uv run ruff check src scripts tests
