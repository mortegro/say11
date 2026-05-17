---
title: Configuration
nav_order: 4
---

# Configuration
{: .no_toc }

<details open markdown="block">
  <summary>Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Priority order

Settings are resolved in this order (highest to lowest priority):

1. **CLI flags** — `-v`, `-r`, `--provider` on the current invocation
2. **Process environment** — `ELEVENLABS_API_KEY` etc. already in the shell
3. **Local `.env`** — `.env` in the current working directory
4. **Home `.env`** — `~/.env`
5. **Saved defaults** — `~/.say-e11/config.json` set via `--set`
6. **Hardcoded defaults** — rate 175, Rachel voice, ElevenLabs first

---

## API keys

Create a `.env` file in your working directory or `~/.env` for a global
default. Both are gitignored automatically.

```bash
# ~/.env
ELEVENLABS_API_KEY=sk_...
DEEPGRAM_API_KEY=...
```

You can also export them in your shell profile:

```bash
# ~/.bashrc or ~/.zshrc
export ELEVENLABS_API_KEY=sk_...
```

### Provider auto-selection

When both keys are present, **ElevenLabs is used**. Override with:

```bash
say --set provider deepgram     # persist for all future calls
say --provider deepgram "once"  # override for one call
```

---

## Saved defaults

`--set` writes to `~/.say-e11/config.json`. The file is created automatically
on first use.

### Available settings

| Key | Values | Example |
|-----|--------|---------|
| `voice` | preset name or raw voice ID | `bella`, `EXAVITQu4vr4xnSDxMaL` |
| `provider` | `elevenlabs` or `deepgram` | `deepgram` |
| `rate` | integer (words per minute) | `200` |

### Setting defaults

```bash
say --set voice bella
say --set provider deepgram
say --set rate 150
```

### Viewing defaults

```bash
say --show-config
```

```
  voice = bella
  provider = elevenlabs
  rate = 150
```

### Editing the file directly

`~/.say-e11/config.json` is plain JSON:

```json
{
  "voice": "bella",
  "provider": "elevenlabs",
  "rate": 150
}
```

Edit it with any text editor. Unknown keys are silently ignored.

### Resetting defaults

Remove specific keys by editing the file, or delete it entirely:

```bash
rm ~/.say-e11/config.json
```

---

## Example: per-project setup

For a project that always uses Deepgram at a slower rate, create a `.env` in
the project root:

```bash
# myproject/.env
DEEPGRAM_API_KEY=...
```

And a project-local shell alias or script:

```bash
alias say='say --provider deepgram -r 150'
```
