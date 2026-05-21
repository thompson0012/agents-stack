# Agents Stack

**A file-backed, adversarial, goal-QA-driven harness for AI agent orchestration.**

AI agents are powerful but unreliable. Without structure, they lose context between sessions, review their own work (badly), chase surface-level fixes without questioning the premise, and leave nothing durable behind when the chat ends.

Agents Stack fixes this by giving AI agents a **file-first operating system** — a harness that enforces adversarial review, enables cold-start recovery, and dispatches parallel specialists. The harness manages a linear spec→plan→tasks→implement→qa→release pipeline with explicit human approval gates and a three-layer rework model that traces failures to their root cause.

---

## What it can do

### Cold-start recovery
A fresh agent with zero chat history can read CONSTITUTION.md, AGENTS.md, and the workstream files in `.agents-stack/` to continue exactly where the previous agent left off. No context caching, no prompt stuffing, no lost progress.

### Adversarial quality control
The harness enforces **Generator ≠ Auditor**: the agent that builds a solution is never the one that verifies it. QA is an independent phase run by a separate worker against the SPEC's Acceptance Criteria.

### Three-layer rework
When QA finds issues, root cause is traced to one of three layers:

1. **L1 (code)** — implementation bug → back to implement phase
2. **L2 (architecture)** — design flaw → back to plan phase
3. **L3 (requirement)** — missing edge case → back to spec phase

A retry fixes execution at the same layer; an iteration questions the premise and goes deeper.

### Parallel specialist dispatch
The orchestrator routes work to the right specialist at the right time — explorer for codebase search, librarian for external docs, oracle for architectural decisions, fixer for bounded implementation, designer for UI/UX. Independent work runs in parallel.

### Structured handoffs
When one agent hands work to another (or the same role continues after a context reset), a structured handoff.md captures artifacts, decisions, constraints, and the next concrete action. No conversation dumps, no re-litigation of settled decisions.

### Extensible skill system
18+ reusable skill packages ship with the stack (reasoning, frontend design, backend & frontend QA, greenfield product development, market scouting, brand extraction, meta-prompting, and more). Create your own leaf skills or router skills with built-in authoring tools.

### Human escalation gates
When agents exceed retry budgets or reach depth limits, the harness has clear escalation paths (`awaiting_human`, `escalated_to_human`) instead of silently producing garbage.

---

## What it can't do

### Replace human judgment
The harness provides structure, adversarial review, and escalation paths — but it doesn't pretend AI review is perfect. LLM reviewers are biased toward agreement and struggle with multi-step verification. Critical decisions still need human eyes.

### Guarantee correct output
Adversarial review raises the quality floor, but it doesn't eliminate hallucination or logical errors. The harness makes failures *detectable and recoverable*, not impossible.

### Execute without files
This is a **file-first** system. If you delete or corrupt the harness files, state is lost. The harness depends on `.agents-stack/tracked-work.json` and per-workstream artifacts being on disk.

### Work as a plug-and-play library
Agents Stack is a **scaffold and methodology**, not an npm package. You copy the template into your project and customize it. It requires commitment to the file-backed workflow.

### Handle multiple concurrent workstreams
By design, only **one workstream is active at a time** — this prevents routing ambiguity. If you need true parallel workstreams, run them in separate git worktrees.

---

## Getting started

### Option A: Copy from a local clone

```sh
git clone https://github.com/labs21-dev/agents-stack.git
cp -R agents-stack/ .agents-stack/
```

### Option B: Scaffold directly from GitHub

```sh
npx degit labs21-dev/agents-stack my-project
```

### What to do after scaffolding

1. Set the project name in `.agents-stack/tracked-work.json`
2. Fill in `.agents-stack/reference/architecture.md` and `.agents-stack/reference/design.md` with your project's truth
3. Read CONSTITUTION.md and AGENTS.md at the repo root
4. Add the first workstream only when it is real, bounded, and ready to track

---

## How it works

### The six phases

```
spec → plan → tasks → implement → qa → release
```

Each phase produces a durable file in `.agents-stack/<workstream-id>/`. The orchestrator checks which files exist and routes to the next phase automatically.

| Phase | Output | Purpose |
|-------|--------|---------|
| spec | spec.md | What & Why: goal, stories, edge cases, BDD ACs |
| plan | plan.md | How: architecture, API, DB, impact analysis, test strategy |
| tasks | tasks.md | Task breakdown with 5-dimension verification |
| implement | code + handoff.md | RED-GREEN-REFACTOR per task, each passes before next |
| qa | qa-report.md | Independent verification against SPEC |
| release | changelog.md | Changelog, reference update, archive |

### Core invariants

| Invariant | What it means |
|-----------|---------------|
| Files beat chat memory | A cold-start agent recovers state from disk, not conversation history |
| One active workstream | Prevents routing ambiguity and context fragmentation |
| Generator ≠ Auditor | The builder never verifies its own work |
| Iteration ≠ Retry | A retry fixes execution at the same layer; an iteration questions the premise |
| Cold start must work | Resuming from zero chat history is the design standard, not an edge case |

### The orchestrator

The orchestrator is the only agent that communicates with the user and the only agent allowed to delegate. Workers execute exactly one phase in a clean context and return. This keeps each worker's task bounded and reviewable.

---

## File layout

```
├── CONSTITUTION.md             # Technical charter — invariants, rules, rework model
├── AGENTS.md                   # Orchestrator resume anchor (quick-resume guide)
├── RTK.md                      # Orchestrator runbook (role, agents, workflow)
├── .agents-stack/
│   ├── tracked-work.json       # Workstream registry and backlog
│   ├── reference/              # Stable project knowledge (read-optimized)
│   │   ├── methodology.md      # Methodology overview
│   │   ├── architecture.md     # Project architecture (fill in)
│   │   └── design.md           # Product design intent (fill in)
│   ├── insights/               # Session retrospectives
│   ├── archive/                # Completed workstreams
│   └── <workstream-id>/        # Active workstream state
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── handoff.md
│       ├── qa-report.md
│       ├── changelog.md
│       └── status.json
├── .agents/skills/             # Active skill packages
├── .agents/agents/             # Agent role definitions
└── skills-optional/            # Domain-specific optional skills
```

---

## Should I use this?

Use Agents Stack if you:

- Work on complex, multi-session projects with AI agents
- Want durable state that survives context resets
- Need adversarial review to catch agent self-deception
- Value structured delegation over monolithic prompting
- Want a methodology, not just a tool

Skip it if you:

- Need a quick one-off answer or script
- Don't want to maintain file-backed state
- Prefer a linear, chat-driven workflow
- Are working on something a single prompt can handle
