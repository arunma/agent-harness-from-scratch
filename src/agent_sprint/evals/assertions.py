"""Day 11 · Code assertions. These come before any judge.

WHAT IT MUST DO
    Check the things that have a right answer, deterministically and for
    free.

TO BUILD
    [ ] Database end-state checks: after scenario X, the disputes table
        contains exactly this row.
    [ ] Tool-trace checks: the required tool was called; the forbidden one
        was not; the approval gate fired before the write.
    [ ] Citation checks: every cited doc_id exists, every page is in range,
        no superseded notice cited as current.
    [ ] Refusal checks: the out-of-corpus question returned "not found".
    [ ] Budget checks: tokens, wall time, tool-call count under ceiling.
    [ ] Clear failure messages. "Assertion failed" costs you an hour on
        Day 15.

RULE
    Anything a code assertion can check must not go to a judge. Judges are
    for the rest.
"""
