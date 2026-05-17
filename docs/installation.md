---
title: Installation
---

# Installation

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.11 or newer |
| [uv](https://docs.astral.sh/uv/) | any recent version |
| PortAudio | system package |
| API key | ElevenLabs **or** Deepgram |

## 1. Install PortAudio

`sounddevice` (the audio playback library) requires PortAudio to be present on
your system.

```bash
# Arch / Manjaro
sudo pacman -S portaudio

# Debian / Ubuntu / Raspberry Pi OS
sudo apt install libportaudio2

# Fedora
sudo dnf install portaudio

# macOS (Homebrew)
brew install portaudio
```

## 2. Install say-e11

### From GitHub (recommended)

```bash
uv tool install git+https://github.com/youruser/say-e11
```

### From a local clone

```bash
git clone https://github.com/youruser/say-e11
cd say-e11
uv tool install .
```

### Editable install for development

```bash
cd say-e11
uv sync               # install runtime + dev deps into .venv
uv tool install --editable .
```

## 3. Verify

```bash
say --help
```

Expected output:

```
usage: say [-h] [-f PATH] [-o PATH] [-v NAME] [-r WPM]
           [--provider {elevenlabs,deepgram}]
           [--set KEY VALUE] [--list-voices] [--show-config]
           [TEXT ...]

Text-to-speech CLI (ElevenLabs / Deepgram)
...
```

## Updating

```bash
uv tool upgrade say-e11
```

Or for a local clone:

```bash
git pull
uv tool install --editable .
```

## Uninstalling

```bash
uv tool uninstall say-e11
```

This removes the `say` executable. Your saved settings in `~/.say-e11/` are
left intact. Remove them manually if needed:

```bash
rm -rf ~/.say-e11
```
