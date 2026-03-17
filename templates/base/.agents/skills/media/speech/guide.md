# Speech Guide

**Default model: Gemini 2.5 Pro TTS.** Always use Gemini unless the user explicitly requests ElevenLabs or the dialogue requires 3+ distinct speakers (Gemini supports max 2 voices, ElevenLabs supports up to 10). Set `model="elevenlabs_tts_v3"` only in those cases.

**Single speaker** — write to `.txt`, specify voice:
```bash
asi-text-to-speech '{"file_path": "/home/user/workspace/script.txt", "voice": "charon"}'
```

**Multi-speaker dialogue** — write to `.json`:
```json
[
  {"speaker": "kore", "text": "Welcome to the show!"},
  {"speaker": "puck", "text": "Thanks for having me."},
  {"speaker": "kore", "text": "So I was thinking we could—"},
  {"speaker": "puck", "text": "[interrupts] Wait, did you see the news?"},
  {"speaker": "kore", "text": "[whispers] ...no, what happened?"}
]
```
```bash
asi-text-to-speech '{"file_path": "/home/user/workspace/dialogue.json"}'
```

## Gemini Voices (default)

Full list in `voices.txt` (this directory). Popular picks:
- **kore**: strong and firm (female) — default voice
- **charon**: calm and professional, deep steady tone (male)
- **puck**: upbeat and lively (male)
- **aoede**: relaxed and natural, good for assistants (female)
- **rasalgethi**: professional narrator style (male)
- **fenrir**: passionate and energetic (male)
- **sulafat**: warm and approachable (female)
- **erinome**: clear and articulate (female)
- **alnilam**: confident and firm (male)
- **callirrhoe**: friendly and easy-going (female)

All 30 Gemini voices: achernar, achird, algenib, algieba, alnilam, aoede, autonoe, callirrhoe, charon, despina, enceladus, erinome, fenrir, gacrux, iapetus, kore, laomedeia, leda, orus, pulcherrima, puck, rasalgethi, sadachbia, sadaltager, schedar, sulafat, umbriel, vindemiatrix, zephyr, zubenelgenubi

## ElevenLabs Voices

Use `model="elevenlabs_tts_v3"` with these voices. Popular picks:
- **sarah**: soft young female, professional/news
- **rachel**: calm soothing female, narration
- **matilda**: warm friendly female, audiobooks
- **adam**: deep authoritative American male, formal narration
- **brian**: deep rich American male, conversational narration
- **daniel**: deep British male, documentaries/news
- **charlie**: casual Australian male, informal

## Delivery Control

| Technique | Example | Effect |
|-----------|---------|--------|
| Em dash (—) | `"But I thought—"` | Cut off / interrupted |
| Ellipsis (...) | `"I don't know..."` | Hesitation, trailing off |
| CAPS | `"This is EXACTLY it"` | Emphasis |
| Emotion tags | `"[laughs] That's funny"` | Delivery cue |
| Flow tags | `"[interrupts] Actually—"` | Turn-taking dynamics |

**Emotion**: `[whispers]`, `[laughs]`, `[sighs]`, `[excited]`, `[sarcastic]`, `[sad]`, `[angry]`, `[surprised]`, `[nervous]`, `[calm]`

**Flow**: `[interrupting]`, `[overlapping]`, `[starting to speak]`, `[cuts in]`, `[talks over]`, `[hesitates]`, `[stammers]`, `[pause]`

**Reactions**: `[gasps]`, `[gulps]`, `[clears throat]`, `[coughs]`, `[sniffles]`, `[groans]`, `[yawns]`

**Sound effects**: `[applause]`, `[door knock]`, `[footsteps]`, `[phone rings]`, `[thunder]`, `[explosion]` — embedded inline

**Accents**: `[British accent]`, `[Southern accent]`, `[French accent]` — use `[strong X accent]` or `[slight X accent]`

Full tag reference with 100+ tags: `tags-reference.md` (this directory)

**Interruption pattern**: Em dash on interrupted speaker + flow tag on interrupter:
```json
{"speaker": "alice", "text": "[starting to speak] So I was thinking we could—"},
{"speaker": "bob", "text": "[interrupting] —wait, did you hear that?"}
```

Note: Flow tags (`[interrupting]`, `[overlapping]`, `[cuts in]`) affect delivery style (rushed entry, natural pacing) but audio is still sequential — no true simultaneous speech. The em dash creates a cut-off sound, and flow tags make transitions feel natural.

## Tips
- Combine tags: `"[whispers][sad] I can't believe it's over..."`
- Max 2 unique voices per dialogue with Gemini, max 10 with ElevenLabs
- Keep lines conversational length for natural pacing
- Output: MP3 at 44.1kHz/128kbps
- ElevenLabs models: `eleven_v3` (dialogue), `eleven_multilingual_v2` (single speaker)
- Never use ffmpeg atempo or other speed adjustments unless the user explicitly asks for it — control duration by adjusting script length instead

## Custom Voices

The `asi-text-to-speech` CLI uses a fixed set of voices (listed in `voices.txt`). For custom or cloned voices, the user needs their own ElevenLabs account:

1. User creates a custom voice in their ElevenLabs account (voice cloning, voice design, etc.)
2. User provides their **voice ID** and **ElevenLabs API key**
3. Use bash to make direct HTTP requests to the ElevenLabs API with the user's credentials — do **not** use `asi-text-to-speech`

Consult the ElevenLabs API docs (`https://elevenlabs.io/docs/api-reference`) for endpoint details. The text-to-speech endpoint is `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` with header `xi-api-key: {api_key}`.
