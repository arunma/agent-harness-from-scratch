"""Day 11 · pass^k runner and scorecard. `make eval` prints this.

WHAT IT MUST DO
    Run every scenario k times, score it, and print one table that tells you
    whether today's change helped.

TO BUILD
    [ ] Load scenarios from evals/d11_2_scenarios/.
    [ ] Reset state between runs -- a fresh database from scripts/seed_bank.py,
        fresh memory. A scenario that passes only because the previous one
        ran is worthless.
    [ ] pass^k with k=4: the scenario passes only if ALL k runs pass. This
        is the reliability number, not the average.
    [ ] Assertions first; judges only on what survives.
    [ ] Scorecard: pass^k per scenario, per failure category, plus tokens,
        cost and p50/p95 latency.
    [ ] Persist each run's result so you can diff today against yesterday.
    [ ] Parallel scenario execution, with the state isolation that requires.

DONE WHEN
    `make eval` prints a scorecard, and the numbers move when you break
    something on purpose.

READ
    https://arxiv.org/abs/2406.12045   (tau-bench, pass^k)
    https://github.com/sierra-research/tau-bench
"""
