---
name: website-building
description: Use when a request could plausibly be an informational site, a web application, or a browser game and the agent must choose the narrowest website-building child.
---

# Website Building

Use this router when the request is about building a website or browser-based experience and more than one web child could fit.

Do not perform the full child workflow here. Choose the narrowest correct child, then hand off.

**Universal design principles** are shared with `using-design/design-foundations`. This family's `shared/` files extend those foundations with web-specific implementation guidance, so children should load the web references they need directly.

## Core Contract

- Choose exactly one primary child skill or decide that no website-building child fits.
- Prefer gameplay first, then app workflows, then informational sites.
- Use `references/children.json` as the source of truth for child boundaries, install hints, and selection order.
- If the best child is missing, say to install it rather than doing weaker work under the wrong child.
- Do not route to multiple sibling web children in parallel for one request.

## Decision Order

| Project Type | Route | Examples |
|---|---|---|
| Browser games | `website-building/game` | 2D Canvas games, Three.js or WebGL games, real-time playable experiences |
| Web applications | `website-building/webapp` | SaaS products, dashboards, admin panels, e-commerce flows, brand experiences with app logic |
| Informational sites | `website-building/informational` | Personal sites, portfolios, editorial sites, blogs, landing pages, small-business sites |

When you need a specific family reference, read it using a path relative to this directory, for example `shared/01-design-tokens.md`.

## Router Output

Return one of these forms, then invoke the selected child if needed:

