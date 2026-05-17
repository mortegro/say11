# say-e11

A `uv`-installable CLI that replicates macOS `say` on Linux, using
[ElevenLabs](https://elevenlabs.io) or [Deepgram](https://deepgram.com) for
text-to-speech. Drop-in replacement for scripts that call `say`.

```bash
say "Hello, world"
echo "piped text" | say
say -v bella "Using a preset voice"
say --set voice rachel        # save a default
```

---

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- PortAudio (`sudo pacman -S portaudio` on Arch/Manjaro, `sudo apt install libportaudio2` on Debian/Ubuntu)
- An ElevenLabs **or** Deepgram API key

---

## Installation

```bash
uv tool install git+https://github.com/youruser/say-e11
```

Or clone and install locally:

```bash
git clone https://github.com/youruser/say-e11
cd say-e11
uv tool install .
```

---

## API key setup

Create `.env` in your working directory **or** `~/.env` for a global default.
Local `.env` takes precedence; both are ignored by git.

```bash
# ElevenLabs (preferred when both present)
ELEVENLABS_API_KEY=sk-...

# Deepgram
DEEPGRAM_API_KEY=...
```

Process environment variables override both files.

---

## Usage

```
say [TEXT ...] [-f FILE] [-o PATH] [-v NAME] [-r WPM] [--provider {elevenlabs,deepgram}]
    [--set KEY VALUE] [--list-voices] [--show-config]
```

### Text input

| Method | Example |
|--------|---------|
| Positional args | `say hello world` |
| Pipe | `echo "hello" \| say` |
| File | `say -f notes.txt` |

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-v, --voice NAME` | Voice name or raw ID | provider default |
| `-r, --rate WPM` | Speaking rate (words per minute) | 175 |
| `-o, --output PATH` | Also write audio to a WAV file | — |
| `--provider` | Force `elevenlabs` or `deepgram` | auto-detect |
| `--set KEY VALUE` | Save a default setting | — |
| `--list-voices` | Print ElevenLabs voice presets and exit | — |
| `--show-config` | Print current saved defaults and exit | — |

---

## Voice presets

Pass a preset name with `-v` instead of a raw voice ID.

| Name | Description |
|------|-------------|
| `rachel` | Default — calm, American female |
| `bella` | Warm, American female |
| `antoni` | American male |
| `elli` | Young American female |
| `josh` | Young American male |
| `arnold` | American male, strong |
| `adam` | Deep American male |
| `sam` | American male, energetic |
| `domi` | American female, confident |
| `dave` | British male |

Raw ElevenLabs voice IDs also work: `say -v EXAVITQu4vr4xnSDxMaL "hello"`.

---

## Saved defaults

Settings are stored in `~/.say-e11/config.json`. CLI flags always override them.

```bash
say --set voice bella          # set default voice
say --set provider deepgram    # set default provider
say --set rate 200             # set default rate

say --show-config              # view current defaults
```

---

## Providers

| Provider | Key env var | Default voice |
|----------|-------------|---------------|
| ElevenLabs | `ELEVENLABS_API_KEY` | rachel (`21m00Tcm4TlvDq8ikWAM`) |
| Deepgram | `DEEPGRAM_API_KEY` | `aura-2-thalia-en` |

ElevenLabs is preferred when both keys are present. Override with `--provider`
or `say --set provider deepgram`.

**Rate control:** ElevenLabs maps `-r` to a speed factor (175 wpm = 1.0×,
clamped to 0.7–1.2×). Deepgram does not support rate control; `-r` is ignored
with a warning.

---

## Examples

```bash
# Speak from stdin (useful in scripts)
git log --oneline -1 | say

# Write to file and play
say -o out.wav "Recording this"

# Use a specific voice and rate
say -v josh -r 200 "Speaking faster"

# Force Deepgram
say --provider deepgram "Using Deepgram"

# Pipe a file
cat report.txt | say -v bella
```

---

## Development

```bash
git clone https://github.com/youruser/say-e11
cd say-e11
uv sync                      # install deps + dev deps
uv run pytest                # run tests
uv tool install --editable . # install say command for local testing
```

See [CLAUDE.md](CLAUDE.md) for architecture notes and contribution guidelines.

---

## License

MIT
