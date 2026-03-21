# Technical Rules & Workflow

Project structure, runtime constraints, local workflows, and the quality checklist.

---

## Project Structure

Create in a project subfolder. Paths below are relative to that project root:

```
project-name/
├── index.html
├── base.css          <- mandatory base stylesheet
├── style.css         <- design tokens + component styles
├── app.js            <- optional interaction logic
└── assets/
    └── (images, fonts)
```

If the task needs a React or fullstack application rather than a static site, route to the appropriate child and follow that child's template workflow instead of forcing everything into a flat HTML folder.

---

## Technical Rules

- **Match the stack to the request.** Plain HTML/CSS/JS is fine for content-first sites. Use a build tool only when the interaction model earns it.
- **Relative asset paths.** Use `./style.css`, `./assets/logo.png`, and similar project-relative imports.
- **CDN libraries are acceptable for simple static sites.** For template-based apps, install packages with the project's package manager instead.
- **Content images and video must be real.** Do not hallucinate media URLs. If the page references a real external asset, verify that the URL actually resolves.
- **External links should open safely.** Add `target="_blank" rel="noopener noreferrer"` for links that should leave the site.
- **Keep navigation honest.** Every meaningful page or state should be reachable from the main UI. Do not hide required views behind magic URLs.
- **Prefer browser-native delivery for media.** If you need to display an image, audio, or video, use the appropriate HTML element rather than trying to reimplement the browser's asset handling.
- **Use a backend only when the product needs one.** Forms, persistence, webhooks, auth, or server-side integrations should route through the backend guidance in `19-backend.md` or the `webapp` child.

---

## Workflow

### Step 1: Design Direction

Clarify purpose and pick an art direction. See `../SKILL.md` for the router-level decision model and the shared design references it points to.

### Step 2: Optional Flow Sketch

For non-trivial web work, sketch the main screens and states before building. Keep it low fidelity: bullets, boxes, wireframes, or a state map are all fine. The point is to expose missing states, navigation gaps, and backend dependencies early, not to produce polished mockups.

### Step 3: Build

Build the site page by page or state by state.

### Step 4: Verify Locally

Run the stack's normal local workflow from the shell:

- Static site: start a simple local server or use the project's existing preview command.
- Vite or React app: `npm install`, then `npm run dev`.
- Production sanity check when relevant: `npm run build`.

Use the browser automation workflow in `12-playwright-interactive.md` to inspect desktop and mobile states, exercise the main interactions, and capture screenshots only when they add evidence.

---

## Examples

- **Landing page:** `index.html`, `base.css`, `style.css`, `assets/`
- **Multi-page site:** `index.html` plus `pages/*.html`, shared CSS and JS
- **Dashboard or app shell:** route to `../webapp/SKILL.md`
- **React/Vite site:** create sources, run `npm install`, `npm run dev`, and `npm run build` for final local verification

---

## Server-Side Logic & Data

For forms, data storage, webhooks, or other backend behavior, read `19-backend.md`.

---

## Quality Checklist

Each detailed design file has deeper guidance. Use this as the practical signoff list.

**Tools** — Research references first. Generate or source real imagery. Create a custom SVG logo when the project needs a mark. Run browser QA at desktop and mobile sizes. Fix issues before signoff.

**Tokens** (`01-design-tokens.md`) — Fluid type scale, 4px spacing rhythm, coherent light and dark tokens when the product supports themes, `base.css` included.

**Typography** (`02-typography.md`) — Distinctive loaded fonts, clear display/body pairing, limited number of text styles, consistent hierarchy.

**Color** — Neutral foundation with controlled accent use, chart colors that fit the art direction, WCAG AA contrast.

**Layout** (`04-layout.md`) — Responsive from mobile upward, strong grid logic, readable measure, consistent radius and border treatment.

**Motion** (`03-motion.md`) — No abrupt show/hide unless the interaction truly calls for it, tasteful easing, reduced-motion support.

**Dashboard** (`../webapp/dashboards.md`) — One clear primary scroll region, stable chrome, KPIs before detail, numeric alignment.

**Mobile** — 375px-first pass, touch targets at least 44px, no hover-only critical UI, readable body text, navigation that still works without precision pointing.

**Accessibility** (`08-standards.md`) — Semantic HTML, keyboard navigation, heading hierarchy, alt text, visible focus states, labels for icon-only controls.

**Performance** — Lazy-load large media, set intrinsic dimensions, preconnect fonts when appropriate, avoid unnecessary JS.

**Taste** (`05-taste.md`) — One primary action per screen, designed empty/loading/error states, even polish across the experience.

**Final QA** — Re-check every important page or state at desktop and mobile sizes. Confirm consistency, no overflow, no placeholder copy, and no broken interactions.

---

## Tips

Use CDN-hosted libraries for small static projects and package-managed dependencies for larger apps. Keep the project folder clean. Read `12-playwright-interactive.md` before browser QA and use the current browser tool workflow for interaction testing and screenshots.
