import os
import sys
from pathlib import Path

from dotenv import dotenv_values

# Iteration order determines auto-selection priority (elevenlabs preferred).
_KEY_MAP = {
    "elevenlabs": "ELEVENLABS_API_KEY",
    "deepgram": "DEEPGRAM_API_KEY",
}


def load_env(
    home_env: Path | None = None,
    local_env: Path | None = None,
) -> None:
    home_vals = dotenv_values(home_env or Path.home() / ".env")
    local_vals = dotenv_values(local_env or Path(".env"))
    merged = {**home_vals, **local_vals}
    for k, v in merged.items():
        if v is not None and k not in os.environ:
            os.environ[k] = v


def pick_provider(forced: str | None = None) -> tuple[str, str]:
    load_env()
    if forced is not None:
        if forced not in _KEY_MAP:
            print(f"Error: unknown provider '{forced}'", file=sys.stderr)
            sys.exit(1)
        key = os.environ.get(_KEY_MAP[forced])
        if not key:
            print(f"Error: no API key for provider '{forced}'", file=sys.stderr)
            sys.exit(1)
        return forced, key
    for name, env_var in _KEY_MAP.items():
        key = os.environ.get(env_var)
        if key:
            return name, key
    print(
        "Error: no API key found. Set ELEVENLABS_API_KEY or DEEPGRAM_API_KEY"
        " in ./.env or ~/.env",
        file=sys.stderr,
    )
    sys.exit(1)
