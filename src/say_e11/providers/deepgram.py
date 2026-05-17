import sys

import httpx

DEFAULT_VOICE = "aura-2-thalia-en"
_BASE_RATE = 175


class DeepgramProvider:
    def __init__(self, api_key: str, *, client: httpx.Client | None = None) -> None:
        self._key = api_key
        self._owns_client = client is None
        self._client = client or httpx.Client()

    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes:
        model = voice or DEFAULT_VOICE
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
                "sample_rate": "24000",
                "container": "none",
            },
            headers={"Authorization": f"Token {self._key}"},
            json={"text": text},
            timeout=30.0,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Deepgram error {r.status_code}: {r.text[:200]}")
        return r.content

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "DeepgramProvider":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
