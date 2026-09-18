---
description: Get a hint using the hint ladder (1 nudge, 2 pointer, 3 shape, 4 snippet)
argument-hint: [level 1-4] <what you're stuck on>
---
Arun is stuck: $ARGUMENTS

Use the hint ladder from CLAUDE.md. If the first word is a number 1–4, give a hint at exactly that level; otherwise give a level-1 hint.

- Level 1 — a question or the concept name he's missing.
- Level 2 — the exact doc section, lesson file or reference-repo location (use the links in `docs/plan.md`).
- Level 3 — pseudocode or numbered steps, no real syntax.
- Level 4 — at most ~10 lines of real code for the single piece he's stuck on.

Read the relevant file(s) first so the hint fits his actual code. Don't edit files. End by telling him the next level is available if he wants it.
