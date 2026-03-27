# Lessons

Read after mistakes, rework, or surprises. Capture only reusable lessons.

## Mistakes

- What happened:
- Why it happened:

## Anti-Patterns

- Pattern to avoid:
- Better default:

## Fixes

- Fix:
- When to apply:
- Evidence:

- Fix: keep `templates/base/docs/live/` generic and move actual session state into the consuming project's `docs/live/`.
- When to apply: whenever adjusting template live docs or adding a workflow skill that writes runtime state.
- Evidence: the template repo previously contained real session content in live docs, which needed to be reset to placeholders.

- Fix: when adding a new control-related leaf, let the leaf own orchestration/persistence while `harness-design` owns the execution-mode contract and integrity rules.
- When to apply: whenever the work spans both roadmap persistence and role/control semantics.
- Evidence: `multi-phase-control` and `harness-design` stay separable but coordinated through explicit references.

- Fix: write router and skill edits under `templates/base/`, not the user-home copy, and remove any accidental repo-root `.agents/` duplicate before verifying.
- When to apply: whenever scaffolding or copying skill packages in this repository.
- Evidence: this task initially wrote to the wrong location and left a duplicate tree until the repo-root copy was deleted.
