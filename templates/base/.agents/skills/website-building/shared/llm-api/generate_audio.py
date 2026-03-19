"""Provider-agnostic async audio generation helper.

Copy this file and ``media_client.py`` into your project, implement
``create_media_client()``, then call these helpers from your handlers.
"""

from media_client import DialogueTurn, create_media_client


async def generate_audio(
    text: str,
    *,
    voice: str = "kore",
    model: str = "gemini_2_5_pro_tts",
) -> bytes:
    client = create_media_client()
    return await client.generate_audio(text, voice=voice, model=model)


async def generate_dialogue(
    dialogue: list[DialogueTurn],
    *,
    model: str = "gemini_2_5_pro_tts",
) -> bytes:
    client = create_media_client()
    return await client.generate_dialogue(dialogue, model=model)
