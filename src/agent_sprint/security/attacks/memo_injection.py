"""Day 3 · Indirect prompt injection through a merchant memo.

WHAT IT MUST DO
    Plant instructions in data the agent reads, and measure how often it
    obeys them -- before and after each defence.

TO BUILD
    [ ] A merchant_memo field in the seeded bank data carrying instructions
        aimed at the agent, not the user.
    [ ] A target action that is unambiguous when it happens: an unapproved
        refund, a write outside the allowed path, a leaked account number.
    [ ] A suite, not one payload. Vary the framing: direct instruction,
        fake system message, fake tool output, urgency, authority.
    [ ] Attack success rate as a number, over N runs. One run proves
        nothing.
    [ ] Run it four times: baseline, + prompt hardening, + hook filtering,
        + architectural separation (the data never reaches the same context
        as the capability).

DONE WHEN
    You have four numbers and can say which defence actually moved the rate
    and which only felt reassuring.

READ
    https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
    https://arxiv.org/abs/2302.12173   (Greshake et al.)
    https://arxiv.org/abs/2503.18813   (CaMeL -- defeating it by design)
"""
