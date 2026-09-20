"""Day 13 · LiteLLM gateway in front of Claude and your 5090.

WHAT IT MUST DO
    Give the harness one endpoint, and give you routing, fallback and spend
    control behind it.

TO BUILD
    [ ] Point at settings.litellm_url; config from the workstation guide.
    [ ] Route by task: judge -> cheap, agent -> Claude, bulk -> local 5090.
    [ ] Fallback when a backend is down; prove it by killing vLLM mid-run.
    [ ] Per-key spend limits and per-task token budgets.
    [ ] Rerun the Day 11 suite through the gateway. Same numbers? If not,
        find out what the gateway changed.

TOOL VERDICT (journal)
    Five questions, plus the latency the extra hop costs at p50 and p95.
"""
