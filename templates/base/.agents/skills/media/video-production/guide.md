# Video Production Guide

You have a full production toolkit: `asi-generate-video` (4 models, native audio, image-to-video), `asi-generate-image` (img2img, multiple aspect ratios), `asi-text-to-speech` (29+ voices, multi-speaker dialogue, emotion tags), `asi-transcribe-audio` (timestamps, diarization), and ffmpeg in the sandbox.

These tools compose freely. A single-clip social post and a multi-scene short film use the same building blocks — the difference is how many you chain together. Individual clips are 4-12 seconds, but frame chaining extends any scene to arbitrary length — don't let per-clip limits constrain your creative planning. Be ambitious.

## Choosing a Video Model

Load the `model-catalog` skill for full specs (resolution, duration, cost). The key distinction for video production:

All four models generate native synchronized audio (dialogue, sound effects, ambient). Sora models produce longer clips (up to 12s); Veo models offer stronger creative control and prompt adherence. But the most important difference is image-to-video behavior:

- **Veo** uses the input image as the **literal first frame** — it faithfully preserves composition, textures, and style. This makes Veo ideal for frame chaining and any workflow where visual continuity from a starting image matters.
- **Sora** treats the input image as a **style/composition reference** — it guides the look but the output may drift from the exact image. Sora also rejects input images containing human faces.

## Audio Design

Two approaches that combine well.

**Native video audio** — All models generate synchronized dialogue, sound effects, and ambient audio with lip-sync. Prompt techniques differ by model family:
- *Veo*: Use colons for dialogue (not quotation marks, which trigger unwanted subtitles): `The detective says: Where were you last night.` Add `(no subtitles)` to the prompt. Use [brackets] for effects ([thunder]), inline ambient descriptions. Keep dialogue under ~8 seconds to avoid unnaturally fast speech.
- *Sora*: Separate dialogue into a labeled block after the visual description. Use character labels and an audio priority hierarchy ("Audio priority: 1st dialogue, 2nd rain, 3rd traffic").

**TTS voiceover** — Use `asi-text-to-speech` when you need specific voice character, precise emotional delivery, or complex multi-speaker dialogue with 29+ voices and emotion/flow tags. Max 5000 chars per call.

**Combining both** — Generate video with native ambient audio, then layer TTS on top via ffmpeg for environmental realism plus precise voice control:
```
ffmpeg -i video.mp4 -i voiceover.mp3 -filter_complex "[0:a]volume=0.3[bg];[1:a]volume=1.0[vo];[bg][vo]amix=inputs=2:duration=longest" -c:v copy output.mp4
```

**Matching durations** — TTS and video are generated independently, so their durations won't match exactly. Never stretch, speed up, slow down, or trim either track to compensate. Instead, generate one first and calibrate the other:
- *Narration-first*: generate the voiceover, measure its duration with `ffprobe -show_entries format=duration`, then generate video clips that add up to that duration (choose clip count and duration_seconds to match)
- *Video-first*: generate the video, then adjust the voiceover script length to fit — fewer words = shorter audio, more words = longer
- *Video too short?* Use frame chaining to extend it — extract the last frame and generate another clip to cover the remaining duration
- *Audio too long?* Shorten the voiceover script and regenerate — fewer words = shorter audio
- Aim for the video to be slightly longer than the voiceover so the tail has ambient audio rather than silence. Use `duration=longest` in the amix filter so nothing gets cut off.

## Prompting for Quality

### Image prompts

Generated images are the starting frames for your videos — their quality determines the entire production's visual standard. The image model defaults to soft illustration styles when prompts are vague. Structure image prompts as: **[subject with specific details] + [action/pose] + [environment/setting] + [lighting] + [camera/composition] + [style]**.

**Describe scenes in natural language, not keyword lists.** "A towering brachiosaurus stands in a dense prehistoric jungle, golden sunlight streaming through the canopy, pterodactyls soaring between ancient trees, photorealistic 3D render with volumetric god rays" — not "dinosaur, jungle, sunset, pretty." Don't use quality keyword spam like "masterpiece, 8K, trending on artstation" — modern models don't need it and it can cause artifacts.

