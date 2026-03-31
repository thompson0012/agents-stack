# Architecture Reference

## System Boundaries

- `templates/base/AGENTS.md` is the constitutional root and first-read index for the template AGENTS hierarchy.
- Approved local rule boundaries live under `templates/base/docs/` and `templates/base/.agents/`; deeper guides should exist only where a copied subtree has its own durable contract.

## Invariants

- The root discovery index must name every must-read local `AGENTS.md` in the same change that adds or removes that guide.
- Template `docs/live/*` files remain inert until a copied repo localizes them into real project state.
- Shipped and optional skill-package surfaces stay structurally separate; optional packages are never implied by shipped truth.

## Major Components

- Root guide: constitutional rules plus the first-read index for every required local guide.
- Docs guides: workflow rules, inert live-doc scaffolds, and durable reference-doc policy.
- `.agents` guides: package-boundary rules, shipped skill-package truth, and optional skill-package semantics.
