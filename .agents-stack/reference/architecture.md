# Architecture — agents-stack v3

## Overview

agents-stack is an AI-native development harness/methodology (not an npm package).
Design goal: enable AI agents to reliably produce high-quality software in a file-first workflow.

## Core Design

### Phase Pipeline

```
spec → plan → tasks → implement → qa → release
```

Each phase produces a durable artifact in `.agents-stack/<workstream-id>/`.

### State Root

`.agents-stack/` is the single canonical state root.
No split-brain between `.harness/` and `docs/`.

### Orchestrator-Worker Model

- Orchestrator: reads state, decides phase, dispatches worker
- Worker: executes one phase, produces artifact, returns
- Dispatch by artifact existence — which artifact is missing determines next phase

### Adversarial Separation

Implement and QA must be different worker instances.
This enforces the Generator ≠ Auditor invariant.

## Key Files

| Path | Purpose |
|------|---------|
| `CONSTITUTION.md` | Technical charter: invariants, rules |
| `AGENTS.md` | Orchestrator resume anchor |
| `.agents-stack/tracked-work.json` | Workstream registry |
| `.agents-stack/<id>/` | Active workstream artifacts |
| `.agents/skills/using-agents-stack/` | Router + phase skills |
