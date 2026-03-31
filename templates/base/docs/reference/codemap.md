# Code Map

## Key Paths

- `templates/base/AGENTS.md` is the constitutional root and first-read index; it must point to every must-read local `AGENTS.md`.
- `templates/base/docs/AGENTS.md`, `templates/base/docs/live/AGENTS.md`, and `templates/base/docs/reference/AGENTS.md` define the approved docs-side boundaries.
- `templates/base/.agents/AGENTS.md`, `templates/base/.agents/skills/AGENTS.md`, and `templates/base/.agents/skills-optional/AGENTS.md` define the approved agent-package boundaries.

## Entrypoints

- Start at `templates/base/AGENTS.md`, then descend only into the local guide for the subtree you enter.
- Approved local guides live only at durable boundaries; hidden or leaf-level guides are not part of the canonical hierarchy.

## High-Value Files

- `templates/base/docs/live/{current-focus.md,progress.md,todo.md,roadmap.md,runtime.md,qa.md}` remain inert until localization in a copied repo.
- `templates/base/.agents/skills/` carries shipped skill-package truth, while `templates/base/.agents/skills-optional/` carries optional packages separately.