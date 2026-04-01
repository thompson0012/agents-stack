# Agent Packages Guide

This `AGENTS.md` extends `../AGENTS.md`. Root constitutional rules cannot be overridden.

## Local Scope

This subtree defines the template's bundled agent packages and the portable machine-readable root router metadata that ships with the copied hierarchy.

## Owns

- `skills/` as the shipped top-level skill packages in this template
- `skills-optional/` as optional top-level packages that are shipped but not default bundled truth
- `router-manifest.json` as the portable root routing inventory for the copied hierarchy

## Does Not Own

- template docs under `../docs/`
- copied-repo runtime state after localization outside the template package

## Required Reads

1. Read `../AGENTS.md` first.
2. Read `skills/AGENTS.md` before acting under `.agents/skills/`.
3. Read `skills-optional/AGENTS.md` before acting under `.agents/skills-optional/`.
4. Use `router-manifest.json` when checking which template-local guide owns a copied-root task.

## Local Update Rules

- Keep the split between shipped and optional package surfaces truthful.
- Keep `router-manifest.json` aligned with the real copied-template entrypoints it advertises.
- When a package moves between shipped and optional surfaces, update every affected inventory in the same change.
- Do not hide required template package guidance outside the indexed subtree guides.

## Failure Modes to Avoid

- leaving stale router paths in `router-manifest.json` after moving a template-local guide
- describing optional packages as shipped default truth
- changing package ownership without updating the affected inventories
- treating this subtree as if it governed the template docs boundary too