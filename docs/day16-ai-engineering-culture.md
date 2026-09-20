# Day 16 — Building an AI-driven engineering culture

> The EM track. Two-page playbook plus the artefacts. Written last, because
> you can only lead this credibly after building agents yourself.

## What the evidence actually says

- DORA 2025 + AI Capabilities Model — the seven capabilities that amplify
- DORA ROI (2026) — the J-curve and the early dip
- METR — perceived vs measured speed-up
- Anthropic — how their own teams use Claude Code

Three things that contradicted your priors:

## Artefacts built today

### Context file

`CLAUDE.md` for a bank engineering repo: conventions, test commands,
forbidden actions (no customer data in prompts, no secrets, no direct prod
access). Where does it live, who owns it, how does it stay true?

### Two team skills

1. Banking PR review — PII in logs, idempotency, audit trail, rollback
2. (incident or migration runbook)

### The plugin

Skills + a hook blocking commits with secrets or failing tests + a slash
command + the Day 9 MCP server, published to a private marketplace repo.

Rollout proof: installed on the 5090 box as a clean machine. What broke?

## Spec-driven development trial

Spec Kit end to end on one small capstone feature: constitution → specify →
plan → tasks → implement, with EARS-style acceptance criteria. Then a
comparable feature with no spec.

| | With spec | Without |
|---|---|---|
| Time to first working version | | |
| Review effort | | |
| Rework after review | | |

Verdict, and where the spec overhead stopped paying.

## The playbook

### Adoption path

Pilot team → champions → paved road (shared marketplace, templates) → org
default. What triggers each step?

### Guardrails

- Which repos and data classes may touch which models, hosted where
- "You commit it, you own it"
- Mandatory human review of AI-authored PRs
- AI-generated code stays inside MAS TRM SDLC controls

### Metrics

DORA four keys segmented by AI-assisted vs not; change-failure rate and
rework on AI PRs; review latency.

**Explicitly not measured:** lines of code, suggestion acceptance rate. Write
down why, because someone will ask for them.

### People

Protecting how juniors learn. Office hours and pairing. Recognising
contributors to the shared marketplace.

### Expectation-setting

The J-curve conversation with executives, in the words you would actually
use.

## Retro

What surprised you in DORA and METR versus your own 16 days.

## Leader lens

AI amplifies whatever system it lands in. Fix the platform, CI, tests and
review culture first; the tooling rollout is the easy part.
