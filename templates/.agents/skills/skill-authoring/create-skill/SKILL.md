---
name: create-skill
description: Use when creating or upgrading a reusable skill package — leaf or router. Covers scaffolding, SKILL.md authoring, resource bundling, and validation. Does not cover agent manifest creation (use create-agents for that).
---

# Create Skill

Use this skill to create or upgrade a reusable skill package that another agent can discover and apply across runtimes.

Build the portable core first. Add runtime-specific metadata or tooling only after the core package works without vendor assumptions.

## Decision Tree

```
What kind of skill do you need?
├─ Leaf skill (single task guidance) ─────────────→ Follow DEFAULT path
├─ Router skill (selects among children) ──────────→ Follow "Router Variant" callouts
└─ Agent manifest (reusable agent profile) ────────→ Use `create-agents`; return here
```

> **Default to leaf.** Most skills should be leaf skills. A router is justified only when you have 3+ related child skills that need explicit selection and fallback behavior. When in doubt, make it a leaf.

## Before You Start (Entry Gate)

Before writing files, answer:

1. **Single responsibility** — What single repeatable job does this skill solve?
2. **Concrete evidence** — What task fails, repeats, or degrades without this skill?
3. **Consumer view** — What does the user provide? What should the skill produce?
4. **Fragility** — How fragile is the workflow (low / medium / high)? This determines instruction specificity.

If you cannot answer these from the request and repo context, ask the smallest focused question needed.

## Default Path: Leaf Skill

### Phase 1 — Define the boundary

Create a skill only when **all** of these are true:

- the workflow will recur
- another agent would benefit from the same guidance
- the behavior is broader than one repository convention
- the knowledge is procedural, domain-specific, or tool-specific enough to matter

Do not create a skill for:

- a one-off task summary
- repo-local instructions better kept in AGENTS.md or project docs
- obvious best practices with no special context (the agent already knows these)

### Phase 2 — Choose the smallest useful package

Start with the smallest shape that honestly covers the job:

```text
SKILL.md only                 → simple, stable workflow
SKILL.md + references/        → heavy or conditional detail (progressive disclosure)
SKILL.md + scripts/           → repeated deterministic code or fragile execution
SKILL.md + assets/            → templates, starter files
```

Do not add `scripts/`, `references/`, or `assets/` upfront. Add them only when a concrete need arises during refinement. The scaffolding scripts (`scripts/scaffold.py`, `scripts/validate.py`, etc.) are optional helpers — the skill works without them.

### Phase 3 — Author SKILL.md

#### Frontmatter

```yaml
---
name: skill-name
description: Use when [trigger conditions and symptoms].
---
```

Rules:

- `name` must match the directory name exactly (lowercase, hyphens).
- Keep `description` under 1024 characters. Focus on **trigger conditions**, not the workflow. Start with "Use when...". (See agentskills.io spec.)
- Add `version`, `license`, `compatibility`, or `metadata` only when the target runtime requires them.

#### Body

Write for fast scanning and reliable execution. Recommended section order:

1. `# Title` + short overview (1-2 sentences, what problem this skill solves)
2. Core contract or non-negotiables (must-read rules)
3. Workflow or phase-by-phase steps (the how)
4. References to bundled files when needed
5. Final checklist or failure modes

Match instruction specificity to fragility:

| Fragility | Style |
|---|---|
| Low (multiple valid approaches) | Describe what to look for, not exact steps |
| Medium | Provide default tool/approach + brief alternatives |
| High (brittle, must match exact sequence) | Prescriptive step-by-step, no room for interpretation |

**Provide defaults, not menus.** When multiple tools could work, pick one and mention alternatives briefly. (See agentskills.io best practices.)

### Phase 4 — Bundle resources (only when justified)

Add resources only when they solve a real problem not addressable in SKILL.md prose:

| Directory | Use for | When |
|---|---|---|
| `references/` | Selection rules, edge cases, domain schemas, platform notes | When detail exceeds ~100 lines |
| `scripts/` | Deterministic steps the agent would otherwise rewrite or execute inconsistently | When you catch the agent reinventing the same logic each run |
| `assets/` | Starter templates meant to be copied, not read as instructions | When the output format needs a template |

Keep references one hop deep — `[details](references/eval.md)` is good; nested chains are not. (Progressive disclosure principle from agentskills.io spec: files load on demand, not upfront.)

