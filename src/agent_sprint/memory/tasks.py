"""Day 10 · File-backed task DAG that survives a kill -9.

WHAT IT MUST DO
    Let a long-running agent be killed mid-task and resume without redoing
    completed work or corrupting state.

TO BUILD
    [ ] Tasks with blockedBy edges. Ready = all blockers complete.
    [ ] State on disk, written atomically. A partial write during a crash is
        the failure mode you are defending against -- write temp, fsync,
        rename.
    [ ] A task in_progress at crash time has a decision attached: retry,
        fail, or needs-human. Decide per task type.
    [ ] Cycle detection at add time, not at run time.
    [ ] Idempotent side effects, or a record of what was already done. The
        DAG cannot un-send an email.

DONE WHEN
    You kill the process mid-task and it resumes correctly. Do it three
    times at different points, including during a state write.

READ
    https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s10_task_system
"""
