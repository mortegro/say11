---
title: Usage
nav_order: 3
---

# Usage
{: .no_toc }

<details open markdown="block">
  <summary>Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Synopsis

```
say [TEXT ...] [-f FILE] [-o PATH] [-v NAME] [-r WPM]
    [--provider {elevenlabs,deepgram}]
    [--set KEY VALUE] [--list-voices] [--show-config]
```

---

## Text input

Text can come from three sources, checked in this order:

### Positional arguments

```bash
say hello world
say "This is a longer sentence."
```

### Standard input (pipe)

When no positional arguments are given, `say` reads from stdin. This makes it
useful in shell pipelines.

```bash
echo "piped text" | say
git log --oneline -1 | say
cat report.txt | say
```

### File (`-f`)

```bash
say -f notes.txt
say -f /tmp/announcement.txt
```

---

## Flags reference

### `-v, --voice NAME`

Set the voice for this invocation. Accepts a preset name or a raw provider
voice ID.

```bash
say -v bella "Hello"
say -v josh "Hello"
say -v EXAVITQu4vr4xnSDxMaL "Hello"   # raw ElevenLabs ID
```

See [Voice Presets](voice-presets) for the full list of named voices.

### `-r, --rate WPM`

Speaking rate in words per minute. The default is **175**, matching macOS `say`.

```bash
say -r 120 "Speaking slowly"
say -r 250 "Speaking quickly"
```

{: .note }
Deepgram does not support rate control. If you use `-r` with Deepgram, a
warning is printed and the audio plays at normal speed.

ElevenLabs maps the rate to a speed factor (`rate / 175`, clamped to 0.7–1.2×).

### `-o, --output PATH`

Write the synthesized audio to a WAV file **in addition to** playing it aloud.

```bash
say -o recording.wav "Saving this"
say -o /tmp/out.wav -v rachel "For later"
```

The output is always 16-bit mono 24 kHz WAV, regardless of the file extension.

### `--provider {elevenlabs,deepgram}`

Force a specific provider for this invocation, overriding auto-detection and
any saved default.

```bash
say --provider deepgram "Using Deepgram"
say --provider elevenlabs "Using ElevenLabs"
```

### `--set KEY VALUE`

Save a default setting to `~/.say-e11/config.json`. See
[Configuration](configuration) for details.

```bash
say --set voice bella
say --set provider deepgram
say --set rate 200
```

### `--list-voices`

Print all available ElevenLabs voice presets and exit.

```bash
say --list-voices
```

```
ElevenLabs voice presets:
  rachel     21m00Tcm4TlvDq8ikWAM
  bella      EXAVITQu4vr4xnSDxMaL
  ...
```

### `--show-config`

Print current saved defaults and exit.

```bash
say --show-config
```

```
  voice = bella
  rate = 200
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (no text, no API key, HTTP error, bad output path, etc.) |

Error messages are always written to **stderr**.

---

## Examples

```bash
# Basic usage
say "Good morning"

# Pipe from a command
date | say

# Read a file aloud
say -f README.md

# Record to a file while playing
say -o morning.wav "Recording this greeting"

# Use a different voice and speed
say -v josh -r 220 "Faster with Josh"

# Force a specific provider
say --provider deepgram "Via Deepgram"

# Check what voice is set as default
say --show-config
```
