# Architecture Reference

## Current Shipped Surfaces

### Skill routers (`templates/base/.agents/skills/`)

| Router | Owns | Children |
|--------|------|----------|
| `using-labs21-suite` | Top-level suite boundary | Routes to `using-design`, `using-reasoning`, `delivery-control`, and direct leaves |
| `using-design` | Design-family selection | Foundations, tokens, generative UI, liquid-glass |
| `using-reasoning` | Reasoning-family selection | Calibration, framing, foresight, reality checks, advisory, multi-lens |
| `delivery-control` | Software delivery lifecycle | `harness-design`, `frontend-evaluator` |
| `labs21-product-suite` | Stage-gated product development | `labs21-chief-architect`, `labs21-prd-writer`, `labs21-system-architect` |

### Direct leaves (`templates/base/.agents/skills/`)

`context-compaction`, `self-cognitive`, `meta-prompting`, `prompt-augmentation`, `create-skill`, `create-router-skill`, `startup-pressure-test`.

### Doc surfaces

| Surface | Location | Job |
|---------|----------|-----|
| Agent contract | `AGENTS.md` | Always-injected index; read/update rules |
| Repo live state | `docs/live/` | Mutable execution state: focus, progress, todo, roadmap |
| Template delivery-control live state | `templates/base/docs/live/` | Baton state and evaluator evidence (`runtime`, `qa`) when explicit delivery-control exists |
| Durable reference | `docs/reference/` | Architecture, codemap, memory, lessons, implementation, design |
| Generated scaffold | `templates/base/` | Inert starter files for new projects |

## Historical / Removed Names

These names appeared in earlier iterations and no longer exist in the shipped skill tree. They must not be referenced as current:

| Removed name | What replaced it |
|-------------|-----------------|
| `coding-and-data` | Moved to `skills-optional/`; no shipped replacement. Implementation tasks route through `delivery-control` or direct leaves. |
| `website-building` | Moved to `skills-optional/`; browser QA now lives in `delivery-control/frontend-evaluator`. |
| `project-founding` | Deleted. Startup viability lives in `startup-pressure-test`; product ideation in `labs21-product-suite`. |
| `using-sales`, `using-marketing`, `using-legal`, `using-finance`, `using-research`, `using-documents` | Removed from shipped suite. If re-added, they need their own shipped router under `templates/base/.agents/skills/`. |
| `software-delivery` | Renamed to `delivery-control`. |

## Invariants

- **Suite boundary honesty.** `using-labs21-suite` may claim only the currently shipped top-level families and direct leaves. Deleted or moved families must disappear from the router in the same change.
- **Harness scope.** `delivery-control/harness-design` is only for cross-session control, compaction rules, baton passing, and planner/generator/evaluator structure. Routine single-session work does not enter harness design.
- **Evaluator ownership.** Independent browser signoff belongs to `delivery-control/frontend-evaluator`. No separate shipped builder-QA family exists unless one actually ships under `templates/base/.agents/skills/`.
- **Live-doc split.** Repo-level live docs are `docs/live/current-focus.md`, `docs/live/progress.md`, `docs/live/todo.md`, and `docs/live/roadmap.md`. Template delivery-control baton and evaluator state live separately under `templates/base/docs/live/runtime.md` and `templates/base/docs/live/qa.md`.
- **Template inertness.** Generated scaffolds under `templates/base/docs/` must contain no prefilled content. They are structural placeholders only.
- **Router metadata as source of truth.** `references/children.json` in each router package is the authority for child inventory. Prose in `SKILL.md` must not duplicate or contradict the metadata.

## Major Components

| Component | Responsibility | Key dependency |
|-----------|----------------|----------------|
| `using-labs21-suite/` | Top-level discoverability router | `references/children.json`, `references/category-map.md` |
| `delivery-control/` | Software delivery routing | `references/children.json`, nested `harness-design/`, `frontend-evaluator/` |
| `labs21-product-suite/` | Stage-gated product development | `references/children.json`, `references/router-metadata.md`, `references/relationship-types.md`, nested stage children |
| `using-design/` | Design-family routing | `references/children.json`, shipped design children |
| `using-reasoning/` | Reasoning-family routing | `references/children.json`, shipped reasoning children |
| `docs/live/` | Repo-level execution state | Truthful updates from the active role before handoff |
| `templates/base/docs/live/` | Template delivery-control state | Baton state and evaluator evidence for explicit delivery-control flows |
