"""Day 1 · The nanochat bridge: what the API hides at the token level.

WHAT IT MUST DO
    Render the same tools-enabled conversation with an open model's tokenizer,
    so you see the string and the token IDs the Messages API never shows you.

TO BUILD
    [ ] uv sync --group w1-tokens, then load the Qwen/Qwen2.5-0.5B-Instruct
        tokenizer.
    [ ] Print tokenizer.chat_template first. It is Jinja. Read it before you
        run anything -- it is the whole answer to "who adds the specials?".
    [ ] apply_chat_template(messages, tools=..., tokenize=False,
        add_generation_prompt=True). Print the rendered string exactly, with
        whitespace and special tokens visible.
    [ ] Encode it. Print the token count and the first ~40 (id, piece) pairs.
    [ ] Render with and without tools=. The difference is the per-turn token
        tax your tool schemas cost. Write that number down.
    [ ] Hand-write the parser for Qwen's tool-call syntax (it emits JSON
        inside <tool_call> tags). Feed it a sample assistant string, return
        the tool name and arguments.
    [ ] Render a tool result back into the template; show the next prompt.

DONE WHEN
    The journal has the rendered string, the token IDs and the schema token
    cost, and you can state what Anthropic does on your behalf.

READ
    https://huggingface.co/docs/transformers/main/en/chat_templating
    https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

BRIDGE
    Same token-id pipeline as nanochat. The only new thing is a Jinja template
    deciding which special tokens wrap which role.
"""