**Always specify a visual style.** Without one, the model defaults to children's book illustration. Anchor every prompt with style direction:
- Photorealistic: "photorealistic, cinematic lighting, shot on Arri Alexa"
- 3D render: "Pixar-quality 3D render, subsurface scattering, global illumination"
- Stylized: "cel-shaded anime, bold outlines, Studio Ghibli"

**Use specific materials and textures.** "Brushed aluminum" not "metal," "crushed velvet" not "fabric," "wet cobblestone" not "wet ground." Concrete material names produce dramatically sharper, more realistic results.

**Include camera and lighting.** The model understands technical photography language: lens type ("85mm f/1.4 portrait lens"), shot type ("extreme close-up," "wide establishing shot"), angle ("low-angle," "bird's eye view"), and lighting ("golden hour rim light," "three-point softbox setup," "volumetric god rays through fog"). Name 3-5 palette colors for visual stability ("deep teal, warm amber, charcoal").

**Match the video aspect ratio.** Set `aspect_ratio` on `asi-generate-image` to match your target video (e.g., "16:9" for landscape, "9:16" for vertical). This avoids cropping or letterboxing when the image becomes a video starting frame.

### Visual consistency

For any production with recurring subjects (characters, locations, products), establish visual identity before generating scenes:

**Define a style string.** Write one style/aesthetic description for the whole production (e.g., "Pixar-quality 3D animation, vibrant saturated colors, soft global illumination, expressive cartoon characters") and include it verbatim in every image and video prompt. This prevents style drift between scenes.

**Generate character/subject references first.** Before any scene work, generate reference images of each recurring subject — characters, key locations, signature props. Use these as reference inputs to `asi-generate-image` when generating storyboard keyframes so subjects look consistent across scenes. The image model supports multiple reference images per call.

### Video prompts

Video prompts control the motion, action, and energy of each clip. A strong starting keyframe with a weak video prompt produces static, lifeless output.

**One action + one camera move per clip.** This is the most reliable pattern. Each clip should have a single clear subject action and a single clear camera movement. Break complex sequences into multiple clips rather than cramming everything into one.

**Describe motion in sequential beats.** "She takes three steps to the window, pauses, and pulls the curtain aside" — not "she goes to the window." Beats and counts give the model timing structure.

**Specify camera movement.** Dolly in, tracking shot, crane up, slow orbit, handheld shake, static locked-off, whip pan, parallax dolly — the model responds to professional cinematography terms. No camera direction defaults to subtle or random movement.

**Match energy to the moment.** Slow, gentle prompts for quiet scenes ("camera drifts slowly across a still lake at dawn"); fast, dynamic prompts for action ("rapid zoom out as the asteroid tears through the atmosphere, fire and shockwaves rippling across the sky").

**For image-to-video: describe only motion and changes.** The model can already see the starting image — don't redescribe its contents. Focus on what happens next: camera movement, subject action, lighting shifts, temporal changes. Redescribing the image in detail can actually reduce motion or produce unexpected results.

**Specify ambient sound explicitly.** Veo models can hallucinate unwanted audio (e.g., audience laughter) when ambient sound isn't defined. Include brief sound direction: "sounds of distant traffic and wind through trees" or "quiet room tone with a ticking clock."

## Composable Techniques

These are building blocks — mix and match them freely. Not every video needs all of them. A single text-to-video clip with a good prompt is a perfectly valid production for quick requests. Scale up the workflow to match the ambition of the project.

### Storyboarding

For multi-scene productions, plan before generating. For narrated content (explainers, stories, documentaries), generate narration first so you know the exact duration and can plan visuals to match:

