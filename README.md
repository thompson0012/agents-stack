# AI Agents Setup

Battle-tested configuration for AI coding agents.

## Documentation Structure

| Path | Purpose | Start Here |
|------|---------|------------|
| `AGENTS.md` | **Constitution** — behavior rules and protocols | ✅ Always read first |
| `/.agents/docs/GUIDELINES.md` | **Teaching Guide** — how to think and write docs | ✅ Read when writing docs |
| `/.agents/docs/PRD.md` | Product requirements (template) | Fill per project |
| `/.agents/docs/TECH_STACK.md` | Technology choices (template) | Fill per project |
| `/.agents/docs/PROGRESS.md` | Session state (template) | Update each session |
| `/.agents/docs/LESSONS.md` | Learned patterns (template) | Log corrections here |
| `/.agents/docs/MEMORY.md` | Architectural decisions (template) | Fill per project |
| `/.agents/docs/CODEMAP.md` | Architecture codemap — load at session start | Update after structural changes |
| `/.agents/docs/CHANGELOG.md` | System change log — load last 5 entries | Add entry after system changes |
| `/.agents/docs/OBJECTIVE_LEDGER.md` | Task objective schema and template | Create per non-trivial task |
| `/.agents/docs/SESSION_BOOTSTRAP.md` | Session startup protocol | Follow at every session start |
| `/.agents/docs/ledgers/` | Active task objective ledgers (one per task) | Create + update during tasks |
| `/.agents/roles/` | Agent role system prompts + swarm assignment protocol | Load when using multi-agent workflows |

**Domain-Specific** (fill based on GUIDELINES.md Part 3):
- `/.agents/docs/BACKEND.md` — Backend patterns
- `/.agents/docs/FRONTEND.md` — Frontend standards

## Installed Skills

| Path | Purpose |
|------|---------|
| `/.agents/skills/self-cognitive/SKILL.md` | Self-cognitive meta skill (verification, retrospectives, persistence) |
| `/.agents/skills/tailwind-design-system/SKILL.md` | Tailwind v4 design system and UI standardization |
| `/.agents/skills/remotion-best-practices/SKILL.md` | Remotion video creation best practices |
| `/.agents/skills/better-auth-best-practices/SKILL.md` | Better Auth integration guidance |
| `/.agents/skills/ui-ux-pro-max/SKILL.md` | UI/UX design intelligence and guidelines |
| `/.agents/skills/agent-browser/SKILL.md` | Browser automation CLI workflows |
| `/.agents/skills/web-design-guidelines/SKILL.md` | UI/UX review against Web Interface Guidelines |
| `/.agents/skills/brainstorming/SKILL.md` | Required pre-design brainstorming workflow |
| `/.agents/skills/reflexion-architect/SKILL.md` | Prompt architecture and reflexion-based optimization workflow |
| `/.agents/skills/skill-creator/SKILL.md` | Skill authoring guidance |
| `/.agents/skills/find-skills/SKILL.md` | Discover/install skills from skills.sh |
| `/.agents/skills/seedance2.0-prompt-skill/SKILL.md` | Generate production-ready video prompts for ByteDance Seedance 2.0 (即梦) |
| `/.agents/skills/context-compaction/SKILL.md` | Compact long sessions into a canonical state snapshot for handoff or continuation |

## Installed Roles

| Path | Purpose |
|------|---------|
| `/.agents/roles/swarm-coordinator.md` | Orchestrates task decomposition, assignment, and escalation |
| `/.agents/roles/researcher.md` | Gathers evidence and constraints before implementation |
| `/.agents/roles/implementer.md` | Executes approved changes with verification |
| `/.agents/roles/reflexion-architect.md` | Designs and refines SOTA prompts with recursive reflexion |
| `/.agents/roles/reviewer.md` | Runs severity-first reviews for risks/regressions |
| `/.agents/roles/verifier.md` | Validates acceptance criteria and completion |
| `/.agents/roles/assignment-protocol.md` | Shared handoff contract for swarm execution |

## Quick Start

### Option A — New project (scaffold from scratch)

```bash
# 1. Scaffold into a new directory (no git history, README excluded via degit.json)
npx degit labs21/agents-docs-kits my-project

# 2. Enter the directory and initialise git
cd my-project
git init
```

