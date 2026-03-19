"""Provider-agnostic async video generation helper.

Copy this file and ``media_client.py`` into your project, implement
``create_media_client()``, then call ``generate_video()`` from your handlers.
"""

from media_client import create_media_client


async def generate_video(
    prompt: str,
    *,
    image_bytes: bytes | None = None,
    image_media_type: str | None = None,
    aspect_ratio: str = "16:9",
    duration: int = 8,
    audio: bool = True,
    model: str = "sora_2",
) -> bytes:
    client = create_media_client()
    return await client.generate_video(
        prompt,
        image_bytes=image_bytes,
        image_media_type=image_media_type,
        aspect_ratio=aspect_ratio,
        duration=duration,
        audio=audio,
        model=model,
    )
