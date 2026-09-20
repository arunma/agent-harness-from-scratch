"""Day 5 · OpenTelemetry spans -> Langfuse. Every run from today is evidence.

WHAT IT MUST DO
    Emit a trace per agent run that you can still mine on Day 11, when the
    conversation that produced it is long forgotten.

TO BUILD
    [ ] uv sync --group w1-tracing. Langfuse from infra/mac/docker-compose.yml.
    [ ] Span hierarchy: run -> turn -> (llm call | tool call). Decide it once
        and keep it stable; Day 11 queries depend on the shape.
    [ ] GenAI semantic-convention attribute names, not invented ones:
        gen_ai.system, gen_ai.request.model, gen_ai.usage.input_tokens, etc.
    [ ] Tool spans carry name, permission decision, duration, error state.
    [ ] Dual export to LangSmith, so you can compare the two UIs on the same
        runs.
    [ ] Decide what must not leave the machine in a trace payload. Write the
        answer down -- Day 14 asks for it.

DONE WHEN
    A run appears in Langfuse with per-turn token counts and cache hit rate,
    and you can pull 50 such runs back out as JSON on Day 11.

READ
    https://opentelemetry.io/docs/specs/semconv/gen-ai/
    https://langfuse.com/self-hosting
"""
