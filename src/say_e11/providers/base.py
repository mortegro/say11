from typing import Protocol


class Provider(Protocol):
    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes: ...
