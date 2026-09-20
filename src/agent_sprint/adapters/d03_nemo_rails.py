"""Day 3 · NeMo Guardrails behind your interface.

WHAT IT MUST DO
    Sit at the same seam as d03_hooks.py, so the Day 3 attack suite can run
    with your defence, theirs, or both.

TO BUILD
    [ ] uv sync --group w1-guardrails.
    [ ] Llama Guard and Prompt Guard served on the 5090
        (settings.vllm_chat_url).
    [ ] Same in/out shape as your own hook, so the attack suite swaps one
        for the other with a flag.
    [ ] Rerun the full attack suite. Report attack success rate AND added
        latency per turn -- the second number is the one vendors omit.

TOOL VERDICT (journal)
    What does it do that I could not? What does it hide that I need to see?
    What does it cost -- dependencies, latency, lock-in? What breaks when it
    breaks? Would I ship it?
"""
