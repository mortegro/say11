---
title: Voice Presets
---

# Voice Presets

## ElevenLabs presets

Use a preset name anywhere a voice is accepted: `-v NAME` or `--set voice NAME`.
Names are case-insensitive (`Rachel`, `rachel`, and `RACHEL` all work).

| Name | Voice ID | Character |
|------|----------|-----------|
| `rachel` *(default)* | `21m00Tcm4TlvDq8ikWAM` | Calm, American female |
| `bella` | `EXAVITQu4vr4xnSDxMaL` | Warm, American female |
| `domi` | `AZnzlk1XvdvUeBnXmlld` | Confident, American female |
| `elli` | `MF3mGyEYCl7XYWbV9V6O` | Young, American female |
| `adam` | `pNInz6obpgDQGcFmaJgB` | Deep, American male |
| `antoni` | `ErXwobaYiN019PkySvjV` | American male |
| `arnold` | `VR6AewLTigWG4xSOukaG` | Strong, American male |
| `josh` | `TxGEqnHWrfWFTfGW9XjX` | Young, American male |
| `sam` | `yoZ06aMxZJJ28mfd3POQ` | Energetic, American male |
| `dave` | `CYw3kZ78EXa7QGL7Umo` | British male |

```bash
say --list-voices    # print this table from the terminal
```

## Using a raw voice ID

If you have a custom voice or a voice not in the preset list, pass its ID
directly:

```bash
say -v EXAVITQu4vr4xnSDxMaL "Using Bella by ID"
say --set voice EXAVITQu4vr4xnSDxMaL
```

Any string that is not a recognized preset name is passed through as a raw ID.

## Deepgram voices

Deepgram voices are specified by model name. There are no named presets — pass
the model name directly with `-v`:

```bash
say --provider deepgram -v aura-2-orion-en "Using Orion"
say --provider deepgram -v aura-2-luna-en  "Using Luna"
```

The default Deepgram model is `aura-2-thalia-en`.

Refer to the
[Deepgram voice catalogue](https://developers.deepgram.com/docs/tts-models)
for a full list of available models.

## Setting a default voice

```bash
# By preset name
say --set voice bella

# By raw ID
say --set voice EXAVITQu4vr4xnSDxMaL

# Verify
say --show-config
```
