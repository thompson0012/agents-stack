# LLM & Media API Access

The `anthropic` and `openai` SDKs (Python and Node.js) and `pplx.python.sdks.llm_api` are pre-installed in the sandbox. **Credentials are NOT available by default** — you must inject them via the `api_credentials` field on the `start_server` tool every time you start or restart a server.

**Important:** The OpenAI proxy only supports the Responses API (`client.responses.create`), not Chat Completions.

### Credential Presets

| Preset | TTL | Use when |
|--------|-----|----------|
| `llm-api:website` | Auto-refreshed | Website backend servers |

**Every `start_server()` call that starts a server using LLM/media APIs must include `api_credentials=["llm-api:website"]`.** Without it, API calls will fail with authentication errors.

```
start_server(command="python server.py", project_path="/home/user/workspace", port=8000, api_credentials=["llm-api:website"])
```

## Available Models

**Text/Chat:** claude_sonnet_4_5, claude_opus_4_5, claude_opus_4_6, claude_sonnet_4_6, claude_haiku_4_5, gpt5_mini, gpt5_nano, gpt_5_chat, gpt_5_1, gpt_5_1_chat, gpt_5_2, gpt_5_3_codex, gpt_5_4, gpt_5_2_pro, grok_4_1_reasoning, gemini_3_pro, gemini_3_1_pro, gemini_3_flash

**Image:** nano_banana_pro, nano_banana_2

**Video:** sora_2, sora_2_pro, veo_3_1, veo_3_1_fast

**Audio:** elevenlabs_tts_v3, elevenlabs_scribe_v2, gemini_2_5_pro_tts

## Text/Chat — Anthropic SDK (Messages API)

```python
from anthropic import Anthropic
client = Anthropic()
message = client.messages.create(
    model="claude_sonnet_4_6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

## Text/Chat — OpenAI SDK (Responses API)

```python
from openai import OpenAI
client = OpenAI()
response = client.responses.create(
    model="gpt_5_1",
    input="Hello",
)
```

## Media Generation & Transcription — SDK Helper Scripts

Media generation (image, video, audio) and transcription use a separate SDK (`pplx.python.sdks.llm_api`). **Do not use the Anthropic SDK for media.** Ready-to-use async helper scripts are in `shared/llm-api/`. **Read the relevant file, then copy it into your project directory** and import it from your FastAPI handlers.

| File | What it does | Key function |
|------|-------------|--------------|
| `shared/llm-api/generate_image.py` | Text-to-image, image-to-image editing | `await generate_image(prompt, image_bytes=..., aspect_ratio=...)` |
| `shared/llm-api/generate_video.py` | Text-to-video, image-to-video animation | `await generate_video(prompt, image_bytes=..., duration=...)` |
| `shared/llm-api/generate_audio.py` | Text-to-speech, multi-speaker dialogue | `await generate_audio(text, voice=...)` / `await generate_dialogue(lines)` |
| `shared/llm-api/transcribe_audio.py` | Audio/video transcription with diarization | `await transcribe_audio(audio_bytes, media_type=..., diarize=...)` |

### Website Backend Example

Read the helper file, copy it into your project, then import it. **Always use `start_server` with `api_credentials=["llm-api:website"]`** — this is required every time you start or restart the server process.

```python
from generate_image import generate_image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import base64

app = FastAPI()

@app.post("/api/generate")
async def generate(prompt: str, file: UploadFile | None = None, aspect_ratio: str = "1:1"):
    image_bytes = await file.read() if file else None
    result = await generate_image(
        prompt,
        image_bytes=image_bytes,
        image_media_type=file.content_type if file else None,
        aspect_ratio=aspect_ratio,
    )
    b64 = base64.b64encode(result).decode()
    return {"image": f"data:image/png;base64,{b64}"}
```

### Image Generation Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Image description | Required |
| `image_bytes` | Input image bytes for img2img | None |
| `image_media_type` | MIME type of input image (image/png, image/jpeg, image/webp) | image/png |
| `aspect_ratio` | 1:1, 3:4, 4:3, 9:16, 16:9 | 1:1 |
| `model` | nano_banana_pro, nano_banana_2 | nano_banana_2 |

### Video Generation Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Video description | Required |
| `image_bytes` | Starting frame image for image-to-video | None |
| `image_media_type` | MIME type of starting frame | image/png |
| `aspect_ratio` | 16:9, 9:16 | 16:9 |
| `duration` | 4, 6, 8, 12 (seconds) | 8 |
| `audio` | Generate audio track | True |
| `model` | sora_2, sora_2_pro, veo_3_1, veo_3_1_fast | sora_2 |

### Audio Generation Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `text` | Text to speak | Required |
| `voice` | Voice name (see below) | kore |
| `model` | elevenlabs_tts_v3, gemini_2_5_pro_tts | gemini_2_5_pro_tts |

**Multi-speaker dialogue:** Use `generate_dialogue()` with a list of `{"speaker": "voice", "text": "..."}` dicts.

**Gemini voices (max 2 in dialogue):** achernar, achird, algenib, algieba, alnilam, aoede, autonoe, callirrhoe, charon, despina, enceladus, erinome, fenrir, gacrux, iapetus, kore, laomedeia, leda, orus, pulcherrima, puck, rasalgethi, sadachbia, sadaltager, schedar, sulafat, umbriel, vindemiatrix, zephyr, zubenelgenubi

**ElevenLabs voices (max 10 in dialogue):** rachel, adam, alice, antoni, arnold, bill, brian, callum, charlie, charlotte, chris, clyde, daniel, dave, domi, dorothy, drew, emily, ethan, fin, freya, george, gigi, giovanni, glinda, grace, harry, james, jeremy, jessie, joseph, josh, liam, lily, matilda, michael, mimi, nicole, patrick, paul, sam, santa, sarah, serena, thomas

### Transcription Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `audio_bytes` | Audio/video file bytes | Required |
| `media_type` | MIME type (audio/mpeg, audio/wav, audio/mp4, audio/webm, audio/ogg, audio/flac) | audio/mpeg |
| `timestamps` | none, word, character | none |
| `diarize` | Enable speaker diarization | False |
| `num_speakers` | Expected speakers (1-32, with diarize) | auto-detect |
| `language` | ISO 639-1 code (e.g. en, es, fr) | auto-detect |
| `model` | elevenlabs_scribe_v2 | elevenlabs_scribe_v2 |
