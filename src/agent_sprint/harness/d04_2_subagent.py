"""Day 4 · Subagents: a fresh messages[] behind a tool call.

WHAT IT MUST DO
    Run a nested agent loop with its own context, returning only its
    conclusion to the parent.

TO BUILD
    [ ] A tool on the parent that takes a task description and returns text.
    [ ] Inside it, a brand-new messages list. The parent's transcript does
        not leak in; that isolation is the entire point.
    [ ] Decide the subagent's tool set -- narrower than the parent's.
    [ ] Decide what crosses back: a summary, structured findings, or files
        on disk. Everything else is discarded.
    [ ] Independent limits: iterations, tokens, wall clock.
    [ ] Parallel subagents where the parent asks for several.
    [ ] Stretch, and the bridge to Day 5: a second flavour that FORKS
        instead -- the child starts from the parent's exact prefix, byte for
        byte, so the prompt cache still hits. Isolation drops; cost drops
        with it. Measure both and say which you would ship.

EXPERIMENT (today's number)
    One investigation task, run twice: single agent vs orchestrator + 3
    subagents. Measure tokens, wall time, and quality against a rubric you
    write BEFORE you run either.

DONE WHEN
    You have both numbers and a sentence on when the N-times token cost was
    worth it.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s06_subagent
    https://www.anthropic.com/engineering/multi-agent-research-system
    https://cognition.ai/blog/dont-build-multi-agents   (they disagree)
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch08-sub-agents.md -- what a child inherits and what it may
        return; book/ch09-fork-agents.md for the fork variant above;
        book/ch10-coordination.md on the cost of orchestration.
"""
