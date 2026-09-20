"""Day 12 · The card-dispute flow as a LangGraph workflow.

WHAT IT MUST DO
    Run the same business flow as dispute_agent.py, but with the control
    flow written by you rather than decided by the model each turn.

TO BUILD
    [ ] Explicit nodes and edges for the dispute flow: intake, classify,
        retrieve policy, check eligibility, decide, approve, execute, notify.
    [ ] LLM nodes only where judgement is genuinely needed. Every node that
        could be an if-statement should be an if-statement.
    [ ] An interrupt before the write, for human approval. Resume after.
    [ ] Persistence, so an interrupted run resumes in a different process.
    [ ] Same tools as the agent version -- the comparison is invalid
        otherwise.

DONE WHEN
    The Day 11 suite runs against it and produces pass^k, cost, latency and
    an auditability judgement.

READ
    LangGraph docs: persistence, durable execution, interrupts
    https://arxiv.org/abs/2407.01489   (Agentless -- the case for this side)
"""
