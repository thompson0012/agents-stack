# agents-docs-kits

Minimal agent docs kit for context injection, progressive disclosure, and reliable hand-off in a single worktree.

## What this repo is

This repository is a template-first docs kit for projects that want a small, durable agent memory structure.

- `AGENTS.md` is the only always-injected index.
- `docs/live/` stores the current execution state.
- `docs/reference/` stores durable project context.
- `templates/base/` contains the generic starter files used to initialize a new project.

## Generated project files

The base template generates this structure:

```text
.
├── AGENTS.md
└── docs/
    ├── live/
    │   ├── current-focus.md
    │   ├── todo.md
    │   └── progress.md
    └── reference/
        ├── implementation.md
        ├── design.md
        ├── architecture.md
        ├── codemap.md
        ├── memory.md
        └── lessons.md
```

This repository also includes:

- `README.md` to explain the kit itself
- `templates/base/` to hold the reusable scaffold
- `degit.json` for a narrow repo-level cleanup case when scaffolding from the repository root

## How progressive disclosure works

Read only the smallest set of docs needed for the task:

1. Start with `AGENTS.md`.
2. Read `docs/live/current-focus.md` for the active objective.
3. Read `docs/live/progress.md` for continuity and latest verification.
4. Read `docs/live/todo.md` only when choosing the next action.
5. Read `docs/reference/implementation.md` or `docs/reference/design.md` only when the work needs them.

The goal is to keep the default context small while still making deeper project knowledge retrievable on demand.

## First useful run

Pick the stage that matches your situation. Stop as soon as it gives you what you need — you do not have to run every stage.

- **Problem or goal is unclear** — use `using-reasoning` to frame the problem, map assumptions, and stress-test an approach before committing to a direction.
- **Non-trivial software feature work needs lifecycle guidance** — use `software-delivery` to route across discovery, harness control, plan review, implementation handoff, independent frontend evaluation, and ship-readiness checks.
- **Need requirements before building** — use `feature-spec` to draft scope, acceptance criteria, and open questions for any feature or project.
- **Coding or data work in an existing repo** — use `coding-and-data` to hand off structured implementation or analysis tasks to a focused subagent.
- **Building a web project** — use `website-building` to route to the right child skill for informational sites, full-stack apps, or browser games.
- **Risky or irreversible step ahead** — use `self-cognitive` for a preflight confidence check, repeatable-workflow extraction, or postmortem.

Not sure which applies? Use `using-agent-practices` — it routes to the narrowest skill that matches your request.

## Initialize a project from the template

Primary and recommended path: scaffold from `templates/base` so the new project gets only the starter docs.

```bash
npx degit <owner>/<repo>/templates/base my-project
```

Then fill in:

- `AGENTS.md` with your project-specific retrieval contract
- `docs/live/*` with current execution state
- `docs/reference/*` with durable implementation and product context

## Secondary root-scaffold cleanup note

- The root `README.md` is repository documentation for this kit, not part of the recommended generated project.
- If someone scaffolds from the repository root instead of `templates/base`, `degit.json` keeps that narrower flow from carrying the repo-level `README.md` into the generated project.
