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

- Decision: After meaningful work, explicitly triage whether any `docs/reference/*` file must change instead of waiting for user prompting or relying on memory.
- Preserve because: durable defaults, routing rules, package moves, and reusable lessons are otherwise easy to ship without updating the long-lived docs that future sessions depend on.
- Revisit only if: a stronger automated diff-based enforcement mechanism replaces the guide-level writeback gate.

- Decision: Keep harsh startup survivability work in `startup-pressure-test`, and route broad analytical-family ambiguity through `using-reasoning` instead of reviving deleted founding or research-family claims inside the top-level suite.
- Preserve because: this keeps commercial pressure testing separate from generic reasoning-family selection and prevents stale deleted-family routes from reappearing in the top-level router.
- Revisit only if: the template intentionally reintroduces a distinct founding or research-family router with its own shipped boundary.

- Decision: Keep the template's top-level suite router scoped to the shipped Labs21 skill surface under `templates/base/.agents/skills/`, with `using-labs21-suite` routing across the current top-level families `using-design`, `using-reasoning`, and `delivery-control` plus the direct leaves.
- Preserve because: the router boundary must tell the truth about the shipped skill tree, or discovery and first-hop routing drift immediately when families are added, removed, or moved.
- Revisit only if: the template intentionally re-bundles other families under the top-level suite or replaces the top-level router boundary entirely.