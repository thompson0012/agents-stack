"""Provider-agnostic async transcription helper.

Copy this file and ``media_client.py`` into your project, implement
``create_media_client()``, then call ``transcribe_audio()`` from your handlers.
"""

from media_client import TranscriptionResult, create_media_client


async def transcribe_audio(
    audio_bytes: bytes,
    *,
    media_type: str = "audio/mpeg",
    timestamps: str = "none",
    diarize: bool = False,
    num_speakers: int | None = None,
    language: str | None = None,
    model: str = "elevenlabs_scribe_v2",
) -> TranscriptionResult:
    client = create_media_client()
    return await client.transcribe_audio(
        audio_bytes,
        media_type=media_type,
        timestamps=timestamps,
        diarize=diarize,
        num_speakers=num_speakers,
        language=language,
        model=model,
    )
