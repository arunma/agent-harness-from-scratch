"""Day 5 · Skill loading: a catalogue in context, bodies on demand.

WHAT IT MUST DO
    Keep instructions out of the prompt until the model needs them.

TO BUILD
    [ ] A skill on disk: name, one-line description, and a body the model
        only sees when it asks.
    [ ] A catalogue rendered into the system prompt -- names and
        descriptions only. Measure what that costs per turn.
    [ ] A load tool that returns one skill body.
    [ ] Decide what happens to a loaded body at compaction: pinned, or
        dropped and reloadable?
    [ ] Two real skills for the capstone, e.g. a dispute-handling procedure
        and a policy-citation format.

DONE WHEN
    You can state the token difference between all skills always loaded and
    the catalogue-plus-load design, on the same 40-turn task.

READ
    https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s07_skill_loading
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch12-extensibility.md, the skills half -- two-phase loading, the
        frontmatter contract, and why a skill body from an untrusted source
        is a security boundary.
"""
