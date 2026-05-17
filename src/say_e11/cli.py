import argparse
import sys
from pathlib import Path

from say_e11.audio import play_pcm, write_wav
from say_e11.config import pick_provider
from say_e11.providers import build_provider


def _resolve_text(args: argparse.Namespace) -> str:
    if args.text:
        return " ".join(args.text)
    if args.file:
        try:
            return Path(args.file).read_text()
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
    parser.add_argument("-v", "--voice", metavar="NAME", help="Voice ID/name")
    parser.add_argument(
        "-r", "--rate", type=int, default=175, metavar="WPM",
        help="Speaking rate in words per minute (default: 175)",
    )
    parser.add_argument(
        "--provider", choices=["elevenlabs", "deepgram"], help="Force a provider",
    )
    args = parser.parse_args()

    text = _resolve_text(args).strip()
    if not text:
        print("Error: text is empty", file=sys.stderr)
        sys.exit(1)

    provider_name, key = pick_provider(args.provider)
    provider = build_provider(provider_name, key)

    try:
        pcm = provider.synthesize(text, args.voice, args.rate)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if args.output:
        write_wav(pcm, args.output)

    play_pcm(pcm)
