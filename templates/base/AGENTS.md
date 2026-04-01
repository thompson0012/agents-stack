# Project Agent Guide

This `AGENTS.md` is the constitutional root for `templates/base`. Read it first. Local `AGENTS.md` files add subtree-specific rules and cannot override this file.

## Project Context

This directory packages a portable AGENTS and skill hierarchy that can be copied into another repository and localized there.

- `AGENTS.md` is the always-loaded root index for the copied hierarchy.
- `.agents/` carries bundled skill packages and package-surface rules.
- `docs/live/` ships as inert scaffolds until the copied repo localizes them into active project state.
- `docs/reference/` ships durable template truths that should be adapted only when the copied project changes the underlying contract.

## Mandatory First Reads

1. Read this file first before acting in the copied hierarchy.
2. Before acting in `.agents/`, `.agents/skills/`, `.agents/skills-optional/`, `docs/`, `docs/live/`, or `docs/reference/`, read the indexed local guide for that subtree.
3. If you copy only part of this template, revalidate every parent-relative guide path before relying on local rules.

## Operational Commands

This template ships no seeded install, build, lint, or test commands by default.

- After copying into a downstream repo, replace this section with that repo's exact commands before relying on autonomous verification.
- Keep the copied template command-free until the downstream repo localizes its real toolchain honestly.
- Use `.agents/router-manifest.json` plus the indexed local guides to route work until those commands are localized.

## Skill Invocation Precedence

- Check project-local shipped skills under `.agents/skills/` before relying on generic knowledge.
- Use the most specific shipped skill that matches the task.
- Treat `.agents/skills-optional/` as opt-in surfaces, not default bundled truth.

## Safety Boundaries

### Always do

- Keep the root guide short, truthful, and index-like.
- Update the discovery index in the same change that adds or removes a must-read local `AGENTS.md`.
- Keep template live docs inert until a copied repo localizes them.

### Ask first

- If a copied repo wants this template root to own downstream install/build/lint/test commands permanently instead of localizing them.
- If you plan to merge optional skill surfaces into shipped default truth.

### Never do

- Do not treat template placeholder content as active copied-repo truth.
- Do not hide required guidance in non-indexed leaves.
- Do not describe optional or planned surfaces as shipped default truth.

## Injected Context Contract

- This root `AGENTS.md` is the only always-in-context index for the template hierarchy.
- Pull deeper guides and docs on demand; do not assume child guides or `docs/*` content were injected unless you read them.
- Keep the root guide short, truthful, and index-like.

## Hierarchical Discovery

- Local guides may add subtree-specific rules, but they cannot override this file.
- Every must-read local `AGENTS.md` must appear in the discovery index in the same change that adds or removes it.
- Do not hide required guidance in non-indexed leaves.

## Live-Doc Writeback Obligation

- In this template, `docs/live/` remains inert until a copied repo localizes it into real project state.
- If work changes the template live-doc contract or localization expectations, update the governing docs in the same change.
- Do not seed or preserve plausible live-doc state as shipped template truth.

## Reference Writeback Gate

- Before yielding after meaningful work, decide whether any `docs/reference/*` file must change to keep durable truth aligned.
- If no reference-doc update is needed, record that conclusion explicitly in your working notes.
- Do not describe planned or optional surfaces as shipped truth.

## Cross-System Precedence

- Root constitutional rules win over subtree guides.
- A deeper local guide may narrow behavior inside its durable boundary, but it does not own root-level policy.
- When a copied repo localizes these templates, explicit copied-repo truth beats template placeholder content.

## Discovery Index

| Topic | Location |
|-------|----------|
| Portable router manifest | `.agents/router-manifest.json` |
| Agent package boundary | `.agents/AGENTS.md` |
| Shipped skill package rules | `.agents/skills/AGENTS.md` |
| Optional skill package rules | `.agents/skills-optional/AGENTS.md` |
| Documentation workflow rules | `docs/AGENTS.md` |
| Live-doc scaffold rules | `docs/live/AGENTS.md` |
| Reference-doc rules | `docs/reference/AGENTS.md` |