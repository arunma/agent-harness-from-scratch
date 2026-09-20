"""Day 11 · One LLM judge, validated against your own labels.

WHAT IT MUST DO
    Score what code cannot -- and prove it agrees with you before you trust
    a single one of its verdicts.

TO BUILD
    [ ] ONE judge, with one rubric, doing one thing. Resist the panel.
    [ ] Binary or small ordinal output with a stated reason. Not 1-10.
    [ ] Your own labels first: hand-label ~50 outputs, then measure the
        judge's TPR and TNR against them. An unvalidated judge is a random
        number generator with good manners.
    [ ] Position and verbosity bias controls if you compare two outputs.
    [ ] A cheaper model for the judge (settings.judge_model) -- and check
        whether that changed the agreement numbers.

DONE WHEN
    You can state the judge's TPR and TNR on your labels, and you know which
    failure mode it is blind to.

READ
    https://arxiv.org/abs/2306.05685   (Judging LLM-as-a-Judge)
    https://arxiv.org/abs/2404.12272   (Who Validates the Validators?)
    https://hamel.dev/blog/posts/evals-faq/
"""
