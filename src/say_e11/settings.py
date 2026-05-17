import json
import sys
from pathlib import Path

_CONFIG_DIR = Path.home() / ".say-e11"
_CONFIG_FILE = _CONFIG_DIR / "config.json"

VALID_KEYS = {"voice", "provider", "rate"}
_PROVIDER_CHOICES = {"elevenlabs", "deepgram"}


def load() -> dict:
    if not _CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_key(key: str, value: str) -> None:
    if key not in VALID_KEYS:
        print(
            f"Error: unknown setting '{key}'. Valid: {', '.join(sorted(VALID_KEYS))}",
            file=sys.stderr,
        )
        sys.exit(1)
    config = load()
    if key == "rate":
        try:
            config[key] = int(value)
        except ValueError:
            print(f"Error: rate must be an integer, got '{value}'", file=sys.stderr)
            sys.exit(1)
    elif key == "provider" and value not in _PROVIDER_CHOICES:
        print(
            f"Error: provider must be one of {', '.join(sorted(_PROVIDER_CHOICES))}",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        config[key] = value
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Default {key} set to '{value}'")
