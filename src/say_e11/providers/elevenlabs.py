import httpx

DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL = "eleven_turbo_v2_5"
_SPEED_MIN = 0.7
_SPEED_MAX = 1.2
_BASE_RATE = 175

# Friendly name → ElevenLabs voice ID
VOICE_PRESETS: dict[str, str] = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "bella":  "EXAVITQu4vr4xnSDxMaL",
    "antoni": "ErXwobaYiN019PkySvjV",
    "elli":   "MF3mGyEYCl7XYWbV9V6O",
    "josh":   "TxGEqnHWrfWFTfGW9XjX",
    "arnold": "VR6AewLTigWG4xSOukaG",
    "adam":   "pNInz6obpgDQGcFmaJgB",
    "sam":    "yoZ06aMxZJJ28mfd3POQ",
    "domi":   "AZnzlk1XvdvUeBnXmlld",
    "dave":   "CYw3kZ78EXa7QGL7Umo",
}


def resolve_voice(voice: str | None) -> str:
    if voice is None:
        return DEFAULT_VOICE
    return VOICE_PRESETS.get(voice.lower(), voice)


class ElevenLabsProvider:
    def __init__(self, api_key: str, *, client: httpx.Client | None = None) -> None:
        self._key = api_key
        self._owns_client = client is None
        self._client = client or httpx.Client()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "ElevenLabsProvider":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes:
        voice_id = resolve_voice(voice)
        speed = max(_SPEED_MIN, min(_SPEED_MAX, rate / _BASE_RATE))
        r = self._client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            params={"output_format": "pcm_24000"},
            headers={"xi-api-key": self._key},
            json={
                "text": text,
                "model_id": DEFAULT_MODEL,
                "voice_settings": {"speed": speed},
            },
            timeout=30.0,
        )
        if r.status_code != 200:
            raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text[:200]}")
        return r.content
