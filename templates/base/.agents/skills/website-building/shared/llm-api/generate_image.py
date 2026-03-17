"""Async image generation via LLM API. Copy into your project and call from FastAPI handlers.

Usage:
    from generate_image import generate_image

    image_bytes = await generate_image("A sunset over mountains")
    image_bytes = await generate_image("Make this a cartoon", image_bytes=uploaded, image_media_type="image/jpeg")
"""

import base64

from pplx.python.sdks.llm_api import (
    Client,
    Conversation,
    Identity,
    ImageBlock,
    ImageGenAspectRatio,
    ImageGenParams,
    ImageSource,
    ImageSourceType,
    LLMAPIClient,
    MediaGenParams,
    SamplingParams,
    TextBlock,
)

ASPECT_RATIOS = {
    "1:1": ImageGenAspectRatio.RATIO_1_1,
    "3:4": ImageGenAspectRatio.RATIO_3_4,
    "4:3": ImageGenAspectRatio.RATIO_4_3,
    "9:16": ImageGenAspectRatio.RATIO_9_16,
    "16:9": ImageGenAspectRatio.RATIO_16_9,
}


async def generate_image(
    prompt: str,
    *,
    image_bytes: bytes | None = None,
    image_media_type: str | None = None,
    aspect_ratio: str = "1:1",
    model: str = "nano_banana_2",
) -> bytes:
    client = LLMAPIClient()
    convo = Conversation()
    content: list = []
    if image_bytes:
        b64 = base64.b64encode(image_bytes).decode()
        content.append(
            ImageBlock(
                source=ImageSource(
                    type=ImageSourceType.BASE64,
                    media_type=image_media_type or "image/png",
                    data=b64,
                )
            )
        )
    content.append(TextBlock(text=prompt))
    convo.add_user(content)

    result = await client.messages.create(
        model=model,
        convo=convo,
        identity=Identity(client=Client.ASI, use_case="webserver_image_gen"),
        sampling_params=SamplingParams(max_tokens=1),
        media_gen_params=MediaGenParams(
            image=ImageGenParams(
                number_of_images=1,
                aspect_ratio=ASPECT_RATIOS.get(aspect_ratio, ImageGenAspectRatio.RATIO_1_1),
            ),
        ),
    )

    if not result.images:
        raise RuntimeError("No image generated")
    return base64.b64decode(result.images[0].b64_data)
