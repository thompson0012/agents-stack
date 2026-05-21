# Design Token Standards

Measurable validation criteria for brand design tokens.

## Typography

| Property | Minimum | Recommended | Notes |
|---|---|---|---|
| Body text size | 16px | 16-18px | Readability baseline |
| Line height | 1.5 | 1.5-1.6 | Optimal reading |
| Line length | — | 45-75 chars | Prevents eye fatigue |
| Heading size ratio | Clear step | 1.25x-1.5x per level | Visual hierarchy |
| Font families | — | 1-2 max | Consistency |
| Font weights | — | 2-3 max | Controlled hierarchy |

## Touch & Interaction

| Property | Minimum | Recommended | Notes |
|---|---|---|---|
| Button height | 44px | 48-56px | WCAG touch target |
| Input height | 44px | 44-48px | WCAG touch target |
| Tap target | 44x44px | 48x48px | Mobile minimum |
| Click area spacing | 8px | 8-12px | Prevents mis-clicks |

## Contrast & Accessibility

| Property | Minimum (AA) | Enhanced (AAA) | Notes |
|---|---|---|---|
| Normal text | 4.5:1 | 7:1 | Body, labels, inputs |
| Large text (18px+) | 3:1 | 4.5:1 | Headings |
| UI components | 3:1 | 4.5:1 | Buttons, icons, borders |
| Focus indicators | Visible | High contrast | Keyboard navigation |

## Spacing

| Property | Rule |
|---|---|
| Scale | Systematic (e.g., 4px, 8px, 12px, 16px...) |
| Base unit | Same unit throughout (px or rem) |
| Arbitrary values | NOT allowed — every value must be in the scale |

## Color

| Property | Rule |
|---|---|
| Brand color usage | ≤ 10% of total screen area (60-30-10 rule) |
| Neutrals | ≥ 50% of palette |
| Semantic colors | Distinct + icon backup for colorblind safety |
| Number of colors | 3-5 functional colors, not 20+ |

## Border Radius

| Property | Rule |
|---|---|
| Value count | 2-4 values (sm, md, lg, pill) |
| Consistency | Same radius used for same component type |
| Mixed radii | Allowed only when functionally distinct |

## Shadows

| Property | Rule |
|---|---|
| Count | 2-3 levels (sm, md, lg) |
| Style | Consistent direction, color, blur |
| Muddy shadows | NOT allowed (low opacity + large blur = dirty) |

## Brand Identity YAML Schema (v2.0)

The brand identity specification is stored as a YAML block under `## Visual System` in `.agents-stack/reference/design.md`. Validate extracted tokens against this schema:

### Required Top-Level Keys
| Key | Purpose |
|---|---|
| `color_policy` | Dominant/accent/text/glass colors with hex values, hard constraints, finish rules |
| `design_tokens` | spacing, radius, shadow, blur, motion, typography — all with px/ms values and `--kebab-case` tokens |
| `form_language` | Primary/secondary forms, geometry rules with severity |
| `material_language` | Approved materials, surface behavior rules |
| `scene_density_rules` | whitespace_ratio_min (≥0.55), max_primary_objects (≤3), max_secondary_objects (≤6) |
| `object_library` | Approved, conditional, forbidden items — each with severity |
| `ui_translation` | Interface principles mapped to tokens, preferred components with CSS var values |
| `negative_prompt_policy` | Hard negative terms list, inject_format per generation tool |
| `input_variables` | Required/optional params, value enums for scene_type, density, composition_mode, background_mode |
| `application_presets` | Per-use-case defaults (brand_kv, landing_page, product_ui, app_illustration, motion_scene, campaign_visual) |
| `prompt_seed` | Master prompt template with variable slots |
| `rule_severity` | hard/soft/directional tiers — which sections belong to which tier |

### Validation Rules
- All hex values must use `#RRGGBB` format (6 digits, uppercase)
- All token names must use `--kebab-case` CSS custom property format
- Every constraint must carry a `severity` field: `hard`, `soft`, or `directional`
- `hard` violations → generation MUST fail or reject
- `soft` violations → deviation requires explicit flagging
- `directional` → aspiration only, no enforcement
- Spacing scale must be systematic (multiples of base_unit)
- Glass colors must carry an `alpha` field (0–1) separate from hex
- Blur values must carry a `unit` field (px)
- Motion values must carry `duration` (number), `unit` (ms), and `easing` (CSS easing string)