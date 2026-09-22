"""Day 5 · Context policy: four-stage compaction.

WHAT IT MUST DO
    Keep a long run inside a token budget without losing what the task
    depends on.

TO BUILD
    [ ] Measure before you cut: tokens per message, per tool result, per
        turn. You cannot manage what you are not counting.
    [ ] Four stages, in order, each with a trigger you can state as a number:
        1. nothing (under budget)
        2. trim -- drop or truncate old tool results
        3. summarise -- collapse old turns into one summary message
        4. hard reset -- summary plus the current todo list only
    [ ] Rules about what is never dropped: the system prompt, the current
        todo list, the last tool result, the original task.
    [ ] Prompt-cache awareness: compaction invalidates the prefix. Every
        compaction has a cash cost on the next turn. Log the cache hit rate.

EXPERIMENT (today's number)
    One 40-turn task at 3 context budgets. Report tokens, cost, cache hit
    rate and whether the task still succeeded.

BRIDGE
    KV bytes per token = 2 * n_layers * n_kv_heads * head_dim * bytes.
    Compute it for the Day 13 local model; that is what context costs in
    VRAM when you are the one serving it.

READ
    https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    https://arxiv.org/abs/2307.03172  (Lost in the Middle)
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s08_context_compact
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch05-agent-loop.md, the context-management section -- one
        shipped harness's layers and the trigger for each;
        book/ch09-fork-agents.md on keeping the cached prefix intact.
"""
