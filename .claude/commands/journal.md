---
description: Draft today's journal entry from the day's changes, for Arun to review and revise
argument-hint: [day number, optional]
---
Draft `journal/day-NN.md` for day $ARGUMENTS (if empty, NN is one past the highest existing `journal/day-*.md`; check first).

If `journal/day-NN.md` already exists, say so and stop — never overwrite a file he's already started or finished.

Gather the day's material:
- `git log` and `git diff` for everything touched today, learn zone and plumbing both.
- The conversation this session: what was explained, hinted at, reviewed, and built, and any number he stated as a prediction before running the experiment.
- The relevant day section in `docs/plan.md` for the stated goal, "the number," and (on adopt days) the leader-lens question.

Copy `journal/TEMPLATE.md` and fill in every section as a best-effort first pass:
- **Prediction** — only if he actually stated a number before the experiment in this conversation. Never invent one.
- **Concept** — plain-language explanation, as if to the study group. This is a draft for him to correct, not a final answer.
- **Diagram** — mermaid flowchart of what was actually built; `<br/>` for line breaks inside nodes, not `\n`.
- **Annotated code** — the 10–30 key lines from today's diff, tagged `[SDK]` `[H]` `[P]` `[T]`.
- **The number** — actual results from test/eval output seen this session; if none were run, write `TODO — rerun` rather than guessing.
- **Tool verdict** — only on adopt days; delete the section otherwise.
- **Leader lens** — your best attempt at the day's leader-lens question.
- **Didn't land yet** — anything that errored, was reverted, or he said he'd return to.
- **Questions for tomorrow's quiz** — five questions drawn from today's actual material.

Put this line at the very top of the file, above the title: `> Drafted by Claude on <today's date> — review and revise before it counts.`

Write the file. Then tell Arun in one line what day/topic you drafted and that it needs his review — a drafted entry isn't a finished one.
