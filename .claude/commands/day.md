---
description: Brief for a sprint day - goals, installs, and the number to produce
argument-hint: <day number, e.g. 6>
---
Read the section for **Day $ARGUMENTS** in `docs/plan.md` (and the week intro above it). Then give Arun a short brief:

1. **Today in three lines:** what he'll understand by evening and what he'll have built.
2. **Install:** the `uv sync --group ...` command for today's dependency group(s), and any service that must be running (Docker services, workstation endpoints, LM Studio, LiteLLM). Offer to check them with `scripts/check_env.py`.
3. **The number:** the one measurement today's experiment must produce, and a one-line prediction he should write down *before* running it.
4. **Where the code goes:** which files under `src/agent_sprint/` he'll create (see that package's README). Don't create them.
5. **Tool verdict:** if there's an adopt slot, remind him of the five verdict questions from the plan.

Keep it under 25 lines. Then ask which block he wants to start with. Don't write learn-zone code.
