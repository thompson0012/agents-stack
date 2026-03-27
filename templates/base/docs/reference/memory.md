# Memory

Read for durable truths worth preserving across sessions. Do not store transient status here.

## Durable Truths

- Truth:
- Why it persists:

## Decisions to Preserve

- Decision: `using-agent-practices` is the canonical top-level discoverability router for the template skill suite, and its `references/category-map.md` inventory must stay in sync with every live top-level skill under `templates/base/.agents/skills/`.
- Preserve because: missing standalone leaves in the top-level router create silent discovery holes even when the skills themselves are valid and present on disk.
- Revisit only if: the template adopts a different top-level discovery mechanism or moves standalone specialist skills behind a new explicit family router.

- Decision: roadmap-driven work must preserve source goal, plan goal, and current phase goal in `docs/live/roadmap.md`, and goal changes must retire the old goal explicitly instead of overwriting it silently.
- Preserve because: phased delivery drifts when the agent reconstructs intent from chat memory after compaction.
- Revisit only if: the repository stops using roadmap-led phased execution or adopts a different authoritative goal lineage artifact.
