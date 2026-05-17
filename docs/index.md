---
title: Home
layout: home
nav_order: 1
---

# say-e11

{: .fs-6 .fw-300 }
A `uv`-installable CLI that brings macOS `say` to Linux, powered by
[ElevenLabs](https://elevenlabs.io) or [Deepgram](https://deepgram.com).

[Get started](#quick-start){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/youruser/say-e11){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What it does

`say-e11` reads text and speaks it aloud through your speakers — just like the
`say` command on macOS. It automatically picks whichever TTS provider you have
an API key for, with no extra configuration.

```bash
say "Hello, world"
echo "piped text" | say
say -v bella "Using a preset voice"
say -f script.txt
```

## Quick start

**1. Install PortAudio** (system dependency for audio playback)

```bash
# Arch / Manjaro
sudo pacman -S portaudio

# Debian / Ubuntu
sudo apt install libportaudio2
```

**2. Install say-e11**

```bash
uv tool install git+https://github.com/youruser/say-e11
```

**3. Add an API key**

```bash
# ~/.env  (or ./.env in your working directory)
ELEVENLABS_API_KEY=sk-...
# or
DEEPGRAM_API_KEY=...
```

**4. Speak**

```bash
say "It works"
```

---

## Key features

- **Drop-in `say` replacement** — same basic interface, works in existing scripts
- **Two providers** — ElevenLabs and Deepgram; auto-selected by available key
- **Voice presets** — `say -v rachel`, `say -v bella`, and 8 more named voices
- **Saved defaults** — `say --set voice bella` persists across sessions
- **WAV output** — `say -o out.wav "record this"` speaks *and* saves
- **Zero system deps beyond PortAudio** — pure Python, no ffmpeg
