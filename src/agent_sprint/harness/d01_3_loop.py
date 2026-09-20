"""Day 1 · The agent loop. Under 80 lines, written from memory.

WHAT IT MUST DO
    call -> tool_use? -> execute -> append result -> repeat, until the model
    stops asking for tools or a limit trips.

TO BUILD
    [ ] A messages list you own and mutate. Everything the model said stays
        in it verbatim.
    [ ] One call site, reusing d01_1_raw_call.py's request function.
    [ ] Branch on stop_reason. tool_use means continue; end_turn means stop.
    [ ] Execute every tool_use block in the turn -- there can be more than
        one -- and return all results in a single user message.
    [ ] A tool that raises comes back as a tool_result with is_error, not as
        a crash. The model has to see the failure to recover from it.
    [ ] Hard limits as constants at the top: max iterations, max total tokens.
    [ ] One trace line per iteration: turn, stop_reason, tool names called,
        cumulative tokens.

DONE WHEN
    Rewritten from memory in under 80 lines, and it survives a tool that
    throws, a tool that returns nothing, and a turn with two tool calls.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s01_agent_loop
    Read it, close it, then write this from memory.

LATER DAYS PLUG IN HERE
    Day 2 replaces inline dispatch with d02_tools.py. Day 3 wraps execution in
    permissions + hooks. Day 5 wraps the loop in a trace span and a context
    policy. Design those seams now or you will rewrite this four times.
"""
