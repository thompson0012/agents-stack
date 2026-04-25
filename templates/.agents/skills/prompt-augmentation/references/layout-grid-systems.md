# Layout & Grid Systems Reference

Domain-specific terms for text-to-design prompt augmentation.

## Grid Types

- **Columnar** — Vertical columns with gutters; flexible content flow (12-col, 8-col)
- **Modular** — Rows + columns forming cells; structured, grid-of-cards layouts
- **Baseline** — Horizontal lines aligned to text baseline; vertical rhythm consistency
- **Manuscript** — Single centered column with margins; editorial, long-form reading
- **Hierarchical** — Nested grids per content zone; complex, content-driven layouts
- **Asymmetric** — Unequal columns or offset positions; dynamic, editorial tension

## Spacing Scales

- **4pt grid** — Fine-grained increments of 4px; tight, pixel-precise spacing
- **8pt grid** — Most common base unit; balances flexibility and consistency
- **16pt grid** — Coarser scale for large-scale layouts; generous spacing rhythm

## Composition Patterns

- **Z-pattern** — Eye follows Z path; works for sparse, scannable landing pages
- **F-pattern** — Eye follows F path; ideal for text-heavy, content-driven pages
- **Gutenberg diagram** — Primary/optimal zone top-left, terminal zone bottom-right

## Safe Zones

- **Gesture safe area** — Region clear of edge-swipe conflicts on touch devices
- **Thumb zone** — Center-lower screen area reachable by thumb one-handed
- **Safe area insets** — Padding to avoid notches, rounded corners, home indicators

## Whitespace Strategies

- **Generous whitespace** — Large margins and gutters; premium, luxurious feel
- **Dense** — Minimal spacing; information-rich, data-heavy dashboards
- **Airy** — Open breathing room between sections; relaxed, modern aesthetic
- **Breathable** — Balanced whitespace; readable, uncluttered, approachable

## Responsive Breakpoints

| Token         | Range           | Common Use              |
|---------------|-----------------|-------------------------|
| `mobile`      | 0–639px         | Phone portrait          |
| `tablet`      | 640–1023px      | Tablet / small laptop   |
| `desktop`     | 1024–1439px     | Standard laptop/desktop |
| `widescreen`  | 1440px+         | Large monitor / TV      |