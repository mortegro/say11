import argparse
import sys
from pathlib import Path

from say_e11.audio import play_pcm, write_wav
from say_e11.config import pick_provider
from say_e11.providers import build_provider
from say_e11.providers.elevenlabs import VOICE_PRESETS
from say_e11.settings import load as load_settings, save_key


def _resolve_text(args: argparse.Namespace) -> str:
    if args.text:
        return " ".join(args.text)
    if args.file:
        try:
            return Path(args.file).read_text(encoding="utf-8")
        except OSError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    print(
        "Error: no text provided. Pass text as arguments, use -f FILE, or pipe via stdin.",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="say",
        description="Text-to-speech CLI (ElevenLabs / Deepgram)",
    )
    parser.add_argument("text", nargs="*", help="Text to speak")
    parser.add_argument("-f", "--file", metavar="PATH", help="Read text from file")
    parser.add_argument("-o", "--output", metavar="PATH", help="Write audio to WAV file")
    parser.add_argument("-v", "--voice", metavar="NAME", help="Voice name or ID (overrides default)")
    parser.add_argument(
        "-r", "--rate", type=int, default=None, metavar="WPM",
        help="Speaking rate in words per minute (default: 175)",
    )
    parser.add_argument(
        "--provider", choices=["elevenlabs", "deepgram"], help="Force a provider",
    )
    parser.add_argument(
        "--set", nargs=2, metavar=("KEY", "VALUE"),
        help="Save a default setting: voice, provider, or rate",
    )
    parser.add_argument(
        "--list-voices", action="store_true",
        help="List available ElevenLabs voice presets",
    )
    parser.add_argument(
        "--show-config", action="store_true",
        help="Show current default settings",
    )
    args = parser.parse_args()

    # --- non-TTS commands ---
    if args.set:
        save_key(args.set[0], args.set[1])
        return

    if args.list_voices:
        print("ElevenLabs voice presets:")
        for name, vid in VOICE_PRESETS.items():
            print(f"  {name:<10} {vid}")
        return

    if args.show_config:
        cfg = load_settings()
        if not cfg:
            print("No defaults set. Use `say --set KEY VALUE` to configure.")
        else:
            for k, v in cfg.items():
                print(f"  {k} = {v}")
        return

    # --- apply saved defaults (CLI flags override) ---
    cfg = load_settings()
    effective_voice = args.voice or cfg.get("voice")
    effective_rate = args.rate if args.rate is not None else cfg.get("rate", 175)
    effective_provider = args.provider or cfg.get("provider")

    text = _resolve_text(args).strip()
    if not text:
        print("Error: text is empty", file=sys.stderr)
        sys.exit(1)

    provider_name, key = pick_provider(effective_provider)
    with build_provider(provider_name, key) as provider:
        try:
            pcm = provider.synthesize(text, effective_voice, effective_rate)
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

    if args.output:
        try:
            write_wav(pcm, args.output)
        except OSError as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)

    play_pcm(pcm)
