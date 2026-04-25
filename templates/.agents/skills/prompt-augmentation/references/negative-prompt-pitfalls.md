# Negative Prompt Pitfalls

Per-domain failure modes and corresponding negative terms for prompt augmentation.

## Image Failure Modes

- **Anatomy errors** — `extra limbs, extra fingers, wrong proportions, distorted hands, backward hands`
- **Extra limbs** — `extra arms, extra legs, fused limbs, asymmetric limb count`
- **Fused fingers** — `fused fingers, missing fingers, extra fingers, deformed hands`
- **Deformed faces** — `asymmetric eyes, crooked mouth, crossed eyes, double chin, distorted jaw`
- **Cluttered background** — `busy background, messy scene, random objects, visual noise`
- **Watermark** — `watermark, logo overlay, brand stamp, copyright notice`
- **Signature** — `artist signature, signed, signature in corner`
- **Text overlay** — `unwanted text, captions, subtitles, floating words`
- **Blurry** — `blurry, out of focus, soft focus, motion blur, depth-of-field error`
- **Low quality** — `low resolution, pixelated, jpeg compression, upscaled artifacts`
- **JPEG artifacts** — `compression artifacts, banding, posterization, blocky edges`

## Video Failure Modes

- **Jitter** — `frame jitter, micro-stutter, position flicker, unstable camera`
- **Flicker** — `brightness flicker, color flicker, inconsistent exposure`
- **Inconsistent lighting** — `lighting shift, shadow jump, ambient change, flicker of light`
- **Morphing objects** — `object morphing, shape drift, identity shift, structure change`
- **Temporal incoherence** — `temporal inconsistency, scene jump, discontinuity, frame mismatch`
- **Frame duplication** — `looped frames, repeated frames, freeze frame, stutter loop`

## Design Failure Modes

- **Misaligned elements** — `misaligned, off-grid, uneven spacing, ragged edges`
- **Inconsistent spacing** — `inconsistent gap, uneven margin, random padding`
- **Broken grid** — `broken grid, column overflow, collapsed layout, overflowing content`
- **Unreadable text** — `illegible text, tiny font, poor contrast text, overlapping type`
- **Color clash** — `color clash, garish palette, oversaturated, competing hues`
- **Poor contrast** — `low contrast, faded text, invisible element, insufficient contrast`
- **Missing hover states** — `no hover state, static buttons, dead interactive, no cursor change`
- **Generic placeholder look** — `generic template, stock look, wireframe feel, Lorem ipsum design, placeholder aesthetic`