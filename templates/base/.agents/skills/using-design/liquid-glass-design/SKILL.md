---
name: liquid-glass-design
description: Use when implementing or evaluating experimental Apple-like liquid glass UI effects in the browser with CSS/SVG refraction, displacement maps, and backdrop filters. Best for Chromium or Electron prototypes; not for general visual design, cross-browser parity, or production-ready glass.
---


# Liquid Glass CSS/SVG

Source: <https://kube.io/blog/liquid-glass-css-svg/>

## What this gives you

A reusable implementation note for building an Apple-like liquid glass effect in the browser with:

- a physically motivated refraction field
- an SVG `<feDisplacementMap>`
- a specular rim highlight
- CSS `backdrop-filter` for live UI components

This is a proof-of-concept pattern, not production-ready glass.

## Use this when

Use this approach when you want:

- refractive glass, not just blur + transparency
- a controllable bezel/lens profile
- a Chromium or Electron-only experimental UI effect
- a workflow you can tune for capsules, search boxes, sliders, switches, or magnifiers

Do not use this as-is when you need:

- cross-browser parity
- cheap dynamic resizing
- true 3D optics
- multiple refraction events or perspective-correct ray tracing

## Hard constraints

The article deliberately narrows the problem. Keep these assumptions unless you are prepared to redo the math:

- Ambient medium has refractive index `n1 = 1`.
- Glass material has `n2 > 1`, typically `1.5`.
- Only one refraction event is modeled.
- Incoming rays are orthogonal to the background plane.
- The object is treated as a 2D shape parallel to the background.
- There is no gap between the glass and the sampled background plane.
- The article derives the field from circles, then stretches them into rounded rectangles.

## Browser reality

- The effect is fully useful only in Chrome/Chromium because the key trick is `backdrop-filter: url(#svgFilterId)`.
- Safari and Firefox can still render the underlying math if you apply the SVG as a regular `filter`, but not as a live backdrop refraction layer.
- Filter image dimensions must match the target element size; they do not auto-track the element.

## Core optics model

Refraction follows Snell's law:

`n1 * sin(theta1) = n2 * sin(theta2)`

The implementation strategy is:

1. describe the glass surface as a height function
2. derive the surface normal from that function
3. compute refraction displacement from the normal
4. precompute a symmetric radial displacement profile
5. rotate/project that profile into a 2D vector field
6. encode the field into an SVG displacement map
7. blend a specular highlight on top

## Surface profiles

These are the useful surface families from the article:

| Profile | Equation | Behavior | Notes |
| --- | --- | --- | --- |
| Convex circle | `y = sqrt(1 - (1 - x)^2)` | Dome-like lens | Simple, but sharper transition near the flat interior |
| Convex squircle | `y = (1 - (1 - x)^4)^(1/4)` | Softer dome | Best default for stretched rounded rectangles |
| Concave | `y = 1 - Convex(x)` | Bowl-like depression | Pushes rays outside the object bounds |
| Lip | `mix(Convex(x), Concave(x), Smootherstep(x))` | Raised rim, shallow center dip | Good for switch-like controls |

Practical takeaway:

- Prefer convex profiles when you want displacement to stay inside the object.
- Prefer the convex squircle when you need smooth refraction across stretched rounded rectangles.
- Use the lip profile when you want an inset center and stronger edge behavior.
- Avoid concave profiles unless you explicitly want displacement to escape the bounds.

## Implementation workflow

### 1. Define the glass surface

Model thickness from border to flat interior with a scalar function:

```ts
const height = f(distanceFromSide);
```

Where:

- `0` means the outer edge
- `1` means the end of the bezel / start of the flat interior

### 2. Compute the surface normal

Approximate the derivative numerically, then rotate it to get the normal:

```ts
const delta = 0.001;
const y1 = f(distanceFromSide - delta);
const y2 = f(distanceFromSide + delta);
const derivative = (y2 - y1) / (2 * delta);
const normal = { x: -derivative, y: 1 };
```

This normal is what drives the local incident angle and therefore the refraction amount.

### 3. Ray-trace one radius, not the whole object

Because the system is symmetric around the bezel:

- compute displacement magnitude on a single radius
- reuse it around the perimeter
- keep only about `127` useful samples to fit SVG displacement-map channel precision

That symmetry is the main computational shortcut.

### 4. Keep the displacement inside bounds when possible

The article's simulations show:

- convex surfaces keep rays inside the glass footprint
- concave surfaces can push rays beyond the object edge

If the displacement leaves the object, you now need valid background samples from outside the glass. That makes the UI effect much harder to use robustly.

### 5. Normalize the vector magnitudes

