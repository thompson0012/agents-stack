# Agent Practices Category Map

This repository's live first-party suite under `templates/base/.agents/skills/` currently contains these skills.

## Suite Router

- `using-agent-practices` — top-level discoverability router for first-party skills when the right leaf skill or family router is not obvious yet

## Orchestration and Continuity

- `context-compaction` — compact session state for handoff or continuation
- `self-cognitive` — verify reasoning, run retros, and extract repeatable workflows

## Prompt and Spec Artifact Creation

- `meta-prompting` — design or evaluate a prompt artifact such as a system prompt, prompt template, prompt architecture, rubric, or eval plan
- `prompt-augmentation` — enrich a sparse prompt or generate prompt variants for text, image, or video generation while preserving the user's core subject
- `feature-spec` — draft or review a PRD, feature spec, or requirements document before implementation

## Skill Authoring

- `create-skill` — create or upgrade a reusable leaf skill package, scaffold a portable skill directory, or rewrite skill guidance into a reusable package
- `create-router-skill` — create or upgrade a discoverable router skill whose main job is selecting among child skills, carrying explicit child metadata, and handling install-or-fallback behavior honestly

Use `create-skill` when the package's job is one repeatable workflow. Use `create-router-skill` only when the package's job is family routing.

## Support Operations

- `cx-ticket-triage` — categorize support tickets, assign priority/SLA, check duplicates, and route the next owner

## Software Delivery Routing

Route through `software-delivery` when the request is non-trivial software feature work and the user needs lifecycle guidance across discovery, harness control, plan review, independent frontend evaluation, implementation handoff, or ship-readiness.

- `software-delivery/feature-discovery` — turn a fuzzy feature idea or change request into a clear problem statement, wedge, and next-step recommendation
- `software-delivery/multi-phase-control` — set up persistence structure and phase gates for multi-phase work that must preserve original intent across context resets
- `software-delivery/harness-design` — choose the honest delivery-control mode across single-session work, compacted continuation, or planner/generator/evaluator execution with explicit handoffs
- `software-delivery/plan-product-review` — challenge a plan on user value, scope, sequencing, and MVP shape before implementation
- `software-delivery/plan-engineering-review` — challenge a plan on architecture, failure modes, rollback, tests, and observability before implementation
- `software-delivery/plan-design-review` — challenge a plan on UX flows, states, accessibility, and interface clarity before implementation
- `software-delivery/frontend-evaluator` — provide strict independent browser-facing acceptance with evidence, defects, and retry guidance after implementation exists
- shared companions remain top-level: `feature-spec` for scoped artifacts, `coding-and-data` for repo-backed execution, `website-building` for web build or builder-side browser QA, and `self-cognitive` for confidence checks or retrospectives

## Code and Data Work

- `data-exploration` — profile unfamiliar datasets, assess quality, infer grain and joins, document schema, and surface anomalies or meaningful segments before downstream analysis
- `visualization` — choose chart types, write Python visualization code, and apply chart-specific accessibility guidance
- `coding-and-data` — route repo-backed coding, debugging, refactors, or other generic execution to a focused implementation subagent

Keep dataset profiling and schema discovery in `data-exploration` instead of collapsing them into generic `coding-and-data`. Keep chart-type selection, plotting code, and chart-specific accessibility in `visualization`; use `using-design/design-foundations` when the request is only about palette, typography, spacing, or broad chart styling.

## Commercial Reality Testing

- `startup-pressure-test` — pressure-test a startup, launch thesis, or business model with market, funnel, monetization, and runway realism

## Design Workflow Routing

Route through `using-design` when the request is broadly about a visual system, design stack, or design-family selection and could plausibly fit more than one of these:

- `using-design/design-foundations` — choose colors, typography, spacing, chart styling, and general visual-system defaults when no project-specific system already governs the work
- `using-design/generating-design-tokens` — turn brand inputs into a design token spec or brand system
- `using-design/generative-ui` — build or evaluate model-generated browser UI with sandboxed HTML, typed component schemas, or streamed UI
- `using-design/liquid-glass-design` — implement or evaluate experimental liquid-glass UI effects in the browser

Normal site, app, or browser-game builds still route through `website-building` even when visual polish, art direction, or interaction taste are major concerns.

## Media Generation and Transcription

- `media` — use the harness media CLI for image or video generation, text-to-speech, and audio or video transcription

Keep PDF, Word, PowerPoint, Excel, OCR, and other document-artifact workflows in `using-documents` even when pages are rendered to images or audio/video files are embedded in the source material.

## Web Project Routing

Route through `website-building` when the request could plausibly fit more than one of these:

- `website-building/informational` — build content-first sites such as portfolios, landing pages, editorial sites, blogs, and small-business pages
- `website-building/webapp` — build fullstack or app-like web products such as SaaS tools, dashboards, admin panels, and ecommerce apps
- `website-building/game` — build browser games and real-time interactive web experiences

## Document Workflow Routing

Route through `using-documents` when the request could plausibly fit more than one of these:

