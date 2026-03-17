"""Async audio generation (TTS) via LLM API. Copy into your project and call from FastAPI handlers.

Usage:
    from generate_audio import generate_audio, generate_dialogue

    audio_bytes = await generate_audio("Hello world", voice="kore")
    audio_bytes = await generate_dialogue([
        {"speaker": "kore", "text": "Welcome!"},
        {"speaker": "charon", "text": "Thanks for having me."},
    ])
"""

import base64

from pplx.python.sdks.llm_api import (
    AudioGenParams,
    Client,
    Conversation,
    DialogueInput,
    Identity,
    LLMAPIClient,
    MediaGenParams,
    SamplingParams,
)

TTS_OUTPUT_FORMAT = "mp3_44100_128"


async def generate_audio(
    text: str,
    *,
    voice: str = "kore",
    model: str = "gemini_2_5_pro_tts",
) -> bytes:
    client = LLMAPIClient()
    convo = Conversation()
    convo.set_single_audio_prompt(text)

    result = await client.messages.create(
        model=model,
        convo=convo,
        identity=Identity(client=Client.ASI, use_case="webserver_audio_gen"),
        sampling_params=SamplingParams(max_tokens=1),
        media_gen_params=MediaGenParams(
            audio=AudioGenParams(voice=voice, output_format=TTS_OUTPUT_FORMAT),
        ),
    )

    if not result.audios:
        raise RuntimeError("No audio generated")
    return base64.b64decode(result.audios[0].b64_data)


async def generate_dialogue(
    dialogue: list[dict],
    *,
    model: str = "gemini_2_5_pro_tts",
) -> bytes:
    client = LLMAPIClient()
    inputs = [DialogueInput(voice=d["speaker"], text=d["text"]) for d in dialogue]
    convo = Conversation()
    convo.set_dialogue_prompt(inputs)

    result = await client.messages.create(
        model=model,
        convo=convo,
        identity=Identity(client=Client.ASI, use_case="webserver_audio_gen"),
        sampling_params=SamplingParams(max_tokens=1),
        media_gen_params=MediaGenParams(
            audio=AudioGenParams(output_format=TTS_OUTPUT_FORMAT, dialogue_inputs=inputs),
        ),
    )

    if not result.audios:
        raise RuntimeError("No audio generated")
    return base64.b64decode(result.audios[0].b64_data)
