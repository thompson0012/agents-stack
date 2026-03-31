# Agent Packages Guide

This `AGENTS.md` extends `../AGENTS.md`. Root constitutional rules cannot be overridden.

## Local Scope

This subtree defines the template's bundled agent packages.

- `skills/` contains the shipped top-level skill packages in this template.
- `skills-optional/` contains optional top-level skill packages that ship in the template but are not part of the default bundled surface.

## Read Order

1. Read `skills/AGENTS.md` before acting under `.agents/skills/`.
2. Read `skills-optional/AGENTS.md` before acting under `.agents/skills-optional/`.
3. Use the root guide for startup order and cross-subsystem precedence.