- `using-documents/docx` — create or edit editable Word documents, tracked changes, or PDF-to-Word conversions
- `using-documents/pdf` — fill, extract, OCR, render, split, merge, or otherwise manipulate fixed-layout PDFs
- `using-documents/pptx` — create, edit, or QA slide decks and presentation templates
- `using-documents/xlsx` — create, update, or debug spreadsheet workbooks, formulas, pivots, and workbook automation

## Legal Workflow Routing

Route through `using-legal` when the request could plausibly fit more than one of these:

- `using-legal/contract-review` — review and redline commercial agreements against a negotiation playbook
- `using-legal/legal-compliance` — support operational privacy-compliance work such as DPAs, DSARs, breach timing, transfers, and regulatory monitoring

## Sales Workflow Routing

Route through `using-sales` when the request could plausibly fit more than one of these:

- `using-sales/account-research` — gather company, contact, and qualification intelligence before sales action
- `using-sales/sales-call-prep` — build a prep brief for an upcoming sales conversation
- `using-sales/sales-draft-outreach` — draft personalized outbound email or LinkedIn outreach

## Marketing Workflow Routing

Route through `using-marketing` when the request could plausibly fit more than one of these:

- `using-marketing/marketing-performance-analytics` — measure performance, choose KPIs, and diagnose funnel or attribution issues
- `using-marketing/marketing-competitive-analysis` — compare competitors, messaging, positioning, and battlecards
- `using-marketing/content-creation` — draft or structure marketing content artifacts across channels

## Research Workflow Routing

Route through `using-research` when the request could plausibly fit more than one of these:

- `using-research/investment-research` — research stocks, theses, investor styles, and portfolios
- `using-research/market-research` — run framework-based market sizing, competitive, or strategic market research
- `using-research/research-assistant` — deliver broad deep-dive research and synthesis when no narrower child fits

## Finance Workflow Routing

Route through `using-finance` when the request could plausibly fit more than one of these:

- `using-finance/finance-audit-support` — support SOX, internal-control, workpaper, and deficiency-evaluation work
- `using-finance/finance-markets` — handle finance data tools, connector patterns, and structured market-data retrieval

## Reasoning and Strategy

Route through `using-reasoning` when the request could plausibly fit more than one of these:

- `using-reasoning/thinking-ground` — calibrate reasoning state before analysis
- `using-reasoning/problem-definition` — turn a messy situation into one clean problem statement
- `using-reasoning/strategic-foresight` — run scenarios around a concrete external signal or threshold
- `using-reasoning/reality-check` — surface hidden rules, survivability traps, resource mismatch, or platform ceilings
- `using-reasoning/domain-expert-consultation` — produce a structured advisory memo or expert recommendation
- `using-reasoning/dynamic-problem-solving` — analyze a clearly defined complicated problem through multiple lenses

## Routing Rule of Thumb

Ask first: what is the primary artifact or workflow needed?

- compacted state -> `context-compaction`
- audit or retro -> `self-cognitive`
- system prompt, prompt template, prompt architecture, rubric, or eval plan -> `meta-prompting`
- sparse prompt enrichment or prompt variants for text, image, or video generation -> `prompt-augmentation`
- feature spec, PRD, or requirements document -> `feature-spec`
- reusable leaf-skill creation or upgrade -> `create-skill`
- family router skill creation or upgrade with child metadata -> `create-router-skill`
- startup sanity check, business-model teardown, launch stress test, or startup simulation -> `startup-pressure-test`
- support-ticket categorization, priority assignment, dedupe, or routing -> `cx-ticket-triage`
- non-trivial software feature work that still needs discovery, delivery-control routing, plan review, strict frontend acceptance, or stage-by-stage routing -> `software-delivery`
- profile unfamiliar data, assess schema quality, or find anomalies before analysis -> `data-exploration`
- choose chart types, write plotting code, or apply chart-specific accessibility guidance -> `visualization`
- repo-backed coding, debugging, refactor, or other generic execution -> `coding-and-data`
- ambiguous design-family work across visual systems, design stacks, foundations, tokens, generative UI, or liquid-glass experimentation -> `using-design`
- `using-design/design-foundations` — design foundations for colors, typography, spacing, or chart styling
- `using-design/generating-design-tokens` — design token spec
- `using-design/generative-ui` — generative browser UI, schema-driven component rendering, or streamed agent surfaces
- `using-design/liquid-glass-design` — liquid-glass implementation note
- harness image/video generation, text-to-speech, or transcription CLI work -> `media`
- ambiguous website or browser-based build across site, app, or game -> `website-building`
- ambiguous document work across Word, PDF, PowerPoint, or Excel artifacts -> `using-documents`
- ambiguous legal help across contract redlines or privacy compliance -> `using-legal`
- ambiguous sales help across research, meeting prep, or outreach -> `using-sales`
- ambiguous marketing help across analytics, competitor analysis, or content creation -> `using-marketing`
- ambiguous research help across broad research, market frameworks, or investment analysis -> `using-research`
- ambiguous finance help across audit support or finance-data tooling -> `using-finance`
- analytical framing, calibration, advisory judgment, or scenario reasoning -> `using-reasoning`
