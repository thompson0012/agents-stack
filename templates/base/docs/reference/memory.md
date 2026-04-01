# Memory

Durable truths that survive beyond a single session. Each entry carries freshness metadata so readers can assess staleness.

## Routing Decisions

### Suite router scoped to shipped skills only
- **Truth:** The top-level suite router (`using-labs21-suite`) is scoped to the shipped Labs21 skill surface under `templates/base/.agents/skills/`. It routes across `using-design`, `using-reasoning`, and `delivery-control` plus direct leaves. Deleted families must not reappear.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** `templates/base/.agents/skills/using-labs21-suite/references/children.json`
- **Revisit if:** the template intentionally re-bundles other families or replaces the top-level router boundary.

### Startup survivability separated from reasoning
- **Truth:** Harsh startup survivability work lives in `startup-pressure-test`. Broad analytical-family ambiguity routes through `using-reasoning`. Deleted founding or research-family claims must not re-enter the suite router.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** architecture invariant; `using-labs21-suite/references/children.json`
- **Revisit if:** the template intentionally reintroduces a distinct founding or research-family router.

### Product-suite router hands off to stage child
- **Truth:** `labs21-product-suite` hands off to the selected stage child and continues with that child's workflow after emitting the route line.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** `templates/base/.agents/skills/labs21-product-suite/SKILL.md`
- **Revisit if:** the suite is intentionally flattened or nested child handoff becomes impossible.

## Packaging Decisions

### Bundled leaves under router packages
- **Truth:** When creating a new bundled router family around existing first-party skills, move those leaves under the router package in the same change. Do not route to external top-level leaves first.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** migration experience from `using-design`, `using-reasoning`, `delivery-control` build-outs.
- **Revisit if:** a leaf is intentionally shared across multiple families or the runtime cannot discover nested children.

### Canonical router package shape
- **Truth:** Router packages follow the shape: `SKILL.md`, `references/children.json`, `references/router-metadata.md`, `references/relationship-types.md`, optionally `assets/` and `scripts/validate_router.py`.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** `labs21-product-suite/` as canonical exemplar; `create-router-skill/` authoring guide.
- **Revisit if:** the router family shape intentionally changes across the shipped template set.

## Process Decisions

### Reference writeback gate
- **Truth:** After meaningful work, explicitly triage whether any `docs/reference/*` file must change. Do not wait for user prompting or rely on memory.
- **Status:** active
- **Recorded at:** 2026-03-27
- **Last verified at:** 2026-04-01
- **Source:** `AGENTS.md` Reference Writeback Gate section.
- **Revisit if:** a stronger automated enforcement mechanism replaces the guide-level gate.

### Template live docs must be inert
- **Truth:** Generated scaffolds under `templates/base/docs/` contain no prefilled content. They are structural placeholders only.
- **Status:** active
- **Recorded at:** 2026-03-31
- **Last verified at:** 2026-04-01
- **Source:** current-focus.md objective; architecture invariant.
- **Revisit if:** the template intentionally seeds starter content for specific project types.

### Repo live docs are four files only
- **Truth:** Repo-level live docs are `docs/live/current-focus.md`, `docs/live/progress.md`, `docs/live/todo.md`, and `docs/live/roadmap.md`. Template delivery-control baton and evaluator state live separately under `templates/base/docs/live/runtime.md` and `templates/base/docs/live/qa.md`.
- **Status:** active
- **Recorded at:** 2026-04-01
- **Last verified at:** 2026-04-01
- **Source:** current-focus.md objective; AGENTS.md / architecture split.
- **Revisit if:** the repository intentionally adds or removes repo-level live-doc artifacts or moves template delivery-control state elsewhere.

### Roadmap as goal-lineage authority
- **Truth:** The roadmap (`docs/live/roadmap.md`) is the authoritative carrier for source goal, plan goal, phase goal, and goal retirement history. After compaction, agents rehydrate from live docs — not chat memory.
- **Status:** active
- **Recorded at:** 2026-03-31
- **Last verified at:** 2026-04-01
- **Source:** current-focus.md objective; harness goal-lineage hardening plan.
- **Revisit if:** a different mechanism replaces the roadmap as the goal-lineage carrier.
