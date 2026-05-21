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

### v3.1 — Stabilization
- [ ] Dogfood: run agents-stack own development through its own pipeline
- [ ] Fix cold-start edge cases found during dogfooding
- [ ] Improve QA adversarial detection (false pass prevention)

### v3.2 — Integration
- [ ] GitHub Actions template for CI
- [ ] Git worktree helpers for parallel workstreams
- [ ] VSCode/Cursor extension with file tree visualization

### v4 — Multi-Agent
- [ ] Native multi-agent workstream support
- [ ] Parallel task execution within same workstream
- [ ] Inter-agent communication protocol