1. Write the full script — narration text plus visual direction for each segment.
2. Work scene by scene. For each segment:
   a. Generate the voiceover for this segment with `asi-text-to-speech`. Measure its duration with `ffprobe`.
   b. Plan video clips to cover that duration (e.g., 18s of narration → 3 × 8s clips). Each clip should depict a distinct moment — don't reuse starting images.
   c. Generate a unique storyboard keyframe for each clip using `asi-generate-image` or `run_subagent` with type "asset_designer". Match the video aspect ratio. **Review each keyframe** — verify it matches the intended style, subject consistency, and composition before proceeding. Regenerate any that miss the mark.
   d. Generate video clips from each keyframe. **Review each clip** — check that motion, style, and subject look correct. Measure actual durations — if total video falls short, frame-chain one more clip to cover the gap.
   e. Segment is done and locked. Move to the next.
3. Stitch all segments together and concatenate the per-segment voiceovers into the final audio track.

For short narrations where seamless vocal delivery matters more, a single TTS call works — use `asi-transcribe-audio` with `timestamps="word"` to find segment boundaries.

For non-narrated content (music videos, montages, product demos), plan the visual sequence upfront with enough unique keyframes to avoid repetition, but you can also discover the direction as you go — generate a few clips, see what works, and adapt.

**Longer productions** — For videos over ~5 minutes, break the script into independent chapters (e.g., a 30-minute documentary → 6 chapters of ~5 minutes each). Produce each chapter as its own complete unit. Stitch chapters together at the end. Write the full script upfront so chapters flow together narratively, but produce them one at a time.

### Frame Chaining

Extend a continuous shot to any length by feeding the last frame of each clip into the next:

1. Generate the first clip (text-to-video or image-to-video)
2. Extract the last frame: `ffmpeg -sseof -0.1 -i clip-1.mp4 -frames:v 1 -q:v 2 last-frame.jpg`
3. Save the frame to workspace, generate the next clip using it as `image_path` with a prompt describing how the scene *continues*
4. Repeat for as many clips as needed, then stitch together

Write continuation prompts naturally — if clip 1 shows "a woman walking through a forest", the next prompt continues: "she reaches a clearing and looks up at the sky".

**Use Veo models for frame chaining** — they treat the input image as the literal first frame, giving seamless visual continuity. Sora treats it as a style reference, which can cause visual drift between clips.

Combines naturally with storyboarding: use a unique storyboard keyframe for the first clip of each scene, then frame-chain within a scene for longer continuous shots. Frame chaining works well for continuous motion, slow ambient shots, gradual transitions, and establishing shots — but don't use it as a shortcut to avoid generating new keyframes for visually distinct moments.

### Image Transformation

When the user provides photos that aren't ideal as direct starting frames (wrong style, too busy, not cinematic), transform them:

1. Use `asi-generate-image` with the user's image(s) as reference inputs, prompting for a version optimized as a video starting frame — clean composition, cinematic look. Set the aspect ratio to match your target video (e.g., 16:9).
2. Use the generated image as `image_path` in `asi-generate-video`.

Example: user uploads a product photo → `asi-generate-image` with the photo as reference, prompt "cinematic product shot centered on dark gradient background, studio lighting, clean composition" → `asi-generate-video` with the result as `image_path`, prompt "camera slowly orbits around the product, dramatic lighting shifts..."

### Custom Voiceover

When you want precise control over narration or dialogue:

1. Write the voiceover script — either a .txt file for single narrator or .json for multi-speaker dialogue with emotion/flow tags
2. Generate audio with `asi-text-to-speech`
3. Mix the voiceover over video using ffmpeg (see Audio Design section above)

### Subtitles

Generate subtitles from any video's audio:

1. `asi-transcribe-audio` with `timestamps="word"` on the video file → produces JSON with word-level timing
2. Convert to .srt format
3. Burn in with ffmpeg: `ffmpeg -i video.mp4 -vf "subtitles=subs.srt" -preset fast output.mp4`

### Stitching Clips

All multi-clip productions need a final stitch. For hard cuts between scenes:
```
ffmpeg -f concat -safe 0 -i videos.txt -c copy final.mp4
```
Where `videos.txt` lists one `file 'clip-N.mp4'` per line.

For smoother scene transitions (crossfades, fade to/from black), use ffmpeg's xfade filter between clips:
```
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "xfade=transition=fade:duration=0.5:offset=7.5" output.mp4
```
Where `offset` = duration of first clip minus the transition duration. Choose transitions that match the tone — `fade` or `dissolve` for narrative content, hard cuts for fast-paced edits.

