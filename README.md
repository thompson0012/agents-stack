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
