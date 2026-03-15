# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Create a root-level `skills.md` that distills the kube.io Liquid Glass CSS/SVG article into a reusable implementation note.

## Scope

- Create `skills.md` from <https://kube.io/blog/liquid-glass-css-svg/>.
- Preserve the article's usable implementation details: optics assumptions, surface profiles, SVG displacement-map pipeline, component patterns, and browser caveats.
- Keep the artifact practical and concise enough to reuse as a build note.

## Constraints

- Do not invent production guarantees the article does not claim.
- Call out the Chromium-only `backdrop-filter: url(#svgFilterId)` limitation.
- Limit work to `skills.md` and the live-state docs for this objective.
- Do not commit from this task.

## Success Criteria

- `skills.md` exists at the repository root.
- The file captures the article's refraction model, SVG displacement-map workflow, specular highlight step, and operational caveats.
- The live docs record the completed work and verification state.