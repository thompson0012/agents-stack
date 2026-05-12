# Agents Stack

**A file-backed, adversarial, spiral-resumable harness for AI agent orchestration.**

AI agents are powerful but unreliable. Without structure, they lose context between sessions, review their own work (badly), chase surface-level fixes without questioning the premise, and leave nothing durable behind when the chat ends.

Agents Stack fixes this by giving AI agents a **file-first operating system** — a harness that manages understanding depth, enforces adversarial review, enables cold-start recovery, and dispatches parallel specialists. The harness doesn't just track tasks; it tracks how a problem's understanding evolves from vague confusion to a validated framework.

---

## What it can do

### Cold-start recovery
A fresh agent with zero chat history can read 4–5 files and continue exactly where the previous agent left off. No context caching, no prompt stuffing, no lost progress.

### Adversarial quality control
The harness enforces **Generator ≠ Auditor**: the agent that builds a solution is never the one that verifies it. Claims are challenged by independent reviewer agents (oracle, council) before they reach the user.

### Spiral understanding
Work doesn't flow linearly. The harness models it as a three-layer spiral:

1. **Direction** — form a falsifiable thesis, then challenge it adversarially
2. **Method** — design tactical responses to gaps, then synthesize them into a coherent framework
3. **Action** — contract-bounded build, then independent audit

An audit that uncovers a deeper insight triggers a **spiral turn** — not a retry, but a return to a new thesis with greater depth. This is how the harness manages understanding, not just task completion.

### Parallel specialist dispatch
The orchestrator routes work to the right specialist at the right time — explorer for codebase search, librarian for external docs, oracle for architectural decisions, council for multi-model consensus, fixer for bounded implementation, designer for UI/UX. Independent work runs in parallel.

### Structured handoffs
When one agent hands work to another (or the same role continues after a context reset), a structured JSON payload captures artifacts, decisions, constraints, and the next concrete action. No conversation dumps, no re-litigation of settled decisions.

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
This is a **file-first** system. If you delete or corrupt the harness files, state is lost. The harness depends on `plan.md`, `tracked-work.json`, and per-workstream artifacts being on disk.

### Work as a plug-and-play library
Agents Stack is a **scaffold and methodology**, not an npm package. You copy the template into your project and customize it. It requires commitment to the file-backed workflow.

### Handle multiple concurrent workstreams
By design, only **one workstream is active at a time** — this prevents routing ambiguity. If you need true parallel workstreams, run them in separate git worktrees.

---

## Getting started

### Option A: Copy from a local clone

```sh
git clone https://github.com/labs21-dev/agents-stack.git
cp -R agents-stack/templates/. my-project
cd my-project
./docs/scripts/init.sh
```

### Option B: Scaffold directly from GitHub

```sh
npx degit labs21-dev/agents-stack/templates my-project
cd my-project
./docs/scripts/init.sh
```

### What to do after scaffolding

1. Set the project name in `docs/live/tracked-work.json`
2. Record the real source goal in `docs/live/plan.md`
3. Fill in `docs/reference/architecture.md` and `docs/reference/design.md` with the truth of your project
4. Add the first backlog item only when it is real, bounded, and ready to track

---

## How it works

### The seven phases

```
thesis → challenge → response → synthesis → contract → build → audit
```

Each phase produces a durable file in `.harness/<workstream-id>/`. The orchestrator checks which files exist and routes to the next phase automatically.

### Core invariants

| Invariant | What it means |
|-----------|---------------|
| Files beat chat memory | A cold-start agent recovers state from disk, not conversation history |
| One active workstream | Prevents routing ambiguity and context fragmentation |
| Generator ≠ Auditor | The builder never verifies its own work |
| Spiral turn ≠ Retry | A retry fixes execution; a spiral turn questions the premise |
| Cold start must work | Resuming from zero chat history is the design standard, not an edge case |

### The orchestrator

The orchestrator is the only agent that communicates with the user and the only agent allowed to delegate. Workers execute exactly one phase in a clean context and return. This keeps each worker's task bounded and reviewable.

---

## File layout

```
├── AGENTS.md                  # Repo constitution and harness rules
├── RTK.md                     # Orchestrator runbook (role, agents, workflow)
├── docs/
│   ├── live/
│   │   ├── plan.md            # Resume anchor (Why / What / Next)
│   │   └── tracked-work.json  # Workstream registry and backlog
│   └── reference/
│       ├── architecture.md    # Project architecture (fill in)
│       └── design.md          # Product design intent (fill in)
├── .harness/<workstream-id>/  # Active sprint state
│   ├── thesis.md
│   ├── challenge.md
│   ├── response.md
│   ├── synthesis.md
│   ├── contract.md
│   ├── handoff.md
│   ├── audit.md
│   └── status.json
├── .agents/skills/            # Active skill packages
├── .agents/agents/            # Agent role definitions
└── skills-optional/           # Domain-specific optional skills
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
