from typing import Protocol


# Not @runtime_checkable — use for static type checking only.
class Provider(Protocol):
    def synthesize(self, text: str, voice: str | None, rate: int) -> bytes: ...
