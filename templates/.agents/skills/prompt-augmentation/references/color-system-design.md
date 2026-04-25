# Color System & Design Reference

Domain-specific terms for text-to-design prompt augmentation.

## Semantic Color

- **Primary** — Brand anchor color; CTAs, key actions, focal elements
- **Secondary** — Supporting accent; secondary buttons, less prominent actions
- **Tertiary** — Third-level accent; subtle highlights, decorative elements
- **Success** — Confirms positive outcome; green-family, check icon pairing
- **Warning** — Cautions without blocking; amber/yellow, caution icon pairing
- **Error** — Indicates failure or invalid state; red-family, alert icon pairing
- **Danger** — Destructive action emphasis; deeper red, confirmation required
- **Info** — Neutral informational accent; blue-family, info icon pairing
- **Neutral** — Non-emphasized UI elements; gray scale for text, borders, dividers
- **Surface** — Container background for cards, sheets; distinct from page background
- **Background** — Page-level base color; light or dark depending on mode
- **On-primary** — Text/icon color placed on primary; guarantees contrast on primary

## Accessibility Ratios

- **WCAG AA 4.5:1** — Minimum contrast for normal text; standard compliance level
- **WCAG AAA 7:1** — Enhanced contrast for normal text; highest accessibility tier
- **Large text 3:1** — Reduced ratio for 18px+ bold or 24px+ regular; larger is easier

## Mode Adaptation

- **Light mode** — Light background, dark text; default for most designs
- **Dark mode** — Dark background, light text; reduces eye strain in low light
- **High contrast** — Maximized foreground/background separation; vision accessibility
- **Color blind safe** — Palette distinguishable without hue; avoids red-green only cues

## Overlay & Elevation

- **Scrim** — Semi-transparent overlay dimming background; focuses modal content
- **Shadow depth 1** — Subtle lift; cards, small containers, resting elevation
- **Shadow depth 2** — Medium lift; raised cards, dropdowns, hover state
- **Shadow depth 3** — Prominent lift; floating action buttons, popovers
- **Shadow depth 4** — Strong lift; modals, dialogs, prominent floating elements
- **Shadow depth 5** — Maximum lift; critical overlays, drag-and-drop previews
- **Glassmorphism** — Frosted translucent layers with blur; depth without opacity
- **Neumorphism** — Soft extruded/inset shapes; light-source shadow UI aesthetic
- **Frosted glass** — Background blur with translucent fill; modern iOS-style layering