This copies `AGENTS.md`, `.agents/`, and all templates. `README.md` is automatically removed by `degit.json` so your project starts clean.

### Option B — Add to an existing project

```bash
# Clone the repo temporarily, then copy only what you need
git clone https://github.com/labs21/agents-docs-kits.git /tmp/agents-docs-kits

cp /tmp/agents-docs-kits/AGENTS.md ./AGENTS.md
cp -r /tmp/agents-docs-kits/.agents ./.agents

rm -rf /tmp/agents-docs-kits
```

### After scaffolding (both options)

1. **Read** `.agents/docs/GUIDELINES.md` — learn how to fill templates properly
2. **Fill** `PRD.md` and `TECH_STACK.md` with your project details
3. **Set** `AGENTS.md` as your AI tool's instruction/rules file
4. **Optionally fill** `BACKEND.md` / `FRONTEND.md` (see GUIDELINES.md Part 3)

### Learning Path for AI Agents

```
First Session:
AGENTS.md ──► Understand behavior rules
     │
     ▼
GUIDELINES.md ──► Learn how to think & write
     │
     ▼
Fill PRD.md, TECH_STACK.md ──► Establish project context

Ongoing:
PROGRESS.md ◄──► Update each session
LESSONS.md ◄──► Log when corrected
```

## Agent Processing Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      SESSION START                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  READ: AGENTS.md → PROGRESS.md → Risk-based tiered docs     │
│  LOAD: CODEMAP.md + last 5 CHANGELOG entries (architecture)  │
│  LOAD: Objective Ledger for current task                     │
│  ├─ Low:   Target files only                                │
│  ├─ Normal: + PRD.md, TECH_STACK.md                         │
│  └─ High:   + SECURITY.md, all relevant docs                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
            ┌────────────────────┐
            │   TASK CLASSIFY    │
            │  ┌──────────────┐  │
            │  │ ≤20 LOC,     │  │
            │  │ 1 file,      │──┼──► TRIVIAL? ──Yes──► EXECUTE
            │  │ no new       │  │                      │
            │  │ behavior     │  │                      No
            │  └──────────────┘  │                       │
            └────────────────────┘                       ▼
                                               ┌─────────────────┐
                                               │   CREATE PLAN   │
                                               │  - Goal/Scope   │
                                               │  - Tasks        │
                                               │  - Risks        │
                                               └────────┬────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  AWAIT APPROVAL │
                                               │ (unless AUTO-   │
                                               │  PILOT mode)    │
                                               └────────┬────────┘
                                                        │
                                                        ▼
┌───────────────────────────────────────────────────────┴──────┐
│                         EXECUTE                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Implement  │───►│   Verify    │───►│   Document      │  │
│  │  (atomic)   │    │  LSP/tests  │    │  PROGRESS.md    │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Success │ │  Error   │ │ Security │
    │   Done   │ │   ───►   │ │   Vuln   │
    └──────────┘ │ Diagnose │ │   ───►   │
                 │ Reproduce│ │   Stop   │
                 │  Retry   │ │   Warn   │
                 │          │ │Escalate  │
                 └──────────┘ └──────────┘
```

## Reading Flow

```
AGENTS.md → PROGRESS.md → [Tier-based docs]
```

- **Low risk**: Targets only
- **Normal risk**: + PRD.md, TECH_STACK.md
- **High risk**: + All relevant docs

## Key Concepts

- **Lazy Reading**: Read only what you need (tier-based)
- **Explicit Approval**: Plans need approval (unless AUTO-PILOT)
- **Template→Production**: Fill templates before relying on them
- **AGENTS.md First**: Always check constitution before other docs
- **GUIDELINES.md Teaches**: It's a tutorial, not just reference — explains HOW to think and write

### For AI Agents: How to Use This System

1. **Thinking**: See GUIDELINES.md Part 1 (The AI Mindset)
2. **Writing**: See GUIDELINES.md Part 2 (The Writing Process)
3. **Backend/Frontend**: See GUIDELINES.md Part 3 (Domain Guides)  
4. **Templates**: See GUIDELINES.md Part 4 (Document Templates)

See `AGENTS.md` for complete behavior rules.
