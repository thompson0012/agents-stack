# Agents Stack Starter

This scaffold is a file-backed agents-stack project.

If you are already inside the generated scaffold, skip the copy step and run `./docs/scripts/init.sh`.

```sh
# From the starter source, copy the scaffold into a clean project directory.
cp -R templates/. my-project
cd my-project

# Create any missing baseline files and directories without overwriting work.
./docs/scripts/init.sh
```

If you want to clone the starter from GitHub instead of copying locally:

```sh
npx degit thompson0012/agents-stack/templates new-project && cd new-project && ./docs/scripts/init.sh
```

After that, the repo is ready for truthful initialization work.

The copied scaffold starts blank: no active sprint, no archive history, and no seeded feature backlog.

## What to edit first

1. Set the project name in `docs/live/tracked-work.json`.
2. Record the real source goal in `docs/live/roadmap.md` and `docs/live/current-focus.md`.
3. Add the first backlog item only when it is real, bounded, and ready to track.
4. Fill in `docs/reference/architecture.md` and `docs/reference/design.md` with the truth of the new project.

## What lives where

- `AGENTS.md` — the repo constitution and harness rules.
- `docs/live/tracked-work.json` — the authoritative backlog and single runnable-sprint selector.
- `docs/live/ideas.md` — pre-sprint exploration and rejected directions.
- `docs/live/progress.md` — reviewed outcomes and durable next actions.
- `docs/live/memory.md` — durable lessons captured after compounding.
- `docs/reference/*` — stable architecture and design intent.
- `.harness/<feature-id>/` — sprint-local execution state.
- `docs/archive/*` — finished sprint history.

## Normal harness flow

`project-initializer -> generator-brainstorm -> generator-proposal -> evaluator-contract-review -> generator-execution -> adversarial-live-review -> state-update -> compound-capture`

Keep exactly one runnable sprint at a time. If `docs/live/tracked-work.json` is missing or untrustworthy, start with `project-initializer`.

## Notes

- `./docs/scripts/init.sh` is safe to run repeatedly; it only creates missing baseline files.
- `docs/live/tracked-work.json` is the source of truth for what is runnable right now.
- `docs/live/ideas.md` is not a runnable schedule.
