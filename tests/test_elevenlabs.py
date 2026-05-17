import json
import httpx
import pytest
from say_e11.providers.elevenlabs import ElevenLabsProvider

FAKE_PCM = b"\x00\x01" * 100


class MockTransport(httpx.BaseTransport):
    def __init__(self, content: bytes, status_code: int = 200):
        self._content = content
        self._status = status_code

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return httpx.Response(self._status, content=self._content)


class CaptureTransport(httpx.BaseTransport):
    def __init__(self, content: bytes = FAKE_PCM):
        self._content = content
        self.requests: list[httpx.Request] = []
        self.bodies: list[dict] = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        self.bodies.append(json.loads(request.content))
        return httpx.Response(200, content=self._content)


def test_synthesize_returns_pcm():
    client = httpx.Client(transport=MockTransport(FAKE_PCM))
    p = ElevenLabsProvider("key-abc", client=client)
    assert p.synthesize("hello", None, 175) == FAKE_PCM


def test_synthesize_uses_default_voice():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    assert "21m00Tcm4TlvDq8ikWAM" in str(t.requests[0].url)


def test_synthesize_uses_custom_voice():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", "my-voice", 175)
    assert "my-voice" in str(t.requests[0].url)


def test_synthesize_sends_api_key_header():
    t = CaptureTransport()
    p = ElevenLabsProvider("secret-key", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    assert t.requests[0].headers["xi-api-key"] == "secret-key"


def test_synthesize_requests_pcm_format():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    assert "pcm_24000" in str(t.requests[0].url)


def test_synthesize_speed_at_default_rate():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    speed = t.bodies[0]["voice_settings"]["speed"]
    assert speed == pytest.approx(1.0)


def test_synthesize_clamps_speed_low():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 10)  # very slow → should clamp to 0.7
    speed = t.bodies[0]["voice_settings"]["speed"]
    assert speed == pytest.approx(0.7)


def test_synthesize_clamps_speed_high():
    t = CaptureTransport()
    p = ElevenLabsProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 500)  # very fast → should clamp to 1.2
    speed = t.bodies[0]["voice_settings"]["speed"]
    assert speed == pytest.approx(1.2)


def test_synthesize_raises_on_http_error():
    client = httpx.Client(transport=MockTransport(b"bad request", status_code=400))
    p = ElevenLabsProvider("key-abc", client=client)
    with pytest.raises(RuntimeError, match="ElevenLabs error 400"):
        p.synthesize("hello", None, 175)
