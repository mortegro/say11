from say_e11.providers.base import Provider
from say_e11.providers.deepgram import DeepgramProvider
from say_e11.providers.elevenlabs import ElevenLabsProvider


def build_provider(name: str, key: str) -> Provider:
    if name == "elevenlabs":
        return ElevenLabsProvider(key)
    if name == "deepgram":
        return DeepgramProvider(key)
    raise ValueError(f"Unknown provider: {name!r}")
