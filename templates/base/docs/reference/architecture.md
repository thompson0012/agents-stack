# Architecture Reference

## System Boundaries

- `AGENTS.md` is the constitutional root and first-read index for the template AGENTS hierarchy after copy.
- Approved local rule boundaries live under `docs/` and `.agents/`; deeper guides should exist only where a copied subtree has its own durable contract.
- `AGENTS.md` carries portable template context, clean startup-safe operational guidance, and template-root safety boundaries in addition to constitutional precedence.


## Invariants

- The root discovery index must name every must-read local `AGENTS.md` in the same change that adds or removes that guide.
- Template `docs/live/*` files remain inert until a copied repo localizes them into real project state.
- Shipped and optional skill-package surfaces stay structurally separate; optional packages are never implied by shipped truth.
- The template root guide must stay portable enough to be copied into another repo without pretending to know that downstream repo's toolchain; downstream repos localize their exact install/build/lint/test commands after copy.
- The template root guide remains short and index-like even after adding portable context, clean startup-safe operational guidance, and safety boundaries.


## Major Components

- Root guide: constitutional rules, portable template context, clean startup-safe operational guidance, safety boundaries, and the first-read index for every required local guide.
- Docs guides: workflow rules, inert live-doc scaffolds, and durable reference-doc policy.
- `.agents` guides: package-boundary rules, portable router metadata, shipped skill-package truth, and optional skill-package semantics.
