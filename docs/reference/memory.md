# Memory

Read for durable truths worth preserving across sessions. Do not store transient status here.

## Durable Truths

- Truth:
- Why it persists:

## Decisions to Preserve

- Decision:
- Preserve because:
- Revisit only if:


- Decision: Keep repo-local AGENTS-governance workflow in `.agents/skills/using-agents-md/SKILL.md`, with `AGENTS.md` owning boundary rules, `docs/reference/*` owning durable truth, and `docs/live/*` owning session state.
- Preserve because: this keeps the root skill-discovery pointer honest and prevents boundary rules, durable policy, and live progress from collapsing into the same file.
- Revisit only if: the repository intentionally retires repo-local skills or folds the same decision procedure directly into the root `AGENTS.md` without losing clarity.

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
- Decision: The `labs21-product-suite` router must hand off to the selected stage child and continue with that child's workflow after emitting the route line.
- Preserve because: greenfield product work needs a clean, stage-aware route from strategy to PRD to architecture; a route that stops at the top layer stalls the task instead of continuing it.
- Revisit only if: the suite is intentionally flattened into a single leaf skill or nested child handoff becomes impossible in the runtime.

- Decision: The `labs21-product-suite` router package follows the canonical router shape with `SKILL.md`, `references/children.json`, `references/router-metadata.md`, `references/relationship-types.md`, `assets/router-skill-template.md`, `assets/children-template.json`, and `scripts/validate_router.py` instead of a prose category map.
- Preserve because: keeping router metadata and package templates machine-readable and colocated with the package makes future routing changes honest and avoids duplicating the stage map in a separate category page.
- Revisit only if: the router family shape intentionally changes across the shipped Labs21 template set.