SVG displacement maps work best when you normalize vectors, store the max magnitude, and restore real scale through the filter:

```ts
const maximumDisplacement = Math.max(...displacementMagnitudes);

const normalized = {
  angle: normalAtBorder,
  magnitude: magnitude / maximumDisplacement,
};
```

Keep `maximumDisplacement`; it becomes the SVG filter's `scale`.

### 6. Convert polar vectors to SVG color channels

Convert angle + magnitude into Cartesian components:

```ts
const x = Math.cos(angle) * magnitude;
const y = Math.sin(angle) * magnitude;
```

Then map them to red/green channels:

```ts
const pixel = {
  r: 128 + x * 127,
  g: 128 + y * 127,
  b: 128,
  a: 255,
};
```

Meaning:

- red stores X displacement
- green stores Y displacement
- blue is ignored
- alpha stays opaque

### 7. Build the SVG displacement filter

```xml
<svg color-interpolation-filters="sRGB">
  <filter id="liquidGlass">
    <feImage
      href="data:image/png;base64,..."
      x="0"
      y="0"
      width="100%"
      height="100%"
      result="displacement_map"
    />
    <feDisplacementMap
      in="SourceGraphic"
      in2="displacement_map"
      scale="MAX_DISPLACEMENT"
      xChannelSelector="R"
      yChannelSelector="G"
    />
  </filter>
</svg>
```

Key limits:

- each channel is 8-bit
- neutral is `128`
- practical per-axis range is `[-128, 127]` pixels before scaling concerns become awkward

The important trick is that `scale` restores the real-world pixel displacement from the normalized map.

### 8. Add a specular rim highlight

The article models the highlight as a simple rim light, driven by the surface normal relative to a fixed light direction.

This is not the physically hard part. It is the artistic part.

Use a separate generated image for the highlight and combine it with the refracted result using SVG blending.

### 9. Blend refraction and highlight

Pipeline:

- `feImage` for displacement map
- `feDisplacementMap` for refraction
- another `feImage` for specular highlight
- `feBlend` to combine both

This is where most of the visual tuning happens.

### 10. Apply the filter as a live backdrop

```css
.glass-panel {
  backdrop-filter: url(#liquidGlass);
}
```

This is the crucial Chromium-only step for real UI glass.

## Recommended defaults

Start here:

- surface: convex squircle
- refractive index: `1.5`
- one refraction event only
- low to medium blur
- moderate specular opacity
- moderate saturation for the highlight

These choices stay closest to the article's practical sweet spot.

## Component patterns from the article

### Search box
- convex bezel
- lower refraction level
- light blur
- useful for subtle UI chrome

### Slider
- convex bezel
- minimal or zero blur
- lets the current value remain visible through the control

### Switch
- lip bezel
- convex outer edge + concave middle
- creates a zoomed-out center with active edge refraction

### Magnifying glass
- two displacement maps
- one for side refraction
- one stronger field for zooming
- combine with shadow and scale for a more lens-like interaction

### Music-player style panel
- convex bezel
- restrained highlight
- emphasizes the panel edges rather than aggressive distortion

## Failure modes and costs

### 1. Channel clipping
If your displacement exceeds the useful map range, your encoded field stops representing the physics cleanly.

### 2. Outside-of-bounds sampling
Concave profiles can displace pixels beyond the glass boundary and require background data you may not have.

### 3. Rebuild cost
Changing shape or size is expensive because it usually forces a complete displacement-map rebuild.

### 4. Browser lock-in
The live backdrop version is effectively Chromium-only today.

### 5. Geometry mismatch
If the filter image size does not match the element geometry, the effect distorts incorrectly.

## Minimal build recipe

If you want the shortest path to a working prototype:

1. use a convex squircle bezel
2. precompute radial displacement magnitudes
3. normalize them and store `maximumDisplacement`
4. rotate them into a full 2D field
5. encode X/Y into R/G channels
6. feed the map into `<feDisplacementMap>`
7. set `scale = maximumDisplacement`
8. add a soft specular rim layer
9. apply via `backdrop-filter: url(#filterId)` in Chromium

## What to preserve if you productionize it

If you take this further, keep these design truths intact:

- The displacement map is the core asset; everything else is support.
- Convex geometry is the safe default.
- Normalize once, then drive real intensity with filter scale.
- Separate physically motivated refraction from artistically tuned highlight.
- Treat resize and shape mutation as expensive operations unless you redesign the pipeline.

## Bottom line

The article's real contribution is not "glass with blur." It is a reusable browser pipeline:

- derive a lens profile
- convert optics into a displacement field
- encode that field into SVG
- apply it as a live backdrop filter
- layer a specular highlight for readability and polish

That is the skill worth carrying forward.