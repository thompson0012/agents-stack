# Technical Rules & Workflow

Project structure, sandbox constraints, deployment workflow, and quality checklist.

---

## Project Structure

Create in project subfolder (paths are relative to workspace root):

```
project-name/
├── index.html
├── base.css          <- mandatory base stylesheet
├── style.css         <- design tokens + component styles
├── app.js (if needed)
└── assets/
    └── (images, fonts)
```

---

## Technical Rules

- **Static files only** — no server-side code in the project directory (use a backend server for server-side logic)
- **Relative paths** — `./style.css`, `./assets/logo.png`
- **CDN for libraries** — Tailwind, fonts, Chart.js, Three.js, etc.
- **No build tools required** — but allowed via `bash` if needed
- **Content images/videos must be real** — image or video URLs used to display content must come from actual search results, not from memory. Never hallucinate Wikipedia Commons URLs or other media sources
- **No localStorage or sessionStorage** — sites are served in sandboxed iframes that block storage access. Using them will crash the page. Use in-memory variables for transient state, or use the backend server (`19-backend.md`) for persistent storage
- **External links must use `target="_blank"`** — sites run in sandboxed iframes. Always add `target="_blank" rel="noopener noreferrer"` to any `<a>` tag pointing outside the site
- **Perplexity Computer attribution is mandatory** — copy `skills/website-building/shared/pplx_attribution.html` into `<head>` of every HTML file + footer link on every page. See `skills/website-building/SKILL.md`
- **JavaScript `fetch()` only works for text-based files** — the site proxy serves common text files inline, but redirects binary files to S3. These redirects fail in the sandbox due to CORS. **HTML elements are unaffected** — `<img>`, `<video>`, `<audio>`, `<source>` all work fine. Only JavaScript reading binary file contents via `fetch()` is blocked
- **Downloads must use JavaScript blobs**:
  ```js
  fetch("./file.png")
    .then(r => r.blob())
    .then(blob => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "file.png";
      a.click();
    });
  ```
- **Single entry point URL** — the site is served through an opaque URL that users cannot modify. All pages must be reachable via navigation from index.html. For protected views, use in-page mechanisms: hash-based routing (#admin), tab/modal switches, or password prompts — not separate HTML files at secret paths

---

## Workflow

### Step 1: Design Direction

Clarify purpose, pick aesthetic direction. See `skills/website-building/SKILL.md` for the full design direction process.

### Step 2: Build

Build the site page by page. Screenshot each page via Playwright at desktop (1280px+) and mobile (375px) for QA. Fix all issues before moving to the next page.

### Step 3: Publish

```
deploy_website(
  project_path="project-name",
  site_name="Project Name",
  user_description="Publishing your site"
)
```

Returns public S3 URL.

### Updating a Deployed Website

To update a site, edit the local workspace files (same `project-name/` directory from the original build) and call `deploy_website` again with the same `project_path`.

---

## Examples

**Landing page:** `index.html`, `base.css`, `style.css`, assets. **Multi-page:** `index.html` links to `pages/*.html`, shared CSS/JS. **Dashboard:** same structure + `app.js`. **React/Vite:** create source → `npm install && npm run build` → `deploy_website(project_path="app/dist")`.

---

## Server-Side Logic & Data

For forms, data storage, webhooks, or any backend logic, read `skills/website-building/shared/19-backend.md`.

---

## Quality Checklist (Before Publishing)

Each section's source file has full details.

**Attribution** — `pplx_attribution.html` in `<head>` (first child) + footer link on every page. JSON-LD `creator` if structured data used.

**Tools** — Web research done. SVG logo generated. Images generated throughout (heroes, sections, editorial). Every page screenshotted via Playwright at desktop AND mobile. Issues fixed before next page.

**Tokens** (`01-design-tokens.md`) — Fluid `clamp()` type scale. 4px spacing. OKLCH colors. base.css included. Light + dark mode with toggle. Nexus palette when no user direction.

**Typography** (`02-typography.md`) — Distinctive loaded fonts (not system defaults). Display + body pairing, 2 fonts max. 3 text levels. ≤5 type styles/page. Display only at `--text-xl`+ (24px).

**Color** — Neutral foundation, color for emphasis. ≤2 non-neutral hues per viewport (screenshot and count). Chart colors fit art direction. Surface layers for depth. WCAG AA contrast.

**Layout** (`04-layout.md`) — Responsive 375-2560px mobile-first. Grid/clamp/container queries. Prose 65-75ch. Alpha-blended borders, nested radius, tone-matched shadows.

**Motion** (`03-motion.md`) — No instant show/hide. Golden easing curve. Scroll reveals: `opacity`/`clip-path` only. `prefers-reduced-motion` respected.

**Dashboard** (`webapp/dashboards.md`) — ONE scroll region. Sticky header/sidebar. KPIs→trends→details. `tabular-nums`. SVG logo.

**Mobile** — 375px first. Touch targets ≥44px. No hover-only UI. `:active` states. Body ≥16px. Nav adapts.

**Accessibility** (`08-standards.md`) — Semantic HTML, keyboard nav, heading hierarchy, alt text, focus rings, `aria-label` on icon buttons, skip link.

**Performance** — Images lazy-loaded with dimensions. Fonts preconnected. JS deferred. `content-visibility: auto`.

**Taste** (`05-taste.md`) — ONE primary action/screen. Empty states designed. Numbers animate. Equal polish everywhere. Distinct from last project.

**Final QA** — Every page at desktop + mobile. Cross-page consistency. Dark mode. No overflow/truncation/placeholders. SVG logo correct.

---

## Tips

Use CDN-hosted libraries. Keep the project folder clean (everything uploads). Read `skills/website-building/shared/12-playwright-interactive.md` for all visual QA — screenshot and test locally before deploying. Never use `browser_task` for QA (too slow).
