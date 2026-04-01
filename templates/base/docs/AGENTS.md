# Documentation Workflow Guide

This `AGENTS.md` extends `../AGENTS.md`. Root constitutional rules cannot be overridden.

## Local Scope

- `live/` contains inert runtime scaffolds that must be localized before agents treat them as active project truth.
- `reference/` contains durable documentation that survives across sessions and copies.

## Owns

- the docs boundary under `docs/` in the copied hierarchy
- the split between inert live-doc scaffolds and durable reference docs

## Does Not Own

- template agent packages under `../.agents/`
- copied-repo runtime state after localization outside the template package

## Required Reads

1. Read `../AGENTS.md` first.
2. Read `live/AGENTS.md` before relying on anything under `docs/live/`.
3. Read `reference/AGENTS.md` before changing durable docs under `docs/reference/`.

## Local Update Rules

- Keep template live docs inert.
- Record durable documentation policy in `docs/reference/*`.
- Do not add new local guides below `docs/` unless the subtree earns a durable boundary.

## Failure Modes to Avoid

- treating inert template live docs as if they were active project state
- putting durable policy only in live-doc scaffolds
- adding non-durable local guides below `docs/` just to hold one-off instructions

## Discovery Index

| Topic | Location |
|-------|----------|
| Live-doc scaffold rules | `live/AGENTS.md` |
| Reference-doc rules | `reference/AGENTS.md` |