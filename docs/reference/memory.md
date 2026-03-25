# Memory

Read for durable truths worth preserving across sessions. Do not store transient status here.

## Durable Truths

- Truth:
- Why it persists:

## Decisions to Preserve

- Decision:
- Preserve because:
- Revisit only if:


- Decision: When creating a new bundled router family around existing first-party skills, default to moving those bundled leaves under the router package in the same change instead of routing to external top-level leaves first.
- Preserve because: the one-step cutover keeps the package boundary honest, avoids duplicated migration work, and prevents stale path references from surviving a temporary external-child phase.
- Revisit only if: a leaf is intentionally shared across multiple families or the runtime cannot discover nested children reliably enough to support the bundled layout.