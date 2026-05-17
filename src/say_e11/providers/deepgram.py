import sys

import httpx

DEFAULT_VOICE = "aura-2-thalia-en"
_BASE_RATE = 175

VOICE_PRESETS: dict[str, str] = {
    "thalia":   "aura-2-thalia-en",
    "asteria":  "aura-2-asteria-en",
    "luna":     "aura-2-luna-en",
    "aurora":   "aura-2-aurora-en",
    "athena":   "aura-2-athena-en",
    "zeus":     "aura-2-zeus-en",
    "orion":    "aura-2-orion-en",
    "orpheus":  "aura-2-orpheus-en",
    "apollo":   "aura-2-apollo-en",
    "hermes":   "aura-2-hermes-en",
}


def resolve_voice(voice: str | None) -> str:
    if voice is None:
        return DEFAULT_VOICE
    return VOICE_PRESETS.get(voice.lower(), voice)


class DeepgramProvider:
    def __init__(self, api_key: str, *, client: httpx.Client | None = None) -> None:
        self._key = api_key
        self._owns_client = client is None
        self._client = client or httpx.Client()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "DeepgramProvider":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes:
        model = resolve_voice(voice)
        if rate != _BASE_RATE:
            print(
                f"Warning: Deepgram does not support rate control; ignoring -r {rate}",
                file=sys.stderr,
            )
        r = self._client.post(
            "https://api.deepgram.com/v1/speak",
            params={
                "model": model,
                "encoding": "linear16",
                "sample_rate": 24000,
                "container": "none",
            },
            headers={"Authorization": f"Token {self._key}"},
            json={"text": text},
            timeout=30.0,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Deepgram error {r.status_code}: {r.text[:200]}")
        return r.content
