import pytest
from say_e11.providers import build_provider
from say_e11.providers.elevenlabs import ElevenLabsProvider
from say_e11.providers.deepgram import DeepgramProvider


def test_build_elevenlabs():
    assert isinstance(build_provider("elevenlabs", "key"), ElevenLabsProvider)


def test_build_deepgram():
    assert isinstance(build_provider("deepgram", "key"), DeepgramProvider)


def test_build_unknown_raises():
    with pytest.raises(ValueError, match="Unknown provider"):
        build_provider("openai", "key")
