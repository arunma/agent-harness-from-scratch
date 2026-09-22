"""Day 2 · Tool registry and dispatch. The agent-computer interface.

WHAT IT MUST DO
    Own the tools, their schemas, their dispatch and their failure modes, so
    d01_3_loop.py never knows a tool's name.

TO BUILD
    [ ] Five tools: read_file, write_file, grep, run_sql, http_get.
    [ ] One place where a tool's name, description, JSON Schema and
        implementation live together. Registering a tool is one step, not
        three files to edit.
    [ ] Emit the Anthropic tool-definition list from the registry. Never
        maintain the schemas twice.
    [ ] Dispatch: name -> callable, with arguments validated against the
        schema before the call.
    [ ] Parallel execution when a turn asks for several tools; results keyed
        by tool_use_id, not ordered by completion.
    [ ] Partition before you parallelise: each tool declares whether it is
        concurrency-safe. Read-only tools (read_file, grep, http_get) run in
        one batch; anything that writes or mutates state runs serially, in
        the order the model asked for it. Two writes to the same file in
        "parallel" is a bug you only see once, in production.
    [ ] Every failure becomes an observation the model can read: unknown
        tool, bad arguments, exception, timeout.
    [ ] Bound the blast radius today, even though Day 3 formalises it:
        file tools confined to a root, run_sql read-only over
        settings.bank_db_path, http_get on an allow-list.

EXPERIMENT (today's number)
    10 tasks x 3 description variants (terse / good / misleading)
    -> success rate and tokens per variant. Same tools, same schemas; only
    the description strings change. Table goes in the journal.

DONE WHEN
    The table exists and you can point at one failure that was the
    description's fault rather than the model's.

READ
    https://www.anthropic.com/engineering/writing-tools-for-agents
    https://arxiv.org/abs/2405.15793  (SWE-agent, the ACI section)
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch07-concurrency.md -- the partition algorithm and streaming
        executor; book/ch06-tools.md for the execution pipeline and result
        budgeting.
"""
