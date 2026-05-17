import httpx

DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
_SPEED_MIN = 0.7
_SPEED_MAX = 1.2
_BASE_RATE = 175


class ElevenLabsProvider:
    def __init__(self, api_key: str, *, client: httpx.Client | None = None) -> None:
        self._key = api_key
        self._client = client or httpx.Client()

    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes:
        voice_id = voice or DEFAULT_VOICE
        speed = max(_SPEED_MIN, min(_SPEED_MAX, rate / _BASE_RATE))
        r = self._client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            params={"output_format": "pcm_24000"},
            headers={"xi-api-key": self._key},
            json={
                "text": text,
                "model_id": "eleven_turbo_v2_5",
                "voice_settings": {"speed": speed},
            },
            timeout=30.0,
        )
        if r.status_code != 200:
            raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text[:200]}")
        return r.content