### Phase 5 — Validate

Run the bundled validator if it exists:

```bash
python3 scripts/validate.py <skill-dir>
```

If no validator exists, verify manually:

- [ ] `name` matches directory name exactly
- [ ] `description` starts with "Use when" and describes triggers, not workflow
- [ ] SKILL.md stays focused on execution guidance
- [ ] All linked local files exist
- [ ] No dead code, unused references, or speculative scaffolding

## Router Variant

If the decision tree routed you here (the skill's main job is selecting among child skills), follow the same 5 phases with these adjustments.

### When it's really a router

A router is justified when **all** of these are true:

- the package's main job is choosing among child skills, not performing the work itself
- the child set forms a stable family worth naming (3+ related skills)
- discovery or routing fails without an explicit family entrypoint
- the relationships between children matter enough to record metadata

Do not create a router for:

- a single leaf skill (make it a leaf instead)
- a loose category page with no decision logic
- a folder tree that exists only for visual organization (name prefixes are enough)

### Phase 2 changes (package shape)

Default router shape:

```text
router-name/
├── SKILL.md
├── references/
│   ├── children.json       ← required: child inventory with selection metadata
│   ├── router-metadata.md  ← optional: field reference for children.json
│   └── relationship-types.md ← optional: requires/recommends/fallbacks_to definitions
├── assets/
│   ├── router-skill-template.md  ← optional: starter SKILL.md for routers
│   └── children-template.json    ← optional: starter children.json
├── scripts/
│   └── validate_router.py        ← optional: validate router metadata
├── child-one/SKILL.md
└── child-two/SKILL.md
```

The `references/children.json` is the source of truth for: selection order, child summaries, route-when signals, dependencies, install hints, and explicit fallbacks. Keep child inventory there, not in SKILL.md. The bundled `router-metadata.md` and `relationship-types.md` references explain the metadata schema and relationship types in detail — read them alongside `children-template.json` when authoring a router.

### Phase 3 changes (SKILL.md body)

The router SKILL.md should cover only:

1. Family boundary — what domain does this router own?
2. Selection order — in what order should children be considered?
3. Child inventory — link to `references/children.json` (do not duplicate inline)
4. Missing/install/fallback policy — what happens when the best child is absent?
5. Router output format — the handoff contract

A good router output:

- `Route to router-name/child-a.`
- `Install router-name/child-a, then route to router-name/child-a.`
- `Fallback to router-name/child-b.`
- `No family child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit.

### Phase 5 changes (validation)

```bash
python3 scripts/validate_router.py <router-dir>   # if bundled
```

Manual router checks:

- [ ] SKILL.md covers only selection, handoff, and fallback — no child execution
- [ ] `references/children.json` is the current source of truth for child metadata
- [ ] Missing/install/fallback behavior is explicit and honest
- [ ] Each child self-identifies as a nested child of this router family
- [ ] All child SKILL.md files exist

## Eval (Optional, On-Demand)

Do not create eval files during the first pass. Add them only when:

- you need to compare skill output against a baseline
- trigger precision matters and the description isn't reliable enough

When evals are justified, follow the structure in [evaluation](references/evaluation.md) and [evals template](assets/evals-template.json). The pattern:

1. Direct match (obvious trigger)
2. Ambiguous near miss (adjacent request)
3. Noisy case (distractions, misleading keywords)

Compare the candidate against a believable baseline (no skill, old skill, or default workflow). Patch only the missing instruction — do not bloat.

## Security (Optional)

If the skill includes scripts, external network access, or file system writes, review [security](references/security.md). Minimum checks:

- No secrets hardcoded
- No script writes outside intended paths
- No hidden network calls
- Remote content treated as untrusted input

## Final Checklist

- [ ] The skill solves one repeatable job (not a one-off)
- [ ] `name` matches directory name exactly
- [ ] `description` starts with "Use when" and describes triggers, not workflow
- [ ] SKILL.md stays focused on execution guidance (under 500 lines)
- [ ] Heavy detail lives in `references/`, `scripts/`, `assets/` only when justified
- [ ] All linked local files exist
- [ ] Router variants: `references/children.json` is current; no child execution inline
- [ ] No dead code, unused references, or speculative scaffolding