- `Route to website-building/game.`
- `Route to website-building/webapp.`
- `Route to website-building/informational.`
- `Install <child-path>, then route to <child-path>.`
- `No website-building child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit.

## References

- `references/children.json`

## Sub-File Reference

### Shared (`shared/`) — Available across website projects

| File | Covers | Load |
|---|---|---|
| `shared/01-design-tokens.md` | Type scale, spacing, default palette, base stylesheet guidance | **Always** |
| `shared/02-typography.md` | Font selection, pairing, loading, blacklist | **Always** |
| `shared/04-layout.md` | Spatial composition, responsive behavior, mobile-first layout | **Always** † |
| `shared/05-taste.md` | Empty, loading, and error states; interaction polish | **Always** |
| `shared/08-standards.md` | Accessibility, performance, anti-patterns | **Always** |
| `shared/09-technical.md` | Project structure, runtime constraints, local build and QA workflow | **Always** † |
| `shared/03-motion.md` | Motion systems, transitions, scroll behavior, hover/cursor work | When animated |
| `shared/06-css-and-tailwind.md` | Tailwind, modern CSS, shadcn-compatible patterns | When using Tailwind |
| `shared/07-toolkit.md` | Libraries, React, Three.js, maps, icons, SVG patterns/filters | When choosing libraries |
| `shared/10-charts-and-dataviz.md` | Chart.js, Recharts, D3, KPIs, sparklines | When data visualization matters |
| `shared/11-web-technologies.md` | Framework versions and browser compatibility checks | When checking compatibility |
| `shared/12-playwright-interactive.md` | Browser-tool QA workflow for interaction testing, observation, and screenshots | When testing |
| `shared/19-backend.md` | Backend patterns, WebSocket/SSE guidance, API/server choices | When backend logic is needed |
| `shared/20-llm-api.md` | LLM chat plus image, video, and audio API guidance | When the site uses AI features |

† Skip these for the pre-wired webapp template when the child already provides the equivalent setup. Design tokens and typography are still authoritative defaults for all project types.

### Domain-Specific — Load one primary child

| File | When to load |
|---|---|
| `informational/SKILL.md` | Personal site, portfolio, editorial, small-business site, landing page |
| `webapp/SKILL.md` | SaaS, dashboard, admin, e-commerce, brand experience with app logic |
| `webapp/dashboards.md` | Dashboard or other data-dense interface after loading `website-building/webapp` |
| `game/SKILL.md` | Browser game, real-time playable experience, Three.js or WebGL project |
| `game/2d-canvas.md` | 2D Canvas companion after loading `website-building/game` |
| `game/game-testing.md` | Game-specific QA companion after loading `website-building/game` |

## Family Workflow Boundary

1. The router chooses the narrowest child.
2. The selected child owns the implementation workflow and builder-side browser QA.
3. The shared web references apply after the child is selected.
4. For non-trivial or signoff-sensitive browser-facing work, recommend `software-delivery/frontend-evaluator` after builder QA for an independent acceptance pass. Do not treat that evaluator lane as mandatory for every small web edit.

## Use Every Tool Honestly

- **Research first.** Search the web for reference sites, trends, and competitor examples before designing. Fetch any URLs the user provides.
- **Generate real assets when the work calls for them.** Produce logos, illustrations, and imagery that match the chosen art direction. Do not ship placeholders.
- **Verify in the browser as the builder.** Use the browser automation tool to inspect, interact with, and, when needed, capture screenshots at desktop and mobile sizes while implementing. Read `shared/12-playwright-interactive.md` before complex QA.
- **Recommend independent evaluator signoff when warranted.** For non-trivial or signoff-sensitive browser-facing work, hand off to `software-delivery/frontend-evaluator` after builder QA has stabilized the experience and evidence. Do not treat that evaluator lane as mandatory for every small web edit.
- **Use normal shell workflows for local work.** Install, run, and build projects with the stack's own commands such as `npm install`, `npm run dev`, and `npm run build`.

## SVG Logo Generation

Every project should get a custom inline SVG logo unless the user explicitly wants a text-only mark.

1. **Understand the brand** — purpose, tone, and one defining word.
2. **Write SVG directly** — geometric shapes, letterforms, or abstract marks. Aim for one memorable shape.
3. **Principles:** geometric and minimal, readable at 24px and 200px, monochrome first, `currentColor` for theme compatibility.
4. **Implement inline** with `aria-label`, `viewBox`, `fill="none"`, and `currentColor` strokes or fills.
5. **Generate a favicon** when the project needs one.

For SVG animation, see `shared/03-motion.md`. For SVG patterns and filters, see `shared/07-toolkit.md`.

## Visual QA Testing Process

Every website project should pass builder-side visual QA before signoff.

Read `shared/12-playwright-interactive.md` for the full browser QA workflow.

**Builder cycle:** `Build → Builder Browser QA → Fix → Repeat`

For non-trivial or signoff-sensitive browser-facing work, finish the builder cycle first, then recommend `software-delivery/frontend-evaluator` for an independent final pass. Do not present that evaluator step as mandatory for every trivial edit.

### Stage 1: Page-by-Page QA

After building each meaningful page or state:
1. Inspect desktop and mobile viewports.
2. Evaluate whether the result looks intentional and professionally designed.
3. Fix every issue before moving on.

### Stage 2: Final Builder QA

1. Re-check every page or critical application state at desktop and mobile sizes.
2. Check cross-page consistency in spacing, color, and typography.
3. Verify dark mode when the product supports it.
4. Check hover, focus, active, loading, empty, and error states as applicable.
5. Do a cold-open first-impression check.

Common QA failures: overflow, inconsistent spacing, weak contrast, broken mobile layout, placeholder content, missing states, or generic-looking art direction.

## Step 1: Art Direction — Infer Before You Ask, Ask Before You Default

Every site should have a visual identity derived from its subject matter.

1. **Infer from the subject.** The product domain should drive palette, typography, spacing, motion, and imagery.
2. **Check the child guidance.** `informational/SKILL.md`, `webapp/SKILL.md`, and `game/SKILL.md` each provide concept-driven starting points.
3. **Derive the five pillars:** color, typography, spacing, motion, and imagery.
4. **If the subject is genuinely ambiguous, ask** for mood or reference sites.
5. **Use the default palette only as a fallback.** Reach for the shared defaults after inference and a brief question fail to produce direction.

### Fallback: Clean and Swiss

When inference and a brief question still yield no style guidance, fall back to `shared/01-design-tokens.md` with:

- **Typography:** Satoshi or General Sans body when available, otherwise Inter or DM Sans. Keep the type system compact.
- **Color:** neutral surfaces with one controlled accent.
- **Layout:** grid-aligned with generous margins.
- **Motion:** minimal and functional.
- **Imagery:** generated or sourced visuals that fit the subject. No stock-photo filler.

See `shared/08-standards.md` for anti-patterns to avoid.
