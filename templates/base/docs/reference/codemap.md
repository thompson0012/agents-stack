# Code Map

## If you want to…

| Goal | Start here |
|------|-----------|
| Find the right skill for a request | `templates/base/.agents/skills/using-labs21-suite/SKILL.md` |
| See what the suite router owns | `templates/base/.agents/skills/using-labs21-suite/references/children.json` |
| Track phased work | `docs/live/roadmap.md` |
| Understand the live-doc contract | `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` |
| Route a design request | `templates/base/.agents/skills/using-design/SKILL.md` |
| Route an analytical request | `templates/base/.agents/skills/using-reasoning/SKILL.md` |
| Route software delivery work | `templates/base/.agents/skills/delivery-control/SKILL.md` |
| Start a product from idea to architecture | `templates/base/.agents/skills/labs21-product-suite/SKILL.md` |
| Create or upgrade a leaf skill | `templates/base/.agents/skills/create-skill/SKILL.md` |
| Create or upgrade a router package | `templates/base/.agents/skills/create-router-skill/SKILL.md` |

## Key Paths

### Skill routers (route to children)

- `templates/base/.agents/skills/using-labs21-suite/` — top-level suite router. Owns the shipped boundary: `using-design`, `using-reasoning`, `delivery-control`, plus direct leaves (`context-compaction`, `self-cognitive`, `meta-prompting`, `prompt-augmentation`, `create-skill`, `create-router-skill`, `startup-pressure-test`).
- `templates/base/.agents/skills/using-design/` — design-family router. Children cover foundations, tokens, generative UI, liquid-glass.
- `templates/base/.agents/skills/using-reasoning/` — reasoning-family router. Children cover calibration, framing, foresight, reality checks, advisory, multi-lens.
- `templates/base/.agents/skills/delivery-control/` — delivery-family router. Children: `harness-design`, `frontend-evaluator`.
- `templates/base/.agents/skills/labs21-product-suite/` — stage-gated product router. Children: `labs21-chief-architect`, `labs21-prd-writer`, `labs21-system-architect`.

### Direct leaves (no children)

- `templates/base/.agents/skills/context-compaction/` — session compaction and handoff snapshots.
- `templates/base/.agents/skills/self-cognitive/` — confidence checks, retrospectives, workflow extraction.
- `templates/base/.agents/skills/meta-prompting/` — prompt architecture and system-prompt design.
- `templates/base/.agents/skills/prompt-augmentation/` — enrich sparse generation prompts.
- `templates/base/.agents/skills/create-skill/` — leaf skill authoring.
- `templates/base/.agents/skills/create-router-skill/` — router package authoring.
- `templates/base/.agents/skills/startup-pressure-test/` — harsh startup viability teardown.

### Docs

- `docs/live/` — mutable repo-level execution state (`current-focus`, `progress`, `todo`, `roadmap`).
- `templates/base/docs/live/` — template delivery-control live docs (`runtime`, `qa`) for baton state and evaluator evidence when explicit delivery-control flows are in play.
- `docs/reference/` — durable project context (`architecture`, `codemap`, `memory`, `lessons`, `implementation`, `design`).
- `templates/base/docs/` — inert generated-project docs scaffold.

## Router metadata

Each router package stores its child inventory and selection rules in `references/children.json`. That file is the source of truth for:

- Which children the router owns.
- When to route to each child.
- Install hints for missing children.

Human-readable companion files (`references/router-metadata.md`, `references/relationship-types.md`) exist in some routers for reviewer context but do not override `children.json`.
