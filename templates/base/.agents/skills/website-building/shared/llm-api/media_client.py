"""Provider-agnostic media adapter contract for copied helper scripts.

Implement ``create_media_client()`` in your project with the SDK your runtime supports.
The helper scripts in this directory call only this narrow interface so the shared
reference stays portable.
"""

from __future__ import annotations

from typing import Protocol, TypedDict


class DialogueTurn(TypedDict):
    speaker: str
    text: str


class TranscriptionWord(TypedDict, total=False):
    text: str
    start: float | int
    end: float | int
    speaker_id: int | str | None


class TranscriptionResult(TypedDict, total=False):
    text: str
    language_code: str | None
    words: list[TranscriptionWord]


class MediaClient(Protocol):
    async def generate_image(
        self,
        prompt: str,
        *,
        image_bytes: bytes | None = None,
        image_media_type: str | None = None,
        aspect_ratio: str = "1:1",
        model: str = "nano_banana_2",
    ) -> bytes: ...

    async def generate_video(
        self,
        prompt: str,
        *,
        image_bytes: bytes | None = None,
        image_media_type: str | None = None,
        aspect_ratio: str = "16:9",
        duration: int = 8,
        audio: bool = True,
        model: str = "sora_2",
    ) -> bytes: ...

    async def generate_audio(
        self,
        text: str,
        *,
        voice: str = "kore",
        model: str = "gemini_2_5_pro_tts",
    ) -> bytes: ...

    async def generate_dialogue(
        self,
        dialogue: list[DialogueTurn],
        *,
        model: str = "gemini_2_5_pro_tts",
    ) -> bytes: ...

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        *,
        media_type: str = "audio/mpeg",
        timestamps: str = "none",
        diarize: bool = False,
        num_speakers: int | None = None,
        language: str | None = None,
        model: str = "elevenlabs_scribe_v2",
    ) -> TranscriptionResult: ...


def create_media_client() -> MediaClient:
    raise NotImplementedError(
        "Implement create_media_client() with the provider SDK your project uses before calling these helpers."
    )
