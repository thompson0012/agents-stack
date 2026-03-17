"""Async audio transcription via LLM API. Copy into your project and call from FastAPI handlers.

Usage:
    from transcribe_audio import transcribe_audio

    result = await transcribe_audio(audio_bytes, media_type="audio/mpeg")
    print(result["text"])

    result = await transcribe_audio(audio_bytes, media_type="audio/mpeg", diarize=True, timestamps="word")
    for word in result["words"]:
        print(f"[Speaker {word['speaker_id']}] {word['text']} ({word['start']}-{word['end']})")
"""

import base64

from pplx.python.sdks.llm_api import (
    AudioBlock,
    AudioSource,
    Client,
    Conversation,
    Identity,
    LLMAPIClient,
    MediaGenParams,
    SamplingParams,
    SpeechToTextParams,
)


async def transcribe_audio(
    audio_bytes: bytes,
    *,
    media_type: str = "audio/mpeg",
    timestamps: str = "none",
    diarize: bool = False,
    num_speakers: int | None = None,
    language: str | None = None,
    model: str = "elevenlabs_scribe_v2",
) -> dict:
    client = LLMAPIClient()
    b64 = base64.b64encode(audio_bytes).decode()
    convo = Conversation()
    convo.add_user(AudioBlock(source=AudioSource(media_type=media_type, data=b64)))

    result = await client.messages.create(
        model=model,
        convo=convo,
        identity=Identity(client=Client.ASI, use_case="webserver_transcription"),
        sampling_params=SamplingParams(max_tokens=1),
        media_gen_params=MediaGenParams(
            speech_to_text=SpeechToTextParams(
                diarize=diarize,
                num_speakers=num_speakers,
                timestamps_granularity=timestamps,
                language_code=language,
            ),
        ),
    )

    if not result.transcriptions:
        raise RuntimeError("No transcription generated")

    t = result.transcriptions[0]
    return {
        "text": t.text,
        "language_code": t.language_code,
        "words": [{"text": w.text, "start": w.start, "end": w.end, "speaker_id": w.speaker_id} for w in t.words],
    }
