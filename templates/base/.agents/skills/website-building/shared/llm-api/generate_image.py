"""Provider-agnostic async image generation helper.

Copy this file and ``media_client.py`` into your project, implement
``create_media_client()``, then call ``generate_image()`` from your handlers.
"""

from media_client import create_media_client


async def generate_image(
    prompt: str,
    *,
    image_bytes: bytes | None = None,
    image_media_type: str | None = None,
    aspect_ratio: str = "1:1",
    model: str = "nano_banana_2",
) -> bytes:
    client = create_media_client()
    return await client.generate_image(
        prompt,
        image_bytes=image_bytes,
        image_media_type=image_media_type,
        aspect_ratio=aspect_ratio,
        model=model,
    )
