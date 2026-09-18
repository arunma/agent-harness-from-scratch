---
description: Review uncommitted changes without editing anything
argument-hint: [optional path or focus]
---
Review Arun's current work. Scope: $ARGUMENTS (if empty, review `git diff` plus untracked files under `src/`).

Follow the review format in CLAUDE.md:
- Numbered findings, most severe first, labelled **bug**, **risk**, **design** or **nit**.
- For each: file and line, what's wrong, why it matters, and the direction of the fix in words. No rewritten code; at most a one-line illustration if a word description would be unclear.
- Tag code as `[SDK]`, `[H]`, `[P]` or `[T]`.
- Call out anything that breaks the sprint's safety rules: secrets in code, real data, irreversible actions without a gate.
- Finish with one question that checks he understands the most important finding.

Do not edit any files.
