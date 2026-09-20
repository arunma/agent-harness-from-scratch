"""Day 4 · TodoWrite: the agent's externalised plan.

WHAT IT MUST DO
    Let the model write and revise a task list that lives outside the
    context window, and that you can inspect mid-run.

TO BUILD
    [ ] A todo_write tool the model calls with the full list, not a diff.
    [ ] Per item: content, status (pending / in_progress / completed), and
        whatever ordering or dependency you decide you need.
    [ ] State lives in the harness, not only in the transcript. The model
        should be able to re-read it after compaction.
    [ ] An invariant worth enforcing: at most one item in_progress.
    [ ] Render the current list into the prompt -- decide where, and what it
        costs in tokens per turn.

DONE WHEN
    A 20-step task still knows what it is doing at step 18.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s05_todo_write
    https://arxiv.org/abs/2303.11366  (Reflexion)
"""