## Quality Verification

Review your work at every stage — don't wait until the final stitch to discover problems.

**After each keyframe**: Does it match the style string? Is the subject consistent with references? Is the composition clean and the aspect ratio correct? Regenerate before building video on top of a bad frame.

**After each video clip**: Does the motion look natural? Does the subject match the keyframe? Is there any visual artifact or distortion? Check actual duration with `ffprobe`.

**After each segment**: Play back the segment's video with its voiceover. Does the pacing feel right? Is the audio/video alignment close enough? Lock the segment before moving on.

**Final production check**: After stitching everything together, review the complete video end-to-end. Check for: jarring transitions between scenes, inconsistent visual style, audio sync issues, any silent gaps or abrupt cuts. Fix individual segments rather than trying to patch the final output.

## Generated Video vs. Captured Video

AI video models create new visual content — they don't reproduce existing artifacts faithfully. Text, layouts, and precise details will drift or distort.

When the goal is to **show something that already exists** (an app, a website, a document, a dashboard, a design), capture it directly: take screenshots or screen grabs, then stitch them into a video with ffmpeg transitions and optional TTS narration or music. This is cheaper, faster, and accurate.

When the goal is to **create something new** (a cinematic trailer, a mood piece, product concept art, storytelling), AI video generation is the right tool.

## Guidelines

- Be ambitious with creative video production — break complex requests into steps and execute.
- **STOP and confirm before expensive work.** For longer productions, you MUST use confirm_action to get user approval before generating any video — let them know this will use a lot of credits. The user only needs to know how long the video is and that it's expensive, they don't need implementation details like number of clips compiled together. Do not skip this step.
- Never re-encode or reduce video quality to shrink file size — send full-quality output to the user
- **Never use ffmpeg atempo, setpts, asetpts, or any time-stretching/speed adjustment on generated video or speech audio.** This always produces distorted, unusable output. If video is too short, use frame chaining to extend it. If audio is too long, shorten the script and regenerate.
- Use the same aspect ratio throughout all clips in a production
- For frame chaining workflows, prefer Veo models (literal first frame) over Sora (style reference that can drift)
- Video generation takes 1-3 minutes per clip — inform the user and generate sequentially
- Don't create title cards or text overlays with ffmpeg drawtext — they look cheap. For titles and intros, generate a title image with `asi-generate-image` and animate it with `asi-generate-video` — a 4-second animated title sequence looks far more professional than a static card

## FFmpeg in the Sandbox

The sandbox has only 2 vCPUs. Encode settings and timeouts must account for this.

**Encoding presets:** Use `-preset fast` or `-preset medium`. Never use `slow`, `slower`, or `veryslow` — they will timeout or take unreasonably long on 2 vCPUs.

**Quality (CRF):** Use `-crf 23` for general output. For social media, `-crf 26` to `-crf 28` is fine since platforms re-encode anyway. For archival or broadcast, `-crf 18` to `-crf 20`.

**Pixel format:** Always use `-pix_fmt yuv420p`. AI-generated images are often RGB, which causes libx264 to default to `yuv444p` (H.264 High 4:4:4 Predictive profile). Browsers only decode 4:2:0.

**Bash timeout:** Always set the bash tool timeout to at least 300000 (5 minutes) for any ffmpeg command. Complex filter chains or longer videos may need even more.

**Example — fast encode:**
```bash
ffmpeg -i input.mp4 -preset fast -crf 26 -pix_fmt yuv420p -c:a aac -b:a 128k output.mp4
```

## Vertical Video (9:16)

To convert landscape footage to vertical 1080x1920:

**Crop + scale filter chain:**
```
-vf "crop=ih*9/16:ih,scale=1080:1920"
```

**ASS subtitles for vertical video:** Set `PlayResX: 1080` and `PlayResY: 1920` in the ASS header so text positions map correctly to the vertical frame:
```
[Script Info]
PlayResX: 1080
PlayResY: 1920
```
