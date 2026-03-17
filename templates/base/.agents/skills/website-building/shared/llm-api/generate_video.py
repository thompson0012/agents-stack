"""Async video generation via LLM API. Copy into your project and call from FastAPI handlers.

Usage:
    from generate_video import generate_video

    video_bytes = await generate_video("A wave crashing on shore")
    video_bytes = await generate_video("Animate this", image_bytes=frame, image_media_type="image/png")
"""

import base64

from pplx.python.sdks.llm_api import (
    Client,
    Conversation,
    Identity,
    ImageBlock,
    ImageGenAspectRatio,
    ImageSource,
    ImageSourceType,
    LLMAPIClient,
    MediaGenParams,
    SamplingParams,
    TextBlock,
    VideoGenDuration,
    VideoGenParams,
)

ASPECT_RATIOS = {
    "16:9": ImageGenAspectRatio.RATIO_16_9,
    "9:16": ImageGenAspectRatio.RATIO_9_16,
}

DURATIONS = {
    4: VideoGenDuration.DURATION_4S,
    6: VideoGenDuration.DURATION_6S,
    8: VideoGenDuration.DURATION_8S,
    12: VideoGenDuration.DURATION_12S,
}


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
        identity=Identity(client=Client.ASI, use_case="webserver_video_gen"),
        sampling_params=SamplingParams(max_tokens=1),
        media_gen_params=MediaGenParams(
            video=VideoGenParams(
                number_of_videos=1,
                duration=DURATIONS.get(duration, VideoGenDuration.DURATION_8S),
                generate_audio=audio,
                aspect_ratio=ASPECT_RATIOS.get(aspect_ratio, ImageGenAspectRatio.RATIO_16_9),
            ),
        ),
    )

    if not result.videos:
        raise RuntimeError("No video generated")
    return base64.b64decode(result.videos[0].b64_data)
