# Code Map

## Key Paths

- `AGENTS.md` is the constitutional root and first-read index; it carries portable template context, clean startup-safe operational guidance, and root safety boundaries for copied repos.
- `docs/AGENTS.md`, `docs/live/AGENTS.md`, and `docs/reference/AGENTS.md` define the approved docs-side boundaries.
- `.agents/AGENTS.md`, `.agents/skills/AGENTS.md`, and `.agents/skills-optional/AGENTS.md` define the approved agent-package boundaries.

## Entrypoints

- `.agents/router-manifest.json` is the machine-readable routing inventory that ships with the copied template hierarchy.
- Start at `AGENTS.md`, then descend only into the local guide for the subtree you enter.
- Approved local guides live only at durable boundaries; hidden or leaf-level guides are not part of the canonical hierarchy.

## High-Value Files

- `docs/live/{current-focus.md,progress.md,todo.md,roadmap.md,runtime.md,qa.md}` remain inert until localization in a copied repo.
- `.agents/skills/` carries shipped skill-package truth, while `.agents/skills-optional/` carries optional packages separately.
