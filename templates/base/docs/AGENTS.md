# Documentation Workflow Guide

This `AGENTS.md` extends `../AGENTS.md`. Root constitutional rules cannot be overridden.

## Local Scope

- `live/` contains inert runtime scaffolds that must be localized before agents treat them as active project truth.
- `reference/` contains durable documentation that survives across sessions and copies.

## Read Order

1. Read `live/AGENTS.md` before relying on anything under `docs/live/`.
2. Read `reference/AGENTS.md` before changing durable docs under `docs/reference/`.
3. Use the root guide for startup order and cross-subsystem precedence.

## Update Rules

- Keep template live docs inert.
- Record durable documentation policy in `docs/reference/*`.
- Do not add new local guides below `docs/` unless the subtree earns a durable boundary.

## Discovery Index

| Topic | Location |
|-------|----------|
| Live-doc scaffold rules | `live/AGENTS.md` |
| Reference-doc rules | `reference/AGENTS.md` |
