# Lessons

Read after mistakes, rework, or surprises. Capture only reusable lessons.

## Mistakes

- What happened:
- Why it happened:

## Anti-Patterns

### Scope Drift via "Helpful" Additions
- Pattern: Adding features "that would be nice" or "while I'm here"
- Detection: Work touches files not in Scope or creates new files not explicitly listed
- Better default: Add to `docs/live/todo.md` as a separate task; do not implement inline

### Premature Abstraction
- Pattern: Creating frameworks or utilities for single-use code
- Detection: New utility files created before the feature works end-to-end
- Better default: Implement the feature first; extract utilities only after 2+ use cases

### Documentation-Driven Development
- Pattern: Updating docs before implementation works
- Detection: More doc edits than code edits in a session
- Better default: Implement, verify, then update docs

## Fixes

- Fix:
- When to apply:
- Evidence:


### Router Family Created Before Physical Bundling
- Pattern: Adding a new router over existing top-level leaves first, then doing a second pass to move those leaves under the router package.
- Detection: The router metadata points at external leaf targets even though the leaves are bundled with the repo and clearly belong inside the same family boundary.
- Better default: When a new bundled router family is justified, default to nesting the bundled leaves under that router in the same change and cut all routes/references over once.