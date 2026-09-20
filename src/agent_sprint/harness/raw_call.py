"""Day 1 · One Messages API call with tools, over raw httpx. No SDK.

WHAT IT MUST DO
    Send a single POST to the Messages API with one tool defined, then print
    enough of the response that you can name every field in it.

TO BUILD
    [ ] Request: model, max_tokens, messages, tools. Headers: x-api-key,
        anthropic-version, content-type. Key from settings.anthropic_api_key --
        never hard-coded, never printed.
    [ ] One tool definition: name, description, input_schema (JSON Schema).
        Something bank-ish, e.g. get_balance(account_id) over the seeded
        SQLite at settings.bank_db_path.
    [ ] Ask a question that forces the tool. Print the raw response JSON.
    [ ] Print, labelled: stop_reason, every content block and its type, and
        for the tool_use block its id, name and input.
    [ ] Second turn: append the assistant message verbatim, then a user
        message carrying a tool_result block with the matching tool_use_id.
        Print the final answer.
    [ ] Print usage.input_tokens / output_tokens for both turns.

DONE WHEN
    You can explain every field without looking it up: why the assistant turn
    must be echoed back verbatim, what stop_reason tells the harness, and what
    breaks when tool_use_id does not match.

READ
    https://docs.claude.com/en/api/messages
    https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview

WATCH OUT
    No SDK import in this file -- that is the whole exercise.
"""
