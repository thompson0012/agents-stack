# Design System Tokens

Quick-reference for token categories and conventions useful in text-to-design prompt augmentation.

## Token Categories

- **Color** — Semantic palette tokens: primary, secondary, neutral, success, warning, error, surface, background, on-surface
- **Spacing** — Scale-based gaps: 4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px
- **Sizing** — Component dimensions: icon-size, avatar-size, button-height, input-height, max-width
- **Typography** — Font family, weight, size, line-height, letter-spacing tokens
- **Border-radius** — Corner rounding: none / sm / md / lg / xl / full
- **Border-width** — Stroke weight: hairline / thin / medium / thick
- **Shadow** — Layered box-shadow tokens: sm / md / lg / xl
- **Elevation** — Z-depth levels (0–5) mapping to shadow + overlay opacity
- **Opacity** — Transparency scale: disabled / hover / pressed / drag / focus
- **Motion duration** — Transition lengths: micro (100ms) / short (200ms) / medium (300ms) / long (500ms)
- **Motion easing** — Timing functions (see Motion Tokens below)

## Density

- **Dense** — Minimal padding, tight spacing, small touch targets, info-heavy layouts
- **Comfortable** — Balanced whitespace, default touch targets, readable density
- **Spacious** — Generous padding, breathing room, editorial/hero layouts
- **Compact** — Slightly tighter than comfortable, sidebar/dashboards, reduced line-height

## Platform Conventions

- **Web** — Responsive, CSS flex/grid, 8px base grid, hover/focus states
- **iOS HIG** — San Francisco font, safe areas, large hit targets (44pt), blur/vibrancy
- **Material Design** — Elevation system, density scale, dynamic color, motion principles
- **Android** — Material You, edge-to-edge, gesture nav, window insets
- **Windows Fluent** — Acrylic material, reveal hover, connected animations, 4px grid
- **macOS** — Vibrancy, sidebar patterns, toolbars, native spacing, system font (SF)

## Motion Tokens

- **ease-in** — Accelerates from rest; use for exiting elements
- **ease-out** — Decelerates to rest; use for entering elements
- **ease-in-out** — Symmetrical; use for position/size changes within view
- **spring** — Physics-based overshoot; natural-feeling micro-interactions
- **bounce** — Overshoot + settle; playful feedback, attention-grabbing
- **snap** — Immediate with slight settle; near-instant state changes

## Border / Shape Tokens

- **Sharp** — 0 radius; data tables, code blocks, structured content
- **Rounded** — 4–8px radius; buttons, cards, inputs, most UI elements
- **Pill (full)** — 9999px radius; chips, badges, toggle buttons
- **Circular** — 50% radius; avatars, icons, FABs, status dots
- **Squircle** — Superellipse continuous curvature; iOS icons, premium feel