# ROADMAP

## Vision
agents-stack 的目標是成為 AI 原生開發的最佳實踐 harness — 一套讓 AI agent 能夠可靠地產出高品質軟體的工作流系統。

## Current Status: v3 (Goal-QA-Driven)
- [DONE] Replace spiral model with spec→plan→tasks→implement→qa→release pipeline
- [DONE] .agents-stack/ as single canonical state root (was .harness/ + docs/ split-brain)
- [DONE] 5-dimension task verification in tasks.md
- [DONE] Three-layer rework model (L1 code / L2 plan / L3 spec)
- [DONE] CONSTITUTION.md technical charter

## Next

### v3.1 — Stabilization & Quick Wins
- [ ] Dogfood: run agents-stack own development through its own pipeline
- [ ] Fix cold-start edge cases found during dogfooding
- [ ] Improve QA adversarial detection (false pass prevention)
- [ ] Decision log (`decisions.md`) — record why choices were made, traceable across phases
- [ ] Encoded decision principles in CONSTITUTION.md — reduce human-in-the-loop for routine decisions
- [ ] Fat skills resolver in AGENTS.md (partial — resolver table added, needs auto-dispatch refinement)

### v3.2 — Process & Infrastructure
- [ ] GitHub Actions template for CI
- [ ] **CI enforcement gates** — pre-commit hooks and CI checks that verify TDD (RED phase evidence), 5-dimension coverage, and QA reproduce gate before merge. Automates what v3.1 added as SKILL.md enforcement. (was "Prune-review pipeline gate" — deprecated after prune-review v2 analysis found it over-engineered)
- [ ] Git worktree helpers for parallel workstreams
- [ ] VSCode/Cursor extension with file tree visualization
- [ ] **Agent context auto-sync** — sync reference/ + workstream state across phase transitions so workers always get fresh context (SpecKit-inspired)
- [ ] **Templated artifact system** — extract templates from SKILL.md inline code blocks into `.agents-stack/templates/` for independent versioning (SpecKit-inspired)
- [ ] **Stuck/idle self-detection** — agent-side timeout protocol with diagnostics before escalating (GSD-inspired)

### v3.3 — Architecture (需詳細設計後再實作)
- [ ] **Compact protocol / phase-level rotation** — introduce `compass.md` to compact orchestrator context after each phase; reduce context rot without requiring session-level rotation (GSD-inspired)
- [ ] **Three-layer memory model formalization** — reference/ as durable knowledge, decisions.md as operational state, session as ephemeral context (GBrain-inspired)
- [ ] **Multi-model routing** — annotate workstream config with per-phase model preference (GStack-inspired)

### v4 — Multi-Agent + Browser QA
- [ ] Native multi-agent workstream support
- [ ] Parallel task execution within same workstream
- [ ] Inter-agent communication protocol
- [ ] **Browser QA daemon** — persistent Chromium daemon for sub-second frontend QA, with cookie persistence and idle shutdown (GStack-inspired)
