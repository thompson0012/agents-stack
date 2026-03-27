# Memory

Read for durable truths worth preserving across sessions. Do not store transient status here.

## Durable Truths

- Truth:
- Why it persists:

## Decisions to Preserve

- Decision: `using-agent-practices` is the canonical top-level discoverability router for the template skill suite, and its `references/category-map.md` inventory must stay in sync with every live top-level skill under `templates/base/.agents/skills/`.
- Preserve because: missing standalone leaves in the top-level router create silent discovery holes even when the skills themselves are valid and present on disk.
- Revisit only if: the template adopts a different top-level discovery mechanism or moves standalone specialist skills behind a new explicit family router.

- Decision: `templates/base/docs/live/` are template skeletons only; actual runtime state belongs in the consuming project's `docs/live/`.
- Preserve because: populating the template repo's live docs with real session state confuses reusable templates with actual project memory.
- Revisit only if: the repository stops being a template source and becomes the runtime workspace itself.

- Decision: `harness-design` owns execution-mode contracts, retry ceilings, live-doc integrity, and out-of-scope evaluation routing, while `multi-phase-control` remains the orchestration layer for preserving roadmap intent across phases.
- Preserve because: the two skills solve adjacent but distinct problems, and keeping them separate avoids a bloated single skill.
- Revisit only if: the family is intentionally collapsed into one broader control skill.

- Decision: `software-delivery/multi-phase-control` is the canonical leaf for phase-gated roadmap persistence and drift prevention, and `software-delivery` routes to it before `harness-design` when preserving original intent across phases is the primary need.
- Preserve because: multi-phase work fails when original intent lives only in chat context instead of an explicit persistence workflow.
- Revisit only if: phase preservation becomes part of another router or a new control model replaces the current multi-phase workflow.
