import httpx
import pytest
from say_e11.providers.deepgram import DeepgramProvider

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

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(200, content=self._content)


def test_synthesize_returns_pcm():
    client = httpx.Client(transport=MockTransport(FAKE_PCM))
    p = DeepgramProvider("key-abc", client=client)
    assert p.synthesize("hello", None, 175) == FAKE_PCM


def test_synthesize_sends_auth_header():
    t = CaptureTransport()
    p = DeepgramProvider("dg-secret", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    assert t.requests[0].headers["Authorization"] == "Token dg-secret"


def test_synthesize_requests_linear16():
    t = CaptureTransport()
    p = DeepgramProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    url = str(t.requests[0].url)
    assert "linear16" in url
    assert "24000" in url
    assert "container=none" in url


def test_synthesize_uses_default_voice():
    t = CaptureTransport()
    p = DeepgramProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", None, 175)
    assert "aura-2-thalia-en" in str(t.requests[0].url)


def test_synthesize_uses_custom_voice():
    t = CaptureTransport()
    p = DeepgramProvider("key-abc", client=httpx.Client(transport=t))
    p.synthesize("hello", "aura-2-orion-en", 175)
    assert "aura-2-orion-en" in str(t.requests[0].url)


def test_synthesize_warns_on_non_default_rate(capsys):
    client = httpx.Client(transport=MockTransport(FAKE_PCM))
    p = DeepgramProvider("key-abc", client=client)
    p.synthesize("hello", None, 200)
    assert "rate" in capsys.readouterr().err.lower()


def test_synthesize_no_warning_at_default_rate(capsys):
    client = httpx.Client(transport=MockTransport(FAKE_PCM))
    p = DeepgramProvider("key-abc", client=client)
    p.synthesize("hello", None, 175)
    assert capsys.readouterr().err == ""


def test_synthesize_raises_on_http_error():
    client = httpx.Client(transport=MockTransport(b"unauthorized", status_code=401))
    p = DeepgramProvider("key-abc", client=client)
    with pytest.raises(RuntimeError, match="Deepgram error 401"):
        p.synthesize("hello", None, 175)
