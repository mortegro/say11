# say-e11 — Claude Code context

TTS CLI that replicates macOS `say` on Linux. Installed as the `say` command
via `uv tool install`.

## Essential commands

```bash
uv sync                       # install all deps (runtime + dev)
uv run pytest                 # run test suite (66 tests, ~0.2s)
uv run pytest tests/test_X.py # run one file
uv tool install --editable .  # reinstall say after code changes
say --help                    # verify CLI
```

## Architecture

```
src/say_e11/
  cli.py            # argparse entry point; orchestrates everything
  config.py         # .env/.~env loading; pick_provider()
  settings.py       # ~/.say-e11/config.json read/write; --set logic
  audio.py          # play_pcm() via sounddevice; write_wav() via stdlib wave
  providers/
    base.py         # Provider Protocol (static typing only)
    __init__.py     # build_provider(name, key) factory
    elevenlabs.py   # ElevenLabs REST TTS; VOICE_PRESETS; resolve_voice()
    deepgram.py     # Deepgram REST TTS
```

## Key design decisions

**No SDKs.** Both providers are called via `httpx` directly — the TTS endpoints
are single POST calls and the SDKs add large dependency trees for no benefit.

**Raw PCM throughout.** Both providers return 16-bit mono 24 kHz PCM
(`pcm_24000` / `linear16 + container=none`). This avoids ffmpeg/decoding deps.
`sounddevice` plays it directly; `wave` wraps it for file output.

**Priority order for settings:** CLI flag > `./.env`/`~/.env` > `~/.say-e11/config.json` > hardcoded defaults.
For env loading specifically: process env > local `.env` > `~/.env`.

**`dotenv_values` not `load_dotenv`.** `config.py` reads `.env` files into
dicts without mutating `os.environ`, then applies only missing keys. This
preserves the process environment as the top priority.

**Provider selection:** `_KEY_MAP` iteration order determines priority
(ElevenLabs first). `--provider` and `pick_provider(forced=...)` bypass this.

**`httpx.Client` lifecycle.** Both providers own their client when one is not
injected (`_owns_client`). `cli.py` uses `with build_provider(...) as provider`
to ensure `close()` is called. Tests inject a client directly.

## Provider APIs

### ElevenLabs
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=pcm_24000
Headers: xi-api-key: <key>
Body: {"text": ..., "model_id": "eleven_turbo_v2_5", "voice_settings": {"speed": <factor>}}
```
Speed factor = `rate / 175`, clamped to `[0.7, 1.2]`.

### Deepgram
```
POST https://api.deepgram.com/v1/speak?model=<voice>&encoding=linear16&sample_rate=24000&container=none
Headers: Authorization: Token <key>
Body: {"text": ...}
```
No rate control (warns if `-r` is non-default).

## Testing patterns

- HTTP is mocked with `httpx.BaseTransport` subclasses — no real network calls.
- `CaptureTransport` inspects actual request URL, headers, and JSON body.
- `no_audio` autouse fixture patches `say_e11.cli.play_pcm` to a no-op.
- `no_settings` autouse fixture patches `say_e11.cli.load_settings` to `{}`.
- `config.py` tests patch `say_e11.config.load_env` to isolate selection logic.
- `settings.py` tests patch `_CONFIG_DIR` / `_CONFIG_FILE` via `tmp_path`.
- Audio playback (`play_pcm`) is not unit-tested — hardware dependent.

## System dependency

`sounddevice` requires PortAudio:
```bash
sudo pacman -S portaudio     # Arch/Manjaro
sudo apt install libportaudio2  # Debian/Ubuntu
brew install portaudio       # macOS
```

## Adding a new provider

1. Create `src/say_e11/providers/yourprovider.py` with a class matching the
   `Provider` Protocol: `synthesize(text, voice, rate) -> bytes` returning raw
   PCM (16-bit, 24 kHz, mono).
2. Add `close()`, `__enter__`, `__exit__` following the existing pattern.
3. Add an entry to `_KEY_MAP` in `config.py`.
4. Add a branch in `build_provider()` in `providers/__init__.py`.
5. Add tests in `tests/test_yourprovider.py` with a mocked transport.

## Adding voice presets for Deepgram

`VOICE_PRESETS` lives in `elevenlabs.py` and is ElevenLabs-specific. A
Deepgram voice list would go in `deepgram.py` similarly, with a
`resolve_voice()` function. `cli.py` would need to know which preset list to
use — currently it passes `effective_voice` directly to the provider, which
handles resolution internally.

## Files that should never be committed

- `.env` — API keys (covered by `.gitignore`)
- `~/.say-e11/config.json` — user settings (outside repo)
